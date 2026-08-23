# Experimental Setup

## 1. Mục tiêu thực nghiệm

Phần thực nghiệm được thiết kế nhằm đánh giá một cách có hệ thống ảnh hưởng của các phương pháp **tiền xử lý dữ liệu chuỗi thời gian** đến chất lượng dữ liệu đầu vào và hiệu quả của các mô hình học máy. Trọng tâm của thực nghiệm không chỉ là so sánh độ chính xác dự báo, mà còn là xác định **khi nào, trong điều kiện nào và với mục đích gì** một nhóm phương pháp tiền xử lý có thể cải thiện kết quả mô hình.

Theo định hướng của nghiên cứu, quy trình thực nghiệm được tổ chức thành một pipeline thống nhất:

$$
\text{Raw Data}
\rightarrow
\text{Data Cleaning}
\rightarrow
\text{Data Transformation}
\rightarrow
\text{Feature Engineering}
\rightarrow
\text{Feature Selection}
\rightarrow
\text{Modeling}
\rightarrow
\text{Evaluation}.
$$

Cách tổ chức này cho phép tách biệt tương đối tác động của từng nhóm phương pháp, đồng thời tạo cơ sở để liên kết kết quả thực nghiệm với taxonomy được trình bày trong [Chương 2](../02_overview/02_taxonomy.md).

---

## 2. Thiết kế thực nghiệm

Thực nghiệm sử dụng dữ liệu chuỗi thời gian thực tế, trong đó mỗi quan sát được biểu diễn dưới dạng

$$
\mathbf{z}_t =
\left[
y_t,
\mathbf{x}_t
\right],
$$

với $y_t$ là biến mục tiêu và $\mathbf{x}_t$ là vector các biến đầu vào tại thời điểm $t$.

Do dữ liệu có cấu trúc thời gian, việc chia dữ liệu được thực hiện theo thứ tự thời gian thay vì lấy mẫu ngẫu nhiên. Với chuỗi có $N$ quan sát, dữ liệu được chia thành ba tập:

$$
\mathcal{D}=

\mathcal{D}*{\mathrm{train}}
\cup
\mathcal{D}*{\mathrm{val}}
\cup
\mathcal{D}_{\mathrm{test}},
$$

trong đó

$$
\mathcal{D}*{\mathrm{train}}
\prec
\mathcal{D}*{\mathrm{val}}
\prec
\mathcal{D}_{\mathrm{test}}.
$$

Ký hiệu $\prec$ thể hiện rằng các tập dữ liệu được sắp xếp theo trình tự thời gian và không có sự xáo trộn giữa chúng.

Thiết kế này tránh hiện tượng **temporal leakage**, trong đó thông tin từ tương lai vô tình được sử dụng trong quá trình huấn luyện hoặc lựa chọn phương pháp tiền xử lý.

---

## 3. Các nhóm phương pháp được đánh giá

Dựa trên taxonomy của nghiên cứu, các phương pháp tiền xử lý được phân thành các nhóm chính:

1. **Data cleaning**: xử lý giá trị thiếu, phát hiện và xử lý ngoại lệ, giảm nhiễu.
2. **Data transformation**: scaling, normalization, transformation và xử lý tính dừng.
3. **Decomposition**: phân rã chuỗi thành các thành phần có cấu trúc đơn giản hơn.
4. **Feature engineering**: xây dựng đặc trưng thời gian, lag, rolling và các biểu diễn đặc trưng.
5. **Feature selection**: lựa chọn các biến có thông tin hữu ích và giảm dư thừa.
6. **Dimensionality reduction**: ánh xạ không gian đặc trưng ban đầu sang không gian có số chiều thấp hơn.

Các nhóm này không nhất thiết được áp dụng đồng thời trong mọi thí nghiệm. Mỗi phương pháp được đánh giá trong bối cảnh phù hợp với đặc điểm dữ liệu và mục tiêu xử lý tương ứng.

Ví dụ, scaling chủ yếu tác động đến miền giá trị của biến, trong khi feature selection tác động đến số lượng và thành phần của biến đầu vào. Vì vậy, hai nhóm phương pháp này được xem là các bước xử lý khác nhau thay vì được gộp thành một phép biến đổi duy nhất.

---

## 4. Baseline và các cấu hình so sánh

Một **baseline pipeline** được xây dựng từ dữ liệu sau các bước xử lý tối thiểu cần thiết. Baseline đóng vai trò mốc tham chiếu để xác định mức cải thiện hoặc suy giảm khi bổ sung một phương pháp tiền xử lý.

Với một mô hình $f_\theta$, dự báo của baseline được biểu diễn bởi

$$
\widehat{y}_t^{,\mathrm{base}}=

f_{\theta}
\left(
\mathbf{x}_t^{,\mathrm{base}}
\right).
$$

Khi áp dụng một phương pháp tiền xử lý $P$, dữ liệu đầu vào trở thành

$$
\mathbf{x}_t^{(P)}=

P(\mathbf{x}_t),
$$

và dự báo tương ứng là

$$
\widehat{y}_t^{(P)}=

f_{\theta^{(P)}}
\left(
\mathbf{x}_t^{(P)}
\right).
$$

Hiệu quả của phương pháp được đánh giá thông qua sự thay đổi của các chỉ số đánh giá so với baseline:

$$
\Delta M=

M^{(P)}-M^{(\mathrm{base})},
$$

trong đó $M$ là một metric được sử dụng trong thực nghiệm.

Đối với các metric lỗi như MAE hoặc RMSE, giá trị $\Delta M<0$ cho thấy phương pháp $P$ cải thiện kết quả dự báo.

---

## 5. Nguyên tắc tránh data leakage

Một yêu cầu quan trọng của thiết kế thực nghiệm là **mọi tham số học được từ dữ liệu phải được xác định chỉ trên tập huấn luyện**.

Ví dụ, với phép chuẩn hóa Standardization:

$$
x_t'=
\frac{x_t-\mu}{\sigma},
$$

các tham số

$$
\mu=

\frac{1}{N_{\mathrm{train}}}
\sum_{t\in\mathcal{D}_{\mathrm{train}}}x_t
$$

và

$$
\sigma=

\sqrt{
\frac{1}{N_{\mathrm{train}}}
\sum_{t\in\mathcal{D}_{\mathrm{train}}}
(x_t-\mu)^2
}
$$

chỉ được ước lượng từ $\mathcal{D}_{\mathrm{train}}$.

Sau đó, cùng một phép biến đổi được áp dụng cho validation và test:

$$
\mathbf{X}_{\mathrm{val}}'=

P_{\mathrm{train}}(\mathbf{X}_{\mathrm{val}}),
$$

$$
\mathbf{X}_{\mathrm{test}}'=

P_{\mathrm{train}}(\mathbf{X}_{\mathrm{test}}).
$$

Nguyên tắc tương tự được áp dụng cho imputation, feature selection, dimensionality reduction và các phương pháp có tham số cần ước lượng từ dữ liệu. Việc sử dụng toàn bộ dataset để xác định tham số preprocessing trước khi chia dữ liệu có thể làm cho kết quả thực nghiệm lạc quan giả tạo.

---

## 6. Temporal validation

Do đối tượng nghiên cứu là dữ liệu chuỗi thời gian, validation được thực hiện theo thứ tự thời gian. Không sử dụng random shuffle khi phân chia dữ liệu thành training, validation và test.

Một cấu hình tổng quát có dạng:

$$
\mathcal{D}_{\mathrm{train}}=

{1,\ldots,t_1},
$$

$$
\mathcal{D}_{\mathrm{val}}=

{t_1+1,\ldots,t_2},
$$

$$
\mathcal{D}_{\mathrm{test}}=

{t_2+1,\ldots,N}.
$$

Validation được sử dụng để lựa chọn phương pháp tiền xử lý, cấu hình mô hình và hyperparameters. Tập test chỉ được sử dụng ở bước đánh giá cuối cùng.

Cách thiết kế này phù hợp với bản chất forecasting, trong đó mục tiêu thực tế là sử dụng dữ liệu quá khứ để dự đoán các quan sát trong tương lai.

---

## 7. Mô hình dự báo

Các phương pháp preprocessing được đánh giá thông qua tác động của chúng đến một hoặc nhiều mô hình dự báo đại diện. Mô hình nhận đầu vào đã qua preprocessing và tạo ra dự báo:

$$
\widehat{y}_{t+h}=

f_\theta
\left(
\mathbf{X}_{t-L+1:t}
\right),
$$

trong đó $L$ là độ dài cửa sổ quan sát và $h$ là forecasting horizon.

Đối với dữ liệu chuỗi thời gian, biểu diễn dạng cửa sổ cho phép mô hình khai thác thông tin lịch sử thay vì xem mỗi quan sát là một mẫu độc lập.

Việc giữ cấu trúc đầu vào và quy trình đánh giá nhất quán giữa các cấu hình giúp giảm khả năng kết quả khác biệt chỉ xuất phát từ thay đổi kiến trúc mô hình thay vì từ phương pháp preprocessing.

---

## 8. Đánh giá

Hiệu quả của các pipeline được đánh giá trên tập validation trong quá trình lựa chọn và trên tập test sau khi cấu hình cuối cùng được xác định.

Đối với bài toán hồi quy, các metric chính gồm MAE, RMSE và $R^2$.

Mean Absolute Error:

$$
\mathrm{MAE}=

\frac{1}{N}
\sum_{i=1}^{N}
\left|
y_i-\widehat{y}_i
\right|.
$$

Root Mean Squared Error:

$$
\mathrm{RMSE}=

\sqrt{
\frac{1}{N}
\sum_{i=1}^{N}
\left(
y_i-\widehat{y}_i
\right)^2
}.
$$

Coefficient of Determination:

$$
R^2=

1-
\frac{
\sum_{i=1}^{N}
(y_i-\widehat{y}*i)^2
}{
\sum*{i=1}^{N}
(y_i-\bar{y})^2
}.
$$

MAE phản ánh sai số tuyệt đối trung bình, RMSE nhạy hơn với các sai số lớn, trong khi $R^2$ đánh giá mức độ biến thiên của biến mục tiêu được giải thích bởi mô hình.

Khi so sánh các phương pháp preprocessing, không sử dụng một metric duy nhất để đưa ra kết luận. Kết quả cần được xem xét đồng thời theo **độ chính xác, độ phức tạp, số chiều dữ liệu, khả năng bảo toàn thông tin và chi phí tính toán**.

---

## 9. Phân tích tác động của preprocessing

Thiết kế thực nghiệm tập trung vào hai câu hỏi:

* Phương pháp preprocessing có cải thiện hiệu quả dự báo hay không?
* Mức cải thiện có đi kèm với chi phí hoặc mất mát thông tin đáng kể hay không?

Do đó, kết quả không chỉ được biểu diễn bằng metric dự báo mà còn được xem xét theo các đặc tính của dữ liệu sau preprocessing.

Một phương pháp được xem là có lợi khi nó đạt được sự cân bằng hợp lý giữa:

$$
\text{Predictive Performance}
\quad\leftrightarrow\quad
\text{Information Preservation}
\quad\leftrightarrow\quad
\text{Computational Cost}.
$$

Cách tiếp cận này phù hợp với mục tiêu của survey: không tìm kiếm một phương pháp preprocessing tối ưu cho mọi dataset, mà xác định **trade-off và điều kiện lựa chọn phương pháp** dựa trên đặc điểm của dữ liệu và bài toán.

---

## 10. Liên kết với các phần tiếp theo

Thiết kế thực nghiệm trong mục này là cơ sở cho các phần còn lại của [Chương 9](../09_empirical_analysis/):

* [02_dataset.md](02_dataset.md) mô tả các dataset được sử dụng và đặc điểm dữ liệu;
* [03_preprocessing_methods.md](03_preprocessing_methods.md) xác định cụ thể các phương pháp preprocessing được đưa vào thực nghiệm;
* [04_evaluation_metrics.md](04_evaluation_metrics.md) trình bày chi tiết các tiêu chí đánh giá;
* [05_results.md](05_results.md) trình bày kết quả định lượng và so sánh giữa các cấu hình;
* [06_findings.md](06_findings.md) tổng hợp các phát hiện thực nghiệm và liên hệ với taxonomy của survey.

Như vậy, chương thực nghiệm được tổ chức theo chuỗi logic:

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

Cấu trúc này đảm bảo kết quả thực nghiệm có thể truy nguyên từ dữ liệu và phương pháp preprocessing đến metric đánh giá, đồng thời tạo cơ sở cho phần thảo luận về trade-off và giới hạn nghiên cứu ở [Chương 10](../10_discussion/01_comparison.md).
