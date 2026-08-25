# 12.3 Common Mistakes

Preprocessing time-series data có thể cải thiện đáng kể chất lượng dữ liệu và hiệu quả của mô hình, nhưng cũng có thể làm sai lệch kết quả nếu được thực hiện không đúng cách. Các lỗi preprocessing thường không xuất hiện dưới dạng lỗi chương trình mà tồn tại dưới dạng **sai lệch phương pháp luận**, khiến kết quả thực nghiệm có vẻ tốt nhưng không phản ánh đúng khả năng tổng quát hóa của mô hình.

Trong nghiên cứu này, các common mistakes được phân loại thành bốn nhóm chính:

$$
\boxed{
\text{Data Errors}
+
\text{Temporal Errors}
+
\text{Statistical Errors}
+
\text{Experimental Errors}
}
$$

Các lỗi này cần được kiểm soát xuyên suốt pipeline từ raw data đến AI-ready data.

---

## 1. Applying Preprocessing Without Identifying the Data Problem

Một lỗi phổ biến là áp dụng preprocessing chỉ vì một phương pháp được sử dụng rộng rãi.

Ví dụ:

* luôn luôn standardize mọi feature;
* luôn luôn remove outliers;
* luôn luôn interpolate missing values;
* luôn luôn difference time series;
* luôn luôn apply dimensionality reduction.

Cách tiếp cận này có thể được biểu diễn:

$$
\text{Method}
\rightarrow
\text{Data}
$$

thay vì quy trình hợp lý:

$$
\text{Data Problem}
\rightarrow
\text{Method}.
$$

Một preprocessing operation chỉ nên được sử dụng khi tồn tại một lý do dữ liệu hoặc modeling rõ ràng để áp dụng nó.

Ví dụ, nếu:

$$
N_{missing}=0,
$$

thì missing-value imputation không tạo ra giá trị bổ sung cho dataset.

Nguyên tắc:

$$
\boxed{
\text{No identified problem}
\Rightarrow
\text{No unnecessary preprocessing}
}
$$

---

## 2. Randomly Shuffling Time-Series Data

Random shuffling là một trong những lỗi nghiêm trọng nhất khi xử lý time series.

Với dữ liệu thông thường, random split:

$$
\mathcal{D}
\rightarrow
\mathcal{D}_{train}
\cup
\mathcal{D}_{test}
$$

có thể phù hợp nếu các observations độc lập và identically distributed.

Tuy nhiên, với time series:

$$
t_1 \lt t_2 \lt \cdots \lt t_N,
$$

thông tin tại thời điểm tương lai có thể liên quan trực tiếp đến thông tin tại thời điểm quá khứ.

Nếu random split được sử dụng:

$$
\mathcal{D}*{train}
\cap
\mathcal{D}*{future}
\neq\varnothing,
$$

thì training set có thể chứa các observations xảy ra sau một số observations trong test set.

Một chronological split phù hợp hơn:

$$
\mathcal{D}_{train}=

{t_1,\ldots,t_{T_1}},
$$

$$
\mathcal{D}_{val}=

{t_{T_1+1},\ldots,t_{T_2}},
$$

$$
\mathcal{D}_{test}=

{t_{T_2+1},\ldots,t_N}.
$$

Vì vậy, **temporal ordering phải được xem là một constraint của experimental design**, không chỉ là một đặc tính của dataset.

---

## 3. Fitting Preprocessing on the Entire Dataset

Một lỗi phổ biến khác là fit preprocessing parameters trên toàn bộ dataset trước khi split.

Ví dụ, StandardScaler được tính bằng:

$$
\mu=

\frac{1}{N}
\sum_{i=1}^{N}x_i,
$$

$$
\sigma=

\sqrt{
\frac{1}{N}
\sum_{i=1}^{N}(x_i-\mu)^2
}.
$$

Sau đó:

$$
z_i=\frac{x_i-\mu}{\sigma}.
$$

Nếu $\mu$ và $\sigma$ được tính từ cả training và test data, thì test distribution đã ảnh hưởng đến training representation.

Đây là **data leakage**.

Cách đúng là:

$$
\mu_{train}=

\operatorname{mean}(\mathcal{D}_{train}),
$$

$$
\sigma_{train}=

\operatorname{std}(\mathcal{D}_{train}),
$$

sau đó áp dụng cùng parameters cho validation và test.

Nguyên tắc:

$$
\boxed{
\text{Fit on Train}
\rightarrow
\text{Transform Train/Validation/Test}
}
$$

---

## 4. Performing Feature Engineering Before the Temporal Split

Feature engineering cũng có thể tạo leakage ngay cả khi không sử dụng trực tiếp target.

Ví dụ, một rolling mean được tính:

$$
r_t=

\frac{1}{2w+1}
\sum_{i=-w}^{w}x_{t+i}.
$$

Biểu thức này sử dụng cả:

$$
x_{t+1},\ldots,x_{t+w},
$$

tức là thông tin tương lai.

Đối với forecasting, representation đúng phải là causal:

$$
r_t=

\frac{1}{w}
\sum_{i=0}^{w-1}x_{t-i}.
$$

Tương tự, normalization, aggregation hoặc feature selection sử dụng toàn bộ temporal range trước khi split cũng có thể làm leakage.

Do đó, không chỉ preprocessing parameters mà **feature construction process cũng phải tôn trọng temporal boundary**.

---

## 5. Treating Every Extreme Value as an Error

Một observation có giá trị cực đoan không đồng nghĩa với observation sai.

Giả sử:

$$
x_t \gg \operatorname{median}(X).
$$

Observation này có thể là:

1. measurement error;
2. sensor malfunction;
3. communication error;
4. hoặc một genuine extreme event.

Việc tự động loại bỏ:

$$
x_t \rightarrow \varnothing
$$

có thể làm mất thông tin quan trọng.

Đặc biệt trong energy, traffic, finance hoặc environmental time series, extreme events có thể chính là những observations quan trọng nhất đối với forecasting.

Do đó:

$$
\boxed{
\text{Outlier detection}
\neq
\text{Outlier removal}
}
$$

Quyết định xử lý cần dựa trên cả statistical evidence và domain semantics.

---

## 6. Ignoring the Missingness Pattern

Chỉ báo cáo:

$$
\text{Missing Rate}=

\frac{N_{missing}}{N}
$$

là chưa đủ.

Hai datasets có cùng missing rate:

$$
MR(\mathcal{D}_1)=

MR(\mathcal{D}_2)
$$

có thể có tác động hoàn toàn khác nhau nếu:

* $\mathcal{D}_1$ có nhiều gaps ngắn;
* $\mathcal{D}_2$ có một hoặc nhiều gaps dài.

Ví dụ:

$$
x_1,x_2,\boxed{?},x_4,x_5
$$

khác về mặt temporal structure so với:

$$
x_1,\boxed{?,?,?,?,?},x_7.
$$

Interpolation có thể hợp lý trong trường hợp đầu tiên nhưng tạo ra giá trị giả đáng kể trong trường hợp thứ hai.

Do đó cần xem xét:

$$
\boxed{
\text{Missing Rate}
+
\text{Gap Length}
+
\text{Temporal Pattern}
}
$$

trước khi lựa chọn imputation method.

---

## 7. Ignoring Timestamp Quality

Time-series preprocessing có thể trở nên không hợp lệ nếu timestamp không được kiểm tra.

Một dataset có thể chứa:

* duplicate timestamps;
* missing timestamps;
* unordered timestamps;
* irregular sampling;
* timezone inconsistencies;
* timestamp parsing errors.

Giả sử sampling interval mong đợi là $\Delta t$. Cần kiểm tra:

$$
t_{i+1}-t_i=\Delta t.
$$

Nếu:

$$
t_{i+1}-t_i\neq\Delta t,
$$

thì dữ liệu không còn là một sequence đều theo sampling grid giả định.

Điều này ảnh hưởng trực tiếp đến:

* lag features;
* rolling windows;
* temporal alignment;
* forecasting horizon;
* window generation;
* decomposition.

Vì vậy, timestamp validation phải được thực hiện trước các operations phụ thuộc vào temporal distance.

---

## 8. Applying the Same Transformation to All Features

Một lỗi phổ biến là coi feature matrix như một khối đồng nhất:

$$
\mathbf{X}\in\mathbb{R}^{N\times F}
$$

và áp dụng một transformation duy nhất cho toàn bộ $F$ features.

Trong thực tế:

$$
\mathbf{X}=

[
\mathbf{X}_{continuous},
\mathbf{X}_{binary},
\mathbf{X}_{cyclical},
\mathbf{X}_{categorical}
].
$$

Các feature types này có properties khác nhau.

Ví dụ, cyclic feature:

$$
(\sin\theta,\cos\theta)
$$

đã có representation bounded trong $[-1,1]$.

Binary feature:

$$
x\in{0,1}
$$

cũng không có cùng ý nghĩa với continuous measurement.

Do đó, preprocessing nên được feature-aware:

$$
T(\mathbf{X})=

[
T_c(\mathbf{X}_c),
T_b(\mathbf{X}_b),
T_{cyc}(\mathbf{X}_{cyc}),
T_{cat}(\mathbf{X}_{cat})
].
$$

---

## 9. Over-Processing the Data

Over-processing xảy ra khi quá nhiều transformations được áp dụng mà không có evidence rằng chúng cần thiết.

Một pipeline có thể trở thành:

$$
\text{Imputation}
\rightarrow
\text{Outlier Removal}
\rightarrow
\text{Smoothing}
\rightarrow
\text{Transformation}
\rightarrow
\text{Differencing}
\rightarrow
\text{Scaling}
\rightarrow
\text{PCA}
\rightarrow
\text{Feature Engineering}.
$$

Mặc dù mỗi bước riêng lẻ có thể hợp lý, việc kết hợp tất cả chúng có thể dẫn đến:

* information loss;
* reduced interpretability;
* accumulated errors;
* excessive computational cost;
* difficulty in reproducing results.

Đặc biệt, nhiều transformations có thể làm thay đổi bản chất của signal.

Nguyên tắc:

$$
\boxed{
\text{More preprocessing}
\not\Rightarrow
\text{better data}
}
$$

Mục tiêu là **sufficient preprocessing**, không phải maximum preprocessing.

---

## 10. Excessive Smoothing

Noise reduction là một preprocessing task quan trọng, nhưng smoothing quá mạnh có thể làm mất signal.

Với moving average:

$$
\tilde{x}_t=

\frac{1}{w}
\sum_{i=0}^{w-1}x_{t-i},
$$

khi $w$ tăng, signal càng smooth.

Nếu:

$$
w\rightarrow T,
$$

thì local dynamics bị triệt tiêu và series tiến gần tới một global average.

Điều này có thể làm mất:

* peaks;
* sudden changes;
* short-term dependencies;
* event boundaries.

Do đó, smoothing parameter cần được lựa chọn dựa trên temporal scale của signal.

---

## 11. Incorrect Transformation of the Target

Một lỗi quan trọng trong supervised forecasting là preprocessing target không được quản lý đúng cách.

Giả sử:

$$
y_t
$$

là target ở original unit.

Nếu target được standardized:

$$
y_t'=

\frac{y_t-\mu_y}{\sigma_y},
$$

thì predictions phải được inverse-transform trước khi tính metrics trong original unit:

$$
\hat{y}_t=

\sigma_y\hat{y}_t'
+
\mu_y.
$$

Nếu RMSE được tính trực tiếp trên scaled target:

$$
RMSE_{scaled}=

\sqrt{
\frac{1}{N}
\sum_{i=1}^{N}
(y_i'-\hat{y}_i')^2
},
$$

thì metric không còn có đơn vị gốc của bài toán.

Do đó, cần phân biệt rõ:

$$
\boxed{
\text{Training representation}
\neq
\text{Evaluation representation}
}
$$

---

## 12. Creating Lag Features Without Respecting Causality

Lag feature phải sử dụng thông tin đã tồn tại tại thời điểm prediction.

Nếu dự báo:

$$
\hat{y}_{t+H},
$$

thì feature tại $t$ chỉ được sử dụng:

$$
{x_t,x_{t-1},x_{t-2},\ldots}.
$$

Không được sử dụng:

$$
x_{t+1},x_{t+2},\ldots
$$

trong input.

Một lỗi tương tự xảy ra khi sử dụng centered rolling window:

$$
r_t=

\operatorname{mean}
(x_{t-w},\ldots,x_t,\ldots,x_{t+w}).
$$

Đây là representation không causal đối với forecasting.

Vì vậy:

$$
\boxed{
\text{Forecasting feature}
\Rightarrow
\text{causal construction}
}
$$

---

## 13. Ignoring Duplicate or Invalid Observations

Duplicate timestamps có thể dẫn đến:

$$
t_i=t_j,
\qquad i\neq j.
$$

Điều này làm cho một timestamp có nhiều observations và có thể gây ra:

* incorrect aggregation;
* ambiguous temporal ordering;
* duplicated information;
* incorrect window generation.

Tương tự, giá trị:

$$
NaN,\quad +\infty,\quad -\infty
$$

cần được kiểm tra trước khi đưa vào model.

Data validation tối thiểu nên đảm bảo:

$$
\forall x_i\in\mathcal{D},
\qquad
x_i\in\mathbb{R},
$$

và đối với timestamp:

$$
t_i\neq t_j
\quad
\text{unless duplicates are explicitly supported}.
$$

---

## 14. Using Test Data for Model or Method Selection

Test set phải được giữ độc lập cho đến khi quá trình lựa chọn model và preprocessing hoàn tất.

Một quy trình sai là:

$$
P_1,P_2,\ldots,P_K
\rightarrow
\text{evaluate on Test}
\rightarrow
\text{select best }P.
$$

Sau đó test set không còn là unbiased evaluation set.

Quy trình đúng:

$$
{P_1,\ldots,P_K}
\rightarrow
\text{Train/Validation}
\rightarrow
P^*
\rightarrow
\text{Test once}.
$$

Do đó:

$$
\boxed{
\text{Validation selects}
\qquad
\text{Test evaluates}
}
$$

Đây là nguyên tắc quan trọng để bảo đảm validity của empirical analysis.

---

## 15. Comparing Methods Under Different Experimental Conditions

Một preprocessing method không thể được so sánh công bằng nếu mỗi method được đánh giá bằng một experimental protocol khác nhau.

Ví dụ, nếu:

$$
P_1
\rightarrow
M_1
$$

và:

$$
P_2
\rightarrow
M_2,
$$

thì sự khác biệt về performance có thể đến từ model thay vì preprocessing.

Để isolate preprocessing effect, nên giữ cố định:

$$
\boxed{
\text{Dataset}
+
\text{Split}
+
\text{Model}
+
\text{Training Protocol}
+
\text{Metrics}
}
$$

và chỉ thay đổi preprocessing strategy.

Điều này đặc biệt quan trọng đối với empirical comparison trong Chapter 09.

---

## 16. Ignoring the Inverse Transformation

Một preprocessing transformation có thể thay đổi representation của dữ liệu nhưng không được phép làm mất khả năng diễn giải kết quả.

Nếu:

$$
z=T(x),
$$

thì cần biết liệu tồn tại:

$$
x=T^{-1}(z).
$$

Ví dụ:

$$
z=\frac{x-\mu}{\sigma}
$$

có inverse:

$$
x=\sigma z+\mu.
$$

Trong khi một số operations như aggressive dimensionality reduction hoặc lossy compression có thể không khôi phục chính xác dữ liệu ban đầu.

Do đó, cần xác định rõ:

$$
\text{reversible}
\quad\text{vs.}\quad
\text{irreversible transformation}.
$$

Điều này đặc biệt quan trọng khi model predictions phải được chuyển về original physical units.

---

## 17. Ignoring Computational Constraints

Một preprocessing strategy có thể hợp lý về mặt thống kê nhưng không phù hợp về mặt triển khai.

Ví dụ, với dataset lớn:

$$
N\gg 10^6,
$$

một transformation có complexity:

$$
O(NF^2)
$$

có thể trở nên đáng kể nếu $F$ lớn.

Trong edge/IoT systems, constraints còn nghiêm ngặt hơn:

$$
\text{Memory}
\downarrow,
\qquad
\text{CPU}
\downarrow,
\qquad
\text{Energy}
\downarrow.
$$

Vì vậy, method selection phải xem xét cả:

$$
C_{compute},
\quad
C_{memory},
\quad
C_{latency},
\quad
C_{energy}.
$$

Một phương pháp có accuracy cao hơn rất nhỏ nhưng computational cost lớn hơn nhiều có thể không phải lựa chọn tối ưu.

---

## 18. Failing to Version the Preprocessing Pipeline

Preprocessing configuration có thể thay đổi theo thời gian.

Ví dụ:

$$
P^{(1)}
\neq
P^{(2)}.
$$

Nếu không lưu version, rất khó xác định tại sao hai experiments sử dụng cùng dataset nhưng tạo ra kết quả khác nhau.

Một preprocessing artifact nên ghi nhận ít nhất:

* dataset version;
* preprocessing version;
* feature definitions;
* learned parameters;
* transformation order;
* configuration;
* random seed khi cần.

Có thể biểu diễn experiment artifact:

$$
A
=

(
D_v,P_v,\theta,M_v,E_v
).
$$

Điều này hỗ trợ reproducibility và auditability.

---

## 19. Reporting Only the Final Model Performance

Chỉ báo cáo:

$$
RMSE=...
$$

mà không mô tả preprocessing pipeline là chưa đủ để tái lập nghiên cứu.

Một experimental result cần cho biết:

$$
\text{Result}=

f(
\text{Dataset},
\text{Preprocessing},
\text{Split},
\text{Model},
\text{Training},
\text{Metric}
).
$$

Do đó, cần báo cáo ít nhất:

1. preprocessing methods;
2. method parameters;
3. train/validation/test protocol;
4. feature construction;
5. scaling strategy;
6. target transformation;
7. evaluation metrics.

Nếu thiếu các thông tin này, rất khó xác định performance improvement đến từ preprocessing hay từ một thay đổi khác trong experimental pipeline.

---

## 20. Common Mistakes as Failure Modes

Các lỗi trên có thể được tổng hợp thành một failure-mode framework:

| Failure mode                   | Consequence               |
| ------------------------------ | ------------------------- |
| Random temporal split          | Temporal leakage          |
| Fit scaler on full data        | Data leakage              |
| Future information in features | Look-ahead bias           |
| Automatic outlier removal      | Information loss          |
| Blind interpolation            | Artificial signal         |
| Excessive smoothing            | Loss of temporal dynamics |
| Uniform transformation         | Semantic distortion       |
| Excessive feature generation   | Redundancy and complexity |
| Test-driven method selection   | Optimistic evaluation     |
| Missing inverse transformation | Incorrect interpretation  |
| Uncontrolled pipeline changes  | Poor reproducibility      |
| Ignoring computational cost    | Deployment infeasibility  |

Các failure modes này cho thấy preprocessing errors thường không chỉ làm giảm data quality mà còn có thể làm **thay đổi validity của toàn bộ experimental conclusion**.

---

## 21. Prevention Principles

Để giảm các lỗi trên, preprocessing pipeline nên tuân thủ các nguyên tắc:

$$
\boxed{
\begin{aligned}
&\text{Validate before transforming}\\
&\text{Respect temporal ordering}\\
&\text{Fit learned transformations on Train only}\\
&\text{Construct features causally}\\
&\text{Preserve meaningful information}\\
&\text{Match methods to feature semantics}\\
&\text{Keep Test isolated}\\
&\text{Validate preprocessing empirically}\\
&\text{Track preprocessing versions}
\end{aligned}
}
$$

Một pipeline hợp lệ do đó không chỉ trả lời câu hỏi:

> *“Dữ liệu đã được xử lý chưa?”*

mà phải trả lời:

> *“Dữ liệu đã được xử lý đúng, không leakage, phù hợp với temporal structure và phù hợp với mục tiêu của mô hình hay chưa?”*

---

## 22. Summary

Các common mistakes trong time-series preprocessing chủ yếu xuất phát từ việc xem preprocessing như một chuỗi thao tác kỹ thuật độc lập thay vì một thành phần của experimental methodology.

Ba lỗi có mức độ ảnh hưởng đặc biệt nghiêm trọng là:

$$
\boxed{
\text{Temporal Leakage}
+
\text{Improper Transformation Fitting}
+
\text{Information Loss}
}
$$

Trong đó, temporal leakage và improper fitting có thể tạo ra performance estimates không hợp lệ, còn information loss có thể làm giảm khả năng biểu diễn các dynamics quan trọng của time series.

Vì vậy, một preprocessing pipeline đáng tin cậy cần duy trì:

$$
\boxed{
\text{Correctness}
+
\text{Causality}
+
\text{Leakage Control}
+
\text{Information Preservation}
+
\text{Reproducibility}
}
$$

Các nguyên tắc này hoàn thiện **Chapter 12 — Lessons Learned**:

* [12.1 Key Principles](01_key_principles.md) xác định các nguyên tắc nền tảng;
* [12.2 Method Selection](02_method_selection.md) xác định cách lựa chọn preprocessing methods;
* **12.3 Common Mistakes** xác định các failure modes cần tránh.

Do đó, Chapter 12 cung cấp một lớp nguyên tắc tổng hợp cho toàn bộ survey, kết nối taxonomy, empirical analysis, trade-offs và pipeline AI-ready thành một quy trình preprocessing có kiểm soát.

### Reference

[1] A. Tawakuli, B. Havers, V. M. Gulisano, D. Kaiser, and T. Engel, “Time-series data preprocessing: A survey and an empirical analysis,” *Journal of Engineering Research*, vol. 13, no. 2, pp. 674–711, 2025. DOI: 10.1016/j.jer.2024.02.018.
