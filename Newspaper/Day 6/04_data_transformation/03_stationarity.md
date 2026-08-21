# 03. Stationarity

## 1. Khái niệm Stationarity

Trong dữ liệu chuỗi thời gian, **stationarity (tính dừng)** mô tả trạng thái mà các đặc tính thống kê của chuỗi không thay đổi theo thời gian. Một chuỗi dừng yếu (weakly stationary) thường được đặc trưng bởi:

$$E[X_t]=\mu$$

$$Var(X_t)=\sigma^2$$

$$Cov(X_t,X_{t-k})=\gamma_k$$

Trong đó $\mu$ và $\sigma^2$ không phụ thuộc vào thời điểm $t$, còn hiệp phương sai chỉ phụ thuộc vào độ trễ $k$, không phụ thuộc vào vị trí tuyệt đối trên trục thời gian.

Ngược lại, chuỗi có **trend**, **seasonality** hoặc phương sai thay đổi theo thời gian thường được xem là non-stationary. Đây là đặc điểm phổ biến trong dữ liệu thực tế như năng lượng, tài chính, cảm biến và nhu cầu tiêu thụ theo thời gian.

Stationarity không phải là yêu cầu bắt buộc đối với mọi mô hình học máy. Tuy nhiên, nó có ý nghĩa quan trọng trong phân tích chuỗi thời gian vì nhiều phương pháp thống kê và mô hình dự báo giả định rằng quan hệ thống kê của dữ liệu tương đối ổn định theo thời gian.

---

## 2. Non-stationarity trong dữ liệu chuỗi thời gian

Một chuỗi có thể trở nên non-stationary do nhiều nguyên nhân:

* **Trend:** mức trung bình thay đổi theo thời gian.
* **Seasonality:** xuất hiện các biến động có chu kỳ xác định.
* **Changing variance:** độ phân tán của dữ liệu thay đổi theo thời gian.
* **Structural change:** cơ chế sinh dữ liệu thay đổi giữa các giai đoạn.

Ví dụ, với một chuỗi có xu hướng tăng:

$$X_t=\beta_0+\beta_1t+\epsilon_t$$

nếu $\beta_1\neq0$, giá trị kỳ vọng của chuỗi phụ thuộc vào $t$:

$$E[X_t]=\beta_0+\beta_1t$$

Do đó chuỗi không thỏa mãn điều kiện trung bình không đổi và được xem là non-stationary.

Trong thực tế, việc xác định non-stationarity không nên dựa trên một tiêu chí duy nhất. Có thể kết hợp **time-series plot**, **rolling statistics**, **ACF** và các kiểm định thống kê như **Augmented Dickey-Fuller (ADF)** và **KPSS**. ACF của chuỗi non-stationary thường suy giảm chậm theo lag, trong khi chuỗi stationary thường có ACF suy giảm nhanh hơn.

---

## 3. Phát hiện tính không dừng

### 3.1. Phân tích trực quan

Biểu đồ chuỗi theo thời gian là bước kiểm tra ban đầu để phát hiện:

* xu hướng dài hạn;
* biến động theo mùa;
* thay đổi mức độ phân tán;
* thay đổi cấu trúc của chuỗi.

Nếu chuỗi dao động quanh một mức trung bình tương đối ổn định và phương sai không thay đổi đáng kể, dữ liệu có dấu hiệu stationary. Ngược lại, trend hoặc seasonal pattern rõ ràng là dấu hiệu của non-stationarity.

### 3.2. Rolling statistics

Có thể sử dụng trung bình và phương sai trên cửa sổ trượt để kiểm tra sự ổn định theo thời gian:

$$\mu_t^{(w)}=\frac{1}{w}\sum_{i=0}^{w-1}X_{t-i}$$

$$\sigma_t^{2(w)}=\frac{1}{w-1}\sum_{i=0}^{w-1}(X_{t-i}-\mu_t^{(w)})^2$$

Nếu $\mu_t^{(w)}$ hoặc $\sigma_t^{2(w)}$ thay đổi đáng kể giữa các giai đoạn, chuỗi có khả năng chứa non-stationarity.

### 3.3. Kiểm định thống kê

Hai kiểm định thường được sử dụng với giả thuyết đối lập:

**ADF test**

* $H_0$: chuỗi có unit root → non-stationary.
* $H_1$: chuỗi không có unit root → stationary.

**KPSS test**

* $H_0$: chuỗi stationary.
* $H_1$: chuỗi non-stationary.

Do hai kiểm định có giả thuyết gốc khác nhau, việc sử dụng kết hợp ADF và KPSS giúp giảm khả năng kết luận dựa trên một kiểm định đơn lẻ.

---

## 4. Các phương pháp chuyển đổi về Stationarity

Mục tiêu của stationarization không phải là biến đổi dữ liệu một cách máy móc, mà là **loại bỏ hoặc giảm thành phần gây ra sự thay đổi thống kê theo thời gian trong khi vẫn bảo toàn thông tin cần thiết cho bài toán dự báo**.

### 4.1. Differencing

Differencing là phương pháp phổ biến để loại bỏ trend:

$$\Delta X_t=X_t-X_{t-1}$$

Với differencing bậc $d$:

$$\Delta^dX_t=(1-B)^dX_t$$

trong đó $B$ là toán tử lag.

First-order differencing thường được sử dụng khi chuỗi có non-stationarity ở mức trung bình. Nếu dữ liệu có seasonality với chu kỳ $s$, có thể sử dụng seasonal differencing:

$$\Delta_sX_t=X_t-X_{t-s}$$

Differencing giúp ổn định mức trung bình bằng cách loại bỏ sự thay đổi của level và trend; tuy nhiên, differencing quá mức có thể làm mất thông tin dài hạn và tạo thêm nhiễu.

### 4.2. Logarithmic transformation

Khi phương sai tăng theo mức của chuỗi, logarithmic transformation có thể giúp ổn định variance:

$$X'_t=\log(X_t)$$

Đối với dữ liệu có giá trị dương, phép biến đổi này đặc biệt phù hợp với các chuỗi có tăng trưởng theo cấp số nhân.

Sau khi dự báo, cần áp dụng phép biến đổi ngược để đưa kết quả về không gian ban đầu:

$$\hat{X}_t=\exp(\hat{X}'_t)$$

Nếu dữ liệu chứa giá trị bằng hoặc nhỏ hơn 0, cần lựa chọn một transformation phù hợp thay vì áp dụng trực tiếp logarithm.

### 4.3. Detrending

Nếu non-stationarity chủ yếu đến từ trend, có thể ước lượng thành phần xu hướng và loại bỏ nó:

$$X_t=T_t+R_t$$

với $T_t$ là trend và $R_t$ là residual.

Sau khi ước lượng $\hat{T}_t$:

$$R_t=X_t-\hat{T}_t$$

Nếu residual có đặc tính ổn định hơn theo thời gian, mô hình có thể được xây dựng trên $R_t$ và sau đó tái kết hợp trend khi chuyển dự báo về không gian ban đầu. Phương pháp này phù hợp khi trend có thể được mô hình hóa tương đối rõ ràng.

---

## 5. Stationarity và thứ tự xử lý dữ liệu

Trong pipeline preprocessing, stationarity cần được xem xét **sau khi dữ liệu đã được làm sạch và trước khi áp dụng các biến đổi phụ thuộc vào cấu trúc động của chuỗi**.

Quan hệ với các mục trong Chương 4 có thể biểu diễn như sau:

```text
Raw Time Series
      │
      ▼
Data Cleaning
      │
      ├── Missing Data
      ├── Outlier Detection
      └── Noise Reduction
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
      ├── Stationary
      │       │
      │       ▼
      │   Continue Pipeline
      │
      └── Non-stationary
              │
              ▼
       Differencing /
       Detrending /
       Variance Transformation
              │
              ▼
       Re-evaluate Stationarity
              │
              ▼
       Decomposition
```

Tuy nhiên, **stationarization không phải bước bắt buộc trong mọi pipeline machine learning**. Đối với các mô hình có khả năng học trực tiếp trend hoặc seasonal structure, chẳng hạn một số kiến trúc deep learning, việc differencing dữ liệu có thể làm mất thông tin mà mô hình có thể khai thác.

Do đó, quyết định stationarize phải phụ thuộc vào **mục tiêu dự báo, đặc tính dữ liệu và mô hình được sử dụng**.

---

## 6. Trade-off của Stationarization

Stationarization tạo ra sự cân bằng giữa **tính ổn định thống kê** và **khả năng bảo toàn thông tin gốc**.

| Phương pháp           | Mục tiêu chính         | Ưu điểm                        | Hạn chế                       |
| --------------------- | ---------------------- | ------------------------------ | ----------------------------- |
| Differencing          | Loại trend             | Đơn giản, hiệu quả             | Mất thông tin level           |
| Seasonal differencing | Loại seasonal pattern  | Phù hợp dữ liệu chu kỳ         | Có thể làm tăng nhiễu         |
| Log transformation    | Ổn định variance       | Giảm ảnh hưởng của giá trị lớn | Yêu cầu xử lý giá trị $\leq0$ |
| Detrending            | Loại xu hướng          | Giữ được residual structure    | Phụ thuộc mô hình trend       |
| Decomposition         | Tách trend/seasonality | Giữ riêng các thành phần       | Có thể phức tạp hơn           |

Vì vậy, không nên mặc định rằng chuỗi phải được biến đổi thành stationary trước khi đưa vào mô hình. Một phép biến đổi chỉ nên được sử dụng khi nó giải quyết một vấn đề cụ thể của dữ liệu và không làm mất thông tin quan trọng đối với nhiệm vụ dự báo.

---

## 7. Nguyên tắc áp dụng trong nghiên cứu

Đối với preprocessing chuỗi thời gian, stationarity được sử dụng theo bốn nguyên tắc:

1. **Phát hiện trước khi biến đổi:** xác định nguyên nhân non-stationarity trước khi lựa chọn phương pháp.
2. **Chọn transformation theo nguyên nhân:** trend sử dụng differencing hoặc detrending; variance thay đổi có thể sử dụng log transformation.
3. **Đánh giá lại sau transformation:** kiểm tra lại time plot, rolling statistics, ACF và statistical tests.
4. **Bảo toàn khả năng diễn giải:** nếu transformation được áp dụng cho target, cần lưu phép biến đổi để có thể inverse-transform dự báo về đơn vị ban đầu.

Như vậy, stationarity đóng vai trò là **cầu nối giữa transformation và decomposition** trong Chương 4. Sau khi dữ liệu được đưa về trạng thái phù hợp hoặc xác định rằng stationarization không cần thiết, **04_decomposition.md** sẽ tiếp tục xử lý việc tách chuỗi thành các thành phần như trend, seasonal và residual nhằm phân tích cấu trúc bên trong của dữ liệu.

---

## Tài liệu tham khảo chính

* NIST, *Engineering Statistics Handbook — Stationarity*.
* Hyndman, R. J. & Athanasopoulos, G., *Forecasting: Principles and Practice*, phần Stationarity and Differencing.
* Amiri-Simkooei, A., Tiberius, C. & Verhagen, S., *Time Series Stationarity*, Delft University of Technology.
