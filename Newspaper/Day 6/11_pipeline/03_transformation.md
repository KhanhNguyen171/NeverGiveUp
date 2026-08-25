# 11.3 Transformation Pipeline

## 1. Mục tiêu

Data transformation là giai đoạn biến đổi dữ liệu sau cleaning thành biểu diễn phù hợp hơn cho các thuật toán phân tích, machine learning và deep learning. Khác với **data cleaning**, tập trung vào việc khắc phục các vấn đề về chất lượng dữ liệu, transformation tập trung vào **thay đổi scale, distribution, temporal properties hoặc structural representation của dữ liệu** mà vẫn bảo toàn thông tin cần thiết cho nhiệm vụ downstream.

Với chuỗi thời gian:

$$
\mathcal{D}_{clean}=

\left \{
(t_i,\mathbf{x}_i)
\right \}_{i=1}^{N},
$$

transformation pipeline có thể được biểu diễn tổng quát:

$$
\mathcal{D}_{clean}
\xrightarrow{f_1}
\mathcal{D}_1
\xrightarrow{f_2}
\cdots
\xrightarrow{f_K}
\mathcal{D}_{transformed}.
$$

Mỗi phép biến đổi:

$$
f_k:\mathcal{X}_{k-1}\rightarrow\mathcal{X}_k
$$

phải được lựa chọn dựa trên đặc điểm dữ liệu và yêu cầu của mô hình.

Trong nghiên cứu này, transformation pipeline tập trung vào bốn nhóm chính:

1. scaling và normalization;
2. mathematical transformation;
3. stationarity transformation;
4. time-series decomposition.

Các nhóm này tương ứng với các nội dung đã được trình bày trong **Chương 4 — Data Transformation**, nhưng ở đây được tổ chức lại thành một quy trình có khả năng triển khai.

---

## 2. Vị trí của Transformation trong toàn bộ pipeline

Transformation được thực hiện sau Data Cleaning:

```text
Raw Data
    │
    ▼
Data Validation
    │
    ▼
Data Cleaning
    │
    ▼
┌──────────────────────────┐
│   Transformation         │
│                          │
│  ├─ Scaling              │
│  ├─ Normalization        │
│  ├─ Mathematical         │
│  │   Transformation      │
│  ├─ Stationarity         │
│  └─ Decomposition        │
└────────────┬─────────────┘
             │
             ▼
Feature Engineering
             │
             ▼
AI-Ready Data
```

Một transformation không nhất thiết phải được áp dụng cho mọi dataset. Pipeline cần xác định **transformation objectives** trước khi lựa chọn phương pháp.

Ví dụ:

| Vấn đề                              | Transformation phù hợp                |
| ----------------------------------- | ------------------------------------- |
| Features có scale rất khác nhau     | Standardization / Min-Max             |
| Distribution bị lệch                | Log / Power transformation            |
| Variance thay đổi theo level        | Log / Box-Cox                         |
| Chuỗi chứa trend mạnh               | Differencing / detrending             |
| Chuỗi chứa seasonality              | Seasonal differencing / decomposition |
| Muốn tách trend và seasonal pattern | Decomposition                         |

Do đó:

$$
\boxed{
\text{Transformation}
\neq
\text{Apply all methods}
}
$$

mà:

$$
\boxed{
\text{Transformation}=

\text{Select necessary transformations}
}
$$

---

## 3. Transformation contract

Một transformation nên được định nghĩa bởi bốn thành phần:

$$
T=
(\text{method},
\text{parameters},
\text{fit data},
\text{application scope}).
$$

Ví dụ, với Standardization:

$$
T_{std}=

(\text{StandardScaler},
\mu,\sigma,
\mathcal{D}_{train},
\text{features}).
$$

Cách biểu diễn này giúp pipeline xác định rõ:

* sử dụng phương pháp nào;
* tham số được ước lượng như thế nào;
* tham số được học từ tập dữ liệu nào;
* transformation được áp dụng lên feature nào.

Điều này đặc biệt quan trọng đối với machine learning vì transformation có tham số học được phải tránh data leakage.

---

# 4. Scaling và Normalization

## 4.1. Mục tiêu

Các numerical features thường có đơn vị và scale khác nhau. Ví dụ:

$$
x^{(1)}\in[0,1],
\qquad
x^{(2)}\in[0,10^3],
\qquad
x^{(3)}\in[0,10^6].
$$

Nếu đưa trực tiếp vào các thuật toán dựa trên distance hoặc gradient, feature có scale lớn có thể chi phối objective function.

Transformation nhằm tạo ra:

$$
\mathbf{z}_t=

f(\mathbf{x}_t)
$$

sao cho các feature có scale phù hợp hơn.

---

## 4.2. Min-Max Scaling

Min-Max scaling đưa feature về một khoảng xác định, thường là $[0,1]$:

$$
z_t=

\frac{x_t-x_{\min}}
{x_{\max}-x_{\min}}.
$$

Tổng quát với khoảng $[a,b]$:

$$
z_t=

a+
\frac{(x_t-x_{\min})(b-a)}
{x_{\max}-x_{\min}}.
$$

Ưu điểm:

* giữ nguyên thứ tự tương đối;
* bounded range;
* phù hợp với một số neural network architectures.

Nhược điểm:

* nhạy với extreme values;
* một outlier có thể làm thay đổi đáng kể $x_{\min}$ và $x_{\max}$.

Trong pipeline machine learning, $x_{\min}$ và $x_{\max}$ phải được ước lượng từ training data.

---

## 4.3. Standardization

Standardization biến đổi feature thành zero mean và unit variance:

$$
z_t=

\frac{x_t-\mu}
{\sigma}.
$$

Trong đó:

$$
\mu=

\frac{1}{N}
\sum_{i=1}^{N}x_i,
$$

và

$$
\sigma=

\sqrt{
\frac{1}{N}
\sum_{i=1}^{N}
(x_i-\mu)^2
}.
$$

Trong supervised learning:

$$
\mu,\sigma=

\operatorname{Fit}
(\mathcal{D}_{train}),
$$

sau đó áp dụng cùng transformation cho validation và test.

Standardization thường phù hợp khi:

* feature có distribution tương đối ổn định;
* model nhạy với scale;
* muốn giảm chênh lệch magnitude giữa các feature.

---

## 4.4. Robust Scaling

Khi dữ liệu chứa nhiều extreme values, median và IQR có thể được sử dụng:

$$
z_t=

\frac{x_t-\operatorname{median}(x)}
{IQR(x)},
$$

với:

$$
IQR(x)=Q_{0.75}(x)-Q_{0.25}(x).
$$

Robust scaling ít bị ảnh hưởng bởi outlier hơn Standardization.

Tuy nhiên, robust scaling không tự động giải quyết outliers. Nó chỉ làm giảm ảnh hưởng của chúng đến quá trình xác định scale.

---

# 5. Mathematical Transformation

Scaling thay đổi scale của dữ liệu, trong khi mathematical transformation có thể thay đổi cả distribution hoặc variance structure.

## 5.1. Logarithmic transformation

Với dữ liệu dương:

$$
z_t=\log(x_t).
$$

Nếu tồn tại giá trị bằng hoặc nhỏ hơn zero, có thể sử dụng:

$$
z_t=\log(x_t+c),
$$

với $c$ được chọn sao cho:

$$
x_t+c \gt 0.
$$

Log transformation thường được sử dụng khi:

* dữ liệu có right-skew;
* variance tăng theo magnitude;
* giá trị có dynamic range lớn.

Ví dụ, nếu:

$$
x_t\in[1,10^6],
$$

log transformation có thể nén dynamic range đáng kể.

Tuy nhiên, transformation này thay đổi interpretation của target và do đó cần được inverse-transform khi cần đưa prediction về đơn vị ban đầu.

---

## 5.2. Power transformation

Một họ transformation tổng quát là:

$$
x_t^{(\lambda)}
=
\begin{cases}
\dfrac{x_t^\lambda - 1}{\lambda},
& \lambda \neq 0, \\[6pt]
\log(x_t),
& \lambda = 0.
\end{cases}
$$

Trong đó $\lambda$ điều khiển mức độ biến đổi.

Box-Cox transformation thường được sử dụng với dữ liệu dương để giảm skewness và làm variance ổn định hơn.

---

## 5.3. Yeo-Johnson transformation

Khi dữ liệu có thể chứa cả giá trị dương và âm, Yeo-Johnson là một lựa chọn tổng quát hơn Box-Cox.

Transformation được xác định theo $\lambda$ và miền của $x_t$.

Ưu điểm chính là không yêu cầu:

$$
x_t \gt 0.
$$

Điều này làm nó phù hợp với nhiều numerical time-series features có thể nhận cả giá trị âm và dương.

---

# 6. Stationarity Transformation

## 6.1. Mục tiêu

Một chuỗi được xem là stationary khi các đặc tính thống kê cơ bản không thay đổi theo thời gian.

Một cách mô tả đơn giản:

$$
E[X_t]=\mu,
$$

$$
Var(X_t)=\sigma^2,
$$

và autocovariance phụ thuộc chủ yếu vào lag:

$$
Cov(X_t,X_{t-k})=

\gamma(k).
$$

Trong thực tế, nhiều time series chứa:

* trend;
* seasonality;
* changing variance.

Các thành phần này có thể làm cho chuỗi không stationary.

---

## 6.2. Differencing

First-order differencing:

$$
\Delta x_t=

x_t-x_{t-1}.
$$

Nếu một chuỗi chứa linear trend:

$$
x_t=

\beta_0+\beta_1t+\epsilon_t,
$$

thì:

$$
\Delta x_t=

\beta_1+
\epsilon_t-\epsilon_{t-1},
$$

có thể loại bỏ phần trend tuyến tính.

Higher-order differencing:

$$
\Delta^d x_t=

\Delta
\left(
\Delta^{d-1}x_t
\right).
$$

Tuy nhiên, differencing quá mức có thể làm mất thông tin dài hạn và tăng noise.

---

## 6.3. Seasonal differencing

Với seasonality có chu kỳ $s$:

$$
\Delta_s x_t=

x_t-x_{t-s}.
$$

Nếu chuỗi có seasonal pattern:

$$
x_t=T_t+S_t+\epsilon_t,
$$

seasonal differencing có thể làm giảm thành phần $S_t$.

Một chuỗi có cả trend và seasonality có thể sử dụng:

$$
\Delta\Delta_s x_t.
$$

Tuy nhiên, transformation cần được kiểm chứng thay vì mặc định áp dụng.

---

# 7. Decomposition

Decomposition tách chuỗi thành các thành phần có ý nghĩa hơn:

$$
x_t=T_t+S_t+R_t,
$$

trong đó:

* $T_t$: trend;
* $S_t$: seasonal component;
* $R_t$: residual.

Đối với multiplicative decomposition:

$$
x_t=T_tS_tR_t.
$$

Multiplicative decomposition thường phù hợp hơn khi biên độ seasonality tăng theo level của chuỗi.

---

## 7.1. Trend extraction

Trend biểu diễn long-term behavior:

$$
T_t=f(t).
$$

Các phương pháp phổ biến gồm:

* moving average;
* smoothing;
* regression;
* decomposition-based methods.

Trend có thể được sử dụng trực tiếp như một feature hoặc được loại bỏ trước khi mô hình hóa residual.

---

## 7.2. Seasonal extraction

Seasonal component biểu diễn pattern lặp lại theo chu kỳ:

$$
S_{t+s}=S_t.
$$

Ví dụ:

* hourly seasonality;
* daily seasonality;
* weekly seasonality;
* yearly seasonality.

Việc xác định $s$ phải dựa trên sampling frequency và domain knowledge.

---

## 7.3. Residual

Sau khi loại bỏ trend và seasonality:

$$
R_t=

x_t-T_t-S_t.
$$

Residual phản ánh phần biến động chưa được giải thích bởi hai thành phần chính.

Residual có thể được sử dụng để:

* phát hiện anomaly;
* đánh giá decomposition;
* xây dựng mô hình residual;
* kiểm tra mức độ còn lại của temporal structure.

---

# 8. Thứ tự thực hiện Transformation

Không tồn tại một thứ tự duy nhất cho mọi dataset. Tuy nhiên, một pipeline có thể được tổ chức như sau:

```text
Clean Data
    │
    ▼
Distribution Analysis
    │
    ├── Skewed?
    │      │
    │      ▼
    │   Mathematical
    │   Transformation
    │
    ▼
Stationarity Analysis
    │
    ├── Non-stationary?
    │      │
    │      ├── Trend
    │      │    └── Differencing / Detrending
    │      │
    │      └── Seasonality
    │           └── Seasonal Differencing /
    │               Decomposition
    │
    ▼
Scaling / Normalization
    │
    ▼
Transformed Data
```

Điểm quan trọng là **transformation cần được quyết định dựa trên diagnostics**.

Ví dụ:

$$
\text{Skewness}
\rightarrow
\text{Log / Power Transformation},
$$

trong khi:

$$
\text{Trend}
\rightarrow
\text{Differencing / Detrending},
$$

và:

$$
\text{Different Feature Scales}
\rightarrow
\text{Scaling}.
$$

Không nên áp dụng cả ba phép biến đổi chỉ vì chúng tồn tại trong pipeline.

---

# 9. Fit và Apply Transformation

Đối với transformation có tham số học được, pipeline phải tách rõ hai operation:

$$
\theta=

\operatorname{Fit}
(\mathcal{D}_{train}),
$$

và:

$$
\mathcal{D}'=

f_\theta(\mathcal{D}).
$$

Ví dụ với Standardization:

$$
\theta=(\mu_{train},\sigma_{train}).
$$

Sau đó:

$$
x_{train}'=

\frac{x_{train}-\mu_{train}}
{\sigma_{train}},
$$

$$
x_{val}'=

\frac{x_{val}-\mu_{train}}
{\sigma_{train}},
$$

$$
x_{test}'=

\frac{x_{test}-\mu_{train}}
{\sigma_{train}}.
$$

Không được sử dụng:

$$
\mu_{all},
\qquad
\sigma_{all},
$$

được tính từ:

$$
\mathcal{D}_{train}
\cup
\mathcal{D}_{val}
\cup
\mathcal{D}_{test}.
$$

Đây là nguyên tắc quan trọng để ngăn preprocessing leakage.

---

# 10. Inverse Transformation

Một số transformation cần khả năng đưa kết quả trở lại original space.

Nếu:

$$
z_t=f(x_t),
$$

và $f$ khả nghịch, ta có:

$$
x_t=f^{-1}(z_t).
$$

Ví dụ với Standardization:

$$
x_t=

z_t\sigma+\mu.
$$

Với forecasting, nếu target được transform trước khi training:

$$
y_t'=

f(y_t),
$$

model tạo prediction:

$$
\hat{y}_t',
$$

thì prediction cuối cùng phải được đưa về original space:

$$
\hat{y}_t=

f^{-1}(\hat{y}_t').
$$

Việc này đặc biệt quan trọng khi metric được báo cáo theo đơn vị vật lý ban đầu.

---

# 11. Transformation và temporal leakage

Transformation trên time series phải đặc biệt chú ý đến temporal ordering.

Ví dụ, rolling transformation:

$$
z_t=

\frac{1}{w}
\sum_{k=0}^{w-1}
x_{t-k}
$$

chỉ sử dụng dữ liệu quá khứ và hiện tại.

Ngược lại, nếu sử dụng centered window:

$$
z_t=

\frac{1}{2w+1}
\sum_{k=-w}^{w}
x_{t+k},
$$

thì $z_t$ sử dụng:

$$
x_{t+1},\ldots,x_{t+w},
$$

tức thông tin tương lai.

Đối với forecasting, điều này có thể tạo ra **temporal leakage**.

Do đó:

$$
\boxed{
\text{Transformation at time }t
\text{ must not use unavailable future information}
}
$$

nếu transformation được thực hiện trong production forecasting setting.

---

# 12. Transformation và feature semantics

Không phải mọi feature đều nên được transform giống nhau.

Giả sử:

$$
\mathbf{x}_t=

[
x_t^{numeric},
x_t^{binary},
x_t^{categorical},
x_t^{cyclical}
].
$$

Một pipeline hợp lý có thể sử dụng:

$$
x_t^{numeric}
\rightarrow
\text{Standardization},
$$

trong khi:

$$
x_t^{binary}
\rightarrow
\text{Passthrough},
$$

và categorical features có thể được:

$$
x_t^{categorical}
\rightarrow
\text{Encoding}.
$$

Đối với cyclical features đã được biểu diễn:

$$
\sin\left(\frac{2\pi c_t}{P}\right),
\qquad
\cos\left(\frac{2\pi c_t}{P}\right),
$$

không nên tiếp tục áp dụng một transformation không cần thiết nếu nó làm mất ý nghĩa hình học của representation.

Do đó, transformation phải được **feature-aware** thay vì áp dụng đồng nhất trên toàn bộ feature matrix.

---

# 13. Transformation trong Edge/IoT

Trong Edge/IoT, transformation phải cân bằng giữa chất lượng representation và chi phí tính toán.

Các phép transformation đơn giản như:

$$
z_t=\frac{x_t-\mu}{\sigma}
$$

có computational cost thấp và dễ triển khai trên edge devices.

Trong khi đó, decomposition hoặc model-based transformation có thể yêu cầu:

* nhiều bộ nhớ;
* nhiều phép tính;
* model parameters;
* processing latency cao hơn.

Do đó, có thể phân chia:

```text
Sensor
   │
   ▼
Edge
   ├── lightweight scaling
   ├── normalization
   └── simple filtering
   │
   ▼
Cloud / Server
   ├── decomposition
   ├── advanced transformation
   └── model-specific processing
```

Lựa chọn này phụ thuộc vào bandwidth, latency, computational capacity và yêu cầu privacy của hệ thống.

---

# 14. Transformation validation

Sau transformation, cần kiểm tra dataset trước khi chuyển sang feature engineering.

Các kiểm tra chính:

### Scale

Kiểm tra range hoặc distribution:

$$
\operatorname{mean}(z)
\approx0,
\qquad
\operatorname{std}(z)
\approx1
$$

đối với Standardization.

### Distribution

Kiểm tra xem transformation có thực sự làm giảm skewness hoặc variance heterogeneity hay không.

### Temporal integrity

Transformation không được làm thay đổi:

$$
t_1 \lt t_2 \lt \cdots \lt t_N.
$$

### Missing values

Transformation không được tạo ra NaN hoặc infinite values ngoài các trường hợp đã được kiểm soát:

$$
z_t\notin
{\mathrm{NaN},+\infty,-\infty}.
$$

### Invertibility

Nếu transformation yêu cầu inverse transformation, cần kiểm tra:

$$
f^{-1}(f(x))
\approx x.
$$

Sai số numerical nhỏ có thể chấp nhận được:

$$
|f^{-1}(f(x))-x| \lt \epsilon.
$$

---

# 15. Decision logic

Transformation pipeline có thể được tóm tắt bằng decision logic:

```text
                    Clean Data
                        │
                        ▼
              Analyze Distribution
                 /            \
             Skewed          Not Skewed
                │                 │
                ▼                 │
        Log / Power               │
                │                 │
                └────────┬────────┘
                         ▼
                 Analyze Stationarity
                    /           \
              Non-stationary   Stationary
                  │                │
                  ▼                │
          Differencing /           │
          Decomposition            │
                  │                │
                  └───────┬────────┘
                          ▼
                    Scale Features
                          │
                          ▼
                  Transformation
                       Output
```

Decision process này phản ánh nguyên tắc **need-based transformation**: chỉ thực hiện transformation khi diagnostics cho thấy nó có mục đích rõ ràng.

---

# 16. Đầu ra của Transformation Pipeline

Sau transformation, dataset có dạng:

$$
\mathcal{D}_{transformed}=

\left \{
(t_i,\mathbf{z}_i)
\right \}_{i=1}^{N},
$$

với:

$$
\mathbf{z}_i=

T(\mathbf{x}_i).
$$

Dữ liệu này được chuyển sang Feature Engineering Pipeline để xây dựng các temporal, lag, rolling và representation features.

Quan hệ giữa hai giai đoạn:

$$
\boxed{
\mathcal{D}_{clean}
\xrightarrow{
\text{Transformation}
}
\mathcal{D}_{transformed}
\xrightarrow{
\text{Feature Engineering}
}
\mathcal{D}_{feature}
}
$$

Transformation vì vậy đóng vai trò **cầu nối giữa data quality và model representation**. Nó không nhằm tối ưu trực tiếp mô hình AI mà chuẩn bị numerical representation sao cho phù hợp với assumptions, optimization procedure và input requirements của mô hình downstream.

---

## 17. Tóm tắt

Transformation pipeline gồm bốn nhóm chính:

$$
\boxed{
\text{Scaling}
+
\text{Mathematical Transformation}
+
\text{Stationarity Transformation}
+
\text{Decomposition}
}
$$

Trong đó:

* **Scaling** điều chỉnh magnitude giữa các features;
* **Mathematical transformation** điều chỉnh distribution và variance structure;
* **Stationarity transformation** xử lý trend và seasonal non-stationarity khi cần;
* **Decomposition** tách các thành phần temporal để tạo representation hoặc hỗ trợ modeling.

Nguyên tắc cốt lõi của pipeline là:

$$
\boxed{
\text{Diagnose}
\rightarrow
\text{Select}
\rightarrow
\text{Fit}
\rightarrow
\text{Transform}
\rightarrow
\text{Validate}
}
$$

Thay vì áp dụng toàn bộ các phương pháp transformation, pipeline chỉ lựa chọn những phép biến đổi có cơ sở từ đặc điểm dữ liệu và yêu cầu của downstream task. Cách tiếp cận này giúp giảm over-processing, hạn chế information loss và duy trì khả năng tái lập của toàn bộ preprocessing workflow.

### Tài liệu tham khảo chính

Tawakuli, A., Havers, B., Gulisano, V. M., Kaiser, D., & Engel, T. (2025). *Survey: Time-Series Data Preprocessing: A Survey and an Empirical Analysis*. **Journal of Engineering Research, 13**(2), 674–711. DOI: 10.1016/j.jer.2024.02.018. Bài nghiên cứu cung cấp taxonomy và empirical analysis về các kỹ thuật preprocessing cho numerical time series, trong đó transformation là một thành phần quan trọng của quá trình chuẩn bị dữ liệu cho AI. [ScienceDirect — bài báo gốc](https://www.sciencedirect.com/science/article/pii/S2307187724000452?utm_source=chatgpt.com)
