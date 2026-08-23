# Results

## 1. Tổng quan kết quả

Phần này trình bày kết quả thực nghiệm nhằm đánh giá ảnh hưởng của các phương pháp preprocessing đối với **chất lượng dữ liệu đầu vào** và **hiệu quả của mô hình AI**. Đây cũng là mục tiêu thực nghiệm được xác định trong bài nghiên cứu gốc: không chỉ khảo sát các kỹ thuật preprocessing cho numerical time-series data mà còn đánh giá thực nghiệm tác động của chúng đến data quality và model performance.

Kết quả được phân tích theo chuỗi:

$$
\text{Preprocessing}
\rightarrow
\text{Data Quality}
\rightarrow
\text{Model Input}
\rightarrow
\text{Model Performance}.
$$

Việc phân tích không nhằm xác định một phương pháp tốt nhất trong mọi trường hợp, mà nhằm xác định mối quan hệ giữa **đặc điểm dữ liệu**, **phương pháp preprocessing** và **kết quả của mô hình**.

---

## 2. Kết quả theo nhóm preprocessing

Các kết quả được tổ chức theo các nhóm chính trong taxonomy của survey:

$$
\boxed{
\text{Data Cleaning}
\rightarrow
\text{Data Transformation}
\rightarrow
\text{Feature Engineering}
\rightarrow
\text{Feature Selection}
}
$$

Mỗi nhóm được đánh giá theo hai khía cạnh:

1. tác động lên representation của dữ liệu;
2. tác động lên performance của mô hình.

Cách phân tích này phù hợp với phạm vi của nghiên cứu gốc, trong đó preprocessing được xem là một quá trình có cấu trúc thay vì một phép biến đổi đơn lẻ. Bài nghiên cứu cũng nhấn mạnh rằng preprocessing vừa cần thiết để đưa dữ liệu về dạng phù hợp với mô hình, vừa có thể ảnh hưởng đến hiệu quả huấn luyện và độ chính xác đầu ra.

---

## 3. Kết quả đối với Data Cleaning

### 3.1. Missing data

Missing-value handling có vai trò đảm bảo tính đầy đủ của input trước khi dữ liệu được đưa vào mô hình.

Về mặt representation, nếu dữ liệu ban đầu có:

$$
N_{\mathrm{missing}}
$$

giá trị thiếu, preprocessing cần tạo ra representation mà mô hình có thể xử lý:

$$
\mathbf{X}*{\mathrm{raw}}
\rightarrow
\mathbf{X}*{\mathrm{clean}}.
$$

Tuy nhiên, việc loại bỏ quan sát và việc impute giá trị tạo ra hai loại tác động khác nhau.

Deletion làm giảm số lượng mẫu:

$$
N'
\lt
N,
$$

trong khi imputation giữ nguyên kích thước dataset:

$$
N'=N.
$$

Do đó, kết quả cần được diễn giải đồng thời theo prediction performance và lượng dữ liệu được giữ lại.

Một phương pháp imputation chỉ được xem là có lợi khi việc khôi phục các giá trị thiếu không làm suy giảm đáng kể thông tin temporal hoặc gây ra sai lệch trong phân phối dữ liệu.

---

### 3.2. Outlier handling

Outlier detection tạo ra một trade-off quan trọng.

Nếu các extreme values là lỗi đo:

$$
x_t\in\mathcal{O}_{\mathrm{error}},
$$

việc loại bỏ hoặc sửa chúng có thể cải thiện chất lượng input.

Ngược lại, nếu:

$$
x_t\in\mathcal{O}_{\mathrm{valid}},
$$

chúng có thể chứa thông tin quan trọng về các sự kiện bất thường.

Do đó:

$$
\text{Outlier Removal}
\not\equiv
\text{Information Improvement}.
$$

Kết quả thực nghiệm cần được diễn giải dựa trên sự thay đổi của cả data quality và model performance thay vì chỉ dựa trên số lượng outliers được loại bỏ.

---

### 3.3. Noise reduction

Noise reduction có thể làm cho chuỗi mượt hơn:

$$
x_t=

s_t+\epsilon_t
\quad
\rightarrow
\quad
\widehat{s}_t.
$$

Khi $\epsilon_t$ chiếm tỷ trọng đáng kể, smoothing có khả năng làm giảm variance không mong muốn và tạo representation ổn định hơn.

Tuy nhiên, nếu cửa sổ smoothing quá lớn:

$$
w\gg w_{\mathrm{optimal}},
$$

các biến động ngắn hạn cũng có thể bị loại bỏ.

Vì vậy, kết quả được diễn giải theo trade-off:

$$
\text{Noise Suppression}
\leftrightarrow
\text{Signal Preservation}.
$$

---

## 4. Kết quả đối với Data Transformation

### 4.1. Scaling và normalization

Scaling chủ yếu thay đổi numerical representation mà không làm thay đổi thứ tự tương đối của các quan sát đối với những phép biến đổi đơn điệu.

Với Standardization:

$$
x_t'=

\frac{x_t-\mu}{\sigma},
$$

các biến có magnitude khác nhau được đưa về cùng một scale.

Ảnh hưởng của scaling phụ thuộc vào thuật toán. Đối với các mô hình nhạy với scale của feature, normalization có thể giúp quá trình tối ưu ổn định hơn. Ngược lại, với các mô hình dựa trên partition hoặc rule, tác động có thể nhỏ hơn.

Do đó, kết quả không nên được diễn giải rằng normalization luôn cải thiện prediction performance.

---

### 4.2. Transformation

Các phép transformation như logarithmic hoặc power transformation có thể thay đổi shape của distribution:

$$
x_t'=

g(x_t).
$$

Nếu transformation làm giảm skewness hoặc ổn định variance, representation có thể phù hợp hơn với một số thuật toán.

Tuy nhiên, transformation cũng làm thay đổi interpretation của feature. Vì vậy, improvement về metric cần được cân nhắc cùng khả năng diễn giải của dữ liệu sau biến đổi.

---

### 4.3. Stationarity và decomposition

Đối với các chuỗi có trend hoặc seasonality, decomposition có thể tách:

$$
x_t
=

T_t+S_t+R_t.
$$

Điều này giúp mô hình xử lý riêng các thành phần có cấu trúc khác nhau.

Differencing có thể giảm trend:

$$
\nabla x_t=

x_t-x_{t-1}.
$$

Tuy nhiên, việc loại bỏ trend không phải lúc nào cũng có lợi cho mô hình AI. Nếu trend chứa thông tin dự báo, preprocessing quá mạnh có thể làm giảm predictive signal.

Do đó, kết quả cần được đánh giá theo nguyên tắc:

$$
\text{Stationarity}
\neq
\text{Prediction Improvement}.
$$

---

## 5. Kết quả đối với Feature Engineering

Feature engineering tạo ra representation mới nhằm biểu diễn rõ hơn temporal structure.

Với lag features:

$$
\mathbf{f}_t^{\mathrm{lag}}=

[
x_{t-1},
x_{t-2},
\ldots,
x_{t-K}
].
$$

Với rolling features:

$$
\mathbf{f}_t^{\mathrm{rolling}}=

[
\mu_t^{(w)},
\sigma_t^{(w)},
\ldots
].
$$

Các feature này có thể giúp mô hình khai thác temporal dependence mà representation dạng point-wise không thể biểu diễn đầy đủ.

Tuy nhiên, feature engineering cũng làm tăng dimensionality:

$$
d_{\mathrm{new}}

\gt

d_{\mathrm{raw}}.
$$

Do đó, improvement về prediction performance phải được cân nhắc với:

$$
\Delta d=

d_{\mathrm{new}}-d_{\mathrm{raw}}.
$$

Nếu số lượng feature tăng đáng kể nhưng performance chỉ cải thiện rất nhỏ, preprocessing configuration đó có thể không có lợi về mặt tổng thể.

---

## 6. Kết quả đối với Feature Selection

Feature selection tìm tập con:

$$
\mathcal{F}^{*}
\subseteq
\mathcal{F}.
$$

Mục tiêu không đơn thuần là giảm số feature mà là loại bỏ các biến dư thừa trong khi duy trì information relevant cho prediction.

Hiệu quả của feature selection có thể được đánh giá thông qua:

$$
(\mathrm{RMSE},\mathrm{MAE},R^2,d').
$$

Một configuration được xem là hiệu quả khi:

$$
d'\ll d
$$

nhưng:

$$
\mathrm{RMSE}*{\mathrm{selected}}
\approx
\mathrm{RMSE}*{\mathrm{full}}
$$

hoặc tốt hơn:

$$
\mathrm{RMSE}*{\mathrm{selected}}
\lt
\mathrm{RMSE}*{\mathrm{full}}.
$$

Khi đó, feature selection vừa giảm dimensionality vừa duy trì hoặc cải thiện khả năng dự báo.

---

## 7. Tổng hợp kết quả theo metric

Kết quả thực nghiệm được tổng hợp bằng ba metric chính:

$$
\mathrm{MAE},
\qquad
\mathrm{RMSE},
\qquad
R^2.
$$

Trong đó:

* MAE càng nhỏ càng tốt;
* RMSE càng nhỏ càng tốt;
* $R^2$ càng lớn càng tốt.

Có thể biểu diễn kết quả của configuration $P_k$ bằng vector:

$$
\mathbf{M}_k=

\left[
\mathrm{MAE}_k,
\mathrm{RMSE}_k,
R_k^2
\right].
$$

So sánh giữa baseline và preprocessing configuration được thực hiện thông qua:

$$
\Delta\mathbf{M}_k=

\mathbf{M}*k-\mathbf{M}*{\mathrm{base}}.
$$

Đối với MAE và RMSE, giá trị âm thể hiện giảm lỗi; đối với $R^2$, giá trị dương thể hiện cải thiện.

---

## 8. Kết quả về Data Quality và Model Performance

Một đóng góp quan trọng của empirical analysis là phân biệt:

$$
\text{Data Quality Improvement}
$$

với

$$
\text{Model Performance Improvement}.
$$

Hai đại lượng này không nhất thiết đồng biến.

Có thể xảy ra trường hợp:

$$
Q_{\mathrm{after}} \gt Q_{\mathrm{before}}
$$

nhưng:

$$
M_{\mathrm{after}}\leq M_{\mathrm{before}}.
$$

Nguyên nhân là preprocessing có thể làm dữ liệu sạch hơn theo một tiêu chí nhưng đồng thời loại bỏ information hữu ích đối với nhiệm vụ dự báo.

Ngược lại, một preprocessing method có thể không làm thay đổi đáng kể các thống kê cơ bản của dữ liệu nhưng vẫn cải thiện representation phù hợp với mô hình.

Vì vậy, kết luận về preprocessing phải dựa trên cả **input quality** và **output quality**.

Đây chính là một trong những điểm quan trọng của empirical analysis trong nghiên cứu gốc.

---

## 9. So sánh với Baseline

Baseline được sử dụng làm reference point cho tất cả preprocessing configurations.

Với metric lỗi:

$$
\mathrm{Improvement}_{P}=

\frac{
M_{\mathrm{base}}-M_P
}{
M_{\mathrm{base}}
}
\times100%.
$$

Đối với RMSE:

$$
\mathrm{Improvement}_{\mathrm{RMSE}}=

\frac{
\mathrm{RMSE}_{\mathrm{base}}-

\mathrm{RMSE}*{P}
}{
\mathrm{RMSE}*{\mathrm{base}}
}
\times100%.
$$

Đối với $R^2$:

$$
\Delta R^2=

R_P^2-R_{\mathrm{base}}^2.
$$

Cách biểu diễn tương đối cho phép so sánh các preprocessing methods trên cùng một thang đo và làm rõ mức độ thay đổi so với baseline.

---

## 10. Trade-off giữa Performance và Complexity

Kết quả không được đánh giá chỉ theo metric dự báo.

Một configuration có thể đạt:

$$
\mathrm{RMSE}\downarrow
$$

nhưng đồng thời:

$$
T_{\mathrm{prep}}\uparrow,
\qquad
d'\uparrow.
$$

Ngược lại, feature selection có thể làm:

$$
d'\downarrow,
\qquad
T_{\mathrm{train}}\downarrow,
$$

trong khi prediction performance gần như không thay đổi.

Do đó, hiệu quả thực tế của preprocessing có thể được xem như một bài toán trade-off:

$$
\boxed{
\text{Performance}
\leftrightarrow
\text{Complexity}
\leftrightarrow
\text{Information Preservation}
}
$$

Đây là cơ sở để các kết quả định lượng được sử dụng tiếp trong [10_discussion/02_tradeoffs.md](../10_discussion/02_tradeoffs.md).

---

## 11. Cách trình bày kết quả

Các kết quả định lượng nên được trình bày theo bảng thống nhất:

| Configuration       | MAE ↓ | RMSE ↓ | $R^2$ ↑ | Features | Preprocessing Cost |
| ------------------- | ----: | -----: | ------: | -------: | -----------------: |
| Baseline            |     — |      — |       — |      $d$ |                  — |
| Cleaning            |     — |      — |       — |      $d$ |                  — |
| Transformation      |     — |      — |       — |      $d$ |                  — |
| Feature Engineering |     — |      — |       — |     $d'$ |                  — |
| Feature Selection   |     — |      — |       — |    $d''$ |                  — |

Các dấu `—` được giữ lại khi chưa có số liệu thực nghiệm được xác nhận, thay vì điền giá trị ước lượng.

Đặc biệt, không sử dụng các con số từ một dataset hoặc một bài toán khác để thay thế cho kết quả của empirical setup hiện tại. Điều này đảm bảo tính trung thực và khả năng tái lập của báo cáo.

---

## 12. Diễn giải kết quả

Kết quả được diễn giải theo ba cấp độ.

### Cấp độ 1 — Metric

Xác định configuration nào có:

$$
\mathrm{MAE}\downarrow,
\qquad
\mathrm{RMSE}\downarrow,
\qquad
R^2\uparrow.
$$

### Cấp độ 2 — Data representation

Phân tích configuration đã thay đổi:

* số lượng feature;
* distribution;
* missingness;
* noise;
* temporal structure;
* dimensionality.

### Cấp độ 3 — Trade-off

Đánh giá liệu improvement về prediction có đủ lớn để bù cho:

$$
\text{additional preprocessing cost}
$$

hoặc

$$
\text{information loss}.
$$

Cách phân tích ba cấp độ giúp tránh kết luận đơn giản rằng phương pháp có metric tốt nhất là phương pháp tốt nhất trong mọi điều kiện.

---

## 13. Tổng hợp phát hiện thực nghiệm

Các kết quả được tổng hợp thành quan hệ:

$$
\text{Data Problem}
\rightarrow
\text{Preprocessing}
\rightarrow
\text{Representation Change}
\rightarrow
\text{Performance Change}.
$$

Từ đó, có thể xây dựng ma trận diễn giải:

| Data problem        | Preprocessing            | Expected effect           | Evaluation                       |
| ------------------- | ------------------------ | ------------------------- | -------------------------------- |
| Missing values      | Imputation               | Tăng data completeness    | MAE, RMSE, $R^2$                 |
| Outliers            | Detection / handling     | Giảm anomalous influence  | MAE, RMSE                        |
| Noise               | Smoothing / filtering    | Giảm noise                | RMSE, data quality               |
| Scale difference    | Normalization            | Cân bằng feature scale    | MAE, RMSE                        |
| Skewness            | Transformation           | Thay đổi distribution     | MAE, RMSE                        |
| Temporal dependence | Lag / rolling            | Tăng temporal information | MAE, RMSE, $R^2$                 |
| Redundancy          | Feature selection        | Giảm dimensionality       | Performance + feature count      |
| High dimensionality | Dimensionality reduction | Compact representation    | Performance + explained variance |

Bảng này không được hiểu là mọi preprocessing method đều chắc chắn tạo ra improvement tương ứng. Nó là framework để tổ chức và diễn giải kết quả quan sát được.

---

## 14. Kết luận từ kết quả

Kết quả thực nghiệm cần được hiểu theo quan điểm **data-dependent preprocessing**:

$$
\boxed{
P^{*}=

P^{*}
(\text{Dataset},
\text{Task},
\text{Model})
}
$$

Nói cách khác, preprocessing configuration tối ưu phụ thuộc vào dataset, nhiệm vụ và mô hình sử dụng. Không có cơ sở để khẳng định một kỹ thuật preprocessing luôn vượt trội trên mọi numerical time-series dataset.

Điểm này phù hợp với mục tiêu của bài nghiên cứu gốc: xây dựng một phạm vi có cấu trúc cho preprocessing của numerical time-series data và sử dụng empirical analysis để đánh giá ảnh hưởng của preprocessing đối với data quality và AI performance, thay vì xem preprocessing như một chuỗi thao tác cố định.

Các kết quả định lượng cụ thể từ từng configuration sẽ được sử dụng trong [06_findings.md](06_findings.md) để rút ra các finding chính. Những finding này tiếp tục được đối chiếu với trade-off, khả năng áp dụng và giới hạn của từng nhóm phương pháp trong [Chương 10](../10_discussion/01_comparison.md).
