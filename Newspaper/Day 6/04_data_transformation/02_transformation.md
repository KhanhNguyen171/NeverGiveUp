# 4.2. Data Transformation

## 4.2.1. Vai trò của Transformation trong tiền xử lý

Ở mục `01_scaling_normalization.md`, scaling và normalization được trình bày với mục tiêu chính là đưa các đặc trưng về những thang đo phù hợp để tránh sự khác biệt về magnitude chi phối quá trình học. Tuy nhiên, việc đưa dữ liệu về cùng scale không đảm bảo rằng **phân bố của dữ liệu đã phù hợp với mô hình**.

Trong dữ liệu chuỗi thời gian, một biến có thể có phân bố lệch, heavy-tailed hoặc phương sai thay đổi theo mức độ của giá trị. Khi đó, vấn đề không còn đơn thuần là scale mà nằm ở **hình dạng của phân bố và quan hệ giữa giá trị với phương sai**.

Data transformation giải quyết vấn đề này bằng cách áp dụng một hàm biến đổi lên dữ liệu:

$$x'_t=f(x_t;\theta)$$

Mục tiêu của transformation trong phạm vi khảo sát là:

* giảm độ lệch của phân bố;
* nén các giá trị cực lớn;
* mở rộng tương đối vùng giá trị nhỏ;
* đưa phân bố gần hơn với Gaussian khi phù hợp;
* ổn định phương sai;
* làm cho một số quan hệ thống kê trở nên phù hợp hơn với mô hình.

Khác với scaling thuần túy, transformation có thể **thay đổi hình dạng phân bố của dữ liệu**, chứ không chỉ thay đổi đơn vị hoặc miền giá trị. Bài khảo sát đặc biệt đề cập đến Log Scaling và Box-Cox như các phép biến đổi có khả năng tác động đến distribution.

---

## 4.2.2. Log Transformation

Log Transformation là phép biến đổi đơn giản nhưng hiệu quả đối với dữ liệu có phân bố lệch phải hoặc heavy-tailed.

Dạng tổng quát:

$$x'_i=\log_a(x_i)$$

Trong đó $a$ là cơ số logarithm.

Ý tưởng chính là **nén các giá trị lớn và mở rộng tương đối các giá trị nhỏ**. Vì vậy, nếu một chuỗi có một số lượng nhỏ quan sát có magnitude rất lớn trong khi phần lớn quan sát tập trung ở vùng giá trị thấp, logarithmic transformation có thể làm giảm sự thống trị của các giá trị lớn.

Theo khảo sát, Log Scaling đặc biệt phù hợp với dữ liệu có **power-law distribution**. Phép biến đổi logarithm có thể làm cho dạng phân bố lệch trở nên gần Gaussian hơn.

Có thể minh họa tác động của phép biến đổi:

```text
Original distribution

Frequency
  │ ███████████████
  │ █████████
  │ ████
  │ ██
  │ █
  └──────────────────────→ x
       small        large


Log transformation

Frequency
  │      █████████
  │    ███████████
  │   ███████████
  │    █████████
  │      ███
  └──────────────────────→ log(x)
```

Log Transformation do đó phù hợp khi vấn đề cần giải quyết là **distributional skewness hoặc heavy tail**, thay vì chỉ khác biệt về scale giữa các feature.

### Điều kiện áp dụng

Trong khảo sát, Log Scaling được xem xét cho các giá trị không âm. Vì logarithm không xác định tại $x=0$, dữ liệu chứa zero hoặc giá trị âm cần được xử lý trước khi áp dụng phép biến đổi.

### Kết quả thực nghiệm

Trên bộ dữ liệu AirQuality, Log Scaling đạt:

| Metric | Kết quả |
| ------ | ------: |
| RMSE   |    0.52 |
| MAE    |    0.36 |
| MAPE   |  33.77% |

Kết quả này thấp hơn Z-score và Robust Standardization trong cùng thực nghiệm. Điều này cho thấy transformation thay đổi distribution không đồng nghĩa với việc luôn cải thiện prediction accuracy.

---

## 4.2.3. Box-Cox Transformation

Box-Cox là một **power transformation** tổng quát hóa Log Transformation. Phép biến đổi được định nghĩa bởi:

$$x'_i=
\begin{cases}
\frac{x_i^\lambda-1}{\lambda}, & \lambda\neq0\
\ln(x_i), & \lambda=0
\end{cases}$$

Trong đó $\lambda$ là tham số điều khiển dạng của phép biến đổi.

Khi:

$$\lambda=0$$

Box-Cox trở thành logarithmic transformation.

Điểm quan trọng của Box-Cox là $\lambda$ không nhất thiết phải được chọn thủ công. Theo khảo sát, tham số này có thể được xác định bằng **maximum likelihood**, **goodness-of-fit** hoặc các phương pháp Bayesian.

---

## 4.2.4. Mục tiêu của Box-Cox

Box-Cox được sử dụng khi dữ liệu có phân bố lệch và cần một phép biến đổi linh hoạt hơn Log Transformation.

Hai mục tiêu chính là:

### 1. Làm phân bố gần Gaussian hơn

Nếu $X$ có phân bố lệch:

$$X\sim\text{Skewed Distribution}$$

ta tìm $\lambda$ sao cho:

$$X'=g(X;\lambda)$$

có phân bố gần Gaussian hơn.

### 2. Ổn định phương sai

Trong chuỗi thời gian, variance có thể thay đổi theo magnitude của signal. Box-Cox có thể được sử dụng để làm giảm sự phụ thuộc này và tạo ra một distribution có variance ổn định hơn.

Bài khảo sát mô tả Box-Cox là phép biến đổi tạo ra phân bố gần Gaussian hơn và **stabilize variances**. Power transformation cũng có thể cải thiện tính hợp lệ của một số association measures, chẳng hạn Pearson Correlation.

---

## 4.2.5. Box-Cox và Log Transformation

Hai phương pháp có quan hệ trực tiếp:

```text
                 Data Transformation
                         │
                Power Transformation
                         │
                  ┌──────┴──────┐
                  │             │
             Box-Cox        λ = 0
                  │             │
                  │        Log Transform
                  │
          λ ≠ 0 → Power Transform
```

Vì vậy:

$$\boxed{\text{Log Transformation} \subset \text{Box-Cox family}}$$

theo cách biểu diễn của khảo sát, với trường hợp đặc biệt $\lambda=0$.

Sự khác biệt chính là Log Transformation sử dụng một dạng cố định, trong khi Box-Cox cho phép lựa chọn $\lambda$ để tìm dạng biến đổi phù hợp hơn với dữ liệu.

---

## 4.2.6. Điều kiện dữ liệu

Một hạn chế quan trọng của Box-Cox là yêu cầu dữ liệu dương. Bài khảo sát chỉ ra rằng Box-Cox, tương tự Log Scaling, được áp dụng cho **positive values**.

Do đó:

$$x_i>0$$

là điều kiện cần trong cách sử dụng được trình bày trong khảo sát.

Nếu dữ liệu có:

$$x_i\leq0$$

thì không thể áp dụng trực tiếp Box-Cox theo dạng trên. Vì vậy, kiểm tra miền giá trị phải được thực hiện trước transformation.

---

## 4.2.7. Kết quả thực nghiệm

Trong thực nghiệm AirQuality, Box-Cox đạt:

| Metric | Kết quả |
| ------ | ------: |
| RMSE   |    0.48 |
| MAE    |    0.31 |
| MAPE   |  28.55% |

Box-Cox đạt kết quả tốt hơn Log Scaling trong cùng thiết lập:

$$RMSE_{Box-Cox}<RMSE_{Log}$$

và:

$$MAE_{Box-Cox}<MAE_{Log}$$

Điều này phù hợp với đặc điểm của Box-Cox: thay vì cố định transformation ở logarithm, $\lambda$ được lựa chọn để thích nghi với distribution của dữ liệu.

Tuy nhiên, Z-score và Robust Standardization vẫn đạt kết quả tốt hơn trong thực nghiệm này. Vì vậy, không thể kết luận rằng Box-Cox luôn vượt trội hơn scaling hoặc standardization. Kết quả phụ thuộc vào distribution và đặc điểm của dataset.

---

## 4.2.8. Transformation kết hợp với Scaling

Scaling và transformation không phải hai thao tác loại trừ nhau. Chúng có thể được áp dụng tuần tự khi mỗi bước giải quyết một vấn đề khác nhau.

Ví dụ:

```text
Raw Data
   │
   ▼
Box-Cox Transformation
   │
   │  Điều chỉnh distribution
   ▼
Transformed Data
   │
   ▼
Z-score Standardization
   │
   │  Điều chỉnh scale
   ▼
Model-ready Data
```

Về mặt toán học:

$$x'_i=T(x_i;\lambda)$$

sau đó:

$$x''_i=\frac{x'_i-\mu_T}{\sigma_T}$$

Trong đó $T$ là transformation, còn $\mu_T$ và $\sigma_T$ được tính trên dữ liệu sau transformation.

Bài khảo sát cũng nêu trực tiếp khả năng kết hợp nhiều normalization/transformation tuần tự, chẳng hạn **Box-Cox để thay đổi distribution** rồi **Z-score để thay đổi scale**.

Điều này tạo sự liên kết trực tiếp với mục `01_scaling_normalization.md`: transformation giải quyết **hình dạng phân bố**, trong khi scaling giải quyết **thang đo**.

---

## 4.2.9. Transformation và thứ tự trong preprocessing pipeline

Các bước preprocessing không nên được xem là những thao tác độc lập. Thứ tự giữa chúng có thể ảnh hưởng đến kết quả.

Bài khảo sát nhấn mạnh rằng preprocessing có các dependency giữa các category. Ví dụ, outlier detection có thể được thực hiện trước normalization để tránh việc outlier làm sai lệch mean và variance dùng cho normalization. Tương tự, một số phương pháp imputation có thể yêu cầu normalization trước nếu chúng nhạy cảm với scale.

Vì vậy, transformation phải được đặt trong **preprocessing pipeline**, thay vì áp dụng một cách độc lập.

Một pipeline khái quát:

```text
Raw Time-Series
      │
      ▼
Data Cleaning
      │
      ├── Missing Data
      │
      ├── Outlier Detection
      │
      └── Noise Handling
      │
      ▼
Transformation
      │
      ├── Log
      │
      └── Box-Cox
      │
      ▼
Scaling / Normalization
      │
      ├── Z-score
      ├── Robust
      └── Min-Max
      │
      ▼
Stationarity Analysis
      │
      ▼
Decomposition
      │
      ▼
Feature Engineering
```

Pipeline thực tế không nhất thiết phải tuân theo đúng thứ tự trên cho mọi dataset. Bài khảo sát nhấn mạnh rằng sequence, parameters và vị trí thực hiện preprocessing phụ thuộc vào loại dữ liệu, nguồn dữ liệu, ứng dụng và thuật toán tiêu thụ dữ liệu.

Do đó, các mục tiếp theo của chương sẽ tiếp tục xem xét những đặc điểm đặc thù của time series thay vì coi transformation là bước độc lập.

---

## 4.2.10. Transformation trong dữ liệu chuỗi thời gian

Transformation đặc biệt có ý nghĩa khi các đặc tính thống kê của chuỗi gây khó khăn cho mô hình.

Có thể phân biệt:

| Vấn đề                                      | Phương pháp phù hợp                   |
| ------------------------------------------- | ------------------------------------- |
| Feature có magnitude khác nhau              | Scaling / Normalization               |
| Phân bố lệch phải                           | Log Transformation                    |
| Heavy-tailed / Power-law                    | Log Transformation                    |
| Skewed distribution                         | Box-Cox                               |
| Variance không ổn định                      | Box-Cox                               |
| Nhiều outlier                               | Robust Standardization                |
| Dữ liệu có đặc tính thay đổi theo thời gian | Adaptive / window-based normalization |

Điểm cần phân biệt là **transformation không phải phương pháp xử lý mọi vấn đề của time series**. Đặc biệt, transformation không trực tiếp giải quyết temporal dependence hoặc non-stationarity. Khảo sát xem việc xử lý non-stationarity như một hướng preprocessing riêng và xác định đây là một hướng cần được nghiên cứu thêm.

Đây là lý do mục `03_stationarity.md` được đặt ngay sau transformation trong cấu trúc chương này.

---

## 4.2.11. Đánh giá transformation

Một transformation không nên được đánh giá chỉ dựa trên việc distribution nhìn "đẹp" hơn. Bài khảo sát đánh giá preprocessing theo hai khía cạnh:

1. **Input Quality** — transformation thay đổi đặc điểm của dữ liệu như thế nào.
2. **Output Quality** — dữ liệu sau preprocessing ảnh hưởng như thế nào đến prediction model.

Trong thực nghiệm, tác giả sử dụng LSTM để đánh giá ảnh hưởng của preprocessing đến prediction accuracy. Điều này quan trọng vì một transformation có thể làm distribution gần Gaussian hơn nhưng không nhất thiết tạo ra prediction tốt hơn.

Do đó, tiêu chí đánh giá cần bao gồm:

$$\text{Transformation Quality}
\neq
\text{Distribution Quality only}$$

mà cần xem xét:

$$\text{Transformation Quality}
\rightarrow
\text{Input Quality}
\rightarrow
\text{Model Performance}
$$

---

## 4.2.12. Kết luận của mục

Transformation mở rộng mục tiêu của scaling và normalization từ **điều chỉnh scale** sang **điều chỉnh distribution và variance**.

Hai kỹ thuật tiêu biểu trong khảo sát là:

* **Log Transformation**: phù hợp với dữ liệu power-law hoặc heavy-tailed; nén các giá trị lớn và mở rộng tương đối các giá trị nhỏ.
* **Box-Cox Transformation**: tổng quát hóa Log Transformation bằng tham số $\lambda$, hướng tới phân bố gần Gaussian hơn và ổn định variance.

Trong thực nghiệm AirQuality, Box-Cox đạt RMSE $0.48$, MAE $0.31$ và MAPE $28.55%$, tốt hơn Log Scaling với RMSE $0.52$, MAE $0.36$ và MAPE $33.77%$. Tuy nhiên, Z-score và Robust Standardization vẫn đạt kết quả tốt hơn trong cùng thiết lập.

Vì vậy, nguyên tắc lựa chọn không phải là tìm một transformation "tốt nhất", mà là xác định **vấn đề thống kê cần giải quyết** trước khi lựa chọn phép biến đổi.

Mục tiếp theo, **`03_stationarity.md`**, sẽ chuyển từ vấn đề *phân bố của giá trị* sang vấn đề đặc trưng thống kê **thay đổi theo thời gian**. Đây là bước quan trọng đối với time-series preprocessing, bởi một chuỗi có thể đã được transformation và scaling nhưng vẫn chưa đạt tính ổn định cần thiết cho các phương pháp phân tích và mô hình hóa tiếp theo.
