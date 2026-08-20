# 04. Comparison of Data Cleaning Methods

## 1. Tổng quan

Data Cleaning là lớp preprocessing đầu tiên nhằm xử lý các vấn đề về chất lượng dữ liệu trước khi thực hiện các bước transformation, feature engineering hoặc đưa dữ liệu vào mô hình AI.

Trong Time-Series Data, các vấn đề chính được xem xét gồm:

```text
Data Cleaning
│
├── Missing Data
│
├── Outliers
│
└── Noise
```

Ba vấn đề này có quan hệ với nhau nhưng không đồng nhất:

$$
\boxed{
Missing\ Data
\neq
Outlier
\neq
Noise
}
$$

* **Missing Data**: observation không tồn tại hoặc không được ghi nhận.
* **Outlier**: observation có hành vi bất thường so với context hoặc distribution.
* **Noise**: biến động không mong muốn chồng lên underlying signal.

Vì vậy, không thể sử dụng một preprocessing method duy nhất cho toàn bộ Data Cleaning.

Mục tiêu của comparison là xác định:

> **Phương pháp nào phù hợp với loại vấn đề nào, trong điều kiện nào và với trade-off nào?**

## 1.1. Cách đọc kết quả theo bài báo

Empirical analysis của survey không so sánh mọi phương pháp trong cùng một thí nghiệm độc lập. Tác giả xây dựng một preprocessing pipeline trên bộ dữ liệu AirQuality: thay thế missing bằng NaN, phát hiện outlier bằng Grubbs cho feature có phân phối Gaussian hoặc IQR otherwise, thay outlier bằng cubic spline, dùng cubic spline cho missing đơn lẻ và EM cho missing theo chuỗi, sau đó đánh giá mô hình LSTM bằng RMSE, MAE và MAPE. Vì vậy, các bảng dưới đây là khung lựa chọn phương pháp, không phải bảng xếp hạng hiệu năng phổ quát.

---

# 2. Data Cleaning trong kiến trúc preprocessing

Survey không xem Data Cleaning là toàn bộ quá trình preprocessing.

Có thể đặt Data Cleaning trong pipeline lớn hơn:

```text
Raw Time-Series Data
        │
        ▼
┌─────────────────────┐
│    Data Cleaning    │
│                     │
│ Missing Data        │
│ Outlier Detection   │
│ Noise Reduction     │
└──────────┬──────────┘
           │
           ▼
Data Transformation
           │
           ▼
Feature Engineering
           │
           ▼
Feature Selection
           │
           ▼
AI / ML / DL
```

Điều này rất quan trọng khi đọc survey:

> **Data Cleaning giải quyết vấn đề về data quality, nhưng không phải toàn bộ preprocessing pipeline.**

Các chương sau của survey tiếp tục xử lý transformation, feature engineering, dimensionality reduction, fusion và compression.

---

# 3. So sánh Missing Data, Outlier và Noise

| Vấn đề        | Bản chất               | Ví dụ                  | Mục tiêu xử lý             |
| ------------- | ---------------------- | ---------------------- | -------------------------- |
| Missing Data  | Thiếu observation      | `10, 11, NaN, 13`      | Estimate / Impute          |
| Outlier       | Observation bất thường | `10, 11, 100, 13`      | Detect → Validate → Handle |
| Noise         | Biến động ngẫu nhiên   | `10.2, 9.8, 10.3, 9.7` | Denoise                    |
| Normal Signal | Hành vi hợp lệ         | `10, 11, 12, 13`       | Preserve                   |

Có thể biểu diễn:

```text
Missing
   ↓
No observation
   ↓
Imputation

Outlier
   ↓
Abnormal observation
   ↓
Detection + Decision

Noise
   ↓
Unwanted variation
   ↓
Filtering / Denoising
```

Điểm quan trọng là **cách xử lý hoàn toàn khác nhau**.

Không nên:

```text
Missing → Smoothing
Outlier → Mean Fill
Noise   → Delete
```

một cách máy móc.

---

# 4. So sánh phương pháp xử lý Missing Data

Các phương pháp Missing Data có thể được chia thành ba mức độ chính:

```text
Simple
  ↓
Statistical
  ↓
Model-based
```

## 4.1. Simple Imputation

Ví dụ:

* Forward Fill
* Backward Fill
* Mean
* Median

Ưu điểm:

* dễ triển khai;
* computational cost thấp;
* phù hợp baseline;
* phù hợp với missing rate thấp.

Nhược điểm:

* ít khai thác temporal dependency;
* có thể làm thay đổi distribution;
* có thể tạo artificial patterns.

---

## 4.2. Interpolation

Các phương pháp:

* Linear Interpolation
* Polynomial Interpolation
* Spline

Tận dụng temporal continuity:

$$
x_t
\approx
f(x_{t-1},x_{t+1})
$$

Phù hợp với các signal thay đổi tương đối liên tục.

Tuy nhiên interpolation không phù hợp với mọi loại time series, đặc biệt khi missing block dài hoặc signal có biến động đột ngột.

---

## 4.3. Model-based Imputation

Có thể sử dụng:

```text
Regression
KNN
AR / ARIMA
Kalman Filter
RNN
LSTM
Transformer
```

Ưu điểm:

* khai thác temporal dependency;
* có thể khai thác multivariate dependency;
* phù hợp với missing pattern phức tạp.

Nhược điểm:

* computational cost cao hơn;
* cần lựa chọn model;
* dễ đưa thêm assumptions vào preprocessing.

---

# 5. So sánh Outlier Detection

Outlier Detection có thể chia thành:

```text
Statistical
     ↓
Window-based
     ↓
Robust
     ↓
Model-based
     ↓
Learning-based
```

## 5.1. Statistical Methods

Ví dụ:

$$
z_t=\frac{x_t-\mu}{\sigma}
$$

hoặc:

$$
IQR=Q_3-Q_1
$$

Ưu điểm:

* đơn giản;
* nhanh;
* dễ giải thích;
* phù hợp với resource-constrained environments.

Nhược điểm:

* phụ thuộc assumptions;
* global statistics có thể không phù hợp với non-stationary series;
* khó xử lý contextual anomalies.

---

## 5.2. Window-based Methods

Thay vì tính threshold trên toàn bộ dataset, statistics được tính trên local window:

$$
W_t=
{x_{t-w+1},...,x_t}
$$

Điều này cho phép threshold thay đổi theo thời gian.

Ưu điểm:

* phù hợp với local behavior;
* thích hợp với streaming data;
* có thể xử lý một phần non-stationarity.

Nhược điểm:

* phụ thuộc window size;
* window quá nhỏ → unstable;
* window quá lớn → mất local characteristics.

---

## 5.3. Robust Methods

Sử dụng:

* Median;
* IQR;
* MAD;
* Robust Scale Estimators.

Ưu điểm:

$$
\text{Less sensitive to extreme values}
$$

Đặc biệt hữu ích khi chính outliers có thể làm distortion của mean và standard deviation.

---

## 5.4. Model-based Methods

Dựa trên residual:

$$
e_t=x_t-\hat{x}_t
$$

Nếu:

$$
|e_t| \gt \tau
$$

thì observation được xem là potential anomaly.

Ưu điểm:

* hiểu temporal dynamics;
* phù hợp với complex time series.

Nhược điểm:

* computational cost cao;
* phụ thuộc chất lượng model;
* cần training hoặc parameter estimation.

---

# 6. So sánh Noise Reduction

Noise Reduction chủ yếu tìm cách estimate underlying signal:

$$
x_t=s_t+n_t
$$

và:

$$
\hat{s}_t\approx s_t
$$

Các phương pháp có thể phân thành:

```text
Smoothing
   ↓
Filtering
   ↓
Frequency-domain
   ↓
State-space
   ↓
Learning-based
```

---

## 6.1. Smoothing

Ví dụ:

* Moving Average;
* Weighted Moving Average;
* Exponential Smoothing.

Đặc điểm:

* computational cost thấp;
* dễ triển khai;
* phù hợp streaming.

Trade-off:

$$
\text{More smoothing}
\leftrightarrow
\text{More information loss}
$$

---

## 6.2. Filtering

Ví dụ:

* Median Filter;
* Savitzky-Golay.

Có khả năng giữ local structure tốt hơn một số phương pháp smoothing đơn giản.

---

## 6.3. Frequency-domain

Ví dụ:

* Fourier-based filtering;
* Low-pass filtering;
* Wavelet-based denoising.

Phù hợp khi noise có đặc tính frequency rõ ràng.

Nhưng cần giả định:

> Noise và useful signal có thể phân biệt tương đối tốt trong frequency domain.

---

## 6.4. State-space

Ví dụ:

* Kalman Filter.

Mô hình hóa:

$$
x_t=Fx_{t-1}+w_t
$$

và:

$$
z_t=Hx_t+v_t
$$

Phù hợp với hệ thống dynamic và streaming.

---

# 7. Comparison Matrix

Bảng dưới đây tổng hợp trade-off giữa các nhóm phương pháp:

| Method                | Missing | Outlier | Noise | Temporal Dependency |     Complexity | Streaming |
| --------------------- | ------: | ------: | ----: | ------------------: | -------------: | --------: |
| Mean / Median         |       ✓ |       — |     — |                Thấp |           Thấp |         ✓ |
| Forward Fill          |       ✓ |       — |     — |                Thấp |           Thấp |         ✓ |
| Interpolation         |       ✓ |       — |     — |          Trung bình |           Thấp |         △ |
| KNN                   |       ✓ |       △ |     — |             Thấp–TB | Trung bình–Cao |         △ |
| Regression            |       ✓ |       △ |     — |          Trung bình |     Trung bình |         △ |
| Z-score               |       — |       ✓ |     — |                Thấp |           Thấp |         ✓ |
| IQR                   |       — |       ✓ |     — |             Thấp–TB |           Thấp |         ✓ |
| MAD                   |       — |       ✓ |     — |             Thấp–TB |           Thấp |         ✓ |
| Moving Average        |       — |       △ |     ✓ |               Local |           Thấp |         ✓ |
| Exponential Smoothing |       — |       △ |     ✓ |            Temporal |           Thấp |         ✓ |
| Median Filter         |       — |       △ |     ✓ |               Local |           Thấp |         ✓ |
| Wavelet               |       — |       — |     ✓ |         Multi-scale | Trung bình–Cao |         △ |
| Kalman Filter         |       △ |       △ |     ✓ |                 Cao |     Trung bình |         ✓ |
| Deep Learning         |       ✓ |       ✓ |     ✓ |             Rất cao |    Cao–Rất cao |         △ |

Ký hiệu:

```text
✓  : phù hợp trực tiếp
△  : có thể sử dụng tùy trường hợp
—  : không phải mục tiêu chính
```

Bảng này không phải ranking về performance.

Nó mô tả **phạm vi sử dụng và trade-off**.

---

# 8. So sánh theo Computational Cost

Một trong những khác biệt quan trọng giữa các phương pháp là computational requirement.

Có thể hình dung:

```text
Low Cost
│
├── Mean / Median
├── Forward Fill
├── IQR
├── Z-score
├── Moving Average
│
├── Interpolation
├── Exponential Smoothing
├── Kalman
│
├── KNN
├── Wavelet
├── Model-based
│
└── Deep Learning
      ↓
High Cost
```

Các phương pháp computationally cheap phù hợp hơn với:

* Edge devices;
* IoT;
* streaming;
* real-time preprocessing.

Các phương pháp phức tạp hơn phù hợp với:

* offline preprocessing;
* large-scale infrastructure;
* complex temporal patterns;
* high-value applications.

Survey đặc biệt xem xét preprocessing trong bối cảnh Edge/IoT, nơi computational resource, storage và communication cost là các constraint quan trọng.

---

# 9. So sánh theo Temporal Dependency

Một tiêu chí quan trọng hơn computational cost là:

> **Phương pháp có hiểu cấu trúc thời gian hay không?**

### Không hoặc ít temporal modeling

```text
Mean
Median
Z-score
IQR
```

Chủ yếu dựa trên distribution.

### Local temporal modeling

```text
Moving Window
Moving Average
Interpolation
Median Filter
```

Sử dụng lân cận của observation.

### Strong temporal modeling

```text
ARIMA
Kalman
RNN
LSTM
Transformer
```

Mô hình hóa dependency theo thời gian.

Có thể biểu diễn:

$$
\text{Temporal Awareness}
:
Statistical
\lt
Local
\lt
Model-based
\lt
Deep Learning
$$

Tuy nhiên temporal awareness cao hơn **không đồng nghĩa luôn tốt hơn**.

Model phức tạp chỉ đáng sử dụng khi complexity của dữ liệu thực sự yêu cầu.

---

# 10. So sánh theo Robustness

Một preprocessing method phải chịu được:

* extreme values;
* changing variance;
* non-stationarity;
* missing blocks;
* noise bursts.

Ví dụ:

### Mean

Nhạy với outlier:

$$
\mu
\rightarrow
\text{strongly affected}
$$

### Median

Robust hơn:

$$
median
\rightarrow
\text{less affected}
$$

### IQR / MAD

Robust statistics:

$$
\text{Extreme values}
\rightarrow
\text{limited influence}
$$

Do đó khi data quality kém, robust methods thường có lợi thế hơn các phương pháp dựa trực tiếp trên mean và variance.

---

# 11. So sánh theo Data Characteristics

Không nên chọn preprocessing method trước khi hiểu dữ liệu.

Có thể sử dụng decision matrix:

| Data Characteristic        | Phương pháp ưu tiên          |
| -------------------------- | ---------------------------- |
| Missing ít                 | Simple Imputation            |
| Missing ngắn               | Interpolation                |
| Missing dài                | Model-based Imputation       |
| Outlier rõ ràng            | IQR / MAD                    |
| Local anomaly              | Sliding Window               |
| Noise nhỏ                  | Simple Smoothing             |
| Noise có spike             | Median Filter                |
| Frequency-specific noise   | Fourier / Wavelet            |
| Strong temporal dependency | Kalman / Time-series Model   |
| Streaming                  | Online / Incremental Methods |
| Edge resource hạn chế      | Lightweight Methods          |
| Complex multivariate       | Model-based / Learning-based |

Đây là cách tiếp cận quan trọng hơn việc tìm một thuật toán “tốt nhất”.

---

# 12. Data Cleaning và Edge Computing

Survey đặt preprocessing trong một bối cảnh rộng hơn: dữ liệu có thể được xử lý tại **Edge** trước khi truyền về hệ thống trung tâm.

Kiến trúc:

```text
Sensors
   │
   ▼
Edge Device
   │
   ├── Missing Handling
   ├── Outlier Detection
   ├── Noise Reduction
   │
   ▼
Clean Data
   │
   ▼
Network
   │
   ▼
Cloud / Central AI
```

Lợi ích:

$$
\boxed{
Cleaning\ at\ Edge
\rightarrow
Less\ Data
\rightarrow
Less\ Communication
\rightarrow
Less\ Central\ Computation
}
$$

Điều này làm computational efficiency trở thành một tiêu chí quan trọng khi so sánh các preprocessing methods.

Một phương pháp có accuracy tốt hơn nhưng computational cost quá cao có thể không phù hợp với Edge device.

---

# 13. Data Cleaning và AI Performance

Mục tiêu cuối cùng của Data Cleaning không phải chỉ là:

> tạo ra dữ liệu nhìn “đẹp”.

Mục tiêu là:

> tạo ra dữ liệu có chất lượng tốt hơn cho downstream task.

Pipeline:

```text
Raw Data
   ↓
Data Cleaning
   ↓
Clean Data
   ↓
Feature Engineering
   ↓
AI Model
   ↓
Performance
```

Do đó một cleaning method nên được đánh giá theo:

$$
\text{Data Quality}
+
\text{Information Preservation}
+
\text{AI Performance}
+
\text{Computational Cost}
$$

Một phương pháp làm giảm noise rất mạnh nhưng đồng thời loại bỏ feature quan trọng có thể làm model performance giảm.

Vì vậy:

$$
\boxed{
Better\ Cleanliness
\neq
Better\ AI\ Performance
}
$$

---

# 14. Data Cleaning Trade-offs

Không có phương pháp nào tối ưu đồng thời mọi tiêu chí.

Có thể biểu diễn:

```text
                 Data Quality
                     ▲
                     │
                     │
      Robustness     │     Accuracy
                     │
                     │
                     └──────────────►
                       Complexity
```

Các trade-off chính:

### Accuracy vs Complexity

Model-based methods có thể chính xác hơn nhưng phức tạp hơn.

### Smoothing vs Information Preservation

Smoothing mạnh hơn:

$$
Noise\downarrow
$$

nhưng:

$$
Signal\ information\downarrow
$$

### Robustness vs Simplicity

Robust methods xử lý dữ liệu bất thường tốt hơn nhưng có thể cần thêm computation hoặc parameter tuning.

### Central Processing vs Edge Processing

Central processing:

```text
More computation
More communication
```

Edge processing:

```text
Less communication
Limited computation
```

---

# 15. Một điểm quan trọng: Không nên xử lý mọi thứ bằng một bước

Một sai lầm phổ biến là xây dựng pipeline:

```text
Raw Data
   ↓
One Cleaning Algorithm
   ↓
Clean Data
```

Trong thực tế nên:

```text
Raw Data
   ↓
Data Profiling
   ↓
Identify Problem
   │
   ├── Missing?
   │      ↓
   │   Imputation
   │
   ├── Outlier?
   │      ↓
   │   Detection
   │
   └── Noise?
          ↓
       Denoising
```

Tức là:

$$
\boxed{
Problem
\rightarrow
Method
}
$$

thay vì:

$$
\boxed{
Method
\rightarrow
Problem
}
$$

---

# 16. Thứ tự xử lý

Không có một thứ tự cố định cho mọi dataset.

Tuy nhiên cần xem xét dependency giữa các bước.

Ví dụ:

```text
Missing
   ↓
Imputation
   ↓
Outlier Detection
   ↓
Noise Reduction
```

hoặc:

```text
Outlier Detection
   ↓
Correction
   ↓
Missing Imputation
```

có thể phù hợp hơn nếu outlier cần được chuyển thành missing trước khi interpolation.

Vì vậy thứ tự phải dựa trên:

* data generation process;
* missing pattern;
* outlier mechanism;
* noise characteristics;
* downstream task.

---

# 17. Temporal Integrity

Đối với Time-Series Forecasting, đây là tiêu chí bắt buộc.

Một preprocessing step không được sử dụng information từ tương lai để xử lý quá khứ.

Nguyên tắc:

$$
\boxed{
x_t^{clean}=f(x_1,\ldots,x_t)
}
$$

nếu pipeline hoạt động online/causal.

Không nên:

$$
x_t^{clean}=f(x_1,\ldots,x_t,x_{t+1},...)
$$

nếu $x_{t+1},...$ không tồn tại tại thời điểm $t$.

Điều này đặc biệt quan trọng với:

* interpolation;
* centered moving average;
* smoothing;
* outlier threshold estimation;
* model-based preprocessing.

---

# 18. Data Cleaning trong Train / Validation / Test

Một preprocessing pipeline đúng cần phân biệt:

```text
Train
Validation
Test
```

Không được để thông tin của Validation/Test ảnh hưởng đến preprocessing statistics của Train.

Ví dụ:

```text
Full Dataset
      ↓
❌ Calculate Global Statistics
      ↓
Train + Validation + Test
```

Thay vào đó:

```text
Train
  ↓
Fit Cleaning / Transformation Parameters
  ↓
Train Transformation
  ↓
Validation / Test Transformation
```

Trong forecasting, temporal split càng làm nguyên tắc này quan trọng hơn.

---

# 19. Tiêu chí lựa chọn phương pháp

Có thể tổng hợp thành 6 câu hỏi:

### 1. Vấn đề gì đang xảy ra?

```text
Missing?
Outlier?
Noise?
```

### 2. Temporal dependency mạnh đến đâu?

```text
Weak
   ↓
Strong
```

### 3. Dataset có non-stationarity không?

Nếu có, global statistics có thể không phù hợp.

### 4. Cần real-time không?

Nếu có:

```text
Latency
+
Memory
+
Computation
```

trở thành constraints.

### 5. Dữ liệu được xử lý ở đâu?

```text
Cloud
Server
Edge
Sensor
```

### 6. Downstream task là gì?

Ví dụ:

```text
Forecasting
Classification
Anomaly Detection
Regression
```

Cùng một preprocessing method có thể phù hợp với task này nhưng không phù hợp với task khác.

---

# 20. Comparison Framework

Có thể đánh giá một preprocessing method theo framework:

$$
Score =
f(
Data\ Quality,
Robustness,
Information\ Preservation,
AI\ Performance,
Complexity,
Latency
)
$$

Không có một scalar score chung cho mọi ứng dụng.

Thay vào đó cần xác định **priority**.

Ví dụ:

### IoT Edge

```text
Priority:

Low Latency
Low Memory
Low Communication
Acceptable Accuracy
```

### Medical Time Series

```text
Priority:

Signal Preservation
Robustness
Reliability
Interpretability
```

### Offline Forecasting

```text
Priority:

Forecasting Performance
Temporal Integrity
Reproducibility
```

---

# 21. Tổng hợp Comparison

Có thể rút gọn toàn bộ Data Cleaning thành:

```text
                    DATA CLEANING
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
     Missing           Outlier            Noise
        │                 │                 │
        ▼                 ▼                 ▼
   Imputation          Detection         Denoising
        │                 │                 │
        ├───────┬─────────┴─────────┬───────┤
        │       │                   │       │
        ▼       ▼                   ▼       ▼
    Simple   Statistical       Window   Model-based
        │       │                   │       │
        └───────┴──────────┬────────┴───────┘
                           ▼
                    Clean Time Series
                           │
                           ▼
                 Transformation
                           │
                           ▼
                 Feature Engineering
                           │
                           ▼
                        AI Model
```

---

# 22. Những điểm quan trọng cần ghi nhớ

## 22.1. Không có một phương pháp Data Cleaning tốt nhất

Phương pháp phải phụ thuộc vào:

$$
\boxed{
Data\ Characteristics
+
Task
+
Resource
}
$$

---

## 22.2. Statistical methods là baseline quan trọng

Các phương pháp như:

```text
Mean
Median
IQR
Z-score
Moving Average
```

đơn giản nhưng rất hữu ích vì:

* dễ hiểu;
* dễ triển khai;
* computational cost thấp;
* dễ benchmark.

---

## 22.3. Temporal context rất quan trọng

Time Series khác tabular data ở dependency:

$$
x_t\leftrightarrow x_{t-1},x_{t-2},...
$$

Do đó local/window-based và model-based methods thường có lợi thế khi temporal structure mạnh.

---

## 22.4. Robustness quan trọng hơn sự đơn giản khi data quality thấp

Khi dataset có nhiều extreme values:

```text
Mean / Std
    ↓
Sensitive

Median / IQR / MAD
    ↓
More Robust
```

---

## 22.5. Data Cleaning phải bảo vệ information

Mục tiêu không phải:

$$
\text{Maximum Cleaning}
$$

mà là:

$$
\boxed{
\text{Maximum Useful Information Preservation}
}
$$

---

# 23. Kết quả empirical cần nhớ

Trong thiết lập AirQuality của paper, pipeline đầy đủ cho kết quả LSTM tốt hơn pipeline tối thiểu: RMSE trung bình giảm từ `0.60` xuống `0.32`, MAE từ `0.45` xuống `0.23`, và MAPE từ `51.41%` xuống `25.26%`. Đây là kết quả của **toàn bộ pipeline và dataset/thí nghiệm cụ thể**, không đủ để kết luận rằng một thuật toán cleaning riêng lẻ luôn tốt hơn thuật toán khác.

Paper cũng ghi nhận cubic spline cho missing đơn lẻ và EM cho missing theo chuỗi là một hybrid phù hợp trong thí nghiệm; lựa chọn này nên được kiểm chứng lại bằng validation theo thời gian trước khi áp dụng cho dữ liệu khác.

---

## 22.6. Edge làm thay đổi tiêu chí lựa chọn

Trong Edge/IoT:

$$
Accuracy
$$

không phải tiêu chí duy nhất.

Cần đồng thời xem xét:

$$
Memory,\ CPU,\ Latency,\ Bandwidth,\ Energy
$$

Đây là một trong những lý do survey mở rộng discussion từ preprocessing methods sang **deployment considerations**.

---

# 23. Kết luận

Data Cleaning trong Time-Series Data gồm ba vấn đề lớn:

$$
\boxed{
Missing\ Data
+
Outlier
+
Noise
}
$$

Mỗi vấn đề yêu cầu một chiến lược khác nhau:

```text
Missing
   → Imputation

Outlier
   → Detection + Validation + Handling

Noise
   → Denoising + Signal Preservation
```

Các phương pháp đơn giản có ưu thế về:

$$
Low\ Cost + Easy\ Deployment
$$

trong khi các phương pháp model-based có khả năng khai thác:

$$
Temporal\ Dependency + Complex\ Patterns
$$

Nhưng complexity cao không đồng nghĩa với performance tốt hơn trong mọi trường hợp.

Một Data Cleaning pipeline tốt phải cân bằng:

$$
\boxed{
Data\ Quality
+
Temporal\ Integrity
+
Information\ Preservation
+
AI\ Performance
+
Computational\ Efficiency
}
$$

Do đó, bài học quan trọng nhất từ phần Data Cleaning của survey là:

> **Không lựa chọn preprocessing method chỉ vì nó mạnh hơn. Hãy lựa chọn method dựa trên bản chất của dữ liệu, temporal structure, downstream task và computational constraints của hệ thống.**
