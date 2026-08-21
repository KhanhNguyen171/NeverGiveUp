# 7. Sensor Fusion

## 7.1. Sensor Fusion

Trong các hệ thống thu thập dữ liệu từ cảm biến, một nguồn dữ liệu đơn lẻ thường không đủ để mô tả đầy đủ trạng thái của đối tượng quan sát. Mỗi cảm biến có thể đo một đại lượng khác nhau, có độ chính xác, phạm vi đo và mức nhiễu riêng. **Sensor fusion** là quá trình kết hợp thông tin từ nhiều cảm biến hoặc nhiều nguồn đo nhằm tạo ra một biểu diễn thống nhất, giàu thông tin và đáng tin cậy hơn so với việc sử dụng từng nguồn độc lập.

Về mặt toán học, giả sử tại thời điểm $t$ có $M$ cảm biến cùng quan sát một hệ thống:

$$\mathbf{z}_t^{(m)} = h_m(\mathbf{s}_t) + \boldsymbol{\epsilon}_t^{(m)}, \qquad m=1,\ldots, M$$

trong đó:

* $\mathbf{s}_t$ là trạng thái thực của hệ thống;
* $\mathbf{z}_t^{(m)}$ là quan sát từ cảm biến thứ $m$;
* $h_m(\cdot)$ là hàm ánh xạ trạng thái thực sang không gian quan sát của cảm biến;
* $\boldsymbol{\epsilon}_t^{(m)}$ là sai số hoặc nhiễu đo.

Mục tiêu của sensor fusion là xây dựng một biểu diễn hoặc ước lượng:

$$
\hat{\mathbf{s}}_t=

f\left(
\mathbf{z}_t^{(1)},
\mathbf{z}_t^{(2)},
\ldots,
\mathbf{z}_t^{(M)}
\right),
$$

sao cho $\hat{\mathbf{s}}_t$ chứa thông tin hữu ích hơn, giảm ảnh hưởng của nhiễu và cải thiện khả năng mô hình hóa trạng thái hệ thống.

Trong bối cảnh **multivariate time series**, sensor fusion không chỉ là ghép các biến theo chiều đặc trưng. Các nguồn cảm biến phải được xem xét đồng thời dưới ba khía cạnh: **giá trị đo**, **thời gian quan sát** và **độ tin cậy của nguồn dữ liệu**. Vì vậy, sensor fusion có mối liên hệ trực tiếp với các bước preprocessing trước đó như xử lý missing data, outlier, noise reduction và transformation.

### 7.1.1. Vai trò của sensor fusion trong dữ liệu cảm biến

Sensor fusion đặc biệt quan trọng khi các cảm biến có tính bổ sung về thông tin. Một cảm biến có thể cung cấp tín hiệu chính, trong khi các cảm biến khác cung cấp các biến môi trường hoặc biến điều kiện giúp giải thích sự biến động của tín hiệu đó.

Ví dụ, trong bài toán quan trắc chất lượng không khí, các phép đo ô nhiễm có thể được kết hợp với các biến khí tượng như nhiệt độ, độ ẩm hoặc các phép đo từ những cảm biến khác. Việc kết hợp này cho phép mô hình quan sát hiện tượng dưới nhiều góc độ thay vì chỉ dựa trên một chuỗi đo duy nhất. Các nghiên cứu về data fusion trong quan trắc không khí cho thấy việc kết hợp dữ liệu từ cảm biến chi phí thấp với các nguồn thông tin khác có thể cải thiện khả năng ước lượng, nhưng đồng thời phải xử lý sai số đo và sự không chắc chắn của cảm biến.

Do đó, giá trị của sensor fusion không nằm đơn thuần ở việc **tăng số lượng biến**, mà ở khả năng khai thác **tính bổ sung và quan hệ phụ thuộc giữa các nguồn dữ liệu**.

### 7.1.2. Biểu diễn dữ liệu sau khi fusion

Sau khi các nguồn dữ liệu được đồng bộ theo thời gian, dữ liệu đa cảm biến có thể được biểu diễn dưới dạng ma trận:

$$
\mathbf{X}=

\begin{bmatrix}
\mathbf{x}_1^\top \
\mathbf{x}_2^\top \
\vdots \
\mathbf{x}_T^\top
\end{bmatrix}
\in
\mathbb{R}^{T\times F},
$$

trong đó $T$ là số thời điểm quan sát và $F$ là tổng số đặc trưng đến từ các cảm biến.

Tại mỗi thời điểm $t$:

$$
\mathbf{x}_t=

\left[
x_t^{(1)},
x_t^{(2)},
\ldots,
x_t^{(F)}
\right]^\top.
$$

Đối với bài toán dự báo chuỗi thời gian, biểu diễn này thường được chuyển thành các cửa sổ quan sát:

$$
\mathbf{X}_{t-L+1:t}=

\left[
\mathbf{x}_{t-L+1},
\ldots,
\mathbf{x}_t
\right],
$$

sau đó được sử dụng để dự báo trạng thái hoặc giá trị mục tiêu trong tương lai:

$$
\hat{y}_{t+H}=

f_\theta
\left(
\mathbf{X}_{t-L+1:t}
\right).
$$

Cách biểu diễn này cho phép mô hình học đồng thời **phụ thuộc theo thời gian** và **phụ thuộc giữa các nguồn cảm biến**.

### 7.1.3. Những vấn đề cần kiểm soát

Sensor fusion chỉ có ý nghĩa khi dữ liệu đầu vào có chất lượng và được đưa về cùng một hệ quy chiếu thời gian. Ba vấn đề quan trọng cần được kiểm soát là:

**Thứ nhất, sai khác về thời gian lấy mẫu.** Các cảm biến có thể có sampling rate khác nhau. Nếu không đồng bộ, các giá trị được ghép tại cùng một chỉ số hàng có thể không thực sự mô tả cùng một trạng thái của hệ thống.

**Thứ hai, sai lệch và nhiễu giữa các cảm biến.** Hai cảm biến đo cùng một đại lượng có thể tạo ra các phân phối khác nhau do calibration, drift hoặc noise. Vì vậy, dữ liệu cần được kiểm tra chất lượng trước khi fusion. Trong nghiên cứu về fusion dữ liệu cảm biến chất lượng không khí, việc xử lý các quan sát không đáng tin cậy và measurement drift được xem là bước cần thiết trước khi thực hiện fusion.

**Thứ ba, độ tin cậy không đồng nhất.** Không phải mọi nguồn dữ liệu đều có mức uncertainty giống nhau. Một phương pháp fusion có thể cần gán trọng số hoặc mô hình hóa uncertainty để tránh việc nguồn dữ liệu kém tin cậy chi phối kết quả cuối cùng. Các nghiên cứu về air-quality data fusion cho thấy measurement uncertainty có ảnh hưởng trực tiếp đến chất lượng của kết quả fusion.

Vì vậy, quy trình tổng quát có thể được mô tả:

$$
\text{Raw Sensors}
\rightarrow
\text{Quality Control}
\rightarrow
\text{Temporal Alignment}
\rightarrow
\text{Fusion}
\rightarrow
\text{Unified Representation}.
$$

Trong đó, **temporal alignment** là điều kiện nền tảng để các mức fusion được trình bày ở mục tiếp theo có ý nghĩa đối với dữ liệu chuỗi thời gian.

### 7.1.4. Sensor fusion và feature engineering

Sensor fusion cần được phân biệt với feature engineering. Feature engineering tạo ra các đặc trưng mới từ dữ liệu hiện có, trong khi sensor fusion tập trung vào việc **kết hợp thông tin từ nhiều nguồn quan sát**.

Tuy nhiên, hai quá trình có thể được sử dụng nối tiếp:

$$
\text{Multiple Sensors}
\rightarrow
\text{Fusion}
\rightarrow
\text{Feature Engineering}
\rightarrow
\text{Feature Selection}
\rightarrow
\text{AI Model}.
$$

Ví dụ, sau khi kết hợp nhiều cảm biến, có thể tiếp tục xây dựng lag features hoặc rolling statistics trên từng tín hiệu hoặc trên các tín hiệu đã fusion. Điều này tạo ra một biểu diễn giàu thông tin hơn cho các mô hình machine learning và deep learning.

Ngược lại, nếu fusion được thực hiện trên dữ liệu chưa được kiểm soát chất lượng, nhiễu và sai lệch của một cảm biến có thể được truyền sang toàn bộ representation. Do đó, sensor fusion phải được đặt **sau các bước kiểm soát chất lượng dữ liệu cần thiết** thay vì được xem như một phép ghép dữ liệu đơn giản.

### 7.1.5. Ý nghĩa đối với nghiên cứu dữ liệu cảm biến

Trong phạm vi nghiên cứu này, sensor fusion được xem là một thành phần của preprocessing pipeline nhằm xây dựng **AI-ready multivariate representation**. Trọng tâm không phải là phát triển một thuật toán fusion mới, mà là xác định cách các nguồn cảm biến có thể được kết hợp một cách nhất quán trước khi đưa vào các bước feature engineering, feature selection và mô hình hóa.

Từ góc nhìn đó, ba câu hỏi chính cần được giải quyết là:

1. **Fusion ở đâu?** — xác định mức độ mà các nguồn dữ liệu được kết hợp.
2. **Fusion như thế nào?** — xác định phép kết hợp hoặc cơ chế tích hợp thông tin.
3. **Fusion khi nào?** — xác định thời điểm và quy trình đồng bộ dữ liệu trước khi kết hợp.

Ba vấn đề này dẫn trực tiếp đến **fusion levels** và **temporal alignment**, lần lượt được trình bày trong `02_fusion_levels.md` và `03_temporal_alignment.md`.

Như vậy, sensor fusion đóng vai trò cầu nối giữa **dữ liệu cảm biến riêng lẻ** và **biểu diễn đa biến thống nhất**. Một quy trình fusion phù hợp không chỉ làm tăng lượng thông tin đầu vào mà còn phải duy trì tính nhất quán về thời gian, chất lượng đo và mức độ tin cậy của từng nguồn. Đây là điều kiện cần để các bước preprocessing và mô hình AI phía sau có thể khai thác đúng thông tin từ hệ thống cảm biến đa nguồn.
