# 04. Feature Representation

## 1. Vị trí của Feature Representation trong Chapter 5

Trong ba mục trước, chúng ta đã xây dựng feature theo từng lớp thông tin:

```text
01_temporal_features.md
        │
        ▼
Temporal Information
        │
        ▼
02_lag_features.md
        │
        ▼
Historical Information
        │
        ▼
03_rolling_features.md
        │
        ▼
Window-level Information
        │
        ▼
04_feature_representation.md
        │
        ▼
Final Feature Representation
        │
        ▼
Downstream AI Model
```

Có thể tóm tắt:

* `01_temporal_features.md`: xác định **thông tin nào đến từ thời gian**.
* `02_lag_features.md`: đưa **giá trị quá khứ** vào feature space.
* `03_rolling_features.md`: tổng hợp **một temporal window** thành các statistic.
* `04_feature_representation.md`: tổ chức tất cả những information trên thành **representation cuối cùng** cho downstream model.

Vì vậy, `04_feature_representation.md` là phần **kết thúc Chapter 5**.

---

# 2. Feature Representation là gì?

Feature Representation là cách biểu diễn dữ liệu sau preprocessing và feature engineering thành một dạng mà downstream algorithm có thể sử dụng.

Giả sử observation ban đầu tại thời điểm (t) là:

$$
x_t
$$

Sau các bước feature engineering, chúng ta có thể thu được:

$$
z_t=
[
x_t,
x_{t-1},
x_{t-2},
\mu_t^{(w)},
\sigma_t^{(w)},
\tau_t
]
$$

Trong đó:

* $x_t$: giá trị hiện tại.
* $x_{t-1},x_{t-2}$: lag features.
* $\mu_t^{(w)}$: rolling statistic.
* $\sigma_t^{(w)}$: rolling variability.
* $\tau_t$: temporal feature.

Toàn bộ vector:

$$
z_t
$$

chính là một **feature representation**.

---

# 3. Tại sao cần Feature Representation?

Raw time-series data thường không ở dạng trực tiếp phù hợp với downstream model.

Ví dụ:

```text
Timestamp
2026-01-01 08:00
2026-01-01 08:10
2026-01-01 08:20
...
```

Chỉ có timestamp chưa nói trực tiếp cho model:

* thời điểm trong ngày;
* ngày trong tuần;
* giá trị quá khứ;
* local mean;
* local variability;
* temporal context.

Chapter 5 lần lượt biến những information này thành representation:

```text
Timestamp
    │
    ▼
Temporal Features
    │
    ▼
Lag Features
    │
    ▼
Rolling Features
    │
    ▼
Feature Representation
```

Mục tiêu không phải đơn giản là tạo càng nhiều feature càng tốt.

Mục tiêu là:

$$
\boxed{
Raw\ Information
\rightarrow
Useful\ Representation
}
$$

---

# 4. Feature Representation và Feature Engineering

Hai khái niệm này có quan hệ nhưng không hoàn toàn giống nhau.

### Feature Engineering

Là quá trình tạo hoặc biến đổi feature.

Ví dụ:

$$
x_t
\rightarrow
x_{t-1}
$$

hoặc:

$$
x_t
\rightarrow
\mu_t^{(24)}
$$

### Feature Representation

Là cách các feature sau quá trình engineering được tổ chức thành representation cuối cùng.

Ví dụ:

$$
z_t=
[
x_t,
x_{t-1},
x_{t-2},
\mu_t^{(24)},
\sigma_t^{(24)}
]
$$

Do đó:

```text
Feature Engineering
        │
        ▼
Feature Construction / Transformation
        │
        ▼
Feature Representation
```

---

# 5. Feature Representation trong Survey

Paper *Time-Series Data Preprocessing: A Survey and an Empirical Analysis* xem preprocessing là một quá trình rộng, không chỉ giới hạn ở việc xử lý missing values hoặc outliers.

Survey xây dựng taxonomy cho các preprocessing techniques và xem xét cả **Feature Engineering**, bên cạnh các nhóm preprocessing khác.

Điểm quan trọng của survey là preprocessing phải được xem xét trong mối quan hệ với:

```text
Data
  │
  ├── Data characteristics
  │
  ├── Application
  │
  ├── Available resources
  │
  └── Downstream AI algorithm
```

Do đó Feature Representation không có một dạng duy nhất áp dụng cho mọi Time-Series Data.

Cách representation phù hợp phụ thuộc vào:

$$
	ext{Representation}
= f(\text{Data},\text{Task},\text{Model},\text{Resources})
$$

Paper cũng thực hiện empirical analysis để đánh giá tác động của preprocessing lên chất lượng dữ liệu và hiệu năng AI, thay vì giả định rằng một preprocessing technique luôn tốt trong mọi trường hợp.

**Lưu ý:** Feature Representation trong file này là khái niệm tổng hợp để hoàn thiện Chapter 5. Không được viết rằng tác giả đề xuất một "Feature Representation Algorithm" riêng.

---

# 6. Từ Temporal Features đến Final Representation

Ở `01_temporal_features.md`, temporal information được chuyển thành feature.

Ví dụ:

$$
timestamp
\rightarrow
hour,\ day,\ month,\ weekday
$$

Sau đó `02_lag_features.md` bổ sung historical information:

$$
x_t
\rightarrow
[x_t,x_{t-1},x_{t-2}]
$$

Tiếp theo `03_rolling_features.md` bổ sung local statistics:

$$
x_{t-w:t}
\rightarrow
[
\mu_t^{(w)},
\sigma_t^{(w)},
max_t^{(w)}
]
$$

Cuối cùng representation có thể trở thành:

$$
z_t=
[
Temporal_t,
Current_t,
Lag_t,
Rolling_t
]
$$

Toàn bộ Chapter 5 được kết nối:

```text
Temporal Features
        │
        ├── hour
        ├── weekday
        └── seasonality-related information
        │
        ▼
Lag Features
        │
        ├── lag_1
        ├── lag_2
        └── lag_k
        │
        ▼
Rolling Features
        │
        ├── rolling_mean
        ├── rolling_std
        └── rolling_max
        │
        ▼
Feature Representation
```

---

# 7. Một Feature Vector hoàn chỉnh

Giả sử tại thời điểm (t):

### Temporal features

$$
T_t=
[
hour_t,
weekday_t
]
$$

### Current values

$$
X_t=
[
x_t^{(1)},
x_t^{(2)}
]
$$

### Lag features

$$
L_t=
[
x_{t-1}^{(1)},
x_{t-1}^{(2)},
x_{t-2}^{(1)},
x_{t-2}^{(2)}
]
$$

### Rolling features

$$
R_t=
[
\mu_t^{(1,24)},
\mu_t^{(2,24)},
\sigma_t^{(1,24)},
\sigma_t^{(2,24)}
]
$$

Representation cuối:

$$
Z_t=
[T_t,X_t,L_t,R_t]
$$

Hay:

$$
Z_t=
[
hour_t,
weekday_t,
x_t^{(1)},
x_t^{(2)},
x_{t-1}^{(1)},
x_{t-1}^{(2)},
x_{t-2}^{(1)},
x_{t-2}^{(2)},
\mu_t^{(1,24)},
\mu_t^{(2,24)},
\sigma_t^{(1,24)},
\sigma_t^{(2,24)}
]
$$

Đây chính là feature vector mà một tabular downstream model có thể nhận.

---

# 8. Tabular Representation

Một cách phổ biến là biến mỗi thời điểm thành một vector cố định:

$$
Z_t\in\mathbb{R}^{D}
$$

Trong đó (D) là số lượng feature.

Ví dụ:

```text
Time t
   │
   ├── Temporal features
   ├── Current features
   ├── Lag features
   └── Rolling features
             │
             ▼
      Fixed-size vector
             │
             ▼
         ML Model
```

Dataset sau đó có dạng:

$$
Z\in\mathbb{R}^{N\times D}
$$

với:

* (N): số observation.
* (D): số feature.

Đây là representation phù hợp với nhiều mô hình Machine Learning dạng tabular.

---

# 9. Sequence Representation

Không phải lúc nào historical information cũng nên flatten thành một vector.

Thay vì:

$$
Z_t=
[x_t,x_{t-1},x_{t-2}]
$$

có thể giữ temporal structure:

$$
Z_t=
\begin{bmatrix}
x_{t-2}\\
x_{t-1}\\
x_t
\end{bmatrix}
$$

Nếu mỗi observation có $F$ features và lookback là $L$:

$$
Z_t\in\mathbb{R}^{L\times F}
$$

Dataset batch có thể trở thành:

$$
X\in\mathbb{R}^{B\times L\times F}
$$

Trong đó:

* $B$: batch size.
* $L$: sequence length.
* $F$: số feature.

Representation này phù hợp tự nhiên hơn với các sequence models như:

* RNN;
* LSTM;
* GRU;
* Transformer.

---

# 10. Hai cách biểu diễn cùng một Temporal Information

Cùng historical information:

```text
x(t-2), x(t-1), x(t)
```

có thể biểu diễn theo hai cách.

### Tabular

$$
[
x_{t-2},
x_{t-1},
x_t
]
$$

Tất cả được xem như các feature dimensions.

### Sequence

$$
\begin{bmatrix}
x_{t-2}\\
x_{t-1}\\
x_t
\end{bmatrix}
$$

Temporal dimension được giữ nguyên.

Điểm khác biệt:

```text
Tabular Representation
        ↓
Temporal information
được encode thành feature dimensions

Sequence Representation
        ↓
Temporal information
được giữ thành sequence dimension
```

Đây là một trong những quyết định quan trọng nhất khi chuyển từ preprocessing sang downstream AI.

---

# 11. Representation không chỉ là "ghép tất cả feature"

Một sai lầm phổ biến:

```text
Temporal Features
+
Lag Features
+
Rolling Features
=
Tất cả feature
```

rồi đưa trực tiếp vào model.

Điều này có thể tạo ra:

* redundancy;
* high dimensionality;
* highly correlated features;
* unnecessary computation;
* overfitting;
* representation không phù hợp với model.

Do đó cần một bước đánh giá:

$$
\boxed{
Feature\ Generation
\neq
Feature\ Selection
\neq
Feature\ Representation
}
$$

---

# 12. Feature Selection trước Representation cuối

Giả sử sau engineering chúng ta có:

$$
D=200
$$

features.

Không nhất thiết phải giữ cả 200.

Có thể thực hiện:

```text
Raw Features
     │
     ▼
Feature Engineering
     │
     ▼
200 Features
     │
     ▼
Feature Selection / Reduction
     │
     ▼
50 Features
     │
     ▼
Final Representation
```

Điều này đặc biệt quan trọng khi sử dụng nhiều:

* lag values;
* rolling windows;
* rolling statistics;
* temporal encodings.

Survey xem feature engineering trong một hệ sinh thái preprocessing rộng hơn, trong đó việc giảm hoặc biến đổi representation cũng là một phần quan trọng để kiểm soát complexity.

---

# 13. Feature Transformation

Representation cuối cùng có thể cần transformation.

Ví dụ một feature:

$$
x
$$

có thể được scale:

$$
x'=
\frac{x-\mu}{\sigma}
$$

hoặc được biến đổi bằng một transformation phù hợp.

Mục đích:

```text
Raw Feature
     ↓
Transformation
     ↓
Numerically suitable representation
```

Tuy nhiên cần phân biệt:

> **Feature representation** là cách biểu diễn information.

> **Feature scaling/transformation** là một phép biến đổi representation.

Hai khái niệm có liên quan nhưng không đồng nhất.

---

# 14. Representation và Feature Scaling

Giả sử representation:

$$
Z_t=
[
temperature,
humidity,
lag_1,
rolling_mean
]
$$

Các feature có thể có scale rất khác nhau:

```text
temperature      ~ 20
humidity         ~ 70
energy           ~ 1000
rolling_energy   ~ 10000
```

Nếu downstream model nhạy với scale, cần preprocessing thích hợp.

Có thể sử dụng:

$$
z'=
\frac{z-\mu}{\sigma}
$$

Nhưng thống kê scaling phải được học đúng theo pipeline train/validation/test.

Điểm này liên kết với các chương preprocessing trước:

```text
Data Cleaning
      ↓
Feature Engineering
      ↓
Feature Representation
      ↓
Scaling / Transformation
      ↓
Model
```

Không nên fit preprocessing statistics trên Test set.

---

# 15. Representation và Missing Values

Feature engineering có thể tạo ra missing values.

Ví dụ lag:

$$
x_{t-1}
$$

không tồn tại tại observation đầu tiên.

Rolling window:

$$
\mu_t^{(24)}
$$

không thể tính đầy đủ nếu chưa có đủ 24 observations.

Do đó:

```text
Raw Data
   ↓
Lag / Rolling
   ↓
Initial Missing Values
   ↓
Missing-value Strategy
   ↓
Final Representation
```

Điều này nối trực tiếp với:

```text
Chapter 3
01_missing_data.md
```

Tuy nhiên thứ tự xử lý phải được thiết kế theo pipeline cụ thể.

Không được mặc định rằng mọi missing value phát sinh sau feature engineering phải được xử lý bằng cùng một phương pháp.

---

# 16. Representation và Outliers

Rolling features có thể tạo ra representation nhạy với extreme values.

Ví dụ:

$$
x=
[10,11,12,100]
$$

Rolling mean có thể bị kéo lên mạnh bởi (100).

Do đó:

```text
Chapter 3
Outlier Detection
        │
        ▼
Data Quality
        │
        ▼
Chapter 5
Rolling / Feature Representation
```

Hai chapter liên kết với nhau nhưng có mục tiêu khác nhau:

$$
Chapter\ 3
\rightarrow
Data\ Quality
$$

$$
Chapter\ 5
\rightarrow
Information\ Representation
$$

---

# 17. Representation và Noise

Tương tự, nếu input chứa nhiều noise:

```text
Raw Signal
     │
     ▼
Noise
     │
     ▼
Rolling Statistics
```

rolling mean có thể tạo ra một representation ít dao động hơn.

Nhưng cần nhớ:

$$
Rolling\ Feature
\neq
Noise\ Reduction
$$

`03_rolling_features.md` đã phân biệt hai mục tiêu này.

Ở Chapter 3, noise reduction nhằm tạo ra signal sạch hơn.

Ở Chapter 5, rolling statistic được tạo ra để cung cấp thêm information cho model.

---

# 18. Feature Redundancy

Sau khi kết hợp temporal, lag và rolling features:

$$
Z_t=
[
T_t,
X_t,
L_t,
R_t
]
$$

có thể tồn tại redundancy.

Ví dụ:

$$
x_t
$$

và:

$$
rolling_mean_t^{(3)}
$$

có thể tương quan cao.

Hoặc:

$$
lag_1,\ lag_2,\ lag_3
$$

có thể chứa information tương tự trong một signal có autocorrelation cao.

Do đó representation cần được đánh giá về:

* relevance;
* redundancy;
* dimensionality;
* computational cost;
* downstream performance.

---

# 19. Dimensionality

Giả sử:

* (F): original features;
* (K): số lag;
* (R): số rolling statistics;
* (W): số window sizes;
* (T): số temporal features.

Feature dimension có thể tăng gần theo:

$$
D
\approx
T+F+FK+FRW
$$

Đây chỉ là một cách mô tả về mặt cấu trúc, không phải công thức bắt buộc cho mọi pipeline.

Điểm quan trọng:

$$
K,R,W\uparrow
\Rightarrow
D\uparrow
$$

Feature engineering có thể nhanh chóng biến một dataset đơn giản thành feature space rất lớn.

---

# 20. Feature Representation và Curse of Dimensionality

Khi (D) tăng quá lớn:

```text
Feature Count
      │
      ▼
Higher Dimensional Space
      │
      ├── More computation
      ├── More memory
      ├── More redundancy
      └── Potential overfitting
```

Do đó:

$$
\boxed{
More\ Features
\neq
Better\ Representation
}
$$

Một representation tốt phải giữ information hữu ích trong khi hạn chế complexity không cần thiết.

Đây là lý do Feature Engineering cần được đánh giá cùng với downstream model, phù hợp với tinh thần empirical analysis của survey.

---

# 21. Feature Representation và Model Architecture

Representation không thể tách hoàn toàn khỏi model.

Ví dụ:

### Linear Model

```text
Z_t
 │
 ▼
Fixed-dimensional vector
 │
 ▼
Linear Model
```

### Tree-based Model

```text
Z_t
 │
 ▼
Tabular Features
 │
 ▼
Decision Tree / Ensemble
```

### LSTM

```text
Z_t
 │
 ▼
[L × F]
 │
 ▼
LSTM
```

### Transformer

```text
Z_t
 │
 ▼
[L × F]
 │
 ▼
Embedding / Projection
 │
 ▼
Transformer
```

Do đó:

$$
\boxed{
Representation
\leftrightarrow
Model\ Architecture
}
$$

Một representation tốt cho Random Forest chưa chắc là representation tốt nhất cho Transformer.

---

# 22. Feature Representation và Temporal Models

Đây là điểm đặc biệt quan trọng đối với Time-Series.

Một pipeline có thể chọn:

```text
Option A

Time Series
    ↓
Lag + Rolling
    ↓
Tabular Representation
    ↓
ML Model
```

hoặc:

```text
Option B

Time Series
    ↓
Temporal Window
    ↓
Sequence Representation
    ↓
LSTM / Transformer
```

Hai pipeline đều có thể sử dụng historical information nhưng encode information theo cách khác nhau.

### Option A

Model nhận:

$$
Z_t\in\mathbb{R}^{D}
$$

### Option B

Model nhận:

$$
Z_t\in\mathbb{R}^{L\times F}
$$

Đây là lý do không thể nói một representation là tốt trong mọi trường hợp.

---

# 23. Feature Representation trong Forecasting

Giả sử task:

$$
X_{t-L+1:t}
\rightarrow
y_{t+H}
$$

thì representation có thể giữ nguyên temporal dimension:

$$
X_t\in\mathbb{R}^{L\times F}
$$

Trong trường hợp này:

```text
Historical Window
       │
       ▼
Sequence Representation
       │
       ▼
Forecasting Model
       │
       ▼
Future Target
```

Nếu thay vào đó flatten:

$$
X_t
\rightarrow
\mathbb{R}^{L\times F}
\rightarrow
\mathbb{R}^{LF}
$$

thì temporal structure được chuyển thành feature dimensions.

Điều này có thể phù hợp với một số tabular models nhưng làm thay đổi cách model nhìn nhận temporal structure.

---

# 24. Representation và Temporal Integrity

Một representation time-series hợp lệ phải bảo toàn temporal ordering.

Ví dụ:

```text
t-3 → t-2 → t-1 → t
```

không được biến thành:

```text
t-1 → t-3 → t → t-2
```

đối với sequence representation.

Đồng thời khi tạo lag/rolling:

$$
x_{t-k}
$$

phải thực sự thuộc về thời điểm (t-k).

Do đó feature representation phụ thuộc vào:

* timestamp;
* ordering;
* sampling interval;
* continuity;
* temporal boundaries.

Đây là lý do `01_temporal_features.md` là nền tảng của toàn bộ Chapter 5.

---

# 25. Representation và Temporal Leakage

Một representation có thể trông hoàn toàn hợp lệ về mặt shape nhưng vẫn sai về mặt temporal information.

Ví dụ:

```text
Target: y(t+1)

Features:
x(t-2)
x(t-1)
x(t)
x(t+1)   ← Leakage
```

Shape có thể hoàn toàn đúng:

$$
X\in\mathbb{R}^{N\times D}
$$

nhưng information flow sai.

Do đó:

$$
\boxed{
Valid\ Shape
\neq
Valid\ Time-Series\ Representation
}
$$

Representation phải đảm bảo:

$$
Information_{feature}
\subseteq
Information_{available\ at\ prediction\ time}
$$

---

# 26. Representation và Train / Validation / Test

Một pipeline đúng cần giữ temporal separation:

```text
Train
──────────────────
       │
       ▼
Feature Engineering
       │
       ▼
Train Representation

Validation
──────────────────
       │
       ▼
Validation Representation

Test
──────────────────
       │
       ▼
Test Representation
```

Không được để information từ Validation/Test quay ngược vào quá trình xây dựng representation của Train.

Đặc biệt với:

* rolling statistics;
* normalization;
* feature selection;
* dimensionality reduction.

Các bước học được parameters/statistics từ dữ liệu phải tuân thủ temporal split.

---

# 27. Representation Quality

Một feature representation tốt không chỉ được đánh giá bằng số lượng feature.

Có thể xem xét:

### Information

Representation có giữ được information quan trọng không?

### Relevance

Feature có liên quan đến target/task không?

### Redundancy

Có quá nhiều feature giống nhau không?

### Stability

Representation có ổn định khi dữ liệu thay đổi không?

### Complexity

Chi phí computation và memory có chấp nhận được không?

### Downstream Performance

Representation có hỗ trợ model tốt hơn không?

Có thể hình dung:

```text
                 Representation
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
   Information     Complexity     Model Performance
       │               │               │
       └───────────────┼───────────────┘
                       ▼
               Final Evaluation
```

Đây phù hợp với tinh thần empirical analysis của survey: preprocessing nên được đánh giá cả về data quality và downstream AI performance.

---

# 28. Một Pipeline Feature Representation hoàn chỉnh

Từ toàn bộ Chapter 5:

```text
                         TIME SERIES
                              │
                              ▼
                 01 Temporal Features
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
          Time Information          Temporal Context
                 │                         │
                 └────────────┬────────────┘
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
                   Window Statistics
                              │
                              ▼
               Feature Construction
                              │
                              ▼
                Feature Selection /
                   Transformation
                              │
                              ▼
                04 Feature Representation
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
              Tabular Form       Sequence Form
                    │                   │
                    ▼                   ▼
               ML Models        LSTM / Transformer
```

Đây là kiến trúc logic của Chapter 5.

---

# 29. Mối liên hệ giữa 4 file

## `01_temporal_features.md`

Trả lời:

> **Time-Series có information nào liên quan đến thời gian?**

Kết quả:

$$
Temporal\ Information
$$

↓

## `02_lag_features.md`

Trả lời:

> **Làm sao đưa historical information vào feature space?**

Kết quả:

$$
Historical\ Features
$$

↓

## `03_rolling_features.md`

Trả lời:

> **Làm sao tổng hợp historical observations thành local temporal information?**

Kết quả:

$$
Window\ Features
$$

↓

## `04_feature_representation.md`

Trả lời:

> **Làm sao tổ chức tất cả information thành input cuối cùng cho model?**

Kết quả:

$$
Final\ Representation
$$

Do đó:

$$
\boxed{
Temporal
\rightarrow
Lag
\rightarrow
Rolling
\rightarrow
Representation
}
$$

---

# 30. Feature Representation không phải bước cuối của toàn bộ ML Pipeline

Cần phân biệt:

```text
Chapter 5
Feature Engineering
        ↓
Feature Representation
```

với:

```text
Complete ML Pipeline
        ↓
Data Cleaning
        ↓
Feature Engineering
        ↓
Feature Representation
        ↓
Scaling / Transformation
        ↓
Dataset Construction
        ↓
Model
        ↓
Evaluation
```

Feature Representation là **kết quả của quá trình feature engineering**, nhưng vẫn còn các bước preprocessing/model preparation khác tùy pipeline.

Điều này cũng phù hợp với survey: preprocessing không phải một operation đơn lẻ mà là một pipeline gồm nhiều kỹ thuật có thể được kết hợp tùy application và downstream model.

---

# 31. Ví dụ tổng hợp

Giả sử có dữ liệu:

```text
timestamp          energy
08:00               100
08:10               110
08:20               120
08:30               140
08:40               130
```

### Bước 1 — Temporal Feature

Từ timestamp:

$$
hour=8
$$

### Bước 2 — Lag

Tại 08:40:

$$
lag_1=140
$$

$$
lag_2=120
$$

### Bước 3 — Rolling

Với window 3:

$$
	ext{rolling\_mean} =

\frac{120+140+130}{3}

= 130
$$

### Bước 4 — Representation

Có thể tạo:

$$
Z_t=
[
hour,
energy_t,
lag_1,
lag_2,
rolling_mean
]
$$

Kết quả:

```text
[
  8,
  130,
  140,
  120,
  130
]
```

Đây là một **tabular feature representation**.

---

# 32. Nếu sử dụng Sequence Representation

Thay vì flatten:

```text
[
  8,
  130,
  140,
  120,
  130
]
```

có thể giữ historical sequence:

$$
Z_t=
\begin{bmatrix}
x_{t-2}\
x_{t-1}\
x_t
\end{bmatrix}
$$

và thêm temporal features tương ứng:

```text
t-2 ── features
t-1 ── features
 t ── features
```

Khi đó representation giữ lại temporal ordering.

Đây là nền tảng để chuyển sang các architecture sequence-based.

---

# 33. Những điều không được hiểu sai

### Không phải:

> Feature representation càng lớn càng tốt.

Mà:

$$
Useful\ Information

>

Raw\ Feature\ Count
$$

---

### Không phải:

> Lag và rolling là hai preprocessing độc lập.

Mà:

```text
Lag
 ↓
Historical Points
 ↓
Rolling
 ↓
Historical Window Summary
```

chúng có quan hệ trực tiếp.

---

### Không phải:

> Tabular representation luôn tốt hơn sequence representation.

Representation phải phụ thuộc vào downstream model.

---

### Không phải:

> Rolling mean hoặc lag feature là contribution riêng của survey.

Paper là survey về time-series preprocessing và empirical analysis, không đề xuất một "Lag/Rolling Feature Representation Algorithm" riêng.

---

### Không phải:

> Feature Engineering chỉ là tạo feature.

Mà:

$$
	ext{Feature Engineering} =

Construction
+
Transformation
+
Selection
+
Representation\ Design
$$

tùy theo pipeline và taxonomy đang xét.

---

# 34. Key Takeaways

## 1. Feature Representation là kết quả của Chapter 5

$$
\boxed{
Temporal
\rightarrow
Lag
\rightarrow
Rolling
\rightarrow
Representation
}
$$

---

## 2. Representation biến information thành model input

$$
Raw\ Information
\rightarrow
Z_t
\rightarrow
Model
$$

---

## 3. Có hai hướng biểu diễn quan trọng

### Tabular

$$
Z_t\in\mathbb{R}^{D}
$$

### Sequence

$$
Z_t\in\mathbb{R}^{L\times F}
$$

---

## 4. Representation phải phù hợp với downstream model

$$
Representation
\leftrightarrow
Model
$$

---

## 5. Không được bỏ qua temporal integrity

Một representation có shape đúng nhưng chứa future information vẫn là representation sai.

$$
Valid\ Shape
\neq
Valid\ Temporal\ Information
$$

---

## 6. Feature engineering cần kiểm soát dimensionality

$$
More\ Features
\neq
Better\ Model
$$

Cần cân bằng:

$$
Information
\leftrightarrow
Complexity
$$

---

# 35. Kết luận Chapter 5

Chapter 5 bắt đầu từ một observation đơn giản:

> **Time-Series Data chứa information theo thời gian.**

Từ đó xây dựng từng lớp representation:

$$
\boxed{
Temporal\ Information
}
$$

↓

$$
\boxed{
Historical\ Information
}
$$

↓

$$
\boxed{
Window\ Information
}
$$

↓

$$
\boxed{
Final\ Feature\ Representation
}
$$

Cụ thể:

```text
01 Temporal Features
        ↓
Hiểu temporal context

02 Lag Features
        ↓
Đưa historical values vào representation

03 Rolling Features
        ↓
Tóm tắt historical windows

04 Feature Representation
        ↓
Tổ chức toàn bộ information
thành model input
```

Do đó `04_feature_representation.md` là điểm kết thúc tự nhiên của Chapter 5:

$$
\boxed{
Raw\ Time\ Series
\rightarrow
Temporal\ Features
\rightarrow
Lag
\rightarrow
Rolling
\rightarrow
Feature\ Representation
\rightarrow
AI
}
$$

Theo tinh thần của survey, **không tồn tại một representation tối ưu cho mọi time-series dataset**. Representation phải được lựa chọn dựa trên đặc điểm dữ liệu, mục tiêu ứng dụng, tài nguyên và downstream AI algorithm; cuối cùng cần được đánh giá bằng cả chất lượng dữ liệu và hiệu năng của AI system.

