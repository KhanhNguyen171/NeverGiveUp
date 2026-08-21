# 2.1 Research Scope

Nghiên cứu này tập trung khảo sát và hệ thống hóa các phương pháp **data preprocessing cho dữ liệu chuỗi thời gian số (numerical time-series data)** nhằm chuyển đổi dữ liệu thô thành dữ liệu có chất lượng và phù hợp cho các hệ thống phân tích dữ liệu, Machine Learning (ML) và Artificial Intelligence (AI). Phạm vi được xây dựng theo quan điểm rằng preprocessing không chỉ là quá trình loại bỏ dữ liệu lỗi, mà là một chuỗi các phép biến đổi có thể tác động trực tiếp đến chất lượng dữ liệu, đặc trưng đầu vào và hiệu quả của mô hình. Quan điểm này phù hợp với phạm vi mở rộng của Tawakuli et al., trong đó preprocessing được xem xét một cách tổng thể thay vì chỉ giới hạn ở data cleaning.

## 2.1.1 Đối tượng dữ liệu

Đối tượng chính của nghiên cứu là **dữ liệu chuỗi thời gian số**, trong đó mỗi quan sát được gắn với một thời điểm và các giá trị quan sát có thể thay đổi theo thời gian. Dữ liệu có thể ở dạng univariate hoặc multivariate, với một hoặc nhiều biến được quan sát đồng thời.

Có thể biểu diễn một chuỗi thời gian dưới dạng

$$
\mathcal{X} = {(t_i, \mathbf{x}*i)}*{i=1}^{T},
$$

trong đó:

* $t_i$ là timestamp của quan sát thứ $i$;
* $\mathbf{x}_i \in \mathbb{R}^{F}$ là vector gồm $F$ biến tại thời điểm $t_i$;
* $T$ là số lượng quan sát.

Với dữ liệu multivariate, tập dữ liệu có thể được biểu diễn dưới dạng ma trận

$$
\mathbf{X} =
\begin{bmatrix}
x_{1,1} & x_{1,2} & \cdots & x_{1,F} \
x_{2,1} & x_{2,2} & \cdots & x_{2,F} \
\vdots & \vdots & \ddots & \vdots \
x_{T,1} & x_{T,2} & \cdots & x_{T,F}
\end{bmatrix}.
$$

Đặc điểm quan trọng của loại dữ liệu này là **thứ tự thời gian mang thông tin**, do đó các thao tác preprocessing không được làm mất hoặc làm sai lệch quan hệ temporal giữa các quan sát.

Phạm vi này bao gồm các tình huống dữ liệu được thu thập từ sensor, hệ thống giám sát, thiết bị IoT, hệ thống công nghiệp, môi trường, năng lượng và các nguồn dữ liệu có cấu trúc thời gian tương tự.

## 2.1.2 Mục tiêu của preprocessing

Nghiên cứu xem preprocessing như một quá trình biến đổi

$$
\mathcal{X}*{raw}
\rightarrow
\mathcal{X}*{clean}
\rightarrow
\mathcal{X}*{transformed}
\rightarrow
\mathcal{X}*{feature}
\rightarrow
\mathcal{X}_{AI},
$$

trong đó dữ liệu được từng bước chuyển từ trạng thái thu thập ban đầu sang trạng thái phù hợp cho phân tích hoặc mô hình hóa.

Các mục tiêu chính gồm:

1. **Cải thiện data quality** bằng cách phát hiện và xử lý missing values, outliers và noise.
2. **Chuẩn hóa biểu diễn dữ liệu** thông qua scaling, normalization và các phép transformation phù hợp.
3. **Xử lý đặc tính temporal** như non-stationarity, trend và seasonality.
4. **Tạo ra các biểu diễn có thông tin hơn** thông qua feature engineering.
5. **Giảm thông tin dư thừa và dimensionality** khi số lượng biến lớn.
6. **Kết hợp dữ liệu từ nhiều nguồn hoặc nhiều sensor** khi bài toán yêu cầu.
7. **Giảm kích thước dữ liệu và chi phí xử lý** trong các hệ thống có hạn chế về tài nguyên.

Các mục tiêu này phản ánh quan điểm preprocessing có thể đồng thời tác động đến **chất lượng dữ liệu, hiệu quả huấn luyện và chất lượng đầu ra của hệ thống AI**.

## 2.1.3 Phạm vi các nhóm phương pháp

Để tránh việc khảo sát các kỹ thuật một cách rời rạc, nghiên cứu tổ chức preprocessing thành các nhóm có quan hệ với nhau.

### Data cleaning

Nhóm thứ nhất tập trung vào việc phát hiện và xử lý các vấn đề trực tiếp của dữ liệu quan sát, bao gồm:

* missing data;
* outlier;
* noise;
* các vấn đề về tính hợp lệ và nhất quán của dữ liệu.

Nội dung này được trình bày trong **Chapter 3 – Data Cleaning**.

### Data transformation

Nhóm thứ hai nghiên cứu các phép biến đổi nhằm đưa dữ liệu về representation phù hợp hơn với thuật toán phân tích. Phạm vi bao gồm:

* scaling;
* normalization;
* transformation;
* stationarity;
* decomposition.

Các phương pháp này được trình bày trong **Chapter 4 – Data Transformation**.

### Feature engineering

Preprocessing không chỉ làm sạch dữ liệu mà còn có thể tạo ra các biểu diễn mới từ cấu trúc temporal. Nghiên cứu xem xét:

* temporal features;
* lag features;
* rolling features;
* feature representation.

Nhóm này được trình bày trong **Chapter 5 – Feature Engineering**.

### Feature selection và dimensionality reduction

Khi số lượng biến tăng, preprocessing cần xem xét việc loại bỏ các biến không cần thiết hoặc xây dựng một không gian biểu diễn có số chiều thấp hơn. Phạm vi bao gồm:

* filter methods;
* wrapper methods;
* embedded methods;
* dimensionality reduction.

Các phương pháp được hệ thống hóa trong **Chapter 6 – Feature Selection**.

### Sensor fusion

Trong hệ thống có nhiều sensor hoặc nhiều nguồn dữ liệu temporal, preprocessing có thể bao gồm quá trình kết hợp các nguồn dữ liệu thành một representation thống nhất. Nghiên cứu xem xét:

* fusion levels;
* phương thức kết hợp dữ liệu;
* temporal alignment.

Nội dung này được trình bày trong **Chapter 7 – Sensor Fusion**.

### Data compression

Đối với các hệ thống có giới hạn về storage, bandwidth hoặc computational resources, preprocessing còn có thể bao gồm giảm kích thước dữ liệu. Nghiên cứu phân biệt:

* lossless compression;
* lossy compression;
* các vấn đề triển khai trong edge/IoT.

Nhóm này được trình bày trong **Chapter 8 – Data Compression**.

Việc đưa sensor fusion và data compression vào phạm vi nghiên cứu là có chủ đích. Tawakuli et al. xây dựng một quan điểm preprocessing mang tính holistic, trong đó preprocessing không chỉ xử lý các vấn đề về chất lượng dữ liệu mà còn bao gồm sensor fusion và data compression.

## 2.1.4 Phạm vi theo mục đích sử dụng dữ liệu

Nghiên cứu không giới hạn preprocessing cho một thuật toán ML hoặc AI cụ thể. Thay vào đó, preprocessing được xem xét như một **data preparation layer** nằm trước quá trình phân tích hoặc modeling.

Có thể mô hình hóa pipeline tổng quát như sau:

$$
\text{Raw Time Series}
\rightarrow
\text{Preprocessing}
\rightarrow
\text{Feature Representation}
\rightarrow
\text{ML/AI Model}
\rightarrow
\text{Prediction/Analysis}.
$$

Do đó, một phương pháp preprocessing không được đánh giá độc lập hoàn toàn với downstream task. Việc lựa chọn phương pháp phụ thuộc vào:

* đặc điểm của dữ liệu;
* mục tiêu phân tích;
* cấu trúc temporal;
* loại mô hình sử dụng;
* yêu cầu về computational resources;
* yêu cầu về chất lượng đầu ra.

Bản thân Tawakuli et al. cũng nhấn mạnh rằng thứ tự preprocessing, vị trí thực hiện, tham số và tập kỹ thuật phù hợp phụ thuộc vào loại dữ liệu, nguồn dữ liệu, context của hệ thống và thuật toán sử dụng dữ liệu.

## 2.1.5 Phạm vi đánh giá thực nghiệm

Nghiên cứu không chỉ khảo sát về mặt lý thuyết mà còn xem xét preprocessing từ góc độ **empirical evaluation**. Hai khía cạnh chính được quan tâm là:

$$
\text{Preprocessing}
\rightarrow
\begin{cases}
\text{Data Quality}\
\text{Model Performance}
\end{cases}
$$

Trong đó, data quality phản ánh mức độ cải thiện của dữ liệu sau preprocessing, còn model performance phản ánh tác động của preprocessing đối với nhiệm vụ downstream.

Phạm vi thực nghiệm được trình bày trong **Chapter 9 – Empirical Analysis**, bao gồm:

* experimental setup;
* datasets;
* preprocessing methods;
* evaluation metrics;
* results;
* findings.

Cách tiếp cận này phù hợp với mục tiêu của bài báo nền tảng, trong đó survey được kết hợp với empirical analysis để đánh giá ảnh hưởng của preprocessing lên chất lượng dữ liệu và hiệu năng của AI algorithms.

## 2.1.6 Phạm vi triển khai: Centralized và Edge/IoT

Nghiên cứu cũng xem xét preprocessing dưới góc nhìn hệ thống. Cụ thể, preprocessing có thể được thực hiện tại:

$$
\text{Data Source}
\rightarrow
\begin{cases}
\text{Central/Cloud}\
\text{Edge}\
\text{Hybrid}
\end{cases}
$$

Việc đưa preprocessing đến edge có thể làm giảm lượng dữ liệu cần truyền về hệ thống trung tâm, giảm workload và resource consumption, đồng thời hỗ trợ các ứng dụng EdgeAI. Đây cũng là một trong những khía cạnh được Tawakuli et al. đưa vào survey.

Trong nghiên cứu này, khía cạnh edge/IoT được tập trung chủ yếu ở **Chapter 8 – Data Compression**, nơi các vấn đề về giảm kích thước dữ liệu và khả năng triển khai preprocessing trong môi trường tài nguyên hạn chế được xem xét.

## 2.1.7 Những nội dung nằm ngoài phạm vi

Để duy trì trọng tâm, nghiên cứu **không xem xét preprocessing như một nghiên cứu toàn diện về toàn bộ machine learning pipeline**. Các nội dung sau không phải trọng tâm chính:

* thiết kế kiến trúc ML/DL;
* tối ưu hyperparameter của model;
* training algorithm;
* model architecture;
* model deployment độc lập với preprocessing;
* giải thích mô hình;
* đánh giá forecasting algorithm như một chủ đề riêng biệt.

Các nội dung này chỉ được đề cập khi cần thiết để giải thích **tác động hoặc yêu cầu của preprocessing đối với downstream model**.

Tương tự, data collection cũng không phải trọng tâm của nghiên cứu. Điểm bắt đầu của phạm vi là dữ liệu sau khi đã được thu thập và cần được chuyển đổi thành dữ liệu có chất lượng, phù hợp cho phân tích và AI.

## 2.1.8 Ranh giới giữa các chương

Phạm vi trên tạo thành một chuỗi logic cho toàn bộ nghiên cứu:

$$
\boxed{
\text{Data Quality}
\rightarrow
\text{Transformation}
\rightarrow
\text{Feature Construction}
\rightarrow
\text{Feature Reduction}
\rightarrow
\text{Fusion}
\rightarrow
\text{Compression}
}
$$

Từ đó, **Chapter 3** tập trung trả lời câu hỏi *dữ liệu có vấn đề gì và làm thế nào để xử lý?*; 

**Chapter 4** trả lời *làm thế nào biến đổi dữ liệu để có representation phù hợp?*; 

**Chapter 5** tập trung vào *làm thế nào khai thác cấu trúc temporal để tạo feature?*; 

**Chapter 6** giải quyết *làm thế nào giảm redundancy và dimensionality?*; 

**Chapter 7** nghiên cứu *làm thế nào kết hợp nhiều nguồn dữ liệu temporal?*; 

và **Chapter 8** xem xét *làm thế nào giảm chi phí lưu trữ và truyền dữ liệu?*

Sau khi các nhóm phương pháp được khảo sát, **Chapter 9** đánh giá chúng trên dữ liệu thực nghiệm, 

**Chapter 10** tổng hợp các trade-off và limitations, 

còn **Chapter 11** chuyển các kết quả khảo sát thành một preprocessing pipeline hướng tới dữ liệu sẵn sàng cho AI.

Như vậy, phạm vi nghiên cứu được giới hạn đủ rõ để tránh biến survey thành một tổng quan chung về machine learning, đồng thời đủ rộng để phản ánh bản chất đa bước của preprocessing cho numerical time-series data. Đây cũng là điểm tương đồng cốt lõi với survey của Tawakuli et al., trong đó preprocessing được xây dựng theo một phạm vi có cấu trúc và mang tính holistic thay vì chỉ tập trung vào cleaning.

**Tài liệu nền tảng:** Tawakuli, A., Havers, B., Gulisano, V., Kaiser, D., & Engel, T., *Survey: Time-Series Data Preprocessing: A Survey and an Empirical Analysis*, **Journal of Engineering Research**, 13(2), 674–711, 2025. DOI: `10.1016/j.jer.2024.02.018`.
