# 03. Rolling Features

## 1. Vị trí của Rolling Features trong Chapter 5

Ở `01_temporal_features.md`, chúng ta xác định rằng **Time-Series Data chứa information theo thời gian**, vì vậy thứ tự của các observation không thể bị xem như thứ tự tùy ý.

Tiếp theo, trong `02_lag_features.md`, temporal dependency được đưa trực tiếp vào feature representation thông qua các giá trị quá khứ:

$$
x_{t-k}
$$

Lag Feature trả lời câu hỏi:

> **Tại một thời điểm trước đó, giá trị của biến là bao nhiêu?**

Rolling Features đi thêm một bước:

> **Trong một khoảng thời gian gần đây, đặc điểm của dữ liệu là gì?**

Do đó cấu trúc của Chapter 5 được liên kết như sau:

```text
05_feature_engineering/
│
├── 01_temporal_features.md
│   └── Temporal structure
│
├── 02_lag_features.md
│   └── Historical point
│
├── 03_rolling_features.md
│   └── Historical window
│
└── 04_feature_representation.md
    └── Final representation
```

Logic:

```text
Temporal Structure
        ↓
Historical Dependency
        ↓
Lag Features
        ↓
Temporal Window
        ↓
Rolling Features
        ↓
Feature Representation
```

Vì vậy `03_rolling_features.md` không phải một topic độc lập. Nó tiếp tục trực tiếp từ Lag Features và chuẩn bị cho phần **Feature Representation** ở file tiếp theo.

---

# 2. Lưu ý về phạm vi của Paper

Paper *Survey: Time-Series Data Preprocessing: A Survey and an Empirical Analysis* xây dựng một taxonomy rộng cho preprocessing của **numerical time-series data**. Tác giả không giới hạn preprocessing vào data cleaning mà mở rộng sang các nhóm như feature engineering, sensor fusion và data compression. Paper cũng thực hiện empirical analysis để đánh giá tác động của preprocessing lên data quality và AI performance. ([research.chalmers.se][1])

Tuy nhiên, **Rolling Features không phải là một thuật toán hoặc contribution riêng được tác giả đề xuất trong paper**.

Do đó cần phân biệt:

```text
Paper
    ↓
Khung tổng quát về Time-Series Data Preprocessing
```

với:

```text
Chapter 5 của tài liệu học
    ↓
Triển khai sâu các khái niệm Feature Engineering
    ↓
Temporal Features
    ↓
Lag Features
    ↓
Rolling Features
    ↓
Feature Representation
```

Rolling Features trong file này được trình bày như **kiến thức feature engineering cần thiết để hiểu temporal representation**, đồng thời được đặt trong phạm vi rộng hơn về preprocessing mà survey xây dựng.

Không được ghi:

> "Tác giả Tawakuli et al. đề xuất Rolling Features."

---

# 3. Rolling Feature là gì?

Rolling Feature được tạo bằng cách áp dụng một phép toán trên một **cửa sổ thời gian trượt**.

Cho time series:

$$
X={x_1,x_2,\ldots,x_t,\ldots,x_T}
$$

với window size (w), rolling window tại thời điểm (t) có thể được biểu diễn:

$$
W_t=
{x_{t-w+1},\ldots,x_{t-1},x_t}
$$

Sau đó áp dụng một hàm:

$$
z_t=f(W_t)
$$

để tạo ra một feature mới.

Ví dụ:

$$
z_t=
\frac{1}{w}
\sum_{i=0}^{w-1}x_{t-i}
$$

thì (z_t) chính là **rolling mean**.

---

# 4. Từ Lag Feature đến Rolling Feature

Đây là mối liên kết quan trọng nhất giữa file `02_lag_features.md` và file hiện tại.

Trong Lag Features:

$$
Lag_k=x_{t-k}
$$

chúng ta lấy **một observation trong quá khứ**.

Trong Rolling Features:

$$
W_t=
{x_{t-w+1},\ldots,x_t}
$$

chúng ta lấy **một tập observation trong quá khứ/gần hiện tại**.

So sánh:

```text
Lag Feature

x(t-3)
  │
  ▼
Một historical value
```

và:

```text
Rolling Feature

x(t-3) x(t-2) x(t-1) x(t)
   │      │      │      │
   └──────┴──────┴──────┘
             │
             ▼
       Aggregation
             │
             ▼
      Rolling Feature
```

Do đó:

$$
\boxed{
Lag = Historical\ Point
}
$$

trong khi:

$$
\boxed{
Rolling = Historical\ Window
}
$$

---

# 5. Vì sao cần Rolling Features?

Một giá trị đơn lẻ có thể không đại diện tốt cho trạng thái gần đây của hệ thống.

Ví dụ:

```text
Temperature:

10
11
12
13
30
```

Nếu chỉ sử dụng:

$$
x_t=30
$$

model biết giá trị hiện tại rất cao nhưng không trực tiếp biết:

* mức trung bình gần đây;
* mức dao động;
* xu hướng local;
* độ biến thiên;
* giá trị cực đại/cực tiểu gần đây.

Rolling Features cho phép tóm tắt một khoảng temporal context:

```text
Historical Window
       ↓
┌─────────────────────┐
│ x(t-4) ... x(t)     │
└──────────┬──────────┘
           ↓
     Statistical Summary
           ↓
      Rolling Feature
```

Do đó rolling feature chuyển:

$$
\text{Multiple Historical Observations}
$$

thành:

$$
\text{Compact Temporal Representation}
$$

---

# 6. Rolling Mean

Một trong những rolling features cơ bản nhất là rolling mean.

Với window (w):

$$
\mu_t^{(w)}
 = \frac{1}{w}

\sum_{i=0}^{w-1}x_{t-i}
$$

Ví dụ:

```text
Time:       t1   t2   t3   t4   t5
Value:      10   12   14   16   20
```

Với:

$$
w=3
$$

tại (t_5):

$$
\mu_5^{(3)}
 = \frac{14+16+20}{3}

\approx 15.33
$$

Khi thời gian dịch chuyển:

```text
t1 t2 t3
   ↓
   t2 t3 t4
       ↓
       t3 t4 t5
```

window liên tục trượt về phía trước.

---

# 7. Rolling Standard Deviation

Rolling Mean mô tả **mức trung tâm** của local window.

Rolling Standard Deviation mô tả **mức độ biến động**.

Có thể tính:

$$
\sigma_t^{(w)}
 =

\sqrt{
\frac{1}{w}
\sum_{i=0}^{w-1}
(x_{t-i}-\mu_t^{(w)})^2
}
$$

Ví dụ:

```text
Window A:

10 11 10
```

có độ biến động nhỏ.

Trong khi:

```text
Window B:

5 15 10
```

có độ biến động lớn hơn.

Hai window có thể có mean tương tự nhưng volatility khác nhau.

Do đó:

```text
Rolling Mean
     ↓
Local Level

Rolling Std
     ↓
Local Variability
```

---

# 8. Rolling Min và Rolling Max

Có thể lấy:

$$
Min_t^{(w)}=

\min
{x_{t-w+1},...,x_t}
$$

và:

$$
Max_t^{(w)}=

\max
{x_{t-w+1},...,x_t}
$$

Các feature này mô tả phạm vi hoạt động của signal trong một khoảng thời gian.

Ví dụ:

```text
Window:

10 12 15 13 11
```

thì:

$$
Min=10
$$

và:

$$
Max=15
$$

Có thể sử dụng:

$$
Range_t^{(w)}=

Max_t^{(w)}-Min_t^{(w)}
$$

để mô tả biên độ biến động.

---

# 9. Rolling Sum

Đối với những đại lượng có ý nghĩa cộng dồn, rolling sum có thể hữu ích:

$$
S_t^{(w)}=

\sum_{i=0}^{w-1}x_{t-i}
$$

Ví dụ với energy consumption:

```text
10
12
15
```

rolling sum trong 3 bước:

$$
10+12+15=37
$$

Khác với rolling mean:

$$
\frac{10+12+15}{3}=12.33
$$

Ý nghĩa của hai feature hoàn toàn khác nhau.

* Rolling mean → mức trung bình.
* Rolling sum → tổng lượng trong window.

Vì vậy phép aggregation phải phù hợp với semantics của feature.

---

# 10. Rolling Median

Có thể sử dụng median thay vì mean:

$$
m_t^{(w)}=

\operatorname{median}
(
x_{t-w+1},...,x_t
)
$$

Rolling median có thể robust hơn rolling mean khi window chứa extreme values.

Ví dụ:

```text
Window:

10 11 100
```

Mean:

$$
40.33
$$

Median:

$$
11
$$

Điều này cho thấy rolling median ít bị kéo mạnh bởi một extreme observation.

Tuy nhiên cần phân biệt:

> Rolling Median là một cách tổng hợp local window; nó không tự động giải quyết outlier detection.

Outlier detection thuộc Chapter 3.

---

# 11. Rolling Quantiles

Có thể mở rộng rolling statistics thành quantiles.

Ví dụ:

$$
Q_{0.25,t}^{(w)}
$$

là percentile 25% trong window.

Tương tự:

$$
Q_{0.75,t}^{(w)}
$$

là percentile 75%.

Từ đó có thể tạo:

$$
IQR_t^{(w)} = Q_{0.75,t}^{(w)} - Q_{0.25,t}^{(w)}

$$

Đây là một ví dụ cho thấy rolling representation có thể kết nối với các khái niệm Data Cleaning đã học ở Chapter 3.

Tuy nhiên:

```text
Chapter 3
→ dùng IQR để phát hiện outlier

Chapter 5
→ rolling IQR có thể được dùng như một feature mô tả local variability
```

Mục tiêu của hai trường hợp khác nhau.

---

# 12. Rolling Window và Local Context

Một trong những giá trị quan trọng nhất của rolling features là **local context**.

Global statistics:

$$
\mu(X)
$$

mô tả toàn bộ dataset.

Rolling statistics:

$$
\mu_t^{(w)}
$$

chỉ mô tả một vùng lân cận tại thời điểm (t).

So sánh:

```text
Global

Entire Time Series
────────────────────────────
        ↓
      One Mean
```

với:

```text
Rolling

────── Window 1 ──────
        ↓
      Mean 1

       ────── Window 2 ──────
               ↓
             Mean 2

              ────── Window 3 ──────
                      ↓
                    Mean 3
```

Vì vậy rolling features có khả năng biểu diễn **local dynamics** tốt hơn global statistics.

---

# 13. Window Size là Hyperparameter quan trọng

Window size (w) quyết định temporal context được sử dụng.

### Window nhỏ

$$
w\downarrow
$$

thì feature phản ứng nhanh với biến động:

```text
Small Window
     ↓
Local behavior
     ↓
High responsiveness
```

nhưng statistic có thể nhiễu hơn.

### Window lớn

$$
w\uparrow
$$

thì feature ổn định hơn:

```text
Large Window
     ↓
Longer context
     ↓
More smoothing
```

nhưng có thể làm mất các biến động ngắn hạn.

Do đó:

$$
\boxed{
Window\ Size
\rightarrow
Temporal\ Resolution
}
$$

không phải chỉ là một tham số kỹ thuật.

---

# 14. Rolling Features và Multi-Scale Representation

Một time series có thể có nhiều temporal scales:

```text
Short-term
    ↓
minutes / hours

Medium-term
    ↓
days

Long-term
    ↓
weeks / months
```

Có thể sử dụng nhiều window:

$$
w_1<w_2<w_3
$$

Ví dụ:

```text
Rolling Mean 3
Rolling Mean 12
Rolling Mean 24
```

Mỗi feature đại diện cho một temporal scale khác nhau.

Có thể hình dung:

```text
Signal
│
├── Window 3
│      ↓
│   Short-term
│
├── Window 12
│      ↓
│   Medium-term
│
└── Window 24
       ↓
    Longer-term
```

Điều này giúp representation chứa nhiều mức temporal context.

Nhưng đồng thời:

$$
Number\ of\ Features\uparrow
$$

và computational cost tăng.

---

# 15. Rolling Features và Trend

Rolling statistics có thể hỗ trợ biểu diễn local trend.

Ví dụ có hai rolling means:

$$
\mu_t^{(w)}
$$

và:

$$
\mu_{t-w}^{(w)}
$$

Có thể xem sự thay đổi:

$$
\Delta\mu_t = \mu_t^{(w)} - \mu_{t-w}^{(w)}

$$

Nếu:

$$
\Delta\mu_t>0
$$

local level đang tăng.

Nếu:

$$
\Delta\mu_t<0
$$

local level đang giảm.

Đây là một ví dụ về cách feature engineering biến temporal history thành một representation có ý nghĩa hơn.

---

# 16. Rolling Features không phải là Smoothing

Rolling Mean có thể được sử dụng như một **smoothed signal**, nhưng trong Feature Engineering hai khái niệm cần phân biệt.

### Chapter 3 — Noise Reduction

Mục tiêu:

$$
x_t
\rightarrow
\hat{x}_t
$$

để giảm noise.

### Chapter 5 — Rolling Feature

Mục tiêu:

$$
x_t
\rightarrow
z_t
$$

để tạo thêm information cho model.

Pipeline khác nhau:

```text
Noise Reduction:

Raw
 ↓
Denoising
 ↓
Clean Signal
 ↓
Model
```

trong khi:

```text
Feature Engineering:

Raw / Clean Signal
 ↓
Rolling Statistic
 ↓
New Feature
 ↓
Model
```

Vì vậy không nên đánh đồng:

> Rolling Mean = Noise Reduction.

Nó có thể tạo ra một representation smooth hơn, nhưng mục đích của rolling feature trong feature engineering là **tạo thêm feature**.

---

# 17. Rolling Features và Lag Features

Hai loại feature này nên được sử dụng cùng nhau khi cần biểu diễn cả **specific history** và **local summary**.

Ví dụ:

```text
Current:
x_t

Lag:
x_(t-1)
x_(t-2)
x_(t-3)

Rolling:
mean_(t-2:t)
std_(t-2:t)
max_(t-2:t)
```

Representation:

$$
Z_t=
[
x_t,
x_{t-1},
x_{t-2},
x_{t-3},
\mu_t^{(3)},
\sigma_t^{(3)},
max_t^{(3)}
]
$$

Lag trả lời:

> **Các giá trị cụ thể trong quá khứ là gì?**

Rolling trả lời:

> **Đặc tính tổng quát của khoảng quá khứ là gì?**

Đây là lý do `03_rolling_features.md` phải nối trực tiếp với `02_lag_features.md`.

---

# 18. Rolling Features và Feature Representation

Sau khi tạo:

```text
Current Features
        +
Lag Features
        +
Rolling Features
```

ta có một feature space lớn hơn.

Ví dụ:

```text
Original
[x1, x2]

      ↓

Lag
[x1_lag1, x1_lag2,
 x2_lag1, x2_lag2]

      ↓

Rolling
[x1_mean, x1_std,
 x2_mean, x2_std]
```

Tất cả phải được tổ chức thành representation cuối:

$$
Z_t=
[
X_t,
Lag_t,
Rolling_t
]
$$

Đây chính là cầu nối sang:

```text
04_feature_representation.md
```

File tiếp theo sẽ trả lời:

> **Sau khi đã tạo nhiều temporal features, representation cuối cùng nên được tổ chức như thế nào để downstream model có thể sử dụng?**

---

# 19. Rolling Features cho Multivariate Time Series

Cho:

$$
\mathbf{x}_t =

[x_t^{(1)},x_t^{(2)},...,x_t^{(F)}]
$$

có thể tính rolling statistic cho từng feature:

$$
\mu_t^{(j,w)} =

\frac{1}{w}
\sum_{i=0}^{w-1}
x_{t-i}^{(j)}
$$

với:

$$
j=1,\ldots,F
$$

Ví dụ:

```text
Temperature
    ↓
Rolling Mean Temperature

Humidity
    ↓
Rolling Mean Humidity

Pressure
    ↓
Rolling Mean Pressure
```

Nếu có:

* (F) features;
* (R) rolling statistics;
* (W) window sizes;

thì số lượng rolling-derived features có thể tăng theo:

$$
F\times R\times W
$$

Điều này cho thấy rolling features có thể nhanh chóng làm feature space trở nên lớn.

---

# 20. Redundancy

Các rolling features có thể có correlation cao.

Ví dụ:

```text
rolling_mean_6
rolling_mean_12
rolling_mean_24
```

có thể chứa information tương tự nhau.

Tương tự:

```text
lag_1
lag_2
lag_3
```

có thể có tương quan cao trong một smooth time series.

Do đó:

$$
Feature\ Engineering
\neq
Feature\ Maximization
$$

Mục tiêu phải là:

$$
\boxed{
Useful\ Representation
}
$$

chứ không phải tạo càng nhiều feature càng tốt.

Điểm này nối trực tiếp tới phần **feature reduction/selection** trong taxonomy rộng hơn của survey. Paper xem feature engineering/preprocessing cùng với các vấn đề giảm feature và transformation, vì vậy việc tạo feature cần được cân bằng với complexity của representation. ([research.chalmers.se][1])

---

# 21. Rolling Features và Downstream Model

Rolling features có thể trở thành input cho nhiều loại model:

```text
Rolling Features
       │
       ├── Linear Regression
       │
       ├── Tree-based Models
       │
       ├── Neural Networks
       │
       └── Sequence Models
```

Nhưng model khác nhau có thể khai thác representation khác nhau.

Ví dụ:

```text
Tabular ML

[x_t, lag_1, lag_2, rolling_mean]
        ↓
       Model
```

trong khi sequence model có thể nhận:

```text
[x_(t-k), ..., x_(t-1), x_t]
        ↓
     Sequence Model
```

Do đó rolling feature không phải lúc nào cũng cần thiết.

Nếu model đã có khả năng học temporal representation trực tiếp, việc thêm quá nhiều manually engineered rolling statistics có thể không đem lại lợi ích tương ứng với complexity.

---

# 22. Rolling Features và Information Preservation

Rolling aggregation nén nhiều observations thành một giá trị.

Ví dụ:

```text
Original:

10 12 14 16 20

Rolling Mean:

14.4
```

Ta đã biến:

$$
{10,12,14,16,20}
$$

thành:

$$
14.4
$$

Điều này làm representation đơn giản hơn nhưng đồng thời làm mất một phần information.

Do đó:

$$
\boxed{
Aggregation
\rightarrow
Compression
+
Information\ Loss
}
$$

Ví dụ rolling mean không còn cho biết:

* giá trị nào lớn nhất;
* giá trị nào nhỏ nhất;
* thứ tự chính xác;
* signal có peak ở đâu.

Đây là lý do nên kết hợp rolling features với lag hoặc những representation khác nếu information chi tiết vẫn quan trọng.

---

# 23. Rolling Features và Data Leakage

Trong forecasting, rolling features phải được xây dựng theo temporal direction.

Ví dụ dự đoán:

$$
y_{t+1}
$$

thì feature tại (t) có thể sử dụng:

$$
x_t,x_{t-1},...,x_{t-k}
$$

nhưng không được sử dụng:

$$
x_{t+1}
$$

hoặc:

$$
x_{t+2}
$$

nếu chúng chưa tồn tại tại thời điểm dự báo.

Causal rolling mean:

$$
\mu_t^{(w)} =

\frac{1}{w}
\sum_{i=0}^{w-1}x_{t-i}
$$

Còn centered rolling mean:

$$
	ilde{\mu}_t =

f(x_{t-k},...,x_t,...,x_{t+k})
$$

có thể sử dụng future observations.

Vì vậy trong forecasting:

$$
\boxed{
Rolling\ Feature
\rightarrow
Causal\ Construction
}
$$

khi task yêu cầu causal/online prediction.

---

# 24. Rolling Features và Train / Validation / Test

Feature construction phải được thực hiện theo temporal boundaries.

Ví dụ:

```text
Train
───────────────────┐
                   │ Validation
                   ├──────────────────┐
                                      │ Test
                                      ├──────────
```

Không được để quá trình preprocessing của training sử dụng observations ở Validation/Test.

Đặc biệt cần phân biệt:

### History hợp lệ

Một sample ở cuối Train có thể cần historical observations trước đó trong Train.

### Future leakage

Không được lấy dữ liệu thuộc Validation/Test để tạo feature cho sample Train.

Do đó:

$$
\boxed{
Past\ Context
\neq
Future\ Context
}
$$

---

# 25. Rolling Features và Irregular Time Series

Rolling window có thể được định nghĩa theo hai cách.

### Observation-based Window

Window chứa (w) observations:

$$
W_t=
{x_{t-w+1},...,x_t}
$$

### Time-based Window

Window chứa một khoảng thời gian thực:

$$
W_t=
{x_s:t-\Delta t\le s\le t}
$$

Hai cách này chỉ tương đương khi sampling đều.

Ví dụ:

```text
10:00
10:10
10:20
10:30
```

thì 3 observations gần tương ứng với 30 phút.

Nhưng nếu:

```text
10:00
10:02
10:20
11:00
```

thì 3 observations không còn tương đương với một fixed temporal duration.

Điều này quay trở lại `01_temporal_features.md`: **temporal resolution và temporal structure phải được hiểu trước khi xây dựng feature**.

---

# 26. Rolling Features trong Pipeline

Đến đây Chapter 5 có thể được nhìn như:

```text
Raw Time Series
       │
       ▼
01 Temporal Features
       │
       ▼
Understand Time Structure
       │
       ▼
02 Lag Features
       │
       ▼
Historical Values
       │
       ▼
03 Rolling Features
       │
       ▼
Window-level Statistics
       │
       ▼
04 Feature Representation
       │
       ▼
Final Feature Space
       │
       ▼
Downstream Model
```

Hoặc toán học:

$$
X_t
\rightarrow
{X_{t-k},...,X_t}
\rightarrow
\phi(X_{t-k:t})
\rightarrow
Z_t
\rightarrow
f(Z_t)
$$

Trong đó:

* (X_t): original feature vector.
* (X_{t-k:t}): temporal window.
* (\phi): rolling transformation.
* (Z_t): final representation.
* (f): downstream model.

---

# 27. Rolling Features và Survey's Main Principle

Một điểm xuyên suốt paper là preprocessing không nên được lựa chọn độc lập với downstream task.

Survey nhấn mạnh preprocessing là một quá trình phức tạp; kỹ thuật được lựa chọn phải xét đến data characteristics, application requirements và thuật toán AI phía sau. Paper cũng đánh giá empirically ảnh hưởng của preprocessing lên AI performance thay vì chỉ xem xét preprocessing ở mức data quality. ([research.chalmers.se][1])

Đối với Rolling Features, nguyên tắc này có nghĩa:

```text
Không phải:

Time Series
    ↓
Add rolling features
```

mà:

```text
Time Series
    ↓
Understand Task
    ↓
Understand Temporal Dependency
    ↓
Select Window
    ↓
Select Statistic
    ↓
Evaluate Representation
    ↓
Evaluate Downstream Model
```

---

# 28. Trade-offs

| Quyết định       | Lợi ích                 | Chi phí / Rủi ro                   |
| ---------------- | ----------------------- | ---------------------------------- |
| Window nhỏ       | Bắt local changes       | Nhạy với noise                     |
| Window lớn       | Ổn định hơn             | Mất short-term information         |
| Nhiều statistics | Giàu representation     | Tăng dimensionality                |
| Nhiều windows    | Multi-scale information | Tăng computation                   |
| Rolling Mean     | Đơn giản, ổn định       | Có thể mất peaks                   |
| Rolling Std      | Mô tả variability       | Không biểu diễn level              |
| Rolling Min/Max  | Bắt extremes            | Nhạy với outlier                   |
| Rolling Median   | Robust                  | Có thể bỏ qua fine structure       |
| Causal Window    | Phù hợp forecasting     | Ít information hơn centered window |
| Centered Window  | Mô tả local signal tốt  | Có thể dùng future information     |

Không có cấu hình rolling feature tốt nhất cho mọi dataset.

---

# 29. Cách lựa chọn Rolling Window

Có thể bắt đầu từ câu hỏi:

### Câu hỏi 1: Sampling frequency là gì?

Ví dụ:

$$
\Delta t=10\ minutes
$$

### Câu hỏi 2: Temporal pattern quan trọng ở scale nào?

Ví dụ:

```text
Short-term
Medium-term
Daily
Weekly
```

### Câu hỏi 3: Feature cần mô tả gì?

```text
Mean
Variance
Range
Trend
Extreme
Accumulation
```

### Câu hỏi 4: Downstream model cần representation nào?

```text
Tabular Model
Sequence Model
Deep Learning
```

### Câu hỏi 5: Có constraint về computation không?

Đặc biệt quan trọng trong Edge/streaming systems, một chủ đề mà survey cũng xem xét khi thảo luận khả năng phân phối preprocessing xuống Edge. ([research.chalmers.se][1])

---

# 30. Key Takeaways

## 1. Rolling Feature là representation của một temporal window

$$
W_t=
{x_{t-w+1},...,x_t}
$$

sau đó:

$$
z_t=f(W_t)
$$

---

## 2. Rolling Feature mở rộng Lag Feature

```text
Lag
→ Một historical point

Rolling
→ Một historical window
```

---

## 3. Window size quyết định temporal scale

$$
w\downarrow
\rightarrow
Short-term
$$

$$
w\uparrow
\rightarrow
Longer-term
$$

---

## 4. Rolling Feature không giống Noise Reduction

```text
Noise Reduction
→ Clean Signal

Rolling Feature
→ New Feature
```

---

## 5. Rolling aggregation có thể làm mất information

$$
Multiple\ Values
\rightarrow
One\ Statistic
$$

Do đó cần cân bằng:

$$
Representation\ Simplicity
\leftrightarrow
Information\ Preservation
$$

---

## 6. Rolling Features có thể làm feature space tăng nhanh

$$
Features
\times
Statistics
\times
Windows
$$

có thể tạo ra số lượng feature lớn.

Vì vậy cần cân nhắc feature reduction/selection.

---

## 7. Forecasting cần causal rolling features

$$
Feature_t = f(x_{\leq t})

$$

không được sử dụng future observations nếu chúng chưa khả dụng tại prediction time.

---

# 31. Kết luận

Rolling Features là bước chuyển từ việc biểu diễn **một historical value** sang biểu diễn **đặc tính của một historical window**.

Chuỗi logic của Chapter 5 là:

$$
\boxed{
Temporal\ Structure
\rightarrow
Lag
\rightarrow
Rolling
\rightarrow
Feature\ Representation
}
$$

Trong đó:

* `01_temporal_features.md` giải thích **vì sao thời gian chứa information**.
* `02_lag_features.md` biến **historical observations thành explicit features**.
* `03_rolling_features.md` tổng hợp **historical observations thành local temporal statistics**.
* `04_feature_representation.md` sẽ quyết định **cách tổ chức toàn bộ các feature thành representation cuối cùng cho downstream model**.

Rolling Features vì vậy không phải chỉ là một tập hợp các công thức `rolling_mean`, `rolling_std` hay `rolling_max`. Về bản chất, đây là một cách **nén temporal context thành những đặc trưng mà model có thể sử dụng**:

$$
\boxed{
Temporal\ Window
\rightarrow
Aggregation
\rightarrow
Feature
}
$$

Tuy nhiên, theo tinh thần của survey, một preprocessing/feature-engineering method chỉ thực sự có giá trị khi representation mới **phù hợp với dữ liệu, giữ được information quan trọng và cải thiện hoặc hỗ trợ downstream AI task**, thay vì chỉ tạo ra nhiều feature hơn. ([research.chalmers.se][1])

[1]: https://research.chalmers.se/publication/540495/file/540495_Fulltext.pdf?utm_source=chatgpt.com "Survey: Time-Series Data Preprocessing: A Survey and an Empirical"
