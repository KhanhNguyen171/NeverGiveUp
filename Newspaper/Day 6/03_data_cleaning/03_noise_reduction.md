# 03. Noise Reduction

## 1. Tổng quan

Trong quá trình thu thập Time-Series Data, dữ liệu thường chứa các biến động không mong muốn do:

- Sensor noise
- Measurement error
- Communication error
- Environmental interference
- Hardware limitations
- Quantization error
- Data acquisition problems

Các biến động này có thể làm che khuất **underlying signal** mà chúng ta thực sự quan tâm.

Có thể biểu diễn một time series quan sát được:

$$
x_t=s_t+n_t
$$

trong đó:

- $x_t$: giá trị quan sát được;
- $s_t$: tín hiệu thực;
- $n_t$: noise.

Mục tiêu của Noise Reduction là ước lượng:

$$
\hat{s}_t \approx s_t
$$

từ dữ liệu quan sát $x_t$.

Quá trình tổng quát:

```text
Raw Time Series
       ↓
Observed Signal
       ↓
Noise Detection / Characterization
       ↓
Noise Reduction
       ↓
Estimated Clean Signal
       ↓
AI / Analytics
```

Survey xem preprocessing là quá trình biến raw data thành quality input data cho AI, trong đó data cleaning là một thành phần nhưng phạm vi preprocessing của bài báo còn mở rộng sang transformation, feature processing, sensor fusion và compression. ([research.chalmers.se][2])

Trong survey, noise reduction được đặt cạnh missing-data handling và outlier detection trong phạm vi preprocessing. Kết quả làm mượt cần được đánh giá theo cả mức giảm nhiễu và mức bảo toàn tín hiệu, không chỉ bằng cảm quan trên đồ thị.

---

# 2. Noise là gì?

Noise là thành phần không mong muốn xuất hiện trong dữ liệu đo.

Một mô hình đơn giản:

$$
x_t=s_t+n_t
$$

Nếu $s_t$ là tín hiệu thực và $n_t$ là noise, thì preprocessing cố gắng giảm ảnh hưởng của $n_t$ mà vẫn giữ lại thông tin quan trọng trong $s_t$.

Ví dụ:

```text
True Signal:

──────╮      ╭──────
      ╰──────╯

Observed Signal:

──╮─╲─╱╲──╮──╲──╱─
  ╰─╯    ╰──╯

          ↓

Noise Reduction

──────╮      ╭──────
      ╰──────╯
```

Tuy nhiên, vấn đề quan trọng là:

> Noise Reduction không phải là làm cho dữ liệu càng smooth càng tốt.

Nếu filtering quá mạnh, các đặc trưng thật của signal cũng có thể bị loại bỏ.

---

# 3. Noise khác Outlier như thế nào?

Noise và Outlier thường xuất hiện cùng nhau nhưng không phải cùng một vấn đề.

### Noise

Noise thường là các biến động nhỏ và xảy ra liên tục:

```text
10.1
9.9
10.2
9.8
10.1
10.0
```

### Outlier

Outlier thường là observation lệch mạnh:

```text
10
10.2
9.9
50
10.1
```

Có thể hình dung:

```text
Noise Reduction
      ↓
Giảm biến động ngẫu nhiên

Outlier Detection
      ↓
Tìm observation bất thường
```

Do đó hai bước có thể liên quan nhưng không nên đồng nhất:

$$
\boxed{
Noise \neq Outlier
}
$$

---

# 4. Vì sao cần Noise Reduction?

Noise có thể ảnh hưởng đến nhiều bước phía sau:

```text
Noise
  ↓
Distorted Signal
  ↓
Feature Extraction
  ↓
Model Training
  ↓
Prediction
```

Ví dụ một sensor đo nhiệt độ:

```text
True:

20  21  22  23  24

Observed:

20.2  20.7  22.5  22.8  24.3
```

Nếu noise lớn, model có thể học cả:

$$
s_t+n_t
$$

thay vì chỉ học:

$$
s_t
$$

Điều này có thể làm tăng model complexity và giảm khả năng tổng quát hóa.

---

# 5. Các hướng Noise Reduction

Noise reduction trong Time Series có thể được thực hiện bằng nhiều nhóm phương pháp:

```text
Noise Reduction
│
├── Statistical Smoothing
│   ├── Moving Average
│   ├── Weighted Moving Average
│   └── Exponential Smoothing
│
├── Filtering
│   ├── Median Filter
│   ├── Gaussian Filter
│   └── Savitzky-Golay Filter
│
├── Frequency-domain Methods
│   ├── Fourier Transform
│   ├── Low-pass Filter
│   └── Wavelet-based Methods
│
└── Model-based Methods
    ├── Kalman Filter
    ├── State-space Models
    └── Learning-based Denoising
```

Không phải tất cả phương pháp đều phù hợp cho mọi loại Time Series.

---

# 6. Moving Average

Moving Average là một trong những phương pháp đơn giản nhất.

Với window size $w$:

$$
\hat{x}_t=
\frac{1}{w}
\sum_{i=0}^{w-1}x_{t-i}
$$

Ví dụ với:

$$
w=3
$$

và:

```text
10  12  11  20  13
```

giá trị tại vị trí tiếp theo có thể được smooth bằng:

$$
\hat{x}_t=
\frac{10+12+11}{3}
=11
$$

Pipeline:

```text
Raw Signal
    ↓
Sliding Window
    ↓
Calculate Mean
    ↓
Smoothed Signal
```

### Ưu điểm

* đơn giản;
* computational cost thấp;
* dễ triển khai;
* phù hợp với streaming data.

### Nhược điểm

* làm mất peak;
* làm mờ sudden changes;
* tạo lag;
* phụ thuộc mạnh vào window size.

---

# 7. Window Size

Window size là một hyperparameter quan trọng.

### Window nhỏ

```text
w = 3
```

Giữ lại nhiều chi tiết:

```text
Signal
 ↓
Ít smoothing
 ↓
Nhiều noise còn lại
```

### Window lớn

```text
w = 20
```

Smoothing mạnh hơn:

```text
Signal
 ↓
Strong smoothing
 ↓
Có thể mất signal information
```

Do đó:

$$
\boxed{
\text{Larger Window}
\rightarrow
\text{More Smoothing}
\rightarrow
\text{More Information Loss}
}
$$

Không nên lựa chọn window size chỉ dựa trên việc signal nhìn “đẹp” hơn.

---

# 8. Weighted Moving Average

Thay vì cho mọi observation trọng số bằng nhau, Weighted Moving Average sử dụng:

$$
\hat{x}_t=
\sum_{i=0}^{w-1}w_i x_{t-i}
$$

với:

$$
\sum_i w_i=1
$$

Ví dụ:

$$
w=[0.2,0.3,0.5]
$$

Observation gần hiện tại có trọng số lớn hơn.

```text
Past ───────────→ Present

0.2      0.3       0.5
```

Điều này có thể phản ánh tốt hơn những series trong đó observation gần hiện tại có giá trị dự báo cao hơn.

---

# 9. Exponential Smoothing

Exponential Smoothing cũng gán trọng số lớn hơn cho các observation gần hiện tại.

Công thức cơ bản:

$$
s_t=
\alpha x_t+(1-\alpha)s_{t-1}
$$

với:

$$
0<\alpha<1
$$

Trong đó:

* $\alpha$ lớn → phản ứng nhanh với thay đổi;
* $\alpha$ nhỏ → smoothing mạnh hơn.

Có thể hình dung:

```text
Current Observation
        │
        ▼
     α × xt
        │
        ├──────┐
        │      ▼
        │   Previous
        │   Smoothed
        │      │
        │   (1-α)
        │      │
        └──────┤
               ▼
             st
```

Exponential Smoothing đặc biệt hữu ích khi cần xử lý dữ liệu theo streaming hoặc online.

---

# 10. Median Filter

Median Filter thay thế observation bằng median của một local window.

Ví dụ:

```text
10  11  50  12  13
```

Với window:

```text
11  50  12
```

median là:

$$
median(11,50,12)=12
$$

Do đó:

```text
10  11  12  12  13
```

Median Filter có khả năng loại bỏ các spike ngắn trong khi ít bị ảnh hưởng bởi extreme values hơn mean-based smoothing.

Đây là lý do median filtering có thể phù hợp khi dữ liệu vừa chứa noise vừa xuất hiện các spike bất thường.

---

# 11. Low-pass Filtering

Một cách tiếp cận khác là xem Time Series trong **frequency domain**.

Một signal có thể được biểu diễn thành các thành phần tần số:

```text
Signal
  │
  ├── Low Frequency
  │       ↓
  │   Trend / Slow Change
  │
  └── High Frequency
          ↓
       Fast Change / Noise
```

Nếu noise chủ yếu nằm ở high-frequency components, có thể sử dụng Low-pass Filter để giữ lại low-frequency components.

Ý tưởng:

$$
X(f)
\rightarrow
H(f)X(f)
$$

trong đó:

* $X(f)$: frequency representation;
* $H(f)$: filter;
* output: filtered signal.

Pipeline:

```text
Time Series
     ↓
Transform to Frequency Domain
     ↓
Frequency Filter
     ↓
Remove High-frequency Components
     ↓
Inverse Transform
     ↓
Clean Signal
```

---

# 12. Fourier Transform

Fourier Transform chuyển signal từ time domain sang frequency domain.

Discrete Fourier Transform:

$$
X_k=
\sum_{n=0}^{N-1}
x_n e^{-i2\pi kn/N}
$$

Sau đó có thể xác định những frequency components đóng góp vào signal.

Ví dụ:

```text
Time Domain
──────────────────
     noisy signal
          ↓
      Fourier
          ↓
Frequency Domain
──────────────────
Low frequencies | High frequencies
      ↑                ↑
   signal             noise
```

Nếu giả định noise nằm chủ yếu ở high frequencies, có thể loại bỏ chúng.

Tuy nhiên giả định này không phải lúc nào cũng đúng.

---

# 13. Wavelet-based Denoising

Fourier Transform biểu diễn signal bằng frequency components nhưng không cung cấp localization theo thời gian tốt.

Wavelet Transform giải quyết vấn đề này bằng cách phân tích signal ở nhiều scale.

```text
Signal
  ↓
Wavelet Transform
  │
  ├── Approximation
  │
  └── Detail
        ↓
     Threshold
        ↓
 Remove Noise
        ↓
Inverse Wavelet
        ↓
Clean Signal
```

Có thể biểu diễn:

$$
x(t)=A(t)+D_1(t)+D_2(t)+\cdots
$$

trong đó:

* $A(t)$: approximation;
* $D_i(t)$: detail components.

Các detail coefficients có magnitude nhỏ có thể được xem là noise và được threshold.

---

# 14. Savitzky-Golay Filter

Savitzky-Golay Filter thực hiện smoothing bằng cách fitting một polynomial cục bộ trong từng window.

Trong mỗi window:

$$
x_i\approx
a_0+a_1t+a_2t^2+\cdots+a_dt^d
$$

Sau đó sử dụng polynomial để ước lượng giá trị trung tâm.

Ưu điểm quan trọng:

> Có khả năng làm smooth dữ liệu nhưng giữ được shape và peak tốt hơn một số phương pháp moving average.

Pipeline:

```text
Time Series
     ↓
Sliding Window
     ↓
Polynomial Fit
     ↓
Estimate Center Point
     ↓
Move Window
     ↓
Smoothed Signal
```

Phương pháp này phù hợp khi hình dạng của signal cần được bảo toàn.

---

# 15. Kalman Filter

Kalman Filter xem hệ thống như một **state-space model**.

Có hai bước chính:

```text
Prediction
    ↓
Update
    ↓
Estimated State
```

State transition:

$$
x_t=Fx_{t-1}+w_t
$$

Observation:

$$
z_t=Hx_t+v_t
$$

trong đó:

* $x_t$: hidden state;
* $z_t$: observation;
* $w_t$: process noise;
* $v_t$: measurement noise.

Kalman Filter sử dụng cả:

```text
Previous State
+
Current Observation
        ↓
State Estimation
```

Do đó nó khác với moving average ở chỗ nó **mô hình hóa trạng thái của hệ thống** thay vì chỉ lấy trung bình local observations.

---

# 16. Model-based Denoising

Với những time series phức tạp, có thể xây dựng model để học underlying signal.

Ví dụ:

```text
Noisy Signal
     ↓
Time-Series Model
     ↓
Latent / Predicted Signal
     ↓
Denoised Signal
```

Một số hướng:

```text
AR / ARIMA
State-space Model
Kalman Filter
Autoencoder
LSTM
Transformer
```

Mục tiêu là học:

$$
f(X)\rightarrow\hat{S}
$$

trong đó:

* $X$: noisy observation;
* $\hat{S}$: estimated clean signal.

Các phương pháp này mạnh hơn nhưng có chi phí computation và yêu cầu mô hình hóa cao hơn.

---

# 17. Noise Reduction và Signal Preservation

Đây là trade-off quan trọng nhất.

Nếu filtering quá yếu:

```text
Noise remains
```

Nếu filtering quá mạnh:

```text
True Signal
     ↓
Removed
```

Có thể biểu diễn:

$$
\text{Denoising Quality}=\text{Noise Reduction}
+
\text{Signal Preservation}
$$

Mục tiêu không phải:

$$
\min Noise
$$

mà là:

$$
\boxed{
\min Noise
\quad
\text{while preserving useful signal information}
}
$$

---

# 18. Ví dụ về Over-smoothing

Giả sử signal có một peak thực:

```text
          TRUE EVENT
              ▲
              │
──────────────┼──────────────
```

Nếu smoothing quá mạnh:

```text
          ───╮
─────────────╰──────────────
```

Peak đã bị giảm.

Điều này đặc biệt nguy hiểm nếu peak đó đại diện cho:

* anomaly;
* machine failure;
* energy spike;
* medical event;
* traffic peak;
* sensor event.

Vì vậy:

> Một điểm dữ liệu “trông giống noise” chưa chắc là noise.

---

# 19. Noise Reduction trong Multivariate Time Series

Với multivariate time series:

$$
X_t=
[x_t^{(1)},x_t^{(2)},...,x_t^{(d)}]
$$

noise có thể xuất hiện riêng ở từng sensor hoặc có correlation giữa các sensor.

Ví dụ:

```text
Sensor A ──┐
Sensor B ──┼──→ Common Noise
Sensor C ──┘
```

Do đó có thể sử dụng information từ các biến khác để cải thiện estimation.

Đây là điểm kết nối giữa:

```text
Noise Reduction
       ↓
Multivariate Structure
       ↓
Sensor Fusion
```

Survey có phạm vi rộng, trong đó sensor fusion được xem là một phần của holistic preprocessing taxonomy chứ không chỉ tập trung vào cleaning đơn thuần. ([research.chalmers.se][2])

---

# 20. Noise Reduction cho Streaming Data

Một đặc điểm quan trọng của Time-Series Data là dữ liệu có thể đến liên tục:

```text
Sensor
  ↓
x1 → x2 → x3 → x4 → x5 → ...
```

Do đó không phải lúc nào cũng có thể chờ toàn bộ dataset rồi preprocessing.

Một pipeline online:

```text
Sensor
  ↓
Observation xt
  ↓
Online Filter
  ↓
Denoised xt
  ↓
AI / Analytics
```

Các phương pháp có computational cost thấp như moving average hoặc exponential smoothing phù hợp với môi trường streaming.

Đây cũng liên quan đến mục tiêu của survey về **Edge preprocessing**: đưa một phần preprocessing đến gần nguồn dữ liệu có thể giảm workload của hệ thống trung tâm, giảm resource consumption và hỗ trợ EdgeAI. ([ScienceDirect][1])

---

# 21. Noise Reduction tại Edge

Một kiến trúc điển hình:

```text
┌─────────────┐
│   Sensor    │
└──────┬──────┘
       │ Raw Data
       ▼
┌─────────────┐
│ Edge Device │
│             │
│ Denoising   │
└──────┬──────┘
       │ Clean Data
       ▼
┌─────────────┐
│ Central AI  │
└─────────────┘
```

Lợi ích:

* giảm data transmission;
* giảm bandwidth;
* giảm workload central server;
* giảm resource consumption;
* giảm lượng dữ liệu cần lưu trữ;
* hỗ trợ real-time processing.

Đây là một trong những động lực lớn của survey: preprocessing không chỉ được nhìn như bước chuẩn bị dữ liệu cho model mà còn được xem xét về **where preprocessing should happen**, đặc biệt trong hệ thống Edge/IoT. ([ScienceDirect][1])

---

# 22. So sánh các phương pháp

| Method                  | Temporal Context | Computational Cost |  Giữ Peak |          Streaming |    Edge |
| ----------------------- | ---------------: | -----------------: | --------: | -----------------: | ------: |
| Moving Average          |            Local |               Thấp |   Thấp–TB |                Tốt |     Tốt |
| Weighted Moving Average |            Local |               Thấp |        TB |                Tốt |     Tốt |
| Exponential Smoothing   |         Temporal |               Thấp |        TB |            Rất tốt | Rất tốt |
| Median Filter           |            Local |               Thấp |       Khá |                Tốt |     Tốt |
| Low-pass Filter         |        Frequency |                 TB |        TB | Tùy implementation |     Tùy |
| Savitzky-Golay          |            Local |                 TB |       Tốt |             Có thể |  Có thể |
| Wavelet                 |      Multi-scale |             TB–Cao |       Tốt |                Tùy |     Tùy |
| Kalman Filter           |      State-based |                 TB |       Tốt |            Rất tốt |     Tốt |
| Deep Learning           |          Learned |        Cao–Rất cao | Tùy model |                Khó | Hạn chế |

Bảng trên nên được hiểu như **trade-off giữa computational cost, temporal modeling và information preservation**, không phải một ranking tuyệt đối.

---

# 23. Cách lựa chọn Noise Reduction Method

Có thể sử dụng decision process:

```text
Noise nhỏ?
    │
    ├── Yes → Simple Smoothing
    │
    └── No
         ↓
Signal có sudden changes?
    │
    ├── Yes → Median / Savitzky-Golay / Model-based
    │
    └── No
         ↓
Có temporal dynamics mạnh?
    │
    ├── Yes → Exponential / Kalman / Time-series Model
    │
    └── No
         ↓
Noise nằm ở frequency cụ thể?
    │
    ├── Yes → Frequency-domain Filter
    │
    └── No → Statistical / Model-based Method
```

Quan trọng nhất là phải biết **noise có đặc tính gì trước khi chọn filter**.

---

# 24. Noise Reduction và Data Leakage

Trong Time-Series Forecasting, preprocessing phải bảo toàn temporal ordering.

Không nên xây dựng một filter sử dụng toàn bộ dataset nếu điều đó khiến dữ liệu tại thời điểm (t) sử dụng information từ tương lai.

Ví dụ:

```text
Past                    Future
───────────────────┬────────────────
x1 x2 x3 x4 x5     │ x6 x7 x8
                   ↑
                   t
```

Nếu smoothing tại (t) sử dụng:

$$
[x_{t-2},x_{t-1},x_t,x_{t+1},x_{t+2}]
$$

thì preprocessing đã sử dụng future observations.

Trong forecasting pipeline, điều này có thể tạo **future information leakage**.

Do đó cần phân biệt:

### Offline analysis

Có thể sử dụng centered filtering nếu mục tiêu chỉ là signal analysis.

### Forecasting

Cần đảm bảo:

$$
\boxed{
\hat{x}_t=f(x_1,\ldots,x_t)
}
$$

thay vì:

$$
\hat{x}_t=f(x_1,\ldots,x_{t-1},x_t,x_{t+1},...)
$$

nếu $x_{t+1},...$ không khả dụng tại thời điểm dự báo.

---

# 25. Noise Reduction trong Pipeline Preprocessing

Noise Reduction không nên được xem như một bước độc lập.

Một pipeline tổng quát:

```text
Raw Time Series
       │
       ▼
Data Validation
       │
       ▼
Missing Data
       │
       ▼
Outlier Detection
       │
       ▼
Noise Reduction
       │
       ▼
Transformation
       │
       ▼
Feature Engineering
       │
       ▼
Feature Selection
       │
       ▼
AI Model
```

Tuy nhiên thứ tự thực tế có thể thay đổi tùy bài toán.

Ví dụ nếu outlier là spike sensor error, filtering trước khi outlier detection có thể làm spike bị che mất.

Vì vậy:

> Thứ tự preprocessing phải dựa trên cơ chế sinh dữ liệu và mục tiêu của bài toán.

---

# 26. Những điểm chính từ Survey

## 26.1. Preprocessing không chỉ là Cleaning

Survey xây dựng một taxonomy rộng hơn data cleaning truyền thống, bao gồm nhiều nhóm preprocessing khác nhau và đánh giá tác động của chúng đến data quality và AI performance. ([research.chalmers.se][2])

## 26.2. Noise Reduction là bài toán Information Preservation

Mục tiêu không phải loại bỏ mọi biến động mà là giảm noise trong khi giữ lại signal.

$$
\boxed{
Noise\ Reduction
\neq
Maximum\ Smoothing
}
$$

## 26.3. Không có một filter tốt nhất

Method phải phụ thuộc vào:

* noise characteristics;
* sampling frequency;
* temporal dynamics;
* signal shape;
* computational constraints;
* application requirements.

## 26.4. Edge là một consideration quan trọng

Survey đặc biệt quan tâm đến khả năng phân phối preprocessing xuống Edge nhằm giảm workload central systems, resource consumption và hỗ trợ EdgeAI. ([ScienceDirect][1])

## 26.5. Preprocessing có thể ảnh hưởng trực tiếp đến AI

Một preprocessing method tốt không chỉ tạo dữ liệu “sạch hơn” mà phải tạo dữ liệu **phù hợp hơn cho downstream AI task**.

---

# 27. Kết luận

Noise Reduction là quá trình ước lượng underlying signal từ noisy observations:

$$
x_t=s_t+n_t
$$

và mục tiêu là:

$$
\hat{s}_t\approx s_t
$$

Các phương pháp đơn giản như **Moving Average, Weighted Moving Average và Exponential Smoothing** phù hợp khi cần computational efficiency và streaming processing. **Median Filter và Savitzky-Golay** có thể hữu ích khi cần giữ cấu trúc local của signal. **Frequency-domain methods** phù hợp khi noise có đặc tính tần số rõ ràng. **Kalman Filter và model-based methods** phù hợp khi cần mô hình hóa temporal dynamics.

Điểm quan trọng nhất:

$$
\boxed{
\text{Denoise}
\rightarrow
\text{Preserve Signal}
\rightarrow
\text{Improve Data Quality}
\rightarrow
\text{Support AI}
}
$$

Noise Reduction chỉ có giá trị khi nó làm giảm thành phần không mong muốn **mà không phá hủy thông tin có ý nghĩa đối với downstream task**.

### Ghi chú quan trọng khi học phần này

Trong survey, tác giả **không xây dựng một thuật toán Noise Reduction mới**. Đây là **survey + empirical analysis**, mục tiêu là hệ thống hóa các nhóm preprocessing và đánh giá tác động của chúng. Bài báo cũng nhấn mạnh góc nhìn rộng: preprocessing vừa nhằm nâng chất lượng dữ liệu/AI, vừa có thể được phân phối xuống Edge để giảm tải hệ thống trung tâm.

Đặc biệt, mình sẽ **không gán Moving Average, Kalman, Wavelet, Savitzky–Golay... là “thuật toán do paper đề xuất”**. Đây là các kỹ thuật nền được đưa vào bối cảnh survey; phần quan trọng khi học paper là hiểu **tác giả phân loại preprocessing như thế nào, mỗi nhóm giải quyết vấn đề gì và empirical analysis cho thấy preprocessing tác động ra sao**.

[1]: https://www.sciencedirect.com/science/article/pii/S2307187724000452?utm_source=chatgpt.com "Survey:Time-series data preprocessing: A survey and an empirical analysis - ScienceDirect"
[2]: https://research.chalmers.se/publication/540495/file/540495_Fulltext.pdf?utm_source=chatgpt.com "Survey: Time-Series Data Preprocessing: A Survey and an Empirical"
