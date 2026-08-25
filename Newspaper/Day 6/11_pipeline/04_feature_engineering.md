# 11.4 Feature Engineering Pipeline

## 1. Mục tiêu

Feature engineering là giai đoạn chuyển dữ liệu đã được làm sạch và biến đổi thành các đặc trưng có khả năng biểu diễn những cấu trúc liên quan đến nhiệm vụ phân tích hoặc dự đoán.

Đối với time-series data, giá trị tại thời điểm $t$ thường không chứa đầy đủ thông tin cần thiết để mô hình hóa. Quan hệ giữa các quan sát theo thời gian, chu kỳ lặp lại, xu hướng cục bộ và trạng thái lịch sử có thể mang thông tin quan trọng hơn bản thân observation hiện tại.

Với dữ liệu sau transformation:

$$
\mathcal{D}_{transformed}=

\left \{
(t_i,\mathbf{x}_i)
\right \}_{i=1}^{N},
$$

feature engineering xây dựng:

$$
\mathbf{z}_t=

\Phi
\left(
t,\mathbf{x}_{1:t}
\right),
$$

trong đó $\Phi(\cdot)$ là feature-engineering mapping.

Trong phạm vi pipeline này, feature engineering tập trung vào bốn nhóm:

1. **temporal features**;
2. **lag features**;
3. **rolling features**;
4. **feature representation**.

Mục tiêu là tạo ra representation:

$$
\mathcal{D}_{feature}=

\left \{
(t_i,\mathbf{z}_i)
\right \}_{i=1}^{N'},
$$

có thể được sử dụng trực tiếp để xây dựng AI-ready data.

---

# 2. Vị trí của Feature Engineering trong Pipeline

Feature engineering được thực hiện sau data cleaning và transformation:

```text
Raw Time-Series Data
          │
          ▼
    Data Cleaning
          │
          ▼
 Data Transformation
          │
          ▼
┌──────────────────────────┐
│   Feature Engineering    │
│                          │
│  ├─ Temporal Features    │
│  ├─ Lag Features         │
│  ├─ Rolling Features     │
│  └─ Representation       │
└────────────┬─────────────┘
             │
             ▼
      Feature Validation
             │
             ▼
       AI-Ready Data
```

Các phép biến đổi trước đó chủ yếu thay đổi **quality hoặc numerical representation**, trong khi feature engineering tạo ra **new information representation** từ dữ liệu hiện có.

Có thể phân biệt:

$$
\text{Transformation}
:
\mathbf{x}_t
\rightarrow
f(\mathbf{x}_t),
$$

trong khi:

$$
\text{Feature Engineering}
:
{\mathbf{x}_{t-k}}_{k=0}^{L}
\rightarrow
\mathbf{z}_t.
$$

Do đó, feature engineering đặc biệt quan trọng đối với time series vì nó đưa temporal dependency trực tiếp vào input representation.

---

# 3. Feature Engineering Contract

Mỗi feature được tạo ra cần xác định rõ:

$$
F=
(
\text{name},
\text{source},
\text{formula},
\text{window},
\text{availability},
\text{output type}
).
$$

Ví dụ với lag feature:

$$
F_{lag}=

(
x_{t-1},
x_t,
1,
\text{past-only},
\text{numeric}
).
$$

Một feature hợp lệ phải thỏa mãn ba điều kiện:

1. có ý nghĩa đối với downstream task;
2. có thể tính toán từ thông tin available tại thời điểm dự đoán;
3. không tạo temporal leakage.

Do đó, feature engineering không nên được đánh giá theo số lượng feature tạo ra mà theo **information value và validity của feature**.

---

# 4. Temporal Features

## 4.1. Mục tiêu

Timestamp thường chứa thông tin định kỳ nhưng không thể đưa trực tiếp vào mô hình dưới dạng raw integer.

Ví dụ:

$$
hour \in {0,\ldots,23}.
$$

Nếu biểu diễn trực tiếp:

$$
hour=23
$$

và:

$$
hour=0,
$$

hai giá trị này có khoảng cách số học:

$$
|23-0|=23,
$$

trong khi trên chu kỳ 24 giờ chúng thực tế nằm cạnh nhau.

Do đó, temporal features cần biểu diễn cấu trúc tuần hoàn của thời gian.

---

## 4.2. Hour-of-day

Với:

$$
h_t\in{0,\ldots,23},
$$

có thể tạo:

$$
h_t^{sin}=

\sin
\left(
\frac{2\pi h_t}{24}
\right),
$$

và:

$$
h_t^{cos}=

\cos
\left(
\frac{2\pi h_t}{24}
\right).
$$

Hai feature này tạo representation liên tục của chu kỳ ngày.

---

## 4.3. Day-of-week

Với:

$$
d_t\in{0,\ldots,6},
$$

ta có:

$$
d_t^{sin}=

\sin
\left(
\frac{2\pi d_t}{7}
\right),
$$

$$
d_t^{cos}=

\cos
\left(
\frac{2\pi d_t}{7}
\right).
$$

Representation này cho phép mô hình nhận biết rằng:

$$
Sunday
\leftrightarrow
Monday
$$

có quan hệ gần nhau trong chu kỳ tuần.

---

## 4.4. Month-of-year

Với:

$$
m_t\in{1,\ldots,12},
$$

có thể tạo:

$$
m_t^{sin}=

\sin
\left(
\frac{2\pi m_t}{12}
\right),
$$

$$
m_t^{cos}=

\cos
\left(
\frac{2\pi m_t}{12}
\right).
$$

Các representation này đặc biệt hữu ích đối với dữ liệu có annual seasonality.

---

## 4.5. Weekend indicator

Một binary feature có thể được định nghĩa:

$$
weekend_t=

\begin{cases}
1,
& d_t\in{Saturday,Sunday},\\
0,
& \text{otherwise}.
\end{cases}
$$

Feature này không phải cyclic feature mà là categorical/binary indicator.

Do đó, không cần áp dụng sine/cosine transformation cho nó.

---

# 5. Lag Features

## 5.1. Mục tiêu

Lag feature biểu diễn giá trị lịch sử của một biến:

$$
x_t^{(k)}=

x_{t-k}.
$$

Với tập lag:

$$
\mathcal{L}=

{1,2,\ldots,K},
$$

vector lag có thể được viết:

$$
\mathbf{x}_t^{lag}=

[
x_{t-1},
x_{t-2},
\ldots,
x_{t-K}
].
$$

Lag features cho phép mô hình khai thác temporal dependency mà không cần tự học toàn bộ historical representation từ raw timestamp.

---

## 5.2. Lag theo sampling interval

Nếu dữ liệu được lấy mẫu với chu kỳ $\Delta t$, lag $k$ tương ứng với:

$$
\tau_k=k\Delta t.
$$

Ví dụ, nếu:

$$
\Delta t=10\text{ minutes},
$$

thì:

$$
x_{t-6}
$$

biểu diễn giá trị cách thời điểm hiện tại:

$$
6\times10=60\text{ minutes}.
$$

Do đó, lag selection nên dựa trên **temporal semantics**, không chỉ dựa trên số nguyên $k$.

---

## 5.3. Multi-scale lag features

Một tập lag có thể được chọn để biểu diễn nhiều temporal scales:

$$
\mathcal{L}=

{1,2,3,6,12,24,\ldots}.
$$

Các lag ngắn biểu diễn local dependency, trong khi lag dài có thể biểu diễn periodicity hoặc long-range dependency.

Ví dụ với dữ liệu hourly:

$$
x_{t-1}
\rightarrow
\text{1-hour history},
$$

$$
x_{t-24}
\rightarrow
\text{daily history},
$$

$$
x_{t-168}
\rightarrow
\text{weekly history}.
$$

Việc chọn lag phải dựa trên sampling frequency và domain characteristics.

---

# 6. Rolling Features

## 6.1. Mục tiêu

Lag features giữ lại từng observation lịch sử, trong khi rolling features tổng hợp nhiều observations thành các statistical descriptors.

Với cửa sổ có độ dài $w$:

$$
W_t^{(w)}=

{
x_{t-w+1},
\ldots,
x_t
}.
$$

Từ cửa sổ này có thể xây dựng nhiều features.

---

## 6.2. Rolling mean

Rolling mean:

$$
\mu_t^{(w)}=

\frac{1}{w}
\sum_{k=0}^{w-1}
x_{t-k}.
$$

Feature này biểu diễn local level của chuỗi.

---

## 6.3. Rolling standard deviation

Rolling standard deviation:

$$
\sigma_t^{(w)}=

\sqrt{
\frac{1}{w}
\sum_{k=0}^{w-1}
\left(
x_{t-k}-\mu_t^{(w)}
\right)^2
}.
$$

Nó biểu diễn mức độ biến động cục bộ.

---

## 6.4. Rolling minimum và maximum

Rolling minimum:

$$
x_{t,min}^{(w)}=

\min_{0\leq k<w}
x_{t-k}.
$$

Rolling maximum:

$$
x_{t,max}^{(w)}=

\max_{0\leq k<w}
x_{t-k}.
$$

Khoảng biến động có thể được biểu diễn:

$$
R_t^{(w)}= x_{t,max}^{(w)}

x_{t,min}^{(w)}.
$$

---

## 6.5. Rolling median

Rolling median:

$$
\tilde{x}_t^{(w)}=

\operatorname{median}
\left(
W_t^{(w)}
\right).
$$

Median ít nhạy với extreme values hơn mean và có thể hữu ích khi chuỗi chứa outlier còn sót lại sau cleaning.

---

# 7. Causal Rolling Features

Đối với forecasting, rolling feature phải được tính từ dữ liệu đã có tại thời điểm dự báo.

Rolling mean hợp lệ:

$$
\mu_t^{(w)}=

\frac{1}{w}
\sum_{k=0}^{w-1}
x_{t-k}.
$$

Ngược lại, centered rolling mean:

$$
\tilde{\mu}_t^{(w)}=

\frac{1}{2w+1}
\sum_{k=-w}^{w}
x_{t+k}
$$

sử dụng:

$$
x_{t+1},\ldots,x_{t+w},
$$

tức thông tin tương lai.

Trong forecasting pipeline:

$$
\boxed{
\text{Rolling Features}
\Rightarrow
\text{Past-only / Causal}
}
$$

trừ khi feature được xây dựng cho một nhiệm vụ không yêu cầu online prediction.

---

# 8. Multi-window Rolling Features

Một cửa sổ duy nhất có thể không đủ để biểu diễn nhiều temporal scales.

Có thể xây dựng:

$$
\mu_t^{(w_1)},
\qquad
\mu_t^{(w_2)},
\qquad
\mu_t^{(w_3)},
$$

với:

$$
w_1<w_2<w_3.
$$

Ví dụ:

```text
Short-term     Medium-term       Long-term
    │               │                │
    ▼               ▼                ▼
  w = 3           w = 12            w = 24
    │               │                │
    └───────────────┴────────────────┘
                    │
                    ▼
            Multi-scale features
```

Short windows phản ánh local fluctuations, trong khi long windows phản ánh broader temporal context.

Tuy nhiên, số lượng windows quá lớn có thể làm tăng feature dimensionality và redundancy.

---

# 9. Feature Representation

Feature engineering không chỉ tạo thêm feature mà còn quyết định **cách biểu diễn feature**.

Với một feature ban đầu:

$$
x_t,
$$

có thể tạo representation:

$$
\phi(x_t)=

[
x_t,
x_{t-1},
x_{t-2},
\mu_t^{(w)},
\sigma_t^{(w)}
].
$$

Do đó:

$$
\mathbf{z}_t=

\Phi(\mathbf{x}_{1:t})
$$

có thể chứa cả:

* current state;
* historical state;
* temporal context;
* local statistics;
* periodic information.

---

# 10. Window-based Representation

Đối với deep learning trên time series, một cách biểu diễn phổ biến là sequence window.

Với lookback $L$:

$$
\mathbf{X}_{t-L+1:t}=

\begin{bmatrix}
\mathbf{x}_{t-L+1}\\
\mathbf{x}_{t-L+2}\\
\vdots\\
\mathbf{x}_{t}
\end{bmatrix}
\in
\mathbb{R}^{L\times d}.
$$

Target forecasting có thể được xác định:

$$
y_{t+H},
$$

với $H$ là forecasting horizon.

Tập supervised samples:

$$
\mathcal{D}_{seq}=

\left \{
\left(
\mathbf{X}*{t-L+1:t},
y*{t+H}
\right)
\right \}.
$$

Representation này phù hợp với các mô hình như:

* RNN;
* LSTM;
* GRU;
* Temporal CNN;
* Transformer-based time-series models.

Điểm quan trọng là feature engineering và sequence construction có thể là hai bước khác nhau:

$$
\text{Feature Engineering}
\rightarrow
\text{Sequence Construction}.
$$

Feature engineering xác định feature vector $\mathbf{x}_t$, còn sequence construction xác định cách các vectors được tổ chức thành input tensor.

---

# 11. Feature Interaction

Một số thông tin chỉ xuất hiện khi kết hợp nhiều features.

Ví dụ:

$$
x_t^{interaction}=

x_t^{(1)}
\cdot
x_t^{(2)}.
$$

Hoặc một feature có thể được điều kiện hóa theo temporal context:

$$
z_t=

f
\left(
x_t,
hour_t,
day_t
\right).
$$

Tuy nhiên, feature interaction làm tăng dimensionality và có thể dẫn đến redundancy.

Do đó, interaction features chỉ nên được tạo khi:

* có cơ sở domain;
* có ý nghĩa thống kê;
* hoặc có giả thuyết rõ ràng về quan hệ giữa các variables.

---

# 12. Feature Engineering và Leakage

Feature engineering là một trong những nguồn temporal leakage phổ biến nhất.

Giả sử mục tiêu là dự đoán:

$$
y_{t+1}.
$$

Feature tại $t$ chỉ được phép sử dụng:

$$
\mathcal{I}_t=

{
x_\tau:\tau\leq t
}.
$$

Do đó:

$$
z_t=

f(\mathcal{I}_t).
$$

Không được sử dụng:

$$
x_{t+1},
x_{t+2},\ldots
$$

khi chúng không có sẵn tại thời điểm prediction.

Ví dụ không hợp lệ:

$$
z_t=

\operatorname{mean}
(x_{t-2},x_{t-1},x_t,x_{t+1}),
$$

vì $x_{t+1}$ chính là future information.

Do đó:

$$
\boxed{
\text{Feature availability}
\leq
\text{Prediction time}
}
$$

là nguyên tắc bắt buộc đối với forecasting pipeline.

---

# 13. Feature Engineering và Train/Test Split

Chronological split phải được thực hiện cẩn thận.

Với:

$$
\mathcal{D}=

\mathcal{D}_{train}
\cup
\mathcal{D}_{val}
\cup
\mathcal{D}_{test},
$$

cần duy trì:

$$
t_{train}
\lt
t_{val}
\lt
t_{test}.
$$

Lag và rolling features có thể cần historical observations từ trước boundary của một split.

Ví dụ, để tạo:

$$
x_{t-24},
$$

cho observation đầu tiên của validation, cần observation từ training period.

Điều này không nhất thiết là leakage nếu feature chỉ sử dụng **quá khứ thực sự có sẵn tại thời điểm validation prediction**.

Ngược lại, không được sử dụng bất kỳ observation nào thuộc tương lai của timestamp đang được dự đoán.

---

# 14. Feature Availability

Mỗi feature cần có một availability rule.

Có thể phân loại:

| Feature              | Availability                          |
| -------------------- | ------------------------------------- |
| Current sensor value | $t$                                   |
| Lag-1                | $t-1$                                 |
| Lag-$k$              | $t-k$                                 |
| Rolling mean         | $[t-w+1,t]$                           |
| Hour-of-day          | timestamp $t$                         |
| Day-of-week          | timestamp $t$                         |
| Future target        | $t+H$ — **không được dùng làm input** |

Target:

$$
y_{t+H}
$$

chỉ tồn tại ở label side, không được đưa vào feature computation nếu nó chưa available tại prediction time.

---

# 15. Feature Validation

Sau khi tạo features, cần kiểm tra:

## 15.1. Shape

Nếu có $N$ observations và $d'$ features:

$$
\mathbf{X}
\in
\mathbb{R}^{N\times d'}.
$$

Đối với sequence representation:

$$
\mathbf{X}
\in
\mathbb{R}^{B\times L\times d'},
$$

với:

* $B$: batch size;
* $L$: lookback;
* $d'$: feature dimension.

---

## 15.2. Missingness

Lag và rolling operations có thể tạo missing values ở đầu chuỗi.

Ví dụ với lag $k$:

$$
x_1,\ldots,x_k
$$

không có đầy đủ historical observations.

Tương tự, rolling window $w$ tạo ra tối đa:

$$
w-1
$$

observations không đủ history nếu không sử dụng partial windows.

Pipeline phải xác định rõ:

* drop incomplete rows;
* padding;
* minimum periods;
* hoặc giữ missing values để xử lý ở bước khác.

---

## 15.3. Temporal alignment

Đối với mỗi sample:

$$
(\mathbf{X}_{t-L+1:t},y_{t+H}),
$$

cần xác minh rằng input và target được căn chỉnh đúng.

Điều kiện:

$$
\max(\mathbf{X}_{t-L+1:t})
\leq t
\lt
t+H.
$$

Nói cách khác, input không được chứa observation sau thời điểm dự báo.

---

# 16. Feature Redundancy

Feature engineering có thể nhanh chóng làm tăng dimensionality.

Nếu tạo:

* $d$ original features;
* $K$ lag features;
* $W$ rolling statistics;
* $C$ temporal features;

thì feature dimension có thể tăng gần:

$$
d'
\approx
d+K+W+C.
$$

Nếu áp dụng nhiều combinations:

$$
d'\gg d.
$$

Dimensionality cao có thể dẫn đến:

* computational cost;
* memory cost;
* multicollinearity;
* overfitting;
* feature redundancy.

Do đó, feature engineering phải kết hợp với **feature selection** được trình bày trong Chương 6.

Quan hệ:

$$
\boxed{
\text{Feature Engineering}
\rightarrow
\text{Feature Selection}
}
$$

là một phần quan trọng của preprocessing workflow.

---

# 17. Feature Engineering Pipeline hoàn chỉnh

Một pipeline có thể được tổ chức:

```text
Transformed Data
       │
       ▼
Temporal Feature Generation
       │
       ▼
Lag Feature Generation
       │
       ▼
Rolling Feature Generation
       │
       ▼
Feature Representation
       │
       ▼
Temporal Alignment
       │
       ▼
Feature Validation
       │
       ▼
Feature Matrix
       │
       ▼
Sequence / Model Input Construction
```

Tương ứng về mặt toán học:

$$
\mathbf{x}_t
\xrightarrow{\Phi_{temp}}
\mathbf{x}_t^{temp}
\xrightarrow{\Phi_{lag}}
\mathbf{x}_t^{lag}
\xrightarrow{\Phi_{roll}}
\mathbf{x}_t^{roll}
\xrightarrow{\Phi_{repr}}
\mathbf{z}_t.
$$

Cuối cùng:

$$
\mathcal{D}_{feature}=

\left \{
(t,\mathbf{z}_t)
\right \}.
$$

---

# 18. Selection Strategy

Feature engineering nên được thực hiện theo một chiến lược có kiểm soát:

$$
\boxed{
\text{Domain Knowledge}
\rightarrow
\text{Candidate Features}
\rightarrow
\text{Validation}
\rightarrow
\text{Selection}
}
$$

### Bước 1 — Domain knowledge

Xác định các temporal patterns có khả năng liên quan đến target.

### Bước 2 — Candidate features

Tạo một tập feature vừa đủ để kiểm tra hypothesis.

### Bước 3 — Validation

Đánh giá:

* correlation;
* temporal relevance;
* predictive utility;
* redundancy;
* computational cost.

### Bước 4 — Selection

Loại bỏ features không cần thiết bằng các phương pháp được trình bày trong **Chương 6 — Feature Selection**.

Feature engineering vì vậy không phải quá trình tối đa hóa số lượng features, mà là quá trình xây dựng **compact and informative representation**.

---

# 19. Feature Engineering trong Edge/IoT

Trong Edge/IoT, feature engineering có vai trò đặc biệt vì truyền raw sensor data liên tục lên cloud có thể tạo ra bandwidth và latency overhead.

Thay vì:

```text
Sensor
  │
  │ raw stream
  ▼
Cloud
  │
  ▼
Feature Engineering
```

có thể thực hiện:

```text
Sensor
  │
  ▼
Edge Node
  ├── temporal features
  ├── lag statistics
  └── rolling statistics
  │
  ▼
Compact Feature Stream
  │
  ▼
Cloud / AI Service
```

Nếu raw data có $d$ dimensions và sampling rate $r$, data transmission rate có thể tăng đáng kể theo:

$$
R_{raw}
\propto
d\times r.
$$

Feature engineering tại edge có thể giảm lượng dữ liệu cần truyền nếu nhiều raw measurements được tổng hợp thành một representation nhỏ hơn.

Tuy nhiên, việc đưa computation xuống edge làm tăng:

* CPU usage;
* memory usage;
* energy consumption;
* implementation complexity.

Do đó:

$$
\text{Edge Feature Engineering}=

\text{Information Reduction}
+
\text{Local Computation}.
$$

Lựa chọn vị trí thực hiện feature engineering phải dựa trên trade-off giữa bandwidth, latency, energy và predictive performance.

---

# 20. AI-Ready Feature Representation

Sau feature engineering, dữ liệu có thể được biểu diễn:

$$
\mathbf{Z}=

\begin{bmatrix}
\mathbf{z}_1\
\mathbf{z}_2\
\vdots\
\mathbf{z}_N
\end{bmatrix}
\in
\mathbb{R}^{N\times d'}.
$$

Đối với sequence model:

$$
\mathcal{X}
\in
\mathbb{R}^{B\times L\times d'}.
$$

Representation này cần thỏa mãn:

1. feature semantics rõ ràng;
2. temporal alignment chính xác;
3. không chứa future information;
4. dimensionality được kiểm soát;
5. numerical values hợp lệ;
6. tương thích với input requirements của model.

Khi các điều kiện này được thỏa mãn, feature matrix có thể chuyển sang bước cuối cùng của pipeline:

$$
\boxed{
\mathcal{D}*{feature}
\rightarrow
\mathcal{D}*{AI-ready}
}
$$

---

# 21. Tóm tắt

Feature Engineering Pipeline chuyển dữ liệu đã được cleaning và transformation thành representation có khả năng biểu diễn temporal information:

$$
\boxed{
\text{Temporal}
+
\text{Lag}
+
\text{Rolling}
+
\text{Representation}
}
$$

Trong đó:

* **Temporal features** biểu diễn các đặc tính theo lịch và chu kỳ;
* **Lag features** biểu diễn historical dependencies;
* **Rolling features** biểu diễn local statistics và temporal dynamics;
* **Feature representation** tổ chức các features thành dạng phù hợp với downstream model.

Nguyên tắc thiết kế pipeline có thể tóm tắt:

$$
\boxed{
\text{Generate}
\rightarrow
\text{Align}
\rightarrow
\text{Validate}
\rightarrow
\text{Select}
\rightarrow
\text{Represent}
}
$$

Đặc biệt, mọi feature dùng cho forecasting phải thỏa mãn điều kiện causal:

$$
\mathbf{z}_t=

f
\left(
\mathbf{x}_{\tau}
:
\tau\leq t
\right).
$$

Điều này bảo đảm feature representation phản ánh đúng thông tin có thể quan sát tại thời điểm dự báo và ngăn temporal leakage.

Feature Engineering Pipeline do đó là bước cuối cùng trước khi dữ liệu được chuyển thành **AI-ready representation**, tạo cầu nối trực tiếp giữa preprocessing và model training.

### Tài liệu tham khảo chính

Tawakuli, A., Havers, B., Gulisano, V. M., Kaiser, D., & Engel, T. (2025). *Survey: Time-Series Data Preprocessing: A Survey and an Empirical Analysis*. **Journal of Engineering Research, 13**(2), 674–711. DOI: 10.1016/j.jer.2024.02.018. Nghiên cứu cung cấp taxonomy và empirical analysis về preprocessing numerical time series, làm cơ sở cho việc tổ chức các bước xây dựng temporal representation trong pipeline này.

[ScienceDirect — bài báo gốc](https://www.sciencedirect.com/science/article/pii/S2307187724000452?utm_source=chatgpt.com)
