# Preprocessing Methods

## 1. Mục tiêu

Các phương pháp preprocessing trong thực nghiệm được lựa chọn theo taxonomy được trình bày ở [Chương 2](../02_overview/02_taxonomy.md), với mục tiêu đánh giá tác động của từng nhóm xử lý đối với **chất lượng dữ liệu**, **biểu diễn đầu vào** và **hiệu quả của mô hình AI**.

Nghiên cứu gốc nhấn mạnh rằng preprocessing là một quá trình gồm nhiều bước và có ảnh hưởng trực tiếp đến hiệu quả huấn luyện cũng như chất lượng đầu ra của các hệ thống AI. Đồng thời, nghiên cứu tổ chức preprocessing của numerical time series thành các nhóm có cấu trúc và thực hiện empirical analysis để đánh giá tác động của các kỹ thuật này.

Trong chương thực nghiệm này, các phương pháp được tổ chức thành pipeline:

$$
\text{Raw Time Series}
\rightarrow
\text{Cleaning}
\rightarrow
\text{Transformation}
\rightarrow
\text{Feature Engineering}
\rightarrow
\text{Feature Selection}
\rightarrow
\text{Model Input}.
$$

Không phải mọi phương pháp đều được áp dụng đồng thời. Việc lựa chọn phương pháp phụ thuộc vào vấn đề dữ liệu mà phương pháp đó nhằm giải quyết.

---

## 2. Data Cleaning

Data cleaning là nhóm preprocessing đầu tiên, nhằm loại bỏ hoặc xử lý các vấn đề về chất lượng dữ liệu trước khi thực hiện các phép biến đổi tiếp theo.

Ba vấn đề chính được xem xét là:

$$
\boxed{
\text{Missing Values}
+
\text{Outliers}
+
\text{Noise}
}
$$

### 2.1. Missing-value handling

Với một chuỗi thời gian

$$
\mathcal{X}=

{x_t}_{t=1}^{T},
$$

missing value xuất hiện khi $x_t$ không quan sát được.

Các chiến lược được xem xét gồm:

* **Deletion**: loại bỏ các quan sát chứa giá trị thiếu;
* **Forward fill**: sử dụng giá trị quan sát trước đó;
* **Backward fill**: sử dụng giá trị quan sát tiếp theo;
* **Mean/median imputation**: thay thế bằng thống kê trung tâm;
* **Interpolation**: ước lượng giá trị dựa trên các quan sát lân cận.

Đối với time series, interpolation có thể được biểu diễn đơn giản bởi:

$$
\widehat{x}_t=

x_{t_1}
+
\frac{t-t_1}{t_2-t_1}
(x_{t_2}-x_{t_1}),
$$

với $t_1 \lt t \lt t_2$ là hai thời điểm có dữ liệu quan sát.

Việc lựa chọn phương pháp phải xét đến cấu trúc thời gian. Mean hoặc median có thể làm mất temporal structure, trong khi interpolation có khả năng bảo toàn tốt hơn xu hướng cục bộ đối với các khoảng thiếu ngắn.

---

## 3. Outlier Detection and Handling

Outlier là quan sát có giá trị khác biệt đáng kể so với hành vi thông thường của chuỗi.

Một phương pháp cơ bản là **Interquartile Range (IQR)**:

$$
IQR=Q_3-Q_1.
$$

Một quan sát được xác định là outlier nếu:

$$
x_t \lt Q_1-\alpha IQR
$$

hoặc

$$
x_t \gt Q_3+\alpha IQR,
$$

với $\alpha$ thường được chọn bằng $1.5$.

Một lựa chọn khác là Z-score:

$$
z_t=
\frac{x_t-\mu}{\sigma}.
$$

Quan sát có

$$
|z_t|>\tau
$$

có thể được đánh dấu là outlier.

Tuy nhiên, đối với time series, một giá trị cực trị không nhất thiết là lỗi. Nó có thể biểu diễn một sự kiện thực tế. Vì vậy, preprocessing không mặc định loại bỏ toàn bộ outlier.

Các chiến lược xử lý bao gồm:

$$
\text{Outlier}
\rightarrow
\begin{cases}
\text{Drop}\
\text{Clip}\
\text{Interpolation}\
\text{Smoothing}
\end{cases}
$$

Việc phân biệt **detection** và **handling** là cần thiết: detection xác định vị trí bất thường, còn handling quyết định cách dữ liệu được biến đổi sau đó.

---

## 4. Noise Reduction

Dữ liệu cảm biến có thể được mô hình hóa bởi:

$$
x_t=s_t+\epsilon_t,
$$

trong đó $s_t$ là tín hiệu có cấu trúc và $\epsilon_t$ là noise.

Mục tiêu của noise reduction là tìm một phép biến đổi $R(\cdot)$ sao cho:

$$
\widehat{s}_t=

R(x_t),
$$

trong khi vẫn bảo toàn các biến động có ý nghĩa của $s_t$.

Các phương pháp điển hình gồm:

* moving average;
* exponential smoothing;
* median filtering;
* low-pass filtering;
* các phương pháp smoothing dựa trên mô hình.

Ví dụ, moving average với cửa sổ $w$:

$$
\widehat{x}_t=

\frac{1}{w}
\sum_{i=0}^{w-1}x_{t-i}.
$$

Kích thước cửa sổ càng lớn thì mức smoothing càng mạnh, nhưng đồng thời nguy cơ làm mất các biến động ngắn hạn cũng tăng.

Do đó, noise reduction được đánh giá theo trade-off:

$$
\text{Noise Reduction}
\leftrightarrow
\text{Signal Preservation}.
$$

---

## 5. Scaling and Normalization

Sau data cleaning, các biến có thể vẫn có miền giá trị khác nhau. Scaling đưa các biến về một thang đo phù hợp hơn với thuật toán học máy.

### 5.1. Min-Max normalization

Min-Max scaling được định nghĩa:

$$
x_t'=

\frac{x_t-x_{\min}}
{x_{\max}-x_{\min}}.
$$

Phép biến đổi này thường đưa dữ liệu về khoảng $[0,1]$.

### 5.2. Standardization

Standardization được định nghĩa:

$$
x_t'=

\frac{x_t-\mu}{\sigma}.
$$

Sau biến đổi, dữ liệu có trung bình gần $0$ và độ lệch chuẩn gần $1$ trên tập dùng để ước lượng $\mu$ và $\sigma$.

Trong thực nghiệm, các tham số scaling phải được học trên training set:

$$
P_{\mathrm{train}}=

\operatorname{fit}
(\mathcal{D}_{\mathrm{train}}),
$$

sau đó áp dụng cho validation và test:

$$
\mathcal{D}_{\mathrm{val}}'=

P_{\mathrm{train}}
(\mathcal{D}_{\mathrm{val}}),
$$

$$
\mathcal{D}_{\mathrm{test}}'=

P_{\mathrm{train}}
(\mathcal{D}_{\mathrm{test}}).
$$

Quy tắc này nhằm tránh leakage từ validation hoặc test vào preprocessing pipeline.

---

## 6. Data Transformation

Scaling chỉ thay đổi thang đo. Data transformation rộng hơn, nhằm thay đổi representation hoặc phân phối của biến.

Một dạng tổng quát là:

$$
x_t'=

g(x_t),
$$

với $g(\cdot)$ là một transformation function.

Các transformation có thể được sử dụng để:

* giảm skewness;
* ổn định variance;
* làm giảm ảnh hưởng của extreme values;
* đưa dữ liệu về representation phù hợp hơn với mô hình.

Một ví dụ là logarithmic transformation:

$$
x_t'=

\log(1+x_t).
$$

Đối với dữ liệu có giá trị dương và phân phối lệch phải, transformation này có thể làm giảm độ lệch của phân phối.

Transformation phải được lựa chọn dựa trên đặc điểm dữ liệu thay vì áp dụng mặc định cho mọi biến.

---

## 7. Stationarity and Decomposition

Đối với time series, preprocessing có thể bao gồm các phép biến đổi nhằm làm rõ hoặc loại bỏ các thành phần có cấu trúc.

Một chuỗi có thể được biểu diễn theo dạng:

$$
x_t=

T_t+S_t+R_t,
$$

trong đó:

* $T_t$: trend;
* $S_t$: seasonal component;
* $R_t$: residual.

Decomposition tách chuỗi thành các thành phần để mô hình có thể xử lý từng thành phần riêng biệt.

Trong trường hợp multiplicative decomposition:

$$
x_t=

T_tS_tR_t.
$$

Các kỹ thuật decomposition được trình bày chi tiết trong [04_decomposition.md](../04_data_transformation/04_decomposition.md).

Đối với stationarity, một phép sai phân đơn giản được biểu diễn:

$$
\nabla x_t=

x_t-x_{t-1}.
$$

Sai phân có thể làm giảm trend và hỗ trợ các mô hình yêu cầu chuỗi gần stationary.

Tuy nhiên, differencing không được xem là một bước bắt buộc cho mọi mô hình học máy. Việc áp dụng phải dựa trên đặc điểm của chuỗi và yêu cầu của mô hình.

---

## 8. Feature Engineering

Sau khi dữ liệu được làm sạch và biến đổi, temporal structure có thể được chuyển thành các đặc trưng rõ ràng hơn.

### 8.1. Temporal features

Từ timestamp có thể xây dựng:

$$
\mathbf{f}_t^{\mathrm{time}}=

[
\mathrm{hour},
\mathrm{day},
\mathrm{week},
\mathrm{month},
\mathrm{weekday},
\ldots
].
$$

Đối với biến tuần hoàn, có thể sử dụng encoding:

$$
x_{\sin}=

\sin
\left(
\frac{2\pi t}{P}
\right),
$$

$$
x_{\cos}=

\cos
\left(
\frac{2\pi t}{P}
\right),
$$

với $P$ là chu kỳ.

### 8.2. Lag features

Lag feature biểu diễn quá khứ của một biến:

$$
x_{t-k},
\qquad
k\in\mathcal{K}.
$$

Một vector lag có dạng:

$$
\mathbf{f}_t^{\mathrm{lag}}=

[
x_{t-1},
x_{t-2},
\ldots,
x_{t-K}
].
$$

Lag features cho phép các mô hình dạng tabular khai thác temporal dependence.

### 8.3. Rolling features

Rolling statistics được tính trên cửa sổ:

$$
W_t=

{x_{t-w+1},\ldots,x_t}.
$$

Rolling mean:

$$
\mu_t^{(w)}=

\frac{1}{w}
\sum_{i=0}^{w-1}x_{t-i}.
$$

Rolling standard deviation:

$$
\sigma_t^{(w)}=

\sqrt{
\frac{1}{w}
\sum_{i=0}^{w-1}
(x_{t-i}-\mu_t^{(w)})^2
}.
$$

Các đặc trưng này mô tả trạng thái cục bộ của chuỗi và có thể giúp mô hình nhận diện trend hoặc volatility.

---

## 9. Feature Selection

Feature engineering có thể làm tăng số lượng biến:

$$
d_{\mathrm{engineered}}

\gt

d_{\mathrm{raw}}.
$$

Không phải tất cả các biến mới đều mang thông tin hữu ích. Feature selection nhằm tìm một tập con:

$$
\mathcal{F}^{*}
\subseteq
\mathcal{F}
$$

sao cho mô hình vẫn duy trì hoặc cải thiện hiệu quả trong khi giảm số lượng đặc trưng.

Các nhóm chính gồm:

### Filter methods

Đánh giá đặc trưng độc lập với mô hình dựa trên các tiêu chí thống kê hoặc tương quan.

### Wrapper methods

Đánh giá các tập đặc trưng thông qua hiệu quả của một mô hình cụ thể.

### Embedded methods

Thực hiện selection trong quá trình huấn luyện mô hình.

Chi tiết được trình bày trong [06_feature_selection](../06_feature_selection/01_feature_selection.md).

---

## 10. Dimensionality Reduction

Khác với feature selection, dimensionality reduction tạo ra các biến mới từ không gian đặc trưng ban đầu.

Với ma trận:

$$
\mathbf{X}
\in
\mathbb{R}^{N\times d},
$$

mục tiêu là tìm representation:

$$
\mathbf{Z}=

f(\mathbf{X}),
\qquad
\mathbf{Z}\in\mathbb{R}^{N\times k},
$$

với

$$
k<d.
$$

Một phương pháp điển hình là Principal Component Analysis (PCA). PCA tìm các hướng có phương sai lớn nhất và biểu diễn dữ liệu trên các principal components.

Nếu $\mathbf{X}$ đã được center, covariance matrix là:

$$
\mathbf{\Sigma}=

\frac{1}{N-1}
\mathbf{X}^{\top}\mathbf{X}.
$$

Các principal components được xác định từ bài toán eigenvalue:

$$
\mathbf{\Sigma}\mathbf{v}_j=

\lambda_j\mathbf{v}_j.
$$

Representation sau giảm chiều có thể viết:

$$
\mathbf{Z}=

\mathbf{X}
\mathbf{V}_k.
$$

Dimensionality reduction được đánh giá dựa trên sự cân bằng giữa giảm số chiều và bảo toàn thông tin.

---

## 11. Experimental Preprocessing Configurations

Để kết quả có thể so sánh, các phương pháp được tổ chức thành các configuration thay vì áp dụng tùy ý.

Một configuration tổng quát được biểu diễn:

$$
C
=

(P_{\mathrm{clean}},
P_{\mathrm{transform}},
P_{\mathrm{feature}},
P_{\mathrm{selection}}).
$$

Baseline:

$$
C_0=

(
P_{\mathrm{minimal}}
).
$$

Một configuration mở rộng có thể có dạng:

$$
C_1=

(
P_{\mathrm{clean}},
P_{\mathrm{scale}}
),
$$

trong khi configuration đầy đủ có thể biểu diễn:

$$
C_2=

(
P_{\mathrm{clean}},
P_{\mathrm{scale}},
P_{\mathrm{feature}},
P_{\mathrm{selection}}
).
$$

Các configuration được đánh giá trên cùng dataset, cùng temporal split và cùng evaluation protocol. Điều này giúp giảm ảnh hưởng của các yếu tố ngoài preprocessing khi so sánh kết quả.

---

## 12. Nguyên tắc lựa chọn phương pháp

Không có preprocessing method duy nhất phù hợp với mọi time series. Việc lựa chọn được thực hiện dựa trên quan hệ:

$$
\text{Data Problem}
\rightarrow
\text{Preprocessing Method}.
$$

Có thể tóm tắt:

| Vấn đề                   | Phương pháp ưu tiên          |
| ------------------------ | ---------------------------- |
| Missing observations     | Imputation                   |
| Extreme observations     | Outlier detection / handling |
| High-frequency noise     | Smoothing / filtering        |
| Different feature scales | Scaling / normalization      |
| Skewed distribution      | Transformation               |
| Trend / seasonality      | Differencing / decomposition |
| Temporal dependence      | Lag / rolling features       |
| Redundant features       | Feature selection            |
| High dimensionality      | Dimensionality reduction     |

Việc lựa chọn không dựa đơn thuần trên khả năng cải thiện metric. Một phương pháp còn phải được xem xét theo khả năng bảo toàn temporal structure, computational cost và khả năng triển khai.

---

## 13. Kiểm soát data leakage

Tất cả preprocessing methods có tham số được học từ dữ liệu phải tuân thủ nguyên tắc:

$$
\boxed{
\text{Fit on Train}
\rightarrow
\text{Transform Validation/Test}
}
$$

Ví dụ, với feature selection:

$$
\mathcal{F}^{*}=

S(\mathcal{D}_{\mathrm{train}}),
$$

sau đó chỉ các feature trong $\mathcal{F}^{*}$ mới được sử dụng cho validation và test.

Tương tự, PCA phải được fit trên training data:

$$
\mathbf{V}_k=

\operatorname{PCA}
(\mathcal{D}_{\mathrm{train}}),
$$

sau đó áp dụng cùng projection cho các tập còn lại.

Đây là điều kiện bắt buộc để kết quả phản ánh khả năng tổng quát hóa thực sự thay vì lợi thế do information leakage.

---

## 14. Liên kết với đánh giá thực nghiệm

Sau preprocessing, dữ liệu được đưa vào cùng một modeling pipeline:

$$
\mathcal{D}
\xrightarrow{P}
\mathcal{D}'
\xrightarrow{f_\theta}
\widehat{\mathbf{y}}
\xrightarrow{M}
\text{Performance}.
$$

Trong đó:

* $P$ là preprocessing pipeline;
* $\mathcal{D}'$ là dữ liệu sau preprocessing;
* $f_\theta$ là mô hình học máy;
* $\widehat{\mathbf{y}}$ là dự báo;
* $M$ là evaluation metric.

Do đó, sự khác biệt về performance giữa hai configuration được quy về sự khác biệt trong preprocessing khi các thành phần khác được giữ cố định.

Các metric được sử dụng trong thực nghiệm được trình bày trong [04_evaluation_metrics.md](04_evaluation_metrics.md), trong khi kết quả định lượng được trình bày trong [05_results.md](05_results.md).

Nội dung này cũng phù hợp với mục tiêu của nghiên cứu gốc: xây dựng một phạm vi preprocessing có cấu trúc cho numerical time series, đồng thời đánh giá thực nghiệm tác động của preprocessing đến chất lượng dữ liệu và hiệu quả của các thuật toán AI.
