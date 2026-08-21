# 1.2. Vấn đề nghiên cứu

Dữ liệu chuỗi thời gian được sử dụng làm đầu vào cho nhiều bài toán phân tích và dự báo bằng học máy và học sâu. Tuy nhiên, dữ liệu thu thập từ cảm biến, hệ thống giám sát hoặc các nguồn dữ liệu thực tế thường chứa nhiều vấn đề về chất lượng và cấu trúc. Các vấn đề này không chỉ ảnh hưởng đến giá trị của từng quan sát mà còn có thể làm thay đổi quan hệ phụ thuộc theo thời gian. Do đó, việc đưa dữ liệu thô trực tiếp vào mô hình có thể dẫn đến quá trình học không ổn định, khả năng khái quát hóa kém hoặc kết quả dự báo không đáng tin cậy.

Vấn đề đầu tiên là **sự không đồng nhất về chất lượng dữ liệu**. Một chuỗi thời gian có thể đồng thời chứa missing values, outliers, noise, duplicate observations và các khoảng thời gian bị gián đoạn. Những vấn đề này có nguồn gốc khác nhau và không thể xử lý bằng một phương pháp duy nhất. Missing values yêu cầu các chiến lược khôi phục hoặc loại bỏ phù hợp; outliers cần được phân biệt giữa lỗi đo và sự kiện thực tế; trong khi noise cần được giảm thiểu mà không làm mất tín hiệu quan trọng. Vì vậy, preprocessing phải xem xét bản chất của từng loại lỗi thay vì áp dụng một quy trình làm sạch cố định.

Vấn đề thứ hai là **sự khác biệt về phân phối và biểu diễn của các biến**. Các đặc trưng có thể có đơn vị đo, phạm vi giá trị và phân phối hoàn toàn khác nhau. Một số thuật toán nhạy cảm với scale của dữ liệu, trong khi một số chuỗi có thể thể hiện skewness hoặc phương sai thay đổi theo thời gian. Scaling, normalization và các phép transformation vì vậy có thể cần thiết để đưa dữ liệu về biểu diễn phù hợp hơn. Tuy nhiên, lựa chọn sai phép biến đổi có thể làm mất đặc tính vật lý hoặc thống kê vốn có của dữ liệu. Đặc biệt đối với time series, transformation phải được thực hiện sao cho không phá vỡ cấu trúc temporal relationship.

Vấn đề thứ ba là **tính không dừng (non-stationarity)**. Trong nhiều chuỗi thời gian thực tế, các đặc tính thống kê như mean, variance hoặc covariance thay đổi theo thời gian. Xu hướng dài hạn, seasonality và các biến động theo chu kỳ có thể khiến mô hình khó học một quan hệ ổn định giữa quá khứ và tương lai. Do đó, preprocessing cần có khả năng nhận diện và xử lý các thành phần này thông qua transformation, differencing hoặc decomposition khi cần thiết. Tuy nhiên, việc loại bỏ xu hướng hoặc seasonality một cách máy móc có thể đồng thời loại bỏ những tín hiệu mà mô hình dự báo cần sử dụng.

Vấn đề thứ tư liên quan đến **biểu diễn đặc trưng**. Dữ liệu chuỗi thời gian thường chứa thông tin phụ thuộc vào lịch sử của chính nó. Giá trị tại thời điểm hiện tại có thể phụ thuộc vào các quan sát trước đó, xu hướng cục bộ hoặc trạng thái của hệ thống trong một khoảng thời gian. Nếu chỉ sử dụng giá trị quan sát tại thời điểm hiện tại, mô hình có thể không nhận được đầy đủ thông tin temporal context. Điều này dẫn đến nhu cầu xây dựng các temporal features, lag features và rolling features. Tuy nhiên, feature engineering cũng làm tăng số chiều của dữ liệu và có thể tạo ra các đặc trưng dư thừa hoặc tương quan cao.

Vấn đề thứ năm là **high dimensionality và feature redundancy**. Khi nhiều biến được thu thập đồng thời hoặc một số lượng lớn đặc trưng được tạo ra từ dữ liệu gốc, số chiều đầu vào có thể tăng nhanh. Không phải tất cả đặc trưng đều đóng góp hữu ích cho nhiệm vụ dự đoán. Các đặc trưng không liên quan hoặc dư thừa có thể làm tăng chi phí tính toán, gây khó khăn cho quá trình tối ưu và làm tăng nguy cơ overfitting. Vì vậy, feature selection và dimensionality reduction trở thành các bước quan trọng trong những pipeline có số lượng đặc trưng lớn.

Vấn đề thứ sáu xuất hiện khi dữ liệu đến từ **nhiều cảm biến hoặc nhiều nguồn khác nhau**. Các nguồn dữ liệu có thể có sampling rate, timestamp, đơn vị đo và độ tin cậy khác nhau. Nếu các nguồn này không được đồng bộ trước khi kết hợp, dữ liệu sau fusion có thể biểu diễn những trạng thái khác nhau của hệ thống tại cùng một chỉ số thời gian. Do đó, sensor fusion không chỉ là phép nối các feature mà còn đòi hỏi giải quyết bài toán temporal alignment và lựa chọn mức độ fusion phù hợp.

Vấn đề thứ bảy là **chi phí lưu trữ và truyền tải dữ liệu**. Đối với hệ thống IoT và edge computing, dữ liệu cảm biến có thể được tạo ra liên tục với tốc độ cao. Việc truyền toàn bộ dữ liệu thô về cloud hoặc server trung tâm làm tăng bandwidth, storage và computational cost. Data compression có thể giảm kích thước dữ liệu, nhưng cần cân bằng giữa mức độ nén và lượng thông tin bị mất. Đặc biệt, lossy compression có thể làm thay đổi tín hiệu và ảnh hưởng đến các nhiệm vụ downstream nếu mức độ mất mát không được kiểm soát.

Bên cạnh các vấn đề riêng lẻ trên, một thách thức quan trọng hơn là **mối quan hệ giữa các bước preprocessing**. Các kỹ thuật không tồn tại độc lập mà có thể tác động lẫn nhau. Chẳng hạn, outlier detection có thể ảnh hưởng đến scaling; transformation có thể thay đổi kết quả feature selection; decomposition có thể tạo ra các thành phần mới cho feature engineering; trong khi compression có thể làm thay đổi chất lượng dữ liệu trước khi mô hình sử dụng chúng. Vì vậy, việc đánh giá từng phương pháp một cách biệt lập không đủ để xác định một preprocessing pipeline hiệu quả.

Một vấn đề đặc biệt quan trọng đối với time-series forecasting là **data leakage**. Do dữ liệu có thứ tự thời gian, các thống kê hoặc tham số preprocessing được tính từ toàn bộ dataset có thể vô tình sử dụng thông tin thuộc validation hoặc test set. Ví dụ, nếu scaler được fit trên toàn bộ dữ liệu trước khi chia tập, thông tin về phân phối của tương lai đã được truyền vào quá trình huấn luyện. Tương tự, việc xây dựng rolling hoặc lag features không đúng cách có thể khiến thông tin tương lai xuất hiện trong input của mô hình. Vì vậy, preprocessing phải được thiết kế theo nguyên tắc bảo toàn temporal ordering và chỉ sử dụng thông tin có sẵn tại thời điểm dự báo.

Từ các vấn đề trên, nghiên cứu đặt ra **bài toán tổng quát**: làm thế nào để lựa chọn, tổ chức và đánh giá các kỹ thuật preprocessing sao cho dữ liệu chuỗi thời gian từ trạng thái thô có thể trở thành dữ liệu có chất lượng, có cấu trúc và phù hợp với các mô hình AI, đồng thời bảo toàn thông tin thời gian và tránh data leakage.

Bài toán này có thể được biểu diễn dưới dạng:

$$X_{\mathrm{raw}} \xrightarrow{\mathcal{P}} X_{\mathrm{AI}}$$

trong đó (X_{\mathrm{raw}}) là dữ liệu chuỗi thời gian ban đầu, (\mathcal{P}) là một preprocessing pipeline gồm nhiều phép biến đổi và (X_{\mathrm{AI}}) là dữ liệu đầu ra sẵn sàng cho mô hình AI. Một pipeline phù hợp cần thỏa mãn đồng thời các yêu cầu:

$$\mathcal{P}= {\mathcal{C}, \mathcal{T}, \mathcal{F}, \mathcal{S}, \mathcal{A}, \mathcal{K}}$$

với:

* $\mathcal{C}$: **Data Cleaning** — xử lý missing data, outlier và noise.
* $\mathcal{T}$: **Data Transformation** — scaling, normalization, transformation, stationarity và decomposition.
* $\mathcal{F}$: **Feature Engineering** — xây dựng temporal, lag, rolling và feature representation.
* $\mathcal{S}$: **Feature Selection** — loại bỏ đặc trưng không cần thiết và giảm dimensionality.
* $\mathcal{A}$: **Sensor Fusion** — kết hợp dữ liệu từ nhiều nguồn và đồng bộ theo thời gian.
* $\mathcal{K}$: **Data Compression** — giảm chi phí lưu trữ và truyền tải trong các hệ thống có giới hạn tài nguyên.

Từ đó, nghiên cứu không đặt mục tiêu tìm ra một kỹ thuật preprocessing duy nhất tốt nhất cho mọi trường hợp. Thay vào đó, trọng tâm là **hệ thống hóa không gian các phương pháp, xác định điều kiện sử dụng, phân tích trade-off và đánh giá tác động của chúng đối với dữ liệu và mô hình downstream**. Cách tiếp cận này tạo cơ sở cho Chương 2 trong việc xác định phạm vi và xây dựng taxonomy; đồng thời làm nền tảng cho các chương tiếp theo khi phân tích từng nhóm kỹ thuật preprocessing một cách độc lập nhưng vẫn duy trì mối liên hệ trong toàn bộ pipeline.

Đối với phần thực nghiệm, vấn đề trên được cụ thể hóa thông qua bộ dữ liệu **UCI Appliances Energy Prediction**, trong đó dữ liệu cảm biến năng lượng được sử dụng để minh họa cách các kỹ thuật preprocessing được áp dụng từ dữ liệu ban đầu đến biểu diễn phù hợp cho bài toán dự báo. Trường hợp nghiên cứu này được trình bày chi tiết ở Chương 13 và được sử dụng để kiểm chứng mối liên hệ giữa taxonomy lý thuyết và preprocessing pipeline thực tế.
