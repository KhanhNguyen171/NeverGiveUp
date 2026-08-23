# Dataset

## 1. Tổng quan dữ liệu

Phần thực nghiệm sử dụng các dataset chuỗi thời gian thực tế nhằm đánh giá ảnh hưởng của các phương pháp preprocessing đến chất lượng dữ liệu và hiệu quả của mô hình học máy. Việc lựa chọn dataset tập trung vào các bộ dữ liệu có đặc trưng điển hình của time-series, bao gồm quan sát theo thời gian, nhiều biến liên quan, khả năng xuất hiện missing values, noise, outliers, xu hướng và tính mùa vụ.

Dataset chính được sử dụng trong nghiên cứu thực nghiệm là **Air Quality Data Set**, được xây dựng từ dữ liệu quan trắc chất lượng không khí tại một khu vực đô thị ở Ý. Dataset cung cấp các phép đo liên tục từ nhiều cảm biến hóa học và các biến khí tượng theo thời gian, do đó phù hợp để đánh giá nhiều nhóm preprocessing được khảo sát trong survey.

Dataset được lựa chọn vì có đồng thời ba đặc điểm quan trọng:

1. dữ liệu có cấu trúc thời gian rõ ràng;
2. nhiều biến có quan hệ phụ thuộc với nhau;
3. dữ liệu cảm biến tồn tại các vấn đề thực tế cần preprocessing trước khi đưa vào mô hình học máy.

Những đặc điểm này cho phép đánh giá preprocessing trong điều kiện gần với các bài toán time-series thực tế thay vì chỉ sử dụng dữ liệu nhân tạo hoặc dữ liệu đã được làm sạch hoàn toàn.

---

## 2. Cấu trúc dữ liệu

Mỗi quan sát trong dataset được gắn với một timestamp và một vector các thuộc tính đo được:

$$
\mathbf{z}_t=

\left(
t,
\mathbf{x}_t
\right),
$$

trong đó $t$ biểu diễn thời điểm quan sát và

$$
\mathbf{x}_t=

[x_t^{(1)},x_t^{(2)},\ldots,x_t^{(d)}]
$$

là vector gồm $d$ biến tại thời điểm $t$.

Với toàn bộ dataset:

$$
\mathcal{D}=

\left \{
(t_i,\mathbf{x}_i)
\right \}_{i=1}^{N},
$$

trong đó $N$ là số lượng quan sát.

Các biến trong Air Quality dataset bao gồm các phép đo liên quan đến chất lượng không khí và điều kiện khí tượng. Các biến ô nhiễm chính được đo bởi hệ thống cảm biến bao gồm nồng độ của các chất khí như CO, NMHC, C6H6, NOx và NO2, cùng với các biến nhiệt độ, độ ẩm và các đại lượng khí tượng liên quan.

Do các cảm biến hoạt động đồng thời, các biến trong $\mathbf{x}_t$ không độc lập hoàn toàn. Sự phụ thuộc giữa các biến tạo điều kiện để đánh giá các phương pháp transformation, feature engineering, feature selection và dimensionality reduction.

---

## 3. Đặc trưng thời gian

Timestamp là thành phần quan trọng của dataset vì các quan sát không chỉ được xem như một tập dữ liệu dạng bảng mà còn biểu diễn một quá trình diễn ra theo thời gian.

Từ timestamp, có thể biểu diễn dữ liệu dưới dạng chuỗi:

$$
\mathbf{X}=

\left[
\mathbf{x}_1,
\mathbf{x}_2,
\ldots,
\mathbf{x}_N
\right]^{\top},
$$

với thứ tự của các hàng được bảo toàn theo thời gian.

Cấu trúc này cho phép phân tích các đặc điểm như:

* temporal dependence;
* trend;
* periodicity;
* seasonal variation;
* autocorrelation;
* temporal gaps.

Các đặc điểm trên đặc biệt quan trọng đối với các phương pháp được trình bày trong [05_feature_engineering](../05_feature_engineering/), chẳng hạn temporal features, lag features và rolling features.

---

## 4. Các vấn đề dữ liệu được xem xét

Dataset cảm biến được sử dụng để đánh giá preprocessing vì dữ liệu thực tế có thể chứa nhiều dạng bất thường.

### 4.1. Missing values

Một số phép đo cảm biến có thể không tồn tại hoặc được biểu diễn bằng các giá trị đặc biệt. Missing data được biểu diễn tổng quát bởi:

$$
x_t^{(j)} = \mathrm{NaN},
$$

với $j$ là chỉ số của biến và $t$ là thời điểm quan sát.

Missing values là cơ sở để đánh giá các phương pháp được trình bày trong [01_missing_data.md](../03_data_cleaning/01_missing_data.md).

---

### 4.2. Outliers

Các cảm biến có thể tạo ra các quan sát khác biệt đáng kể so với phân phối thông thường:

$$
x_t^{(j)}
\notin
\mathcal{R}_{\mathrm{normal}}^{(j)}.
$$

Các quan sát này có thể xuất phát từ nhiễu cảm biến, lỗi đo hoặc các sự kiện môi trường thực sự.

Do đó, outlier không mặc nhiên được xem là lỗi. Việc loại bỏ một quan sát cực trị chỉ được thực hiện khi có đủ cơ sở cho thấy quan sát đó không đại diện cho quá trình sinh dữ liệu.

---

### 4.3. Noise

Dữ liệu cảm biến thường chứa thành phần nhiễu:

$$
x_t
=

s_t+\epsilon_t,
$$

trong đó $s_t$ là tín hiệu có cấu trúc và $\epsilon_t$ là thành phần nhiễu.

Noise reduction nhằm giảm $\epsilon_t$ nhưng đồng thời phải hạn chế làm mất các biến động có ý nghĩa của $s_t$. Đây là lý do noise reduction được đánh giá riêng với outlier detection trong [03_noise_reduction.md](../03_data_cleaning/03_noise_reduction.md).

---

### 4.4. Khác biệt về thang đo

Các biến có thể có miền giá trị rất khác nhau:

$$
x^{(j)}
\in
[a_j,b_j].
$$

Khi độ lớn giữa các biến khác biệt đáng kể, một số thuật toán có thể bị chi phối bởi các biến có magnitude lớn hơn.

Do đó, scaling và normalization được xem xét như một nhóm preprocessing độc lập trong [01_scaling_normalization.md](../04_data_transformation/01_scaling_normalization.md).

---

## 5. Tiền xử lý ban đầu

Trước khi áp dụng các phương pháp được đánh giá, dữ liệu cần được chuyển về một representation thống nhất.

Quy trình ban đầu gồm:

$$
\text{Raw Dataset}
\rightarrow
\text{Timestamp Parsing}
\rightarrow
\text{Data Type Validation}
\rightarrow
\text{Missing-value Identification}
\rightarrow
\text{Basic Quality Check}.
$$

Các bước này chỉ nhằm đảm bảo dữ liệu có thể được sử dụng trong pipeline thực nghiệm và không được xem là một phương pháp cạnh tranh trong comparison.

Đặc biệt, timestamp phải được chuyển sang representation thời gian thống nhất trước khi thực hiện các thao tác phụ thuộc vào thứ tự thời gian.

---

## 6. Chia dữ liệu

Dữ liệu được chia theo thứ tự thời gian như đã quy định trong [01_experimental_setup.md](01_experimental_setup.md).

$$
\mathcal{D}=

\mathcal{D}*{\mathrm{train}}
\cup
\mathcal{D}*{\mathrm{val}}
\cup
\mathcal{D}_{\mathrm{test}},
$$

với

$$
\mathcal{D}*{\mathrm{train}}
\prec
\mathcal{D}*{\mathrm{val}}
\prec
\mathcal{D}_{\mathrm{test}}.
$$

Không thực hiện random split nhằm tránh việc các quan sát ở tương lai xuất hiện trong tập huấn luyện.

Các tham số của preprocessing có khả năng học từ dữ liệu chỉ được ước lượng trên $\mathcal{D}_{\mathrm{train}}$. Validation được sử dụng để lựa chọn cấu hình, trong khi test được giữ độc lập cho đánh giá cuối cùng.

---

## 7. Dataset và các nhóm preprocessing

Air Quality dataset được sử dụng như một môi trường thực nghiệm thống nhất để khảo sát nhiều nhóm preprocessing.

| Đặc điểm dữ liệu         | Nhóm phương pháp liên quan       |
| ------------------------ | -------------------------------- |
| Missing observations     | Missing-data handling            |
| Giá trị cực trị          | Outlier detection                |
| Nhiễu cảm biến           | Noise reduction                  |
| Khác biệt thang đo       | Scaling / normalization          |
| Phân phối lệch           | Data transformation              |
| Temporal dependence      | Temporal features / lag features |
| Biến động theo cửa sổ    | Rolling features                 |
| Nhiều biến tương quan    | Feature selection                |
| Không gian đặc trưng lớn | Dimensionality reduction         |

Cách ánh xạ này cho phép dataset đóng vai trò cầu nối giữa taxonomy lý thuyết và đánh giá thực nghiệm. Mỗi phương pháp được lựa chọn dựa trên một vấn đề dữ liệu cụ thể thay vì áp dụng toàn bộ preprocessing pipeline một cách tùy ý.

---

## 8. Vai trò của dataset trong nghiên cứu

Dataset không được sử dụng để chứng minh rằng một preprocessing method luôn tốt hơn các phương pháp khác. Thay vào đó, nó cung cấp một môi trường thực nghiệm để kiểm tra các giả thuyết về mối quan hệ giữa **đặc điểm dữ liệu**, **phương pháp preprocessing** và **hiệu quả mô hình**.

Có thể mô hình hóa mối quan hệ này như sau:

$$
\text{Dataset Characteristics}
\rightarrow
\text{Preprocessing Choice}
\rightarrow
\text{Data Representation}
\rightarrow
\text{Model Performance}.
$$

Do đó, kết quả thu được cần được diễn giải trong phạm vi đặc điểm của dataset. Một phương pháp có thể cải thiện kết quả trên dữ liệu cảm biến nhưng không nhất thiết đạt hiệu quả tương tự trên các loại time-series khác như tài chính, năng lượng hoặc giao thông.

Vấn đề về khả năng khái quát hóa này được thảo luận tiếp trong [10_discussion/03_limitations.md](../10_discussion/03_limitations.md).

---

## 9. Liên kết với thực nghiệm UCI Appliances

Ngoài dataset được sử dụng trong empirical analysis, nghiên cứu còn có một case study riêng trên **UCI Appliances Energy Prediction dataset**, được trình bày trong [Chương 13](../13_uci_appliances/01_dataset.md).

Hai phần có vai trò khác nhau:

* **Chương 9** sử dụng dataset thực nghiệm để đánh giá và so sánh các nhóm preprocessing trong phạm vi survey.
* **Chương 13** sử dụng UCI Appliances như một case study cụ thể để minh họa cách chuyển các nguyên tắc preprocessing thành một pipeline hoàn chỉnh cho bài toán forecasting.

Vì vậy, Chương 13 không thay thế cho empirical analysis của Chương 9 mà đóng vai trò **application-oriented case study**, giúp kiểm tra khả năng áp dụng các kết luận của survey vào một bài toán time-series forecasting thực tế.

---

## 10. Tóm tắt

Dataset được lựa chọn phải đồng thời thể hiện được cấu trúc thời gian và các vấn đề dữ liệu thường gặp trong thực tế. Air Quality dataset đáp ứng yêu cầu này thông qua dữ liệu cảm biến đa biến, temporal dependence và các vấn đề liên quan đến chất lượng phép đo.

Trong thiết kế thực nghiệm, dataset được giữ nguyên thứ tự thời gian, chia thành training, validation và test theo chronological split, đồng thời kiểm soát data leakage trong toàn bộ preprocessing pipeline.

Do đó, dataset cung cấp nền tảng để thực hiện chuỗi đánh giá:

$$
\boxed{
\text{Data Characteristics}
\rightarrow
\text{Preprocessing Methods}
\rightarrow
\text{Feature Representation}
\rightarrow
\text{Predictive Evaluation}
}
$$

Kết quả cụ thể của từng preprocessing method và cấu hình thực nghiệm được trình bày trong [03_preprocessing_methods.md](03_preprocessing_methods.md) và [05_results.md](05_results.md).
