# 04. Connection to Survey

## 1. Vai trò của AirQuality trong survey

Các mục trước đã mô tả AirQuality dataset, quy trình preprocessing và cách xây dựng feature representation. Mục này đặt case study vào **toàn bộ taxonomy preprocessing** được xây dựng trong survey.

AirQuality không được sử dụng để giới thiệu một preprocessing method mới. Thay vào đó, dataset đóng vai trò **empirical case study** để kiểm chứng cách các nhóm phương pháp trong survey được áp dụng trên một dữ liệu cảm biến chuỗi thời gian thực tế.

Mối quan hệ tổng quát được biểu diễn:

$$
\mathrm{Preprocessing\ Taxonomy}\rightarrow\mathrm{AirQuality\ Case\ Study}\rightarrow\mathrm{Empirical\ Evaluation}
$$

Do đó, Chương 13 tạo cầu nối giữa phần phương pháp luận ở các Chương 3–8 và phần đánh giá thực nghiệm ở Chương 9.

---

## 2. Mapping giữa Survey và AirQuality

Các thành phần của AirQuality case study có thể ánh xạ với taxonomy của survey như sau:

| Survey                   | AirQuality                          | Vai trò                                     |
| ------------------------ | ----------------------------------- | ------------------------------------------- |
| `03_data_cleaning`       | Missing values, outliers            | Kiểm soát chất lượng dữ liệu                |
| `04_data_transformation` | Normalization                       | Chuẩn hóa feature space                     |
| `05_feature_engineering` | Temporal và sequence representation | Khai thác cấu trúc thời gian                |
| `06_feature_selection`   | NCA, Laplacian Scores               | Giảm feature redundancy                     |
| `07_sensor_fusion`       | Sensor + pollutant + environment    | Kết hợp nhiều nguồn measurement             |
| `08_data_compression`    | Không phải thành phần chính         | Phân biệt compression với feature reduction |
| `09_empirical_analysis`  | Preprocessing experiments           | Định lượng tác động của preprocessing       |
| `10_discussion`          | Comparison và trade-offs            | Phân tích ưu nhược điểm                     |
| `11_pipeline`            | End-to-end preprocessing            | Chuyển raw data thành model-ready data      |

Mapping này cho thấy AirQuality có khả năng bao phủ nhiều nhóm preprocessing khác nhau trong cùng một dataset.

---

## 3. Connection với Data Cleaning

Trong `03_data_cleaning`, survey xem **missing data** và **outlier** là hai vấn đề trung tâm của data quality.

AirQuality thể hiện rõ cả hai vấn đề này.

Giá trị `-200` được sử dụng làm missing-value marker:

$$
x_t=-200\Rightarrow x_t=\mathrm{NaN}
$$

Sau đó, outliers được phát hiện bằng các phương pháp như Grubbs Test hoặc IQR.

Do đó, case study minh họa pipeline:

$$
\mathrm{Raw\ Value}\rightarrow\mathrm{Missing/Outlier\ Detection}\rightarrow\mathrm{Treatment}
$$

Một nguyên tắc quan trọng được thể hiện ở đây là:

$$
\boxed{\mathrm{Detection}\neq\mathrm{Treatment}}
$$

Việc phát hiện một observation là outlier không đồng nghĩa với việc phải xóa observation đó. Trong AirQuality, interpolation được sử dụng để thay thế các giá trị bất thường và duy trì temporal structure.

---

## 4. Connection với Missing Data

AirQuality đặc biệt phù hợp để minh họa nội dung `03_data_cleaning/01_missing_data.md`.

Có thể phân biệt:

$$
\mathrm{Missing\ Value}
$$

và:

$$
\mathrm{Missing\ Sequence}
$$

Các trường hợp missing khác nhau yêu cầu các chiến lược khác nhau.

Đối với missing values cô lập:

$$
x_t=\mathrm{NaN}\Rightarrow x_t\leftarrow\hat{x}_t
$$

với $\hat{x}_t$ được ước lượng bằng interpolation.

Đối với missing sequences dài, bài báo sử dụng Expectation Maximization.

Điều này minh họa nguyên tắc:

$$
\boxed{\mathrm{Method\ Selection}\propto\mathrm{Missing\ Pattern}}
$$

Nói cách khác, không nên lựa chọn imputation method chỉ dựa trên tên thuật toán mà phải xem xét **cấu trúc của missingness**.

---

## 5. Connection với Outlier Detection

Trong `03_data_cleaning/02_outlier_detection.md`, survey phân biệt các nhóm phương pháp statistical, distance-based và density-based.

AirQuality sử dụng các phương pháp thống kê:

$$
\mathrm{Grubbs\ Test}
$$

và:

$$
\mathrm{IQR}
$$

Điều này tạo ra một trường hợp thực tế để minh họa rằng lựa chọn outlier detector phụ thuộc vào đặc điểm dữ liệu.

Grubbs Test phù hợp hơn với các trường hợp có giả định phân phối phù hợp, trong khi IQR ít phụ thuộc hơn vào assumption về normality.

Do đó:

$$
\boxed{\mathrm{Outlier\ Method}\neq\mathrm{Universal}}
$$

Một phương pháp tốt trên feature này không nhất thiết là phương pháp tốt nhất trên feature khác.

---

## 6. Connection với Data Transformation

Chương `04_data_transformation` trình bày scaling và normalization như các phương pháp thay đổi representation nhưng không nhất thiết thay đổi thứ tự tương đối của observations.

Trong AirQuality, normalization được sử dụng để giảm ảnh hưởng của sự khác biệt về magnitude giữa các feature.

Ví dụ Min-Max transformation:

$$
x'=\frac{x-x_{\min}}{x_{\max}-x_{\min}}
$$

Khi đó:

$$
x'\in[0,1]
$$

Điều này đặc biệt quan trọng khi các feature có đơn vị và scale khác nhau.

AirQuality vì vậy minh họa mối quan hệ:

$$
\mathrm{Heterogeneous\ Scale}\rightarrow\mathrm{Normalization}\rightarrow\mathrm{Stable\ Model\ Input}
$$

Tuy nhiên, normalization không tự động làm dữ liệu "tốt hơn". Nó chỉ phù hợp khi scale của feature tạo ra vấn đề đối với downstream model.

---

## 7. Connection với Feature Engineering

Chương `05_feature_engineering` phân biệt:

* temporal features;
* lag features;
* rolling features;
* feature representation.

AirQuality cho thấy temporal structure có thể được khai thác trực tiếp thông qua sequence representation:

$$
\mathbf{X}*{t-L+1:t}=\left[\mathbf{x}*{t-L+1},\mathbf{x}_{t-L+2},\ldots,\mathbf{x}_t\right]
$$

Trong đó:

$$
\mathbf{x}_t\in\mathbb{R}^{F}
$$

và:

$$
\mathbf{X}_{t-L+1:t}\in\mathbb{R}^{L\times F}
$$

LSTM sử dụng representation này để học dependency giữa các observations.

Do đó, case study cho thấy feature engineering trong time series không nhất thiết phải tạo thêm hàng loạt feature. Nó có thể là quá trình **chuyển đổi dữ liệu từ observation-level sang sequence-level representation**.

---

## 8. Connection với Feature Selection

Feature selection là một thành phần quan trọng trong experimental pipeline của bài báo.

Hai phương pháp được sử dụng:

$$
\mathrm{NCA}
$$

và:

$$
\mathrm{Laplacian\ Score}
$$

Điều này liên kết trực tiếp với `06_feature_selection`.

Nếu feature space ban đầu có (F) features:

$$
\mathbf{x}_t\in\mathbb{R}^{F}
$$

sau selection:

$$
\mathbf{x}_t^{*}\in\mathbb{R}^{F^{*}}
$$

với:

$$
F^{*}\leq F
$$

Feature selection do đó thực hiện hai chức năng:

1. loại bỏ feature ít hữu ích;
2. giảm complexity của representation.

Tuy nhiên:

$$
F^{*} \lt F
$$

không đồng nghĩa với:

$$
\mathrm{Performance}(F^{*}) \gt \mathrm{Performance}(F)
$$

Đây chính là lý do feature selection cần được đánh giá empirically thay vì giả định rằng giảm dimensionality luôn có lợi.

---

## 9. Connection với Sensor Fusion

AirQuality chứa nhiều nguồn information:

$$
\mathrm{Sensor}+\mathrm{Pollutant}+\mathrm{Environment}
$$

Có thể biểu diễn feature vector:

$$
\mathbf{x}_t=\left[\mathbf{s}_t,\mathbf{p}_t,\mathbf{e}_t\right]
$$

trong đó:

* $\mathbf{s}_t$: sensor responses;
* $\mathbf{p}_t$: pollutant measurements;
* $\mathbf{e}_t$: environmental measurements.

Đây là một ví dụ của **feature-level fusion**.

Các measurements cần được căn chỉnh theo cùng temporal index:

$$
t_{\mathrm{sensor}}=t_{\mathrm{pollutant}}=t_{\mathrm{environment}}
$$

Nếu không, feature vector có thể chứa information của các thời điểm khác nhau.

Do đó, AirQuality liên kết `07_sensor_fusion` với `07_sensor_fusion/03_temporal_alignment.md`.

---

## 10. Connection với Data Compression

`08_data_compression` tập trung vào việc giảm chi phí lưu trữ hoặc truyền tải dữ liệu.

Trong AirQuality case study, compression không phải là thành phần chính của experimental preprocessing pipeline.

Điểm quan trọng là phân biệt:

$$
\mathrm{Compression}\neq\mathrm{Feature\ Selection}
$$

Feature selection làm giảm số lượng semantic variables:

$$
F\rightarrow F^{*}
$$

trong khi compression tìm cách biểu diễn dữ liệu bằng ít storage hoặc transmission cost hơn mà vẫn giữ information cần thiết.

Do đó, AirQuality giúp xác định ranh giới giữa **representation reduction** và **data compression**.

---

## 11. Connection với Empirical Analysis

Vai trò quan trọng nhất của AirQuality là cung cấp nền tảng cho `09_empirical_analysis`.

Thay vì chỉ hỏi:

> Phương pháp preprocessing nào tồn tại?

nghiên cứu chuyển sang câu hỏi:

> Phương pháp preprocessing nào thực sự cải thiện kết quả trên dữ liệu thực tế?

Một preprocessing configuration có thể biểu diễn:

$$
C=(M,O,I,F,N)
$$

trong đó:

* $M$: missing-data method;
* $O$: outlier detection;
* $I$: imputation;
* $F$: feature selection;
* $N$: normalization.

Với mỗi configuration $C_i$, mô hình LSTM được đánh giá bằng cùng experimental protocol.

Khi đó:

$$
P_i=\mathrm{Performance}(C_i)
$$

và các configuration có thể được so sánh thông qua:

$$
\Delta P_i=P_i-P_{\mathrm{baseline}}
$$

Cách tiếp cận này biến preprocessing từ một **data preparation step** thành một **experimental factor**.

---

## 12. Connection với Evaluation Metrics

Bài báo sử dụng:

$$
\mathrm{RMSE}
$$

$$
\mathrm{MAE}
$$

và:

$$
\mathrm{MAPE}
$$

để đánh giá prediction performance.

RMSE:

$$
\mathrm{RMSE}=\sqrt{\frac{1}{N}\sum_{i=1}^{N}(y_i-\hat{y}_i)^2}
$$

MAE:

$$
\mathrm{MAE}=\frac{1}{N}\sum_{i=1}^{N}|y_i-\hat{y}_i|
$$

MAPE:

$$
\mathrm{MAPE}=\frac{100}{N}\sum_{i=1}^{N}\left|\frac{y_i-\hat{y}_i}{y_i}\right|
$$

Các metrics này cho phép chuyển câu hỏi về preprocessing thành một đại lượng có thể đo lường:

$$
\mathrm{Preprocessing}\rightarrow\mathrm{Prediction\ Performance}
$$

Từ đó, effectiveness của preprocessing được đánh giá thông qua downstream task thay vì chỉ thông qua statistics của dataset.

---

## 13. Connection với Trade-offs

AirQuality cũng minh họa các trade-offs được trình bày trong `10_discussion/02_tradeoffs.md`.

### Cleaning vs information preservation

Aggressive outlier removal có thể giảm noise nhưng đồng thời loại bỏ những observation thực tế.

$$
\mathrm{Cleaning}\uparrow\Rightarrow\mathrm{Noise}\downarrow
$$

nhưng:

$$
\mathrm{Cleaning}\uparrow\Rightarrow\mathrm{Information\ Loss}\uparrow
$$

### Feature selection vs information

Giảm feature dimension:

$$
F^{*} \lt F
$$

có thể giảm redundancy và computational cost, nhưng có nguy cơ loại bỏ predictive information.

### Transformation vs interpretability

Normalization đưa các feature về cùng scale nhưng làm mất phần nào ý nghĩa trực tiếp của magnitude ban đầu.

### Preprocessing complexity vs performance

Một pipeline phức tạp hơn:

$$
C_{\mathrm{complex}}>C_{\mathrm{simple}}
$$

không đảm bảo:

$$
P_{\mathrm{complex}}>P_{\mathrm{simple}}
$$

Do đó, preprocessing cần được lựa chọn dựa trên **empirical evidence**, không chỉ dựa trên số lượng kỹ thuật được sử dụng.

---

## 14. Connection với AI-ready Data Pipeline

Chương `11_pipeline` định nghĩa preprocessing như một chuỗi biến đổi từ raw data thành model-ready representation.

AirQuality có thể được ánh xạ:

```text
Raw AirQuality
      ↓
Missing-value Encoding
      ↓
Outlier Detection
      ↓
Imputation
      ↓
Feature Selection
      ↓
Normalization
      ↓
Temporal Sequence
      ↓
LSTM
      ↓
Prediction
```

Ở mỗi bước, representation được biến đổi:

$$
D_0\rightarrow D_1\rightarrow D_2\rightarrow\cdots\rightarrow D_k
$$

Mục tiêu cuối cùng là:

$$
D_k\in\mathrm{Model\text{-}Ready\ Data}
$$

Do đó, case study minh họa rằng AI-ready data không phải là một trạng thái cố định. Nó phụ thuộc vào **downstream model và task**.

---

## 15. Connection với Lessons Learned

AirQuality cung cấp một số bài học tổng quát cho toàn bộ survey.

### 15.1. Dataset semantics phải được hiểu trước preprocessing

Giá trị `-200` nếu được xem là observation bình thường sẽ làm sai lệch toàn bộ pipeline.

Do đó:

$$
\boxed{\mathrm{Understand\ Data}\rightarrow\mathrm{Preprocess\ Data}}
$$

### 15.2. Không có preprocessing method tốt tuyệt đối

Grubbs, IQR, Spline, EM, NCA và Laplacian Scores giải quyết các vấn đề khác nhau.

Do đó:

$$
\mathrm{Best\ Method}=\mathrm{Context\ Dependent}
$$

### 15.3. Preprocessing phải phục vụ downstream task

Một preprocessing configuration chỉ thực sự có giá trị nếu nó cải thiện hoặc ít nhất không làm suy giảm mục tiêu của hệ thống.

$$
\mathrm{Preprocessing\ Quality}\not\equiv\mathrm{Data\ Appearance}
$$

Mà:

$$
\mathrm{Preprocessing\ Quality}\rightarrow\mathrm{Downstream\ Utility}
$$

### 15.4. Temporal structure phải được bảo toàn

AirQuality là time series nên việc randomize hoặc phá vỡ temporal ordering có thể làm thay đổi bản chất bài toán.

Do đó:

$$
\boxed{\mathrm{Temporal\ Order}\rightarrow\mathrm{Preserve}}
$$

---

## 16. Vị trí của AirQuality trong toàn bộ nghiên cứu

AirQuality đóng vai trò là **case study tích hợp** cho taxonomy preprocessing.

Luồng nghiên cứu có thể biểu diễn:

```text
03 Data Cleaning
       ↓
04 Data Transformation
       ↓
05 Feature Engineering
       ↓
06 Feature Selection
       ↓
07 Sensor Fusion
       ↓
08 Data Compression
       ↓
09 Empirical Analysis
       ↓
10 Discussion
       ↓
11 AI-ready Pipeline
       ↓
13 AirQuality Case Study
```

Trong đó, Chương 13 không thay thế các chương lý thuyết trước đó mà thực hiện quá trình:

$$
\mathrm{Theory}\rightarrow\mathrm{Method}\rightarrow\mathrm{Dataset}\rightarrow\mathrm{Experiment}
$$

AirQuality vì vậy là điểm kiểm chứng để xác định liệu các nguyên tắc preprocessing được trình bày trong survey có thực sự hữu ích trên dữ liệu cảm biến thực tế hay không.

---

## 17. Tổng kết

Mối liên hệ giữa AirQuality và toàn bộ survey có thể cô đọng thành:

$$
\boxed{\mathrm{Raw\ Data}\rightarrow\mathrm{Cleaning}\rightarrow\mathrm{Transformation}\rightarrow\mathrm{Feature\ Engineering}\rightarrow\mathrm{Feature\ Selection}\rightarrow\mathrm{Model\ Input}}
$$

và:

$$
\boxed{\mathrm{Preprocessing}\rightarrow\mathrm{LSTM}\rightarrow\mathrm{Evaluation}}
$$

AirQuality cho thấy preprocessing không phải là một tập hợp các thao tác độc lập. Các quyết định về missing values, outliers, imputation, normalization, feature selection và temporal representation có quan hệ với nhau và cùng quyết định chất lượng của representation cuối cùng.

Vì vậy, giá trị của case study nằm ở việc chứng minh một nguyên tắc trung tâm của survey:

$$
\boxed{\mathrm{Effective\ Preprocessing}=\mathrm{Data\ Quality}+\mathrm{Appropriate\ Representation}+\mathrm{Task\ Compatibility}}
$$

Đây là cầu nối trực tiếp từ phần **survey methodology** sang phần **empirical analysis**, đồng thời tạo cơ sở để các kết quả thực nghiệm trong Chương 9 được diễn giải dưới góc nhìn của toàn bộ taxonomy preprocessing.
