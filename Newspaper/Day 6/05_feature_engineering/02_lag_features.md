# 02. Lag Features

## 1. Vị trí của Lag Features trong Chapter 5

Ở `01_temporal_features.md`, chúng ta đã xác định một đặc điểm cốt lõi của Time-Series Data:

$$
x_1 \rightarrow x_2 \rightarrow \cdots \rightarrow x_t
$$

Các observation không tồn tại hoàn toàn độc lập mà được sắp xếp theo thời gian.

Từ đó xuất hiện một câu hỏi quan trọng:

> Làm thế nào để đưa thông tin từ các thời điểm trước đó vào representation mà Machine Learning model có thể sử dụng?

Một trong những cách trực tiếp nhất là **Lag Features**.

Cấu trúc của Chapter 5:

```text
05_feature_engineering/
│
├── 01_temporal_features.md
│   └── Temporal structure và temporal information
│
├── 02_lag_features.md
│   └── Đưa thông tin quá khứ vào feature representation
│
├── 03_rolling_features.md
│   └── Tổng hợp thông tin trên một temporal window
│
└── 04_feature_representation.md
    └── Biểu diễn cuối cùng được đưa vào downstream model
```

Do đó:

$$
Temporal\ Structure
\rightarrow
Lag\ Features
\rightarrow
Rolling\ Features
\rightarrow
Feature\ Representation
$$

Đây là logic xuyên suốt của Chapter 5.

---

# 2. Lưu ý về phạm vi của Paper

Cần phân biệt rõ:

> **Lag Features không phải là một nhóm thuật toán được paper khảo sát như một mục độc lập.**

Paper xây dựng một taxonomy rộng cho preprocessing numerical time-series data và xem Feature Engineering là một thành phần của preprocessing. Trong taxonomy đó, Feature Engineering bao gồm các hướng như **feature reduction, feature transformation và feature synthesis**. ([research.chalmers.se][1])

Paper tập trung khảo sát các preprocessing techniques theo taxonomy của mình và thực hiện empirical analysis về ảnh hưởng của preprocessing lên data quality và AI performance. ([ScienceDirect][2])

Vì vậy:

```text
Paper
│
├── Time-Series Preprocessing
│
├── Feature Engineering
│
└── Các kỹ thuật feature-related được paper khảo sát
```

không đồng nghĩa với:

```text
Paper
└── Lag Features
      ├── lag_1
      ├── lag_7
      └── lag_24
```

Các lag features cụ thể trong file này được trình bày như **kiến thức nền và phần mở rộng để hiểu cách temporal information có thể được đưa vào feature representation**.

Không được ghi:

> "Tác giả đề xuất Lag Features."

---

# 3. Lag Feature là gì?

Lag Feature là một feature được tạo từ giá trị của cùng một biến tại một thời điểm trước đó.

Với time series:

$$
x_t
$$

lag (k) được định nghĩa:

$$
x_{t-k}
$$

Trong đó:

* (t): thời điểm hiện tại.
* (k): số bước thời gian lùi lại.
* (x_{t-k}): giá trị của biến tại thời điểm trước đó (k) bước.

Ví dụ:

```text
Time:       t1   t2   t3   t4   t5
Value:      10   12   15   14   18
```

Lag 1:

```text
Current:    10   12   15   14   18
Lag-1:       -   10   12   15   14
```

Lag 2:

```text
Current:    10   12   15   14   18
Lag-2:       -    -   10   12   15
```

Do đó tại $t_5$:

$$
Lag_1=x_{t_5-1}=14
$$

và:

$$
Lag_2=x_{t_5-2}=15
$$

---

# 4. Tại sao Lag Features quan trọng?

Temporal information ở `01_temporal_features.md` mới chỉ cho chúng ta biết rằng observation có thứ tự.

Lag Features biến temporal dependency đó thành một phần rõ ràng của feature representation.

Không chỉ sử dụng:

$$
X_t=x_t
$$

ta có thể sử dụng:

$$
X_t=
[x_t,x_{t-1},x_{t-2},\ldots,x_{t-k}]
$$

Khi đó model có quyền truy cập trực tiếp vào historical information.

Có thể hình dung:

```text
                 Past
                  │
        ┌─────────┼─────────┐
        │         │         │
       t-3       t-2       t-1
        │         │         │
        └─────────┼─────────┘
                  │
                  ▼
                 t
                  │
                  ▼
             Feature Vector
```

Đây là bước chuyển từ:

```text
Temporal Ordering
```

sang:

```text
Temporal Representation
```

---

# 5. Từ Temporal Structure đến Lag Features

Ở file `01_temporal_features.md`, chúng ta đã phân biệt:

$$
Time-Series
\neq
Independent\ Observations
$$

Lag Features cụ thể hóa ý tưởng này.

Ví dụ:

```text
Original:

x1 → x2 → x3 → x4 → x5
```

Sau khi tạo lag:

```text
At t4:

[x4, x3, x2, x1]
```

Do đó một observation mới không còn chỉ là:

$$
x_t
$$

mà trở thành:

$$
\mathbf{X}_t=
[x_t,x_{t-1},\ldots,x_{t-k}]
$$

Có thể xem đây là một dạng **temporal feature representation**.

---

# 6. Một Lag hay nhiều Lag?

Không nhất thiết chỉ sử dụng một lag.

Có thể tạo:

$$
X_t=
[x_t,x_{t-1},x_{t-2},x_{t-3}]
$$

hoặc:

$$
X_t=
[x_t,x_{t-1},x_{t-7},x_{t-24}]
$$

Mỗi lag đại diện cho một khoảng temporal khác nhau.

Ví dụ nếu dữ liệu được lấy mỗi giờ:

```text
lag_1
→ 1 giờ trước

lag_6
→ 6 giờ trước

lag_24
→ 24 giờ trước

lag_168
→ 7 ngày trước
```

Nhưng ý nghĩa của (k) luôn phụ thuộc vào sampling frequency.

Nếu:

$$
\Delta t=10\ minutes
$$

thì:

$$
lag_1=10\ minutes
$$

trong khi:

$$
lag_6=60\ minutes
$$

Do đó không nên nói:

> lag 24 luôn có nghĩa là 24 giờ.

Phải biết temporal resolution trước.

---

# 7. Lag và Sampling Frequency

Đây là một điểm rất quan trọng trong Time-Series Preprocessing.

Giả sử:

$$
\Delta t=1\ hour
$$

thì:

$$
x_{t-24}
$$

đại diện cho khoảng 24 giờ trước.

Nhưng nếu:

$$
\Delta t=10\ minutes
$$

thì:

$$
x_{t-24}
$$

chỉ đại diện cho:

$$
24\times10=240\ minutes
$$

hay:

$$
4\ hours
$$

Do đó:

$$
\boxed{
Lag\ Index
\neq
Physical\ Time
}
$$

mà:

$$
	ext{Physical Time}
=

	ext{Lag Index}
\times
	ext{Sampling Interval}
$$

Điều này nối trực tiếp với nội dung `01_temporal_features.md`: temporal information phải được hiểu trong context của sampling frequency.

---

# 8. Lag Features cho Multivariate Time Series

Với multivariate time series:

$$
\mathbf{x}_t=

[x_t^{(1)},x_t^{(2)},\ldots,x_t^{(F)}]
$$

có thể tạo lag cho từng feature.

Ví dụ:

```text
Feature 1:
x1(t-1), x1(t-2), ...

Feature 2:
x2(t-1), x2(t-2), ...

Feature 3:
x3(t-1), x3(t-2), ...
```

Feature vector có thể trở thành:

$$
\mathbf{X}_t=
[
\mathbf{x}_t,
\mathbf{x}_{t-1},
\mathbf{x}_{t-2}
]
$$

Nếu:

* (F) = số feature;
* (K) = số lag;

thì về mặt khái niệm số lượng temporal observations được đưa vào representation là:

$$
F(K+1)
$$

nếu bao gồm cả thời điểm hiện tại.

Điều này cho thấy một trade-off:

$$
K\uparrow
\Rightarrow
Feature\ Dimension\uparrow
$$

---

# 9. Lag Features và Temporal Dependency

Lag Features đặc biệt hữu ích khi target phụ thuộc vào historical observations.

Ví dụ:

$$
y_t=f(x_t,x_{t-1},x_{t-2})
$$

thay vì:

$$
y_t=f(x_t)
$$

Model có thể học:

```text
Past
 │
 ├── x(t-2)
 ├── x(t-1)
 │
 ▼
Current
 │
 ▼
Prediction
```

Đây chính là cách biến temporal dependency thành explicit features.

Tuy nhiên cần lưu ý:

> Việc tạo lag không đảm bảo model sẽ học được dependency hữu ích.

Nếu lag không chứa predictive information, việc thêm lag chỉ làm tăng dimensionality.

---

# 10. Lag Features và Feature Synthesis

Trong taxonomy của paper, Feature Engineering có thể bao gồm **feature synthesis**: tạo ra representation mới từ dữ liệu ban đầu.

Lag Feature có thể được hiểu theo góc nhìn này:

```text
Original Feature
      │
      ▼
Temporal Shift
      │
      ▼
Lag Feature
```

Ví dụ:

$$
x_t
\rightarrow
x_{t-1}
$$

Từ một biến ban đầu có thể tạo ra nhiều biến biểu diễn lịch sử:

$$
x_t
\rightarrow
{x_{t-1},x_{t-2},\ldots,x_{t-k}}
$$

Điểm quan trọng là đây là **feature construction**, không phải data cleaning.

---

# 11. Lag Features không phải Data Cleaning

Cần phân biệt rõ với Chapter 3.

```text
Chapter 3 — Data Cleaning

Missing
Outlier
Noise
```

trong khi:

```text
Chapter 5 — Feature Engineering

Temporal Features
Lag Features
Rolling Features
Feature Representation
```

Mục tiêu khác nhau:

$$
Data\ Cleaning
\rightarrow
Improve\ Data\ Quality
$$

trong khi:

$$
Feature\ Engineering
\rightarrow
Construct\ Useful\ Representation
$$

Do đó:

```text
Missing Value
```

không phải lag feature.

Và:

```text
x(t-1)
```

không phải một phương pháp imputation.

---

# 12. Lag Features và Data Leakage

Đây là một trong những vấn đề quan trọng nhất khi xây dựng lag features cho Machine Learning.

Giả sử mục tiêu là dự đoán:

$$
y_t
$$

Feature tại thời điểm (t) chỉ được phép sử dụng information có sẵn tại thời điểm dự đoán.

Ví dụ hợp lệ:

$$
X_t=
[x_t,x_{t-1},x_{t-2}]
$$

nếu (x_t) đã được quan sát tại thời điểm dự đoán.

Không được sử dụng:

$$
x_{t+1}
$$

để dự đoán (y_t) nếu (x_{t+1}) chỉ xuất hiện trong tương lai.

Do đó:

$$
\boxed{
Future\ Information
\notin
Past\ Features
}
$$

---

# 13. Causal Temporal Representation

Trong forecasting, một representation causal có dạng:

$$
\mathbf{X}_t=
[x_t,x_{t-1},\ldots,x_{t-k}]
$$

và target:

$$
y_{t+h}
$$

Khi đó:

```text
Past / Present
      │
      ▼
Feature Construction
      │
      ▼
Prediction
      │
      ▼
Future
```

Đây là cách xây dựng feature representation phù hợp với temporal forecasting.

Ngược lại:

```text
Past
 │
 ▼
Feature
 │
 ├──── Future Information
 │
 ▼
Target
```

có thể tạo leakage.

---

# 14. Missing Values trong Lag Features

Lag construction có một hệ quả tự nhiên:

```text
Original:

t1   t2   t3   t4
10   12   15   14
```

Lag 2:

```text
t1   t2   t3   t4
 -    -   10   12
```

Hai observation đầu tiên không có đủ history.

Do đó:

$$
Lag_k
\Rightarrow
k\ initial\ observations
$$

không thể tạo feature hoàn chỉnh nếu không có historical data trước đó.

Có thể xử lý bằng:

* loại bỏ các dòng đầu;
* padding;
* sử dụng history từ trước khoảng dữ liệu;
* hoặc một chiến lược preprocessing khác.

Nhưng cách xử lý cụ thể phải phụ thuộc task.

Không nên mặc định:

> cứ forward fill là đúng.

---

# 15. Lag Features và Window

Lag Features có quan hệ rất gần với **window-based representation**.

Ví dụ với:

$$
K=3
$$

ta có:

$$
\mathbf{X}_t=
[x_{t-3},x_{t-2},x_{t-1},x_t]
$$

Đây chính là một temporal window.

Có thể biểu diễn:

```text
t-3   t-2   t-1    t
 │     │     │     │
 └─────┴─────┴─────┘
          Window
```

Do đó:

$$
Lag\ Features
\approx
Explicit\ Temporal\ History
$$

trong khi:

$$
Window\ Representation
$$

là cách tổ chức nhiều historical observations thành một input sequence.

Sự khác biệt này sẽ trở nên quan trọng khi chuyển sang các model sequence như RNN, LSTM hoặc Transformer.

---

# 16. Lag Features và Rolling Features

Đây là cầu nối trực tiếp tới file tiếp theo:

```text
02_lag_features.md
        │
        ▼
03_rolling_features.md
```

Lag Feature lấy **một historical observation**:

$$
Lag_k=x_{t-k}
$$

Rolling Feature lấy **một tập historical observations trong window**:

$$
W_t=
{x_{t-k+1},...,x_t}
$$

sau đó tính một statistic hoặc transformation.

Ví dụ rolling mean:

$$
\mu_t^{(k)}
 =

\frac{1}{k}
\sum_{i=0}^{k-1}x_{t-i}
$$

Do đó:

```text
Lag Feature

x(t-1)
  │
  ▼
One historical value
```

trong khi:

```text
Rolling Feature

x(t-k) ... x(t-2) x(t-1) x(t)
  │
  ▼
Multiple historical values
  │
  ▼
Aggregation / Transformation
```

Đây là lý do `03_rolling_features.md` phải được đọc sau file này.

---

# 17. Lag và Rolling bổ trợ cho nhau

Giả sử:

```text
Time:

t-4  t-3  t-2  t-1  t
 10   12   13   15  14
```

Lag features:

$$
x_{t-1}=15
$$

$$
x_{t-2}=13
$$

Rolling mean:

$$
\frac{10+12+13+15+14}{5}=12.8
$$

Hai representation chứa thông tin khác nhau.

Lag:

> "Giá trị trước đó là bao nhiêu?"

Rolling:

> "Đặc tính chung của một khoảng thời gian gần đây là gì?"

Do đó:

$$
Lag
\rightarrow
Point\ History
$$

còn:

$$
Rolling
\rightarrow
Window\ Summary
$$

---

# 18. Số lượng Lag và Dimensionality

Nếu có (F) original features và tạo (K) lag cho mỗi feature:

$$
F\times K
$$

feature mới có thể được tạo ra.

Ví dụ:

```text
10 original features
×
5 lag values
=
50 lag-derived features
```

Điều này có thể làm feature space tăng nhanh.

Do đó:

$$
K\uparrow
\Rightarrow
Dimension\uparrow
\Rightarrow
Computation\uparrow
$$

và có thể dẫn tới:

* redundancy;
* increased memory;
* increased training cost;
* overfitting risk.

Vì vậy lag feature engineering phải kết hợp với các bước feature transformation hoặc feature selection khi cần thiết.

---

# 19. Lag Selection

Không phải lag nào cũng hữu ích.

Giả sử:

```text
lag_1
lag_2
lag_3
...
lag_100
```

Không có nghĩa tất cả đều chứa useful information.

Có thể tồn tại:

$$
I(y_t;x_{t-k})
$$

khác nhau theo (k).

Một số lag có thể mang information mạnh:

```text
lag_1
lag_24
lag_168
```

trong khi các lag khác gần như redundant.

Do đó:

$$
\boxed{
More\ Lag
\neq
More\ Information
}
$$

Đây là điểm nối với `04_feature_representation.md`, nơi cần xem xét representation nào thực sự phù hợp cho downstream model.

---

# 20. Lag Features và Feature Selection

Sau khi tạo nhiều lag:

```text
Original Features
      │
      ▼
Lag Construction
      │
      ▼
Large Feature Space
      │
      ▼
Feature Selection / Reduction
      │
      ▼
Final Representation
```

Đây là một pipeline tự nhiên:

$$
Raw
\rightarrow
Lag
\rightarrow
Selection
\rightarrow
Representation
$$

Trong survey, Feature Selection và Feature Reduction là những thành phần của phạm vi Feature Engineering/preprocessing được khảo sát.

Do đó việc tạo thêm feature không có nghĩa là giữ lại toàn bộ feature.

---

# 21. Lag Features và Downstream AI

Lag features có thể được sử dụng để tạo input cho các mô hình Machine Learning.

Ví dụ:

```text
Lag Features
     │
     ▼
Feature Vector
     │
     ├── Linear Model
     ├── Tree-based Model
     └── Neural Network
```

Đây là điểm khác với sequence model.

Với traditional tabular representation:

$$
[x_t,x_{t-1},x_{t-2}]
$$

được xem như một vector feature.

Trong sequence model:

$$
[x_{t-2},x_{t-1},x_t]
$$

có thể được giữ dưới dạng sequence.

Do đó cùng một historical information có thể được biểu diễn theo nhiều cách.

---

# 22. Lag Features và Feature Representation

Đến đây có thể thấy Chapter 5 đang đi theo một chuỗi logic:

```text
01 Temporal Features
        │
        │
        ▼
Temporal Structure
        │
        ▼
02 Lag Features
        │
        │
        ▼
Explicit Historical Information
        │
        ▼
03 Rolling Features
        │
        │
        ▼
Temporal Aggregation
        │
        ▼
04 Feature Representation
        │
        ▼
Final Model Input
```

Do đó bốn file không phải bốn topic độc lập.

Chúng là bốn bước của cùng một quá trình:

$$
\boxed{
Temporal\ Information
\rightarrow
Feature\ Construction
\rightarrow
Feature\ Aggregation
\rightarrow
Representation
}
$$

---

# 23. Quan hệ với Survey

Paper nhấn mạnh rằng preprocessing không có một pipeline cố định cho mọi trường hợp.

Việc lựa chọn preprocessing phụ thuộc vào:

* loại dữ liệu;
* data source;
* system context;
* application;
* available resources;
* downstream algorithm. ([research.chalmers.se][1])

Do đó Lag Features cũng không nên được xem như một preprocessing step bắt buộc.

Có trường hợp:

```text
Raw Sequence
   ↓
LSTM / Transformer
```

đã trực tiếp nhận historical sequence.

Khi đó việc flatten toàn bộ lag thành các feature độc lập có thể không phải lựa chọn tối ưu.

Ngược lại, với các model yêu cầu fixed-dimensional feature vector:

```text
Time Series
   ↓
Lag Construction
   ↓
Feature Vector
   ↓
ML Model
```

Lag Features có thể là một representation hữu ích.

---

# 24. Trade-offs

## Ưu điểm

### 1. Đơn giản

Lag feature dễ xây dựng từ temporal sequence.

### 2. Trực tiếp

Historical information được đưa trực tiếp vào input.

### 3. Có thể sử dụng với nhiều model

Không chỉ neural networks mà còn có thể sử dụng với các tabular ML models.

### 4. Dễ kiểm soát

Người thiết kế có thể chọn chính xác:

$$
k_1,k_2,\ldots,k_n
$$

---

## Hạn chế

### 1. Tăng dimensionality

$$
K\uparrow
\Rightarrow
Features\uparrow
$$

### 2. Redundancy

Các lag gần nhau có thể tương quan mạnh.

### 3. Không tự động hiểu temporal importance

Lag feature chỉ cung cấp historical values.

Model phải học cách sử dụng chúng.

### 4. Có thể gây leakage

Nếu sử dụng future information sai cách.

### 5. Phụ thuộc sampling frequency

Ý nghĩa của lag thay đổi theo temporal resolution.

---

# 25. Lag Features trong Edge / Resource-Constrained Systems

Survey cũng quan tâm đến khả năng phân phối preprocessing lên Edge.

Trong context này, việc tạo nhiều lag có một trade-off:

```text
More Lag Features
       │
       ├── More Information
       │
       ├── More Memory
       │
       ├── More Computation
       │
       └── More Data to Process
```

Do đó trong EdgeAI:

$$
Feature\ Richness
\leftrightarrow
Resource\ Consumption
$$

Việc preprocessing tại Edge có thể giảm lượng dữ liệu cần truyền về central system, nhưng bản thân preprocessing cũng tiêu thụ tài nguyên. Paper xem computational/resource considerations là một phần quan trọng khi đánh giá preprocessing trong context EdgeAI. ([ScienceDirect][2])

---

# 26. Một Pipeline hoàn chỉnh

Kết hợp ba file đầu của Chapter 5:

```text
Raw Time Series
       │
       ▼
01 Temporal Features
       │
       │
       │ Understand temporal structure
       ▼
02 Lag Features
       │
       │
       │ Explicit historical values
       ▼
03 Rolling Features
       │
       │
       │ Historical aggregation
       ▼
04 Feature Representation
       │
       │
       │ Final encoding / representation
       ▼
Downstream AI
```

Có thể biểu diễn toán học:

$$
X_t
\rightarrow
[X_t,X_{t-1},...,X_{t-k}]
\rightarrow
\phi(X_{t-k:t})
\rightarrow
Z_t
\rightarrow
Model
$$

Trong đó:

* (X_t): raw feature vector.
* (X_{t-k:t}): temporal history.
* (\phi(\cdot)): transformation / aggregation.
* (Z_t): final feature representation.

---

# 27. Những điều không được hiểu sai

### Không phải:

> Lag Features luôn cải thiện model.

Mà:

> Lag Features cung cấp historical information mà model có thể khai thác.

---

### Không phải:

> Càng nhiều lag càng tốt.

Mà:

$$
Useful\ Lag

>

Maximum\ Lag
$$

---

### Không phải:

> Lag Features là contribution của paper.

Mà:

> Lag Features là một khái niệm feature engineering được sử dụng ở đây để mở rộng và cụ thể hóa temporal representation; paper không trình bày nó như một contribution riêng.

---

### Không phải:

> Mọi time-series model đều cần lag features.

Sequence models có thể nhận trực tiếp historical sequence.

---

# 28. Key Takeaways

## 1. Lag Features biến temporal dependency thành feature

$$
x_t
\rightarrow
[x_t,x_{t-1},...,x_{t-k}]
$$

---

## 2. Lag phụ thuộc vào sampling frequency

$$
Physical\ Time=

Lag
\times
Sampling\ Interval
$$

---

## 3. Lag Features là Feature Construction

Nó không phải Data Cleaning.

---

## 4. Lag Features có quan hệ trực tiếp với Rolling Features

```text
Lag
→ historical point

Rolling
→ historical window summary
```

Vì vậy `03_rolling_features.md` sẽ tiếp tục trực tiếp từ phần này.

---

## 5. Lag Features có thể làm tăng dimensionality

$$
K\uparrow
\Rightarrow
Feature\ Dimension\uparrow
$$

Do đó cần cân nhắc feature selection/reduction.

---

## 6. Temporal leakage phải được kiểm soát

Feature tại thời điểm (t) không được chứa information từ tương lai nếu task yêu cầu causal forecasting.

$$
Future
\not\rightarrow
Past\ Feature
$$

---

## 7. Paper không khảo sát Lag Features như một mục riêng

Paper cung cấp một taxonomy rộng về time-series preprocessing và Feature Engineering; vì vậy nội dung Lag Features trong file này được sử dụng để xây dựng cầu nối kiến thức từ temporal structure đến feature representation, chứ không được trình bày như một thuật toán do tác giả đề xuất.

---

# 29. Kết luận

Temporal information chỉ thực sự hữu ích cho Machine Learning khi được đưa vào một representation mà model có thể khai thác.

Lag Features thực hiện điều đó bằng cách đưa historical observations vào feature space:

$$
\boxed{
Temporal\ Structure
\rightarrow
Historical\ Values
\rightarrow
Lag\ Features
}
$$

Nhưng việc tạo lag không phải mục tiêu cuối cùng.

Sau khi tạo historical features, cần tiếp tục xem xét:

```text
Lag Features
      │
      ▼
Rolling / Window-based Features
      │
      ▼
Feature Representation
      │
      ▼
Feature Selection / Reduction
      │
      ▼
Downstream Model
```

Vì vậy, trong Chapter 5:

> **`01_temporal_features.md` giải thích tại sao thời gian mang information → `02_lag_features.md` biến historical information thành feature → `03_rolling_features.md` tổng hợp information trên temporal window → `04_feature_representation.md` quyết định cách representation cuối cùng được đưa vào model.**

````

### Liên kết logic của Chapter 5

Mình khuyên **giữ đúng chuỗi này cho 4 file**, để Agent sau này viết các file tiếp theo không bị rời rạc:

| File | Câu hỏi chính | Kết quả |
|---|---|---|
| `01_temporal_features.md` | **Thời gian chứa information gì?** | Temporal structure |
| `02_lag_features.md` | **Làm sao đưa quá khứ vào feature?** | Historical values |
| `03_rolling_features.md` | **Làm sao tổng hợp một khoảng quá khứ?** | Window statistics |
| `04_feature_representation.md` | **Làm sao biểu diễn tất cả thành input?** | Final representation |

Như vậy Chapter 5 có flow:

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
Feature Transformation / Representation
       ↓
Final Input
       ↓
AI Model
````

**Lưu ý quan trọng về độ trung thực với paper:** paper này là một **survey về preprocessing**, không phải paper đề xuất một framework Lag/Rolling Feature Engineering. Vì vậy các file `02` và `03` nên được viết theo kiểu **“kiến thức cần hiểu trong kiến trúc Chapter 5 + liên hệ chính xác với taxonomy của survey”**, chứ không được giả vờ rằng Tawakuli et al. đã đề xuất các công thức lag/rolling đó. Paper xác nhận preprocessing cần được lựa chọn theo data type, application, resources và downstream algorithm; đây là cơ sở để nối các feature-engineering concepts này với survey. ([research.chalmers.se][1])

[1]: https://research.chalmers.se/publication/540495/file/540495_Fulltext.pdf?utm_source=chatgpt.com "Survey: Time-Series Data Preprocessing: A Survey and an Empirical"
[2]: https://www.sciencedirect.com/science/article/pii/S2307187724000452?utm_source=chatgpt.com "Survey:Time-series data preprocessing: A survey and an empirical analysis - ScienceDirect"
