# Limitations

Mặc dù tiền xử lý dữ liệu có vai trò quan trọng trong việc cải thiện chất lượng dữ liệu và hỗ trợ các mô hình AI, các phương pháp được khảo sát trong nghiên cứu này vẫn tồn tại nhiều giới hạn. Những giới hạn này xuất hiện ở cả cấp độ dữ liệu, phương pháp, đánh giá thực nghiệm và triển khai hệ thống. Do đó, kết quả của một kỹ thuật preprocessing không nên được khái quát thành một quy luật áp dụng cho mọi chuỗi thời gian.

## 1. Phụ thuộc vào đặc tính của dữ liệu

Hạn chế quan trọng nhất là hiệu quả của preprocessing phụ thuộc mạnh vào đặc tính của dataset.

Một phương pháp có thể hoạt động tốt trên một chuỗi thời gian nhưng không mang lại lợi ích trên dataset khác do sự khác biệt về:

* sampling frequency;
* missingness pattern;
* noise distribution;
* seasonality;
* trend;
* dimensionality;
* mức độ correlation giữa các biến;
* domain characteristics.

Có thể biểu diễn phụ thuộc này dưới dạng:

$$
M
=

f(\mathcal{D},\mathcal{P},\mathcal{A}),
$$

trong đó $\mathcal{D}$ là dataset, $\mathcal{P}$ là preprocessing pipeline và $\mathcal{A}$ là downstream algorithm.

Do đó, không thể kết luận rằng:

$$
\mathcal{P}_1

\gt

\mathcal{P}_2
$$

một cách tuyệt đối. Một kết luận hợp lý hơn là:

$$
\mathcal{P}_1

\gt

\mathcal{P}_2
\quad
\text{under a specific data and task configuration}.
$$

Đây cũng là một trong những vấn đề được nghiên cứu gốc nhấn mạnh khi đánh giá preprocessing trên nhiều dataset và thuật toán AI khác nhau [1].

---

## 2. Không tồn tại một preprocessing pipeline tối ưu cho mọi bài toán

Các bước preprocessing thường có tính phụ thuộc lẫn nhau. Một pipeline có thể được biểu diễn:

$$
\mathcal{P}=

\mathcal{P}_k
\circ
\cdots
\circ
\mathcal{P}_2
\circ
\mathcal{P}_1.
$$

Thứ tự của các phép biến đổi có thể ảnh hưởng đến kết quả.

Ví dụ, scaling trước hoặc sau transformation có thể tạo ra các representation khác nhau. Tương tự, outlier removal trước feature engineering có thể tạo ra kết quả khác với feature engineering trước rồi mới phát hiện outlier.

Do đó:

$$
\mathcal{P}_2(\mathcal{P}_1(\mathcal{D}))
\neq
\mathcal{P}_1(\mathcal{P}_2(\mathcal{D}))
$$

trong nhiều trường hợp.

Điều này làm cho việc tìm một pipeline preprocessing tối ưu trở thành một bài toán tổ hợp thay vì chỉ lựa chọn một thuật toán đơn lẻ.

---

## 3. Phụ thuộc vào downstream model

Một limitation khác là preprocessing không thể được đánh giá độc lập hoàn toàn với mô hình downstream.

Cùng một representation $\mathcal{D}'$ có thể tạo ra hiệu năng khác nhau:

$$
M_1(\mathcal{D}')
\neq
M_2(\mathcal{D}').
$$

Ví dụ, một phép biến đổi giúp dữ liệu phù hợp hơn với giả định của mô hình thống kê có thể không cần thiết đối với neural network. Ngược lại, scaling thường có ảnh hưởng đáng kể đến các mô hình tối ưu bằng gradient nhưng có thể ít quan trọng hơn đối với một số mô hình dựa trên tree.

Do đó, đánh giá preprocessing chỉ bằng statistical properties của dữ liệu là chưa đủ. Cần xem xét:

$$
\text{Preprocessing}
\rightarrow
\text{Representation}
\rightarrow
\text{Model}
\rightarrow
\text{Task performance}.
$$

---

## 4. Khó xác định ranh giới giữa noise và signal

Noise reduction và outlier detection có một limitation cơ bản: không phải mọi observation bất thường đều là lỗi.

Một giá trị:

$$
x_t \gg \mu
$$

có thể là measurement error, nhưng cũng có thể đại diện cho một event thực tế.

Nếu preprocessing loại bỏ event này, dữ liệu trở nên "sạch" hơn về mặt thống kê nhưng mất thông tin quan trọng đối với mô hình.

Vì vậy:

$$
\text{Statistical abnormality}
\neq
\text{Data error}.
$$

Trong các bài toán IoT, industrial monitoring hoặc anomaly detection, limitation này đặc biệt quan trọng vì các sự kiện hiếm thường chính là những observation có giá trị nhất.

---

## 5. Uncertainty trong missing-value imputation

Imputation thay thế observation không quan sát được bằng một giá trị ước lượng:

$$
x_t
\rightarrow
\hat{x}_t.
$$

Tuy nhiên:

$$
\hat{x}_t
\neq
x_t
$$

nói chung.

Ngay cả khi phương pháp imputation tạo ra một chuỗi liên tục và hợp lý, giá trị được tạo ra vẫn chứa uncertainty. Nếu tỷ lệ missing cao hoặc khoảng missing dài, uncertainty càng lớn.

Do đó, việc biến:

$$
\text{missing}
\rightarrow
\text{observed}
$$

có thể tạo ra false certainty.

Các phương pháp đơn giản cũng có thể làm thay đổi phân phối, autocorrelation hoặc variance của chuỗi. Điều này ảnh hưởng trực tiếp đến các bước modeling phía sau.

---

## 6. Nguy cơ information loss

Hầu hết các phép preprocessing đều có khả năng làm mất thông tin.

Ví dụ:

$$
\text{smoothing}
\rightarrow
\text{high-frequency information loss},
$$

$$
\text{feature selection}
\rightarrow
\text{feature information loss},
$$

$$
\text{dimensionality reduction}
\rightarrow
\text{representation loss},
$$

và

$$
\text{lossy compression}
\rightarrow
\text{signal distortion}.
$$

Vấn đề là information loss không phải lúc nào cũng có thể đo trực tiếp bằng các metric thống kê.

Một representation có reconstruction error thấp vẫn có thể loại bỏ thông tin quan trọng đối với prediction:

$$
D(\mathbf{x},\hat{\mathbf{x}})\approx 0
\quad\not\Rightarrow\quad
M(\mathbf{x})\approx M(\hat{\mathbf{x}}).
$$

Do đó, distortion cần được đánh giá cả ở mức dữ liệu và downstream task.

---

## 7. Hạn chế của feature engineering

Feature engineering phụ thuộc đáng kể vào domain knowledge.

Các đặc trưng như:

$$
x_{t-1},x_{t-24},\operatorname{MA}_{t}^{(24)}
$$

có thể hữu ích trong forecasting, nhưng việc lựa chọn lag hoặc window phù hợp không phải lúc nào cũng rõ ràng.

Nếu tạo quá ít feature:

$$
\text{representation capacity}\downarrow.
$$

Nếu tạo quá nhiều feature:

$$
d\uparrow,
\qquad
\text{redundancy}\uparrow,
\qquad
\text{overfitting risk}\uparrow.
$$

Ngoài ra, feature engineering thủ công có thể không mở rộng tốt sang các domain khác nhau. Các mô hình deep learning có khả năng học representation tự động phần nào giảm phụ thuộc vào feature engineering thủ công, nhưng không loại bỏ hoàn toàn nhu cầu thiết kế input và preprocessing.

---

## 8. Hạn chế của feature selection và dimensionality reduction

Feature selection có thể loại bỏ những biến có contribution nhỏ khi xét riêng lẻ nhưng lại hữu ích thông qua interaction.

Giả sử:

$$
I(X_i;Y)\approx 0,
$$

nhưng:

$$
I(X_i,X_j;Y) \gt 0.
$$

Khi đó, đánh giá từng feature độc lập có thể dẫn đến việc loại bỏ $X_i$ mặc dù nó có predictive value khi kết hợp với $X_j$.

Dimensionality reduction có vấn đề khác. Các representation như PCA tối ưu một tiêu chí thống kê, chẳng hạn explained variance, nhưng không nhất thiết tối ưu predictive information.

Do đó:

$$
\text{Maximum variance}
\neq
\text{Maximum predictive information}.
$$

Đây là giới hạn quan trọng khi sử dụng dimensionality reduction như một bước preprocessing mặc định.

---

## 9. Hạn chế trong xử lý non-stationarity

Stationarity transformation thường dựa trên các giả định nhất định về cấu trúc của chuỗi.

Differencing có thể làm giảm trend:

$$
\Delta x_t=x_t-x_{t-1},
$$

nhưng có thể đồng thời loại bỏ information về level.

Decomposition cũng yêu cầu lựa chọn thành phần phù hợp:

$$
x_t=T_t+S_t+R_t,
$$

trong đó $T_t$, $S_t$ và $R_t$ lần lượt đại diện cho trend, seasonality và residual.

Trong thực tế, trend và seasonality có thể thay đổi theo thời gian. Khi đó, giả định rằng các thành phần này ổn định có thể không còn phù hợp.

Vì vậy, preprocessing cho non-stationarity cần được đánh giá trên từng dataset thay vì áp dụng mechanically.

---

## 10. Hạn chế của sensor fusion

Sensor fusion yêu cầu dữ liệu từ nhiều nguồn phải có temporal và semantic compatibility.

Với:

$$
\mathcal{D}^{(m)}=

{
(t_i^{(m)},\mathbf{x}_i^{(m)})
},
$$

các sensor có thể khác nhau về:

* sampling frequency;
* timestamp precision;
* clock drift;
* latency;
* missingness;
* measurement scale;
* sensor reliability.

Temporal alignment không chính xác có thể dẫn đến:

$$
\mathbf{x}_t^{(1)}
\not\leftrightarrow
\mathbf{x}_t^{(2)}.
$$

Khi đó, fusion có thể tạo ra representation sai lệch thay vì bổ sung thông tin.

Ngoài ra, số lượng sensor tăng làm tăng dimensionality và communication overhead. Vì vậy, nhiều sensor hơn không đồng nghĩa với performance tốt hơn.

---

## 11. Hạn chế của compression

Compression đặc biệt quan trọng trong Edge/IoT, nhưng có hai giới hạn chính.

Thứ nhất, lossless compression bị giới hạn bởi redundancy và entropy của dữ liệu. Không thể đảm bảo một compression ratio cao đối với mọi loại chuỗi.

Thứ hai, lossy compression tạo ra distortion:

$$
\hat{x}_t=x_t+\epsilon_t.
$$

Nếu $\epsilon_t$ làm thay đổi các đặc trưng quan trọng, downstream model có thể suy giảm hiệu năng.

Ngoài ra, compression và decompression cũng yêu cầu CPU và energy. Vì vậy, giảm bandwidth không nhất thiết đồng nghĩa với giảm tổng resource consumption.

---

## 12. Hạn chế về computational resources

Một số preprocessing methods yêu cầu:

$$
O(Nd),
\quad
O(Nd^2)
$$

hoặc thậm chí cao hơn về thời gian và bộ nhớ, tùy theo thuật toán.

Điều này tạo ra giới hạn khi dữ liệu có:

* $N$ rất lớn;
* dimensionality $d$ cao;
* sampling frequency lớn;
* nhiều sensor;
* yêu cầu real-time.

Một phương pháp có thể phù hợp khi preprocessing offline nhưng không phù hợp khi cần xử lý streaming:

$$
\text{Offline feasible}
\not\Rightarrow
\text{Online feasible}.
$$

Đây là limitation quan trọng đối với hệ thống Edge/IoT, nơi tài nguyên tính toán và năng lượng bị giới hạn.

---

## 13. Hạn chế về reproducibility và hyperparameters

Nhiều preprocessing methods phụ thuộc vào hyperparameters:

$$
\theta_{\mathcal{P}}=

{
w,k,\lambda,\tau,\ldots
}.
$$

Ví dụ:

* window size;
* outlier threshold;
* smoothing parameter;
* number of principal components;
* number of selected features;
* compression level.

Một thay đổi nhỏ trong $\theta_{\mathcal{P}}$ có thể dẫn đến representation khác đáng kể.

Do đó, kết quả thực nghiệm cần ghi nhận đầy đủ:

$$
(\mathcal{D},
\mathcal{P},
\theta_{\mathcal{P}},
\mathcal{A},
\text{evaluation protocol}).
$$

Nếu chỉ báo cáo kết quả cuối cùng mà không công bố cấu hình preprocessing, khả năng tái lập sẽ bị hạn chế.

---

## 14. Hạn chế của đánh giá thực nghiệm

Một preprocessing method không nên được đánh giá chỉ bằng một dataset hoặc một model.

Hiệu quả quan sát được có thể phụ thuộc vào:

$$
M
=

f(
\mathcal{D},
\mathcal{P},
\mathcal{A},
\mathcal{H},
\mathcal{S}
),
$$

trong đó $\mathcal{H}$ là hyperparameters và $\mathcal{S}$ là data splitting strategy.

Nếu chỉ sử dụng một experimental configuration, rất khó xác định liệu improvement đến từ preprocessing hay từ tương tác đặc thù giữa preprocessing và model.

Nghiên cứu gốc thực hiện empirical analysis nhằm so sánh tác động của preprocessing đối với nhiều cấu hình dữ liệu và AI, nhưng kết quả thực nghiệm vẫn cần được hiểu trong phạm vi các dataset, phương pháp và experimental settings được khảo sát [1].

---

## 15. Data leakage

Một limitation có tính phương pháp luận nghiêm trọng là preprocessing có thể vô tình sử dụng information từ validation hoặc test set.

Ví dụ, nếu Standardization được tính trên toàn bộ dataset:

$$
\mu=

\frac{1}{N}
\sum_{i=1}^{N}x_i,
$$

thì $\mu$ đã chứa thông tin từ test set.

Quy trình đúng là:

$$
\theta_{\mathcal{P}}=

\operatorname{Fit}
(\mathcal{D}_{train}),
$$

sau đó:

$$
\mathcal{D}_{val}'=

\mathcal{P}(\mathcal{D}*{val};\theta*{\mathcal{P}}),
$$

$$
\mathcal{D}_{test}'=

\mathcal{P}(\mathcal{D}*{test};\theta*{\mathcal{P}}).
$$

Nếu không kiểm soát leakage, performance có thể bị đánh giá cao giả tạo và kết quả không phản ánh khả năng generalization thực tế.

---

## 16. Giới hạn về khả năng khái quát

Một preprocessing pipeline được tối ưu cho một dataset có thể không generalize sang dataset khác.

Ví dụ, nếu một pipeline được thiết kế với:

$$
L=24
$$

để khai thác chu kỳ ngày, nó không nhất thiết phù hợp với dataset có sampling frequency hoặc seasonal period khác.

Tương tự, threshold được học trên một sensor có thể không phù hợp với sensor khác.

Do đó:

$$
\mathcal{P}*{D_1}^{*}
\not\equiv
\mathcal{P}*{D_2}^{*}.
$$

Generalization của preprocessing cần được đánh giá trên nhiều dataset, nhiều domain và nhiều điều kiện vận hành.

---

## 17. Tổng hợp các limitations

Các limitation chính có thể được tóm tắt như sau:

| Limitation                 | Nguyên nhân                         | Hệ quả                                  |
| -------------------------- | ----------------------------------- | --------------------------------------- |
| Dataset dependency         | Đặc tính dữ liệu khác nhau          | Khó khái quát                           |
| Pipeline dependency        | Các bước preprocessing tương tác    | Thứ tự xử lý ảnh hưởng kết quả          |
| Model dependency           | Downstream models khác nhau         | Không có preprocessing tối ưu tuyệt đối |
| Information loss           | Filtering, selection, compression   | Mất tín hiệu hữu ích                    |
| Imputation uncertainty     | Giá trị thiếu không quan sát được   | Có thể tạo bias                         |
| Outlier ambiguity          | Outlier có thể là event thực        | Nguy cơ loại bỏ signal                  |
| High dimensionality        | Feature engineering/fusion          | Tăng memory và computation              |
| Interpretability loss      | Transformation/PCA                  | Khó giải thích                          |
| Resource constraints       | CPU, memory, energy, bandwidth      | Hạn chế Edge/IoT                        |
| Hyperparameter sensitivity | Phụ thuộc $\theta_{\mathcal{P}}$    | Khó reproducibility                     |
| Data leakage               | Fit preprocessing trên toàn bộ data | Đánh giá sai performance                |
| Limited generalization     | Pipeline phụ thuộc dataset          | Khó áp dụng rộng rãi                    |

Những limitation này cho thấy preprocessing không nên được xem là một chuỗi thao tác cố định. Thay vào đó, preprocessing cần được thiết kế dựa trên **đặc tính dữ liệu, downstream task và môi trường triển khai**.

## 18. Hướng xử lý các limitations

Các limitation trên dẫn đến một số định hướng quan trọng cho nghiên cứu và triển khai:

1. **Task-aware preprocessing:** lựa chọn phương pháp dựa trên mục tiêu downstream thay vì chỉ dựa trên statistical properties.
2. **Data-driven parameter selection:** xác định hyperparameters từ đặc tính thực tế của dataset.
3. **Leakage-safe preprocessing:** fit mọi transformation có tham số trên training data.
4. **End-to-end evaluation:** đánh giá preprocessing thông qua cả data quality và downstream performance.
5. **Resource-aware preprocessing:** đưa latency, memory, energy và bandwidth vào quá trình lựa chọn.
6. **Adaptive preprocessing:** cho phép pipeline thay đổi theo distribution drift và điều kiện vận hành.
7. **Reproducible pipelines:** lưu trữ preprocessing configuration, parameters và dataset version để bảo đảm khả năng tái lập.

Các nguyên tắc này tạo cầu nối trực tiếp đến chương [11_pipeline](../11_pipeline/), nơi các kỹ thuật được tổ chức thành một quy trình preprocessing có cấu trúc từ dữ liệu thô đến dữ liệu sẵn sàng cho AI.

### Tài liệu tham khảo

**[1]** A. Tawakuli, B. Havers, V. M. Gulisano, D. Kaiser, and T. Engel, “Time-Series Data Preprocessing: A Survey and an Empirical Analysis,” *Journal of Engineering Research*, 2025.
[ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2307187724000452)
