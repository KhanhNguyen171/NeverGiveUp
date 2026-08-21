# 04. Decomposition

## 1. Khái niệm Decomposition

**Time-series decomposition** là quá trình phân tách một chuỗi thời gian thành các thành phần có ý nghĩa thống kê khác nhau, thường gồm:

* **Trend ($T_t$):** xu hướng dài hạn của chuỗi.
* **Seasonality ($S_t$):** biến động lặp lại theo chu kỳ.
* **Residual/Irregular ($R_t$):** phần biến động còn lại không được giải thích bởi trend và seasonality.

Một mô hình decomposition cơ bản có thể biểu diễn dưới dạng **additive**:

$$X_t=T_t+S_t+R_t$$

hoặc **multiplicative**:

$$X_t=T_t\times S_t\times R_t$$

Trong đó việc lựa chọn additive hay multiplicative phụ thuộc vào quan hệ giữa biên độ seasonal và mức độ của chuỗi.

Decomposition không đơn thuần là một phép biến đổi nhằm chuẩn hóa dữ liệu. Mục tiêu chính là **làm rõ cấu trúc của chuỗi thời gian**, từ đó hỗ trợ lựa chọn phương pháp preprocessing, feature engineering và mô hình dự báo phù hợp.

---

## 2. Vai trò của Decomposition trong Data Transformation

Trong pipeline của nghiên cứu, decomposition được đặt sau các bước **scaling/normalization**, **transformation** và **stationarity analysis**.

```text
Raw Time Series
      │
      ▼
Data Cleaning
      │
      ▼
Scaling / Normalization
      │
      ▼
Transformation
      │
      ▼
Stationarity Analysis
      │
      ▼
Decomposition
      │
      ├── Trend
      ├── Seasonality
      └── Residual
      │
      ▼
Feature Engineering
      │
      ▼
Feature Selection
```

Mối quan hệ giữa các bước là tuần tự nhưng không hoàn toàn độc lập.

* **Data Cleaning** loại bỏ hoặc xử lý missing data, outlier và noise trước khi ước lượng cấu trúc của chuỗi.
* **Transformation** có thể làm thay đổi scale hoặc variance của dữ liệu trước decomposition.
* **Stationarity analysis** xác định trend hoặc seasonal structure có tồn tại và có cần loại bỏ hay không.
* **Decomposition** sau đó tách các thành phần để phục vụ phân tích và feature engineering.
* Các thành phần được tạo ra có thể trở thành **features** ở Chương 5 hoặc được sử dụng để lựa chọn đặc trưng ở Chương 6.

Do đó, decomposition đóng vai trò **cầu nối giữa Data Transformation và Feature Engineering**.

---

## 3. Additive và Multiplicative Decomposition

### 3.1. Additive decomposition

Additive decomposition giả định rằng ảnh hưởng của seasonal component có biên độ tương đối ổn định theo thời gian:

$$X_t=T_t+S_t+R_t$$

Trong đó:

$$T_t=\text{Trend component}$$

$$S_t=\text{Seasonal component}$$

$$R_t=\text{Residual component}$$

Mô hình này phù hợp khi độ lớn của seasonal fluctuation không phụ thuộc đáng kể vào level của chuỗi.

Ví dụ, nếu một chuỗi dao động khoảng $\pm 10$ đơn vị quanh trend trong toàn bộ khoảng thời gian, additive decomposition là lựa chọn hợp lý.

---

### 3.2. Multiplicative decomposition

Multiplicative decomposition biểu diễn chuỗi dưới dạng:

$$X_t=T_t\times S_t\times R_t$$

Mô hình này phù hợp khi biên độ seasonal variation tăng hoặc giảm theo level của chuỗi.

Ví dụ, nếu khi giá trị trung bình của chuỗi tăng thì biên độ dao động seasonal cũng tăng, quan hệ multiplicative có thể phù hợp hơn additive.

Multiplicative decomposition thường yêu cầu dữ liệu có giá trị dương.

---

### 3.3. Log transformation và mối quan hệ với decomposition

Multiplicative decomposition có thể được chuyển thành dạng additive bằng logarithm:

$$X_t=T_tS_tR_t$$

$$\log X_t=\log T_t+\log S_t+\log R_t$$

Điều này tạo mối liên hệ trực tiếp với **02_transformation.md**: logarithmic transformation không chỉ có thể được sử dụng để ổn định variance mà còn giúp biểu diễn một cấu trúc multiplicative dưới dạng additive.

Tuy nhiên, log transformation chỉ phù hợp khi miền giá trị của dữ liệu cho phép áp dụng phép logarithm.

---

## 4. Các thành phần của Decomposition

### 4.1. Trend

Trend biểu diễn chuyển động dài hạn của chuỗi:

$$X_t=T_t+S_t+R_t$$

Trong đó $T_t$ mô tả phần biến động có tính hệ thống trong thời gian dài.

Trend có thể được ước lượng bằng:

* moving average;
* regression;
* smoothing;
* decomposition algorithms.

Trend information có thể được sử dụng để:

* phát hiện non-stationarity;
* tạo trend features;
* phân tích sự thay đổi dài hạn;
* hỗ trợ forecasting.

Nếu trend được loại bỏ, chuỗi detrended có thể được biểu diễn:

$$X_t-T_t=S_t+R_t$$

Điều này liên kết trực tiếp với **03_stationarity.md**, trong đó detrending được xem là một phương pháp xử lý non-stationarity.

---

### 4.2. Seasonality

Seasonality là các biến động lặp lại theo một chu kỳ xác định.

Với seasonal period $s$:

$$S_t=S_{t-s}$$

Ví dụ:

* dữ liệu theo giờ có thể có chu kỳ ngày;
* dữ liệu theo ngày có thể có chu kỳ tuần;
* dữ liệu theo tháng có thể có chu kỳ năm.

Seasonal component có thể cung cấp thông tin quan trọng cho feature engineering. Thay vì loại bỏ seasonality, nghiên cứu có thể biểu diễn nó thành các đặc trưng như:

$$hour_sin=\sin\left(\frac{2\pi h}{24}\right)$$

$$hour_cos=\cos\left(\frac{2\pi h}{24}\right)$$

Cách biểu diễn này sẽ được trình bày chi tiết trong **05_feature_engineering/01_temporal_features.md**.

---

### 4.3. Residual

Residual là phần biến động còn lại sau khi loại bỏ trend và seasonality:

$$R_t=X_t-T_t-S_t$$

đối với additive decomposition.

Residual không nhất thiết là pure noise. Nó có thể chứa:

* random noise;
* outlier chưa được xử lý;
* temporal dependency;
* information chưa được mô hình hóa.

Do đó, residual cần được kiểm tra thay vì mặc định loại bỏ.

Một residual tốt cho decomposition thường không còn cấu trúc temporal rõ ràng. Nếu residual vẫn có autocorrelation mạnh, decomposition chưa giải thích đầy đủ dynamics của chuỗi.

---

## 5. Các phương pháp Decomposition

### 5.1. Moving Average Decomposition

Moving average có thể được sử dụng để ước lượng trend bằng cách làm trơn chuỗi.

Với cửa sổ $m$:

$$\hat{T}*t=\frac{1}{m}\sum*{i=-k}^{k}X_{t+i}$$

với $m=2k+1$.

Sau khi ước lượng trend, seasonal và residual có thể được xác định dựa trên phần còn lại.

Ưu điểm:

* đơn giản;
* dễ diễn giải;
* chi phí tính toán thấp.

Hạn chế:

* nhạy với lựa chọn window;
* xử lý boundary không thuận lợi;
* khó mô hình hóa seasonal pattern phức tạp.

---

### 5.2. Classical Decomposition

Classical decomposition thực hiện việc ước lượng trend, seasonal component và residual theo một cấu trúc xác định.

Đối với additive model:

$$R_t=X_t-\hat{T}_t-\hat{S}_t$$

Đối với multiplicative model:

$$R_t=\frac{X_t}{\hat{T}_t\hat{S}_t}$$

Phương pháp này dễ hiểu và phù hợp để phân tích cơ bản, nhưng khả năng xử lý trend thay đổi hoặc seasonality phức tạp còn hạn chế.

---

### 5.3. STL Decomposition

**STL (Seasonal-Trend decomposition using LOESS)** sử dụng local regression để ước lượng trend và seasonal components.

Một dạng biểu diễn khái quát:

$$X_t=T_t+S_t+R_t$$

STL có khả năng xử lý:

* trend thay đổi theo thời gian;
* seasonal pattern tương đối phức tạp;
* outlier thông qua robust fitting.

So với classical decomposition, STL linh hoạt hơn khi cấu trúc của chuỗi không hoàn toàn ổn định.

Tuy nhiên, STL yêu cầu xác định seasonal period và các tham số smoothing phù hợp. Việc lựa chọn sai seasonal period có thể dẫn đến decomposition không phản ánh đúng cấu trúc thực tế.

---

## 6. Decomposition và Noise Reduction

Decomposition có mối quan hệ trực tiếp với **03_noise_reduction.md** trong Chương 3.

Một cách tiếp cận phổ biến là xem residual như thành phần chứa phần lớn biến động ngẫu nhiên:

$$X_t=T_t+S_t+R_t$$

Nếu mục tiêu là phân tích trend hoặc seasonality, có thể sử dụng:

$$X_t^{smooth}=\hat{T}_t+\hat{S}_t$$

thay vì toàn bộ chuỗi $X_t$.

Tuy nhiên, trong bài toán dự báo, **không nên mặc định loại bỏ residual**. Residual có thể chứa thông tin dự báo quan trọng. Việc loại bỏ nó chỉ hợp lý khi đã xác định rằng residual chủ yếu là noise và không đóng góp đáng kể vào nhiệm vụ downstream.

Điều này thể hiện nguyên tắc chung của preprocessing:

> **Giảm noise không đồng nghĩa với loại bỏ mọi biến động không đều.**

---

## 7. Decomposition trong Feature Engineering

Decomposition có thể tạo ra các đặc trưng mới:

| Component | Có thể sử dụng làm feature          |
| --------- | ----------------------------------- |
| Trend     | Trend value, trend slope            |
| Seasonal  | Seasonal amplitude, seasonal index  |
| Residual  | Residual value, residual statistics |
| Cycle     | Periodic representation             |

Ví dụ, trend slope có thể được ước lượng:

$$s_t=\frac{T_t-T_{t-k}}{k}$$

Trong khi residual rolling statistics có thể được sử dụng để mô tả mức độ biến động:

$$\sigma_t^{(w)}=\sqrt{\frac{1}{w-1}\sum_{i=0}^{w-1}(R_{t-i}-\bar{R}_t)^2}$$

Các đặc trưng này sẽ được xem xét trong **Chương 5 — Feature Engineering**, đặc biệt trong các nhóm temporal, rolling và feature representation.

---

## 8. Decomposition và Data Leakage

Trong forecasting, decomposition phải tuân thủ nguyên tắc **temporal ordering**.

Không được sử dụng thông tin của tương lai để tạo decomposition cho một thời điểm trong quá khứ.

Ví dụ, nếu training data kết thúc tại $t$, việc ước lượng feature tại $t$ không được sử dụng:

$$X_{t+1},X_{t+2},\ldots$$

để tính trend hoặc seasonal component của $X_t$.

Đặc biệt, các phương pháp smoothing hoặc decomposition sử dụng thông tin ở cả hai phía của thời điểm $t$ có thể vô tình đưa future information vào training features.

Vì vậy, trong pipeline forecasting:

```text
Chronological Split
        │
        ├── Train
        ├── Validation
        └── Test
             │
             ▼
   Fit transformation/decomposition
   using allowed historical data
             │
             ▼
       Generate features
             │
             ▼
        Model Training
```

Quy tắc này liên kết trực tiếp với nguyên tắc **train-only fitting** đã được đặt ra trong các bước transformation trước đó.

---

## 9. Lựa chọn phương pháp Decomposition

Không có một phương pháp decomposition tối ưu cho mọi dataset.

Việc lựa chọn nên dựa trên:

1. **Seasonal period:** chu kỳ của dữ liệu có được xác định rõ hay không.
2. **Trend behavior:** trend ổn định hay thay đổi theo thời gian.
3. **Variance:** biên độ seasonal có phụ thuộc vào level hay không.
4. **Noise level:** residual có chứa nhiều biến động ngẫu nhiên hay không.
5. **Forecasting objective:** decomposition dùng để phân tích hay trực tiếp tạo features.
6. **Risk of leakage:** phương pháp có sử dụng future observations hay không.
7. **Computational cost:** phù hợp với kích thước và yêu cầu xử lý dữ liệu.

Có thể khái quát:

```text
Time Series
    │
    ├── Stable variance + stable seasonal amplitude
    │        └── Additive decomposition
    │
    ├── Seasonal amplitude ∝ level
    │        └── Multiplicative / Log-additive
    │
    ├── Changing trend / complex seasonality
    │        └── STL
    │
    └── No meaningful seasonal structure
             └── Trend / residual analysis
```

---

## 10. Kết nối với các chương tiếp theo

Decomposition hoàn thiện nhóm **Data Transformation** bằng cách chuyển từ việc thay đổi biểu diễn dữ liệu sang việc **phân tích cấu trúc bên trong của chuỗi thời gian**.

Mối liên kết của Chương 4 được xác định như sau:

```text
01 Scaling & Normalization
          │
          ▼
02 Transformation
          │
          ▼
03 Stationarity
          │
          ▼
04 Decomposition
          │
          ├── Trend
          ├── Seasonality
          └── Residual
          │
          ▼
05 Feature Engineering
          │
          ▼
06 Feature Selection
```

Trong đó:

* **Scaling/Normalization** đưa các biến về phạm vi hoặc phân phối phù hợp.
* **Transformation** thay đổi dạng biểu diễn nhằm xử lý skewness hoặc variance.
* **Stationarity** đánh giá và xử lý sự thay đổi của các đặc tính thống kê theo thời gian.
* **Decomposition** tách các cấu trúc trend, seasonal và residual.
* **Feature Engineering** chuyển các cấu trúc đã xác định thành các đặc trưng có thể sử dụng cho mô hình.
* **Feature Selection** tiếp tục đánh giá và loại bỏ các đặc trưng dư thừa hoặc không hữu ích.

Do đó, decomposition không phải bước kết thúc của preprocessing mà là **điểm chuyển tiếp từ Data Transformation sang Feature Engineering**.

## 11. Nguyên tắc tổng quát

Decomposition trong nghiên cứu được áp dụng theo các nguyên tắc:

* Không decomposition chỉ vì dữ liệu là time series.
* Xác định seasonal period trước khi áp dụng phương pháp seasonal decomposition.
* Lựa chọn additive hoặc multiplicative dựa trên cấu trúc variance và seasonal amplitude.
* Không loại bỏ residual nếu chưa chứng minh residual chủ yếu là noise.
* Kiểm soát temporal leakage khi ước lượng trend và seasonal components.
* Nếu decomposition tạo ra features, quá trình tạo feature phải tuân thủ cùng nguyên tắc temporal split và train-only fitting.
* Đánh giá decomposition dựa trên khả năng giải thích cấu trúc dữ liệu và giá trị đối với downstream task, không chỉ dựa trên mức độ làm mượt chuỗi.

Như vậy, **decomposition là bước phân tích cấu trúc của dữ liệu sau transformation và stationarity analysis, đồng thời cung cấp cơ sở trực tiếp cho việc xây dựng temporal, trend, seasonal và residual features ở Chương 5.**
