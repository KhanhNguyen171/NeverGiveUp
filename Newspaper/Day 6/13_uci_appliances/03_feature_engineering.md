# 03. Feature Engineering

## 1. Mục tiêu

Trong `13_uci_appliances/02_preprocessing.md`, dữ liệu UCI Appliances đã được kiểm tra về chất lượng, bảo toàn thứ tự thời gian, chia theo chronology và chuyển sang dạng phù hợp với bài toán forecasting. Bước tiếp theo là **feature engineering**, nhằm biến đổi các quan sát ban đầu thành biểu diễn có khả năng cung cấp thông tin hữu ích cho mô hình dự báo.

Đối với dataset này, feature engineering tập trung vào ba nhóm chính:

1. **Temporal features:** biểu diễn các quy luật chu kỳ của thời gian.
2. **Lag features:** đưa thông tin lịch sử của target và các biến ngoại sinh vào biểu diễn tại thời điểm dự báo.
3. **Rolling features:** mô tả mức độ và xu hướng biến động trong một khoảng thời gian quá khứ.

Các đặc trưng được xây dựng phải tuân thủ nguyên tắc causal:

$$
\mathrm{Feature}*t=f\left(\mathbf{x}*{\leq t},y_{\leq t}\right)
$$

Nói cách khác, feature tại thời điểm $t$ chỉ được sử dụng thông tin có sẵn tại hoặc trước thời điểm $t$, không được sử dụng dữ liệu tương lai.

---

## 2. Temporal Features

Timestamp `date` chứa thông tin về cấu trúc chu kỳ của dữ liệu. Tuy nhiên, việc đưa trực tiếp `hour`, `day` hoặc `month` dưới dạng số nguyên có thể tạo ra quan hệ khoảng cách không phù hợp.

Ví dụ, nếu biểu diễn:

$$
\mathrm{hour}\in{0,1,\ldots,23}
$$

thì khoảng cách giữa (23) và (0) về mặt số học là (23), trong khi về mặt thời gian hai thời điểm này chỉ cách nhau một giờ.

Do đó, các biến chu kỳ được biểu diễn bằng hàm sine và cosine.

### 2.1. Hour-of-day

Với (h) là giờ trong ngày:

$$
\mathrm{hour}_{\sin}=\sin\left(2\pi\frac{h}{24}\right)
$$

$$
\mathrm{hour}_{\cos}=\cos\left(2\pi\frac{h}{24}\right)
$$

Hai đặc trưng này tạo ra biểu diễn liên tục cho chu kỳ 24 giờ.

### 2.2. Day-of-week

Với (d) là ngày trong tuần:

$$
\mathrm{dow}_{\sin}=\sin\left(2\pi\frac{d}{7}\right)
$$

$$
\mathrm{dow}_{\cos}=\cos\left(2\pi\frac{d}{7}\right)
$$

Cặp đặc trưng này biểu diễn chu kỳ 7 ngày.

### 2.3. Weekend indicator

Một biến nhị phân được sử dụng để phân biệt ngày cuối tuần:

$$
\mathrm{weekend}_t=\mathbb{I}(d_t\in{5,6})
$$

trong đó $\mathbb{I}(\cdot)$ là hàm chỉ báo.

Như vậy, nhóm temporal features trong nghiên cứu gồm:

```text
hour_sin
hour_cos
dow_sin
dow_cos
weekend
```

Các đặc trưng chu kỳ này được giữ nguyên miền giá trị tự nhiên và **không áp dụng StandardScaler**, phù hợp với nguyên tắc scaling đã trình bày trong `04_data_transformation/01_scaling_normalization.md`.

---

## 3. Lag Features

Temporal features mô tả vị trí của một quan sát trong chu kỳ thời gian, nhưng chưa trực tiếp cung cấp thông tin về trạng thái tiêu thụ trong quá khứ. Vì vậy, lag features được sử dụng để biểu diễn dependency giữa thời điểm hiện tại và các quan sát trước đó.

Với target:

$$
y_t=\mathrm{Appliances}_t
$$

lag (k) được định nghĩa:

$$
\mathrm{lag}*k(t)=y*{t-k}
$$

Ví dụ:

$$
\mathrm{lag}*1(t)=y*{t-1}
$$

biểu diễn mức tiêu thụ tại thời điểm ngay trước $t$.

Vì dữ liệu có chu kỳ 10 phút, một số lag có thể được diễn giải theo thời gian:

|   Lag | Khoảng thời gian |
| ----: | ---------------: |
|   $1$ |          10 phút |
|   $6$ |            1 giờ |
|  $36$ |            6 giờ |
|  $72$ |           12 giờ |
| $144$ |           24 giờ |

Các lag dài hơn cho phép mô hình tiếp cận những dependency ở các quy mô thời gian khác nhau.

Ví dụ, lag 144 tương ứng với cùng thời điểm của ngày trước:

$$
\mathrm{lag}*{144}(t)=y*{t-144}
$$

Điều này đặc biệt phù hợp với dataset có khả năng tồn tại các pattern tiêu thụ theo chu kỳ ngày.

---

## 4. Lag của biến ngoại sinh

Lag features không chỉ được áp dụng cho target. Với một biến ngoại sinh $x_t^{(j)}$, lag được định nghĩa:

$$
\mathrm{lag}*k^{(j)}(t)=x*{t-k}^{(j)}
$$

Các biến như nhiệt độ, độ ẩm hoặc tốc độ gió có thể có ảnh hưởng trễ đến mức tiêu thụ năng lượng.

Tuy nhiên, số lượng lag không được mở rộng tùy ý cho tất cả các biến. Việc tạo quá nhiều lag sẽ làm tăng số chiều:

$$
F_{\mathrm{new}}\gg F_{\mathrm{raw}}
$$

và có thể làm tăng redundancy cũng như computational cost.

Do đó, lag features được lựa chọn dựa trên:

* ý nghĩa temporal;
* độ phân giải 10 phút của dataset;
* mục tiêu forecasting;
* kết quả feature selection;
* nguy cơ tăng dimensionality.

Điều này tạo liên kết trực tiếp với `06_feature_selection/`, nơi các phương pháp filter, wrapper và embedded được sử dụng để kiểm soát số lượng đặc trưng.

---

## 5. Rolling Features

Lag features cung cấp thông tin tại một thời điểm cụ thể, trong khi rolling features mô tả **trạng thái tổng hợp của một khoảng lịch sử**.

Rolling mean với window $w$ được định nghĩa:

$$
\mathrm{rollmean}*w(t)=\frac{1}{w}\sum*{i=1}^{w}y_{t-i}
$$

Điểm quan trọng là cửa sổ rolling được dịch về quá khứ và không bao gồm $y_t$ hoặc bất kỳ giá trị nào sau $t$.

Một số rolling statistics có thể được sử dụng gồm:

### Rolling mean

$$
\mu_w(t)=\frac{1}{w}\sum_{i=1}^{w}y_{t-i}
$$

### Rolling standard deviation

$$
\sigma_w(t)=\sqrt{\frac{1}{w}\sum_{i=1}^{w}\left(y_{t-i}-\mu_w(t)\right)^2}
$$

### Rolling minimum

$$
\mathrm{min}*w(t)=\min*{1\leq i\leq w}y_{t-i}
$$

### Rolling maximum

$$
\mathrm{max}*w(t)=\max*{1\leq i\leq w}y_{t-i}
$$

Các statistics này cung cấp thông tin về:

* mức tiêu thụ trung bình;
* mức độ biến động;
* trạng thái thấp nhất;
* trạng thái cao nhất.

---

## 6. Causal Rolling Window

Đối với forecasting, rolling feature phải được xây dựng theo hướng causal.

Sai:

$$
\mathrm{rollmean}*w(t)=\frac{1}{w}\sum*{i=0}^{w-1}y_{t-i}
$$

vì biểu thức này sử dụng $y_t$, trong khi target tại thời điểm $t+1$ có thể được xây dựng dựa trên thông tin tại $t$, nhưng để đảm bảo định nghĩa feature nhất quán với pipeline forecasting, nghiên cứu sử dụng lịch sử kết thúc tại $t$.

Cách biểu diễn causal được sử dụng là:

$$
\mathrm{rollmean}*w(t)=\frac{1}{w}\sum*{i=1}^{w}y_{t-i}
$$

Do đó:

$$
\mathrm{Feature}*t\perp y*{t+1:t+H}
$$

theo nghĩa feature tại (t) không được phụ thuộc vào các quan sát tương lai.

Nguyên tắc này đặc biệt quan trọng vì chỉ một phép rolling sai alignment cũng có thể tạo ra **temporal leakage** mà không gây lỗi về mặt cú pháp hoặc chương trình.

---

## 7. Quan hệ giữa Lag và Rolling Features

Lag và rolling features có vai trò bổ sung.

Lag feature:

$$
\mathrm{lag}*k(t)=y*{t-k}
$$

cung cấp một điểm quan sát cụ thể.

Rolling feature:

$$
\mathrm{rollmean}*w(t)=\frac{1}{w}\sum*{i=1}^{w}y_{t-i}
$$

cung cấp một thống kê tổng hợp.

Có thể hiểu:

```text
Lag
  ↓
Point-wise historical information

Rolling
  ↓
Aggregated historical information
```

Ví dụ, `lag_1` phản ánh trạng thái tiêu thụ ngay trước thời điểm dự báo, trong khi `rollmean_36` mô tả mức tiêu thụ trung bình trong 6 giờ trước đó.

Sự kết hợp hai loại feature cho phép mô hình đồng thời quan sát **ngắn hạn** và **xu hướng tổng thể**.

---

## 8. Feature Representation

Sau khi temporal, lag và rolling features được tạo, dữ liệu được tổ chức thành các feature groups như đã định nghĩa trong `13_uci_appliances/02_preprocessing.md`.

Một biểu diễn tổng quát tại thời điểm $t$ là:

$$
\mathbf{x}_t=\left[\mathbf{x}_t^{\mathrm{raw}},\mathbf{x}_t^{\mathrm{temporal}},\mathbf{x}_t^{\mathrm{lag}},\mathbf{x}_t^{\mathrm{rolling}}\right]
$$

Trong đó:

* $\mathbf{x}_t^{\mathrm{raw}}$: các biến ngoại sinh ban đầu;
* $\mathbf{x}_t^{\mathrm{temporal}}$: temporal features;
* $\mathbf{x}_t^{\mathrm{lag}}$: lag features;
* $\mathbf{x}_t^{\mathrm{rolling}}$: rolling features.

Sau đó, chuỗi các vector đặc trưng được đưa vào sliding window:

$$
\mathbf{X}*{t-L+1:t}=\left[\mathbf{x}*{t-L+1},\mathbf{x}*{t-L+2},\ldots,\mathbf{x}*{t}\right]
$$

với:

$$
\mathbf{X}_{t-L+1:t}\in\mathbb{R}^{L\times F}
$$

Trong đó $L$ là lookback và $F$ là số lượng feature sau feature engineering.

---

## 9. Kiểm soát Data Leakage

Feature engineering phải được thực hiện sao cho thông tin tương lai không xuất hiện trong input.

Đối với target $y_t$, điều kiện cơ bản là:

$$
\mathbf{x}*t=f\left(y*{\leq t},\mathbf{x}_{\leq t}\right)
$$

và target forecasting:

$$
y_{t+1}=\mathrm{Appliances}_{t+1}
$$

không được sử dụng để tạo $\mathbf{x}_t$.

Đối với rolling features:

$$
\mathrm{Rolling}*t=f(y*{t-1},y_{t-2},\ldots)
$$

thay vì:

$$
\mathrm{Rolling}*t=f(y_t,y*{t-1},\ldots)
$$

nếu $y_t$ không thuộc thông tin quan sát hợp lệ tại thời điểm feature được xác định.

Ngoài ra, feature engineering phải được thực hiện sau chronological split nếu bước đó sử dụng các thống kê được học từ dữ liệu. Điều này duy trì nguyên tắc **Train-only fitting** đã thiết lập ở `13_uci_appliances/02_preprocessing.md`.

---

## 10. Feature Selection sau Feature Engineering

Feature engineering có thể làm tăng đáng kể số lượng biến:

$$
F_{\mathrm{engineered}}>F_{\mathrm{raw}}
$$

Do đó, không phải mọi feature được tạo ra đều mặc nhiên được đưa vào mô hình.

Quá trình tiếp theo được thực hiện theo nội dung của `06_feature_selection/`, bao gồm:

* **Filter methods:** đánh giá feature dựa trên các tiêu chí thống kê;
* **Wrapper methods:** đánh giá tập feature thông qua hiệu quả của mô hình;
* **Embedded methods:** thực hiện selection trong quá trình học;
* **Dimensionality reduction:** xây dựng representation có số chiều thấp hơn khi cần thiết.

Trong case study UCI Appliances, feature engineering và feature selection được xem là hai bước khác nhau:

$$
\mathrm{Raw\ Features}\rightarrow\mathrm{Feature\ Engineering}\rightarrow\mathrm{Feature\ Selection}
$$

Điều này giúp tránh nhầm lẫn giữa việc **tạo thông tin mới** và việc **lựa chọn thông tin có ích**.

---

## 11. Kết nối với mô hình dự báo

Sau feature engineering và feature selection, mỗi mẫu được biểu diễn dưới dạng:

$$
\left(\mathbf{X}_{t-L+1:t},y_{t+1}\right)
$$

và toàn bộ dataset có dạng:

$$
\mathcal{D}=\left\{\left(\mathbf{X}_{t-L+1:t},y_{t+1}\right)\right\}_{t=L}^{N-1}
$$

với:

$$
L\in{36,72,144}
$$

và:

$$
\mathbf{X}_{t-L+1:t}\in\mathbb{R}^{L\times F}
$$

Đây là representation cuối cùng trước khi dữ liệu được chuyển sang mô hình machine learning hoặc deep learning.

Đối với các mô hình sequence như LSTM, input có thể được biểu diễn theo batch:

$$
\mathbf{X}\in\mathbb{R}^{B\times L\times F}
$$

trong đó $B$ là batch size.

Như vậy, feature engineering tạo cầu nối giữa **bảng dữ liệu thời gian ban đầu** và **tensor sequence** được sử dụng bởi mô hình.

---

## 12. Tóm tắt

Feature engineering trên UCI Appliances tập trung vào việc khai thác cấu trúc thời gian thay vì mở rộng đặc trưng một cách tùy ý. Ba thành phần chính gồm:

$$
\boxed{\mathrm{Temporal}+\mathrm{Lag}+\mathrm{Rolling}}
$$

Temporal features biểu diễn chu kỳ ngày và tuần; lag features đưa thông tin lịch sử tại các khoảng thời gian cụ thể; rolling features tổng hợp trạng thái và mức độ biến động trong các khoảng thời gian quá khứ.

Toàn bộ quá trình phải tuân thủ causal constraint:

$$
\boxed{\mathbf{x}_t\text{ chỉ sử dụng thông tin khả dụng đến thời điểm }t}
$$

Sau khi feature engineering hoàn tất, dữ liệu được chuyển thành các cửa sổ:

$$
\mathbf{X}*{t-L+1:t}\rightarrow y*{t+1}
$$

với $L\in{36,72,144}$, tạo đầu vào cho bước **AI-ready data** và đánh giá thực nghiệm ở các phần tiếp theo. Do đó, feature engineering trong case study không phải một bước độc lập mà là mắt xích nối trực tiếp giữa **data transformation**, **feature selection**, **temporal representation** và **forecasting model**.
