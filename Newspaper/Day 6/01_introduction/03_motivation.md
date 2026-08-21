# 1.3. Động lực nghiên cứu

Từ các vấn đề được xác định ở Mục `01_background.md` và `02_problem.md`, có thể thấy rằng **data preprocessing là một thành phần quyết định chất lượng của toàn bộ quy trình phân tích dữ liệu chuỗi thời gian**, thay vì chỉ là bước chuẩn bị đơn giản trước khi đưa dữ liệu vào mô hình AI. Dữ liệu thực tế thường chứa nhiều vấn đề đồng thời, trong khi mỗi kỹ thuật preprocessing chỉ giải quyết một nhóm vấn đề nhất định. Do đó, động lực chính của nghiên cứu là xây dựng một cách tiếp cận có hệ thống để hiểu, lựa chọn và kết hợp các phương pháp preprocessing phù hợp với đặc tính của dữ liệu và mục tiêu của bài toán.

## 1.3.1. Nhu cầu hệ thống hóa các phương pháp preprocessing

Một trong những khó khăn chính của preprocessing time series là số lượng kỹ thuật ngày càng đa dạng và chúng thường được trình bày riêng biệt trong các nghiên cứu khác nhau. Data cleaning, transformation, feature engineering, feature selection, sensor fusion và data compression có thể được xem xét như những nhóm phương pháp độc lập, nhưng trong một pipeline thực tế chúng có quan hệ phụ thuộc lẫn nhau.

Do đó, nghiên cứu cần một taxonomy thống nhất để trả lời ba câu hỏi cơ bản:

1. **Dữ liệu đang gặp vấn đề gì?**
2. **Phương pháp nào có thể giải quyết vấn đề đó?**
3. **Phương pháp được lựa chọn ảnh hưởng như thế nào đến các bước tiếp theo?**

Taxonomy được xây dựng ở Chương 2 sẽ đóng vai trò như cấu trúc điều hướng cho toàn bộ khảo sát. Các nhóm phương pháp trong taxonomy sau đó được phân tích chi tiết ở Chương 3 đến Chương 8.

---

## 1.3.2. Nhu cầu bảo toàn đặc tính thời gian của dữ liệu

Preprocessing dữ liệu chuỗi thời gian khác với preprocessing dữ liệu độc lập bởi vì mỗi quan sát không hoàn toàn độc lập với các quan sát khác. Một phép biến đổi có thể cải thiện chất lượng dữ liệu ở một khía cạnh nhưng đồng thời làm thay đổi temporal structure.

Với một chuỗi thời gian:

$$
X = {x_1, x_2, \ldots, x_T},
$$

giá trị tại thời điểm $t$ có thể phụ thuộc vào lịch sử:

$$
x_t = f(x_{t-1}, x_{t-2}, \ldots) + \epsilon_t.
$$

Do đó, preprocessing cần duy trì thông tin cần thiết để mô hình có thể học được quan hệ:

$$
X_{1:t} \rightarrow Y_{t+h},
$$

trong đó $h$ là forecasting horizon.

Động lực này đặc biệt quan trọng đối với các bước như imputation, outlier detection, decomposition, lag construction và rolling statistics. Một phương pháp chỉ tối ưu theo từng observation có thể không phù hợp khi temporal dependency là thành phần quan trọng của bài toán.

Vì vậy, nghiên cứu không chỉ xem xét **data quality** mà còn xem xét **temporal integrity** của dữ liệu sau preprocessing.

---

## 1.3.3. Nhu cầu kiểm soát data leakage

Một động lực quan trọng khác xuất phát từ nguy cơ **data leakage** trong preprocessing. Trong bài toán dự báo chuỗi thời gian, dữ liệu tương lai không được phép ảnh hưởng đến quá trình xây dựng biểu diễn của dữ liệu quá khứ.

Giả sử dữ liệu được chia theo thứ tự thời gian thành:

$$
D = D_{\mathrm{train}} \cup D_{\mathrm{val}} \cup D_{\mathrm{test}},
$$

với:

$$
t_{\mathrm{train}} < t_{\mathrm{val}} < t_{\mathrm{test}}.
$$

Các tham số của preprocessing phải được học từ tập huấn luyện:

$$
\theta_{\mathrm{prep}}=\operatorname{Fit}(D_{\mathrm{train}}),
$$

sau đó được áp dụng cho các tập còn lại:

$$
D_{\mathrm{val}}'=\operatorname{Transform}(D_{\mathrm{val}};\theta_{\mathrm{prep}}),
$$

$$
D_{\mathrm{test}}'=\operatorname{Transform}(D_{\mathrm{test}};\theta_{\mathrm{prep}}).
$$

Nguyên tắc này đặc biệt quan trọng đối với scaling, normalization, imputation, feature selection và các phương pháp sử dụng thống kê của dữ liệu. Nếu preprocessing sử dụng thông tin từ validation hoặc test set, kết quả đánh giá có thể trở nên lạc quan giả tạo và không phản ánh khả năng tổng quát hóa thực tế.

Do đó, nghiên cứu hướng đến việc xem **data leakage prevention là một nguyên tắc xuyên suốt pipeline**, thay vì chỉ là một bước kiểm tra ở cuối quá trình.

---

## 1.3.4. Nhu cầu cân bằng giữa chất lượng dữ liệu và thông tin

Preprocessing luôn tồn tại một trade-off giữa **loại bỏ các thành phần không mong muốn** và **bảo toàn thông tin hữu ích**.

Có thể biểu diễn mục tiêu khái quát của preprocessing như:

$$\max_{\mathcal{P}} \quad Q(X_{\mathcal{P}})$$

với ràng buộc:

$$I(X_{\mathcal{P}};Y) \approx I(X;Y)$$

trong đó:

* $\mathcal{P}$ là preprocessing pipeline;
* $X_{\mathcal{P}}$ là dữ liệu sau preprocessing;
* $Q(\cdot)$ biểu diễn chất lượng hoặc mức độ phù hợp của dữ liệu;
* $I(\cdot;\cdot)$ là mutual information;
* $Y$ là biến mục tiêu.

Mục tiêu không phải đơn giản là làm cho dữ liệu "sạch hơn". Một preprocessing tốt cần loại bỏ hoặc giảm ảnh hưởng của những thành phần gây hại nhưng đồng thời giữ lại thông tin có ích cho nhiệm vụ downstream.

Ví dụ, một giá trị bất thường có thể là:

* lỗi cảm biến;
* nhiễu đo lường;
* hoặc một sự kiện thực tế quan trọng.

Nếu mọi outlier đều bị loại bỏ, preprocessing có thể làm mất thông tin quan trọng. Tương tự, smoothing quá mạnh có thể làm giảm noise nhưng đồng thời làm mất peak hoặc thay đổi đặc điểm của tín hiệu.

Đây là lý do nghiên cứu cần phân tích **trade-off** của từng phương pháp thay vì chỉ liệt kê ưu điểm và nhược điểm.

---

## 1.3.5. Nhu cầu giảm độ phức tạp của dữ liệu

Khi feature engineering được mở rộng, số lượng đặc trưng có thể tăng nhanh:

$$F_{\mathrm{engineered}} \gg F_{\mathrm{raw}}.$$

Số chiều lớn không nhất thiết đồng nghĩa với lượng thông tin hữu ích lớn hơn. Một tập đặc trưng có thể chứa nhiều biến dư thừa, tương quan cao hoặc không liên quan đến mục tiêu.

Điều này tạo động lực cho việc nghiên cứu **feature selection** và **dimensionality reduction** trong Chương 6. Mục tiêu là tìm một biểu diễn có kích thước hợp lý nhưng vẫn giữ được phần lớn thông tin cần thiết cho nhiệm vụ downstream.

Về mặt khái quát, feature selection có thể được biểu diễn:

$$X = [x_1,x_2,\ldots,x_F] \rightarrow X_S, \qquad S \subseteq {1,\ldots,F}$$

trong đó $X_S$ chỉ chứa các đặc trưng được lựa chọn.

Động lực ở đây không chỉ là giảm computational cost mà còn hướng đến việc cải thiện khả năng diễn giải, giảm redundancy và hạn chế overfitting.

---

## 1.3.6. Nhu cầu thích nghi với hệ thống IoT và Edge AI

Trong các hệ thống IoT, dữ liệu thường được tạo ra liên tục từ nhiều sensor và có thể cần được xử lý ngay tại edge device trước khi truyền đến hệ thống trung tâm. Điều này tạo ra các ràng buộc về:

* computational resources;
* memory;
* storage;
* bandwidth;
* latency;
* energy consumption.

Do đó, preprocessing không chỉ cần quan tâm đến chất lượng dữ liệu mà còn phải xem xét **chi phí thực thi**.

Data compression có thể giảm lượng dữ liệu cần lưu trữ hoặc truyền tải:

$$R = \frac{S_{\mathrm{compressed}}} {S_{\mathrm{original}}}$$

trong đó $R$ là compression ratio.

Tuy nhiên, giảm kích thước dữ liệu quá mức có thể làm mất thông tin quan trọng. Vì vậy, Chương 8 sẽ xem xét lossless compression, lossy compression và các yêu cầu đặc thù của Edge/IoT trong mối quan hệ với chất lượng dữ liệu.

---

## 1.3.7. Nhu cầu đánh giá preprocessing theo tác động downstream

Một preprocessing method không nên chỉ được đánh giá dựa trên mức độ thay đổi của dữ liệu đầu vào. Giá trị thực tế của nó cuối cùng được thể hiện thông qua tác động đến nhiệm vụ downstream.

Có thể mô tả quan hệ tổng quát:

$$X_{\mathrm{raw}} \xrightarrow{\mathcal{P}} X_{\mathrm{processed}} \xrightarrow{\mathcal{M}} \hat{Y}$$

trong đó $\mathcal{P}$ là preprocessing pipeline và $\mathcal{M}$ là mô hình AI.

Hiệu quả của preprocessing do đó cần được đánh giá theo ít nhất ba khía cạnh:

1. **Data quality:** dữ liệu sau xử lý có giảm các vấn đề về chất lượng hay không?
2. **Computational efficiency:** preprocessing có làm tăng hoặc giảm chi phí tính toán, lưu trữ và truyền tải hay không?
3. **Downstream performance:** mô hình sử dụng dữ liệu sau preprocessing có cải thiện kết quả hay không?

Cách tiếp cận này là cơ sở cho Chương 9, nơi các phương pháp được đưa vào một experimental setup thống nhất và đánh giá bằng các metric phù hợp.

---

## 1.3.8. Định hướng từ khảo sát phương pháp đến preprocessing pipeline

Các động lực trên dẫn đến một định hướng chung: nghiên cứu không dừng ở việc tổng hợp từng kỹ thuật preprocessing riêng lẻ mà hướng đến việc xây dựng một **pipeline có cấu trúc** từ dữ liệu thô đến dữ liệu sẵn sàng cho AI.

Pipeline tổng quát được biểu diễn:

$$
X_{\mathrm{raw}}
\rightarrow
\text{Cleaning}
\rightarrow
\text{Transformation}
\rightarrow
\text{Feature Engineering}
\rightarrow
\text{Feature Selection}
\rightarrow
X_{\mathrm{AI}}.
$$

Tùy vào bài toán, pipeline có thể mở rộng thêm sensor fusion hoặc data compression:

$$
X_{\mathrm{raw}}
\rightarrow
\text{Cleaning}
\rightarrow
\text{Transformation}
\rightarrow
\text{Feature Engineering}
\rightarrow
\text{Feature Selection}
\rightarrow
\text{Fusion/Compression}
\rightarrow
X_{\mathrm{AI}}.
$$

Pipeline này không được xem là một thứ tự bắt buộc cho mọi bài toán. Thứ tự và sự xuất hiện của từng bước phụ thuộc vào đặc tính dữ liệu, mục tiêu phân tích và yêu cầu của hệ thống. Chính vì vậy, nghiên cứu tập trung vào **nguyên tắc lựa chọn và tổ chức phương pháp**, thay vì đề xuất một pipeline cố định.

Các động lực trên tạo nền tảng trực tiếp cho **Mục 1.4 — Contributions**, trong đó nghiên cứu sẽ xác định cụ thể những đóng góp đạt được từ việc hệ thống hóa, phân loại, so sánh và kiểm chứng các phương pháp preprocessing. Đồng thời, các động lực này cũng giải thích cấu trúc của toàn bộ nghiên cứu: từ taxonomy ở Chương 2, các nhóm phương pháp ở Chương 3--8, đánh giá thực nghiệm ở Chương 9, phân tích trade-off ở Chương 10 đến pipeline tổng hợp ở Chương 11.
