# 4.1. Scaling và Normalization

## 4.1.1. Vai trò trong tiền xử lý dữ liệu chuỗi thời gian

Trong dữ liệu chuỗi thời gian số, các biến thường có đơn vị, miền giá trị và độ lớn rất khác nhau. Ví dụ, nhiệt độ, độ ẩm và nồng độ khí có thể cùng xuất hiện trong một tập dữ liệu cảm biến nhưng có thang đo hoàn toàn khác nhau. Nếu đưa trực tiếp các biến này vào thuật toán học máy, những đặc trưng có độ lớn lớn hơn có thể chi phối khoảng cách, hướng biến thiên hoặc quá trình tối ưu của mô hình.

Tawakuli et al. xem normalization là một bước tiền xử lý nhằm đưa các đặc trưng số về các thang đo tương đồng, qua đó giảm ảnh hưởng không mong muốn của sự khác biệt về magnitude giữa các đặc trưng. Điều này đặc biệt quan trọng đối với các thuật toán dựa trên khoảng cách như KNN, K-means và SVM; đồng thời có thể cải thiện quá trình hội tụ của gradient descent trong hồi quy tuyến tính, logistic regression và mạng neural. Đối với PCA, scaling còn ngăn các đặc trưng có phạm vi lớn chi phối hướng phương sai lớn nhất.

Với chuỗi thời gian, scaling không làm mất thứ tự thời gian. Nó chỉ biến đổi giá trị quan sát theo một hàm xác định:

$$x'_t = f(x_t;\theta)$$

trong đó $x_t$ là giá trị tại thời điểm $t$, $f$ là phép biến đổi và $\theta$ là các tham số được ước lượng từ dữ liệu.

Điểm quan trọng là các tham số của phép scaling được xác định trong quá trình huấn luyện và sau đó được giữ cố định để biến đổi dữ liệu validation, test hoặc dữ liệu mới. Bài khảo sát nhấn mạnh rằng các tham số như mean và standard deviation của Z-score được lấy trong quá trình training và sử dụng lại cho testing và vận hành trên dữ liệu mới.

---

## 4.1.2. Min-Max Scaling

Min-Max Scaling đưa giá trị của một đặc trưng về một khoảng xác định, phổ biến nhất là $[0,1]$:

$$x'_i = \frac{x_i-\min(X)}{\max(X)-\min(X)}$$

Trong đó $\min(X)$ và $\max(X)$ là giá trị nhỏ nhất và lớn nhất của đặc trưng.

Phương pháp này phù hợp khi:

* Biết hoặc có thể ước lượng đáng tin cậy giới hạn dưới và giới hạn trên.
* Dữ liệu có ít hoặc không có outlier.
* Phân bố dữ liệu tương đối trải đều trong khoảng giá trị.

Theo khảo sát, Min-Max tạo cùng một miền $[0,1]$ cho các đặc trưng sau khi biến đổi. Tuy nhiên, vì sử dụng trực tiếp minimum và maximum, các giá trị cực trị có thể ảnh hưởng đáng kể đến toàn bộ phép biến đổi.

Trong thực nghiệm trên AirQuality, Min-Max đạt:

| Metric | Kết quả |
| ------ | ------: |
| RMSE   |    0.46 |
| MAE    |    0.29 |
| MAPE   |  30.46% |

---

## 4.1.3. Z-score Standardization

Z-score Standardization biến đổi dữ liệu dựa trên trung bình và độ lệch chuẩn:

$$x'_i = \frac{x_i-\mu}{\sigma}$$

với $\mu$ là mean và $\sigma$ là standard deviation của đặc trưng.

Sau biến đổi, dữ liệu có:

$$\mathbb{E}[X'] \approx 0,\qquad Var(X') \approx 1$$

Phương pháp này đặc biệt phù hợp với dữ liệu có phân bố gần Gaussian và không chứa quá nhiều extreme outliers. Z-score cũng phù hợp với các mô hình giả định đầu vào có phân bố Gaussian, chẳng hạn linear regression và logistic regression.

Trong các kỹ thuật được thử nghiệm, Z-score cho kết quả tốt nhất trên bộ dữ liệu AirQuality:

| Metric | Kết quả |
| ------ | ------: |
| RMSE   |    0.35 |
| MAE    |    0.25 |
| MAPE   |  27.26% |

So với dữ liệu không normalization, thực nghiệm báo cáo mức cải thiện khoảng $49%$ đối với RMSE, $56%$ đối với MAE và $54%$ đối với MAPE khi sử dụng Z-score.

---

## 4.1.4. Robust Standardization

Khi dữ liệu chứa nhiều outlier, mean và standard deviation có thể bị ảnh hưởng mạnh. Robust Standardization thay thế chúng bằng median và interquartile range:

$$x'*i = \frac{x_i-\operatorname{median}(X)}{Q*{75}-Q_{25}}$$

trong đó:

$$IQR = Q_{75}-Q_{25}$$

Median và IQR ít nhạy cảm với extreme values hơn mean và standard deviation. Vì vậy, phương pháp này thích hợp khi dữ liệu chuỗi thời gian có nhiều outlier nhưng vẫn cần duy trì phần lớn quan sát.

Trong thực nghiệm:

| Metric | Kết quả |
| ------ | ------: |
| RMSE   |    0.38 |
| MAE    |    0.25 |
| MAPE   |  27.57% |

Kết quả cho thấy Robust Standardization có hiệu quả gần với Z-score và thuộc nhóm các phương pháp tạo ra mô hình LSTM có độ chính xác cao nhất trong thực nghiệm.

---

## 4.1.5. P-Norm Normalization

P-Norm chuẩn hóa một phần tử dựa trên độ lớn của vector:

$$x'*i = \frac{x_i}{\left(\sum*{k=1}^{N}|x_k|^p\right)^{1/p}}$$

Hai trường hợp thường gặp tương ứng với:

* $p=1$: L1 norm.
* $p=2$: L2 norm.

Theo khảo sát, P-Norm có khả năng dung nạp outlier nhưng trong thực nghiệm trên AirQuality cho kết quả thấp hơn đáng kể so với Z-score và Robust Standardization:

| Metric | Kết quả |
| ------ | ------: |
| RMSE   |    0.57 |
| MAE    |    0.46 |
| MAPE   |  49.75% |

Do đó, việc một phương pháp có đặc tính robust về mặt công thức không đồng nghĩa với việc nó luôn tạo ra hiệu năng dự báo tốt nhất trên một chuỗi thời gian cụ thể.

---

## 4.1.6. Decimal Scaling

Decimal Scaling giảm độ lớn của giá trị bằng cách dịch dấu thập phân:

$$x'_i = \frac{x_i}{10^k}$$

với $k$ được lựa chọn dựa trên giá trị tuyệt đối lớn nhất của dữ liệu.

Phương pháp này giữ lại cấu trúc giá trị ban đầu nhưng đưa chúng về miền có độ lớn nhỏ hơn. Bài khảo sát cho biết Decimal Scaling có thể đưa scale về khoảng $[-1,1]$ tùy theo cách lựa chọn $k$.

Kết quả thực nghiệm:

| Metric | Kết quả |
| ------ | ------: |
| RMSE   |    0.45 |
| MAE    |    0.30 |
| MAPE   |  32.42% |

---

## 4.1.7. Log Scaling

Log Scaling không chỉ thay đổi scale mà còn thay đổi hình dạng phân bố:

$$x'_i = \log_a(x_i)$$

Phương pháp đặc biệt hữu ích với dữ liệu có phân bố power-law hoặc heavy-tailed, trong đó một số giá trị lớn chiếm ưu thế trong khi phần lớn quan sát có giá trị nhỏ.

Logarithm nén các giá trị lớn và mở rộng tương đối các giá trị nhỏ, từ đó làm giảm độ lệch của phân bố và có thể đưa phân bố gần hơn với Gaussian. Phương pháp này yêu cầu dữ liệu đầu vào không âm theo cách trình bày trong khảo sát.

Kết quả thực nghiệm:

| Metric | Kết quả |
| ------ | ------: |
| RMSE   |    0.52 |
| MAE    |    0.36 |
| MAPE   |  33.77% |

---

## 4.1.8. Box-Cox Transformation

Box-Cox là một power transformation tổng quát hơn Log Scaling:

$$x'_i =
\begin{cases}
\frac{x_i^\lambda-1}{\lambda}, & \lambda \neq 0\
\ln(x_i), & \lambda = 0
\end{cases}$$

Tham số $\lambda$ có thể được lựa chọn dựa trên maximum likelihood, goodness-of-fit hoặc phương pháp Bayesian. Khi $\lambda=0$, phép biến đổi trở thành logarithmic transformation.

Mục tiêu chính của Box-Cox không đơn thuần là đưa các feature về cùng scale mà còn làm phân bố gần Gaussian hơn và ổn định phương sai. Vì vậy, Box-Cox thuộc nhóm phép biến đổi vừa tác động đến distribution vừa tác động đến scale.

Trong thực nghiệm:

| Metric | Kết quả |
| ------ | ------: |
| RMSE   |    0.48 |
| MAE    |    0.31 |
| MAPE   |  28.55% |

---

## 4.1.9. So sánh các phương pháp

Bảy phương pháp được khảo sát có thể phân biệt theo mục tiêu chính:

| Phương pháp            | Mục tiêu chính                    | Đặc điểm dữ liệu             |
| ---------------------- | --------------------------------- | ---------------------------- |
| Min-Max                | Đưa về cùng khoảng                | Biết giới hạn, ít outlier    |
| Z-score                | Chuẩn hóa theo mean/std           | Ít extreme outlier           |
| Robust Standardization | Chuẩn hóa robust                  | Nhiều outlier                |
| P-Norm                 | Chuẩn hóa theo vector magnitude   | Có khả năng chịu outlier     |
| Decimal Scaling        | Giảm độ lớn                       | Biết maximum                 |
| Log Scaling            | Nén heavy tail                    | Power-law, non-negative      |
| Box-Cox                | Biến đổi distribution và variance | Skewed/Poisson, non-negative |

Kết quả thực nghiệm cho thấy không tồn tại một phương pháp scaling tối ưu cho mọi dữ liệu. Trên AirQuality, Z-score và Robust Standardization tạo ra các mô hình LSTM có độ chính xác cao nhất, trong khi Min-Max và Decimal Scaling đạt kết quả trung gian; P-Norm và Log Scaling cho kết quả kém hơn trong cấu hình thí nghiệm này.

Do đó, lựa chọn scaling cần dựa trên đặc điểm phân bố, outlier, miền giá trị và yêu cầu của thuật toán thay vì lựa chọn một phương pháp cố định cho mọi bài toán.

---

## 4.1.10. Scaling trong chuỗi thời gian và dữ liệu streaming

Đối với dữ liệu chuỗi thời gian, một vấn đề quan trọng là các đặc tính thống kê có thể thay đổi theo thời gian. Dữ liệu streaming có thể xuất hiện volatility và seasonality khiến các thống kê cố định không còn đại diện tốt cho dữ liệu hiện tại.

Bài khảo sát đề cập đến **adaptive normalization**, trong đó các thống kê được tính trên các sliding window có kích thước cố định:

$$\theta_t = g(X_{t-w+1:t})$$

và phép normalization tại thời điểm $t$ sử dụng các thống kê của cửa sổ hiện tại thay vì toàn bộ lịch sử.

Cách tiếp cận này cho phép phép chuẩn hóa thích ứng với sự thay đổi của phân bố theo thời gian. Tuy nhiên, trong hệ thống dự báo chuỗi thời gian, việc cập nhật thống kê phải được kiểm soát để tránh sử dụng thông tin tương lai.

Một ưu điểm quan trọng khác là nhiều normalization techniques có thể đảo ngược nếu các statistical parameters được lưu trữ. Do đó, dữ liệu sau dự báo có thể được đưa trở lại scale ban đầu khi cần thiết.

---

## 4.1.11. Scaling và triển khai tại Edge

Normalization có chi phí tính toán tương đối thấp. Theo khảo sát, các phép normalization chủ yếu cần duyệt qua các phần tử của window và không yêu cầu recursion hoặc các phép toán ma trận phức tạp. Vì vậy, chúng có khả năng triển khai trên các thiết bị edge có tài nguyên hạn chế như smart sensors hoặc Raspberry Pi.

Một kiến trúc triển khai có thể được mô tả:

```text
Raw Sensor Data
       ↓
Training Data
       ↓
Estimate Scaling Parameters
       ↓
Store Parameters
       ↓
┌─────────────────────────┐
│ Edge / Sensor           │
│                         │
│ x_t → Scaling(x_t, θ)   │
└─────────────────────────┘
       ↓
AI Model
       ↓
Prediction
       ↓
Inverse Scaling
       ↓
Original Physical Unit
```

Điểm cốt lõi là tham số scaling phải nhất quán giữa training và inference. Ví dụ, nếu training sử dụng $\mu_{train}$ và $\sigma_{train}$ thì dữ liệu mới phải được biến đổi bằng chính hai tham số này:

$$x'*{new}=\frac{x*{new}-\mu_{train}}{\sigma_{train}}$$

không được tự động tính lại $\mu$ và $\sigma$ từ validation, test hoặc từng sample mới.

---

## 4.1.12. Kết luận của mục

Scaling và normalization không làm thay đổi bản chất của chuỗi thời gian mà điều chỉnh representation của các giá trị để mô hình có thể học ổn định hơn. Tác động của chúng thể hiện ở ba khía cạnh chính:

1. **Cân bằng influence giữa các feature** có scale khác nhau.
2. **Cải thiện quá trình tối ưu**, đặc biệt với các mô hình sử dụng gradient descent.
3. **Điều chỉnh distribution**, trong trường hợp các phép biến đổi như Log Scaling và Box-Cox.

Kết quả của khảo sát cho thấy Z-score và Robust Standardization là hai lựa chọn nổi bật trong thực nghiệm LSTM trên AirQuality, nhưng kết quả này không nên được xem là quy tắc phổ quát. Việc lựa chọn phương pháp phải dựa trên đặc điểm thống kê của từng chuỗi thời gian và phải sử dụng các tham số được ước lượng từ dữ liệu huấn luyện.

Nội dung này tạo cơ sở cho mục tiếp theo của Chương 4, **`02_transformation.md`**: scaling chủ yếu điều chỉnh **scale**, trong khi transformation tập trung sâu hơn vào **hình dạng phân bố, skewness và variance** của dữ liệu trước khi đưa vào các bước xử lý tiếp theo.
