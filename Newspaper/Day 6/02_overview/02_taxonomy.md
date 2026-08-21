# 2.2 Taxonomy of Time-Series Data Preprocessing

Taxonomy của nghiên cứu được xây dựng nhằm tổ chức các phương pháp preprocessing theo **mục tiêu xử lý và vai trò của chúng trong toàn bộ data preparation pipeline**. Thay vì phân loại theo từng thuật toán riêng lẻ, nghiên cứu sử dụng một taxonomy nhiều tầng, trong đó mỗi nhóm phương pháp giải quyết một loại vấn đề khác nhau của numerical time-series data.

Cách phân loại này tạo cầu nối giữa **Chapter 2 – Overview** và các chương phương pháp từ **Chapter 3 đến Chapter 8**, đồng thời cung cấp cơ sở để so sánh các kỹ thuật trong **Chapter 9 – Empirical Analysis** và **Chapter 10 – Discussion**.

---

## 2.2.1 Nguyên tắc xây dựng taxonomy

Một phương pháp preprocessing có thể được phân loại dựa trên ba câu hỏi chính:

1. **Vấn đề nào của dữ liệu cần được giải quyết?**
2. **Phép biến đổi tác động lên dữ liệu ở mức nào?**
3. **Mục tiêu cuối cùng của phép xử lý là gì?**

Từ đó, preprocessing được xem như một hàm biến đổi tổng quát:

$$
\mathcal{P}:
\mathcal{X}*{raw}
\rightarrow
\mathcal{X}*{AI},
$$

trong đó $\mathcal{X}*{raw}$ là dữ liệu chuỗi thời gian ban đầu và $\mathcal{X}*{AI}$ là representation cuối cùng được sử dụng bởi downstream task.

Taxonomy của nghiên cứu được tổ chức thành sáu nhóm chính:

$$
\boxed{
\mathcal{T}_{prep}=

{
\mathcal{C},
\mathcal{T},
\mathcal{F},
\mathcal{S},
\mathcal{U},
\mathcal{K}}}$$

với:

* $\mathcal{C}$: **Data Cleaning**;
* $\mathcal{T}$: **Data Transformation**;
* $\mathcal{F}$: **Feature Engineering**;
* $\mathcal{S}$: **Feature Selection & Dimensionality Reduction**;
* $\mathcal{U}$: **Sensor Fusion**;
* $\mathcal{K}$: **Data Compression**.

Sáu nhóm này tương ứng với các chương phương pháp của nghiên cứu.

---

## 2.2.2 Taxonomy tổng thể

Taxonomy có thể biểu diễn theo pipeline:

```text
                         Time-Series Preprocessing
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
     Data Quality            Representation          Data Efficiency
          │                       │                       │
          ▼                       ▼                       ▼
   Data Cleaning          Transformation          Data Compression
          │                       │
          │              ┌────────┴────────┐
          │              │                 │
          ▼              ▼                 ▼
     Missing Data   Feature Engineering   Feature Selection
     Outliers             │              & Dimensionality
     Noise                │                 Reduction
                          │
                          ▼
                    Sensor Fusion
```

Tuy nhiên, các nhóm trên **không hoàn toàn độc lập**. Một preprocessing pipeline thực tế có thể sử dụng nhiều nhóm đồng thời. Chẳng hạn, một hệ thống sensor có thể thực hiện:

$$
\text{Missing-value Handling}
\rightarrow
\text{Temporal Alignment}
\rightarrow
\text{Scaling}
\rightarrow
\text{Feature Engineering}
\rightarrow
\text{Feature Selection}
\rightarrow
\text{Compression}.
$$

Do đó, taxonomy nên được hiểu là một **phân loại theo chức năng**, không phải một cây phân cấp trong đó mỗi dữ liệu chỉ thuộc duy nhất một nhóm.

---

## 2.2.3 Nhóm I — Data Cleaning

**Data Cleaning** giải quyết các vấn đề liên quan trực tiếp đến chất lượng và tính hợp lệ của observations.

Nhóm này được ký hiệu:

$$\mathcal{C}={C_{missing}, C_{outlier}, C_{noise}}.$$

### Missing data

Missing data xuất hiện khi một hoặc nhiều giá trị tại thời điểm $t$ không được quan sát:

$$
x_{t,f} = \varnothing.
$$

Các chiến lược xử lý bao gồm:

* deletion;
* forward/backward filling;
* interpolation;
* statistical imputation;
* model-based imputation.

Đối với time series, việc xử lý missing data phải xét đến temporal dependency. Một giá trị bị thiếu trong một khoảng thời gian ngắn có bản chất khác với một đoạn dữ liệu bị mất liên tục trong thời gian dài.

### Outlier detection

Outlier là observation có hành vi khác biệt đáng kể so với phân phối hoặc pattern thông thường:

$$
x_t \notin \mathcal{R}_{normal}.
$$

Các phương pháp có thể dựa trên:

* statistical rules;
* distance;
* density;
* isolation;
* temporal context.

Đặc biệt, một giá trị cực đoan trong time series không nhất thiết là lỗi. Nó có thể đại diện cho một event thực tế. Vì vậy, detection và removal phải được phân biệt.

### Noise reduction

Noise là thành phần không mong muốn làm giảm signal-to-noise ratio của chuỗi:

$$
x_t = s_t + \epsilon_t,
$$

trong đó $s_t$ là underlying signal và $\epsilon_t$ là noise.

Các kỹ thuật có thể bao gồm:

* smoothing;
* moving average;
* median filtering;
* signal decomposition;
* frequency-domain filtering.

Chi tiết của nhóm này được trình bày trong **Chapter 3 – Data Cleaning**.

---

## 2.2.4 Nhóm II — Data Transformation

**Data Transformation** biến đổi representation của dữ liệu mà không nhất thiết thay đổi ý nghĩa của observation.

Nhóm này được ký hiệu:

$$
\mathcal{T}=

{
T_{scale},
T_{transform},
T_{stationary},
T_{decompose}
}.
$$

### Scaling và normalization

Scaling đưa các feature về một scale phù hợp:

$$
x' = \frac{x-\mu}{\sigma}.
$$

Normalization có thể đưa dữ liệu về một miền xác định, chẳng hạn:

$$
x' =
\frac{x-x_{min}}
{x_{max}-x_{min}}.
$$

Mục tiêu chính là tránh việc các feature có scale lớn chi phối quá trình tối ưu hoặc khoảng cách.

### Transformation

Transformation thay đổi phân phối hoặc representation của biến:

$$
x' = g(x).
$$

Các phép biến đổi phổ biến gồm:

* logarithmic transformation;
* power transformation;
* Box--Cox transformation;
* Yeo--Johnson transformation.

### Stationarity

Một time series được xem là stationary nếu các đặc tính thống kê cơ bản không thay đổi theo thời gian.

Với weak stationarity:

$$
E[X_t] = \mu,
$$

và

$$
Cov(X_t,X_{t-k}) = \gamma(k),
$$

không phụ thuộc trực tiếp vào $t$.

Các kỹ thuật như differencing hoặc transformation có thể được sử dụng để giảm trend hoặc thay đổi variance.

### Decomposition

Decomposition biểu diễn time series thành các thành phần có ý nghĩa:

$$
X_t = T_t + S_t + R_t,
$$

trong additive decomposition, với:

* $T_t$: trend;
* $S_t$: seasonal component;
* $R_t$: residual.

Nhóm này được trình bày trong **Chapter 4 – Data Transformation**.

---

## 2.2.5 Nhóm III — Feature Engineering

**Feature Engineering** khai thác cấu trúc temporal để xây dựng các biến mới có khả năng biểu diễn thông tin liên quan đến target.

Nhóm này được ký hiệu:

$$
\mathcal{F}=

{
F_{temporal},
F_{lag},
F_{rolling},
F_{representation}
}.
$$

### Temporal features

Temporal features biểu diễn vị trí của observation trong calendar hoặc periodic cycle.

Ví dụ với hour-of-day $h$:

$$
hour_{sin}=

\sin
\left(
\frac{2\pi h}{24}
\right),
$$

$$
hour_{cos}=

\cos
\left(
\frac{2\pi h}{24}
\right).
$$

Cách biểu diễn này tránh discontinuity giữa các giá trị tuần hoàn, chẳng hạn giữa $23:00$ và $00:00$.

### Lag features

Lag feature biểu diễn giá trị của biến tại các thời điểm trước đó:

$$
X_{t-k}.
$$

Một vector lag có thể được biểu diễn:

$$
\mathbf{L}_t=

[
X_{t-1},
X_{t-2},
\dots,
X_{t-p}
].
$$

Lag features là thành phần quan trọng để biểu diễn temporal dependency trong các mô hình không trực tiếp nhận sequence.

### Rolling features

Rolling features tổng hợp thông tin từ một temporal window:

$$
R_t^{(w)}=

f(X_{t-w+1},\ldots,X_t).
$$

Ví dụ rolling mean:

$$
\mu_t^{(w)}=

\frac{1}{w}
\sum_{i=0}^{w-1}X_{t-i}.
$$

Các statistic khác có thể bao gồm:

* rolling standard deviation;
* rolling minimum;
* rolling maximum;
* rolling median.

### Feature representation

Sau khi tạo feature, dữ liệu cần được tổ chức thành representation phù hợp với downstream model.

Có thể biểu diễn:

$$
\mathbf{X}
\in
\mathbb{R}^{T\times F}
$$

hoặc với sequence modeling:

$$
\mathbf{X}
\in
\mathbb{R}^{N\times L\times F},
$$

trong đó:

* $N$: số lượng samples;
* $L$: sequence length;
* $F$: số lượng features.

Nhóm này được trình bày trong **Chapter 5 – Feature Engineering**.

---

## 2.2.6 Nhóm IV — Feature Selection và Dimensionality Reduction

Khi số lượng feature tăng, dữ liệu có thể chứa redundancy, irrelevant features hoặc highly correlated variables.

Nhóm này được ký hiệu:

$$
\mathcal{S}=

{
S_{filter},
S_{wrapper},
S_{embedded},
S_{reduction}
}.
$$

### Filter methods

Filter methods đánh giá feature dựa trên một criterion độc lập với downstream model.

Ví dụ:

$$
Score(X_j,Y)
$$

có thể dựa trên:

* correlation;
* mutual information;
* statistical tests;
* variance.

### Wrapper methods

Wrapper methods đánh giá một tập feature thông qua hiệu năng của model:

$$
S^*=

\arg\max_{S\subseteq\mathcal{F}}
Performance(M,S).
$$

Do phải huấn luyện hoặc đánh giá model nhiều lần, wrapper methods thường có computational cost cao hơn filter methods.

### Embedded methods

Embedded methods thực hiện feature selection trong quá trình training model.

Một ví dụ điển hình là regularization:

$$
\min_{\beta}
\left[
L(\beta)
+
\lambda|\beta|_1
\right],
$$

trong đó $L(\beta)$ là loss function và $\lambda$ kiểm soát mức độ sparsity.

### Dimensionality reduction

Dimensionality reduction tạo ra representation mới có số chiều thấp hơn:

$$
\mathbf{X}
\in
\mathbb{R}^{F}
\rightarrow
\mathbf{Z}
\in
\mathbb{R}^{d},
\qquad d<F.
$$

Khác với feature selection, dimensionality reduction thường tạo ra các feature mới thay vì giữ nguyên một subset của feature ban đầu.

Nhóm này được trình bày trong **Chapter 6 – Feature Selection**.

---

## 2.2.7 Nhóm V — Sensor Fusion

**Sensor Fusion** xử lý dữ liệu đến từ nhiều sensor hoặc nhiều data sources.

Giả sử có $M$ sensor:

$$
\mathcal{X}=

{
X^{(1)},X^{(2)},\ldots,X^{(M)}
}.
$$

Mục tiêu của fusion là xây dựng một representation chung:

$$
X^{fusion}=

\mathcal{F}
\left(
X^{(1)},\ldots,X^{(M)}
\right).
$$

Taxonomy của sensor fusion được phân thành ba mức:

1. **Data-level fusion** — kết hợp dữ liệu gần với raw observations.
2. **Feature-level fusion** — trích xuất feature từ từng nguồn rồi kết hợp.
3. **Decision-level fusion** — kết hợp các output hoặc decisions của các mô hình.

Đối với time series, fusion còn yêu cầu giải quyết **temporal alignment**. Nếu hai sensor có sampling frequency khác nhau hoặc timestamp không đồng nhất, việc kết hợp trực tiếp có thể tạo ra representation sai lệch.

Nhóm này được trình bày trong **Chapter 7 – Sensor Fusion**.

---

## 2.2.8 Nhóm VI — Data Compression

**Data Compression** nhằm giảm lượng dữ liệu cần lưu trữ hoặc truyền tải trong khi duy trì mức thông tin cần thiết cho downstream task.

Có thể biểu diễn quá trình compression:

$$
X
\xrightarrow{\mathcal{K}}
Z,
\qquad
|Z| \lt |X|.
$$

Hai nhóm chính được xem xét.

### Lossless compression

Lossless compression bảo toàn hoàn toàn thông tin:

$$
D(C(X)) = X,
$$

trong đó $C$ là compression và $D$ là decompression.

Nhóm này phù hợp khi dữ liệu không được phép mất thông tin.

### Lossy compression

Lossy compression cho phép một mức sai khác:

$$
D(C(X)) \approx X.
$$

Mục tiêu là đạt được trade-off giữa compression ratio và information loss:

$$
\text{Compression Efficiency}
\leftrightarrow
\text{Information Preservation}.
$$

### Edge/IoT

Trong Edge/IoT, compression có ý nghĩa đặc biệt vì sensor thường có:

* limited storage;
* limited bandwidth;
* limited computational resources;
* yêu cầu truyền dữ liệu liên tục.

Do đó, compression có thể được thực hiện trước khi dữ liệu được truyền đến central server hoặc cloud.

Nhóm này được trình bày trong **Chapter 8 – Data Compression**.

---

## 2.2.9 Quan hệ giữa các nhóm taxonomy

Các nhóm preprocessing không nên được hiểu là những bước bắt buộc phải thực hiện theo một thứ tự cố định.

Một pipeline có thể được biểu diễn tổng quát:

$$
X_{raw}
\xrightarrow{\mathcal{C}}
X_{clean}
\xrightarrow{\mathcal{T}}
X_{transformed}
\xrightarrow{\mathcal{F}}
X_{feature}
\xrightarrow{\mathcal{S}}
X_{selected}
\xrightarrow{\mathcal{U}}
X_{fused}
\xrightarrow{\mathcal{K}}
X_{AI}.
$$

Tuy nhiên, trong thực tế thứ tự có thể thay đổi theo:

* đặc điểm dữ liệu;
* loại sensor;
* downstream task;
* model architecture;
* computational constraints.

Ví dụ, temporal alignment thường phải xảy ra trước feature engineering nếu feature được xây dựng từ nhiều sensor. Ngược lại, compression có thể được thực hiện ở nhiều vị trí khác nhau tùy kiến trúc hệ thống.

Vì vậy, taxonomy được sử dụng trong nghiên cứu như **functional taxonomy**, không phải **strict sequential taxonomy**.

---

## 2.2.10 Mapping taxonomy với cấu trúc nghiên cứu

Taxonomy được ánh xạ trực tiếp vào các chương phương pháp như sau:

| Taxonomy            | Mục tiêu                       | Nội dung                                             |
| ------------------- | ------------------------------ | ---------------------------------------------------- |
| Data Cleaning       | Cải thiện chất lượng dữ liệu   | Missing data, outliers, noise                        |
| Data Transformation | Thay đổi representation        | Scaling, transformation, stationarity, decomposition |
| Feature Engineering | Khai thác temporal information | Temporal, lag, rolling, representation               |
| Feature Selection   | Giảm redundancy                | Filter, wrapper, embedded, dimensionality reduction  |
| Sensor Fusion       | Kết hợp nhiều nguồn            | Fusion levels, temporal alignment                    |
| Data Compression    | Giảm data volume               | Lossless, lossy, Edge/IoT                            |

Mapping này tạo ra cấu trúc:

$$
\text{Chapter 2}
\rightarrow
\text{Taxonomy}
\rightarrow
\text{Chapters 3--8}
\rightarrow
\text{Empirical Analysis}
\rightarrow
\text{Discussion}.
$$

Do đó, **Chapter 2 không lặp lại nội dung của các chương phương pháp**. Vai trò của taxonomy là xác định *phương pháp nào thuộc nhóm nào, giải quyết vấn đề gì và nằm ở đâu trong preprocessing pipeline*. Các thuật toán cụ thể, công thức chi tiết và ưu nhược điểm sẽ được phân tích trong từng chương tương ứng.

---

## 2.2.11 Taxonomy làm cơ sở cho empirical analysis

Taxonomy cũng được sử dụng làm framework cho việc thiết kế thực nghiệm ở **Chapter 9**.

Thay vì so sánh toàn bộ preprocessing methods trong một experiment duy nhất, nghiên cứu đánh giá chúng theo các nhóm chức năng:

$$
\text{Method}
\rightarrow
\text{Preprocessing Objective}
\rightarrow
\text{Data Representation}
\rightarrow
\text{Downstream Performance}.
$$

Điều này cho phép phân biệt hai câu hỏi:

1. **Phương pháp có cải thiện đặc tính của dữ liệu hay không?**
2. **Cải thiện đó có chuyển thành lợi ích cho downstream AI model hay không?**

Sự phân biệt này quan trọng vì một preprocessing method có thể cải thiện một statistical property của dữ liệu nhưng không nhất thiết cải thiện prediction performance.

Do đó, taxonomy không chỉ có vai trò tổ chức literature review mà còn là **khung phân tích để đánh giá trade-off giữa data quality, information preservation, computational cost và model performance**.

---

## 2.2.12 Tóm tắt taxonomy

Toàn bộ phạm vi preprocessing của nghiên cứu có thể cô đọng thành sáu câu hỏi:

$$
\boxed{
\begin{aligned}
&\text{Cleaning:} &&
\text{Dữ liệu có vấn đề gì?}\
&\text{Transformation:} &&
\text{Dữ liệu nên được biểu diễn như thế nào?}\
&\text{Feature Engineering:} &&
\text{Có thể khai thác thêm thông tin temporal nào?}\
&\text{Feature Selection:} &&
\text{Feature nào thực sự cần thiết?}\
&\text{Sensor Fusion:} &&
\text{Làm thế nào kết hợp nhiều nguồn dữ liệu?}\
&\text{Compression:} &&
\text{Làm thế nào giảm data volume mà vẫn giữ thông tin cần thiết?}
\end{aligned}
}
$$

Sáu nhóm này tạo thành taxonomy trung tâm của nghiên cứu. **Chapter 3–8** lần lượt đi sâu vào từng nhóm; **Chapter 9** đánh giá hiệu quả thực nghiệm; **Chapter 10** phân tích comparison, trade-offs và limitations; và **Chapter 11** tổng hợp các nhóm phương pháp thành một preprocessing pipeline hướng tới **AI-ready time-series data**.
