# 02. Outlier Detection

## 1. Tổng quan

Trong Time-Series Data, **outlier** là những quan sát có giá trị bất thường so với hành vi thông thường của chuỗi. Outlier có thể xuất hiện do lỗi cảm biến, lỗi truyền dữ liệu, lỗi hệ thống thu thập hoặc cũng có thể đại diện cho một sự kiện thực sự xảy ra trong hệ thống.

Survey xem **outlier detection** là một thành phần của data preprocessing nhằm cải thiện chất lượng dữ liệu trước khi đưa vào các thuật toán AI. Tác giả cũng nhấn mạnh rằng preprocessing không chỉ giới hạn ở data cleaning mà là một quá trình rộng hơn nhằm biến dữ liệu thô thành dữ liệu đầu vào có chất lượng.

Một điểm rất quan trọng:

> Không phải mọi outlier đều là lỗi dữ liệu.

Survey phân loại anomaly theo ngữ cảnh thành **global**, **local**, **contextual/conditional** và **collective**. Với time series, hai loại sau đặc biệt quan trọng: một điểm chỉ bất thường khi xét thời gian, vị trí hoặc một nhóm điểm liên tiếp.

Ví dụ:

```text
Temperature:

25  25.2  25.4  25.3  40  25.5  25.4
                    ↑
                 outlier?
```

Giá trị `40` có thể là:

* lỗi sensor;
* lỗi truyền dữ liệu;
* hoặc một sự kiện thực tế.

Do đó, **outlier detection** và **outlier removal** là hai vấn đề khác nhau.

---

# 2. Outlier trong Time Series

Với time series:

$$
X={x_1,x_2,\ldots,x_T}
$$

một observation (x_t) được xem là bất thường nếu nó khác đáng kể so với hành vi kỳ vọng của chuỗi.

Có thể biểu diễn:

$$
x_t = s_t + \epsilon_t
$$

trong đó:

* $s_t$: tín hiệu hoặc hành vi bình thường;
* $\epsilon_t$: nhiễu hoặc sai lệch.

Một outlier xảy ra khi:

$$
|x_t-s_t|\gg |\epsilon_t|
$$

Nói cách khác, outlier là một observation có deviation lớn so với mô hình hoặc phân phối kỳ vọng.

---

# 3. Vì sao Outlier là vấn đề đối với Time Series?

Outlier có thể ảnh hưởng trực tiếp đến:

* Mean;
* Variance;
* Covariance;
* Correlation;
* Scaling;
* Regression;
* Model training;
* Forecasting accuracy.

Ví dụ:

```text
Normal:

10  11  12  13  14

Có outlier:

10  11  12  100  14
```

Mean của chuỗi bị kéo mạnh về phía giá trị `100`.

Điều này đặc biệt nguy hiểm khi preprocessing tiếp theo sử dụng mean và standard deviation.

Ví dụ Standardization:

$$
z_i=\frac{x_i-\mu}{\sigma}
$$

Nếu (\mu) và (\sigma) bị outlier làm thay đổi, toàn bộ dữ liệu sau scaling cũng bị ảnh hưởng.

Vì vậy:

```text
Outlier
   ↓
Statistics bị thay đổi
   ↓
Preprocessing bị thay đổi
   ↓
Model Input bị thay đổi
   ↓
Model Performance bị ảnh hưởng
```

---

# 4. Global Outlier và Local Outlier

Trong Time Series cần phân biệt hai trường hợp.

## 4.1. Global Outlier

Một observation bất thường so với toàn bộ dataset.

Ví dụ:

```text
10  11  12  13  100  14  15
             ↑
       Global outlier
```

Nếu phần lớn dữ liệu nằm quanh:

$$
10-20
$$

thì `100` rõ ràng bất thường.

---

## 4.2. Local Outlier

Một observation có thể không bất thường đối với toàn bộ dataset nhưng bất thường trong **context thời gian hiện tại**.

Ví dụ:

```text
Buổi sáng:

20  21  22  23  50  24
            ↑
       Local outlier
```

Nhưng nếu toàn bộ dataset cũng có những thời điểm:

```text
20
50
80
100
```

thì `50` có thể không phải global outlier.

Đây là lý do outlier detection cho Time Series phức tạp hơn dữ liệu tabular thông thường.

> Một observation phải được đánh giá trong **temporal context**, không chỉ dựa trên global distribution.

### Contextual và Collective Outlier

* **Contextual (conditional) outlier**: giá trị chỉ bất thường trong một bối cảnh cụ thể, chẳng hạn `40°C` bất thường vào ban đêm nhưng có thể hợp lệ vào ban ngày.
* **Collective outlier**: một nhóm observation cùng tạo thành hành vi bất thường, dù từng điểm riêng lẻ chưa chắc vượt ngưỡng.

Vì vậy, IQR hoặc Z-score chỉ là bước phát hiện ban đầu; cần kiểm tra nguyên nhân và quy tắc nghiệp vụ trước khi sửa hoặc xóa.

---

# 5. Các nhóm phương pháp Outlier Detection

Survey trình bày các hướng tiếp cận khác nhau để phát hiện outlier. Một trong những nhóm cơ bản được đề cập là các phương pháp thống kê dựa trên **Interquartile Range (IQR)**; tác giả cũng thảo luận các **robust estimators** và khả năng triển khai một số phương pháp theo cửa sổ tại Edge.

Trong empirical analysis, các kỹ thuật outlier được kiểm thử gồm MAD, Grubbs, GESD, IQR, DBSCAN và Isolation Forest. Grubbs/GESD dựa trên giả định phân phối Gaussian; IQR phù hợp hơn khi không muốn dựa vào giả định Gaussian. Moving-window và deep-learning trong tài liệu này là phần mở rộng lý thuyết, không nên gán là kết quả thực nghiệm của paper.

Có thể tổ chức các phương pháp thành:

```text
Outlier Detection
│
├── Statistical Methods
│   ├── IQR
│   ├── Robust Estimators
│   └── Distribution-based Methods
│
├── Window-based Methods
│
├── Model-based Methods
│
└── Learning-based Methods
```

Trong đó, lựa chọn phương pháp phụ thuộc vào:

* distribution;
* temporal dependency;
* mức độ nhiễu;
* kích thước dữ liệu;
* computational resources;
* yêu cầu real-time/edge processing.

---

# 6. IQR Method

## 6.1. Ý tưởng

**Interquartile Range — IQR** dựa trên phân vị của dữ liệu.

Xác định:

$$
IQR=Q_3-Q_1
$$

trong đó:

* $Q_1$: 25th percentile;
* $Q_3$: 75th percentile.

Sau đó xác định hai ngưỡng:

$$
Lower=Q_1-kIQR
$$

$$
Upper=Q_3+kIQR
$$

với giá trị thường được sử dụng:

$$
k=1.5
$$

Một observation được xem là outlier nếu:

$$
x_t \lt Lower
$$

hoặc:

$$
x_t \gt Upper
$$

---

## 6.2. Ví dụ

Giả sử:

$$
Q_1=10
$$

và:

$$
Q_3=20
$$

thì:

$$
IQR=20-10=10
$$

Với:

$$
k=1.5
$$

ta có:

$$
Lower=10-1.5(10)=-5
$$

$$
Upper=20+1.5(10)=35
$$

Do đó:

```text
10   12   15   20   25   30   50
                           ↑
                        Outlier
```

vì:

$$
50 \gt 35
$$

---

# 7. IQR cho Time Series

IQR có thể được áp dụng trên toàn bộ series hoặc trên **sliding window**.

Global:

```text
Entire Time Series
        ↓
Calculate Q1, Q3
        ↓
Calculate IQR
        ↓
Define Bounds
        ↓
Detect Outliers
```

Window-based:

```text
Time Series
     ↓
┌──────────┐
│ Window 1 │
└──────────┘
     ↓
IQR

      ┌──────────┐
      │ Window 2 │
      └──────────┘
           ↓
          IQR
```

Window-based IQR cho phép threshold thay đổi theo temporal context.

Điều này đặc biệt hữu ích khi time series có:

* trend;
* seasonality;
* changing variance.

Survey chỉ ra rằng IQR có hiệu quả thực thi tốt và có thể triển khai tại Edge trong việc phát hiện outlier theo cửa sổ, nhưng phương pháp này **không nhất thiết phát hiện được mọi outlier**.

---

# 8. Robust Estimators

Một vấn đề của các phương pháp thống kê thông thường là chính outlier có thể làm thay đổi các statistics được sử dụng để phát hiện nó.

Ví dụ mean và standard deviation:

$$
\mu=\frac{1}{N}\sum_{i=1}^{N}x_i
$$

$$
\sigma=
\sqrt{
\frac{1}{N}
\sum_{i=1}^{N}(x_i-\mu)^2
}
$$

Nếu xuất hiện một giá trị cực lớn:

```text
10  11  12  13  14  1000
```

thì $\mu$ và $\sigma$ đều bị ảnh hưởng.

Robust estimators cố gắng giảm ảnh hưởng của extreme observations bằng cách sử dụng các thống kê ít nhạy với outlier hơn.

Các đại lượng quan trọng gồm:

```text
Median
IQR
MAD
Robust Scale Estimators
```

Trong đó **Median Absolute Deviation — MAD** được định nghĩa:

$$
MAD=
\operatorname{median}
\left(
|x_i-\operatorname{median}(X)|
\right)
$$

MAD thường robust hơn standard deviation khi dữ liệu chứa extreme values.

---

# 9. Z-Score

Một phương pháp thống kê cơ bản khác là Z-score.

$$
z_t=
\frac{x_t-\mu}{\sigma}
$$

Nếu:

$$
|z_t| \gt \tau
$$

thì observation có thể được đánh dấu là outlier.

Ví dụ với:

$$
\tau=3
$$

ta có:

```text
|z| <= 3
    ↓
Normal

|z| > 3
    ↓
Potential Outlier
```

Tuy nhiên Z-score phụ thuộc vào mean và standard deviation.

Nếu dataset chứa nhiều outlier, chính $\mu$ và $\sigma$ đã bị distortion.

Do đó Z-score phù hợp hơn khi distribution tương đối ổn định và outlier rate không quá lớn.

---

# 10. Moving Window Outlier Detection

Đối với Time Series, một cách tiếp cận tự nhiên hơn là xem xét **local statistics**.

Cho window:

$$
W_t=
{x_{t-w+1},...,x_t}
$$

tính:

$$
\mu_t=
\frac{1}{w}
\sum_{i=t-w+1}^{t}x_i
$$

và:

$$
\sigma_t=
\sqrt{
\frac{1}{w}
\sum_{i=t-w+1}^{t}
(x_i-\mu_t)^2
}
$$

Sau đó đánh giá:

$$
|x_t-\mu_t| \gt k\sigma_t
$$

Nếu điều kiện đúng:

$$
x_t
$$

được đánh dấu là potential outlier.

---

# 11. Vì sao Sliding Window quan trọng?

Giả sử time series có trend:

```text
10
20
30
40
50
60
70
```

Một global threshold có thể xem `70` là bất thường.

Nhưng xét local context:

```text
50
60
70
```

thì `70` hoàn toàn bình thường.

Do đó:

```text
Global Detection
       ↓
Toàn bộ dataset
       ↓
Một threshold
```

khác với:

```text
Local Detection
       ↓
Sliding Window
       ↓
Threshold thay đổi theo thời gian
```

Đối với Time Series, local context thường có ý nghĩa quan trọng hơn global distribution.

---

# 12. Model-based Outlier Detection

Thay vì xác định outlier trực tiếp từ distribution, ta có thể xây dựng model mô tả hành vi bình thường.

Giả sử:

$$
x_t=f(x_{t-1},x_{t-2},...,x_{t-p})+\epsilon_t
$$

Model dự đoán:

$$
\hat{x}_t=f(x_{t-1},...,x_{t-p})
$$

Residual:

$$
e_t=x_t-\hat{x}_t
$$

Nếu:

$$
|e_t|>\tau
$$

thì observation có thể được xem là outlier.

Pipeline:

```text
Historical Values
        ↓
Time-Series Model
        ↓
Prediction x̂t
        ↓
Residual
        ↓
|xt - x̂t|
        ↓
Threshold
        ↓
Outlier / Normal
```

Ưu điểm là model có thể học:

* trend;
* seasonality;
* autocorrelation;
* temporal dependency.

---

# 13. Learning-based Detection

Với dữ liệu phức tạp, có thể sử dụng Machine Learning hoặc Deep Learning.

Ví dụ:

```text
Isolation Forest
One-Class SVM
Autoencoder
LSTM Autoencoder
Transformer-based Models
```

Ý tưởng chung:

$$
x_t
\rightarrow
Model
\rightarrow
Anomaly\ Score
$$

Nếu anomaly score vượt threshold:

$$
A(x_t) \gt \tau
$$

thì:

$$
x_t=\text{Outlier}
$$

Deep Learning đặc biệt hữu ích khi temporal patterns phức tạp, nhưng chi phí tính toán và yêu cầu dữ liệu lớn hơn đáng kể.

---

# 14. Detect ≠ Remove

Một trong những nguyên tắc quan trọng nhất khi xử lý outlier là:

> **Phát hiện outlier không đồng nghĩa với việc phải xóa outlier.**

Ví dụ:

```text
Temperature:

25
26
25
27
80
26
25
```

Giá trị `80` có thể là:

### Trường hợp 1 — Sensor Error

```text
80 = lỗi sensor
```

→ có thể cần correction/imputation.

### Trường hợp 2 — Real Event

```text
80 = sự kiện thực tế
```

→ xóa nó sẽ làm mất information.

Do đó quy trình đúng là:

```text
Detect
   ↓
Validate
   ↓
Determine Cause
   ↓
Remove / Correct / Keep
```

---

# 15. Outlier Correction

Nếu xác định outlier là lỗi, có thể:

### Remove

$$
x_t\rightarrow NaN
$$

sau đó áp dụng Missing Data Imputation.

### Replace

$$
x_t\rightarrow\hat{x}_t
$$

### Winsorization

Giới hạn extreme values:

$$
x_t'=
\begin{cases}
L & x_t \lt L\
x_t & L\le x_t\le U\
U & x_t \gt U
\end{cases}
$$

### Smoothing

Sử dụng local estimate để thay thế observation bất thường.

---

# 16. Outlier Detection và Edge Computing

Một điểm đáng chú ý của survey là preprocessing không nhất thiết phải được thực hiện hoàn toàn ở central server.

Một số kỹ thuật có thể được đưa xuống **Edge**:

```text
Sensor
  ↓
Edge Device
  ↓
Outlier Detection
  ↓
Clean Data
  ↓
Network
  ↓
Central System
```

Lợi ích:

* giảm lượng dữ liệu truyền;
* giảm network traffic;
* giảm workload của central system;
* giảm resource consumption;
* hỗ trợ EdgeAI.

Survey đặc biệt đề cập khả năng triển khai preprocessing tại Edge như một hướng giúp giảm tải hệ thống trung tâm và làm dữ liệu dễ quản lý hơn.

Đối với outlier detection, các phương pháp có computational cost thấp như IQR theo window có lợi thế trong môi trường hạn chế tài nguyên.

---

# 17. So sánh các nhóm phương pháp

| Method                 | Temporal Context |  Robust với Outlier |     Complexity | Phù hợp Edge |
| ---------------------- | ---------------: | ------------------: | -------------: | -----------: |
| Z-Score                |             Thấp |                Thấp |           Thấp |          Cao |
| IQR                    |     Thấp / Local |                 Cao |           Thấp |          Cao |
| MAD / Robust Estimator |     Thấp / Local |             Rất cao |           Thấp |          Cao |
| Moving Window          |              Cao | Phụ thuộc statistic |     Trung bình |          Cao |
| Model-based            |              Cao |                 Cao | Trung bình–Cao |    Tùy model |
| ML-based               |              Cao |                 Cao |            Cao |      Hạn chế |
| Deep Learning          |          Rất cao |                 Cao |        Rất cao |          Khó |

Không tồn tại một phương pháp tốt nhất cho mọi Time Series.

---

# 18. Quy trình Outlier Detection

Một pipeline tổng quát:

```text
Raw Time Series
       │
       ▼
Data Validation
       │
       ▼
Check Temporal Structure
       │
       ▼
Identify Outlier Pattern
       │
       ├── Global
       ├── Local
       └── Temporal / Contextual
       │
       ▼
Select Detection Method
       │
       ├── Statistical
       ├── Window-based
       ├── Robust
       └── Model-based
       │
       ▼
Detect Potential Outliers
       │
       ▼
Validate Anomalies
       │
       ├── Real Event
       │
       └── Data Error
       │
       ▼
Keep / Correct / Remove
       │
       ▼
Clean Time Series
```

---

# 19. Những điểm cần ghi nhớ từ Survey

### 19.1. Outlier là một vấn đề của Data Quality

Outlier detection là một phần của preprocessing nhằm tạo ra dữ liệu đầu vào có chất lượng cho AI.

### 19.2. Không phải outlier nào cũng là lỗi

Một anomaly có thể chứa thông tin quan trọng về một event thực tế.

### 19.3. Time Series cần xét temporal context

Một điểm bình thường xét trên toàn dataset vẫn có thể bất thường trong một khoảng thời gian cụ thể.

### 19.4. Robust statistics rất quan trọng

IQR và các robust estimators giảm ảnh hưởng của extreme observations; survey cũng nhấn mạnh nhóm robust estimators như một hướng tiếp cận cho outlier detection.

### 19.5. Window-based detection phù hợp với dữ liệu streaming

Sliding-window methods cho phép phát hiện outlier theo local context và có khả năng triển khai gần nguồn dữ liệu.

### 19.6. Detection và correction là hai bước khác nhau

```text
Detection ≠ Removal
```

Phải xác định nguyên nhân của anomaly trước khi quyết định xử lý.

---

# 20. Liên hệ với Forecasting

Trong Time-Series Forecasting, xử lý outlier cần đặc biệt cẩn thận.

Không nên thực hiện:

```text
Full Dataset
     ↓
Detect Outlier
     ↓
Use Future Information
     ↓
Train Model
```

nếu detection process sử dụng thông tin từ Validation/Test để quyết định cách xử lý Training data.

Nguyên tắc cần giữ:

$$
\boxed{
Train\ Information
\rightarrow
Train\ Preprocessing
}
$$

và:

$$
\boxed{
Validation/Test
\rightarrow
Evaluation
}
$$

Đặc biệt với rolling statistics, threshold estimation và model-based detection, cần kiểm soát temporal boundary để tránh future information leakage.

---

# 21. Kết luận

Outlier Detection trong Time-Series Data không đơn giản là tìm những giá trị lớn hoặc nhỏ bất thường.

Bài toán thực sự là:

$$
\boxed{
\text{Identify}
\rightarrow
\text{Contextualize}
\rightarrow
\text{Validate}
\rightarrow
\text{Decide}
}
$$

Các phương pháp đơn giản như **Z-score và IQR** cung cấp cách phát hiện dựa trên statistical distribution. **Robust estimators** giúp giảm ảnh hưởng của extreme values, trong khi **moving-window methods** đưa temporal context vào quá trình detection. Với những time series có dynamics phức tạp hơn, có thể sử dụng model-based hoặc learning-based methods.

Điểm quan trọng nhất cần ghi nhớ là:

> **Outlier Detection phải bảo vệ cả Data Quality và Information Integrity.**

Một preprocessing pipeline tốt không phải là pipeline loại bỏ càng nhiều outlier càng tốt, mà là pipeline có khả năng phân biệt giữa **data error** và **real-world event**, đồng thời không phá hủy cấu trúc temporal của dữ liệu.
