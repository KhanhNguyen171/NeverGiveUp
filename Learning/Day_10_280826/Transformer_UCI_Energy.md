Với bài toán **UCI Appliances Energy Prediction** và mục tiêu dự báo ngắn hạn, **Transformer Encoder hoàn toàn có khả năng học temporal dependency có ích**, nhưng cần hiểu chính xác **nó học quan hệ thời gian nào** và **khi nào attention thực sự có giá trị**.

## 1. Đặt đúng bài toán

Với dữ liệu UCI lấy mẫu mỗi 10 phút, nếu dự báo:

$$
\hat{y}_{t+1}
=
f_\theta
\left(
\mathbf{x}_{t-L+1},\ldots,\mathbf{x}_t
\right)
$$

thì với:

$$
L=36
$$

Transformer nhận:

$$
\mathbf{X}_t\in\mathbb{R}^{36\times F}
$$

và cần học:

$$
\mathbf{X}_t
\longrightarrow
Appliances_{t+1}
$$

Đây là **short-term forecasting**: dự đoán 10 phút tiếp theo dựa trên vài giờ lịch sử.

Điểm cần nghiên cứu không phải đơn giản là:

> Transformer có attention hay không?

mà là:

> **Trong 36 timestep quá khứ, Transformer có học được những temporal dependencies có predictive value đối với $y_{t+1}$ hay không?**

---

# 2. Transformer Encoder thực sự nhìn thấy thời gian như thế nào?

Một timestep có dạng:

$$
\mathbf{x}_t
=
[x_t^{(1)},...,x_t^{(F)}]
$$

Ta embedding thành:

$$
\mathbf{z}_t
=
W_e\mathbf{x}_t+\mathbf{b}_e
$$

Sau đó cần positional information:

$$
\mathbf{h}_t^{(0)}
=
\mathbf{z}_t+\mathbf{p}_t
$$

Điều này rất quan trọng.

Nếu **không có positional encoding**, Transformer nhìn sequence gần giống một tập các vector:

$$
\{\mathbf{x}_{t-L+1},...,\mathbf{x}_t\}
$$

và không biết:

$$
x_{t-1}
$$

khác vị trí:

$$
x_{t-30}
$$

như thế nào.

Vì vậy với time series:

$$
\boxed{\text{Temporal order must be explicitly represented}}
$$

---

# 3. Self-Attention có thể học temporal dependency

Với:

$$
Q=HW_Q,\qquad
K=HW_K,\qquad
V=HW_V
$$

attention:

$$
A=
softmax
\left(
\frac{QK^\top}{\sqrt{d_k}}
\right)
$$

Trong đó:

$$
A\in\mathbb{R}^{L\times L}
$$

Với $L=36$:

$$
A\in\mathbb{R}^{36\times36}
$$

Phần tử:

$$
A_{ij}
$$

có thể hiểu trực quan là:

> Khi tạo representation cho timestep $i$, model đang sử dụng thông tin từ timestep $j$ với mức độ nào.

Ví dụ:

```text
t-35 t-34 ... t-12 t-11 ... t-3 t-2 t-1 t
  │    │         │          │   │   │  │
  └────┴─────────┴──────────┴───┴───┴──┘
                    Attention
                         ↓
                       t+1
```

Do đó Transformer **không bị giới hạn chỉ nhìn timestep liền trước** như một số cách xử lý tuần tự.

Nó có thể học quan hệ:

$$
x_t \leftrightarrow x_{t-1}
$$

nhưng đồng thời:

$$
x_t \leftrightarrow x_{t-6}
$$

hoặc:

$$
x_t \leftrightarrow x_{t-24}
$$

---

# 4. Với UCI, temporal relationship nào có khả năng hữu ích?

Đây mới là phần quan trọng.

Với sampling 10 phút:

| Lag | Khoảng thời gian |
| --: | ---------------: |
|   1 |          10 phút |
|   3 |          30 phút |
|   6 |            1 giờ |
|  12 |            2 giờ |
|  36 |            6 giờ |
|  72 |           12 giờ |
| 144 |           24 giờ |

Đối với dự báo Appliances Energy trong 10 phút tiếp theo, ta kỳ vọng tồn tại một số dạng dependency.

### Local dependency

$$
y_{t+1}
\leftarrow
x_t,x_{t-1},x_{t-2}
$$

Ví dụ thiết bị vừa tăng công suất thì khả năng tiếp tục duy trì trạng thái trong vài timestep tiếp theo.

Đây là dependency rất ngắn.

---

### Short-range dependency

Ví dụ:

$$
y_{t+1}
\leftarrow
x_{t-6:t}
$$

tức trạng thái trong khoảng 1 giờ gần đây.

---

### Daily periodic dependency

Nếu hành vi sử dụng năng lượng có chu kỳ ngày:

$$
y_{t+1}
\leftarrow
x_{t-144}
$$

vì:

$$
144\times10\text{ phút}=24\text{ giờ}
$$

Đây là một temporal relationship rất đáng quan tâm.

Nhưng có một nuance:

> **Attention không tự động có nghĩa là Transformer sẽ học được chu kỳ 24 giờ tốt.**

Nếu window chỉ:

$$
L=36
$$

thì model **không nhìn thấy $t-144$**.

Do đó:

$$
\boxed{
L=36
\Rightarrow
\text{không thể trực tiếp học dependency tại lag 144}
}
$$

Đây là lý do lookback là một hyperparameter có ý nghĩa về mặt **information availability**, không chỉ computational cost.

---

# 5. Đây là điểm rất quan trọng với bài UCI

Nếu mục tiêu là **short-term forecasting**, không nên mặc định:

> Transformer cần sequence rất dài.

Ví dụ:

$$
L=36
$$

cho phép model học:

$$
10\text{ phút}\rightarrow6\text{ giờ}
$$

nhưng không cho phép model trực tiếp học:

$$
24\text{ giờ}
$$

Nếu:

$$
L=144
$$

thì model mới có thể học:

$$
t-144\rightarrow t
$$

và phát hiện daily dependency.

Do đó có thể nghiên cứu:

$$
L\in\{36,72,144\}
$$

và xem:

$$
RMSE_{36},
RMSE_{72},
RMSE_{144}
$$

---

# 6. Transformer có lợi thế gì so với LSTM?

LSTM có dạng recurrence:

$$
h_t
=
LSTM(x_t,h_{t-1})
$$

Thông tin phải truyền qua chuỗi:

$$
x_{t-36}
\rightarrow
h_{t-35}
\rightarrow
\cdots
\rightarrow
h_t
$$

Trong Transformer:

$$
x_{t-36}
\leftrightarrow
x_t
$$

có thể tương tác trực tiếp thông qua attention.

Về **path length**, dependency giữa hai timestep có thể được mô hình hóa qua self-attention trong một bước attention.

Đây là ưu điểm lý thuyết quan trọng của Transformer:

$$
\boxed{
\text{Direct pairwise interaction across time}
}
$$

Tuy nhiên điều đó **không đồng nghĩa Transformer chắc chắn tốt hơn LSTM** trên UCI.

Dataset UCI chỉ khoảng vài chục nghìn observations, không phải dataset cực lớn. Transformer có nhiều tham số hơn và có thể không khai thác được lợi thế nếu temporal structure quá đơn giản.

---

# 7. Một câu hỏi quan trọng: attention có thực sự học "quan hệ thời gian"?

Có.

Nhưng nên nói chính xác:

> Transformer học **dependency giữa các token/timestep được biểu diễn trong sequence**, chứ không trực tiếp học khái niệm "thời gian" như con người.

Temporal understanding xuất hiện từ:

$$
\text{value}
+
\text{position}
+
\text{attention}
+
\text{feed-forward transformation}
$$

Tức:

$$
\boxed{
Temporal\ Dependency
=
Content + Position + Interaction
}
$$

---

# 8. Positional Encoding đặc biệt quan trọng

Nếu sử dụng sinusoidal positional encoding:

$$
PE_{(pos,2i)}
=
\sin
\left(
\frac{pos}{10000^{2i/d}}
\right)
$$

$$
PE_{(pos,2i+1)}
=
\cos
\left(
\frac{pos}{10000^{2i/d}}
\right)
$$

thì Transformer biết:

$$
pos=1
$$

khác:

$$
pos=30
$$

Nhưng với time series, còn một vấn đề:

**position trong window không hoàn toàn giống absolute time.**

Ví dụ:

```text
Window A:
08:00 → 13:50

Window B:
18:00 → 23:50
```

Cùng vị trí:

$$
pos=10
$$

nhưng giờ trong ngày hoàn toàn khác.

Do đó feature:

$$
hour_{sin},hour_{cos}
$$

có thể cung cấp thông tin temporal semantics mà positional encoding thuần túy không cung cấp.

Đây là lý do trong UCI, một representation hợp lý có thể là:

$$
X_t=
[
\text{sensor features},
hour_{sin},
hour_{cos},
dow_{sin},
dow_{cos},
weekend
]
$$

---

# 9. Transformer học được gì từ feature engineering?

Đây là điểm liên kết trực tiếp với câu hỏi trước của bạn.

Nếu chỉ đưa:

$$
hour=23
$$

model phải học rằng:

$$
23
\approx
0
$$

về mặt chu kỳ.

Trong khi:

$$
hour_{sin}=\sin(2\pi hour/24)
$$

$$
hour_{cos}=\cos(2\pi hour/24)
$$

đã biến đổi representation thành:

$$
23
\rightarrow
(\sin(23\cdot2\pi/24),
\cos(23\cdot2\pi/24))
$$

Hai thời điểm:

$$
23:00
\quad\text{và}\quad
00:00
$$

trở nên gần nhau trong không gian biểu diễn.

Do đó feature engineering có thể giúp Transformer:

$$
\boxed{
\text{dễ học temporal structure hơn}
}
$$

chứ không nhất thiết tạo thêm information mới.

---

# 10. Với short-term forecasting, dependency quan trọng nhất có thể không phải long-range attention

Đây là kết luận mình cho rằng rất quan trọng khi nghiên cứu UCI.

Nếu:

$$
y_{t+1}
$$

chủ yếu phụ thuộc vào:

$$
x_t,x_{t-1},x_{t-2},...
$$

thì Transformer không nhất thiết cần attention mạnh tới:

$$
x_{t-30}
$$

hoặc:

$$
x_{t-36}
$$

Model có thể học một dạng:

$$
\hat y_{t+1}
\approx
f(x_t,x_{t-1},x_{t-2},...)
$$

Khi đó lợi thế của Transformer về long-range dependency có thể **không phát huy nhiều**.

Đây chính là điều cần **kiểm chứng bằng experiment**, không nên giả định trước.

---

# 11. Thí nghiệm lý thuyết quan trọng nhất

Nếu mục tiêu của bạn là chứng minh Transformer thực sự học temporal relationship hữu ích, tôi sẽ làm:

### Experiment 1 — Shuffle temporal order

Giữ nguyên values nhưng xáo trộn thứ tự timestep:

$$
[x_{t-35},...,x_t]
\rightarrow
[x_{\pi(1)},...,x_{\pi(36)}]
$$

Nếu performance giảm mạnh:

$$
RMSE_{shuffle}\gg RMSE_{normal}
$$

thì đây là bằng chứng rằng **temporal ordering có predictive value**.

---

### Experiment 2 — Short vs long lookback

$$
L=36,72,144
$$

Nếu:

$$
RMSE_{36}
\approx
RMSE_{144}
$$

thì có khả năng short-term dependency đã đủ.

Nếu:

$$
RMSE_{144}<RMSE_{36}
$$

thì information ở khoảng xa hơn có ích.

---

### Experiment 3 — Remove temporal features

So sánh:

$$
X=
[\text{sensor}]
$$

với:

$$
X=
[\text{sensor},
hour_{sin},
hour_{cos},
dow_{sin},
dow_{cos}]
$$

Nếu performance cải thiện, calendar/time representation có predictive value.

---

### Experiment 4 — Compare against order-insensitive baseline

Một test rất thú vị:

```text
Transformer
      vs
MLP / pooling-based model
```

Nếu Transformer tốt hơn đáng kể khi cùng feature information, điều đó cung cấp bằng chứng rằng **sequence interaction** đang mang lại giá trị.

---

# 12. Kết luận cho UCI

Về lý thuyết:

$$
\boxed{
\text{Có, Transformer Encoder có thể học temporal dependencies hữu ích cho dự báo ngắn hạn.}
}
$$

Nhưng với UCI, cần tránh một kết luận quá mạnh rằng:

> "Transformer tốt vì nó học long-range temporal dependency."

Chưa chắc.

Câu hỏi đúng hơn là:

$$
\boxed{
\text{Predictive information của }y_{t+1}
\text{ nằm ở temporal scale nào?}
}
$$

Có thể nó nằm chủ yếu ở:

$$
\boxed{
t,\ t-1,\ t-2,\ldots
}
$$

thay vì:

$$
t-144.
$$

Vì vậy nghiên cứu Transformer trên UCI nên tập trung vào **temporal dependency characterization**:

```text
                 Transformer
                      │
             ┌────────┴────────┐
             ▼                 ▼
       Feature relation   Temporal relation
             │                 │
             │          ┌──────┼──────┐
             │          ▼      ▼      ▼
             │        local  short   daily
             │
             └──────────┬───────────┘
                        ▼
                  y(t + 1)
```

Và câu hỏi thực nghiệm cốt lõi sẽ là:

$$
\boxed{
\text{Which temporal information within the lookback window actually improves short-term forecasting?}
}
$$

Đây là hướng rất phù hợp để nối **feature selection → feature engineering → lookback selection → Transformer temporal learning → ablation study** thành một pipeline nghiên cứu thống nhất.
