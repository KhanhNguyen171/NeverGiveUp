# 7.3. Temporal Alignment

Trong sensor fusion, các nguồn dữ liệu chỉ có thể được kết hợp một cách có ý nghĩa khi các quan sát được quy về **cùng một mốc thời gian**. Vấn đề này được gọi là **temporal alignment**. Đây là bước đặc biệt quan trọng đối với multivariate time series vì các cảm biến có thể có sampling rate khác nhau, timestamp không đồng nhất, độ trễ truyền dữ liệu hoặc các khoảng thời gian bị thiếu.

Nếu temporal alignment không được thực hiện trước fusion, hai giá trị được đặt trên cùng một hàng dữ liệu có thể thực chất mô tả **hai trạng thái khác nhau của hệ thống**. Khi đó, mô hình có thể học các quan hệ giả tạo giữa các biến thay vì quan hệ thực sự tồn tại trong hệ thống.

---

## 7.3.1. Bài toán temporal alignment

Giả sử có $M$ nguồn cảm biến. Mỗi cảm biến tạo ra một chuỗi quan sát:

$$
\mathcal{D}^{(m)}
=
\left\{
\left(
t_i^{(m)},
\mathbf{x}_i^{(m)}
\right)
\right\}_{i=1}^{N_m},
\qquad
m=1,\ldots,M.
$$

trong đó:

* $t_i^{(m)}$ là timestamp của quan sát thứ $i$ từ cảm biến $m$;
* $\mathbf{x}_i^{(m)}$ là vector giá trị quan sát;
* $N_m$ là số quan sát của cảm biến $m$.

Trong trường hợp lý tưởng, tất cả cảm biến sử dụng cùng một tập timestamp:

$$t_i^{(1)}= t_i^{(2)} \cdots t_i^{(M)}$$

Khi đó, dữ liệu có thể được fusion trực tiếp:

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
\right].
$$

Tuy nhiên, trong hệ thống thực tế:

$$
\mathcal{T}^{(1)}
\neq
\mathcal{T}^{(2)}
\neq
\cdots
\neq
\mathcal{T}^{(M)}.
$$

Do đó, cần xây dựng một **common temporal reference** $\mathcal{T}^\ast$ trước khi thực hiện fusion.

---

## 7.3.2. Sampling rate và temporal resolution

Một trong những nguyên nhân chính gây mất đồng bộ là các cảm biến có sampling rate khác nhau.

Giả sử:

* Sensor 1 lấy mẫu mỗi $10$ phút;
* Sensor 2 lấy mẫu mỗi $30$ phút.

Khi đó:

$$
\Delta t_1 = 10\text{ min},
\qquad
\Delta t_2 = 30\text{ min}.
$$

Nếu chọn resolution $10$ phút làm temporal reference, sensor 2 không có quan sát mới ở mọi timestamp.

Ví dụ:

$$
\mathcal{T}^\ast=

{
10,20,30,40,50,60,\ldots
}.
$$

Trong khi sensor 2 chỉ quan sát:

$$
\mathcal{T}^{(2)}=

{
10,40,70,\ldots
}.
$$

Khi đó cần xác định cách ánh xạ:

$$
\mathcal{T}^{(2)}
\rightarrow
\mathcal{T}^\ast.
$$

Đây là vấn đề cốt lõi của temporal alignment.

Temporal resolution nên được lựa chọn dựa trên:

* sampling rate của các nguồn;
* tốc độ biến đổi của hiện tượng;
* mục tiêu dự báo;
* yêu cầu về computational cost;
* mức độ mất thông tin có thể chấp nhận.

Không nên chọn temporal resolution quá nhỏ nếu dữ liệu không thực sự chứa thông tin ở độ phân giải đó, vì điều này có thể tạo ra nhiều giá trị được nội suy hoặc lặp lại mà không bổ sung thông tin thực tế.

---

## 7.3.3. Xây dựng common temporal grid

Một cách tiếp cận phổ biến là xây dựng một **temporal grid** chung:

$$
\mathcal{T}^\ast=

{
t_1^\ast,t_2^\ast,\ldots,t_K^\ast
},
$$

với:

$$
t_{k+1}^\ast-t_k^\ast=

\Delta t^\ast.
$$

Mỗi quan sát của từng cảm biến sau đó được ánh xạ vào temporal grid này.

Có thể biểu diễn quá trình:

$$
\mathcal{D}^{(1)},\ldots,\mathcal{D}^{(M)}
\rightarrow
\mathcal{T}^\ast
\rightarrow
\tilde{\mathcal{D}}^{(1)},\ldots,
\tilde{\mathcal{D}}^{(M)}
\rightarrow
\mathbf{X}.
$$

Sau alignment, mỗi dòng của ma trận $\mathbf{X}$ phải đại diện cho cùng một temporal state:

$$
\mathbf{X}=

\begin{bmatrix}
t_1^\ast & \mathbf{x}*{t_1^\ast}^{(1)} & \cdots & \mathbf{x}*{t_1^\ast}^{(M)} \
t_2^\ast & \mathbf{x}*{t_2^\ast}^{(1)} & \cdots & \mathbf{x}*{t_2^\ast}^{(M)} \
\vdots & \vdots & \ddots & \vdots \
t_K^\ast & \mathbf{x}*{t_K^\ast}^{(1)} & \cdots & \mathbf{x}*{t_K^\ast}^{(M)}
\end{bmatrix}.
$$

Đây là cơ sở để thực hiện data-level hoặc feature-level fusion.

---

## 7.3.4. Các phương pháp temporal alignment

### 7.3.4.1. Exact Timestamp Matching

Phương pháp đơn giản nhất là chỉ ghép các quan sát có timestamp giống hệt nhau.

Với hai nguồn $A$ và $B$:

$$
\mathcal{T}_{AB}=

\mathcal{T}_A
\cap
\mathcal{T}_B.
$$

Chỉ những timestamp thuộc $\mathcal{T}_{AB}$ mới được sử dụng.

Ưu điểm:

* không tạo ra dữ liệu nhân tạo;
* không cần giả định về diễn biến của tín hiệu;
* dễ kiểm tra tính đúng đắn.

Hạn chế là có thể làm giảm đáng kể số lượng quan sát khi các cảm biến có sampling rate khác nhau hoặc timestamp không hoàn toàn đồng nhất.

Vì vậy, phương pháp này phù hợp nhất khi các nguồn đã sử dụng cùng sampling frequency và cùng temporal convention.

---

### 7.3.4.2. Resampling

**Resampling** chuyển dữ liệu từ temporal resolution ban đầu sang một resolution chung.

Nếu dữ liệu có sampling interval $\Delta t$ và cần chuyển sang $\Delta t^\ast$, có thể sử dụng aggregation hoặc interpolation tùy trường hợp.

Ví dụ, khi giảm temporal resolution:

$$
\tilde{x}_k=

\frac{1}{n}
\sum_{i=1}^{n}x_i
$$

có thể được sử dụng để tính giá trị trung bình trong một time bin.

Ngoài mean, có thể sử dụng:

$$
\tilde{x}_k
\in
{
\operatorname{mean},
\operatorname{median},
\operatorname{min},
\operatorname{max},
\operatorname{sum}
}.
$$

Việc lựa chọn aggregation function phải dựa trên ý nghĩa vật lý của biến.

Ví dụ, đối với một đại lượng đo tức thời, mean có thể phù hợp; trong khi đối với một đại lượng tích lũy, sum có thể có ý nghĩa hơn.

---

### 7.3.4.3. Interpolation

Khi temporal grid yêu cầu các giá trị nằm giữa hai quan sát, interpolation có thể được sử dụng.

Với linear interpolation:

$$
\hat{x}(t)=

x(t_1)
+
\frac{t-t_1}{t_2-t_1}
\left[
x(t_2)-x(t_1)
\right],
$$

với:

$$
t_1 \lt t \lt t_2.
$$

Phương pháp này giả định tín hiệu thay đổi tương đối đều giữa hai timestamp.

Interpolation có thể hữu ích khi khoảng cách thiếu dữ liệu nhỏ và tín hiệu biến đổi tương đối trơn. Tuy nhiên, nó không nên được xem là cách khôi phục chính xác một quan sát chưa từng được cảm biến đo.

Đặc biệt, không nên nội suy một cách tùy tiện trên các khoảng gap dài vì có thể tạo ra xu hướng giả:

$$
\text{Large Gap}
\rightarrow
\text{Strong Assumption}
\rightarrow
\text{Potentially Artificial Signal}.
$$

Do đó, cần giới hạn khoảng cách tối đa cho phép interpolation.

---

### 7.3.4.4. Nearest-Neighbor Alignment

Một timestamp có thể được ghép với quan sát gần nhất:

$$
t_j^{(m)}=

\arg\min_{t_i^{(m)}}
\left|
t_i^{(m)}-t_j^\ast
\right|.
$$

Tuy nhiên, cần đặt một ngưỡng tolerance:

$$
\left|
t_i^{(m)}-t_j^\ast
\right|
\leq
\tau.
$$

Nếu không có quan sát nào thỏa mãn điều kiện:

$$
\left|
t_i^{(m)}-t_j^\ast
\right|

>

\tau,
$$

thì giá trị nên được đánh dấu là missing thay vì sử dụng một quan sát quá xa về thời gian.

Tolerance $\tau$ là một hyperparameter quan trọng vì nó quyết định mức độ sai lệch thời gian có thể chấp nhận.

---

## 7.3.5. Temporal Alignment và Missing Data

Temporal alignment thường tạo ra missing values ngay cả khi dữ liệu gốc không có missing.

Giả sử temporal grid chung là:

$$
\mathcal{T}^\ast=

{t_1,t_2,t_3,t_4},
$$

nhưng sensor $B$ chỉ quan sát tại:

$$
\mathcal{T}^{(B)}=

{t_1,t_3,t_4}.
$$

Sau alignment:

$$
\mathbf{x}^{(B)}=

[x_{t_1}^{(B)},\text{NaN},x_{t_3}^{(B)},x_{t_4}^{(B)}].
$$

Do đó:

$$
\text{Temporal Alignment}
\rightarrow
\text{Potential Missing Data}
$$

và hai bước này phải được thiết kế cùng nhau.

Sau alignment, missing values có thể được xử lý bằng các phương pháp đã trình bày ở **Chapter 3 — Data Cleaning**, chẳng hạn interpolation, forward filling hoặc các phương pháp imputation phù hợp.

Tuy nhiên, cần phân biệt:

$$
\text{Missing because of Alignment}
\neq
\text{Original Missing}.
$$

Việc phân biệt nguồn gốc của missing giúp tránh áp dụng một phương pháp imputation không phù hợp với bản chất dữ liệu.

---

## 7.3.6. Temporal Alignment và Data Leakage

Temporal alignment cũng liên quan trực tiếp đến **data leakage**, đặc biệt trong bài toán forecasting.

Giả sử mục tiêu là dự báo:

$$
\hat{y}_{t+H}=

f_\theta
\left(
\mathbf{x}_{t-L+1:t}
\right).
$$

Mọi feature được sử dụng để dự báo phải thỏa mãn:

$$
\text{timestamp(feature)}
\leq t.
$$

Nếu quá trình alignment hoặc interpolation sử dụng một quan sát xảy ra sau thời điểm dự báo $t$, thông tin tương lai có thể vô tình được đưa vào input.

Ví dụ, interpolation:

$$
\hat{x}_t=

f(x_{t-1},x_{t+1})
$$

sử dụng $x_{t+1}$ để xây dựng giá trị tại $t$. Trong forecasting thời gian thực, $x_{t+1}$ chưa tồn tại tại thời điểm $t$. Vì vậy, cách nội suy này có thể tạo ra **future leakage**.

Đây là lý do temporal alignment trong forecasting phải tuân thủ nguyên tắc:

$$
\boxed{
\text{Alignment must respect information availability at prediction time.}
}
$$

Nói cách khác, một phương pháp alignment có thể hợp lệ về mặt thống kê nhưng vẫn không hợp lệ về mặt forecasting nếu nó sử dụng thông tin tương lai.

---

## 7.3.7. Temporal Alignment trong Multivariate Time Series

Sau khi alignment, dữ liệu đa cảm biến có thể được biểu diễn thành:

$$
\mathbf{X}=

\left[
\mathbf{x}_1,
\mathbf{x}_2,
\ldots,
\mathbf{x}_T
\right]^\top
\in
\mathbb{R}^{T\times F}.
$$

Với mỗi thời điểm $t$:

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
\right].
$$

Khi đó, sensor fusion trở thành phép kết hợp các feature vector có cùng temporal reference.

Đối với forecasting với lookback $L$, representation cuối cùng có thể được xây dựng thành:

$$
\mathbf{X}_{t-L+1:t}=

\left[
\mathbf{x}*{t-L+1},
\ldots,
\mathbf{x}*{t}
\right]
\in
\mathbb{R}^{L\times F}.
$$

Đây chính là dạng dữ liệu phù hợp để đưa vào các mô hình sequence như RNN, LSTM, GRU hoặc Transformer.

Do đó, temporal alignment tạo ra cầu nối:

$$
\boxed{
\text{Multiple Sensors}
\rightarrow
\text{Temporal Alignment}
\rightarrow
\text{Sensor Fusion}
\rightarrow
\text{Multivariate Sequence}
\rightarrow
\text{AI Model}
}
$$

---

## 7.3.8. Nguyên tắc thiết kế Temporal Alignment

Một temporal alignment pipeline nên tuân thủ các nguyên tắc sau:

1. **Xác định temporal reference trước khi fusion.**
   Tất cả nguồn dữ liệu phải được quy về một temporal grid hoặc một quy tắc matching rõ ràng.

2. **Không giả định rằng timestamp giống nhau nghĩa là dữ liệu hoàn toàn đồng thời.**
   Cần xem xét sampling interval, acquisition delay và timestamp semantics.

3. **Kiểm soát tolerance.**
   Nearest-neighbor matching phải có giới hạn thời gian tối đa:

   $$
   |t_i-t^\ast|\leq\tau.
   $$

4. **Giới hạn interpolation.**
   Không nội suy trên những khoảng gap lớn nếu giả định về diễn biến tín hiệu không còn đáng tin cậy.

5. **Bảo toàn thứ tự thời gian.**
   Sau alignment:

   $$
   t_1 \lt t_2 \lt \cdots \lt t_T.
   $$

6. **Kiểm tra duplicate timestamps.**
   Mỗi temporal reference nên có quy tắc rõ ràng đối với nhiều quan sát cùng timestamp.

7. **Không sử dụng thông tin tương lai trong forecasting.**
   Alignment phải phù hợp với information set tại thời điểm prediction.

8. **Kiểm tra continuity trước khi tạo sliding windows.**
   Một window:

   $$
   \mathbf{X}_{t-L+1:t}
   $$

   chỉ hợp lệ khi các timestamp trong window thỏa mãn temporal continuity đã định nghĩa.

---

## 7.3.9. Kết nối với Pipeline nghiên cứu

Trong toàn bộ preprocessing pipeline, temporal alignment không phải là một phép xử lý độc lập mà là điều kiện để sensor fusion tạo ra representation có ý nghĩa:

$$
\text{Raw Sensor Data}
\rightarrow
\text{Data Cleaning}
\rightarrow
\text{Temporal Alignment}
\rightarrow
\text{Sensor Fusion}
\rightarrow
\text{Transformation}
\rightarrow
\text{Feature Engineering}
\rightarrow
\text{Feature Selection}
\rightarrow
\text{AI-ready Data}.
$$

Đặc biệt, đối với multivariate forecasting, temporal alignment phải được thực hiện **trước khi tạo lag features, rolling features và sliding windows**. Nếu timestamp chưa được căn chỉnh, các feature phụ thuộc thời gian có thể được xây dựng trên những khoảng thời gian không đồng nhất.

Như vậy, temporal alignment đảm bảo rằng:

$$
\boxed{
\text{One row}
\approx
\text{One common temporal state}
}
$$

và từ đó cho phép sensor fusion tạo ra một representation đa biến nhất quán.

### Tóm tắt

Temporal alignment giải quyết vấn đề **khi nào các quan sát từ nhiều cảm biến thực sự có thể được xem là tương ứng với nhau**. Quy trình cốt lõi gồm:

$$
\boxed{
\text{Choose Time Grid}
\rightarrow
\text{Match/Resample}
\rightarrow
\text{Handle Gaps}
\rightarrow
\text{Validate Continuity}
\rightarrow
\text{Fuse}
}
$$

Trong đó, lựa chọn phương pháp alignment phải cân bằng giữa **độ chính xác thời gian, khả năng bảo toàn thông tin, missingness và nguy cơ tạo dữ liệu nhân tạo hoặc leakage**. Đây là điều kiện nền tảng để dữ liệu đa cảm biến có thể được chuyển thành representation thống nhất và tiếp tục đi qua các bước preprocessing, feature engineering và modeling.
