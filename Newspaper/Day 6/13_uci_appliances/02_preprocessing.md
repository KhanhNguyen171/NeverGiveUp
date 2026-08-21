# 02. Preprocessing

## 1. Mục tiêu preprocessing

Trong `13_air_quality/01_dataset.md`, AirQuality được xác định là dữ liệu chuỗi thời gian đa biến gồm các phép đo cảm biến, chất ô nhiễm và điều kiện môi trường. Đặc điểm quan trọng của dataset là sự tồn tại của **missing values được mã hóa bằng `-200`**, outliers và sự khác biệt về scale giữa các biến.

Trong bài báo, preprocessing được sử dụng như một **biến thực nghiệm** để đánh giá mức độ ảnh hưởng của từng kỹ thuật đến hiệu năng dự đoán CO. Vì vậy, preprocessing không chỉ nhằm làm sạch dữ liệu mà còn phải tạo ra một representation nhất quán cho mô hình LSTM.

Pipeline thực nghiệm có thể khái quát:

```text
Raw AirQuality
      ↓
Missing-value Identification
      ↓
Outlier Detection
      ↓
Outlier Imputation
      ↓
Missing-value Imputation
      ↓
Feature Selection
      ↓
Normalization
      ↓
LSTM
```

Pipeline này liên kết trực tiếp với các chương `03_data_cleaning`, `04_data_transformation` và `06_feature_selection` của survey.

---

## 2. Mã hóa missing values

AirQuality sử dụng giá trị `-200` để biểu diễn các quan sát bị thiếu. Do đó, `-200` không được xem là một giá trị số thực tế của biến cảm biến mà là **missing-value marker**.

Phép chuyển đổi đầu tiên là:

$$
x_t=-200\Rightarrow x_t=\mathrm{NaN}
$$

Sau bước này, missing values mới được xử lý bằng các phương pháp imputation.

Điểm này minh họa nguyên tắc trong `03_data_cleaning/01_missing_data.md`: trước khi lựa chọn phương pháp xử lý missing, cần xác định **semantic meaning** của dữ liệu.

Nếu không thực hiện bước này, các giá trị `-200` sẽ được xem như observations hợp lệ và có thể làm sai lệch:

$$
\mu,\quad \sigma,\quad Q_1,\quad Q_3
$$

cũng như các mô hình thống kê được sử dụng ở các bước sau.

---

## 3. Phân loại missing values

Sau khi thay thế `-200` bằng `NaN`, các missing observations được phân tích theo cấu trúc temporal.

Có thể phân biệt hai trường hợp chính:

### Missing value cô lập

Một hoặc một số observation bị thiếu giữa các observation hợp lệ:

$$
x_{t-1}\neq\mathrm{NaN},\quad x_t=\mathrm{NaN},\quad x_{t+1}\neq\mathrm{NaN}
$$

Các khoảng thiếu ngắn có thể được nội suy dựa trên các observation lân cận.

### Missing sequence

Một chuỗi liên tiếp gồm nhiều observation bị thiếu:

$$
x_t,x_{t+1},\ldots,x_{t+k}=\mathrm{NaN}
$$

Trường hợp này khó xử lý hơn vì thông tin cục bộ xung quanh khoảng thiếu không còn đầy đủ.

Trong experimental setup của bài báo, **Cubic Spline Interpolation** được sử dụng cho missing values cô lập, trong khi **Expectation Maximization (EM)** được sử dụng cho các chuỗi missing values. Điều này cho phép phân biệt giữa missing ngắn và missing có cấu trúc dài hơn.

---

## 4. Outlier Detection

Sau khi xác định missing values, bước tiếp theo là phát hiện các observation bất thường.

Bài báo sử dụng hai phương pháp chính:

* **Grubbs Test**;
* **Interquartile Range (IQR)**.

Việc lựa chọn phương pháp phụ thuộc vào đặc điểm phân phối của feature.

### 4.1. Grubbs Test

Grubbs Test được sử dụng để phát hiện outlier trong dữ liệu có phân phối gần normal.

Thống kê kiểm định có dạng:

$$
G=\frac{\max_i|x_i-\bar{x}|}{s}
$$

trong đó:

* $\bar{x}$ là sample mean;
* $s$ là sample standard deviation.

Nếu thống kê kiểm định vượt quá critical value tương ứng với mức ý nghĩa được lựa chọn, observation có thể được xác định là outlier.

Grubbs Test phù hợp khi giả định về phân phối được đáp ứng; do đó không nên áp dụng máy móc cho mọi feature.

---

## 5. Interquartile Range

Đối với các feature không phù hợp với giả định normality, IQR cung cấp một phương pháp robust hơn.

IQR được định nghĩa:

$$
IQR=Q_3-Q_1
$$

Ngưỡng outlier được xác định:

$$
L=Q_1-1.5IQR
$$

và:

$$
U=Q_3+1.5IQR
$$

Một observation được xem là outlier nếu:

$$
x_t \lt L\quad\text{or}\quad x_t \gt U
$$

Trong dữ liệu cảm biến, outlier không nhất thiết là lỗi đo lường. Một observation cực trị có thể phản ánh một sự kiện ô nhiễm thực tế. Vì vậy, detection và treatment phải được phân biệt:

$$
\mathrm{Detection}\neq\mathrm{Removal}
$$

Đây là điểm quan trọng khi liên hệ với `03_data_cleaning/02_outlier_detection.md`.

---

## 6. Outlier Imputation

Sau khi outlier được xác định, bài báo không đơn giản xóa toàn bộ observation chứa outlier. Thay vào đó, các outlier được xem như những giá trị cần được thay thế để giảm ảnh hưởng của measurement anomalies.

Trong experimental pipeline, **Cubic Spline Interpolation** được sử dụng cho outlier imputation.

Về nguyên lý, spline xây dựng một hàm liên tục:

$$
\hat{x}(t)=S(t)
$$

sao cho giá trị tại các observation hợp lệ được sử dụng để ước lượng giá trị tại vị trí bất thường.

Với một observation bị đánh dấu:

$$
x_t=\mathrm{outlier}
$$

giá trị sau preprocessing trở thành:

$$
x_t\leftarrow\hat{x}_t
$$

trong đó (\hat{x}_t) là giá trị được nội suy.

Việc sử dụng interpolation thay vì xóa observation giúp duy trì cấu trúc temporal của dataset.

---

## 7. Missing-value Imputation

Sau khi outlier đã được xử lý, missing values còn lại được impute.

Đối với missing values cô lập, bài báo sử dụng **Cubic Spline Interpolation**:

$$
x_t=\mathrm{NaN}\Rightarrow x_t\leftarrow\hat{x}_t
$$

Trong trường hợp xuất hiện một chuỗi missing dài, **Expectation Maximization (EM)** được sử dụng.

EM thực hiện lặp giữa hai bước:

### Expectation step

Ước lượng các missing observations dựa trên mô hình hiện tại:

$$
\hat{X}*{\mathrm{miss}}^{(k)}=E[X*{\mathrm{miss}}\mid X_{\mathrm{obs}},\theta^{(k)}]
$$

### Maximization step

Cập nhật tham số mô hình:

$$
\theta^{(k+1)}=\arg\max_{\theta}E[\log p(X\mid\theta)\mid X_{\mathrm{obs}},\theta^{(k)}]
$$

Quá trình lặp cho đến khi hội tụ.

Do đó, bài báo sử dụng hai chiến lược khác nhau tùy theo cấu trúc missing:

$$
\boxed{\mathrm{Short\ Missing}\rightarrow\mathrm{Spline}}
$$

$$
\boxed{\mathrm{Long\ Missing}\rightarrow\mathrm{EM}}
$$

---

## 8. Feature Selection

Sau data cleaning, bước tiếp theo là lựa chọn các feature phù hợp với mô hình.

Bài báo sử dụng hai phương pháp feature selection:

* **Neighborhood Component Analysis (NCA)**;
* **Laplacian Scores**.

Hai phương pháp đại diện cho hai góc nhìn khác nhau về feature relevance.

### 8.1. Neighborhood Component Analysis

NCA đánh giá feature dựa trên khả năng hỗ trợ phân biệt các observation lân cận trong feature space.

Mục tiêu có thể khái quát:

$$
\theta^*=\arg\max_{\theta}\mathcal{L}(\theta)
$$

trong đó (\theta) biểu diễn trọng số của các feature.

Các feature có trọng số thấp có thể được xem xét loại bỏ.

Điều này liên kết với `06_feature_selection/04_embedded_methods.md` vì feature weighting được thực hiện trong quá trình tối ưu của phương pháp.

### 8.2. Laplacian Scores

Laplacian Score đánh giá mức độ phù hợp của một feature với cấu trúc cục bộ của dữ liệu.

Một feature có Laplacian Score thấp thường được xem là có khả năng bảo toàn tốt cấu trúc lân cận của dữ liệu.

Do đó, các feature được xếp hạng theo score và một số feature có relevance thấp được loại bỏ.

Hai phương pháp được sử dụng để tạo ra các feature subsets khác nhau, từ đó cho phép nghiên cứu đánh giá tác động của feature selection.

---

## 9. Normalization

Sau data cleaning và feature selection, các feature được normalization trước khi đưa vào LSTM.

Đối với Min-Max normalization:

$$
x'=\frac{x-x_{\min}}{x_{\max}-x_{\min}}
$$

Giá trị được đưa về khoảng:

$$
x'\in[0,1]
$$

Normalization giúp giảm sự khác biệt về scale giữa các feature.

Điều này đặc biệt quan trọng đối với AirQuality vì dataset chứa các biến có miền giá trị khác nhau, chẳng hạn:

* nồng độ CO;
* nồng độ NOx;
* nồng độ NO2;
* nhiệt độ;
* độ ẩm;
* sensor responses.

Nếu không normalization, các feature có magnitude lớn có thể ảnh hưởng không cân đối đến quá trình tối ưu của mô hình.

---

## 10. Thứ tự của preprocessing

Thứ tự các bước preprocessing trong experimental pipeline có ý nghĩa quan trọng.

Quy trình được sử dụng có thể biểu diễn:

```text
AirQuality
   ↓
-200 → NaN
   ↓
Outlier Detection
   ↓
Outlier Imputation
   ↓
Missing-value Imputation
   ↓
Feature Selection
   ↓
Normalization
   ↓
LSTM
```

Thứ tự này phản ánh dependency giữa các bước.

Ví dụ, nếu normalization được thực hiện trước khi xử lý `-200`, giá trị missing marker có thể được xem như một observation thực và ảnh hưởng đến các tham số normalization.

Tương tự, nếu feature selection được thực hiện trước khi xử lý dữ liệu bất thường, các statistical relationships có thể bị outlier làm sai lệch.

Do đó:

$$
\boxed{\mathrm{Cleaning}\rightarrow\mathrm{Selection}\rightarrow\mathrm{Transformation}}
$$

là logic chính của pipeline thực nghiệm.

---

## 11. Train-Test Protocol

Bài báo chia dataset thành:

$$
D=D_{\mathrm{train}}\cup D_{\mathrm{test}}
$$

với:

$$
|D_{\mathrm{train}}|=0.9|D|
$$

và:

$$
|D_{\mathrm{test}}|=0.1|D|
$$

Tập Test được giữ lại để đánh giá cuối cùng.

Với các transformation có tham số học từ dữ liệu, nguyên tắc tổng quát của survey yêu cầu:

$$
\theta=f(D_{\mathrm{train}})
$$

sau đó:

$$
D_{\mathrm{test}}'=f(D_{\mathrm{test}};\theta)
$$

Như vậy, Test không được tham gia vào quá trình fitting preprocessing.

Đây là điểm cần phân biệt giữa **experimental protocol của bài báo** và **nguyên tắc methodological của survey**: tỷ lệ 90/10 được kế thừa từ bài báo, trong khi Train-only fitting là nguyên tắc kiểm soát leakage được áp dụng khi triển khai pipeline.

---

## 12. Preprocessing Configurations

Một đóng góp quan trọng của bài báo là không chỉ xây dựng một preprocessing pipeline duy nhất. Các kỹ thuật được thay đổi trong các experiment để đánh giá tác động của từng nhóm preprocessing.

Có thể biểu diễn một preprocessing configuration:

$$
C=(M,O,I,F,N)
$$

trong đó:

* $M$: missing-value handling;
* $O$: outlier detection;
* $I$: outlier/missing imputation;
* $F$: feature selection;
* $N$: normalization.

Một configuration cụ thể có thể là:

$$
C_1=(\mathrm{Spline},\mathrm{IQR},\mathrm{Spline},\mathrm{NCA},\mathrm{MinMax})
$$

Trong khi configuration khác có thể thay đổi phương pháp outlier detection hoặc feature selection.

Cách thiết kế này cho phép đánh giá:

$$
\Delta\mathrm{Performance}=

\mathrm{Performance}(C_i)-\mathrm{Performance}(C_{\mathrm{baseline}})
$$

và xác định preprocessing nào tạo ra ảnh hưởng đáng kể đến mô hình.

---

## 13. Kết nối với các chương preprocessing

Case study AirQuality trực tiếp hiện thực hóa các nhóm phương pháp trong survey:

| Survey                                               | AirQuality implementation                              |
| ---------------------------------------------------- | ------------------------------------------------------ |
| `03_data_cleaning/01_missing_data.md`                | `-200 → NaN`, Spline, EM                               |
| `03_data_cleaning/02_outlier_detection.md`           | Grubbs, IQR                                            |
| `03_data_cleaning/03_noise_reduction.md`             | Xử lý các biến động bất thường thông qua preprocessing |
| `04_data_transformation/01_scaling_normalization.md` | Min-Max normalization                                  |
| `06_feature_selection/01_feature_selection.md`       | Feature subset construction                            |
| `06_feature_selection/04_embedded_methods.md`        | NCA-based feature weighting                            |
| `09_empirical_analysis/03_preprocessing_methods.md`  | Experimental comparison                                |
| `09_empirical_analysis/04_evaluation_metrics.md`     | RMSE, MAE, MAPE                                        |

Do đó, Chương 13 không giới thiệu một taxonomy mới mà sử dụng AirQuality để **instantiate taxonomy đã xây dựng ở các chương trước**.

---

## 14. AI-ready Representation

Sau preprocessing, mỗi observation được biểu diễn bằng một vector feature đã được làm sạch, lựa chọn và normalization:

$$
\mathbf{x}_t\in\mathbb{R}^{F}
$$

Target tương ứng là:

$$
y_t=\mathrm{CO}_t
$$

Do đó, dữ liệu đầu vào cho bài toán regression có dạng:

$$
\mathcal{D}=\left{\left(\mathbf{x}*t,y_t\right)\right}*{t=1}^{N}
$$

Trong trường hợp representation được đưa vào LSTM theo chuỗi thời gian, một sequence có thể được biểu diễn:

$$
\mathbf{X}*{t-L+1:t}=\left[\mathbf{x}*{t-L+1},\mathbf{x}_{t-L+2},\ldots,\mathbf{x}_t\right]
$$

và target tương ứng:

$$
y_t=\mathrm{CO}_t
$$

Khác với pipeline forecasting của **UCI Appliances** mà chúng ta đã viết trước đó, **không nên mặc định dùng $y_{t+1}$ hoặc sequence-to-one horizon $H=1$ ở đây nếu không có trong experimental protocol của bài báo**. AirQuality trong bài báo được sử dụng để đánh giá preprocessing cho bài toán dự đoán CO với LSTM, vì vậy ký hiệu phải bám theo formulation thực tế của bài báo.

---

## 15. Tóm tắt

Preprocessing của AirQuality tập trung vào năm thành phần chính:

$$
\boxed{\mathrm{Missing}\rightarrow\mathrm{Outlier}\rightarrow\mathrm{Imputation}\rightarrow\mathrm{Feature\ Selection}\rightarrow\mathrm{Normalization}}
$$

Trong đó:

* `-200` được chuyển thành missing values;
* Grubbs Test và IQR được sử dụng cho outlier detection;
* Cubic Spline và EM được sử dụng cho imputation;
* NCA và Laplacian Scores được sử dụng cho feature selection;
* normalization được thực hiện trước khi đưa dữ liệu vào LSTM.

Pipeline này thể hiện rõ vai trò của preprocessing trong nghiên cứu: **không chỉ sửa dữ liệu mà còn thay đổi representation của dữ liệu trước khi mô hình học máy được huấn luyện**.

Với AirQuality, mối quan hệ giữa preprocessing và modeling có thể tóm tắt:

$$
\boxed{\mathrm{Raw\ AirQuality}\rightarrow\mathrm{Cleaned\ Data}\rightarrow\mathrm{Selected\ Features}\rightarrow\mathrm{Normalized\ Data}\rightarrow\mathrm{LSTM}}
$$

Đây là cơ sở để mục `13_air_quality/03_feature_engineering.md` phân tích cách các đặc trưng thời gian và đặc trưng cảm biến được biểu diễn, đồng thời kết nối trực tiếp với taxonomy về feature engineering ở Chương 5.
