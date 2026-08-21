# 03. Feature Engineering

## 1. Vai trò của Feature Engineering

Trong `13_air_quality/01_dataset.md`, AirQuality được xác định là một **multivariate time-series dataset** gồm các phép đo chất ô nhiễm, phản hồi của cảm biến và các biến môi trường được ghi nhận theo thời gian. Sau các bước cleaning và preprocessing ở `02_preprocessing.md`, dữ liệu cần được biểu diễn dưới dạng phù hợp với mô hình học máy.

Trong context của bài báo, feature engineering không được xem là một bước tạo ra một tập lớn các feature thủ công như trong một số bài toán tabular truyền thống. Trọng tâm nằm ở việc **tổ chức và biểu diễn thông tin temporal, sensor và environmental** để mô hình LSTM có thể khai thác quan hệ giữa các quan sát liên tiếp.

Có thể khái quát:

$$
\mathrm{Raw\ Observations}\rightarrow\mathrm{Clean\ Features}\rightarrow\mathrm{Temporal\ Representation}\rightarrow\mathrm{LSTM\ Input}
$$

Điều này liên kết trực tiếp với Chương `05_feature_engineering`, đặc biệt là các khái niệm về temporal representation, lag structure và sequence representation.

---

## 2. Feature Space của AirQuality

Sau preprocessing, mỗi observation tại thời điểm $t$ có thể được biểu diễn bằng một feature vector:

$$
\mathbf{x}_t=\left[x_t^{(1)},x_t^{(2)},\ldots,x_t^{(F)}\right]^\top
$$

Trong đó $F$ là số lượng feature được giữ lại sau preprocessing và feature selection.

Target của bài toán là nồng độ Carbon Monoxide:

$$
y_t=\mathrm{CO}(t)
$$

Do đó, bài toán có thể được biểu diễn:

$$
\hat{y}_t=f(\mathbf{x}_t)
$$

với $f(\cdot)$ là mô hình học máy được sử dụng để ước lượng nồng độ CO.

Feature space ban đầu bao gồm ba nhóm thông tin chính:

```text
AirQuality Features
├── Pollutant measurements
├── Sensor responses
└── Environmental measurements
```

Các nhóm này có ý nghĩa khác nhau nhưng cùng được sử dụng để mô tả trạng thái chất lượng không khí tại một thời điểm.

---

## 3. Temporal Representation

AirQuality là dữ liệu chuỗi thời gian nên thứ tự của các observations phải được bảo toàn.

Với hai observations liên tiếp:

$$
\mathbf{x}*t,\mathbf{x}*{t+1}
$$

ta có:

$$
t<t+1
$$

và thứ tự này mang thông tin mà dữ liệu tabular thông thường không có.

Do đó, feature engineering không chỉ tập trung vào giá trị của từng observation mà còn phải bảo toàn temporal dependency:

$$
\mathbf{x}_1\rightarrow\mathbf{x}_2\rightarrow\cdots\rightarrow\mathbf{x}_T
$$

Đây là cơ sở để sử dụng LSTM trong bài báo.

LSTM nhận một sequence thay vì xem mỗi observation là một sample hoàn toàn độc lập:

$$
\mathbf{X}*{t-L+1:t}=\left[\mathbf{x}*{t-L+1},\mathbf{x}_{t-L+2},\ldots,\mathbf{x}_t\right]
$$

với:

$$
\mathbf{X}_{t-L+1:t}\in\mathbb{R}^{L\times F}
$$

Trong đó $L$ là số observations liên tiếp được đưa vào mô hình.

---

## 4. Sensor Features

Một đặc điểm quan trọng của AirQuality là dataset chứa các phản hồi của nhiều cảm biến hóa học.

Các sensor features có thể được biểu diễn:

$$
\mathbf{s}_t=\left[s_t^{(1)},s_t^{(2)},\ldots,s_t^{(K)}\right]
$$

Trong đó mỗi $s_t^{(k)}$ đại diện cho phản hồi của một sensor tại thời điểm $t$.

Các sensor measurements không nhất thiết tương ứng một-một với một chất ô nhiễm duy nhất. Hiện tượng **cross-sensitivity** khiến một sensor có thể phản ứng với nhiều loại khí khác nhau.

Do đó, feature engineering giữ lại mối quan hệ đa biến:

$$
\mathbf{s}_t\rightarrow y_t
$$

thay vì giả định:

$$
s_t^{(k)}\rightarrow y_t
$$

theo từng sensor độc lập.

Điều này đặc biệt phù hợp với các phương pháp feature selection được trình bày trong `02_preprocessing.md`, vì relevance của một feature cần được đánh giá trong **toàn bộ feature space**.

---

## 5. Pollutant Features

Ngoài sensor responses, dataset chứa các phép đo nồng độ của nhiều chất ô nhiễm.

Có thể biểu diễn nhóm pollutant features:

$$
\mathbf{p}_t=\left[p_t^{(1)},p_t^{(2)},\ldots,p_t^{(P)}\right]
$$

Các biến này cung cấp thông tin trực tiếp về trạng thái chất lượng không khí và có thể có quan hệ với target CO.

Do đó, feature representation tại thời điểm (t) có thể được khái quát:

$$
\mathbf{x}_t=\left[\mathbf{s}_t,\mathbf{p}_t,\mathbf{e}_t\right]
$$

trong đó:

* $\mathbf{s}_t$: sensor measurements;
* $\mathbf{p}_t$: pollutant measurements;
* $\mathbf{e}_t$: environmental measurements.

Cách biểu diễn này giúp phân biệt rõ **nguồn gốc của information** trong feature space.

---

## 6. Environmental Features

AirQuality cũng chứa các biến môi trường như:

* temperature;
* relative humidity;
* absolute humidity.

Nhóm này được biểu diễn:

$$
\mathbf{e}_t=\left[T_t,RH_t,AH_t\right]
$$

Các biến môi trường có thể ảnh hưởng đến:

1. trạng thái thực tế của không khí;
2. phản ứng của các cảm biến;
3. mối quan hệ giữa sensor response và pollutant concentration.

Do đó, environmental features không chỉ là auxiliary variables mà có thể đóng vai trò giải thích cho variation của sensor measurements.

Có thể khái quát:

$$
\mathbf{e}_t\rightarrow\mathbf{s}_t
$$

và:

$$
\left(\mathbf{s}_t,\mathbf{e}_t\right)\rightarrow y_t
$$

Đây là một trong những lý do AirQuality phù hợp để nghiên cứu preprocessing trên dữ liệu cảm biến đa biến.

---

## 7. Lag Representation

Đối với time series, giá trị hiện tại có thể phụ thuộc vào các observations trong quá khứ.

Một lag feature được định nghĩa:

$$
\mathrm{Lag}*k(x_t)=x*{t-k}
$$

Với target CO:

$$
\mathrm{Lag}*k(y_t)=y*{t-k}
$$

Lag representation cho phép biến temporal dependency thành explicit features.

Tuy nhiên, trong pipeline sử dụng LSTM, thông tin lịch sử có thể được cung cấp trực tiếp dưới dạng sequence:

$$
\mathbf{X}_{t-L+1:t}
$$

thay vì tạo riêng từng cột:

```text
CO_lag_1
CO_lag_2
CO_lag_3
...
CO_lag_L
```

Vì vậy cần phân biệt:

$$
\boxed{\mathrm{Explicit\ Lag\ Features}\neq\mathrm{Sequence\ Representation}}
$$

Explicit lag features chuyển temporal dependency thành các cột trong tabular representation, trong khi sequence representation giữ nguyên cấu trúc thứ tự để LSTM học temporal dependency.

---

## 8. Rolling Representation

Rolling features tổng hợp information trong một temporal neighborhood.

Ví dụ rolling mean:

$$
\mathrm{MA}*w(t)=\frac{1}{w}\sum*{i=1}^{w}x_{t-i}
$$

Rolling standard deviation:

$$
\mathrm{STD}*w(t)=\sqrt{\frac{1}{w}\sum*{i=1}^{w}\left(x_{t-i}-\bar{x}_t\right)^2}
$$

Các feature này có thể biểu diễn:

* local trend;
* local variability;
* short-term volatility;
* recent average concentration.

Tuy nhiên, rolling features phải được xây dựng theo temporal direction. Không được sử dụng information từ tương lai:

$$
\mathrm{RollingFeature}*t=f(x*{t-1},x_{t-2},\ldots)
$$

thay vì:

$$
f(x_{t-1},x_t,x_{t+1},\ldots)
$$

nếu mục tiêu là forecasting.

Đây là nguyên tắc **causal feature construction** đã được nhấn mạnh trong Chương 5.

---

## 9. Temporal Dependency và LSTM

LSTM được sử dụng trong bài báo vì khả năng mô hình hóa dependency giữa các observations theo thời gian.

Một sequence đầu vào có dạng:

$$
\mathbf{X}*{t-L+1:t}=\left[\mathbf{x}*{t-L+1},\mathbf{x}_{t-L+2},\ldots,\mathbf{x}_t\right]
$$

Tại mỗi time step, LSTM cập nhật hidden state:

$$
\mathbf{h}*t=\mathrm{LSTM}\left(\mathbf{x}*t,\mathbf{h}*{t-1},\mathbf{c}*{t-1}\right)
$$

Trong đó:

* $\mathbf{x}_t$: feature vector tại thời điểm $t$;
* $\mathbf{h}_{t-1}$: hidden state trước đó;
* $\mathbf{c}_{t-1}$: cell state trước đó.

Do đó, temporal feature engineering trong case study không chỉ là tạo thêm variables mà còn bao gồm **định dạng dữ liệu thành sequence phù hợp với inductive bias của LSTM**.

---

## 10. Feature Selection sau Feature Engineering

Feature engineering có thể tạo ra feature space lớn hơn:

$$
F_{\mathrm{engineered}} \gt F_{\mathrm{raw}}
$$

Nhưng việc tăng số lượng feature không đảm bảo prediction performance tăng.

Một feature có thể:

* redundant;
* noisy;
* highly correlated với feature khác;
* ít liên quan đến target;
* làm tăng computational cost.

Do đó, feature engineering cần kết hợp với feature selection:

$$
\mathrm{Feature\ Engineering}\rightarrow\mathrm{Feature\ Selection}
$$

Trong bài báo, **Neighborhood Component Analysis (NCA)** và **Laplacian Scores** được sử dụng để đánh giá feature relevance.

Điều này liên kết trực tiếp `05_feature_engineering` với `06_feature_selection`.

---

## 11. Feature Representation sau Selection

Sau feature selection, feature vector có thể được biểu diễn:

$$
\mathbf{x}_t^{*}\in\mathbb{R}^{F^{*}}
$$

với:

$$
F^{*}\leq F
$$

Trong đó $\mathbf{x}_t^{*}$ chỉ chứa các feature được giữ lại.

Sequence đầu vào tương ứng:

$$
\mathbf{X}*{t-L+1:t}^{*}=\left[\mathbf{x}*{t-L+1}^{*},\mathbf{x}_{t-L+2}^{*},\ldots,\mathbf{x}_{t}^{*}\right]
$$

và:

$$
\mathbf{X}_{t-L+1:t}^{*}\in\mathbb{R}^{L\times F^{*}}
$$

Đây là representation gần với input cuối cùng của LSTM hơn so với raw dataset.

---

## 12. Tránh Data Leakage trong Feature Engineering

Một nguyên tắc quan trọng khi xây dựng temporal features là không sử dụng information từ Test hoặc tương lai để tạo feature cho Train.

Ví dụ, rolling statistic:

$$
\mathrm{RollMean}*t=\frac{1}{w}\sum*{i=1}^{w}x_{t-i}
$$

chỉ sử dụng historical observations.

Nếu sử dụng:

$$
\frac{1}{w}\sum_{i=-a}^{b}x_{t+i}
$$

với (b>0), feature tại (t) sẽ chứa information từ tương lai.

Tương tự, các statistical parameters được học từ dữ liệu phải tuân thủ:

$$
\theta=f(D_{\mathrm{train}})
$$

thay vì:

$$
\theta=f(D_{\mathrm{train}}\cup D_{\mathrm{test}})
$$

Điều này bảo đảm feature representation không chứa information leakage.

---

## 13. Feature Engineering và Sensor Fusion

AirQuality là dữ liệu từ nhiều nguồn sensor và measurement systems. Do đó, feature engineering cũng có thể được xem xét dưới góc độ sensor fusion.

Feature vector tại (t):

$$
\mathbf{x}_t=\left[\mathbf{s}_t,\mathbf{p}_t,\mathbf{e}_t\right]
$$

kết hợp:

$$
\mathrm{Sensor}+\mathrm{Pollutant}+\mathrm{Environment}
$$

trong cùng một representation.

Điều này liên kết với Chương `07_sensor_fusion`, trong đó **feature-level fusion** được sử dụng để đưa các nguồn thông tin khác nhau vào cùng feature space.

Temporal alignment là điều kiện cần:

$$
t_{\mathrm{sensor}}=t_{\mathrm{pollutant}}=t_{\mathrm{environment}}
$$

Nếu các nguồn không được căn chỉnh theo cùng temporal index, feature vector có thể kết hợp các measurements thuộc những thời điểm khác nhau và làm sai lệch quan hệ giữa các biến.

---

## 14. Feature Engineering trong Context của Survey

Feature engineering của AirQuality có thể được ánh xạ với Chương 5 như sau:

| Survey concept          | AirQuality representation                     |
| ----------------------- | --------------------------------------------- |
| Temporal features       | Timestamp và thứ tự thời gian                 |
| Lag features            | Historical observations                       |
| Rolling features        | Local temporal statistics                     |
| Feature representation  | Sensor + pollutant + environmental vector     |
| Sequence representation | Window đưa vào LSTM                           |
| Feature selection       | NCA và Laplacian Scores                       |
| Sensor fusion           | Kết hợp sensor/environment/pollutant features |

Điểm quan trọng là các phương pháp này không nhất thiết được áp dụng đồng thời.

Thay vào đó:

$$
\mathrm{Raw\ Feature}
\rightarrow
\mathrm{Engineered\ Representation}
\rightarrow
\mathrm{Selected\ Representation}
\rightarrow
\mathrm{Model\ Input}
$$

được sử dụng để mô tả quá trình chuyển đổi từ dữ liệu gốc sang representation phù hợp với mô hình.

---

## 15. AI-ready Feature Representation

Sau toàn bộ preprocessing và feature engineering, dữ liệu có thể được biểu diễn ở hai mức.

### Observation-level

$$
\mathbf{x}_t^{*}\in\mathbb{R}^{F^{*}}
$$

Đây là feature vector của một timestamp.

### Sequence-level

$$
\mathbf{X}*{t-L+1:t}^{*}=\left[\mathbf{x}*{t-L+1}^{*},\mathbf{x}_{t-L+2}^{*},\ldots,\mathbf{x}_{t}^{*}\right]
$$

với:

$$
\mathbf{X}_{t-L+1:t}^{*}\in\mathbb{R}^{L\times F^{*}}
$$

Sequence-level representation phù hợp với LSTM vì nó bảo toàn cả:

$$
\mathrm{Feature\ Information}+\mathrm{Temporal\ Order}
$$

Đây chính là bước chuyển từ **preprocessed data** sang **model-ready representation**.

---

## 16. Kết luận

Feature engineering trong AirQuality chủ yếu tập trung vào việc **bảo toàn và biểu diễn cấu trúc đa biến của dữ liệu cảm biến theo thời gian**.

Các thành phần chính có thể khái quát:

$$
\boxed{\mathrm{Sensor}+\mathrm{Pollutant}+\mathrm{Environment}+\mathrm{Temporal\ Structure}}
$$

Sau feature selection, representation cuối cùng được đưa về dạng:

$$
\mathbf{x}_t^{*}\in\mathbb{R}^{F^{*}}
$$

hoặc dạng sequence:

$$
\mathbf{X}*{t-L+1:t}^{*}=\left[\mathbf{x}*{t-L+1}^{*},\mathbf{x}_{t-L+2}^{*},\ldots,\mathbf{x}_{t}^{*}\right]
$$

Qua đó, AirQuality minh họa một nguyên tắc quan trọng của survey:

$$
\boxed{\mathrm{Feature\ Engineering}\neq\mathrm{Adding\ More\ Features}}
$$

Mục tiêu thực sự của feature engineering là xây dựng **một representation chứa thông tin hữu ích, bảo toàn temporal structure, tránh data leakage và phù hợp với inductive bias của mô hình**.
