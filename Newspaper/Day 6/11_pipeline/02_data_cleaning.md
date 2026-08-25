# 11.2 Data Cleaning Pipeline

## 1. Mục tiêu

Data cleaning là giai đoạn đầu tiên của preprocessing pipeline, nhằm chuyển dữ liệu chuỗi thời gian từ trạng thái quan sát ban đầu sang trạng thái có **tính hợp lệ, nhất quán và đủ tin cậy cho các bước biến đổi và xây dựng đặc trưng tiếp theo**.

Đối với numerical time series, các vấn đề chính cần xử lý gồm missing values, outliers, noise, duplicate observations và các bất nhất liên quan đến timestamp. Nghiên cứu của Tawakuli et al. xem việc xử lý các vấn đề này là một thành phần quan trọng của preprocessing, bởi chất lượng dữ liệu có thể ảnh hưởng trực tiếp đến quá trình huấn luyện và kết quả của các thuật toán AI.

Trong pipeline của nghiên cứu này, data cleaning được tổ chức theo nguyên tắc:

$$
\mathcal{X}_{raw}
\xrightarrow{\text{Validation}}
\mathcal{X}_{valid}
\xrightarrow{\text{Missing}}
\mathcal{X}_{complete}
\xrightarrow{\text{Outlier}}
\mathcal{X}_{robust}
\xrightarrow{\text{Noise}}
\mathcal{X}_{clean}.
$$

Mục tiêu không phải là loại bỏ mọi giá trị bất thường, mà là **phân biệt lỗi dữ liệu với biến động thực tế của hệ thống** và chỉ thực hiện correction khi có đủ cơ sở.

---

## 2. Input và output của pipeline

Cho tập dữ liệu chuỗi thời gian:

$$
\mathcal{D}=

\left \{
(t_i,\mathbf{x}_i)
\right \}_{i=1}^{N},
$$

trong đó:

* $t_i$ là timestamp của observation thứ $i$;
* $\mathbf{x}_i \in \mathbb{R}^{d}$ là vector gồm $d$ numerical features;
* $N$ là số lượng observations.

Data cleaning tạo ra:

$$
\mathcal{D}_{clean}=

\left \{
(\tilde{t}_i,\tilde{\mathbf{x}}_i)
\right \}_{i=1}^{N'},
$$

trong đó $N'$ có thể khác $N$ nếu một số observations bị loại bỏ hoặc dữ liệu được tái cấu trúc.

Một pipeline cleaning hợp lệ cần bảo đảm:

1. timestamp hợp lệ;
2. thứ tự thời gian được duy trì;
3. duplicate được phát hiện và xử lý;
4. missing values được xác định rõ;
5. outliers được phát hiện theo tiêu chí phù hợp;
6. noise được giảm khi cần thiết;
7. không làm thay đổi sai lệch cấu trúc temporal của dữ liệu.

---

## 3. Bước 1 — Data validation

Data validation được thực hiện trước các phép sửa đổi dữ liệu. Mục tiêu là xác định trạng thái ban đầu của dataset và phân biệt **data error** với **missingness, anomaly hoặc variation hợp lệ**.

Các kiểm tra cơ bản gồm:

### 3.1. Kiểm tra schema

Xác định:

* tên feature;
* data type;
* timestamp column;
* numerical columns;
* categorical hoặc metadata columns nếu tồn tại;
* đơn vị đo;
* miền giá trị hợp lệ.

Với mỗi feature $x^{(j)}$, cần xác định miền giá trị:

$$
x^{(j)} \in
\mathcal{R}_j,
$$

trong đó $\mathcal{R}_j$ là miền giá trị hợp lệ dựa trên physical constraint hoặc specification của sensor.

### 3.2. Kiểm tra timestamp

Timestamp phải có khả năng sắp xếp và xác định thứ tự temporal:

$$
t_1 < t_2 < \cdots < t_N.
$$

Đối với dữ liệu được lấy mẫu định kỳ với khoảng thời gian $\Delta t$, cần kiểm tra:

$$
\Delta t_i=t_i-t_{i-1}.
$$

Nếu:

$$
\Delta t_i \neq \Delta t,
$$

có thể tồn tại missing observation, irregular sampling hoặc một khoảng thời gian bị gián đoạn.

Không nên tự động nội suy các khoảng này trước khi xác định nguyên nhân, vì việc đó có thể tạo ra dữ liệu nhân tạo và che giấu vấn đề trong quá trình thu thập.

### 3.3. Duplicate observations

Duplicate timestamp có thể gây sai lệch thống kê và ảnh hưởng đến các phép biến đổi dựa trên temporal ordering.

Với timestamp $t$:

$$
\exists i\neq j:
\quad
t_i=t_j
$$

là điều kiện cho thấy timestamp bị trùng.

Cách xử lý phụ thuộc vào nguyên nhân:

* duplicate hoàn toàn → giữ một observation;
* nhiều measurements hợp lệ tại cùng timestamp → cần aggregation;
* duplicate do lỗi hệ thống → loại bỏ hoặc sửa theo metadata.

Do đó, duplicate detection là bước validation, còn cách xử lý phải phụ thuộc vào semantics của dataset.

---

## 4. Bước 2 — Missing data handling

Missing data xuất hiện khi một hoặc nhiều giá trị trong chuỗi không được quan sát. Với multivariate time series:

$$
\mathbf{x}_t=

[x_t^{(1)},\ldots,x_t^{(d)}],
$$

có thể xảy ra:

$$
x_t^{(j)}=\text{NaN}.
$$

Missingness cần được xem xét ở cả **mức giá trị** và **mức thời gian**.

### 4.1. Phân loại missingness

Có thể phân biệt:

* **isolated missing values**: một số điểm đơn lẻ bị thiếu;
* **consecutive missing values**: một đoạn liên tục bị thiếu;
* **feature-wise missingness**: một feature bị thiếu trong nhiều timestamps;
* **record-wise missingness**: toàn bộ observation bị thiếu.

Đối với time series, độ dài của khoảng missing là yếu tố quan trọng vì khả năng nội suy giảm khi khoảng trống tăng.

### 4.2. Xử lý missing values

Một số chiến lược phổ biến gồm:

#### Forward fill

$$
\hat{x}_t=x_{t-1}.
$$

Phương pháp này đơn giản và phù hợp trong một số trường hợp giá trị có tính persistence cao, nhưng có thể tạo ra các đoạn dữ liệu không phản ánh biến động thực tế.

#### Linear interpolation

Với hai observations đã biết:

$$
(t_a,x_a),
\qquad
(t_b,x_b),
$$

giá trị tại $t$ có thể được nội suy:

$$
\hat{x}_t=

x_a+
\frac{t-t_a}{t_b-t_a}
(x_b-x_a).
$$

Phương pháp này phù hợp với khoảng missing ngắn và biến động tương đối liên tục.

#### Model-based imputation

Có thể sử dụng mô hình thống kê hoặc machine learning để ước lượng:

$$
\hat{x}_t=

f
\left(
\mathbf{x}_{t-k:t-1},
\mathbf{x}_{t+1:t+k}
\right).
$$

Nghiên cứu nền tảng cũng khảo sát nhiều phương pháp imputation và chỉ ra rằng lựa chọn phương pháp phụ thuộc đáng kể vào đặc tính của chuỗi; đối với các chuỗi biến động mạnh và có seasonality, các phương pháp univariate đơn giản có thể không biểu diễn đầy đủ cấu trúc dữ liệu.

Vì vậy, không nên xem một phương pháp imputation duy nhất là lựa chọn mặc định cho mọi dataset.

---

## 5. Bước 3 — Outlier detection

Outlier là observation có hành vi khác biệt đáng kể so với phần còn lại của dữ liệu. Tuy nhiên, trong time series, một outlier không nhất thiết là lỗi.

Một observation:

$$
x_t \not\approx
{x_{t-k},\ldots,x_{t+k}}
$$

có thể là:

* lỗi sensor;
* lỗi transmission;
* measurement artifact;
* hoặc một sự kiện thực tế.

Do đó, outlier detection phải được tách khỏi outlier correction.

### 5.1. Global outlier

Global outlier được xác định dựa trên phân phối toàn bộ dataset.

Một tiêu chí đơn giản dựa trên z-score:

$$
z_t=

\frac{x_t-\mu}{\sigma}.
$$

Nếu:

$$
|z_t| \gt \tau,
$$

observation có thể được đánh dấu là outlier.

Tuy nhiên, phương pháp này nhạy với skewed distribution và extreme values.

### 5.2. Robust detection

Median Absolute Deviation (MAD) sử dụng median thay vì mean:

$$
MAD=

\operatorname{median}
\left(
|x_t-\operatorname{median}(x)|
\right).
$$

Một robust score có thể được biểu diễn:

$$
r_t=

\frac{|x_t-\operatorname{median}(x)|}
{MAD}.
$$

MAD có ưu điểm là ít nhạy với extreme values. Nghiên cứu của Tawakuli et al. cũng xem MAD là một phương pháp thống kê robust để phát hiện outlier và lưu ý khả năng áp dụng trong các cửa sổ dữ liệu cục bộ.

### 5.3. Local và contextual outlier

Trong time series, detection toàn cục có thể bỏ sót những anomaly chỉ bất thường trong một khoảng thời gian.

Ví dụ, một giá trị có thể nằm trong miền phân phối toàn dataset nhưng lại bất thường so với các observations lân cận.

Do đó, có thể sử dụng local window:

$$
W_t=

{x_{t-w+1},\ldots,x_t}.
$$

Các thống kê như local median, local mean hoặc local MAD sau đó được sử dụng để xác định deviation.

Nghiên cứu nền tảng phân biệt global, local, contextual và collective outliers, cho thấy việc xác định anomaly cần xét đến context của observation thay vì chỉ dựa trên phân phối toàn cục.

---

## 6. Bước 4 — Outlier treatment

Sau khi phát hiện outlier, pipeline phải quyết định cách xử lý.

Có bốn chiến lược chính:

### 6.1. Keep

Nếu outlier đại diện cho một sự kiện thực tế:

$$
x_t \rightarrow x_t.
$$

Không nên loại bỏ observation chỉ vì nó có giá trị lớn hoặc nhỏ bất thường.

### 6.2. Remove

Nếu có bằng chứng rằng observation là lỗi:

$$
(t,x_t)
\rightarrow
\varnothing.
$$

Tuy nhiên, việc remove có thể tạo ra khoảng trống mới và do đó phải được đưa trở lại bước missing-data handling.

### 6.3. Replace

Có thể thay thế bằng một estimate:

$$
x_t
\rightarrow
\hat{x}_t.
$$

Estimate có thể được lấy từ interpolation, local median hoặc một mô hình phù hợp.

### 6.4. Winsorization hoặc clipping

Giới hạn observation trong một khoảng:

$$
\tilde{x}_t=

\min
\left(
\max(x_t,l),u
\right).
$$

Phương pháp này làm giảm ảnh hưởng của extreme values nhưng thay đổi trực tiếp giá trị quan sát. Vì vậy, chỉ nên sử dụng khi mục tiêu nghiên cứu cho phép.

Nguyên tắc quan trọng là:

> **Detection không đồng nghĩa với removal.**

Outlier detection chỉ tạo ra thông tin về observation bất thường; quyết định treatment phải dựa trên semantics của dữ liệu và mục tiêu downstream.

---

## 7. Bước 5 — Noise reduction

Noise là thành phần biến động không mong muốn trong tín hiệu:

$$
x_t=s_t+\epsilon_t,
$$

trong đó:

* $s_t$ là underlying signal;
* $\epsilon_t$ là noise.

Mục tiêu của noise reduction là ước lượng:

$$
\hat{s}_t=f(x_t),
$$

sao cho $\hat{s}_t$ giữ lại cấu trúc có ý nghĩa của $s_t$ nhưng giảm ảnh hưởng của $\epsilon_t$.

### 7.1. Moving average

Một bộ lọc đơn giản:

$$
\hat{x}_t=

\frac{1}{w}
\sum_{k=0}^{w-1}
x_{t-k}.
$$

Moving average làm giảm high-frequency fluctuation nhưng có thể làm mờ peaks và thay đổi temporal characteristics.

### 7.2. Median filter

Median filter sử dụng:

$$
\hat{x}_t=

\operatorname{median}
\left(
x_{t-k},\ldots,x_t,\ldots,x_{t+k}
\right).
$$

Phương pháp này đặc biệt hữu ích đối với impulsive noise và có khả năng bảo toàn discontinuity tốt hơn moving average trong một số trường hợp.

### 7.3. Advanced filtering

Tùy ứng dụng, pipeline có thể sử dụng:

* exponential smoothing;
* Savitzky–Golay filtering;
* Kalman filtering;
* wavelet-based denoising.

Tuy nhiên, noise reduction không nên được áp dụng mặc định. Một phép smoothing quá mạnh có thể loại bỏ chính các biến động mà mô hình cần học, đặc biệt đối với anomaly detection, event detection và forecasting các biến động ngắn hạn.

---

## 8. Thứ tự xử lý

Một pipeline cleaning thực tế có thể được tổ chức:

```text id="f9d7e3"
Raw Data
   │
   ▼
Schema & Timestamp Validation
   │
   ▼
Duplicate Detection
   │
   ▼
Missingness Analysis
   │
   ▼
Missing Value Treatment
   │
   ▼
Outlier Detection
   │
   ▼
Outlier Treatment
   │
   ▼
Noise Reduction
   │
   ▼
Post-cleaning Validation
   │
   ▼
Clean Time Series
```

Thứ tự này không phải quy tắc tuyệt đối. Ví dụ, trong một số dataset, outlier detection cần được thực hiện trước imputation vì outlier có thể ảnh hưởng đến tham số của phương pháp imputation. Ngược lại, một số phương pháp cần dữ liệu đầy đủ trước khi có thể tính toán.

Do đó, nguyên tắc tổng quát là:

$$
\text{Ordering}=

f(
\text{data characteristics},
\text{method dependencies},
\text{downstream task}
).
$$

Pipeline phải ghi nhận rõ thứ tự thực tế đã sử dụng để bảo đảm khả năng tái lập.

---

## 9. Post-cleaning validation

Sau khi cleaning, cần thực hiện validation lần thứ hai để kiểm tra tác động của các phép biến đổi.

Các điều kiện tối thiểu gồm:

### Temporal integrity

$$
t_1 \lt t_2 \lt \cdots \lt t_N.
$$

### Missingness constraint

Đối với các feature bắt buộc:

$$
\operatorname{MissingRate}(x^{(j)})
\leq
\tau_j.
$$

### Value-range constraint

$$
x_t^{(j)}
\in
\mathcal{R}_j.
$$

### Duplicate constraint

$$
\operatorname{Unique}(t)=

N.
$$

### Finite-value constraint

$$
x_t^{(j)}
\in
\mathbb{R}
\quad
\forall t,j.
$$

Nếu một điều kiện không được thỏa mãn, dataset không nên được chuyển trực tiếp sang transformation stage.

---

## 10. Leakage control trong data cleaning

Một vấn đề đặc biệt quan trọng khi cleaning được sử dụng cho machine learning là **data leakage**.

Các phép xử lý sử dụng thông tin thống kê của toàn bộ dataset có thể vô tình sử dụng thông tin từ validation hoặc test set.

Ví dụ, nếu median được tính trên toàn bộ dataset:

$$
m
=

\operatorname{median}
(\mathcal{D}_{train}
\cup
\mathcal{D}_{val}
\cup
\mathcal{D}_{test}),
$$

thì thông tin từ validation và test đã ảnh hưởng đến preprocessing.

Đối với các tham số có thể học được, pipeline nên tuân theo:

$$
\theta_{clean}=

\operatorname{Fit}
(\mathcal{D}_{train}),
$$

sau đó:

$$
\mathcal{D}_{train}'=

f_{\theta_{clean}}(\mathcal{D}_{train}),
$$

$$
\mathcal{D}_{val}'=

f_{\theta_{clean}}(\mathcal{D}_{val}),
$$

$$
\mathcal{D}_{test}'=

f_{\theta_{clean}}(\mathcal{D}_{test}).
$$

Đặc biệt, các bước như imputation, outlier threshold estimation hoặc noise-model estimation cần được xem xét dưới góc độ leakage nếu chúng sử dụng thông tin được học từ dữ liệu.

---

## 11. Data cleaning trong bối cảnh Edge/IoT

Trong hệ thống IoT, data cleaning có thể được thực hiện tại sensor, edge node hoặc centralized server.

Pipeline phân tán có thể được biểu diễn:

```text id="q0v1tm"
Sensor
  │
  │ raw measurements
  ▼
Edge Node
  ├── validation
  ├── missing-data detection
  ├── outlier detection
  └── lightweight filtering
  │
  │ cleaned stream
  ▼
Central System
  ├── advanced preprocessing
  ├── feature engineering
  └── AI model
```

Nghiên cứu nền tảng chỉ ra rằng phân phối preprocessing về edge có thể giảm workload cho hệ thống trung tâm, giảm tài nguyên tiêu thụ và hỗ trợ EdgeAI. Đặc biệt, xử lý anomaly hoặc missing data sớm trong pipeline có thể hạn chế error propagation sang các bước sau.

Tuy nhiên, các phương pháp phức tạp như multiple imputation hoặc ensemble-based approaches có thể có chi phí tính toán và bộ nhớ cao, khiến chúng kém phù hợp với edge devices có tài nguyên hạn chế.

Vì vậy, lựa chọn cleaning method trong Edge/IoT cần cân bằng:

$$
\text{Cleaning Quality}
\leftrightarrow
\text{Computational Cost}
\leftrightarrow
\text{Latency}
\leftrightarrow
\text{Resource Constraints}.
$$

---

## 12. Nguyên tắc lựa chọn phương pháp

Không có một cleaning method tối ưu cho mọi time series. Việc lựa chọn nên dựa trên bốn yếu tố:

| Vấn đề         | Câu hỏi chính                   | Ví dụ phương pháp                        |
| -------------- | ------------------------------- | ---------------------------------------- |
| Missing        | Khoảng thiếu dài bao nhiêu?     | interpolation, forward fill, model-based |
| Outlier        | Bất thường toàn cục hay cục bộ? | z-score, IQR, MAD, local methods         |
| Noise          | Noise có đặc tính gì?           | moving average, median, Kalman           |
| Data integrity | Timestamp và records có hợp lệ? | validation, duplicate detection          |

Một nguyên tắc quan trọng là **ưu tiên phương pháp ít can thiệp nhất nhưng đủ để khắc phục vấn đề**. Nếu một anomaly có khả năng là sự kiện thực tế, việc loại bỏ nó có thể gây mất thông tin quan trọng. Ngược lại, nếu một giá trị rõ ràng là lỗi sensor, giữ nguyên nó có thể làm sai lệch cả feature engineering và model training.

---

## 13. Đầu ra của Data Cleaning Pipeline

Kết quả của chương này là một dataset thỏa mãn:

$$
\mathcal{D}_{clean}=

\operatorname{Clean}
(
\mathcal{D}_{raw}
),
$$

với các thuộc tính:

* temporal ordering được bảo toàn;
* duplicate được xử lý;
* missing values được kiểm soát;
* outliers được phát hiện và treatment theo context;
* noise được giảm khi cần thiết;
* các constraint về miền giá trị được kiểm tra;
* quá trình xử lý có thể tái lập.

Dataset này chưa nhất thiết là đầu vào cuối cùng của mô hình AI. Nó mới là **đầu vào hợp lệ cho Data Transformation Pipeline**.

Quan hệ giữa hai giai đoạn được biểu diễn:

$$
\boxed{
\mathcal{D}_{raw}
\xrightarrow{\text{Data Cleaning}}
\mathcal{D}_{clean}
\xrightarrow{\text{Transformation}}
\mathcal{D}_{transformed}
}
$$

Trong đó Data Cleaning tập trung vào **data quality**, còn Data Transformation tập trung vào **representation và model compatibility**. Hai mục tiêu này cần được tách biệt để tránh việc một phép biến đổi làm thay đổi semantics của dữ liệu dưới danh nghĩa cleaning.

### Tài liệu tham khảo chính

Tawakuli, A., Havers, B., Gulisano, V. M., Kaiser, D., & Engel, T. (2025). *Survey: Time-Series Data Preprocessing: A Survey and an Empirical Analysis*. **Journal of Engineering Research, 13**(2), 674–711. DOI: 10.1016/j.jer.2024.02.018. Bài báo trình bày taxonomy các kỹ thuật preprocessing cho numerical time series, đồng thời đánh giá thực nghiệm ảnh hưởng của preprocessing đến data quality và hiệu năng AI.

**Liên kết bài báo:** [ScienceDirect — Survey: Time-Series Data Preprocessing: A Survey and an Empirical Analysis](https://www.sciencedirect.com/science/article/pii/S2307187724000452?utm_source=chatgpt.com)
