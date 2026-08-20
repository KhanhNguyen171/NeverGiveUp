# 01. Missing Data

## 1. Tổng quan

**Missing Data** là một trong những vấn đề phổ biến nhất khi xử lý Time-Series Data. Trong dữ liệu thực tế, một số giá trị tại thời điểm $t$ có thể không được ghi nhận do:

* Sensor bị lỗi hoặc mất kết nối.
* Hệ thống thu thập dữ liệu bị gián đoạn.
* Lỗi truyền dữ liệu.
* Database bị thiếu bản ghi.
* Sampling không đều.
* Dữ liệu bị loại bỏ trong quá trình lưu trữ hoặc preprocessing.

Ví dụ:

```text
Time     Temperature
10:00       25.1
10:10       25.4
10:20        NaN
10:30       25.8
10:40       26.0
```

Giá trị tại $10{:}20$ bị thiếu tạo ra một **gap trong chuỗi thời gian**.

Vấn đề quan trọng không chỉ là tìm cách điền giá trị còn thiếu, mà phải xác định:

> **Tại sao giá trị bị thiếu, thiếu ở đâu, thiếu bao nhiêu và việc thay thế giá trị đó có làm thay đổi cấu trúc thời gian của dữ liệu hay không?**

### Đối chiếu với bài báo

Survey phân biệt `isolated missing instances` (điểm thiếu đơn lẻ) và `sequence missing instances` (đoạn thiếu liên tiếp). Trong empirical analysis, tác giả dùng cubic spline interpolation cho điểm thiếu đơn lẻ và Expectation Maximization (EM) cho đoạn thiếu; đây là lựa chọn của thiết kế thực nghiệm, không phải quy tắc tối ưu cho mọi dataset.

---

## 2. Missing Data trong Time Series

Với một time series:

$$X={x_1,x_2,\ldots,x_T}$$

một tập con các quan sát có thể không tồn tại:

$$X_{obs} \subset X$$

và:

$$X_{miss}=X-X_{obs}$$

Mục tiêu của Missing Data Imputation là ước lượng:

$$\hat{x}_t$$

cho các thời điểm:

$$t\in X_{miss}$$

sao cho:

$$\hat{x}_t \approx x_t$$

nếu giá trị thực sự tồn tại nhưng không được quan sát.

Có thể biểu diễn quá trình:

```text
Observed Time Series
        │
        ▼
Detect Missing Values
        │
        ▼
Analyze Missing Pattern
        │
        ▼
Select Imputation Method
        │
        ▼
Estimate Missing Values
        │
        ▼
Complete Time Series
```

---

# 3. Các dạng Missing Data

Một điểm quan trọng khi xử lý Missing Data là **không phải mọi missing pattern đều giống nhau**.

## 3.1. Missing Completely at Random — MCAR

Giá trị bị thiếu hoàn toàn ngẫu nhiên và việc missing không phụ thuộc vào dữ liệu quan sát hay không quan sát.

Ví dụ:

```text
Sensor hoạt động bình thường
        ↓
Một vài packet bị mất ngẫu nhiên
        ↓
Missing
```

Trong trường hợp này, missing pattern không liên quan đến giá trị của time series.

---

## 3.2. Missing at Random — MAR

Xác suất missing phụ thuộc vào những biến đã quan sát.

Ví dụ:

```text
Humidity cao
     ↓
Sensor dễ mất kết nối
     ↓
Temperature bị missing
```

Missing của `Temperature` phụ thuộc vào `Humidity`, trong khi `Humidity` vẫn được quan sát.

---

## 3.3. Missing Not at Random — MNAR

Xác suất missing phụ thuộc trực tiếp vào chính giá trị bị thiếu.

Ví dụ:

```text
Temperature quá cao
        ↓
Sensor quá nhiệt
        ↓
Sensor ngừng ghi dữ liệu
        ↓
Temperature bị missing
```

Trong trường hợp này, missing không còn ngẫu nhiên.

Đây là trường hợp khó xử lý nhất vì dữ liệu bị thiếu có thể chứa chính thông tin mà chúng ta cần dự đoán.

---

# 4. Missing Pattern trong Time Series

Ngoài cơ chế missing, cần xem xét **vị trí của missing values theo thời gian**.

### Missing đơn lẻ

```text
10  11  12  ?  14  15
```

Một điểm bị thiếu.

### Consecutive Missing

```text
10  11  ?  ?  ?  15
```

Một đoạn liên tục bị thiếu.

### Block Missing

```text
████████████
     GAP
████████████
```

Một khoảng thời gian dài hoàn toàn không có dữ liệu.

### Irregular Missing

```text
10  ?  12  ?  ?  15  16  ?  18
```

Các missing values xuất hiện không theo quy luật rõ ràng.

**Pattern của missing ảnh hưởng trực tiếp đến phương pháp imputation phù hợp.**

---

# 5. Deletion

Phương pháp đơn giản nhất là loại bỏ các observation chứa missing values.

Ví dụ:

```text
Original:

10:00   20
10:10   21
10:20   NaN
10:30   23
10:40   24
```

Sau deletion:

```text
10:00   20
10:10   21
10:30   23
10:40   24
```

Ưu điểm:

* đơn giản;
* không tạo ra giá trị giả;
* dễ triển khai.

Nhược điểm:

* mất dữ liệu;
* phá vỡ temporal continuity;
* có thể làm thay đổi distribution;
* đặc biệt nguy hiểm khi missing rate cao.

Do đó deletion thường chỉ phù hợp khi lượng missing rất nhỏ và việc loại bỏ observation không ảnh hưởng đáng kể đến cấu trúc time series.

---

# 6. Mean / Median Imputation

Có thể thay missing value bằng thống kê của dữ liệu.

### Mean

$$\hat{x}_t=\mu$$

với:

$$\mu=
\frac{1}{N}
\sum_{i=1}^{N}x_i$$

Ví dụ:

```text
10  12  ?  14  16
```

Mean:

$$\mu=13$$

suy ra:

```text
10  12  13  14  16
```

### Median

$$\hat{x}_t=\operatorname{median}(X)$$

Median thường robust hơn mean khi dữ liệu có outlier.

### Vấn đề

Phương pháp này **không sử dụng temporal dependency**.

Ví dụ:

```text
10:00   10
10:10   11
10:20   ?
10:30   30
```

Mean toàn bộ series có thể hoàn toàn không phản ánh giá trị hợp lý tại $10{:}20$.

Vì vậy mean/median thường phù hợp hơn với dữ liệu đơn giản hoặc baseline, thay vì các time series có dynamics mạnh.

---

# 7. Forward Fill

Forward Fill sử dụng giá trị quan sát gần nhất trước đó:

$$\hat{x}_t=x_{t-1}$$

Ví dụ:

```text
10
11
?
?
14
```

sẽ trở thành:

```text
10
11
11
11
14
```

Ưu điểm:

* đơn giản;
* giữ temporal ordering;
* phù hợp với dữ liệu có trạng thái thay đổi chậm.

Nhược điểm:

* tạo ra đoạn dữ liệu phẳng;
* không phù hợp khi signal biến động nhanh;
* có thể kéo dài một giá trị cũ quá lâu.

---

# 8. Backward Fill

Ngược lại, Backward Fill sử dụng observation tiếp theo:

$$\hat{x}_t=x_{t+1}$$

Ví dụ:

```text
10
11
?
?
14
```

trở thành:

```text
10
11
14
14
14
```

Phương pháp này đơn giản nhưng cần cẩn thận trong **forecasting**, bởi việc sử dụng giá trị tương lai để điền dữ liệu quá khứ có thể tạo ra **future information leakage** tùy vị trí preprocessing.

---

# 9. Linear Interpolation

Đây là một phương pháp tự nhiên hơn đối với time series có biến động tương đối liên tục.

Giả sử:

$$x_{t_1}=10$$

và:

$$x_{t_2}=20$$

Giá trị tại $t$ nằm giữa hai điểm được tính:

$$\hat{x}_t=x_{t_1}
+
\frac{t-t_1}{t_2-t_1}
(x_{t_2}-x_{t_1})$$

Ví dụ:

```text
10:00   10
10:10    ?
10:20   20
```

thì:

```text
10:10   15
```

### Ưu điểm

* đơn giản;
* tận dụng temporal information;
* phù hợp với signal thay đổi tương đối liên tục.

### Hạn chế

Linear interpolation giả định:

$$x(t)\approx at+b$$

trong khoảng missing.

Nếu signal có peak hoặc biến động phi tuyến mạnh, kết quả có thể không chính xác.

---

# 10. Polynomial Interpolation

Thay vì giả định đường thẳng, có thể dùng polynomial:

$$\hat{x}(t)=
a_0+a_1t+a_2t^2+\cdots+a_nt^n$$

Điều này cho phép mô hình hóa các biến động phi tuyến.

Tuy nhiên polynomial bậc cao có thể gây:

* overfitting;
* oscillation;
* unstable interpolation.

Vì vậy không nên mặc định rằng polynomial bậc cao sẽ tốt hơn linear interpolation.

---

# 11. Spline Interpolation

Spline chia dữ liệu thành các đoạn polynomial nhỏ.

Một cubic spline có dạng:

$$S_i(t)=

a_i+b_i(t-t_i)
+c_i(t-t_i)^2
+d_i(t-t_i)^3$$

Mục tiêu là tạo ra một đường cong **mượt** đi qua các observation.

So với polynomial toàn cục:

```text
Polynomial
    ↓
Một polynomial cho toàn bộ dữ liệu
```

Spline:

```text
Data
 ↓
Segment 1 → polynomial
Segment 2 → polynomial
Segment 3 → polynomial
        ↓
Smooth curve
```

Spline phù hợp với các signal liên tục và có smooth dynamics.

---

# 12. KNN Imputation

KNN không chỉ nhìn vào temporal neighbor mà tìm những observation **tương tự**.

Giả sử mỗi observation có vector:

$$x_i=[x_{i1},x_{i2},...,x_{id}]$$

KNN tìm (k) observation gần nhất:

$$N_k(x_i)$$

sau đó ước lượng:

$$\hat{x}_i=
\frac{1}{k}
\sum_{j\in N_k(x_i)}x_j$$

hoặc weighted average.

Ưu điểm:

* tận dụng similarity;
* có thể sử dụng nhiều feature;
* phù hợp multivariate time series.

Nhược điểm:

* computational cost cao;
* phụ thuộc distance metric;
* cần scaling phù hợp;
* không trực tiếp mô hình hóa temporal dynamics.

---

# 13. Regression-based Imputation

Có thể xem missing value như một bài toán prediction.

Ví dụ:

```text
Temperature
Humidity
Pressure
CO2
   │
   ▼
Regression Model
   │
   ▼
Missing Temperature
```

Ta xây dựng:

$$\hat{x}_t=f(x_t^{(1)},x_t^{(2)},...,x_t^{(d)})$$

Trong đó các feature khác được sử dụng để dự đoán giá trị bị thiếu.

Có thể sử dụng:

* Linear Regression;
* Random Forest;
* Gradient Boosting;
* Neural Network.

Ưu điểm là tận dụng **cross-variable dependency**.

---

# 14. Model-based Time-Series Imputation

Đây là hướng phù hợp hơn với dữ liệu có temporal dependency mạnh.

Có thể sử dụng:

```text
AR
ARIMA
Kalman Filter
State-Space Model
RNN
LSTM
GRU
Transformer
VAE
```

Ví dụ với autoregressive model:

$$x_t=
c+\sum_{i=1}^{p}\phi_i x_{t-i}+\epsilon_t$$

Nếu (x_t) bị missing, model sử dụng các observation trước đó để estimate:

$$\hat{x}_t=
c+\sum_{i=1}^{p}\phi_i x_{t-i}$$

Điểm mạnh của nhóm này là **mô hình hóa cấu trúc temporal**, thay vì chỉ dùng statistic đơn giản.

---

# 15. So sánh các phương pháp

| Method               | Temporal Dependency | Độ phức tạp | Ưu điểm                        | Hạn chế                            |
| -------------------- | ------------------: | ----------: | ------------------------------ | ---------------------------------- |
| Deletion             |               Không |        Thấp | Đơn giản                       | Mất dữ liệu                        |
| Mean                 |               Không |        Thấp | Dễ triển khai                  | Làm mất temporal structure         |
| Median               |               Không |        Thấp | Robust với outlier             | Không hiểu dynamics                |
| Forward Fill         |                  Có |        Thấp | Phù hợp state chậm             | Tạo đoạn phẳng                     |
| Backward Fill        |                  Có |        Thấp | Đơn giản                       | Có nguy cơ dùng future information |
| Linear Interpolation |                  Có |        Thấp | Tốt cho signal liên tục        | Giả định tuyến tính                |
| Polynomial           |                  Có |  Trung bình | Mô hình nonlinear              | Có thể unstable                    |
| Spline               |                  Có |  Trung bình | Smooth                         | Không phù hợp mọi signal           |
| KNN                  |           Gián tiếp |         Cao | Tận dụng similarity            | Tốn computation                    |
| Regression           |                  Có |  Trung bình | Dùng feature khác              | Phụ thuộc model                    |
| Time-Series Model    |                Mạnh |         Cao | Mô hình temporal dynamics      | Phức tạp                           |
| Deep Learning        |            Rất mạnh |     Rất cao | Có thể học dependency phức tạp | Cần nhiều dữ liệu                  |

---

# 16. Nguyên tắc lựa chọn

Không nên hỏi:

> **Phương pháp imputation nào tốt nhất?**

Mà nên hỏi:

> **Phương pháp nào phù hợp nhất với missing pattern và cấu trúc của time series?**

Có thể sử dụng quy tắc đơn giản:

```text
Missing rất ít
      ↓
Deletion / Interpolation

Missing ngắn + signal liên tục
      ↓
Linear / Spline Interpolation

State thay đổi chậm
      ↓
Forward Fill

Multivariate dependency mạnh
      ↓
KNN / Regression

Temporal dependency mạnh
      ↓
Time-Series Model

Missing dài / complex pattern
      ↓
Model-based / Deep Learning
```

---

# 17. Vấn đề quan trọng trong Forecasting

Trong time-series forecasting, imputation phải tuân thủ **temporal integrity**.

Ví dụ:

```text
Train                     Validation              Test
──────────────────┬──────────────────────┬────────────────
                  │                      │
                  │                      │
             preprocessing          preprocessing
```

Không được để quá trình imputation của Train sử dụng thông tin từ Validation hoặc Test.

Đặc biệt cần cẩn thận với:

```text
Backward Fill
Interpolation
Rolling Statistics
Model-based Imputation
```

vì các phương pháp này có thể vô tình sử dụng information từ tương lai.

Nguyên tắc:

$$\boxed{
\text{Information available at time }t
\rightarrow
\text{only information allowed to estimate }x_t
}$$

Đây là điểm rất quan trọng khi chuyển từ **survey preprocessing nói chung** sang **forecasting pipeline thực tế**.

---

# 18. Kết luận

Missing Data không đơn giản là vấn đề:

$$NaN \rightarrow value$$

mà là bài toán:

$$\boxed{
\text{Missing Pattern}
\rightarrow
\text{Temporal Structure}
\rightarrow
\text{Imputation Method}
\rightarrow
\text{Data Integrity}
}$$

Các phương pháp đơn giản như **Mean, Median, Forward Fill, Backward Fill** có chi phí thấp nhưng ít khai thác cấu trúc time series. **Interpolation** tận dụng temporal continuity, trong khi **KNN, Regression và Model-based Methods** có khả năng khai thác quan hệ giữa các biến và dependency theo thời gian mạnh hơn.

Quan trọng nhất, trong các bài toán forecasting, **imputation phải được thiết kế sao cho không đưa thông tin tương lai vào quá khứ**, nếu không preprocessing sẽ trở thành một nguồn **data leakage** và làm kết quả đánh giá không còn đáng tin cậy.
