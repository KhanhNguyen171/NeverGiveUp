# 12.2 Method Selection

Lựa chọn phương pháp preprocessing là một quyết định phụ thuộc vào **đặc tính của dữ liệu, mục tiêu phân tích, cấu trúc thời gian, mô hình downstream và các ràng buộc tính toán**. Không tồn tại một phương pháp preprocessing tối ưu cho mọi time-series dataset. Vì vậy, thay vì áp dụng một pipeline cố định, cần xây dựng một cơ chế lựa chọn phương pháp dựa trên vấn đề dữ liệu cần giải quyết và tác động dự kiến đối với nhiệm vụ cuối cùng.

Trong nghiên cứu này, method selection được xem là bước kết nối giữa **data characteristics**, **preprocessing techniques** và **AI task**:

$$
\text{Data Characteristics}
\rightarrow
\text{Preprocessing Requirement}
\rightarrow
\text{Method Selection}
\rightarrow
\text{AI Task}.
$$

Mục tiêu không phải là tối đa hóa số lượng preprocessing operations, mà là tìm một tập các transformation cần thiết để cải thiện chất lượng và khả năng sử dụng của dữ liệu trong khi hạn chế information loss, computational cost và leakage.

## 1. Selection Should Start from the Data Problem

Phương pháp preprocessing trước hết phải được lựa chọn dựa trên **vấn đề thực sự tồn tại trong dữ liệu**.

Có thể mô hình hóa mapping cơ bản:

$$
\mathcal{P}_{req}=

f(\mathcal{C}_{data}),
$$

trong đó:

* $\mathcal{C}_{data}$ là tập các đặc tính và vấn đề của dữ liệu;
* $\mathcal{P}_{req}$ là tập các preprocessing operations cần thiết.

Ví dụ:

| Data problem                     | Candidate methods                                             |
| -------------------------------- | ------------------------------------------------------------- |
| Missing observations             | Deletion, interpolation, imputation, model-based imputation   |
| Extreme observations             | Statistical detection, robust detection, contextual detection |
| High-frequency noise             | Smoothing, filtering, decomposition                           |
| Different feature scales         | Standardization, Min-Max scaling, robust scaling              |
| Skewed distribution              | Log, Box-Cox, Yeo-Johnson                                     |
| Non-stationarity                 | Differencing, detrending, decomposition                       |
| Temporal dependency              | Lag features, rolling features                                |
| Periodicity                      | Cyclic encoding, seasonal decomposition                       |
| High dimensionality              | Feature selection, PCA, representation learning               |
| Multiple sensors                 | Data fusion, temporal alignment                               |
| Storage/transmission constraints | Lossless/lossy compression                                    |

Bảng trên cho thấy một preprocessing method chỉ có ý nghĩa khi nó giải quyết một vấn đề cụ thể. Nếu dữ liệu không có missing values, việc áp dụng imputation là không cần thiết. Tương tự, nếu các feature đã có cùng scale và mô hình không yêu cầu normalization, scaling có thể không tạo ra lợi ích đáng kể.

---

## 2. Consider the Statistical Characteristics of the Series

Sau khi xác định vấn đề dữ liệu, cần xem xét đặc tính thống kê của từng biến.

Với một time series:

$$
X_t={x_1,x_2,\ldots,x_T},
$$

các đặc tính cần xem xét bao gồm:

* location;
* scale;
* skewness;
* kurtosis;
* autocorrelation;
* seasonality;
* trend;
* stationarity;
* missingness;
* outlier behavior;
* noise level.

Ví dụ, nếu feature có phân phối lệch phải mạnh:

$$
\operatorname{Skew}(X)\gg 0,
$$

một transformation như logarithm có thể được cân nhắc:

$$
x_t'=\log(x_t),
\qquad x_t \gt 0.
$$

Ngược lại, nếu feature chứa giá trị không dương, logarithmic transformation trực tiếp không phù hợp. Khi đó có thể xem xét một transformation khác như Yeo-Johnson.

Vì vậy, **method selection phải dựa trên statistical evidence thay vì chỉ dựa trên convention**.

---

## 3. Match the Method to the Type of Variable

Các feature khác nhau có semantic và statistical properties khác nhau. Vì vậy, không nên áp dụng cùng một preprocessing operation cho toàn bộ feature matrix.

Giả sử:

$$
\mathbf{x}_t=

[
\mathbf{x}_t^{(c)},
\mathbf{x}_t^{(b)},
\mathbf{x}_t^{(cyc)},
\mathbf{x}_t^{(cat)}
],
$$

trong đó:

* $\mathbf{x}^{(c)}$: continuous features;
* $\mathbf{x}^{(b)}$: binary features;
* $\mathbf{x}^{(cyc)}$: cyclical features;
* $\mathbf{x}^{(cat)}$: categorical features.

Mỗi nhóm có thể yêu cầu strategy khác nhau.

Ví dụ, Standardization:

$$
z_t=

\frac{x_t-\mu}{\sigma}
$$

phù hợp với continuous variables trong nhiều mô hình, nhưng không nên áp dụng một cách máy móc cho binary variables hoặc các representation đã được chuẩn hóa theo semantic.

Đặc biệt, với cyclical representation:

$$
x_{\sin}=\sin(2\pi t/P),
\qquad
x_{\cos}=\cos(2\pi t/P),
$$

giá trị đã nằm trong khoảng $[-1,1]$. Việc tiếp tục standardize chúng có thể không cần thiết và làm giảm tính nhất quán của representation.

Do đó, **semantic type là một tiêu chí trực tiếp trong method selection**.

---

## 4. Match the Method to the Missing-Data Mechanism

Không thể lựa chọn missing-data method chỉ dựa trên tỷ lệ missing values.

Giả sử:

$$
M_t=
\begin{cases}
1,&x_t\text{ is missing},\\
0,&x_t\text{ is observed}.
\end{cases}
$$

Cần xem xét cả:

* missing rate;
* missing duration;
* missingness pattern;
* temporal continuity;
* relationship giữa missingness và observed variables.

Một gap ngắn và liên tục có thể phù hợp với interpolation:

$$
\hat{x}_t=

x_{t_1}
+
\frac{t-t_1}{t_2-t_1}
(x_{t_2}-x_{t_1}),
$$

trong khi một gap dài có thể khiến interpolation tạo ra dữ liệu giả không phản ánh dynamics thực tế.

Với time series, do đó cần phân biệt:

$$
\text{short gap}
\neq
\text{long gap}
\neq
\text{systematic missingness}.
$$

Method selection phải dựa trên **cơ chế và cấu trúc temporal của missingness**, không chỉ dựa trên missing percentage.

---

## 5. Select Outlier Methods According to Context

Một quan sát:

$$
x_t\in\mathcal{D}
$$

không nên được xem là outlier chỉ vì nó có giá trị lớn hoặc nhỏ.

Có thể phân biệt:

1. **Global outlier** — bất thường so với toàn bộ distribution.
2. **Contextual outlier** — bất thường trong một temporal context cụ thể.
3. **Collective outlier** — một chuỗi các observations cùng tạo thành pattern bất thường.

Ví dụ, một mức tiêu thụ năng lượng cao có thể là global outlier nhưng hoàn toàn hợp lý vào một thời điểm nhất định trong ngày.

Do đó, lựa chọn giữa:

* IQR;
* Z-score;
* robust statistics;
* isolation-based methods;
* local methods;
* contextual detection;

phải phụ thuộc vào bản chất của dữ liệu và định nghĩa "abnormal" của bài toán.

Nguyên tắc quan trọng là:

$$
\boxed{
\text{Detect first, decide later}
}
$$

Phát hiện outlier không đồng nghĩa với việc tự động loại bỏ nó.

---

## 6. Select Transformation According to Distribution

Transformation nên được sử dụng khi distribution gây ra vấn đề đối với downstream task hoặc model.

Một số lựa chọn phổ biến gồm:

### Log transformation

$$
x_t'=\log(x_t).
$$

Phù hợp chủ yếu với positive-valued variables có right-skewness.

### Box-Cox transformation

$$
x_t^{(\lambda)}=

\begin{cases}
\dfrac{x_t^\lambda-1}{\lambda},
&\lambda\neq0, \\[6pt]
\log(x_t),
&\lambda=0.
\end{cases}
$$

Box-Cox yêu cầu dữ liệu dương.

### Yeo-Johnson transformation

Yeo-Johnson mở rộng khả năng transformation cho dữ liệu có cả giá trị dương và âm.

Method selection do đó phải xét:

$$
\text{Domain}
+
\text{Distribution}
+
\text{Model Assumption}.
$$

Không nên transformation chỉ nhằm làm distribution "đẹp hơn" nếu transformation đó không mang lại lợi ích thực tế cho task.

---

## 7. Select Scaling According to Model Requirements

Scaling được lựa chọn dựa trên scale heterogeneity và sensitivity của model đối với feature magnitude.

### Standardization

$$
z
=

\frac{x-\mu_{train}}{\sigma_{train}}.
$$

### Min-Max scaling

$$
z
=

\frac{x-x_{\min}}
{x_{\max}-x_{\min}}.
$$

### Robust scaling

$$
z
=

\frac{x-\operatorname{median}(x)}
{\operatorname{IQR}(x)}.
$$

Có thể xem decision rule đơn giản:

$$
\text{Scaling requirement}=

f(\text{feature scales},\text{model sensitivity},\text{outlier behavior}).
$$

Các model dựa trên distance, gradient optimization hoặc dot-product magnitude thường nhạy với scale hơn một số tree-based models.

Tuy nhiên, dù model có yêu cầu scaling hay không, learned scaling parameters vẫn phải được fit trên training data:

$$
(\mu,\sigma)=

f(\mathcal{D}_{train}).
$$

---

## 8. Select Stationarity Methods Based on the Modeling Objective

Stationarity không phải lúc nào cũng là mục tiêu bắt buộc.

Một số statistical forecasting models có assumptions liên quan đến stationarity, trong khi nhiều modern machine-learning và deep-learning models có thể học trực tiếp từ non-stationary series.

Do đó:

$$
\text{Need for stationarity}=

f(\text{model},\text{task},\text{data dynamics}).
$$

Nếu differencing được sử dụng:

$$
\nabla x_t=

x_t-x_{t-1},
$$

thì cần đánh giá trade-off giữa:

* giảm trend;
* tăng stationarity;
* mất thông tin về absolute level;
* khả năng inverse transformation.

Không nên differencing chỉ vì một series không stationary nếu downstream model không yêu cầu assumption này.

---

## 9. Select Feature Engineering According to Temporal Dependencies

Lag và rolling features nên được lựa chọn dựa trên temporal dependency.

Với lag order $k$:

$$
x_{t-k},
$$

giá trị $k$ nên phản ánh temporal structure hoặc domain knowledge.

Nếu autocorrelation function được định nghĩa:

$$
\rho(k)=

\operatorname{Corr}(X_t,X_{t-k}),
$$

thì các lag có mức autocorrelation đáng kể có thể cung cấp candidate features.

Tương tự, rolling mean:

$$
\mu_t^{(w)}=

\frac{1}{w}
\sum_{i=0}^{w-1}x_{t-i}
$$

có thể biểu diễn local level hoặc short-term trend.

Tuy nhiên, việc tạo quá nhiều lag hoặc rolling windows sẽ làm tăng dimensionality:

$$
F'
\gg F,
$$

từ đó làm tăng memory usage, training cost và nguy cơ redundancy.

Do đó:

$$
\boxed{
\text{Feature engineering} \neq \text{feature expansion without control}
}
$$

---

## 10. Select Fusion and Alignment Methods According to Sensor Structure

Trong multivariate sensor systems, method selection phải xem xét cả **spatial consistency** và **temporal consistency**.

Với $M$ sensors:

$$
\mathcal{D}^{(m)}=

\left \{
(t_i^{(m)},\mathbf{x}_i^{(m)})
\right \}_{i=1}^{N_m},
\qquad
m=1,\ldots,M.
$$

Các sensors có thể có:

* sampling frequencies khác nhau;
* timestamp offsets;
* missing intervals;
* communication delays;
* different measurement units.

Do đó, trước khi fusion cần xác định temporal alignment strategy.

Một lựa chọn phổ biến là đưa các observations về common timeline:

$$
\mathcal{T}=

{t_1,t_2,\ldots,t_K}.
$$

Sau đó:

$$
\mathbf{x}_{t}=

\operatorname{Align}
\left(
\mathbf{x}^{(1)},
\ldots,
\mathbf{x}^{(M)}
\right).
$$

Method selection phải cân bằng giữa temporal accuracy, information preservation và computational cost.

---

## 11. Consider the Downstream Model

Cùng một dataset có thể cần các preprocessing strategies khác nhau tùy thuộc vào model.

Có thể biểu diễn:

$$
P^*=

\arg\max_{P\in\mathcal{P}}
\operatorname{Performance}
\left(
M,T_P(\mathcal{D})
\right),
$$

trong đó $M$ là downstream model và $T_P$ là transformation pipeline.

Ví dụ:

* linear models có thể hưởng lợi từ scaling và transformation;
* distance-based models thường nhạy với scale;
* tree-based models thường ít phụ thuộc vào monotonic scaling;
* recurrent models có thể hưởng lợi từ normalized inputs;
* transformer-based models thường yêu cầu representation có scale ổn định để optimization hiệu quả.

Do đó, method selection phải được thực hiện trong **context của downstream model**, thay vì đánh giá preprocessing độc lập hoàn toàn với model.

---

## 12. Consider Computational and Deployment Constraints

Một phương pháp có predictive benefit cao nhưng computational cost quá lớn có thể không phù hợp với production hoặc edge deployment.

Có thể biểu diễn tổng chi phí:

$$
C_{total}=

C_{preprocess}
+
C_{storage}
+
C_{transfer}
+
C_{inference}.
$$

Đối với cloud-based systems, một số transformation phức tạp có thể chấp nhận được. Ngược lại, với edge/IoT:

$$
C_{CPU},C_{memory},C_{energy}
$$

có thể trở thành các constraints chính.

Vì vậy, method selection cần xem xét:

$$
\boxed{
\text{Accuracy}
\leftrightarrow
\text{Complexity}
\leftrightarrow
\text{Latency}
\leftrightarrow
\text{Energy}
}
$$

Đây cũng là lý do các phương pháp compression và edge preprocessing được xem xét như một phần của taxonomy trong nghiên cứu này.

---

## 13. Use a Decision Hierarchy

Một quy trình lựa chọn phương pháp có thể được tổ chức theo hierarchy:

$$
\boxed{
\begin{array}{c}
\text{Is there a data problem?}\\
\downarrow\\
\text{What is the problem type?}\\
\downarrow\\
\text{What is the temporal structure?}\\
\downarrow\\
\text{What is the downstream task/model?}\\
\downarrow\\
\text{What constraints exist?}\\
\downarrow\\
\text{Which method is appropriate?}\\
\downarrow\\
\text{Does empirical evaluation justify it?}
\end{array}
}
$$

Cách tiếp cận này tránh việc lựa chọn phương pháp theo thứ tự tùy tiện.

Ví dụ, đối với một continuous feature trong energy time series:

$$
\text{Distribution}
\rightarrow
\text{Outlier behavior}
\rightarrow
\text{Scale}
\rightarrow
\text{Model sensitivity}
\rightarrow
\text{Transformation/Scaling}.
$$

Trong khi với missing values:

$$
\text{Missing pattern}
\rightarrow
\text{Gap length}
\rightarrow
\text{Temporal dependency}
\rightarrow
\text{Imputation strategy}.
$$

---

## 14. Empirical Validation Is the Final Selection Criterion

Phân tích thống kê có thể xác định candidate methods nhưng không thể đảm bảo rằng một method sẽ cải thiện downstream task.

Do đó, sau khi lựa chọn candidate preprocessing methods, cần thực hiện empirical comparison:

$$
P_1,P_2,\ldots,P_K
\rightarrow
\left \{
\mathcal{M}_1,\mathcal{M}_2,\ldots,\mathcal{M}_K
\right \}.
$$

Các pipelines nên được đánh giá dưới cùng điều kiện:

* cùng dataset;
* cùng temporal split;
* cùng model;
* cùng training protocol;
* cùng evaluation metrics;
* cùng test protocol.

Nếu:

$$
E(P_i) \lt E(P_j),
$$

với $E$ là evaluation error, thì $P_i$ có lợi thế trong experimental setting đó. Tuy nhiên, sự khác biệt cần được xem xét cùng computational cost và stability thay vì chỉ dựa vào một metric.

Điều này tạo cơ sở cho **Chapter 09 — Empirical Analysis**, nơi các preprocessing strategies được so sánh thực nghiệm.

---

## 15. Recommended Selection Framework

Từ các nguyên tắc trên, method selection trong nghiên cứu này được tổ chức thành năm bước:

### Step 1 — Characterize the data

Xác định:

$$
\mathcal{C}=

{
\text{missing},
\text{outlier},
\text{noise},
\text{scale},
\text{distribution},
\text{stationarity},
\text{temporal dependency}
}.
$$

### Step 2 — Define the objective

Xác định preprocessing nhằm:

* cleaning;
* stabilization;
* temporal representation;
* dimensionality reduction;
* sensor integration;
* compression;
* hoặc model compatibility.

### Step 3 — Generate candidate methods

Từ taxonomy, lựa chọn các methods có khả năng giải quyết vấn đề:

$$
\mathcal{P}_{candidate}
\subseteq
\mathcal{P}_{all}.
$$

### Step 4 — Filter by constraints

Loại bỏ các methods không đáp ứng:

* temporal integrity;
* leakage constraints;
* semantic constraints;
* computational constraints;
* deployment requirements.

Kết quả:

$$
\mathcal{P}_{valid}
\subseteq
\mathcal{P}_{candidate}.
$$

### Step 5 — Empirically validate

So sánh các candidates trên downstream task:

$$
P^*=

\arg\min_{P\in\mathcal{P}_{valid}}
E(P),
$$

subject to:

$$
\operatorname{Leakage}(P)=0,
$$

và:

$$
C(P)\leq C_{max},
$$

nếu tồn tại computational constraint.

---

## 16. Summary

Method selection trong time-series preprocessing nên được xem là **một quá trình có điều kiện**, không phải một danh sách các kỹ thuật được áp dụng tuần tự cho mọi dataset.

Nguyên tắc cốt lõi là:

$$
\boxed{
\text{Problem}
\rightarrow
\text{Data Characteristics}
\rightarrow
\text{Candidate Methods}
\rightarrow
\text{Constraints}
\rightarrow
\text{Empirical Validation}
}
$$

Một phương pháp chỉ nên được lựa chọn khi nó đồng thời:

1. giải quyết một vấn đề dữ liệu cụ thể;
2. phù hợp với statistical và temporal characteristics;
3. bảo toàn information quan trọng;
4. không tạo information leakage;
5. phù hợp với downstream task và model;
6. đáp ứng computational constraints;
7. có thể tái lập;
8. và được xác nhận bằng empirical evaluation.

Do đó, **method selection không phải là bước chọn preprocessing mạnh nhất, mà là bước chọn preprocessing phù hợp nhất với dữ liệu, mục tiêu và ràng buộc của bài toán**.

Nguyên tắc này tạo nền tảng trực tiếp cho **[12.3 Common Mistakes](03_common_mistakes.md)**, trong đó các lựa chọn preprocessing sai, leakage, over-processing và loss of temporal information sẽ được phân tích như những failure modes phổ biến.

### Reference

[1] A. Tawakuli, B. Havers, V. M. Gulisano, D. Kaiser, and T. Engel, “Time-series data preprocessing: A survey and an empirical analysis,” *Journal of Engineering Research*, vol. 13, no. 2, pp. 674–711, 2025. DOI: 10.1016/j.jer.2024.02.018.
