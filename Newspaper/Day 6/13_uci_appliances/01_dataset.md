# 01. Air Quality Dataset

## 1. Dataset Overview

Nghiên cứu thực nghiệm của Tawakuli et al. sử dụng **AirQuality dataset** từ **UCI Machine Learning Repository** để đánh giá ảnh hưởng của các kỹ thuật tiền xử lý dữ liệu chuỗi thời gian lên chất lượng dữ liệu đầu vào và hiệu năng của mô hình học máy. Bài báo lựa chọn dataset này vì đây là dữ liệu cảm biến thực tế, đa biến và liên tục, phù hợp để đánh giá nhiều nhóm kỹ thuật preprocessing khác nhau.

AirQuality là một **multivariate time-series dataset** gồm **9,358 quan sát** và **15 biến**, với các giá trị được lấy trung bình theo giờ. Dữ liệu được thu thập từ một hệ thống cảm biến chất lượng không khí đặt tại một khu vực có mức độ ô nhiễm cao, ở cấp đường phố, trong một thành phố của Ý. Khoảng thời gian thu thập kéo dài từ **tháng 3 năm 2004 đến tháng 2 năm 2005**, tương ứng khoảng một năm dữ liệu.

Dataset chứa đồng thời các phép đo từ cảm biến hóa học và các nồng độ chất ô nhiễm được cung cấp bởi thiết bị phân tích tham chiếu. Chính sự kết hợp này tạo ra một dữ liệu thực tế có nhiều đặc điểm phù hợp để nghiên cứu preprocessing, bao gồm **missing values, outliers, khác biệt về scale, sensor drift và các mối quan hệ đa biến**.

---

## 2. Data Source and Acquisition

AirQuality dataset được xây dựng từ một **Air Quality Chemical Multisensor Device** gồm một mảng các cảm biến oxide kim loại. Hệ thống sử dụng năm cảm biến hóa học oxide kim loại để ghi nhận phản ứng đối với các chất khí khác nhau. Bên cạnh các tín hiệu cảm biến, dữ liệu còn chứa nồng độ chất ô nhiễm thực tế được đo bởi một thiết bị phân tích tham chiếu đặt cùng vị trí.

Các quan sát được tổng hợp theo giờ. Vì vậy, mỗi timestamp đại diện cho một observation ở độ phân giải một giờ:

$$
\Delta t=1\text{ hour}
$$

Cấu trúc này khiến dataset phù hợp với phạm vi của survey, vốn tập trung vào các kỹ thuật preprocessing áp dụng cho **numerical time-series data**.

Một đặc điểm quan trọng của dataset là sự tồn tại của **cross-sensitivities**, **concept drift** và **sensor drift**. Những hiện tượng này phản ánh các vấn đề thường gặp trong dữ liệu cảm biến thực tế và có thể ảnh hưởng đến khả năng ước lượng nồng độ chất ô nhiễm từ tín hiệu cảm biến.

Do đó, dataset không chỉ cung cấp một bài toán hồi quy mà còn tạo môi trường phù hợp để nghiên cứu tác động của preprocessing lên dữ liệu cảm biến có nhiễu và bất thường.

---

## 3. Dataset Structure

Theo UCI, AirQuality dataset có **15 biến**. Các biến bao gồm timestamp, nồng độ chất ô nhiễm được đo bằng thiết bị tham chiếu, phản hồi của các cảm biến hóa học, nhiệt độ, độ ẩm tương đối và độ ẩm tuyệt đối.

Các biến chính có thể được tổ chức thành các nhóm:

| Nhóm        | Biến tiêu biểu                                                                | Ý nghĩa                                         |
| ----------- | ----------------------------------------------------------------------------- | ----------------------------------------------- |
| Temporal    | `Date`, `Time`                                                                | Thời điểm quan sát                              |
| Target      | `CO(GT)`                                                                      | Nồng độ CO trung bình theo giờ                  |
| Sensor      | `PT08.S1(CO)`, `PT08.S2(NMHC)`, `PT08.S3(NOx)`, `PT08.S4(NO2)`, `PT08.S5(O3)` | Phản hồi của các cảm biến oxide kim loại        |
| Pollutants  | `NMHC(GT)`, `C6H6(GT)`, `NOx(GT)`, `NO2(GT)`                                  | Nồng độ chất ô nhiễm đo bởi thiết bị tham chiếu |
| Environment | `T`, `RH`, `AH`                                                               | Nhiệt độ, độ ẩm tương đối và độ ẩm tuyệt đối    |

Trong nghiên cứu của bài báo, biến **Carbon Monoxide (`CO`)** được lựa chọn làm response variable:

$$
y_t=\mathrm{CO}_t
$$

và các biến còn lại được sử dụng làm predictors:

$$
\mathbf{x}_t=\left[x_t^{(1)},x_t^{(2)},\ldots,x_t^{(14)}\right]
$$

Do đó, bài toán thực nghiệm có thể được biểu diễn dưới dạng:

$$
\mathbf{x}_t\rightarrow y_t
$$

trong đó mô hình học cách dự đoán nồng độ CO từ các biến cảm biến, chất ô nhiễm và điều kiện môi trường.

---

## 4. Missing Values

Một đặc điểm quan trọng của AirQuality dataset là missing values không được biểu diễn trực tiếp bằng `NaN` trong dữ liệu gốc. Thay vào đó, giá trị **`-200` được sử dụng như một giá trị đặc biệt để đánh dấu missing observations**. UCI xác nhận rằng dataset chứa missing values và các giá trị này được mã hóa bằng `-200`.

Do đó, bước đầu tiên trong preprocessing của bài báo là chuyển giá trị:

$$
-200\rightarrow\mathrm{NaN}
$$

Sau phép chuyển đổi này, missing values có thể được xử lý bằng các phương pháp imputation được khảo sát trong survey.

Điểm này có ý nghĩa quan trọng đối với Chương `03_data_cleaning/01_missing_data.md`: missing data không nhất thiết xuất hiện dưới dạng giá trị rỗng mà có thể được mã hóa bằng một **reserved value**. Vì vậy, preprocessing phải hiểu semantics của dataset trước khi thực hiện các phương pháp xử lý missing values.

---

## 5. Experimental Train-Test Split

Trong thực nghiệm của bài báo, AirQuality dataset được chia thành:

$$
D=D_{\mathrm{train}}\cup D_{\mathrm{test}}
$$

với tỷ lệ:

$$
D_{\mathrm{train}}=90%,\quad D_{\mathrm{test}}=10%
$$

Bài báo sử dụng phần dữ liệu 90% cho training và phần còn lại cho testing trong toàn bộ experimental setup nhằm kiểm soát sự khác biệt giữa các thí nghiệm.

Điểm cần phân biệt là **90/10 split này thuộc experimental protocol của bài báo**, không phải một quy tắc preprocessing tổng quát cho mọi time series.

Do đó, khi xây dựng case study, tỷ lệ này cần được giữ nguyên nếu mục tiêu là tái hiện thực nghiệm của bài báo.

---

## 6. Response Variable and Predictors

Bài toán thực nghiệm được xây dựng như một bài toán regression.

Target:

$$
y_t=\mathrm{CO}_t
$$

Input:

$$
\mathbf{x}_t\in\mathbb{R}^{14}
$$

và toàn bộ bài toán có thể biểu diễn:

$$
f:\mathbb{R}^{14}\rightarrow\mathbb{R}
$$

với:

$$
\hat{y}_t=f(\mathbf{x}_t)
$$

Mục tiêu của mô hình là giảm sai số giữa giá trị CO quan sát được $y_t$ và giá trị dự đoán $\hat{y}_t$.

Trong thực nghiệm, bài báo sử dụng **LSTM** làm mô hình dự báo. Kiến trúc gồm sequence input layer, LSTM layer với **200 hidden units**, fully connected layer và regression output layer. Mô hình được huấn luyện bằng Adam với learning rate ban đầu $0.005$ và tối đa 100 epochs.

Do đó, dataset đóng vai trò là đầu vào chung để đánh giá các preprocessing configurations trước khi đưa dữ liệu vào cùng một experimental model.

---

## 7. Preprocessing-Relevant Characteristics

AirQuality dataset được lựa chọn không chỉ vì có kích thước vừa phải mà chủ yếu vì nó chứa nhiều vấn đề preprocessing đại diện cho dữ liệu cảm biến thực tế.

### Missing values

Giá trị `-200` được sử dụng để biểu diễn missing observations:

$$
x_t=-200\Rightarrow x_t=\mathrm{NaN}
$$

Đây là vấn đề đầu tiên được xử lý trong pipeline.

### Outliers

Dataset chứa các quan sát bất thường trong một số biến cảm biến. Vì vậy, bài báo đánh giá các phương pháp phát hiện outlier như **Grubbs test** đối với các feature có phân phối phù hợp với giả định normal và **Interquartile Range (IQR)** đối với các trường hợp còn lại.

### Heterogeneous scales

Các biến có đơn vị và miền giá trị khác nhau, chẳng hạn nồng độ CO, NOx, NO2, nhiệt độ và độ ẩm. Vì vậy, normalization được đưa vào experimental preprocessing nhằm kiểm soát sự khác biệt về scale.

### Multivariate dependency

Các biến cảm biến và biến chất ô nhiễm có quan hệ với nhau. Vì vậy, một số kỹ thuật preprocessing yêu cầu xem xét đồng thời nhiều biến thay vì xử lý từng chuỗi độc lập.

### Sensor characteristics

Cross-sensitivity và sensor drift tạo ra những thách thức đặc thù của dữ liệu cảm biến. Điều này làm cho AirQuality trở thành một case study phù hợp để đánh giá preprocessing trong điều kiện dữ liệu thực tế thay vì dữ liệu được tạo nhân tạo.

---

## 8. Vai trò của AirQuality trong thực nghiệm của bài báo

Một điểm quan trọng cần phân biệt là bài báo **không chỉ sử dụng AirQuality để minh họa dataset**, mà sử dụng nó làm nền tảng cho toàn bộ empirical analysis.

Quy trình thực nghiệm được chuẩn hóa để các kỹ thuật preprocessing có thể được so sánh một cách công bằng. Pipeline mặc định của bài báo bao gồm:

```text
AirQuality Dataset
       ↓
Replace -200 with NaN
       ↓
Outlier Detection
       ↓
Outlier Imputation
       ↓
Missing Data Imputation
       ↓
Feature Selection
       ↓
Normalization
       ↓
LSTM
       ↓
RMSE / MAE / MAPE
```

Trong pipeline mặc định, bài báo sử dụng **Grubbs hoặc IQR** để phát hiện outlier tùy theo đặc điểm phân phối, **Cubic Spline Interpolation** để xử lý outlier, **Cubic Spline Interpolation** cho missing values cô lập và **Expectation Maximization (EM)** cho chuỗi missing values. Sau đó, **Neighborhood Component Analysis (NCA)** và **Laplacian Scores** được sử dụng cho feature selection.

Điểm quan trọng là pipeline này được xây dựng **cho experimental setup cụ thể của bài báo**, không được hiểu như một thứ tự bắt buộc cho mọi bài toán time-series preprocessing.

---

## 9. Evaluation Target

Sau preprocessing, dữ liệu được đưa vào LSTM để dự đoán CO. Ba metrics được sử dụng để đánh giá:

$$
\mathrm{RMSE}=\sqrt{\frac{1}{N}\sum_{i=1}^{N}(y_i-\hat{y}_i)^2}
$$

$$
\mathrm{MAE}=\frac{1}{N}\sum_{i=1}^{N}|y_i-\hat{y}_i|
$$

$$
\mathrm{MAPE}=\frac{100}{N}\sum_{i=1}^{N}\left|\frac{y_i-\hat{y}_i}{y_i}\right|
$$

Các predictions và observations được **denormalize về scale CO ban đầu** trước khi trình bày kết quả, nhằm đảm bảo metrics có thể được so sánh trên cùng đơn vị. Mỗi experiment được lặp ít nhất ba lần và kết quả trung bình của ba lần chạy cuối được sử dụng trong các bảng kết quả.

---

## 10. Dataset as a Case Study for the Survey

AirQuality có vị trí đặc biệt trong cấu trúc của nghiên cứu vì nó cho phép liên kết trực tiếp các nhóm preprocessing được khảo sát với một dữ liệu thực tế.

Có thể biểu diễn mối quan hệ:

$$
\mathrm{Raw\ AirQuality}\rightarrow\mathrm{Data\ Cleaning}\rightarrow\mathrm{Transformation}\rightarrow\mathrm{Feature\ Selection}\rightarrow\mathrm{LSTM}
$$

Trong đó:

* **Data Cleaning:** xử lý missing values và outliers;
* **Data Transformation:** điều chỉnh scale của features;
* **Feature Selection:** xác định các feature hữu ích;
* **Model Input:** tạo dữ liệu phù hợp với LSTM;
* **Evaluation:** đo tác động của preprocessing lên prediction performance.

Điều này làm cho AirQuality trở thành cầu nối giữa phần **survey lý thuyết** và phần **empirical analysis** của nghiên cứu.

---

## 11. Tóm tắt

AirQuality dataset là một **multivariate time-series dataset gồm 9,358 quan sát và 15 biến**, được ghi nhận theo giờ trong khoảng một năm tại một khu vực ô nhiễm ở Ý. Dataset kết hợp dữ liệu cảm biến hóa học, nồng độ chất ô nhiễm tham chiếu và các biến môi trường, đồng thời chứa missing values được mã hóa bằng `-200` và các đặc điểm thực tế như sensor drift và cross-sensitivity.

Trong bài báo, **CO được chọn làm response variable**, 14 biến còn lại được sử dụng làm predictors và dữ liệu được chia theo experimental protocol thành **90% training và 10% testing**. Các preprocessing techniques sau đó được thay đổi từng nhóm trong khi giữ các thành phần còn lại của pipeline cố định, cho phép đánh giá tác động riêng của từng kỹ thuật lên chất lượng dữ liệu và hiệu năng dự báo.

Vì vậy, AirQuality không chỉ là dataset minh họa mà là **experimental case study** của toàn bộ survey:

$$
\boxed{\mathrm{AirQuality}\rightarrow\mathrm{Preprocessing}\rightarrow\mathrm{LSTM}\rightarrow\mathrm{Evaluation}}
$$

Cách xây dựng này tạo nền tảng cho `13_uci_appliances/02_preprocessing.md` và `03_feature_engineering.md` trong cấu trúc hiện tại, nhưng **tên thư mục `13_uci_appliances/` nên được đổi thành `13_air_quality/`** để phản ánh đúng dataset và tránh mâu thuẫn về mặt học thuật.
