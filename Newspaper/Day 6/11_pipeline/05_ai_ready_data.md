# 11.5 AI-Ready Data

## 1. Mục tiêu

AI-ready data là trạng thái cuối của preprocessing pipeline, trong đó dữ liệu đã được **kiểm tra, làm sạch, biến đổi, xây dựng đặc trưng và tổ chức theo đúng yêu cầu của mô hình downstream**.

Đối với time-series data, AI-ready không đơn thuần có nghĩa là dữ liệu không còn missing values. Một dataset chỉ thực sự sẵn sàng cho AI khi đồng thời bảo đảm:

* temporal structure được bảo toàn;
* dữ liệu có schema nhất quán;
* missing values và invalid observations được xử lý;
* numerical representation phù hợp với model;
* features được căn chỉnh chính xác theo thời gian;
* không có temporal hoặc statistical leakage;
* input và target có định nghĩa rõ ràng;
* dữ liệu có thể được tái lập và kiểm chứng.

Pipeline tổng quát:

$$
\mathcal{D}_{raw}
\xrightarrow{\text{Cleaning}}
\mathcal{D}_{clean}
\xrightarrow{\text{Transformation}}
\mathcal{D}_{transformed}
\xrightarrow{\text{Feature Engineering}}
\mathcal{D}_{feature}
\xrightarrow{\text{Validation}}
\mathcal{D}_{AI-ready}.
$$

Do đó, AI-ready data là **output contract của toàn bộ preprocessing pipeline**, chứ không phải một preprocessing technique riêng lẻ.

---

# 2. Định nghĩa AI-Ready Data

Cho dataset chuỗi thời gian:

$$
\mathcal{D}=

\left \{
(t_i,\mathbf{x}_i,y_i)
\right \}_{i=1}^{N},
$$

một dataset được xem là AI-ready nếu tồn tại một representation:

$$
\mathcal{D}_{AI}=

\left \{
(\mathbf{X}_i,y_i)
\right \}_{i=1}^{N'},
$$

trong đó $\mathbf{X}_i$ là input representation hợp lệ và $y_i$ là target tương ứng.

Đối với sequence forecasting:

$$
\mathbf{X}_t=

\left[
\mathbf{z}_{t-L+1},
\ldots,
\mathbf{z}_t
\right ],
$$

và:

$$
y_t^{target}=y_{t+H}.
$$

Khi đó:

$$
\mathcal{D}_{AI}=

\left \{
\left(
\mathbf{X}_t,
y_{t+H}
\right)
\right \}.
$$

Điều kiện quan trọng nhất là:

$$
\boxed{
\mathbf{X}_t
\text{ chỉ sử dụng thông tin có sẵn tại thời điểm }t
}
$$

trong khi target có thể nằm tại tương lai:

$$
y_{t+H}.
$$

---

# 3. AI-Ready Data Contract

Một AI-ready dataset nên được mô tả bởi một data contract:

$$
\mathcal{C}=

(
Schema,
Temporal,
Features,
Target,
Split,
Transformations,
Validation
).
$$

Trong đó:

| Thành phần      | Nội dung                                 |
| --------------- | ---------------------------------------- |
| Schema          | tên, kiểu dữ liệu và đơn vị của features |
| Temporal        | timestamp, sampling frequency, ordering  |
| Features        | input variables và representation        |
| Target          | biến cần dự đoán                         |
| Split           | train/validation/test strategy           |
| Transformations | các preprocessing operations             |
| Validation      | các điều kiện dữ liệu phải thỏa mãn      |

Data contract giúp tách biệt **data preparation** khỏi **model implementation**.

Một model chỉ nên nhận dữ liệu đã thỏa mãn contract thay vì tự thực hiện các preprocessing operations không được kiểm soát.

---

# 4. Data Schema

AI-ready data trước hết phải có schema xác định.

Ví dụ:

$$
\mathbf{z}_t=

[
z_t^{(1)},
z_t^{(2)},
\ldots,
z_t^{(d)}
].
$$

Mỗi feature cần có:

* feature name;
* data type;
* unit;
* source;
* transformation;
* valid range;
* availability time.

Ví dụ:

| Feature     | Type       | Representation       | Availability |
| ----------- | ---------- | -------------------- | ------------ |
| temperature | continuous | standardized         | $t$          |
| humidity    | continuous | standardized         | $t$          |
| hour        | cyclic     | sin/cos              | $t$          |
| weekend     | binary     | $0/1$                | $t$          |
| target      | continuous | original/transformed | $t+H$        |

Schema phải được cố định trước khi model training để tránh tình trạng training và inference sử dụng feature ordering khác nhau.

---

# 5. Temporal Integrity

Đối với time series, temporal integrity là điều kiện bắt buộc.

Timestamp phải duy trì:

$$
t_1 \lt t_2 \lt \cdots \lt t_N.
$$

Nếu sampling interval cố định:

$$
t_{i+1}-t_i=\Delta t.
$$

Nếu sampling không đều, pipeline phải lưu thông tin về irregular intervals thay vì giả định dữ liệu regular.

Temporal integrity còn bao gồm việc phát hiện:

* duplicate timestamp;
* missing intervals;
* reordered observations;
* overlapping windows;
* misaligned target.

Một AI-ready sequence phải bảo đảm:

$$
\mathbf{X}_t=

[
\mathbf{x}_{t-L+1},
\ldots,
\mathbf{x}_t
]
$$

thực sự đại diện cho một khoảng thời gian liên tục hoặc một temporal segment hợp lệ.

---

# 6. Missing Values và Invalid Values

Sau preprocessing, các feature bắt buộc không nên chứa missing values ngoài những trường hợp đã được mô hình xử lý rõ ràng.

Điều kiện tối thiểu:

$$
x_t^{(j)}
\notin
{\mathrm{NaN},+\infty,-\infty}.
$$

Đối với feature matrix:

$$
\mathbf{X}
\in
\mathbb{R}^{N\times d},
$$

cần kiểm tra:

$$
\forall i,j:
\quad
X_{ij}\in\mathbb{R}.
$$

Nếu model hỗ trợ missing values, missingness có thể được giữ lại nhưng phải trở thành một phần rõ ràng của model contract.

Không nên để missing values tồn tại do preprocessing pipeline chưa hoàn chỉnh.

---

# 7. Feature Representation

AI-ready data phải có representation phù hợp với model.

Đối với tabular model:

$$
\mathbf{X}
\in
\mathbb{R}^{N\times d}.
$$

Đối với sequence model:

$$
\mathbf{X}
\in
\mathbb{R}^{B\times L\times d}.
$$

Trong đó:

* $B$: batch size;
* $L$: lookback;
* $d$: feature dimension.

Ví dụ:

$$
\mathbf{X}_t=

\begin{bmatrix}
x_{t-L+1}^{(1)} & \cdots & x_{t-L+1}^{(d)}\\
x_{t-L+2}^{(1)} & \cdots & x_{t-L+2}^{(d)}\\
\vdots & & \vdots\\
x_t^{(1)} & \cdots & x_t^{(d)}
\end{bmatrix}.
$$

Representation phải được cố định giữa training và inference:

$$
d_{train}=

d_{inference}.
$$

Thứ tự feature cũng phải giống nhau:

$$
[
f_1,f_2,\ldots,f_d
]_{train}=

[
f_1,f_2,\ldots,f_d
]_{inference}.
$$

---

# 8. Scaling Consistency

Nếu training data được standardize:

$$
z_t=

\frac{x_t-\mu_{train}}
{\sigma_{train}},
$$

thì inference phải sử dụng chính:

$$
\mu_{train},
\qquad
\sigma_{train}.
$$

Không được fit lại scaler trên inference data:

$$
\mu_{inference}
\neq
\mu_{train}.
$$

Pipeline đúng:

```text id="c4l5gt"
Training Data
     │
     ▼
Fit Scaler
     │
     ├── μ_train
     └── σ_train
     │
     ▼
Transform Train
     │
     ▼
Save Scaler
     │
     ├───────────────┐
     ▼               ▼
Validation        Test / Inference
     │               │
     └───────┬───────┘
             ▼
       Same Scaler
```

Điều này bảo đảm representation có cùng coordinate system trong toàn bộ lifecycle của model.

---

# 9. Target Definition

AI-ready dataset phải xác định rõ target.

Trong forecasting:

$$
y_{t+H}
$$

là target tại horizon $H$.

Input:

$$
\mathbf{X}_t=

[
\mathbf{x}_{t-L+1},
\ldots,
\mathbf{x}_t
].
$$

Một sample được định nghĩa:

$$
(\mathbf{X}_t,y_{t+H}).
$$

Điều này giúp tránh nhầm lẫn giữa:

* prediction timestamp;
* last input timestamp;
* target timestamp.

Có thể biểu diễn:

```text id="gdb2h8"
t-L+1                    t                t+H
  │──────────────────────│────────────────│
          INPUT                 TARGET
       lookback L             horizon H
```

Ví dụ, với $H=1$:

$$
(\mathbf{X}_{t-L+1:t},y_{t+1}).
$$

Target không được xuất hiện trong bất kỳ input feature nào.

---

# 10. Train/Validation/Test Split

AI-ready data phải được chia thành các tập phục vụ training và evaluation.

Đối với time series, chronological split thường được ưu tiên:

$$
\mathcal{D}=

\mathcal{D}_{train}
\cup
\mathcal{D}_{val}
\cup
\mathcal{D}_{test},
$$

với:

$$
\max(t_{train})
\lt
\min(t_{val}),
$$

và:

$$
\max(t_{val})
\lt
\min(t_{test}).
$$

Một cấu hình điển hình:

$$
70% / 15% / 15%.
$$

Không nên shuffle toàn bộ raw time series trước khi split nếu mục tiêu là đánh giá khả năng dự báo trên tương lai.

---

# 11. Leakage Firewall

AI-ready data phải có cơ chế ngăn leakage.

Có thể phân loại leakage thành:

### 11.1. Statistical leakage

Xảy ra khi preprocessing parameters được fit trên validation hoặc test.

Ví dụ:

$$
\mu=

\operatorname{mean}
(\mathcal{D}_{all}).
$$

### 11.2. Temporal leakage

Xảy ra khi feature tại $t$ sử dụng:

$$
x_{t+k},
\qquad k \gt 0.
$$

### 11.3. Target leakage

Xảy ra khi input chứa thông tin trực tiếp hoặc gián tiếp từ:

$$
y_{t+H}.
$$

### 11. Split leakage

Xảy ra khi một sample hoặc information source từ test set xuất hiện trong training process.

Do đó, AI-ready contract phải bảo đảm:

$$
\boxed{
\text{Information available to model}
\subseteq
\text{Information available at prediction time}
}
$$

---

# 12. Window Construction

Sau feature engineering, dữ liệu thường được chuyển thành sliding windows.

Với lookback $L$:

$$
\mathbf{X}_t=

\left[
\mathbf{z}_{t-L+1},
\ldots,
\mathbf{z}_t
\right].
$$

Target:

$$
y_{t+H}.
$$

Một dataset sequence hoàn chỉnh:

$$
\mathcal{D}_{seq}=

\left \{
\left(
\mathbf{X}_t,y_{t+H}
\right)
\right \}_{t\in\mathcal{T}}.
$$

Tuy nhiên, không phải mọi timestamp đều tạo được valid window.

Cần loại bỏ hoặc đánh dấu các trường hợp:

* insufficient history;
* input gap;
* target gap;
* duplicate timestamp;
* invalid temporal segment.

Do đó:

$$
\mathcal{T}_{valid}
\subseteq
\mathcal{T}_{candidate}.
$$

---

# 13. Window Integrity

Một sequence window hợp lệ phải thỏa mãn:

$$
t_{i+1}-t_i=\Delta t
$$

đối với toàn bộ input sequence nếu dataset yêu cầu regular sampling.

Đồng thời:

$$
t_{target} \gt t_{input,last}.
$$

Ví dụ:

$$
\mathbf{X}_t=

[
x_{t-3},x_{t-2},x_{t-1},x_t
]
$$

và:

$$
y=x_{t+1}.
$$

Window:

$$
[x_{t-3},x_{t-2},x_{t-1},x_t,x_{t+1}]
$$

là hợp lệ nếu không tồn tại gap hoặc duplicate trong interval.

---

# 14. Numerical Validation

AI-ready data phải được kiểm tra numerical validity.

Đối với mỗi feature:

$$
x_t^{(j)}
\in
\mathbb{R}.
$$

Kiểm tra:

$$
\operatorname{isfinite}
(x_t^{(j)})=

True.
$$

Ngoài ra cần kiểm tra:

* overflow;
* underflow;
* unexpected extreme values;
* incorrect data types;
* inconsistent units.

Đối với model input:

$$
\mathbf{X}
\in
\mathbb{R}^{B\times L\times d}
$$

phải có shape đúng với model configuration.

Ví dụ:

$$
d=d_{model}.
$$

Nếu:

$$
d\neq d_{model},
$$

dataset chưa thể được xem là AI-ready đối với model đó.

---

# 15. Feature Metadata

AI-ready data không chỉ bao gồm feature matrix.

Một pipeline có khả năng tái lập cần lưu metadata:

$$
\mathcal{M}=

{
\text{feature names},
\text{dtypes},
\text{units},
\text{transformations},
\text{scalers},
\text{lookback},
\text{horizon},
\text{split}
}.
$$

Ví dụ:

```text id="o8jv9n"
Feature Metadata
├── feature_names
├── feature_types
├── units
├── source_features
├── transformation
├── scaler_parameters
├── temporal_frequency
├── lookback
├── horizon
└── split_definition
```

Metadata giúp inference pipeline tái tạo chính xác preprocessing được sử dụng trong training.

---

# 16. Reproducibility

AI-ready data cần có khả năng tái tạo.

Có thể xem toàn bộ preprocessing như một hàm:

$$
\mathcal{P}
:
\mathcal{D}_{raw}
\rightarrow
\mathcal{D}_{AI}.
$$

Để reproducible, cần cố định:

$$
\mathcal{P}=

(
P_{clean},
P_{transform},
P_{feature},
P_{window},
P_{split}
).
$$

Trong đó mỗi thành phần có version và configuration tương ứng.

Ví dụ:

```text id="y5dq1n"
Dataset Version
      │
      ▼
Cleaning Version
      │
      ▼
Transformation Version
      │
      ▼
Feature Version
      │
      ▼
Window Version
      │
      ▼
AI-Ready Dataset
```

Nếu một transformation thay đổi, dataset revision cũng cần được cập nhật.

---

# 17. AI-Ready Data Quality Gates

Trước khi dữ liệu được chuyển sang model training, pipeline nên thực hiện quality gates.

### Gate 1 — Schema

$$
\text{Schema Valid} = True.
$$

### Gate 2 — Temporal

$$
\text{Temporal Integrity} = True.
$$

### Gate 3 — Missing

$$
\text{Missing Constraint} = True.
$$

### Gate 4 — Numerical

$$
\text{All Values Finite} = True.
$$

### Gate 5 — Feature

$$
d=d_{expected}.
$$

### Gate 6 — Alignment

$$
\text{Input/Target Alignment}=True.
$$

### Gate 7 — Leakage

$$
\text{Leakage Check}=Pass.
$$

### Gate 8 — Reproducibility

$$
\text{Metadata Complete}=True.
$$

Chỉ khi:

$$
\bigwedge_{k=1}^{8}
G_k=True
$$

thì dataset mới được sign-off là AI-ready.

---

# 18. AI-Ready Data Manifest

Một manifest có thể được sử dụng để mô tả dataset cuối:

```text id="n9r4tk"
AI-Ready Dataset
│
├── dataset_version
├── dataset_revision
├── timestamp_column
├── sampling_interval
├── feature_count
├── feature_names
├── target_name
├── lookback
├── horizon
├── train_range
├── validation_range
├── test_range
├── transformation_manifest
├── scaler_manifest
├── feature_manifest
├── window_manifest
└── validation_status
```

Manifest không phải là dữ liệu itself mà là **machine-readable description của preprocessing state**.

Nó cho phép downstream components kiểm tra dataset trước khi training.

---

# 19. AI-Ready Data cho các loại mô hình

Một representation có thể phù hợp với một model nhưng không nhất thiết phù hợp với model khác.

### Tabular models

Input:

$$
\mathbf{X}
\in
\mathbb{R}^{N\times d}.
$$

Phù hợp với:

* linear regression;
* random forest;
* gradient boosting;
* support vector machines.

### Sequence models

Input:

$$
\mathbf{X}
\in
\mathbb{R}^{B\times L\times d}.
$$

Phù hợp với:

* RNN;
* LSTM;
* GRU.

### Attention-based models

Input vẫn có thể có dạng:

$$
\mathbf{X}
\in
\mathbb{R}^{B\times L\times d},
$$

nhưng representation có thể cần thêm positional hoặc temporal encoding.

Do đó:

$$
\boxed{
AI-ready
\text{ is model-dependent}
}
$$

Một dataset không thể được gọi là AI-ready một cách tuyệt đối nếu chưa xác định downstream task và model interface.

---

# 20. Từ AI-Ready Data đến Model Training

Pipeline hoàn chỉnh:

```text id="n6k5ea"
Raw Data
    │
    ▼
Data Cleaning
    │
    ▼
Data Transformation
    │
    ▼
Feature Engineering
    │
    ▼
Feature Validation
    │
    ▼
Temporal Windowing
    │
    ▼
Leakage Validation
    │
    ▼
AI-Ready Data
    │
    ▼
Model Training
    │
    ▼
Evaluation
```

Điểm phân cách quan trọng là:

$$
\boxed{
\text{Preprocessing}
\rightarrow
\text{AI-Ready Data}
\rightarrow
\text{Model}
}
$$

Model không nên phải tự suy đoán preprocessing configuration.

---

# 21. Ví dụ cho bài toán Time-Series Forecasting

Giả sử dữ liệu được lấy mẫu mỗi $10$ phút và mục tiêu là dự đoán giá trị ở bước kế tiếp.

Với:

$$
L=36,
\qquad
H=1,
$$

input window tương ứng:

$$
36\times10=360\text{ minutes}=

6\text{ hours}.
$$

Sample thứ $t$:

$$
\mathbf{X}_t=

[
\mathbf{z}_{t-35},
\ldots,
\mathbf{z}_t
],
$$

và:

$$
y_t^{target}=y_{t+1}.
$$

Shape:

$$
\mathbf{X}_t
\in
\mathbb{R}^{36\times d}.
$$

Một batch:

$$
\mathbf{X}_{batch}
\in
\mathbb{R}^{B\times36\times d}.
$$

Đây là representation có thể đưa trực tiếp vào sequence model như LSTM hoặc Transformer.

---

# 22. AI-Ready Data và Evaluation

Một dataset chỉ thực sự có giá trị khi preprocessing không làm sai lệch evaluation.

Nếu target được transform:

$$
y_t'=f(y_t),
$$

model dự đoán:

$$
\hat{y}_t'=f(\hat{y}_t),
$$

thì metric cần được xác định rõ là tính trên transformed space hay original space.

Đối với các metric có đơn vị vật lý như MAE và RMSE, nên đưa prediction trở lại original space:

$$
\hat{y}_t=

f^{-1}
(\hat{y}_t').
$$

Sau đó:

$$
MAE=

\frac{1}{N}
\sum_{i=1}^{N}
|y_i-\hat{y}_i|,
$$

và:

$$
RMSE=

\sqrt{
\frac{1}{N}
\sum_{i=1}^{N}
(y_i-\hat{y}_i)^2
}.
$$

Điều này giúp metric giữ được ý nghĩa thực tế của target.

---

# 23. AI-Ready Data trong Edge/IoT

Trong Edge/IoT, AI-ready data có thể được tạo ở nhiều tầng:

```text id="6p7x3m"
Sensor
  │
  ▼
Edge Cleaning
  │
  ▼
Edge Transformation
  │
  ▼
Edge Feature Engineering
  │
  ▼
Compact AI-Ready Representation
  │
  ▼
Cloud / Edge AI Model
```

Việc tạo AI-ready representation tại edge có thể giảm:

$$
\text{Raw Data Volume}
\rightarrow
\text{Feature Data Volume}.
$$

Điều này có khả năng giảm communication cost và latency.

Tuy nhiên, edge preprocessing phải cân bằng:

$$
\text{Accuracy}
\leftrightarrow
\text{Bandwidth}
\leftrightarrow
\text{Latency}
\leftrightarrow
\text{Energy}
\leftrightarrow
\text{Compute}.
$$

Do đó, AI-ready data trong Edge/IoT không chỉ là vấn đề representation mà còn là vấn đề **resource-aware data processing**.

---

# 24. Final AI-Ready Checklist

Trước khi dataset được đưa vào training, cần kiểm tra:

```text id="1e8qzv"
[ ] Schema is valid
[ ] Timestamp is valid
[ ] Temporal ordering is preserved
[ ] Sampling interval is validated
[ ] Duplicate timestamps are handled
[ ] Missing values are handled
[ ] Invalid values are removed or corrected
[ ] Outliers are treated according to context
[ ] Required transformations are applied
[ ] Transformation parameters use training data only
[ ] Feature definitions are fixed
[ ] Feature ordering is fixed
[ ] Lag features use historical information only
[ ] Rolling features are causal
[ ] Input-target alignment is valid
[ ] No temporal leakage exists
[ ] Train/validation/test split is chronological
[ ] Window integrity is validated
[ ] All model inputs are finite
[ ] Input shape matches model requirements
[ ] Metadata is complete
[ ] Dataset version is recorded
```

Các quality gates này biến AI-ready data từ một khái niệm định tính thành một **có thể kiểm chứng được**.

---

# 25. Vị trí của AI-Ready Data trong nghiên cứu

Chương 11 có thể được tổng hợp thành:

$$
\boxed{
\text{Raw Data}
\rightarrow
\text{Cleaning}
\rightarrow
\text{Transformation}
\rightarrow
\text{Feature Engineering}
\rightarrow
\text{AI-Ready Data}
}
$$

Trong đó:

$$
\text{Cleaning}
\rightarrow
\text{Data Quality},
$$

$$
\text{Transformation}
\rightarrow
\text{Numerical / Statistical Representation},
$$

$$
\text{Feature Engineering}
\rightarrow
\text{Temporal Representation},
$$

và:

$$
\text{AI-Ready Data}
\rightarrow
\text{Model-Compatible Input}.
$$

AI-ready data vì vậy là **điểm giao giữa preprocessing và machine learning**. Đây cũng là điểm mà các quyết định preprocessing được chuyển thành một representation cụ thể mà mô hình AI có thể tiếp nhận.

---

# 26. Tóm tắt

AI-ready data không phải là dữ liệu đã trải qua nhiều preprocessing nhất, mà là dữ liệu đã trải qua **đúng các preprocessing cần thiết cho downstream task**.

Một representation được xem là AI-ready khi:

$$
\boxed{
\begin{aligned}
&\text{Valid} \\
&\land\ \text{Consistent} \\
&\land\ \text{Temporally Aligned} \\
&\land\ \text{Leakage-Free} \\
&\land\ \text{Model-Compatible} \\
&\land\ \text{Reproducible}
\end{aligned}
}
$$

Toàn bộ Chapter 11 do đó tạo thành một pipeline thống nhất:

$$
\boxed{
\mathcal{D}_{raw}
\xrightarrow{\text{Cleaning}}
\mathcal{D}_{clean}
\xrightarrow{\text{Transformation}}
\mathcal{D}_{transformed}
\xrightarrow{\text{Feature Engineering}}
\mathcal{D}_{feature}
\xrightarrow{\text{Validation}}
\mathcal{D}_{AI-ready}
}
$$

Cách tiếp cận này phù hợp với mục tiêu của nghiên cứu nền tảng về preprocessing time series: preprocessing cần được xem xét không chỉ như một tập hợp các kỹ thuật riêng lẻ mà như một **quy trình có hệ thống**, trong đó lựa chọn và thứ tự của các phép biến đổi quyết định chất lượng representation cuối cùng và có thể ảnh hưởng trực tiếp đến hiệu năng của AI model.

### Tài liệu tham khảo chính

Tawakuli, A., Havers, B., Gulisano, V. M., Kaiser, D., & Engel, T. (2025). *Survey: Time-Series Data Preprocessing: A Survey and an Empirical Analysis*. **Journal of Engineering Research, 13**(2), 674–711. DOI: 10.1016/j.jer.2024.02.018. Nghiên cứu cung cấp cơ sở cho việc tổ chức preprocessing time series thành một quy trình có hệ thống và đánh giá tác động của preprocessing đến data quality cũng như AI performance.

[ScienceDirect — bài báo gốc](https://www.sciencedirect.com/science/article/pii/S2307187724000452?utm_source=chatgpt.com)
