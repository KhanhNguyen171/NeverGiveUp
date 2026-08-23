# So sánh các phương pháp tiền xử lý dữ liệu chuỗi thời gian

Các phương pháp tiền xử lý dữ liệu chuỗi thời gian không có một lựa chọn tối ưu cho mọi bài toán. Hiệu quả của một phương pháp phụ thuộc vào đặc trưng của dữ liệu, loại vấn đề cần xử lý, mục tiêu phân tích và mô hình học máy hoặc học sâu ở bước tiếp theo. Tawakuli et al. [1] tổ chức các kỹ thuật tiền xử lý chuỗi thời gian theo nhiều nhóm, đồng thời thực hiện đánh giá thực nghiệm nhằm phân tích ảnh hưởng của chúng đến chất lượng dữ liệu và hiệu năng của các thuật toán AI.

Trong phạm vi nghiên cứu này, việc so sánh tập trung vào các nhóm phương pháp đã trình bày trong [03_data_cleaning](../03_data_cleaning/), [04_data_transformation](../04_data_transformation/), [05_feature_engineering](../05_feature_engineering/), [06_feature_selection](../06_feature_selection/), [07_sensor_fusion](../07_sensor_fusion/) và [08_data_compression](../08_data_compression/). Mục tiêu không phải xác định một thuật toán tốt nhất tuyệt đối, mà xác định **điều kiện sử dụng, ưu điểm, hạn chế và sự đánh đổi** của từng nhóm phương pháp trong một pipeline tiền xử lý chuỗi thời gian.

## 1. Tiêu chí so sánh

Có thể biểu diễn một pipeline tiền xử lý tổng quát dưới dạng

$$
\mathcal{D}*{raw}
\xrightarrow{\mathcal{P}}
\mathcal{D}*{clean}
\xrightarrow{\mathcal{T}}
\mathcal{D}*{transformed}
\xrightarrow{\mathcal{F}}
\mathcal{D}*{feature}
\xrightarrow{\mathcal{S}}
\mathcal{D}_{AI},
$$

trong đó $\mathcal{P}$ biểu diễn các phép làm sạch dữ liệu, $\mathcal{T}$ biểu diễn biến đổi dữ liệu, $\mathcal{F}$ biểu diễn xây dựng đặc trưng và $\mathcal{S}$ biểu diễn lựa chọn hoặc giảm chiều đặc trưng.

Các phương pháp được đánh giá theo năm tiêu chí chính:

1. **Data quality**: khả năng cải thiện tính đầy đủ, nhất quán và độ tin cậy của dữ liệu.
2. **Information preservation**: mức độ bảo toàn thông tin thời gian và quan hệ thống kê ban đầu.
3. **Computational cost**: chi phí thời gian, bộ nhớ và tài nguyên tính toán.
4. **Model compatibility**: mức độ phù hợp với các mô hình AI downstream.
5. **Deployment suitability**: khả năng triển khai trong môi trường hạn chế tài nguyên, đặc biệt là Edge/IoT.

Các tiêu chí này quan trọng vì một phép tiền xử lý có thể cải thiện chất lượng dữ liệu nhưng đồng thời làm mất thông tin, tăng chi phí tính toán hoặc tạo ra dữ liệu không phù hợp với mô hình downstream. Đây cũng là lý do nghiên cứu gốc không chỉ xem xét chất lượng dữ liệu mà còn đánh giá tác động của preprocessing đến hiệu năng AI và khả năng phân phối preprocessing tại edge.

## 2. So sánh các nhóm phương pháp

### 2.1. Missing data

Các phương pháp xử lý giá trị thiếu có thể chia thành nhóm đơn giản như deletion, mean/median hoặc forward/backward filling và nhóm dựa trên mô hình như interpolation, regression, Kalman filtering hoặc các phương pháp học máy.

Phương pháp đơn giản có ưu điểm là dễ triển khai, chi phí thấp và phù hợp khi tỷ lệ missing thấp. Tuy nhiên, chúng có thể làm suy giảm cấu trúc thời gian hoặc làm giảm phương sai của dữ liệu. Với chuỗi thời gian, việc thay thế bằng một giá trị cố định có thể tạo ra các đoạn dữ liệu nhân tạo không phản ánh động lực thực tế.

Các phương pháp sử dụng quan hệ thời gian hoặc quan hệ giữa nhiều biến có khả năng bảo toàn cấu trúc dữ liệu tốt hơn nhưng có chi phí tính toán cao hơn. Vì vậy, lựa chọn phương pháp nên phụ thuộc vào **tỷ lệ missing, cơ chế missing, độ dài khoảng trống và yêu cầu thời gian thực**.

### 2.2. Outlier detection và noise reduction

Outlier detection tập trung xác định các quan sát bất thường, trong khi noise reduction nhằm giảm thành phần nhiễu nhưng vẫn duy trì tín hiệu có ý nghĩa.

Các phương pháp thống kê như Z-score và IQR có chi phí thấp và dễ triển khai. IQR đặc biệt phù hợp với các hệ thống cần xử lý dữ liệu theo cửa sổ vì có thể được tính toán tương đối hiệu quả, mặc dù khả năng phát hiện phụ thuộc vào phân phối dữ liệu và lựa chọn ngưỡng.

Các phương pháp dựa trên clustering, density hoặc Isolation Forest có khả năng xử lý quan hệ đa biến tốt hơn nhưng yêu cầu tài nguyên lớn hơn. Do đó:

$$
\text{Detection capability}
\uparrow
\quad\Longrightarrow\quad
\text{Computational cost}
\uparrow
$$

không phải là quan hệ tuyệt đối, nhưng phản ánh một trade-off phổ biến giữa độ phức tạp của mô hình và khả năng phát hiện bất thường.

Đối với noise reduction, moving average và exponential smoothing có chi phí thấp nhưng có thể làm mất các biến động ngắn hạn. Các phương pháp như Savitzky--Golay hoặc wavelet có khả năng bảo toàn cấu trúc tín hiệu tốt hơn trong một số trường hợp nhưng yêu cầu lựa chọn tham số phù hợp.

### 2.3. Scaling và normalization

Scaling không nhằm sửa lỗi dữ liệu mà nhằm đưa các biến về miền giá trị phù hợp với thuật toán học.

Hai phép biến đổi phổ biến là Min--Max scaling:

$$
x' =
\frac{x-x_{\min}}
{x_{\max}-x_{\min}},
$$

và Standardization:

$$
x' =
\frac{x-\mu}{\sigma}.
$$

Min--Max scaling giữ quan hệ thứ tự và đưa dữ liệu về một khoảng xác định, nhưng nhạy cảm với extreme values. Standardization ít phụ thuộc hơn vào khoảng giá trị cố định và thường phù hợp với các mô hình tối ưu bằng gradient.

Do đó, scaling nên được lựa chọn dựa trên phân phối dữ liệu và yêu cầu của mô hình thay vì áp dụng mặc định. Đặc biệt, các tham số $\mu$, $\sigma$, $x_{\min}$ và $x_{\max}$ phải được ước lượng từ tập huấn luyện để tránh data leakage.

### 2.4. Transformation và stationarity

Các phép biến đổi như logarithm, Box--Cox hoặc Yeo--Johnson có thể giảm skewness và ổn định variance. Trong khi đó, differencing và decomposition thường được sử dụng để xử lý non-stationarity.

Với chuỗi $x_t$, sai phân bậc nhất được định nghĩa:

$$
\Delta x_t = x_t-x_{t-1}.
$$

Ưu điểm của transformation và differencing là làm cho dữ liệu phù hợp hơn với các giả định của một số mô hình thống kê. Tuy nhiên, chúng có thể làm giảm khả năng diễn giải của dữ liệu ở không gian ban đầu và có thể yêu cầu bước inverse transformation khi đưa dự báo trở lại đơn vị gốc.

Do đó, stationarity không nên được xem là mục tiêu bắt buộc đối với mọi mô hình. Các mô hình học sâu hiện đại có thể học trực tiếp từ chuỗi không dừng, trong khi các mô hình thống kê truyền thống thường phụ thuộc mạnh hơn vào các giả định về stationarity.

### 2.5. Feature engineering

Feature engineering chuyển dữ liệu thời gian thành các biểu diễn có khả năng cung cấp thông tin hữu ích hơn cho mô hình.

Các nhóm đặc trưng phổ biến gồm:

* temporal features;
* lag features;
* rolling statistics;
* decomposition-based features;
* domain-specific features.

Ví dụ, đặc trưng lag được biểu diễn bởi

$$
x_{t-k},
\qquad k\in\mathbb{N}^{+},
$$

trong khi rolling mean với cửa sổ $w$ là

$$
\operatorname{MA}_t^{(w)}=

\frac{1}{w}
\sum_{i=0}^{w-1}x_{t-i}.
$$

Feature engineering có khả năng đưa kiến thức miền và cấu trúc thời gian vào mô hình, nhưng số lượng đặc trưng tăng nhanh có thể dẫn đến redundancy và multicollinearity. Vì vậy, feature engineering thường cần kết hợp với feature selection hoặc dimensionality reduction.

### 2.6. Feature selection và dimensionality reduction

Feature selection giữ lại một tập con các biến ban đầu:

$$
\mathcal{F}'\subseteq\mathcal{F},
$$

trong khi dimensionality reduction ánh xạ dữ liệu sang một không gian mới có số chiều thấp hơn:

$$
\mathbf{x}\in\mathbb{R}^{d}
\longrightarrow
\mathbf{z}\in\mathbb{R}^{k},
\qquad k<d.
$$

Filter methods có chi phí thấp và độc lập với mô hình downstream nhưng thường không tận dụng đầy đủ quan hệ giữa các đặc trưng và mô hình. Wrapper methods có thể tìm được tập đặc trưng phù hợp với một mô hình cụ thể nhưng chi phí tính toán cao. Embedded methods tạo ra quá trình lựa chọn trong khi huấn luyện mô hình, do đó đạt được sự cân bằng giữa hai nhóm trên.

PCA là ví dụ điển hình của dimensionality reduction. Phép biến đổi có dạng

$$
\mathbf{z}=

\mathbf{W}^{\top}
(\mathbf{x}-\boldsymbol{\mu}),
$$

trong đó các vector riêng của ma trận covariance được sử dụng làm các principal components.

Ưu điểm của PCA là giảm số chiều và loại bỏ một phần redundancy, nhưng các component mới thường khó diễn giải về mặt vật lý. Vì vậy, feature selection thường phù hợp hơn khi khả năng diễn giải của biến đầu vào là yêu cầu quan trọng.

### 2.7. Sensor fusion và temporal alignment

Đối với hệ thống có nhiều sensor, dữ liệu có thể được biểu diễn:

$$
\mathcal{D}^{(m)}
=
\left\{
\left(t_i^{(m)}, \mathbf{x}_i^{(m)}\right)
\right\}_{i=1}^{N_m},
\qquad
m=1,\ldots,M.
$$

Mỗi sensor có thể có sampling rate, timestamp và độ trễ khác nhau. Temporal alignment nhằm ánh xạ các quan sát về cùng một temporal reference:

$$
t_i^{(m)}
\rightarrow
\tilde{t}_j.
$$

Fusion giúp tăng information coverage và khả năng quan sát hệ thống, nhưng đồng thời làm tăng dimensionality, synchronization complexity và nguy cơ propagation of errors. Vì vậy, sensor fusion chỉ có lợi khi thông tin bổ sung thực sự mang tính bổ trợ cho nhiệm vụ downstream.

### 2.8. Data compression

Compression có mục tiêu giảm kích thước dữ liệu trong khi cân bằng giữa information preservation và resource consumption.

Lossless compression thỏa mãn:

$$
\mathcal{D}_{decoded}=

\mathcal{D}_{original},
$$

do đó bảo toàn hoàn toàn dữ liệu nhưng thường đạt tỷ lệ nén thấp hơn. Ngược lại, lossy compression cho phép:

$$
\mathcal{D}*{decoded}
\neq
\mathcal{D}*{original},
$$

nhưng có thể đạt tỷ lệ nén cao hơn.

Trong Edge/IoT, compression có thể giảm bandwidth, storage và communication cost. Tuy nhiên, nếu nén làm mất các tín hiệu quan trọng đối với nhiệm vụ AI, lợi ích về tài nguyên có thể phải đánh đổi bằng degradation của downstream performance. Nghiên cứu gốc cũng xem xét khả năng phân phối preprocessing tại edge nhằm giảm tải hệ thống trung tâm, tài nguyên sử dụng và hỗ trợ EdgeAI.

## 3. So sánh tổng hợp

| Nhóm phương pháp         | Mục tiêu chính                    | Ưu điểm                            | Hạn chế chính                    | Phù hợp Edge/IoT             |
| ------------------------ | --------------------------------- | ---------------------------------- | -------------------------------- | ---------------------------- |
| Missing data             | Khôi phục quan sát thiếu          | Cải thiện tính đầy đủ              | Có thể tạo bias                  | Cao với phương pháp đơn giản |
| Outlier detection        | Phát hiện bất thường              | Giảm ảnh hưởng của lỗi/anomaly     | Phụ thuộc ngưỡng và phân phối    | Cao với IQR/thống kê         |
| Noise reduction          | Giảm nhiễu                        | Cải thiện signal quality           | Có thể mất biến động ngắn hạn    | Cao với phương pháp nhẹ      |
| Scaling                  | Chuẩn hóa magnitude               | Hỗ trợ optimization                | Có nguy cơ leakage               | Rất cao                      |
| Transformation           | Điều chỉnh distribution           | Giảm skewness/variance instability | Giảm interpretability            | Cao                          |
| Stationarity             | Ổn định đặc tính thống kê         | Hỗ trợ mô hình thống kê            | Có thể mất thông tin xu hướng    | Trung bình                   |
| Feature engineering      | Bổ sung thông tin hữu ích         | Tăng khả năng biểu diễn            | Tăng dimensionality              | Trung bình                   |
| Feature selection        | Loại bỏ biến dư thừa              | Giảm dimensionality                | Có thể loại bỏ thông tin hữu ích | Cao                          |
| Dimensionality reduction | Tạo representation thấp chiều     | Giảm redundancy                    | Khó diễn giải                    | Cao                          |
| Sensor fusion            | Kết hợp nhiều nguồn               | Tăng information coverage          | Synchronization và complexity    | Phụ thuộc hệ thống           |
| Lossless compression     | Giảm kích thước không mất dữ liệu | Bảo toàn thông tin                 | Tỷ lệ nén hạn chế                | Rất cao                      |
| Lossy compression        | Giảm kích thước mạnh              | Tiết kiệm bandwidth/storage        | Mất thông tin                    | Cao nếu kiểm soát distortion |

## 4. Trade-off giữa chất lượng dữ liệu và chi phí xử lý

Không tồn tại quan hệ đơn điệu giữa mức độ phức tạp của preprocessing và chất lượng cuối cùng của mô hình. Một pipeline quá đơn giản có thể để lại missing values, noise hoặc redundancy; ngược lại, pipeline quá phức tạp có thể làm biến đổi dữ liệu quá mức hoặc tạo ra chi phí không cần thiết.

Có thể mô hình hóa mục tiêu lựa chọn preprocessing như một bài toán tối ưu đa mục tiêu:

$$
\mathcal{P}^{*}=

\arg\max_{\mathcal{P}}
\left[
Q(\mathcal{P}),
M(\mathcal{P})
\right],
$$

đồng thời tối thiểu hóa

$$
C(\mathcal{P}),
$$

trong đó:

* $Q(\mathcal{P})$ là chất lượng dữ liệu sau preprocessing;
* $M(\mathcal{P})$ là hiệu năng của mô hình downstream;
* $C(\mathcal{P})$ là chi phí tính toán, bộ nhớ, năng lượng và truyền dữ liệu.

Do đó, preprocessing cần được đánh giá **end-to-end**, thay vì chỉ đánh giá từng thuật toán riêng lẻ.

## 5. Nguyên tắc lựa chọn phương pháp

Từ các nhóm phương pháp trên, có thể rút ra bốn nguyên tắc lựa chọn chính.

**Thứ nhất, preprocessing phải phụ thuộc vào đặc tính dữ liệu.** Missing data, outlier, noise, non-stationarity và redundancy là những vấn đề khác nhau và không nên được xử lý bằng cùng một kỹ thuật.

**Thứ hai, preprocessing phải phụ thuộc vào downstream task.** Một biến đổi có lợi cho ARIMA hoặc các mô hình thống kê không nhất thiết cải thiện LSTM, Transformer hoặc các mô hình học máy khác.

**Thứ ba, cần ưu tiên information preservation.** Đối với chuỗi thời gian, cấu trúc temporal dependency là một phần quan trọng của thông tin. Việc loại bỏ hoặc làm phẳng các biến động có ý nghĩa có thể làm giảm hiệu năng dự báo ngay cả khi dữ liệu nhìn "sạch" hơn.

**Thứ tư, preprocessing phải xét đến môi trường triển khai.** Trong Edge/IoT, latency, memory, energy và bandwidth có thể quan trọng không kém prediction accuracy. Nghiên cứu của Tawakuli et al. nhấn mạnh chính khía cạnh này khi xem xét khả năng phân phối các kỹ thuật preprocessing xuống edge.

## 6. Kết luận

So sánh cho thấy các phương pháp tiền xử lý giải quyết những vấn đề khác nhau và có các trade-off khác nhau giữa **data quality, information preservation, computational cost và downstream performance**. Các phương pháp đơn giản thường có ưu thế về tốc độ và khả năng triển khai, trong khi các phương pháp mô hình hóa phức tạp có thể khai thác tốt hơn cấu trúc của chuỗi thời gian nhưng yêu cầu nhiều tài nguyên hơn.

Vì vậy, một pipeline hiệu quả không nên được xây dựng bằng cách áp dụng tuần tự tất cả các kỹ thuật. Thay vào đó, cần lựa chọn **tối thiểu các phép biến đổi cần thiết để giải quyết các vấn đề thực sự tồn tại trong dữ liệu**, đồng thời đánh giá tác động của chúng đối với nhiệm vụ AI cuối cùng. Quan điểm này phù hợp với mục tiêu của nghiên cứu gốc: preprocessing không chỉ là bước chuẩn bị dữ liệu mà là một thành phần có ảnh hưởng trực tiếp đến chất lượng dữ liệu, hiệu năng AI và khả năng triển khai hệ thống.

### Tài liệu tham khảo

**[1]** A. Tawakuli, B. Havers, V. M. Gulisano, D. Kaiser, and T. Engel, “Survey: Time-Series Data Preprocessing: A Survey and an Empirical Analysis,” *Journal of Engineering Research*, vol. 13, no. 2, pp. 674–711, 2025. DOI: 10.1016/j.jer.2024.02.018.
