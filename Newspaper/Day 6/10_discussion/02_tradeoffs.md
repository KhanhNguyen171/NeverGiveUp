# Trade-offs trong tiền xử lý dữ liệu chuỗi thời gian

Tiền xử lý dữ liệu chuỗi thời gian không phải là quá trình tối ưu một tiêu chí duy nhất. Mỗi phép biến đổi đều có thể cải thiện một thuộc tính của dữ liệu nhưng đồng thời làm suy giảm một thuộc tính khác. Vì vậy, lựa chọn preprocessing cần được xem như một bài toán **trade-off** giữa chất lượng dữ liệu, khả năng bảo toàn thông tin, hiệu năng mô hình và chi phí triển khai.

Trong phạm vi nghiên cứu này, các trade-off được phân tích theo pipeline:

$$
\mathcal{D}*{raw}
\rightarrow
\mathcal{D}*{clean}
\rightarrow
\mathcal{D}*{transformed}
\rightarrow
\mathcal{D}*{feature}
\rightarrow
\mathcal{D}_{AI},
$$

trong đó mỗi phép biến đổi $\mathcal{P}$ cần được đánh giá không chỉ dựa trên chất lượng của dữ liệu đầu ra mà còn dựa trên tác động đến nhiệm vụ downstream.

---

## 1. Accuracy và computational cost

Trade-off cơ bản nhất là giữa **độ chính xác của mô hình** và **chi phí tính toán**.

Một preprocessing phức tạp có thể khai thác tốt hơn cấu trúc dữ liệu:

$$
\mathcal{P}*{simple}
\rightarrow
C*{low},
$$

trong khi

$$
\mathcal{P}*{complex}
\rightarrow
C*{high}.
$$

Tuy nhiên, chi phí cao không đảm bảo hiệu năng mô hình cao hơn. Một kỹ thuật preprocessing chỉ có giá trị khi mức cải thiện downstream performance đủ lớn để bù đắp chi phí bổ sung.

Có thể biểu diễn hiệu quả tương đối của một pipeline bởi:

$$
U(\mathcal{P})= \Delta M(\mathcal{P})

\lambda C(\mathcal{P}),
$$

trong đó $\Delta M$ là mức cải thiện hiệu năng mô hình, $C$ là chi phí preprocessing và $\lambda$ biểu diễn mức độ quan trọng của resource constraint.

Trong môi trường cloud, $\lambda$ có thể nhỏ hơn. Ngược lại, trong Edge/IoT, giới hạn về CPU, memory, energy và latency khiến $\lambda$ có thể lớn hơn.

---

## 2. Data quality và information preservation

Một mục tiêu quan trọng của preprocessing là cải thiện chất lượng dữ liệu. Tuy nhiên, **dữ liệu sạch hơn không đồng nghĩa với dữ liệu chứa nhiều thông tin hữu ích hơn**.

Ví dụ, một bộ lọc smoothing có thể giảm noise:

$$
x_t' = \sum_{k=-K}^{K} w_k x_{t+k},
$$

nhưng đồng thời làm suy giảm các biến động ngắn hạn.

Nếu các biến động này chứa thông tin dự báo, smoothing có thể làm giảm downstream performance:

$$
Q_{data}\uparrow
\quad\not\Rightarrow\quad
M_{AI}\uparrow.
$$

Do đó, preprocessing cần phân biệt giữa:

* **noise thực sự**;
* **signal có tần suất cao**;
* **outlier bất thường**;
* **event cực trị nhưng có ý nghĩa**.

Đặc biệt đối với dữ liệu sensor, một observation có giá trị lớn không nhất thiết là lỗi. Nó có thể đại diện cho một sự kiện vật lý thực tế.

---

## 3. Missing data và bias

Xử lý missing values tạo ra trade-off giữa **data completeness** và **estimation bias**.

Giả sử quan sát bị thiếu tại thời điểm $t$:

$$
x_t = \text{missing}.
$$

Nếu sử dụng forward filling:

$$
\hat{x}*t=x*{t-1},
$$

thì dữ liệu trở nên đầy đủ nhưng có thể tạo ra các đoạn giá trị không đổi.

Interpolation có thể tạo ra trajectory mượt hơn:

$$
\hat{x}_t=

x_{t_0}
+
\frac{t-t_0}{t_1-t_0}
(x_{t_1}-x_{t_0}),
$$

nhưng giả định rằng biến đổi giữa hai điểm quan sát có thể được xấp xỉ bằng một hàm liên tục đơn giản.

Các phương pháp model-based có thể cho kết quả chính xác hơn trong một số trường hợp, nhưng yêu cầu nhiều giả định và chi phí tính toán cao hơn.

Do đó:

$$
\text{Completeness}
\uparrow
\quad\text{có thể đi kèm}\quad
\text{Imputation uncertainty}
\uparrow.
$$

Không nên coi mọi missing value đều cần được điền. Nếu khoảng missing quá dài hoặc không thể ước lượng đáng tin cậy, việc giữ missing hoặc loại bỏ đoạn dữ liệu có thể hợp lý hơn.

---

## 4. Outlier removal và preservation of rare events

Outlier detection tạo ra một trade-off đặc biệt quan trọng đối với time series.

Một observation $x_t$ có thể được xem là outlier nếu:

$$
|x_t-\mu| \gt \lambda\sigma.
$$

Tuy nhiên, observation này có thể là:

1. lỗi đo lường;
2. lỗi truyền dữ liệu;
3. nhiễu;
4. một sự kiện hiếm;
5. một trạng thái bất thường thực sự của hệ thống.

Nếu tất cả outlier đều bị loại bỏ, mô hình có thể mất khả năng học các sự kiện cực trị.

Do đó, thay vì mặc định:

$$
\text{outlier}
\Rightarrow
\text{delete},
$$

cần xem xét:

$$
\text{outlier}
\rightarrow
\begin{cases}
\text{remove}, & \text{measurement error},\
\text{replace}, & \text{corrupted value},\
\text{retain}, & \text{meaningful rare event}.
\end{cases}
$$

Đây là lý do outlier treatment cần kết hợp statistical evidence với domain knowledge.

---

## 5. Smoothing và temporal resolution

Noise reduction thường đánh đổi giữa **signal smoothness** và **temporal resolution**.

Với moving average:

$$
\tilde{x}_t=

\frac{1}{w}
\sum_{i=0}^{w-1}x_{t-i},
$$

khi $w$ tăng:

$$
w\uparrow
\Rightarrow
\text{noise}\downarrow,
\qquad
\text{temporal detail}\downarrow.
$$

Window nhỏ bảo toàn nhiều biến động nhưng khả năng khử nhiễu thấp. Window lớn tạo tín hiệu ổn định hơn nhưng có thể làm mất peaks, sudden changes và local patterns.

Vì vậy, $w$ cần được lựa chọn dựa trên **time scale của hiện tượng cần dự đoán**, không chỉ dựa trên mức độ nhiễu quan sát được.

---

## 6. Transformation và interpretability

Các phép transformation như logarithm, Box--Cox hoặc Yeo--Johnson có thể làm cho phân phối dữ liệu phù hợp hơn với mô hình:

$$
x
\rightarrow
f(x).
$$

Ví dụ:

$$
x'=\log(1+x).
$$

Transformation có thể giảm skewness và giảm ảnh hưởng của extreme values. Tuy nhiên, representation mới có thể khó diễn giải hơn representation ban đầu.

Do đó tồn tại trade-off:

$$
\text{Statistical suitability}
\quad\leftrightarrow\quad
\text{Interpretability}.
$$

Trong các ứng dụng yêu cầu giải thích kết quả theo đơn vị vật lý, transformation cần được sử dụng thận trọng và phải có khả năng inverse transformation:

$$
x=f^{-1}(x').
$$

---

## 7. Stationarity và preservation of temporal structure

Differencing là một phương pháp phổ biến để giảm non-stationarity:

$$
\Delta x_t=x_t-x_{t-1}.
$$

Tuy nhiên, phép biến đổi này làm thay đổi representation của chuỗi. Thông tin về mức tuyệt đối của $x_t$ không còn được biểu diễn trực tiếp trong $\Delta x_t$.

Do đó:

$$
\text{Stationarity}
\uparrow
\quad\leftrightarrow\quad
\text{Original-level information}
\downarrow.
$$

Trade-off này đặc biệt quan trọng khi lựa chọn giữa mô hình thống kê và mô hình học sâu. Nếu mô hình downstream không yêu cầu stationarity, việc differencing chỉ để thỏa mãn một giả định thống kê có thể không cần thiết.

---

## 8. Feature richness và dimensionality

Feature engineering làm tăng khả năng biểu diễn:

$$
\mathbf{x}_t
\rightarrow
\mathbf{z}_t=

[
\mathbf{x}*t,
\mathbf{x}*{t-1},
\ldots,
\mathbf{x}_{t-L},
\mathbf{r}_t
].
$$

Tuy nhiên, khi số lượng feature tăng:

$$
d\uparrow
\Rightarrow
\text{representation capacity}\uparrow,
$$

nhưng đồng thời:

$$
d\uparrow
\Rightarrow
\text{memory cost}\uparrow,
\quad
\text{redundancy}\uparrow,
\quad
\text{overfitting risk}\uparrow.
$$

Do đó, feature engineering cần đi cùng feature selection hoặc dimensionality reduction khi số chiều tăng quá lớn.

Đây là trade-off giữa:

$$
\text{Feature richness}
\quad\leftrightarrow\quad
\text{Model complexity}.
$$

---

## 9. Feature selection và information loss

Feature selection giảm số lượng biến:

$$
\mathcal{F}'
\subseteq
\mathcal{F},
\qquad
|\mathcal{F}'|<|\mathcal{F}|.
$$

Điều này giúp giảm computational cost và có thể cải thiện generalization. Tuy nhiên, một feature có tương quan yếu với target vẫn có thể chứa thông tin hữu ích khi kết hợp với các feature khác.

Do đó:

$$
\text{Low marginal relevance}
\neq
\text{No predictive information}.
$$

Filter methods đặc biệt có nguy cơ bỏ qua interaction effects vì thường đánh giá feature tương đối độc lập với mô hình downstream.

Wrapper và embedded methods có thể giải quyết vấn đề này tốt hơn nhưng phải trả giá bằng computational cost.

---

## 10. Dimensionality reduction và interpretability

Dimensionality reduction tìm một representation mới:

$$
\mathbf{x}\in\mathbb{R}^{d}
\rightarrow
\mathbf{z}\in\mathbb{R}^{k},
\qquad
k\ll d.
$$

PCA tối đa hóa variance được giữ lại:

$$
\max_{\mathbf{w}}
\operatorname{Var}(\mathbf{Xw}),
\qquad
|\mathbf{w}|_2=1.
$$

Phương pháp này có thể giảm đáng kể dimensionality nhưng các component mới không nhất thiết tương ứng với biến vật lý ban đầu.

Vì vậy:

$$
\text{Dimensionality}\downarrow
\quad\Rightarrow\quad
\text{Interpretability}\downarrow
$$

trong nhiều trường hợp.

Nếu mục tiêu chính là prediction, trade-off này có thể chấp nhận được. Nếu mục tiêu là scientific interpretation hoặc domain analysis, feature selection có thể phù hợp hơn PCA.

---

## 11. Sensor fusion và system complexity

Sensor fusion làm tăng information coverage bằng cách kết hợp nhiều nguồn:

$$
\mathbf{z}_t=

\operatorname{Fuse}
\left(
\mathbf{x}_t^{(1)},
\ldots,
\mathbf{x}_t^{(M)}
\right).
$$

Tuy nhiên, số lượng sensor tăng kéo theo:

* synchronization cost;
* communication cost;
* missing-source handling;
* dimensionality;
* sensor-specific noise;
* calibration complexity.

Do đó:

$$
\text{Information coverage}\uparrow
\quad\leftrightarrow\quad
\text{System complexity}\uparrow.
$$

Fusion chỉ nên được thực hiện khi các nguồn dữ liệu cung cấp thông tin bổ sung thực sự hữu ích cho downstream task.

---

## 12. Compression và information distortion

Compression tạo ra trade-off trực tiếp giữa **storage/communication efficiency** và **information preservation**.

Lossless compression bảo toàn:

$$
\hat{\mathcal{D}}=

\mathcal{D},
$$

nhưng tỷ lệ nén bị giới hạn bởi entropy của dữ liệu.

Lossy compression cho phép:

$$
\hat{\mathcal{D}}
\neq
\mathcal{D},
$$

để đạt compression ratio cao hơn.

Có thể mô tả trade-off bằng:

$$
\max R
\qquad
\text{subject to}
\qquad
D(\mathcal{D},\hat{\mathcal{D}})
\leq\epsilon,
$$

trong đó $R$ là compression ratio và $D$ là distortion.

Trong hệ thống AI, $\epsilon$ không nên chỉ được xác định bằng sai khác tín hiệu. Quan trọng hơn là distortion đó có làm giảm downstream performance hay không:

$$
D(\mathcal{D},\hat{\mathcal{D}})\uparrow
\Rightarrow
M_{AI}\downarrow
$$

không phải lúc nào cũng xảy ra, nhưng cần được kiểm chứng thực nghiệm.

---

## 13. Edge/IoT: accuracy, latency, energy và bandwidth

Trong Edge/IoT, preprocessing phải đồng thời tối ưu nhiều tài nguyên:

$$
\mathcal{R}=

{
\text{accuracy},
\text{latency},
\text{energy},
\text{memory},
\text{bandwidth}
}.
$$

Một pipeline có accuracy cao nhưng yêu cầu nhiều tài nguyên có thể không phù hợp với thiết bị edge.

Có thể xem bài toán lựa chọn preprocessing như:

$$
\max_{\mathcal{P}}
\quad
M_{AI}(\mathcal{P})
$$

với các ràng buộc:

$$
C_{CPU}\leq C_{CPU}^{max},
$$

$$
C_{memory}\leq C_{memory}^{max},
$$

$$
L\leq L^{max},
$$

và

$$
E\leq E^{max}.
$$

Do đó, phương pháp tốt nhất trên cloud không nhất thiết là phương pháp tốt nhất trên edge.

---

## 14. Trade-off tổng thể trong pipeline

Các trade-off trên không tồn tại độc lập mà tương tác với nhau. Ví dụ:

$$
\text{Feature engineering}
\rightarrow
d\uparrow
\rightarrow
\text{Feature selection}
\rightarrow
d\downarrow
\rightarrow
\text{Information loss risk}\uparrow.
$$

Hoặc:

$$
\text{Smoothing}
\rightarrow
\text{Noise}\downarrow
\rightarrow
\text{Temporal detail}\downarrow
\rightarrow
\text{Forecasting performance}
\begin{cases}
\uparrow\
\downarrow
\end{cases}.
$$

Tương tự:

$$
\text{Compression}
\rightarrow
\text{Bandwidth}\downarrow
\rightarrow
\text{Storage}\downarrow
\rightarrow
\text{Distortion}\uparrow.
$$

Vì vậy, preprocessing nên được thiết kế như một **pipeline có mục tiêu**, thay vì tập hợp các phép biến đổi độc lập.

Một objective tổng quát có thể viết:

$$
\mathcal{P}^{*}=

\arg\max_{\mathcal{P}}
\left[
\alpha M
+
\beta Q- \gamma C

\delta D
\right],
$$

trong đó:

* $M$: downstream model performance;
* $Q$: data quality;
* $C$: computational/resource cost;
* $D$: information distortion;
* $\alpha,\beta,\gamma,\delta$: trọng số phụ thuộc vào ứng dụng.

Đây không phải một objective bắt buộc cho mọi hệ thống, mà là một framework khái niệm để mô tả bản chất multi-objective của preprocessing.

---

## 15. Nguyên tắc lựa chọn

Từ các trade-off trên, có thể rút ra các nguyên tắc:

1. **Không preprocessing nếu không có vấn đề cần giải quyết.**
   Mọi phép biến đổi đều có khả năng làm thay đổi dữ liệu.

2. **Ưu tiên bảo toàn temporal structure.**
   Đặc biệt đối với forecasting, các quan hệ theo thời gian thường có giá trị dự báo trực tiếp.

3. **Đánh giá preprocessing bằng downstream task.**
   Data quality metrics không đủ để kết luận một phương pháp tốt hơn.

4. **Tránh data leakage.**
   Các tham số preprocessing phải được học từ training data và sau đó áp dụng cho validation/test.

5. **Cân bằng complexity và benefit.**
   Một phương pháp phức tạp chỉ nên được sử dụng khi mức cải thiện có ý nghĩa.

6. **Xét deployment constraints ngay từ đầu.**
   Với Edge/IoT, latency, memory, energy và bandwidth là các tiêu chí thiết kế chứ không phải yếu tố phụ.

7. **Không tối ưu từng bước một cách độc lập.**
   Hiệu quả cuối cùng phải được đánh giá trên toàn bộ pipeline.

## 16. Kết luận

Trade-off là đặc điểm cốt lõi của preprocessing dữ liệu chuỗi thời gian. Không có phương pháp nào đồng thời tối đa hóa data quality, information preservation, model performance và resource efficiency.

Do đó, chiến lược phù hợp là lựa chọn một tập preprocessing **đủ để giải quyết các vấn đề thực tế của dữ liệu**, sau đó đánh giá tác động của pipeline đối với nhiệm vụ downstream. Cách tiếp cận này phù hợp với quan điểm của nghiên cứu gốc rằng preprocessing cần được đánh giá cả về hiệu quả xử lý dữ liệu, tác động đến AI và khả năng triển khai trong các môi trường tài nguyên hạn chế.

Mối quan hệ giữa các trade-off này là cơ sở để xây dựng pipeline được trình bày trong [11_pipeline](../11_pipeline/), trong đó các bước cleaning, transformation và feature engineering được tổ chức theo nguyên tắc **data-driven, task-aware và resource-aware**.

### Tài liệu tham khảo

**[1]** A. Tawakuli, B. Havers, V. M. Gulisano, D. Kaiser, and T. Engel, “Time-Series Data Preprocessing: A Survey and an Empirical Analysis,” *Journal of Engineering Research*, 2025. https://www.sciencedirect.com/science/article/pii/S2307187724000452
