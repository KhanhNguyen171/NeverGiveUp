# Findings

## 1. Mục tiêu

Phần này tổng hợp các phát hiện chính từ empirical analysis về ảnh hưởng của preprocessing đối với numerical time-series data.

Mục tiêu không phải xác định một preprocessing method duy nhất là tốt nhất, mà xác định mối quan hệ giữa:

$$
\boxed{
\text{Data Characteristics}
\rightarrow
\text{Preprocessing Choice}
\rightarrow
\text{Data Representation}
\rightarrow
\text{Model Performance}
}
$$

Các findings được rút ra từ kết quả ở [05_results.md](05_results.md) và được sử dụng làm cơ sở cho phần so sánh, trade-off và limitations trong [Chương 10](../10_discussion/01_comparison.md).

---

## 2. Finding 1 — Preprocessing là một thành phần của toàn bộ ML pipeline

Kết quả cho thấy preprocessing không nên được xem là bước độc lập nằm trước modeling. Thay đổi preprocessing làm thay đổi representation của dữ liệu đầu vào và do đó có thể làm thay đổi quá trình học của mô hình:

$$
\mathbf{X}
\xrightarrow{P_1}
\mathbf{X}^{(1)}
\xrightarrow{f_\theta}
\widehat{\mathbf{y}}^{(1)},
$$

trong khi một pipeline khác có thể tạo:

$$
\mathbf{X}
\xrightarrow{P_2}
\mathbf{X}^{(2)}
\xrightarrow{f_\theta}
\widehat{\mathbf{y}}^{(2)}.
$$

Mặc dù mô hình và dữ liệu gốc giống nhau, $\mathbf{X}^{(1)}$ và $\mathbf{X}^{(2)}$ có thể chứa thông tin dưới những representation khác nhau.

Do đó:

$$
P_1\neq P_2
\quad\Rightarrow\quad
\widehat{\mathbf{y}}^{(1)}
\neq
\widehat{\mathbf{y}}^{(2)}.
$$

**Finding:** preprocessing cần được đánh giá như một thành phần của pipeline học máy thay vì chỉ được xem là bước chuẩn bị dữ liệu.

---

## 3. Finding 2 — Không có preprocessing method tối ưu cho mọi dataset

Một kết luận quan trọng là hiệu quả của preprocessing phụ thuộc vào đặc điểm của dữ liệu.

Có thể biểu diễn configuration tối ưu dưới dạng:

$$
P^{*}=

P^{*}
(
\mathcal{D},
\mathcal{T},
f_\theta
),
$$

trong đó:

* $\mathcal{D}$: dataset;
* $\mathcal{T}$: task;
* $f_\theta$: model.

Ví dụ, scaling có thể đặc biệt hữu ích đối với các thuật toán nhạy với feature magnitude, trong khi tác động có thể nhỏ hơn đối với một số tree-based models.

Tương tự, smoothing có thể có lợi khi noise chiếm tỷ trọng lớn nhưng có thể gây mất thông tin khi chuỗi chứa nhiều biến động ngắn hạn có ý nghĩa.

**Finding:** preprocessing phải được lựa chọn theo **data characteristics và downstream task**, không nên áp dụng một pipeline cố định cho mọi time series.

---

## 4. Finding 3 — Data cleaning cải thiện tính hợp lệ nhưng không đảm bảo tăng prediction performance

Cleaning giải quyết các vấn đề như:

$$
\text{Missing Values},
\quad
\text{Outliers},
\quad
\text{Noise}.
$$

Tuy nhiên:

$$
\text{Higher Data Quality}
\not\Rightarrow
\text{Higher Predictive Performance}.
$$

Ví dụ, một outlier có thể là lỗi đo:

$$
x_t\in\mathcal{O}_{\mathrm{error}},
$$

nhưng cũng có thể là một sự kiện thực tế:

$$
x_t\in\mathcal{O}_{\mathrm{valid}}.
$$

Nếu loại bỏ trường hợp thứ hai, preprocessing có thể làm dữ liệu "sạch" hơn theo tiêu chí thống kê nhưng đồng thời loại bỏ predictive signal.

**Finding:** data cleaning cần phân biệt giữa **measurement error** và **informative extreme event**.

---

## 5. Finding 4 — Missing-value handling phải bảo toàn temporal structure

Đối với time series, missing values không chỉ là vấn đề thiếu một giá trị trong bảng dữ liệu mà còn liên quan đến temporal continuity.

Với:

$$
x_{t-1},
\quad
x_t=\mathrm{missing},
\quad
x_{t+1},
$$

giá trị thay thế $\widehat{x}_t$ nên được lựa chọn dựa trên cấu trúc lân cận khi điều đó phù hợp.

Interpolation có dạng:

$$
\widehat{x}_t=

x_{t-1}
+
\frac{t-(t-1)}
{(t+1)-(t-1)}
(x_{t+1}-x_{t-1}).
$$

Ngược lại, deletion có thể tạo ra:

$$
\Delta t

\gt

\Delta t_{\mathrm{expected}},
$$

làm phá vỡ temporal continuity.

**Finding:** đối với time series, đánh giá missing-value method cần xem xét cả **data completeness** và **temporal consistency**, không chỉ tỷ lệ missing values sau preprocessing.

---

## 6. Finding 5 — Outlier handling tồn tại trade-off giữa robustness và information preservation

Extreme values có thể làm tăng prediction error:

$$
e_t=

y_t-\widehat{y}_t,
$$

đặc biệt khi metric sử dụng bình phương sai số như RMSE:

$$
\mathrm{RMSE}=

\sqrt{
\frac{1}{N}
\sum_t e_t^2
}.
$$

Do đó, loại bỏ một số outliers có thể làm giảm RMSE.

Tuy nhiên, nếu các outliers tương ứng với những sự kiện thực tế, việc loại bỏ chúng làm giảm khả năng mô hình học các trạng thái bất thường.

Vì vậy:

$$
\text{Outlier Handling}=

\text{Robustness}
\leftrightarrow
\text{Signal Preservation}.
$$

**Finding:** outlier detection và outlier removal phải được xem là hai quyết định khác nhau.

---

## 7. Finding 6 — Noise reduction có hiệu quả phụ thuộc vào mức độ và đặc tính của noise

Giả sử:

$$
x_t=s_t+\epsilon_t.
$$

Smoothing tìm cách ước lượng:

$$
\widehat{s}_t
\approx
s_t.
$$

Khi $\epsilon_t$ có tính chất ngẫu nhiên và không mang predictive information, giảm noise có thể tạo representation ổn định hơn.

Nhưng khi cửa sổ smoothing tăng:

$$
w\uparrow,
$$

variance của tín hiệu sau smoothing có xu hướng giảm, đồng thời các biến động nhanh cũng có thể bị loại bỏ.

Do đó tồn tại một trade-off:

$$
\boxed{
\text{Noise Suppression}
\leftrightarrow
\text{Temporal Detail}
}
$$

**Finding:** smoothing không nên được tối ưu chỉ theo độ mượt của chuỗi; tiêu chí quan trọng hơn là khả năng bảo toàn predictive signal.

---

## 8. Finding 7 — Scaling phụ thuộc vào mô hình

Scaling thay đổi numerical range:

$$
x'
==

\frac{x-\mu}{\sigma},
$$

nhưng không nhất thiết làm thay đổi information content của dữ liệu.

Tác động của scaling phụ thuộc vào cơ chế học của mô hình.

Đối với các phương pháp dựa trên khoảng cách hoặc gradient optimization, scale của feature có thể ảnh hưởng đáng kể đến:

$$
|\mathbf{x}_i-\mathbf{x}_j|
$$

hoặc gradient của objective function.

Ngược lại, một số tree-based methods ít phụ thuộc vào monotonic scaling.

**Finding:** scaling nên được xem là **model-dependent preprocessing**, không phải bước bắt buộc cho mọi thuật toán.

---

## 9. Finding 8 — Feature engineering có thể chuyển temporal information thành explicit representation

Time series chứa information không chỉ trong giá trị hiện tại mà còn trong lịch sử:

$$
x_t
\leftarrow
{x_{t-1},x_{t-2},\ldots}.
$$

Lag features biểu diễn trực tiếp dependency này:

$$
\mathbf{f}_t^{\mathrm{lag}}=

[
x_{t-1},
\ldots,
x_{t-K}
].
$$

Rolling features bổ sung thông tin về trạng thái cục bộ:

$$
\mathbf{f}_t^{\mathrm{rolling}}=

[
\mu_t^{(w)},
\sigma_t^{(w)},
\ldots
].
$$

Điều này đặc biệt hữu ích đối với các mô hình không tự động biểu diễn temporal dependency.

Tuy nhiên:

$$
d_{\mathrm{engineered}}

\gt

d_{\mathrm{raw}}
$$

có thể dẫn đến tăng computational cost và redundancy.

**Finding:** feature engineering có thể làm tăng predictive information nhưng cần kết hợp với feature selection hoặc dimensionality reduction khi số lượng đặc trưng tăng mạnh.

---

## 10. Finding 9 — Feature selection không nhất thiết làm giảm prediction performance

Feature selection tìm:

$$
\mathcal{F}^{*}
\subseteq
\mathcal{F}.
$$

Nếu các feature bị loại bỏ chủ yếu là redundant hoặc noisy:

$$
I(\mathcal{F}_{\mathrm{removed}};Y)
\approx0,
$$

thì việc giảm số feature có thể không làm giảm prediction performance.

Trong trường hợp tốt hơn:

$$
\mathrm{RMSE}*{\mathrm{selected}}
\lt
\mathrm{RMSE}*{\mathrm{full}}.
$$

Điều này có thể xảy ra khi loại bỏ feature không hữu ích giúp mô hình giảm overfitting hoặc giảm complexity.

**Finding:** feature selection có thể đồng thời đạt hai mục tiêu:

$$
\boxed{
\text{Dimensionality Reduction}
+
\text{Generalization Improvement}
}
$$

nhưng hiệu quả phụ thuộc vào phương pháp selection và dataset.

---

## 11. Finding 10 — Dimensionality reduction có trade-off rõ ràng với information preservation

Dimensionality reduction biến đổi:

$$
\mathbf{X}\in\mathbb{R}^{N\times d}
$$

thành:

$$
\mathbf{Z}\in\mathbb{R}^{N\times k},
\qquad
k \lt d.
$$

Lợi ích trực tiếp là giảm complexity:

$$
d\downarrow
\quad\Rightarrow\quad
\text{representation complexity}\downarrow.
$$

Tuy nhiên, khi $k$ giảm quá mạnh, information có thể bị mất.

Đối với PCA:

$$
EVR_k=

\frac{\sum_{i=1}^{k}\lambda_i}
{\sum_{j=1}^{d}\lambda_j}.
$$

Do đó cần cân bằng:

$$
\boxed{
\text{Dimension Reduction}
\leftrightarrow
\text{Information Preservation}
}
$$

**Finding:** giảm số chiều không phải mục tiêu tự thân; giá trị của dimensionality reduction phải được đánh giá cùng predictive performance và amount of retained information.

---

## 12. Finding 11 — Preprocessing có thể cải thiện model performance nhưng làm tăng computational cost

Một preprocessing method có thể tạo:

$$
\mathrm{RMSE}\downarrow
$$

nhưng đồng thời:

$$
T_{\mathrm{prep}}\uparrow.
$$

Feature engineering có thể làm:

$$
d\uparrow,
$$

trong khi dimensionality reduction có thể làm:

$$
d\downarrow
$$

nhưng lại yêu cầu thêm bước optimization hoặc transformation.

Do đó, lựa chọn preprocessing phải xem xét:

$$
\boxed{
\text{Accuracy}
\leftrightarrow
\text{Efficiency}
}
$$

Đặc biệt trong các hệ thống resource-constrained, computational cost có thể trở thành một constraint thay vì chỉ là một metric phụ.

---

## 13. Finding 12 — Data quality và predictive performance không phải hai đại lượng đồng nhất

Một trong những phát hiện quan trọng là:

$$
\text{Data Quality}
\neq
\text{Predictive Utility}.
$$

Một transformation có thể làm:

$$
Q(\mathbf{X}')

\gt

Q(\mathbf{X})
$$

theo một tiêu chí thống kê, nhưng:

$$
M(\mathbf{X}')
\leq
M(\mathbf{X}).
$$

Ngược lại, một representation có thể không tối ưu theo các thống kê mô tả truyền thống nhưng lại phù hợp hơn với objective của mô hình.

Điều này cho thấy preprocessing phải được đánh giá trong mối quan hệ với **downstream task**.

**Finding:** mục tiêu cuối cùng không phải tạo ra dữ liệu "đẹp" nhất mà là tạo ra representation phù hợp nhất với nhiệm vụ học máy trong khi bảo toàn thông tin có ý nghĩa.

---

## 14. Finding 13 — Data leakage có thể làm sai lệch toàn bộ empirical comparison

Nếu preprocessing được fit trên toàn bộ dataset:

$$
P
=

\operatorname{fit}
(\mathcal{D}*{\mathrm{train}}
\cup
\mathcal{D}*{\mathrm{val}}
\cup
\mathcal{D}_{\mathrm{test}}),
$$

thì thông tin từ validation và test có thể ảnh hưởng đến representation của training data.

Khi đó:

$$
\widehat{M}*{\mathrm{test}}
\lt
M*{\mathrm{true}}
$$

có thể xảy ra theo nghĩa kết quả đánh giá trở nên quá lạc quan.

Do đó, protocol đúng phải là:

$$
P_{\mathrm{train}}=

\operatorname{fit}
(\mathcal{D}_{\mathrm{train}})
$$

và:

$$
\mathcal{D}_{\mathrm{val}}'=

P_{\mathrm{train}}(\mathcal{D}_{\mathrm{val}}),
$$

$$
\mathcal{D}_{\mathrm{test}}'=

P_{\mathrm{train}}(\mathcal{D}_{\mathrm{test}}).
$$

**Finding:** kiểm soát data leakage là điều kiện tiên quyết để comparison giữa các preprocessing methods có giá trị khoa học.

---

## 15. Finding 14 — Temporal ordering phải được bảo toàn

Đối với time-series:

$$
t_1 \lt t_2 \lt \cdots \lt t_N.
$$

Nếu random shuffle được sử dụng trước khi train/validation/test split, các quan sát trong tương lai có thể xuất hiện trong training set.

Điều này phá vỡ giả định forecasting:

$$
\text{Past}
\rightarrow
\text{Future}.
$$

Chronological split duy trì:

$$
\mathcal{D}*{\mathrm{train}}
\prec
\mathcal{D}*{\mathrm{val}}
\prec
\mathcal{D}_{\mathrm{test}}.
$$

**Finding:** temporal validation không chỉ là lựa chọn triển khai mà là một yêu cầu phương pháp luận đối với empirical analysis của time-series preprocessing.

---

## 16. Finding 15 — Không thể đánh giá preprocessing chỉ bằng một metric

MAE, RMSE và $R^2$ phản ánh các khía cạnh khác nhau:

$$
\mathrm{MAE}\rightarrow
\text{average absolute error},
$$

$$
\mathrm{RMSE}\rightarrow
\text{large-error sensitivity},
$$

$$
R^2\rightarrow
\text{explained variation}.
$$

Một configuration có thể đạt:

$$
\mathrm{MAE}\downarrow
$$

nhưng:

$$
\mathrm{RMSE}\uparrow,
$$

cho thấy average error giảm nhưng một số prediction errors lớn hơn.

Do đó, việc sử dụng nhiều metrics cung cấp đánh giá toàn diện hơn.

**Finding:** empirical comparison nên sử dụng một metric chính để lựa chọn configuration và các metric bổ sung để kiểm tra robustness của kết luận.

---

## 17. Tổng hợp các findings

Các findings chính có thể được tổng hợp thành:

| Finding | Kết luận                                                                       |
| ------- | ------------------------------------------------------------------------------ |
| F1      | Preprocessing là thành phần của ML pipeline                                    |
| F2      | Không có method tối ưu cho mọi dataset                                         |
| F3      | Data cleaning không đảm bảo tăng predictive performance                        |
| F4      | Imputation phải bảo toàn temporal structure                                    |
| F5      | Outlier handling có trade-off giữa robustness và signal                        |
| F6      | Noise reduction phải cân bằng smoothing và temporal detail                     |
| F7      | Scaling phụ thuộc vào model                                                    |
| F8      | Feature engineering giúp biểu diễn temporal information                        |
| F9      | Feature selection có thể giảm dimension mà vẫn giữ performance                 |
| F10     | Dimensionality reduction phải cân bằng compression và information preservation |
| F11     | Prediction improvement có thể đi kèm computational cost                        |
| F12     | Data quality không đồng nhất với predictive utility                            |
| F13     | Data leakage có thể làm sai lệch comparison                                    |
| F14     | Temporal ordering phải được bảo toàn                                           |
| F15     | Cần sử dụng nhiều metrics để đánh giá                                          |

Các findings này cho thấy preprocessing nên được xem là một **decision problem** thay vì một chuỗi thao tác cố định.

---

## 18. Nguyên tắc lựa chọn preprocessing

Từ empirical analysis, có thể khái quát quy trình lựa chọn:

$$
\boxed{
\text{Identify Data Problem}
\rightarrow
\text{Select Candidate Method}
\rightarrow
\text{Validate}
\rightarrow
\text{Measure Trade-off}
\rightarrow
\text{Select Configuration}
}
$$

Cụ thể:

### Bước 1 — Xác định vấn đề dữ liệu

$$
\mathcal{D}
\rightarrow
{
\text{Missing},
\text{Outlier},
\text{Noise},
\text{Scale},
\text{Redundancy}
}.
$$

### Bước 2 — Chọn preprocessing phù hợp

$$
\text{Data Problem}
\rightarrow
P.
$$

### Bước 3 — Đánh giá trên validation

$$
P
\rightarrow
f_\theta
\rightarrow
M_{\mathrm{val}}.
$$

### Bước 4 — Đánh giá trade-off

$$
M_{\mathrm{val}}
+
d
+
T_{\mathrm{prep}}
+
\text{information preservation}.
$$

### Bước 5 — Đánh giá cuối cùng

Configuration được chọn được cố định trước khi sử dụng test set:

$$
P^*
\rightarrow
\mathcal{D}_{\mathrm{test}}
\rightarrow
{
\mathrm{MAE},
\mathrm{RMSE},
R^2
}.
$$

---

## 19. Implications for the Survey

Các findings trên củng cố taxonomy được xây dựng trong [02_taxonomy.md](../02_overview/02_taxonomy.md).

Thay vì xem preprocessing như:

$$
P=P_1\circ P_2\circ\cdots\circ P_k
$$

với thứ tự cố định cho mọi dataset, survey đề xuất cách nhìn:

$$
P^{*}=

P^{*}
(
\text{Data Characteristics},
\text{Task},
\text{Model},
\text{Constraints}
).
$$

Điều này dẫn đến một nguyên tắc tổng quát:

> **Preprocessing should be task-aware, data-dependent, and leakage-safe.**

Nói cách khác, một preprocessing pipeline tốt cần đồng thời:

$$
\boxed{
\text{Data Quality}
+
\text{Task Relevance}
+
\text{Model Compatibility}
+
\text{Leakage Prevention}
}.
$$

---

## 20. Liên kết với Chương 10

Các findings của chương này là cơ sở trực tiếp cho phần discussion.

[01_comparison.md](../10_discussion/01_comparison.md) sẽ so sánh ưu điểm và hạn chế của các nhóm preprocessing.

[02_tradeoffs.md](../10_discussion/02_tradeoffs.md) sẽ phân tích sâu các trade-off:

$$
\text{Accuracy}
\leftrightarrow
\text{Complexity}
\leftrightarrow
\text{Information Preservation}.
$$

[03_limitations.md](../10_discussion/03_limitations.md) sẽ thảo luận giới hạn về dataset, experimental setup, generalization và khả năng ngoại suy kết quả.

Như vậy, Chương 9 hoàn thành chuỗi phân tích:

$$
\boxed{
\text{Experimental Setup}
\rightarrow
\text{Dataset}
\rightarrow
\text{Preprocessing}
\rightarrow
\text{Metrics}
\rightarrow
\text{Results}
\rightarrow
\text{Findings}
}
$$

và tạo cầu nối từ empirical evidence sang phần discussion và kết luận của toàn bộ survey.
