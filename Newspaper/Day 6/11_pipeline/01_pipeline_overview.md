# 11.1 Pipeline Overview

## 1. Mục tiêu của pipeline

Tiền xử lý dữ liệu chuỗi thời gian là một quy trình biến đổi dữ liệu quan sát ở trạng thái thô thành biểu diễn có cấu trúc, nhất quán và phù hợp với thuật toán phân tích hoặc mô hình trí tuệ nhân tạo (AI). Đối với chuỗi thời gian, pipeline không chỉ nhằm cải thiện chất lượng dữ liệu mà còn phải **duy trì cấu trúc thời gian, quan hệ phụ thuộc giữa các quan sát và tính nhất quán của thông tin theo thời gian**.

Nghiên cứu của Tawakuli et al. xem tiền xử lý chuỗi thời gian như một tập hợp các kỹ thuật được tổ chức theo nhiều nhóm chức năng, bao gồm xử lý dữ liệu không hoàn chỉnh, phát hiện bất thường, giảm nhiễu, biến đổi dữ liệu và xây dựng biểu diễn phù hợp cho AI. Nghiên cứu cũng nhấn mạnh rằng tiền xử lý có thể ảnh hưởng trực tiếp đến chất lượng dữ liệu, hiệu quả huấn luyện và kết quả của các thuật toán AI.

Trong phạm vi nghiên cứu này, pipeline được tổ chức thành ba tầng chính:

1. **Data Cleaning** — loại bỏ hoặc xử lý các vấn đề về chất lượng dữ liệu.
2. **Data Transformation** — biến đổi dữ liệu về dạng có tính nhất quán và phù hợp với thuật toán.
3. **Feature Engineering** — xây dựng biểu diễn đặc trưng chứa thông tin hữu ích cho nhiệm vụ học máy.

Đầu ra của toàn bộ quá trình là **AI-ready data**, tức dữ liệu có cấu trúc, chất lượng và biểu diễn phù hợp để đưa vào mô hình AI.

---

## 2. Kiến trúc tổng quát

Pipeline tiền xử lý có thể được biểu diễn như sau:

```text
Raw Time-Series Data
        │
        ▼
┌─────────────────────┐
│   Data Validation   │
│ timestamps, types,  │
│ ranges, duplicates  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Data Cleaning    │
│ missing values      │
│ outliers            │
│ noise               │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Data Transformation │
│ scaling             │
│ normalization       │
│ transformation      │
│ stationarity        │
│ decomposition       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Feature Engineering │
│ temporal features   │
│ lag features        │
│ rolling features    │
│ representation      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   AI-Ready Data     │
│ structured input    │
│ for ML / DL models  │
└─────────────────────┘
```

Pipeline trên không nên được hiểu là một chuỗi thao tác hoàn toàn tuyến tính và bất biến. Thứ tự cụ thể của các bước phụ thuộc vào đặc điểm dữ liệu, mục tiêu dự đoán và giả định của mô hình. Chẳng hạn, việc xử lý missing values có thể cần được thực hiện trước khi tính các đặc trưng rolling; trong khi scaling thường phải được thực hiện sau khi xác định tập đặc trưng cuối cùng. Vì vậy, pipeline cần được thiết kế dựa trên **dependency giữa các phép biến đổi**, thay vì áp dụng một danh sách thao tác cố định cho mọi dataset.

---

## 3. Data Cleaning

Data cleaning là tầng đầu tiên nhằm kiểm soát chất lượng của dữ liệu quan sát. Với chuỗi thời gian, chất lượng dữ liệu không chỉ được đánh giá trên từng giá trị riêng lẻ mà còn trên **tính hợp lệ của chuỗi theo trục thời gian**.

Các vấn đề chính gồm:

* missing values;
* duplicate observations;
* timestamp không hợp lệ hoặc không nhất quán;
* giá trị nằm ngoài miền hợp lệ;
* outliers;
* measurement noise;
* khoảng trống hoặc gián đoạn trong chuỗi thời gian.

Đối với một chuỗi thời gian được biểu diễn bởi

$$
\mathcal{X}=

\left \{
(t_i,\mathbf{x}_i)
\right \}_{i=1}^{N},
$$

mỗi quan sát bao gồm timestamp $t_i$ và vector đặc trưng $\mathbf{x}_i$. Một pipeline hợp lệ phải đảm bảo rằng các phép xử lý không làm phá vỡ quan hệ giữa $t_i$ và $\mathbf{x}_i$.

Ví dụ, nếu dữ liệu được lấy mẫu với chu kỳ $\Delta t$, điều kiện lý tưởng là

$$
t_{i+1}-t_i=\Delta t.
$$

Nếu điều kiện này bị vi phạm, pipeline cần xác định liệu đó là missing observation, sampling irregularity hay một sự kiện thực tế của hệ thống trước khi thực hiện interpolation hoặc resampling.

Do đó, cleaning trong time series cần được xem là quá trình **khôi phục tính hợp lệ của cấu trúc dữ liệu**, thay vì đơn thuần thay thế các giá trị bị thiếu.

---

## 4. Data Transformation

Sau khi dữ liệu đạt mức chất lượng cần thiết, tầng transformation biến đổi phân phối hoặc biểu diễn của dữ liệu nhằm đáp ứng yêu cầu của thuật toán.

Một phép biến đổi tổng quát có thể được viết:

$$
\mathbf{z}_t = f(\mathbf{x}_t),
$$

trong đó $\mathbf{x}_t$ là dữ liệu sau cleaning, $f(\cdot)$ là phép biến đổi và $\mathbf{z}_t$ là biểu diễn mới.

Các nhóm transformation chính trong pipeline gồm:

### 4.1. Scaling và normalization

Scaling đưa các đặc trưng về miền hoặc thang đo phù hợp. Ví dụ, Standardization được định nghĩa bởi

$$
z_t=

\frac{x_t-\mu}{\sigma},
$$

trong đó $\mu$ và $\sigma$ phải được ước lượng từ dữ liệu huấn luyện khi pipeline được sử dụng cho machine learning.

Điều này đặc biệt quan trọng đối với các thuật toán nhạy với scale của feature, chẳng hạn neural networks, distance-based models và nhiều phương pháp tối ưu gradient.

### 4.2. Transformation

Các phép biến đổi như logarithmic transformation hoặc power transformation có thể được sử dụng để điều chỉnh phân phối dữ liệu hoặc giảm ảnh hưởng của độ lệch phân phối.

Ví dụ:

$$
x'_t=\log(x_t+c),
$$

với $c$ được chọn để bảo đảm miền xác định của phép logarithm.

### 4.3. Stationarity

Một số mô hình thống kê yêu cầu chuỗi có tính dừng. Với một chuỗi $x_t$, sai phân bậc nhất được định nghĩa:

$$
\Delta x_t=x_t-x_{t-1}.
$$

Transformation nhằm xử lý trend hoặc các thành phần không dừng phải được lựa chọn dựa trên mục tiêu phân tích; không nên áp dụng differentiation hoặc detrending mặc định cho mọi bài toán.

### 4.4. Decomposition

Chuỗi thời gian có thể được biểu diễn dưới dạng tổng của các thành phần:

$$
x_t = T_t + S_t + R_t,
$$

trong đó:

* $T_t$: trend;
* $S_t$: seasonal component;
* $R_t$: residual.

Decomposition có thể giúp tách các cấu trúc khác nhau của chuỗi trước khi xây dựng đặc trưng hoặc mô hình hóa.

Nghiên cứu được sử dụng làm nền tảng cho survey cũng tổ chức các kỹ thuật preprocessing theo các nhóm chức năng nhằm đánh giá tác động của chúng đến chất lượng dữ liệu và hiệu năng AI.

---

## 5. Feature Engineering

Feature engineering chuyển dữ liệu đã được làm sạch và biến đổi thành các đặc trưng có khả năng biểu diễn cấu trúc thời gian và thông tin liên quan đến nhiệm vụ học.

Với dữ liệu tại thời điểm $t$, vector đặc trưng cuối cùng có thể được viết:

$$
\mathbf{z}_t=

\left[
\mathbf{x}_t,,
\boldsymbol{\phi}_t^{\mathrm{temporal}},,
\boldsymbol{\phi}_t^{\mathrm{lag}},,
\boldsymbol{\phi}_t^{\mathrm{rolling}}
\right],
$$

trong đó:

* $\mathbf{x}_t$ là các đặc trưng quan sát;
* $\boldsymbol{\phi}_t^{\mathrm{temporal}}$ là temporal features;
* $\boldsymbol{\phi}_t^{\mathrm{lag}}$ là lag features;
* $\boldsymbol{\phi}_t^{\mathrm{rolling}}$ là rolling features.

### 5.1. Temporal features

Các thông tin như hour, day-of-week hoặc month có thể được biểu diễn trực tiếp hoặc mã hóa tuần hoàn. Với một biến tuần hoàn có chu kỳ $P$:

$$
x_t^{\sin}=

\sin\left(
\frac{2\pi c_t}{P}
\right),
$$

$$
x_t^{\cos}=

\cos\left(
\frac{2\pi c_t}{P}
\right).
$$

Biểu diễn này bảo toàn tính liên tục giữa điểm cuối và điểm đầu của chu kỳ.

### 5.2. Lag features

Lag feature đưa thông tin lịch sử vào vector đầu vào:

$$
x_t^{(k)} = x_{t-k}.
$$

Do đó, mô hình có thể khai thác trực tiếp dependency theo thời gian mà không cần chỉ dựa vào giá trị hiện tại.

### 5.3. Rolling features

Rolling statistics tổng hợp thông tin trong một cửa sổ lịch sử:

$$
\mu_t^{(w)}=

\frac{1}{w}
\sum_{k=0}^{w-1}
x_{t-k}.
$$

Tương tự, rolling variance, minimum, maximum hoặc các thống kê khác có thể được sử dụng để biểu diễn local temporal behavior.

Feature engineering vì vậy đóng vai trò chuyển từ **giá trị quan sát** sang **biểu diễn có ý nghĩa đối với nhiệm vụ học**.

---

## 6. Từ dữ liệu đã xử lý đến AI-ready data

Sau các bước trên, dữ liệu cần được tổ chức thành dạng phù hợp với mô hình đích. Đối với bài toán supervised learning trên time series, một biểu diễn phổ biến là cửa sổ lịch sử:

$$
\mathbf{X}_{t-L+1:t}=

\left[
\mathbf{z}_{t-L+1},
\ldots,
\mathbf{z}_{t}
\right],
$$

với $L$ là chiều dài cửa sổ.

Target cho bài toán forecasting có thể được biểu diễn:

$$
y_{t+H},
$$

trong đó $H$ là forecasting horizon.

Khi đó, pipeline tạo ra tập mẫu:

$$
\mathcal{D}=

\left \{
\left(
\mathbf{X}_{t-L+1:t},
y_{t+H}
\right)
\right \}.
$$

Đây là bước chuyển từ **time-series data ở dạng record-level** sang **model-ready representation**.

Một dataset được xem là AI-ready khi ít nhất các điều kiện sau được thỏa mãn:

1. timestamp và thứ tự thời gian hợp lệ;
2. missing values được xử lý theo chiến lược xác định;
3. outliers và noise được kiểm soát phù hợp với mục tiêu;
4. các feature có scale và representation phù hợp;
5. không xảy ra temporal leakage;
6. input và target được căn chỉnh chính xác;
7. dữ liệu có cấu trúc phù hợp với mô hình downstream.

---

## 7. Nguyên tắc thiết kế pipeline

Pipeline tiền xử lý trong nghiên cứu này tuân theo bốn nguyên tắc chính.

### 7.1. Preserve temporal structure

Mọi phép biến đổi phải bảo toàn thông tin thứ tự thời gian và dependency giữa các observations. Không được áp dụng các thao tác làm xáo trộn temporal ordering nếu nhiệm vụ yêu cầu cấu trúc tuần tự.

### 7.2. Prevent data leakage

Các tham số được học từ dữ liệu, chẳng hạn $\mu$ và $\sigma$ của Standardization, phải được ước lượng từ training set:

$$
\theta_{\mathrm{transform}}=

\operatorname{Fit}
\left(
\mathcal{D}_{\mathrm{train}}
\right).
$$

Sau đó cùng một transformation được áp dụng cho validation và test:

$$
\mathcal{D}_{\mathrm{val}}'=

f_{\theta}
\left(
\mathcal{D}_{\mathrm{val}}
\right),
$$

$$
\mathcal{D}_{\mathrm{test}}'=

f_{\theta}
\left(
\mathcal{D}_{\mathrm{test}}
\right).
$$

Việc fit transformation trên toàn bộ dataset trước khi chia train/validation/test có thể làm thông tin từ validation hoặc test ảnh hưởng đến quá trình huấn luyện, dẫn đến đánh giá quá lạc quan.

### 7.3. Task-aware preprocessing

Không tồn tại một preprocessing pipeline tối ưu cho mọi bài toán. Một transformation chỉ nên được sử dụng khi nó phù hợp với:

* đặc tính của dữ liệu;
* mục tiêu prediction hoặc analysis;
* assumptions của mô hình;
* yêu cầu triển khai.

Điều này phù hợp với mục tiêu của nghiên cứu gốc: đánh giá preprocessing không chỉ theo khả năng cải thiện data quality mà còn theo tác động thực tế đến hiệu năng của AI.

### 7.4. Reproducibility

Mỗi preprocessing operation cần có thể xác định rõ:

$$
\text{Input}
\rightarrow
\text{Method}
\rightarrow
\text{Parameters}
\rightarrow
\text{Output}.
$$

Do đó, một pipeline nghiên cứu cần lưu lại các thông tin như phương pháp được sử dụng, tham số, thứ tự thực hiện và tập dữ liệu dùng để ước lượng tham số. Điều này cho phép tái tạo chính xác quá trình biến đổi dữ liệu và so sánh công bằng giữa các preprocessing strategies.

---

## 8. Quan hệ với các chương tiếp theo

Chương 11 không giới thiệu thêm một taxonomy mới mà **chuyển taxonomy và các phương pháp đã phân tích ở các chương trước thành một quy trình xử lý thống nhất**.

Cụ thể:

```text
03 Data Cleaning
        │
        ▼
11.02 Data Cleaning Pipeline
        │
        ▼
04 Data Transformation
        │
        ▼
11.03 Transformation Pipeline
        │
        ▼
05 Feature Engineering
        │
        ▼
11.04 Feature Engineering Pipeline
        │
        ▼
11.05 AI-Ready Data
```

Do đó, các mục tiếp theo của chương 11 tập trung vào **cách tổ chức và thực thi pipeline**, thay vì tiếp tục trình bày lại lý thuyết của từng phương pháp.

Cấu trúc này tạo cầu nối giữa phần survey về từng nhóm preprocessing và phần thực nghiệm. Các kỹ thuật được trình bày ở Chương 3–8 cung cấp **methodological components**, trong khi Chương 11 tổ chức các components đó thành một **end-to-end preprocessing workflow** có thể áp dụng cho dữ liệu chuỗi thời gian trước khi đưa vào các mô hình AI.

---

## 9. Tóm tắt

Pipeline preprocessing cho time series có thể được xem là phép ánh xạ:

$$
\mathcal{X}*{\mathrm{raw}}
\xrightarrow{\mathrm{Cleaning}}
\mathcal{X}*{\mathrm{clean}}
\xrightarrow{\mathrm{Transformation}}
\mathcal{X}*{\mathrm{transformed}}
\xrightarrow{\mathrm{Feature\ Engineering}}
\mathcal{X}*{\mathrm{AI-ready}}.
$$

Mục tiêu không phải là thực hiện càng nhiều preprocessing operations càng tốt, mà là xây dựng một chuỗi biến đổi **đủ để giải quyết các vấn đề về chất lượng dữ liệu, phù hợp với yêu cầu của mô hình và không làm mất thông tin có ý nghĩa theo thời gian**.

Theo hướng tiếp cận của nghiên cứu nền tảng, preprocessing cần được đánh giá cả ở cấp độ **data quality** và **AI performance**. Vì vậy, pipeline trong nghiên cứu này được thiết kế như một cầu nối giữa dữ liệu thô và mô hình AI, trong đó mỗi bước biến đổi phải có mục đích rõ ràng, có thể kiểm chứng và có khả năng tái lập.

### Tài liệu tham khảo chính

Tawakuli, A., Havers, B., Gulisano, V. M., Kaiser, D., & Engel, T. (2025). *Survey: Time-Series Data Preprocessing: A Survey and an Empirical Analysis*. **Journal of Engineering Research, 13**(2), 674–711. DOI: 10.1016/j.jer.2024.02.018.
