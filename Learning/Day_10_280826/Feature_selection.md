Với **Transformer Regression cho time series**, một vấn đề rất quan trọng không chỉ là *“mô hình có đủ mạnh không?”* mà là:

> **Trong toàn bộ dữ liệu quan sát được, những thông tin nào thực sự cần thiết để dự đoán target ở tương lai?**

Đây có thể xem là bài toán **feature/data relevance** hoặc rộng hơn là **data necessity**.

### 1. Đặt bài toán

Giả sử ta có time series:

$$
\mathbf{x}_t =
[x_t^{(1)},x_t^{(2)},\ldots,x_t^{(F)}]
$$

và muốn dự đoán:

$$
\hat{y}_{t+H}
=
f_\theta
\left(
\mathbf{x}_{t-L+1},\ldots,\mathbf{x}_t
\right)
$$

Trong đó:

* $L$: lookback/window length.
* $H$: forecast horizon.
* $F$: số lượng feature.
* $y$: target cần regression.

Transformer nhận input:

$$
\mathbf{X}_t
\in
\mathbb{R}^{L\times F}
$$

Nhưng **không phải mọi feature trong $F$ đều đóng góp như nhau**.

Ví dụ:

```text
Temperature       ────────►
Humidity          ────────►
Hour              ────────► Transformer ───► Energy(t+1)
Day of week       ────────►
Random feature    ────────►
```

Có thể:

* Temperature rất quan trọng.
* Humidity có ích.
* Hour giúp mô hình nhận biết chu kỳ.
* Day of week có ích ít hơn.
* Random feature gần như không có thông tin.

Vấn đề nghiên cứu là xác định:

$$
\boxed{
\text{Feature nào thực sự mang information về } y_{t+H}?
}
$$

---

## 2. Cần phân biệt "có dữ liệu" và "dữ liệu cần thiết"

Một feature có thể tồn tại trong dataset nhưng **không nhất thiết cần thiết cho mô hình**.

Ta có thể chia thành:

| Loại           | Ý nghĩa                                          |
| -------------- | ------------------------------------------------ |
| **Essential**  | Bỏ đi làm performance giảm rõ rệt                |
| **Useful**     | Có đóng góp nhưng không quyết định               |
| **Redundant**  | Thông tin đã được feature khác cung cấp          |
| **Irrelevant** | Không giúp dự đoán target                        |
| **Leakage**    | Có vẻ rất hữu ích nhưng chứa thông tin tương lai |

Đặc biệt với time series, **data leakage** nguy hiểm hơn feature irrelevant.

Ví dụ:

$$
X_t \rightarrow y_{t+1}
$$

là hợp lệ.

Nhưng nếu một feature được tính từ:

$$
y_{t+1}
$$

thì Transformer có thể đạt kết quả cực tốt nhưng mô hình **không thể sử dụng feature đó trong thực tế**.

---

# 3. Transformer làm cho vấn đề này đặc biệt thú vị

Transformer sử dụng self-attention:

$$
\operatorname{Attention}(Q,K,V)
=
\operatorname{softmax}
\left(
\frac{QK^\top}{\sqrt{d_k}}
\right)V
$$

Với time series, attention giúp mô hình học:

> thời điểm nào trong quá khứ quan trọng đối với dự đoán hiện tại?

Ví dụ với:

$$
L=36
$$

tức 36 timestep quá khứ:

```text
t-35 t-34 ... t-12 t-11 ... t-3 t-2 t-1 t
 |    |          |           |   |   |  |
 └────┴──────────┴───────────┴───┴───┴──┘
                    Attention
                         ↓
                      y(t+1)
```

Nhưng có **hai chiều relevance khác nhau**:

### Temporal relevance

Thời điểm nào quan trọng?

$$
\text{Importance}(t-i)
$$

### Feature relevance

Feature nào quan trọng?

$$
\text{Importance}(f_j)
$$

Do đó ta thực chất muốn tìm:

$$
I(i,j)
=
\text{importance of feature }j
\text{ at timestep }t-i
$$

Đây mới là góc nhìn rất phù hợp khi nghiên cứu Transformer cho time series.

---

# 4. Không nên chỉ nhìn Attention để kết luận feature quan trọng

Đây là điểm rất quan trọng.

Một sai lầm phổ biến là:

> "Attention cao → feature quan trọng."

Không hoàn toàn đúng.

Attention cho biết mô hình **đang phân bổ attention như thế nào**, nhưng không nhất thiết phản ánh causal importance hay predictive importance.

Do đó nên kết hợp nhiều phương pháp.

### A. Ablation study

Đây là phương pháp rất trực tiếp.

Train:

$$
M_{\text{all}}
$$

với toàn bộ feature.

Sau đó bỏ feature $j$:

$$
M_{-j}
$$

và đo:

$$
\Delta RMSE_j
=
RMSE(M_{-j})-RMSE(M_{\text{all}})
$$

Nếu:

$$
\Delta RMSE_j \gg 0
$$

thì feature $j$ có khả năng quan trọng.

Ví dụ:

| Feature       | RMSE |
| ------------- | ---: |
| All           |   95 |
| − Temperature |  121 |
| − Humidity    |  101 |
| − Hour        |  108 |
| − Random 1    | 95.2 |

Ta có thể suy luận sơ bộ:

```text
Temperature  ███████████████
Hour         ███████
Humidity     ██
Random 1     .
```

---

# 5. Nhưng còn một vấn đề: redundancy

Giả sử:

$$
X_1 = Temperature
$$

và:

$$
X_2 = Temperature + \epsilon
$$

Hai feature chứa gần như cùng information.

Nếu bỏ $X_1$, mô hình vẫn hoạt động tốt vì $X_2$ có thể thay thế.

Khi đó:

$$
\Delta RMSE_{X_1}\approx 0
$$

nhưng không có nghĩa:

> Temperature không quan trọng.

Mà có thể là:

> **Information của Temperature vẫn cần thiết, nhưng feature representation bị dư thừa.**

Vì vậy nên có thêm **group ablation**.

Ví dụ:

```text
Temperature
Temperature-derived features
Weather features
Calendar features
Random controls
```

Sau đó:

$$
\Delta RMSE_{\mathcal{G}}
=
RMSE(M_{-\mathcal{G}})
-
RMSE(M_{\text{all}})
$$

---

# 6. Còn một câu hỏi quan trọng hơn: cần bao nhiêu lịch sử?

Đây là **data necessity theo temporal dimension**.

Giả sử thử:

$$
L\in\{6,12,24,36,72,144\}
$$

thì:

```text
L = 6
L = 12
L = 24
L = 36
L = 72
L = 144
```

Nếu:

```text
L=6    → RMSE 120
L=12   → RMSE 108
L=24   → RMSE 97
L=36   → RMSE 95
L=72   → RMSE 95
L=144  → RMSE 96
```

thì có thể kết luận:

> Information hữu ích chủ yếu nằm trong khoảng 36 timestep gần nhất.

Không cần mặc định rằng:

> **càng nhiều historical data → Transformer càng tốt.**

Window quá dài có thể:

* tăng computation;
* tăng noise;
* tăng số lượng irrelevant patterns;
* làm optimization khó hơn.

---

# 7. Vì vậy nên xem bài toán thành 3 câu hỏi

### Question 1 — Feature necessity

> **Feature nào cần thiết?**

$$
\mathcal{F}^{*}
\subseteq
\mathcal{F}
$$

---

### Question 2 — Temporal necessity

> **Cần bao nhiêu lịch sử?**

$$
L^{*}
=
\arg\min_L
\mathcal{L}_{val}(L)
$$

---

### Question 3 — Data quality necessity

> **Những observation nào thực sự đáng tin cậy?**

Ví dụ:

* missing values;
* duplicate timestamps;
* irregular intervals;
* outliers;
* corrupted measurements;
* sensor failures.

Một observation lỗi có thể khiến Transformer học pattern sai.

---

# 8. Một framework nghiên cứu khá tốt

Nếu bạn đang xây dựng Transformer Regression cho time series, mình sẽ tổ chức thí nghiệm theo pipeline:

```text
Raw Time Series
       │
       ▼
Data Quality Analysis
       │
       ├── Missing
       ├── Duplicate
       ├── Gap
       └── Outlier
       │
       ▼
Feature Groups
       │
       ├── Target history
       ├── Exogenous
       ├── Temporal
       ├── Metadata
       └── Random controls
       │
       ▼
Baseline Transformer
       │
       ▼
Feature Ablation
       │
       ▼
Group Ablation
       │
       ▼
Lookback Ablation
       │
       ▼
Temporal / Feature Importance
       │
       ▼
Minimal Sufficient Dataset
```

Khái niệm cuối cùng rất đáng chú ý:

$$
\boxed{
\text{Minimal Sufficient Dataset}
}
$$

Tức là:

> **Tập dữ liệu nhỏ nhất nhưng vẫn giữ được phần lớn predictive information cần thiết cho bài toán.**

---

## 9. Với bài toán Energy Forecasting

Nếu áp dụng trực tiếp vào bài toán Appliances Energy Prediction, có thể xây dựng:

$$
\mathbf{X}_t
=
[
\text{weather},
\text{indoor sensors},
\text{calendar},
\text{metadata},
\text{random controls}
]
$$

và target:

$$
y_{t+1}
=
Appliances_{t+1}
$$

Sau đó thực hiện:

### Experiment A — Feature ablation

```text
ALL
− weather
− indoor
− calendar
− metadata
− random
```

### Experiment B — Individual feature ablation

```text
− T1
− T2
− RH_1
− RH_2
− hour_sin
− hour_cos
...
```

### Experiment C — Lookback ablation

```text
L = 36
L = 72
L = 144
```

### Experiment D — Random-control test

Giữ:

```text
rv1
rv2
```

trong một experiment riêng.

Nếu:

$$
RMSE_{\text{with random}}
\approx
RMSE_{\text{without random}}
$$

thì đây là một **negative control** tốt: nó cho thấy pipeline không dễ dàng khai thác các biến không có predictive information.

---

# 10. Cách nhìn sâu hơn

Cuối cùng, vấn đề này không chỉ là:

> "Feature selection cho Transformer."

Mà có thể đặt thành một câu hỏi nghiên cứu rộng hơn:

$$
\boxed{
\text{How much historical information and which variables are actually necessary for accurate forecasting?}
}
$$

Tức nghiên cứu **information necessity** theo ba trục:

$$
\boxed{
\text{Feature}
\times
\text{Time}
\times
\text{Data Quality}
}
$$

Trong đó:

```text
                 Data
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
     Feature     Time     Quality
       │           │          │
       ▼           ▼          ▼
   What to use  How far    Which samples
               to look     to trust
```

Đây là hướng rất phù hợp để biến bài Transformer Regression của bạn từ một bài **“train một Transformer rồi báo RMSE”** thành một bài có tính **nghiên cứu thực nghiệm**: không chỉ chứng minh mô hình dự đoán tốt, mà còn chứng minh **tại sao lượng dữ liệu đó là đủ và thông tin nào thực sự tạo ra khả năng dự báo**.
