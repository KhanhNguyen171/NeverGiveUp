# 7.2. Fusion Levels

Sau khi xác định sensor fusion là quá trình kết hợp thông tin từ nhiều nguồn cảm biến, vấn đề tiếp theo là **xác định dữ liệu được kết hợp ở mức nào**. Fusion level mô tả vị trí trong pipeline mà thông tin từ các cảm biến được tích hợp. Đây là một quyết định quan trọng vì mức độ fusion ảnh hưởng trực tiếp đến lượng thông tin được giữ lại, khả năng xử lý nhiễu, độ phức tạp tính toán và yêu cầu đối với mô hình phía sau.

Một cách phân loại phổ biến gồm ba mức chính:

1. **Data-level fusion** — kết hợp dữ liệu quan sát ở mức dữ liệu thô.
2. **Feature-level fusion** — trích xuất đặc trưng từ từng nguồn rồi kết hợp các đặc trưng.
3. **Decision-level fusion** — mỗi nguồn được xử lý độc lập và chỉ kết hợp các kết quả dự đoán hoặc quyết định cuối cùng.

Có thể khái quát:

$$
\text{Raw Data}
\xrightarrow{\text{Data-level Fusion}}
\text{Unified Data}
$$

$$
\text{Raw Data}
\xrightarrow{\text{Feature Extraction}}
\text{Features}
\xrightarrow{\text{Feature-level Fusion}}
\text{Unified Representation}
$$

$$
\text{Raw Data}
\xrightarrow{\text{Independent Models}}
\text{Predictions}
\xrightarrow{\text{Decision-level Fusion}}
\text{Final Decision}.
$$

Ba mức này không phải là các phương pháp hoàn toàn loại trừ nhau. Trong một hệ thống thực tế, chúng có thể được kết hợp thành một **hybrid fusion architecture** tùy thuộc vào đặc điểm dữ liệu và mục tiêu của bài toán.

---

## 7.2.1. Data-Level Fusion

**Data-level fusion** kết hợp trực tiếp các quan sát từ nhiều cảm biến trước khi thực hiện feature extraction hoặc mô hình hóa.

Giả sử có $M$ cảm biến, tại thời điểm $t$ cảm biến thứ $m$ tạo ra vector:

$$
\mathbf{x}_t^{(m)}
\in
\mathbb{R}^{d_m}.
$$

Sau khi temporal alignment, các vector này có thể được nối theo chiều đặc trưng:

$$
\mathbf{x}_t=

\left[
\mathbf{x}_t^{(1)}
\Vert
\mathbf{x}_t^{(2)}
\Vert
\cdots
\Vert
\mathbf{x}_t^{(M)}
\right],
$$

trong đó $\Vert$ biểu thị phép concatenation.

Nếu tất cả cảm biến chỉ tạo ra một giá trị tại mỗi thời điểm:

$$
\mathbf{x}_t=

\left[
x_t^{(1)},
x_t^{(2)},
\ldots,
x_t^{(M)}
\right]^\top.
$$

Toàn bộ dữ liệu sau fusion có dạng:

$$
\mathbf{X}
\in
\mathbb{R}^{T\times F},
$$

với $F=\sum_{m=1}^{M}d_m$.

### Ưu điểm

Data-level fusion giữ lại lượng thông tin lớn nhất từ các cảm biến. Các quan hệ tương quan giữa các tín hiệu vẫn có thể được mô hình hóa trực tiếp bởi các bước preprocessing hoặc mô hình học máy phía sau.

Đặc biệt, đối với dữ liệu time series có sampling rate đồng nhất, cách tiếp cận này tương đối đơn giản:

$$
{\mathbf{x}_t^{(1)},\ldots,\mathbf{x}_t^{(M)}}
\rightarrow
\mathbf{x}_t.
$$

### Hạn chế

Nhược điểm chính là **yêu cầu dữ liệu phải tương thích**. Các cảm biến cần được đồng bộ về thời gian, scale và thường cả hệ tọa độ hoặc đơn vị đo. Nếu một nguồn có nhiễu lớn, dữ liệu nhiễu được đưa trực tiếp vào representation chung.

Ngoài ra, số chiều của dữ liệu có thể tăng nhanh khi số lượng cảm biến tăng:

$$
F=\sum_{m=1}^{M}d_m.
$$

Điều này có thể làm tăng chi phí tính toán và tạo ra nhu cầu feature selection hoặc dimensionality reduction ở các bước tiếp theo.

---

## 7.2.2. Feature-Level Fusion

**Feature-level fusion** thực hiện feature extraction hoặc representation learning riêng cho từng nguồn trước khi kết hợp.

Với cảm biến thứ $m$:

$$
\mathbf{h}_t^{(m)}=

f_m\left(\mathbf{x}_t^{(m)}\right),
$$

trong đó $f_m(\cdot)$ là một hàm feature extraction.

Các representation sau đó được kết hợp:

$$
\mathbf{h}_t=

\left[
\mathbf{h}_t^{(1)}
\Vert
\mathbf{h}_t^{(2)}
\Vert
\cdots
\Vert
\mathbf{h}_t^{(M)}
\right].
$$

Cuối cùng, representation hợp nhất được đưa vào mô hình:

$$
\hat{y}_t=

g_\theta(\mathbf{h}_t).
$$

Khác với data-level fusion, các đặc trưng có thể được chuẩn hóa hoặc biến đổi riêng cho từng nguồn trước khi fusion. Điều này đặc biệt hữu ích khi các cảm biến có **phân phối, scale hoặc bản chất vật lý khác nhau**.

Ví dụ, một nguồn có thể được biểu diễn bằng statistical features:

$$
\mathbf{h}^{(1)}=

[
\mu,\sigma,\min,\max
],
$$

trong khi một nguồn time series khác được chuyển thành representation học được bởi neural network:

$$
\mathbf{h}^{(2)}=

f_\theta(\mathbf{x}^{(2)}).
$$

Sau đó:

$$
\mathbf{h}=

[\mathbf{h}^{(1)}\Vert\mathbf{h}^{(2)}].
$$

### Ưu điểm

Feature-level fusion cung cấp sự cân bằng giữa **mức độ thông tin** và **khả năng kiểm soát representation**. Các bước preprocessing có thể được thiết kế riêng cho từng sensor trước khi đưa chúng vào không gian đặc trưng chung.

Điều này cũng giúp giảm dimensionality khi feature extractor biến đổi dữ liệu thô thành representation có kích thước nhỏ hơn:

$$
d_m
\rightarrow
k_m,
\qquad
k_m \ll d_m.
$$

### Hạn chế

Nhược điểm là quá trình feature extraction có thể làm mất một phần thông tin trong dữ liệu thô. Ngoài ra, chất lượng của representation phụ thuộc vào phương pháp trích xuất đặc trưng.

Đối với deep learning, feature-level fusion còn có thể được thực hiện bằng cách sử dụng các encoder riêng cho từng modality:

$$
\mathbf{h}^{(m)}=

f_{\theta_m}
\left(
\mathbf{X}^{(m)}
\right),
$$

sau đó:

$$
\mathbf{h}=

\operatorname{Fusion}
\left(
\mathbf{h}^{(1)},\ldots,\mathbf{h}^{(M)}
\right).
$$

Cách này linh hoạt nhưng làm tăng độ phức tạp của kiến trúc mô hình.

---

## 7.2.3. Decision-Level Fusion

Ở **decision-level fusion**, mỗi nguồn dữ liệu được xử lý độc lập cho đến khi tạo ra prediction hoặc decision.

Với nguồn thứ $m$:

$$
\hat{y}_t^{(m)}=

f_{\theta_m}
\left(
\mathbf{x}_t^{(m)}
\right).
$$

Các prediction được kết hợp bởi một hàm fusion:

$$
\hat{y}_t=

g
\left(
\hat{y}_t^{(1)},
\hat{y}_t^{(2)},
\ldots,
\hat{y}_t^{(M)}
\right).
$$

Đối với classification, một cách đơn giản là majority voting:

$$
\hat{y}=

\operatorname{mode}
\left(
\hat{y}^{(1)},\ldots,\hat{y}^{(M)}
\right).
$$

Nếu mỗi mô hình tạo ra xác suất:

$$
\mathbf{p}^{(m)}=

[
p_1^{(m)},\ldots,p_C^{(m)}
],
$$

có thể sử dụng weighted averaging:

$$
\mathbf{p}=

\sum_{m=1}^{M}
w_m\mathbf{p}^{(m)},
\qquad
\sum_{m=1}^{M}w_m=1.
$$

### Ưu điểm

Decision-level fusion có tính **modular** cao. Mỗi cảm biến có thể sử dụng một mô hình riêng và các mô hình không nhất thiết phải có cùng kiến trúc.

Điều này đặc biệt hữu ích trong hệ thống phân tán hoặc khi các nguồn dữ liệu không thể được đưa về cùng một representation.

Ngoài ra, việc một cảm biến bị lỗi không nhất thiết làm mất toàn bộ hệ thống nếu các nguồn khác vẫn có thể đưa ra prediction.

### Hạn chế

Thông tin chi tiết từ dữ liệu thô hoặc feature representation đã bị nén thành prediction trước khi fusion. Vì vậy, decision-level fusion thường có khả năng khai thác **cross-sensor relationships** thấp hơn so với data-level và feature-level fusion.

Một khi mô hình riêng đã tạo ra:

$$
\hat{y}^{(m)},
$$

các thông tin về đặc trưng ban đầu của nguồn $m$ không còn trực tiếp có sẵn cho tầng fusion.

---

## 7.2.4. So sánh các mức fusion

| Fusion level       | Dữ liệu được kết hợp     | Thông tin giữ lại | Yêu cầu đồng bộ | Độ phức tạp     |
| ------------------ | ------------------------ | ----------------- | --------------- | --------------- |
| **Data-level**     | Dữ liệu thô              | Cao               | Cao             | Thấp–trung bình |
| **Feature-level**  | Đặc trưng/representation | Trung bình–cao    | Trung bình–cao  | Trung bình–cao  |
| **Decision-level** | Prediction/decision      | Thấp hơn          | Thấp hơn        | Trung bình      |

Có thể xem sự khác biệt giữa ba mức dưới dạng:

$$
\boxed{
\text{Data-level}
\rightarrow
\text{Feature-level}
\rightarrow
\text{Decision-level}
}
$$

khi mức độ trừu tượng của thông tin tăng lên và lượng dữ liệu trực tiếp được giữ lại giảm xuống.

Không tồn tại một fusion level tối ưu cho mọi bài toán. Việc lựa chọn phụ thuộc vào:

* mức độ đồng bộ giữa các cảm biến;
* chất lượng và độ tin cậy của từng nguồn;
* sự khác biệt về sampling rate;
* dimensionality của dữ liệu;
* yêu cầu về latency và computational cost;
* khả năng xử lý missing hoặc sensor failure;
* mục tiêu prediction hoặc inference.

---

## 7.2.5. Lựa chọn fusion level cho multivariate time series

Đối với nghiên cứu dữ liệu cảm biến phục vụ machine learning và deep learning, **data-level fusion** và **feature-level fusion** đặc biệt phù hợp khi mục tiêu là xây dựng một representation đa biến duy nhất cho mô hình dự báo.

Nếu các cảm biến đã có cùng temporal resolution và có thể alignment một cách đáng tin cậy:

$$
\left\{
\mathbf{x}_t^{(1)},
\ldots,
\mathbf{x}_t^{(M)}
\right\}
\rightarrow
\mathbf{x}_t
$$

là cách tiếp cận trực tiếp và minh bạch. Sau đó, các bước scaling, feature engineering và feature selection có thể được áp dụng trên representation thống nhất.

Ngược lại, nếu các nguồn có bản chất hoặc cấu trúc rất khác nhau, feature-level fusion có thể phù hợp hơn:

$$
\mathbf{x}^{(m)}
\rightarrow
f_m(\mathbf{x}^{(m)})
\rightarrow
\mathbf{h}^{(m)}
\rightarrow
\mathbf{h}.
$$

Decision-level fusion phù hợp hơn với các hệ thống trong đó mỗi nguồn có pipeline hoặc mô hình độc lập và chỉ cần kết hợp kết quả cuối cùng.

Trong phạm vi survey này, fusion level được xem như một **quyết định thiết kế của preprocessing pipeline**, không phải một bước độc lập với temporal alignment. Trước khi thực hiện data-level hoặc feature-level fusion trên time series, các nguồn phải được đưa về một temporal reference chung. Vì vậy, vấn đề tiếp theo cần giải quyết là **temporal alignment**, được trình bày trong `03_temporal_alignment.md`.

### Tóm tắt

Ba fusion levels có thể được phân biệt bằng vị trí mà thông tin được kết hợp:

$$
\boxed{
\begin{aligned}
\text{Data-level} &: \text{Raw Data} \rightarrow \text{Fusion} \
\text{Feature-level} &: \text{Features} \rightarrow \text{Fusion} \
\text{Decision-level} &: \text{Predictions} \rightarrow \text{Fusion}
\end{aligned}
}
$$

Data-level giữ lại nhiều thông tin nhất nhưng yêu cầu dữ liệu tương thích cao. Feature-level cung cấp sự cân bằng giữa thông tin và khả năng kiểm soát representation. Decision-level có tính modular và linh hoạt cao nhưng đánh đổi bằng việc mất phần lớn thông tin cấp thấp.

Do đó, lựa chọn fusion level phải được thực hiện dựa trên **đặc tính dữ liệu, yêu cầu temporal alignment, chất lượng cảm biến và mục tiêu của mô hình**, thay vì lựa chọn chỉ dựa trên độ phức tạp của phương pháp.
