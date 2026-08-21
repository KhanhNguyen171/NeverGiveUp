# 04. Connection to Survey

## 1. Vai trò của case study trong survey

Các mục `13_uci_appliances/01_dataset.md`, `02_preprocessing.md` và `03_feature_engineering.md` đã chuyển bộ dữ liệu **UCI Appliances Energy Prediction** từ dạng dữ liệu chuỗi thời gian thô sang biểu diễn phù hợp cho bài toán dự báo. Mục này tổng hợp mối liên hệ giữa case study và taxonomy preprocessing được xây dựng trong toàn bộ survey.

Mục tiêu của phần này không giới thiệu thêm một phương pháp preprocessing mới, mà là **kiểm chứng cách các nguyên tắc lý thuyết trong survey được áp dụng trên một dataset thực tế**.

Có thể khái quát mối quan hệ:

$$
\mathrm{Survey\ Methods}\rightarrow\mathrm{UCI\ Case\ Study}\rightarrow\mathrm{AI\text{-}ready\ Data}
$$

Trong đó, survey cung cấp cơ sở phương pháp luận, còn UCI Appliances đóng vai trò trường hợp thực nghiệm để đánh giá tính phù hợp của các phương pháp đó.

---

## 2. Mapping giữa survey và UCI Appliances

Pipeline preprocessing được xây dựng trong các chương trước có thể ánh xạ trực tiếp sang case study:

| Survey                   | UCI Appliances                            | Vai trò                                |
| ------------------------ | ----------------------------------------- | -------------------------------------- |
| `03_data_cleaning`       | Timestamp, missing, duplicate, continuity | Kiểm soát chất lượng dữ liệu           |
| `04_data_transformation` | Scaling, transformation, stationarity     | Đưa feature về representation phù hợp  |
| `05_feature_engineering` | Temporal, lag, rolling                    | Khai thác temporal dependency          |
| `06_feature_selection`   | Feature groups, control features          | Kiểm soát dimensionality và redundancy |
| `07_sensor_fusion`       | Indoor + outdoor measurements             | Kết hợp nhiều nguồn cảm biến           |
| `08_data_compression`    | Không phải preprocessing chính            | Phân tích khả năng giảm dữ liệu        |
| `09_empirical_analysis`  | Experimental evaluation                   | Đánh giá ảnh hưởng của preprocessing   |
| `10_discussion`          | Comparison và trade-offs                  | Phân tích lựa chọn phương pháp         |
| `11_pipeline`            | UCI preprocessing pipeline                | Chuyển dữ liệu thành AI-ready data     |

Mapping này cho thấy case study không phải một pipeline tách biệt mà là **một instantiation cụ thể của framework preprocessing được trình bày trong survey**.

---

## 3. Data Cleaning

Trong survey, data cleaning được chia thành các vấn đề như missing data, outlier và noise.

Đối với UCI Appliances, dữ liệu gốc được công bố không chứa missing values trong các thuộc tính chính. Tuy nhiên, bước kiểm tra missing vẫn được giữ trong pipeline để đảm bảo tính toàn vẹn của dữ liệu.

Đối với timestamp, preprocessing phải kiểm tra:

$$
\Delta t_i=t_{i+1}-t_i
$$

và kỳ vọng:

$$
\Delta t_i=10\text{ minutes}
$$

Điều này mở rộng khái niệm data cleaning từ việc kiểm tra giá trị của từng cell sang kiểm tra **tính toàn vẹn của cấu trúc temporal**.

Đối với outlier, nguyên tắc trong survey rằng outlier không đồng nghĩa với lỗi được giữ nguyên. Một giá trị tiêu thụ cao có thể là một sự kiện thực tế và không nên bị loại bỏ chỉ dựa trên ngưỡng thống kê.

Do đó:

$$
\mathrm{Outlier}\neq\mathrm{Error}
$$

là nguyên tắc quan trọng được kiểm chứng trong case study.

---

## 4. Data Transformation

Chương `04_data_transformation` trình bày scaling, normalization, transformation, stationarity và decomposition.

Trong UCI Appliances, sự khác biệt về đơn vị giữa nhiệt độ, độ ẩm, áp suất, tốc độ gió và năng lượng khiến scaling trở thành bước cần thiết đối với các mô hình nhạy với scale.

Standardization được thực hiện theo:

$$
x'=\frac{x-\mu_{\mathrm{train}}}{\sigma_{\mathrm{train}}}
$$

với:

$$
\mu_{\mathrm{train}},\sigma_{\mathrm{train}}=f(D_{\mathrm{train}})
$$

Điểm quan trọng không chỉ là sử dụng StandardScaler mà là **chỉ fitting scaler trên Train**.

Do đó, case study minh họa nguyên tắc:

$$
\boxed{\mathrm{Transformation}\rightarrow\mathrm{Fit\ on\ Train}\rightarrow\mathrm{Apply\ to\ Val/Test}}
$$

Đối với các temporal features đã được mã hóa bằng sine/cosine, việc scaling tiếp tục không mang lại ý nghĩa cần thiết vì các feature này đã nằm trong miền:

$$
[-1,1]
$$

Do đó, transformation phải phụ thuộc vào **loại representation**, thay vì áp dụng cùng một phép biến đổi cho toàn bộ feature space.

---

## 5. Stationarity và temporal structure

Trong survey, stationarity được trình bày như một vấn đề quan trọng đối với time-series preprocessing.

UCI Appliances có các đặc điểm temporal như:

* chu kỳ trong ngày;
* chu kỳ theo tuần;
* biến động của điều kiện môi trường;
* thay đổi mức tiêu thụ theo thời gian.

Do đó, thay vì giả định dữ liệu hoàn toàn stationary, case study tập trung vào việc **biểu diễn temporal dependency một cách trực tiếp** thông qua temporal, lag và rolling features.

Có thể biểu diễn quá trình:

$$
\mathrm{Timestamp}\rightarrow\mathrm{Temporal\ Representation}
$$

và:

$$
\mathrm{Historical\ Observations}\rightarrow\mathrm{Lag/Rolling\ Representation}
$$

Cách tiếp cận này không loại bỏ temporal structure mà biến nó thành thông tin có thể khai thác bởi mô hình.

---

## 6. Feature Engineering

Chương `05_feature_engineering` cung cấp cơ sở trực tiếp cho case study.

Temporal features chuyển timestamp thành các biến chu kỳ:

$$
\mathrm{hour}\rightarrow(\mathrm{hour}*{\sin},\mathrm{hour}*{\cos})
$$

và:

$$
\mathrm{dow}\rightarrow(\mathrm{dow}*{\sin},\mathrm{dow}*{\cos})
$$

Lag features biểu diễn dependency lịch sử:

$$
\mathrm{lag}*k(t)=y*{t-k}
$$

Rolling features tổng hợp trạng thái quá khứ:

$$
\mathrm{rollmean}*w(t)=\frac{1}{w}\sum*{i=1}^{w}y_{t-i}
$$

Ba nhóm này minh họa ba cách khác nhau để đưa temporal information vào feature space:

```text
Timestamp
   │
   ├── Temporal Features
   │
Historical Values
   │
   ├── Lag Features
   │
   └── Rolling Features
```

Do đó, UCI Appliances là một trường hợp phù hợp để minh họa rằng feature engineering cho time series không đơn giản là tạo thêm cột, mà là **thiết kế representation dựa trên cấu trúc thời gian của bài toán**.

---

## 7. Feature Selection

Feature engineering có thể làm tăng số lượng đặc trưng:

$$
F_{\mathrm{engineered}} \gt F_{\mathrm{raw}}
$$

Khi đó, feature selection trở thành bước kiểm soát dimensionality và redundancy.

Trong case study, các feature được tổ chức theo nhóm:

$$
G={G_0,G_1,G_2,G_3,G_4}
$$

trong đó các nhóm đại diện cho metadata, target, raw exogenous features, random controls và engineered temporal features.

Cách tổ chức này cho phép thực hiện các thí nghiệm so sánh giữa các feature configurations thay vì chỉ sử dụng một feature set duy nhất.

Đặc biệt, `rv1` và `rv2` đóng vai trò control variables. Nếu mô hình khai thác mạnh các biến này, đó có thể là dấu hiệu rằng mô hình đang tận dụng các pattern ngẫu nhiên hoặc noise.

Do đó, feature selection trong case study không chỉ nhằm giảm số chiều mà còn phục vụ **diagnostic analysis**.

---

## 8. Sensor Fusion

UCI Appliances chứa nhiều nguồn dữ liệu:

$$
\mathrm{Indoor}+\mathrm{Outdoor}+\mathrm{Energy}
$$

Các phép đo nhiệt độ và độ ẩm trong nhiều khu vực được kết hợp với thông tin thời tiết bên ngoài và mức tiêu thụ năng lượng.

Điều này liên kết trực tiếp với `07_sensor_fusion`.

Trong trường hợp này, fusion chủ yếu xảy ra ở **feature level**. Các nguồn cảm biến được căn chỉnh theo timestamp và sau đó được biểu diễn trong cùng feature vector:

$$
\mathbf{x}_t=\left[\mathbf{x}_t^{\mathrm{indoor}},\mathbf{x}_t^{\mathrm{outdoor}},\mathbf{x}_t^{\mathrm{energy}}\right]
$$

Do đó, case study minh họa rằng sensor fusion không chỉ là kết hợp nhiều sensor mà còn yêu cầu **temporal alignment** trước khi các nguồn dữ liệu được đưa vào cùng representation.

---

## 9. Data Compression

Chương `08_data_compression` tập trung vào giảm kích thước dữ liệu thông qua lossless và lossy compression.

Trong UCI Appliances, compression không phải là thành phần preprocessing bắt buộc của pipeline forecasting. Tuy nhiên, case study cho thấy một vấn đề liên quan: feature engineering có thể làm tăng kích thước representation.

Nếu số lượng feature ban đầu là $F_0$, sau feature engineering có thể:

$$
F_1 \gt F_0
$$

và sau feature selection:

$$
F_2\leq F_1
$$

Do đó, dimensionality reduction trong `06_feature_selection/05_dimensionality_reduction.md` có thể được xem như một hướng giảm representation ở cấp feature, trong khi compression tập trung vào giảm chi phí lưu trữ hoặc truyền tải dữ liệu.

Hai mục tiêu này cần được phân biệt:

$$
\mathrm{Dimensionality\ Reduction}\neq\mathrm{Data\ Compression}
$$

---

## 10. AI-ready Representation

Chương `11_pipeline` định nghĩa AI-ready data là dữ liệu đã trải qua các bước cần thiết để có thể đưa trực tiếp vào mô hình.

Đối với UCI Appliances, representation cuối cùng có dạng:

$$
\mathbf{X}_{t-L+1:t}=\left[\mathbf{x}_{t-L+1},\mathbf{x}_{t-L+2},\ldots,\mathbf{x}_t\right]
$$

với:

$$
\mathbf{X}_{t-L+1:t}\in\mathbb{R}^{L\times F}
$$

và target:

$$
y_{t+1}=\mathrm{Appliances}_{t+1}
$$

Toàn bộ dataset được biểu diễn:

$$
\mathcal{D}=\left\{\left(\mathbf{X}_{t-L+1:t},y_{t+1}\right)\right\}_{t=L}^{N-1}
$$

với:

$$
L\in{36,72,144}
$$

Do đó, preprocessing đã chuyển dữ liệu từ:

$$
\mathrm{Raw\ Tabular\ Time\ Series}
$$

sang:

$$
\mathrm{AI\text{-}ready\ Sequential\ Representation}
$$

Đây chính là mục tiêu cuối cùng của pipeline được xây dựng trong survey.

---

## 11. Empirical Analysis

Case study UCI Appliances cũng tạo nền tảng cho `09_empirical_analysis`.

Các phương pháp preprocessing không được đánh giá chỉ dựa trên lý thuyết mà cần được kiểm chứng thông qua thực nghiệm.

Một cấu hình preprocessing có thể được biểu diễn:

$$
C=(S,F,T,W)
$$

trong đó:

* $S$: scaling configuration;
* $F$: feature configuration;
* $T$: temporal feature configuration;
* $W$: window configuration.

Với mỗi cấu hình $C$, mô hình được huấn luyện trên cùng chronological split và đánh giá bằng cùng metric protocol.

Điều này cho phép nghiên cứu trả lời câu hỏi:

$$
\mathrm{Does\ preprocessing\ configuration\ affect\ forecasting\ performance?}
$$

Thay vì chỉ kết luận rằng một phương pháp preprocessing "tốt", nghiên cứu có thể đánh giá **khi nào và trong điều kiện nào phương pháp đó có lợi**.

---

## 12. Trade-offs

Case study cũng minh họa các trade-off được trình bày trong `10_discussion/02_tradeoffs.md`.

### Information vs dimensionality

Tăng số lượng lag và rolling features có thể cung cấp nhiều temporal information hơn:

$$
F\uparrow\Rightarrow\mathrm{Information}\uparrow
$$

nhưng đồng thời:

$$
F\uparrow\Rightarrow\mathrm{Complexity}\uparrow
$$

### Representation vs interpretability

Temporal encoding bằng sine/cosine biểu diễn chu kỳ tốt hơn số nguyên nhưng làm representation khó diễn giải trực tiếp hơn.

### History vs computational cost

Tăng lookback:

$$
L:36\rightarrow72\rightarrow144
$$

cho phép mô hình quan sát lịch sử dài hơn nhưng đồng thời làm tăng kích thước input:

$$
\mathrm{Input\ Size}=L\times F
$$

Do đó, preprocessing luôn là bài toán cân bằng giữa **information, complexity, computational cost và interpretability**.

---

## 13. Lessons Learned

Từ việc áp dụng taxonomy vào UCI Appliances, có thể rút ra một số nguyên tắc.

### 13.1. Preprocessing phụ thuộc vào loại dữ liệu

Không tồn tại một preprocessing pipeline tối ưu cho mọi dataset. Với time series, temporal order và causality phải được ưu tiên.

### 13.2. Data leakage quan trọng hơn việc chọn thuật toán

Một pipeline sử dụng scaler hoặc feature statistics từ toàn bộ dataset có thể tạo ra kết quả đánh giá quá lạc quan, ngay cả khi model hoàn toàn chính xác về mặt implementation.

### 13.3. Feature engineering phải dựa trên domain structure

Temporal, lag và rolling features có ý nghĩa vì chúng phản ánh cấu trúc của bài toán energy forecasting, không phải vì chúng đơn giản là các phép biến đổi phổ biến.

### 13.4. Không phải feature càng nhiều càng tốt

Feature engineering tạo thêm information nhưng đồng thời làm tăng dimensionality và redundancy. Vì vậy, feature engineering cần kết hợp với feature selection.

### 13.5. AI-ready data là kết quả của toàn bộ pipeline

Không thể xem scaling, cleaning hoặc feature engineering là những bước độc lập. Representation cuối cùng phải đồng thời thỏa mãn:

$$
\boxed{\mathrm{Quality}+\mathrm{Consistency}+\mathrm{Causality}+\mathrm{Model\ Compatibility}}
$$

---

## 14. Vị trí của UCI Appliances trong toàn bộ nghiên cứu

UCI Appliances đóng vai trò **case study tích hợp** cho survey.

Luồng liên kết của toàn bộ nghiên cứu có thể biểu diễn:

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
13 UCI Appliances Case Study
```

Trong đó, Chương 13 không lặp lại toàn bộ lý thuyết của các chương trước mà **instantiate** các khái niệm đó trên một dataset cụ thể.

Kết quả cuối cùng là:

$$
\mathrm{Raw\ UCI\ Data}
\rightarrow
\mathrm{Cleaned\ Data}
\rightarrow
\mathrm{Transformed\ Data}
\rightarrow
\mathrm{Engineered\ Features}
\rightarrow
\mathrm{Selected\ Representation}
\rightarrow
\mathrm{AI\text{-}ready\ Windows}
$$

Chuỗi biến đổi này thể hiện chính xác vai trò của preprocessing trong toàn bộ nghiên cứu: **chuyển dữ liệu thô thành một representation có chất lượng, không rò rỉ thông tin và phù hợp với mục tiêu học máy**.

---

## 15. Kết luận

UCI Appliances Energy Prediction cung cấp một trường hợp thực nghiệm phù hợp để kiểm chứng taxonomy preprocessing được xây dựng trong survey. Dataset đồng thời chứa các đặc trưng của dữ liệu thực tế như **temporal dependency, heterogeneous measurements, multiple sensor sources và biến động theo chu kỳ**, qua đó cho phép đánh giá nhiều nhóm preprocessing trong cùng một pipeline.

Mối liên hệ cốt lõi có thể tóm tắt:

$$
\boxed{\mathrm{Preprocessing\ Theory}\rightarrow\mathrm{Method\ Selection}\rightarrow\mathrm{UCI\ Implementation}\rightarrow\mathrm{Empirical\ Evaluation}}
$$

Do đó, case study không chỉ minh họa cách preprocessing được thực hiện, mà còn chứng minh rằng **việc lựa chọn preprocessing phải xuất phát từ cấu trúc dữ liệu, mục tiêu dự báo và ràng buộc thực nghiệm**. Đây là cầu nối từ phần survey lý thuyết sang phần empirical analysis và là cơ sở để đánh giá các trade-off của preprocessing trong một bài toán forecasting thực tế.
