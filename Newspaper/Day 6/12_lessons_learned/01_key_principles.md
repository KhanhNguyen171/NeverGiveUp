# 12.1 Key Principles

Data preprocessing for time-series data should be understood as a **model-independent data preparation process** whose objective is to convert raw observations into a representation that is sufficiently reliable, consistent, informative, and compatible with subsequent analytical or AI tasks. The survey by Tawakuli et al. emphasizes that preprocessing is not merely a technical requirement for satisfying model input formats; it can directly affect data quality, training efficiency, and predictive performance. At the same time, the absence of a single preprocessing strategy applicable to all time-series datasets makes the selection and ordering of preprocessing methods a central methodological issue. [1]

Trong phạm vi nghiên cứu này, các nguyên tắc cốt lõi được tổng hợp từ toàn bộ taxonomy, empirical analysis và pipeline preprocessing được trình bày ở các chương trước. Các nguyên tắc này không nhằm đưa ra một pipeline cố định cho mọi bài toán, mà cung cấp các tiêu chí để lựa chọn và kiểm soát preprocessing một cách có hệ thống.

## 1. Data Quality Is the Primary Objective

Nguyên tắc đầu tiên là **chất lượng dữ liệu phải được xem là mục tiêu nền tảng của preprocessing**. Một mô hình AI không thể bù đắp hoàn toàn cho dữ liệu có missing values, outliers, noise, timestamp không nhất quán hoặc các giá trị không hợp lệ. Vì vậy, preprocessing cần bắt đầu bằng việc xác định và xử lý các vấn đề về chất lượng dữ liệu trước khi thực hiện các phép biến đổi phụ thuộc vào dữ liệu.

Có thể biểu diễn quá trình này một cách khái quát:

$$
\mathcal{D}_{raw}
\xrightarrow{\text{quality assessment}}
\mathcal{D}_{clean}
\xrightarrow{\text{transformation}}
\mathcal{D}_{prepared}.
$$

Trong đó, $\mathcal{D}*{raw}$ là dữ liệu thu thập ban đầu, $\mathcal{D}*{clean}$ là dữ liệu sau khi xử lý các vấn đề về chất lượng, và $\mathcal{D}_{prepared}$ là dữ liệu đã sẵn sàng cho mô hình hoặc bước phân tích tiếp theo.

Điều này phù hợp với phạm vi của nghiên cứu gốc, trong đó preprocessing được xem là quá trình biến đổi dữ liệu thô thành dạng đầu vào phù hợp cho AI đồng thời cải thiện chất lượng dữ liệu và hiệu quả của quá trình học.

Do đó, **không nên lựa chọn preprocessing chỉ dựa trên khả năng cải thiện một metric của mô hình**. Một phương pháp chỉ làm tăng accuracy hoặc giảm RMSE trên một tập dữ liệu cụ thể nhưng làm mất cấu trúc thời gian hoặc tạo information leakage không thể được xem là một preprocessing strategy hợp lệ.

---

## 2. Preserve the Temporal Structure

Đối với time-series data, thứ tự thời gian là một phần của thông tin dữ liệu và phải được bảo toàn trong toàn bộ pipeline.

Cho chuỗi quan sát:

$$
\mathcal{X}=

\left \{
(t_i,\mathbf{x}_i)
\right \}_{i=1}^{N},
\qquad
t_1 \lt t_2 \lt \cdots \lt t_N,
$$

một phép preprocessing hợp lệ phải tránh làm mất hoặc thay đổi tùy tiện quan hệ thứ tự giữa các quan sát.

Nguyên tắc này đặc biệt quan trọng đối với:

* missing-data handling;
* temporal alignment;
* lag features;
* rolling statistics;
* decomposition;
* window construction;
* train/validation/test splitting.

Ví dụ, nếu một rolling feature được định nghĩa bởi:

$$
r_t=

\frac{1}{L}
\sum_{i=0}^{L-1}x_{t-i},
$$

thì $r_t$ chỉ được sử dụng các quan sát có timestamp không vượt quá $t$. Việc sử dụng $x_{t+1}$ hoặc các giá trị tương lai để xây dựng $r_t$ sẽ tạo **look-ahead bias**.

Do đó, preprocessing cho time series khác với preprocessing cho dữ liệu i.i.d. ở điểm quan trọng: **tính đúng đắn của temporal dependency phải được bảo toàn bên cạnh tính đúng đắn về mặt thống kê**.

---

## 3. Avoid Information Leakage

**Information leakage** là một trong những nguyên tắc quan trọng nhất của preprocessing cho machine learning. Mọi thống kê hoặc tham số được học từ dữ liệu phải chỉ được ước lượng trên tập training và sau đó áp dụng cho validation/test.

Giả sử tập dữ liệu được chia thành:

$$
\mathcal{D}=

\mathcal{D}_{train}
\cup
\mathcal{D}_{val}
\cup
\mathcal{D}_{test}.
$$

Với một transformation có tham số $\theta$, nguyên tắc đúng là:

$$
\theta=

f(\mathcal{D}_{train}),
$$

sau đó:

$$
\mathcal{D}'_{train}=

T(\mathcal{D}_{train};\theta),
$$

$$
\mathcal{D}'_{val}=

T(\mathcal{D}_{val};\theta),
$$

và

$$
\mathcal{D}'_{test}=

T(\mathcal{D}_{test};\theta).
$$

Không được ước lượng:

$$
\theta=f(\mathcal{D}_{train}\cup\mathcal{D}_{val})
$$

hoặc

$$
\theta=f(\mathcal{D}_{train}\cup\mathcal{D}_{val}\cup\mathcal{D}_{test}).
$$

Nguyên tắc này áp dụng không chỉ cho scaling mà còn cho imputation, feature selection, dimensionality reduction và các transformation có tham số. Đối với time series, data splitting cũng phải tôn trọng temporal ordering thay vì mặc định sử dụng random shuffling. Các preprocessing pipeline hiện đại cũng nhấn mạnh rằng các transformation phụ thuộc dữ liệu phải được fit trên training partition để tránh leakage.

---

## 4. Preprocessing Must Be Task-Dependent

Không tồn tại một preprocessing pipeline tối ưu cho mọi time-series task.

Hiệu quả của một phương pháp phụ thuộc vào:

* loại dữ liệu;
* sampling frequency;
* mức độ noise;
* missingness mechanism;
* temporal dependency;
* distribution của biến;
* mục tiêu dự báo hoặc phân loại;
* loại mô hình;
* yêu cầu về interpretability;
* tài nguyên tính toán.

Do đó, lựa chọn preprocessing nên được mô hình hóa như một bài toán ra quyết định:

$$
P^*=

\arg\max_{P\in\mathcal{P}}
\mathcal{U}(P;\mathcal{D},\mathcal{T},\mathcal{M},\mathcal{C}),
$$

trong đó:

* $\mathcal{P}$ là tập các preprocessing strategies;
* $\mathcal{D}$ là dataset;
* $\mathcal{T}$ là task;
* $\mathcal{M}$ là model;
* $\mathcal{C}$ là các constraint về computational resources và domain;
* $\mathcal{U}$ là utility của preprocessing strategy.

Vì vậy, một phương pháp không nên được đánh giá đơn độc theo giả định rằng nó luôn "tốt hơn". Chính empirical analysis của nghiên cứu gốc cũng tập trung vào việc đánh giá ảnh hưởng của các preprocessing techniques đối với cả data quality và AI performance thay vì giả định trước một phương pháp tối ưu duy nhất.

---

## 5. Preserve Information Whenever Possible

Preprocessing nên **giảm các thành phần không mong muốn nhưng hạn chế tối đa việc loại bỏ thông tin hữu ích**.

Có thể biểu diễn nguyên tắc này dưới dạng:

$$
\text{Useful information}
;\gg;
\text{unnecessary variation}.
$$

Ví dụ, outlier không mặc nhiên là lỗi. Một giá trị cực đoan có thể biểu diễn:

* sensor failure;
* transmission error;
* hoặc một sự kiện thực tế bất thường.

Do đó, việc phát hiện outlier và việc loại bỏ outlier là hai quyết định khác nhau.

Tương tự, smoothing hoặc denoising có thể làm giảm noise nhưng đồng thời làm mất các biến động ngắn hạn có ý nghĩa. Vì vậy, preprocessing phải phân biệt giữa **noise cần loại bỏ** và **signal cần được bảo toàn**.

Nguyên tắc này đặc biệt quan trọng đối với time-series data vì temporal patterns, abrupt changes, periodicity và local dynamics đều có thể mang thông tin dự báo.

---

## 6. Maintain Statistical and Semantic Consistency

Sau preprocessing, dữ liệu phải duy trì tính nhất quán cả về mặt thống kê và ý nghĩa của biến.

Với một feature $x_j$, transformation:

$$
z_j=T_j(x_j)
$$

chỉ nên được áp dụng nếu transformation đó phù hợp với đặc tính của biến và mục tiêu của mô hình.

Ví dụ:

* Standardization phù hợp khi cần đưa các feature về scale tương đồng;
* logarithmic transformation có thể phù hợp với dữ liệu lệch phải;
* cyclic encoding phù hợp với các biến thời gian tuần hoàn;
* differencing có thể được sử dụng khi cần loại bỏ một phần non-stationarity.

Không nên áp dụng cùng một transformation cho mọi feature chỉ vì tính đơn giản của pipeline.

Đặc biệt, các biến categorical, binary, cyclic và continuous có thể yêu cầu các chiến lược preprocessing khác nhau. Vì vậy, preprocessing cần xem xét **semantic type** của từng feature thay vì chỉ dựa vào kiểu dữ liệu lưu trữ.

---

## 7. Preprocessing Order Matters

Các preprocessing operations không phải lúc nào cũng giao hoán. Thứ tự thực hiện có thể ảnh hưởng trực tiếp đến kết quả cuối cùng.

Một pipeline tổng quát có thể được tổ chức như sau:

$$
\boxed{
\text{Data Validation}
\rightarrow
\text{Cleaning}
\rightarrow
\text{Transformation}
\rightarrow
\text{Feature Engineering}
\rightarrow
\text{Feature Selection}
\rightarrow
\text{Model Input}
}
$$

Tuy nhiên, thứ tự cụ thể phải phụ thuộc vào task và dependency giữa các operations.

Ví dụ, nếu scaling được thực hiện trước khi xử lý một missing-value mechanism phụ thuộc vào distribution, thì các thống kê scaling có thể bị ảnh hưởng. Tương tự, feature selection hoặc dimensionality reduction trước khi xử lý leakage có thể làm cho toàn bộ pipeline không còn đáng tin cậy.

Do đó, preprocessing nên được thiết kế như một **dependency-aware pipeline**, trong đó mỗi bước có input, output và assumptions rõ ràng.

---

## 8. Feature Engineering Should Encode Temporal Information

Feature engineering không đơn thuần là tăng số lượng feature. Mục tiêu là tạo ra representation giúp mô hình khai thác các cấu trúc vốn có trong time series.

Một time series có thể chứa:

$$
\text{Trend}
+
\text{Seasonality}
+
\text{Autocorrelation}
+
\text{Exogenous effects}
+
\text{Noise}.
$$

Các feature như lag, rolling statistics và temporal encoding có thể biểu diễn một phần các cấu trúc này.

Ví dụ, lag feature:

$$
x_{t-k}
$$

cung cấp thông tin về trạng thái của hệ thống tại thời điểm $k$ bước trước.

Temporal cyclic encoding có thể biểu diễn hour-of-day bằng:

$$
x_{\sin}=

\sin\left(
2\pi\frac{h}{P}
\right),
$$

$$
x_{\cos}=

\cos\left(
2\pi\frac{h}{P}
\right),
$$

trong đó $P$ là chu kỳ.

Do đó, feature engineering nên được đánh giá dựa trên **information content và temporal relevance**, không phải chỉ dựa trên số lượng feature được tạo ra.

---

## 9. Complexity Must Be Justified by Benefit

Một preprocessing method phức tạp hơn không mặc nhiên tốt hơn.

Có thể xem quyết định lựa chọn phương pháp dưới dạng trade-off:

$$
\text{Net Utility}=

\text{Predictive Benefit}

\lambda_1\text{Computational Cost}

\lambda_2\text{Complexity}

\lambda_3\text{Risk}.
$$

Trong đó, risk có thể bao gồm leakage, instability hoặc loss of interpretability.

Nguyên tắc này đặc biệt quan trọng khi triển khai preprocessing trên edge hoặc IoT. Nghiên cứu gốc cũng xem xét khả năng phân phối preprocessing tới edge nhằm giảm tải cho hệ thống trung tâm, giảm tài nguyên tiêu thụ và hỗ trợ EdgeAI.

Vì vậy, trong môi trường hạn chế tài nguyên, một phương pháp đơn giản nhưng ổn định có thể phù hợp hơn một phương pháp phức tạp với chi phí tính toán cao.

---

## 10. Reproducibility Is a Requirement

Một preprocessing pipeline khoa học phải có khả năng tái lập.

Với cùng:

$$
(\mathcal{D},P,\theta,\mathcal{V}),
$$

trong đó:

* $\mathcal{D}$ là dữ liệu;
* $P$ là preprocessing pipeline;
* $\theta$ là các learned parameters;
* $\mathcal{V}$ là version/configuration,

kết quả preprocessing phải có thể được tái tạo một cách nhất quán.

Do đó cần lưu giữ:

* preprocessing configuration;
* transformation parameters;
* feature definitions;
* dataset version;
* timestamp và sampling information;
* random seeds khi cần;
* thứ tự các preprocessing operations.

Điều này chuyển preprocessing từ một chuỗi thao tác ad-hoc thành một **reproducible computational artifact**.

---

## 11. Evaluate Preprocessing Empirically

Preprocessing không nên được đánh giá chỉ dựa trên trực giác hoặc giả định lý thuyết. Mỗi transformation cần được đánh giá trên ít nhất hai khía cạnh:

$$
\text{Evaluation}=

\text{Data Quality}
+
\text{Model Performance}.
$$

**Data-quality evaluation** có thể xem xét:

* missingness;
* outlier rate;
* distribution;
* temporal consistency;
* noise level;
* redundancy.

**Model-level evaluation** có thể xem xét:

* MAE;
* RMSE;
* $R^2$;
* classification metrics;
* training efficiency;
* computational cost.

Cách tiếp cận này phù hợp với empirical component của nghiên cứu gốc, trong đó tác giả đánh giá tác động của preprocessing techniques không chỉ đối với chất lượng dữ liệu mà còn đối với hiệu năng của AI algorithms.

Một preprocessing method chỉ nên được xem là có giá trị khi lợi ích của nó được chứng minh trong bối cảnh task cụ thể.

---

## 12. Use the Simplest Valid Pipeline

Từ các nguyên tắc trên, có thể rút ra một nguyên tắc tổng hợp:

> **Chọn preprocessing pipeline đơn giản nhất nhưng vẫn đủ để đáp ứng yêu cầu về data quality, temporal integrity và model compatibility.**

Điều này có nghĩa là không nên:

* áp dụng transformation không có mục đích;
* tạo feature chỉ để tăng dimensionality;
* loại bỏ outlier mà không kiểm tra semantic meaning;
* sử dụng interpolation khi cơ chế missingness không phù hợp;
* áp dụng scaling mà không xem xét loại feature;
* sử dụng một pipeline phức tạp chỉ vì nó tạo ra kết quả tốt trên một experiment duy nhất.

Một pipeline tốt phải đạt được sự cân bằng giữa **data quality, information preservation, predictive utility, computational efficiency và reproducibility**.

---

## 13. Consolidated Principles

Các nguyên tắc của preprocessing cho time-series data có thể được tổng hợp thành một framework gồm sáu yêu cầu chính:

$$
\boxed{
\text{Valid}
+
\text{Temporal}
+
\text{Leakage-free}
+
\text{Informative}
+
\text{Efficient}
+
\text{Reproducible}
}
$$

Trong đó:

| Principle                        | Mục tiêu                                                           |
| -------------------------------- | ------------------------------------------------------------------ |
| **Data Quality**                 | Loại bỏ hoặc điều chỉnh các vấn đề làm suy giảm chất lượng dữ liệu |
| **Temporal Integrity**           | Bảo toàn thứ tự và dependency theo thời gian                       |
| **Leakage Control**              | Ngăn thông tin từ validation/test ảnh hưởng đến training           |
| **Information Preservation**     | Giảm noise và redundancy nhưng giữ signal có ý nghĩa               |
| **Task-aware Selection**         | Chọn phương pháp dựa trên dataset, task và model                   |
| **Efficiency & Reproducibility** | Kiểm soát chi phí và bảo đảm pipeline có thể tái lập               |

Những nguyên tắc này tạo cầu nối giữa taxonomy ở **Chương 02**, các nhóm preprocessing cụ thể ở **Chương 03–08**, empirical analysis ở **Chương 09**, và các trade-off ở **Chương 10**. Chúng cũng là cơ sở để xây dựng pipeline AI-ready được trình bày trong **Chương 11** và pipeline thực nghiệm trên UCI Appliances ở **Chương 13**.

Do đó, preprocessing nên được xem không phải là một tập hợp các kỹ thuật độc lập, mà là **một hệ thống các quyết định có ràng buộc**, trong đó mỗi transformation phải có mục đích rõ ràng, phù hợp với cấu trúc time series, không gây leakage và được kiểm chứng bằng thực nghiệm.

### Reference

[1] A. Tawakuli, B. Havers, V. M. Gulisano, D. Kaiser, and T. Engel, “Survey: Time-series data preprocessing: A survey and an empirical analysis,” *Journal of Engineering Research*, vol. 13, no. 2, pp. 674–711, 2025. DOI: 10.1016/j.jer.2024.02.018.
