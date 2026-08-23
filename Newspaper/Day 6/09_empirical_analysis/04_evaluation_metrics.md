# Evaluation Metrics

## 1. Mục tiêu đánh giá

Mục tiêu của bước evaluation là định lượng ảnh hưởng của các phương pháp preprocessing đến hiệu quả của mô hình dự báo trên dữ liệu chuỗi thời gian.

Với một preprocessing pipeline $P$ và mô hình $f_\theta$, dự báo tại thời điểm $t$ được biểu diễn:

$$
\widehat{y}_t=

f_{\theta}
\left(
P(\mathbf{X}_{t-L+1:t})
\right).
$$

Hiệu quả của pipeline không được đánh giá chỉ dựa trên một metric duy nhất. Một preprocessing method có thể làm giảm sai số dự báo nhưng đồng thời làm tăng số chiều dữ liệu, chi phí tính toán hoặc làm mất thông tin của chuỗi. Vì vậy, evaluation được tổ chức theo ba nhóm:

$$
\boxed{
\text{Predictive Performance}
+
\text{Data Representation}
+
\text{Computational Cost}
}
$$

Trong đó, predictive performance là tiêu chí chính để so sánh các configuration.

---

## 2. Nguyên tắc đánh giá

Evaluation tuân theo các nguyên tắc sau:

1. **Giữ nguyên evaluation protocol** giữa các preprocessing configurations.
2. **Validation set** được sử dụng để lựa chọn configuration và hyperparameters.
3. **Test set** chỉ được sử dụng cho đánh giá cuối cùng.
4. Các metric được tính trên **cùng tập quan sát và cùng target**.
5. Nếu preprocessing có biến đổi target, metric cuối cùng phải được tính trên **đơn vị gốc của biến mục tiêu**.
6. Không sử dụng thông tin từ test set để lựa chọn preprocessing method.
7. Đối với time series, thứ tự thời gian được bảo toàn trong quá trình đánh giá.

Do đó, với các configuration $P_1,\ldots,P_K$, kết quả được so sánh dưới cùng một protocol:

$$
P_k
\rightarrow
f_{\theta_k}
\rightarrow
\widehat{\mathbf{y}}_k
\rightarrow
M_k.
$$

---

## 3. Mean Absolute Error

Mean Absolute Error (MAE) đo sai số tuyệt đối trung bình giữa giá trị thực và giá trị dự báo:

$$
\mathrm{MAE}=

\frac{1}{N}
\sum_{i=1}^{N}
\left|
y_i-\widehat{y}_i
\right|.
$$

MAE có cùng đơn vị với biến mục tiêu. Vì vậy, nếu target là mức tiêu thụ năng lượng tính bằng Wh thì:

$$
[\mathrm{MAE}]=

\mathrm{Wh}.
$$

Ưu điểm của MAE là dễ diễn giải và ít nhạy hơn RMSE đối với các sai số cực lớn.

MAE phù hợp để trả lời câu hỏi:

> Trung bình mô hình dự báo sai bao nhiêu đơn vị?

Giá trị càng nhỏ càng tốt:

$$
\boxed{
\mathrm{MAE}\downarrow
}
$$

---

## 4. Root Mean Squared Error

Root Mean Squared Error (RMSE) được định nghĩa:

$$
\mathrm{RMSE}=

\sqrt{
\frac{1}{N}
\sum_{i=1}^{N}
\left(
y_i-\widehat{y}_i
\right)^2
}.
$$

RMSE cũng có cùng đơn vị với target:

$$
[\mathrm{RMSE}]=

[y].
$$

Do sai số được bình phương trước khi lấy trung bình, RMSE phạt mạnh hơn những dự báo có sai số lớn.

Nếu tồn tại một sai số $e_i$ lớn:

$$
e_i=

y_i-\widehat{y}_i,
$$

thì đóng góp của nó vào RMSE tỷ lệ với:

$$
e_i^2.
$$

Do đó, RMSE đặc biệt hữu ích khi các sai số lớn có ý nghĩa thực tế hoặc cần hạn chế các prediction failure nghiêm trọng.

Giá trị càng nhỏ càng tốt:

$$
\boxed{
\mathrm{RMSE}\downarrow
}
$$

Trong thực nghiệm, RMSE được sử dụng làm **primary validation metric** để lựa chọn preprocessing configuration.

---

## 5. Coefficient of Determination

Coefficient of Determination, ký hiệu $R^2$, được định nghĩa:

$$
R^2=

1-
\frac{
\sum_{i=1}^{N}
(y_i-\widehat{y}_i)^2
}{
\sum_{i=1}^{N}
(y_i-\bar{y})^2
},
$$

trong đó:

$$
\bar{y}=

\frac{1}{N}
\sum_{i=1}^{N}y_i.
$$

Tử số là tổng bình phương sai số dự báo:

$$
SS_{\mathrm{res}}=

\sum_{i=1}^{N}
(y_i-\widehat{y}_i)^2,
$$

còn mẫu số là tổng bình phương tổng thể:

$$
SS_{\mathrm{tot}}=

\sum_{i=1}^{N}
(y_i-\bar{y})^2.
$$

Do đó:

$$
R^2=

1-
\frac{SS_{\mathrm{res}}}{SS_{\mathrm{tot}}}.
$$

$R^2$ cho biết mức độ biến thiên của target được mô hình giải thích tương đối so với baseline dựa trên giá trị trung bình.

Giá trị lớn hơn thường cho thấy mô hình có khả năng giải thích tốt hơn:

$$
\boxed{
R^2\uparrow
}
$$

Tuy nhiên, $R^2$ không thay thế MAE hoặc RMSE vì nó không trực tiếp biểu diễn sai số dự báo theo đơn vị của target.

---

## 6. So sánh MAE và RMSE

MAE và RMSE đều đo prediction error nhưng phản ứng khác nhau với outliers.

Đặt:

$$
e_i=

y_i-\widehat{y}_i.
$$

MAE sử dụng:

$$
|e_i|,
$$

trong khi RMSE dựa trên:

$$
e_i^2.
$$

Do đó:

$$
|e_i|
\lt
e_i^2
\quad
\text{với sai số đủ lớn},
$$

khi xét theo mức độ phạt tương đối.

Có thể diễn giải:

| Metric | Đặc điểm                              | Mục tiêu     |
| ------ | ------------------------------------- | ------------ |
| MAE    | Ít nhạy với sai số lớn                | $\downarrow$ |
| RMSE   | Nhạy với sai số lớn                   | $\downarrow$ |
| $R^2$  | Đánh giá mức độ giải thích biến thiên | $\uparrow$   |

Việc sử dụng đồng thời MAE và RMSE giúp phân biệt hai trường hợp:

$$
\text{Low average error}
\neq
\text{Low large-error risk}.
$$

Một preprocessing method có MAE thấp nhưng RMSE cao có thể tạo ra prediction tốt trong phần lớn thời gian nhưng vẫn xuất hiện một số sai số rất lớn.

---

## 7. Metrics cho chất lượng biểu diễn dữ liệu

Predictive performance không phải tiêu chí duy nhất để đánh giá preprocessing.

Một preprocessing method có thể giảm số chiều:

$$
d'
\lt
d,
$$

nhưng nếu làm mất quá nhiều thông tin, prediction performance có thể suy giảm.

Do đó, đối với các phương pháp feature selection và dimensionality reduction, cần theo dõi thêm:

### 7.1. Feature count

Số lượng feature sau preprocessing:

$$
d'
=

|\mathcal{F}'|.
$$

Mức giảm số chiều:

$$
\rho_d=

1-
\frac{d'}{d}.
$$

$\rho_d$ càng lớn nghĩa là số lượng feature được loại bỏ càng nhiều.

---

### 7.2. Explained variance

Đối với PCA, có thể sử dụng explained variance ratio:

$$
EVR_k=

\frac{\sum_{i=1}^{k}\lambda_i}
{\sum_{j=1}^{d}\lambda_j},
$$

trong đó $\lambda_i$ là eigenvalue thứ $i$.

$EVR_k$ biểu diễn tỷ lệ phương sai được giữ lại khi sử dụng $k$ components.

Giá trị càng cao cho thấy representation mới bảo toàn nhiều biến thiên hơn:

$$
\boxed{
EVR\uparrow
}
$$

---

## 8. Metrics cho chi phí tính toán

Preprocessing có thể cải thiện prediction nhưng đồng thời làm tăng computational cost.

Vì vậy, có thể ghi nhận:

* preprocessing time;
* training time;
* inference time;
* memory usage;
* số lượng feature sau preprocessing.

Thời gian preprocessing được biểu diễn:

$$
T_{\mathrm{prep}}= T_{\mathrm{end}}

T_{\mathrm{start}}.
$$

Training time:

$$
T_{\mathrm{train}}= T_{\mathrm{fit,end}}

T_{\mathrm{fit,start}}.
$$

Đối với các phương pháp được triển khai trên hệ thống tài nguyên hạn chế, computational cost có thể trở thành một tiêu chí quan trọng bên cạnh predictive performance.

---

## 9. So sánh tương đối với baseline

Để định lượng mức cải thiện của preprocessing method $P$, metric có thể được so sánh với baseline.

Đối với metric lỗi như MAE hoặc RMSE:

$$
\Delta M_P= M_{\mathrm{base}}

M_P.
$$

Phần trăm cải thiện:

$$
\mathrm{Improvement}(%)=

\frac{
M_{\mathrm{base}}-M_P
}{
M_{\mathrm{base}}
}
\times100.
$$

Giá trị dương thể hiện preprocessing giúp giảm lỗi.

Đối với $R^2$, có thể sử dụng:

$$
\Delta R^2=

R_P^2-R_{\mathrm{base}}^2.
$$

Do đó:

$$
\Delta R^2 \gt 0
$$

cho thấy mức độ giải thích biến thiên được cải thiện so với baseline.

---

## 10. Aggregation

Metric được tính trên toàn bộ prediction–target pairs của tập đánh giá:

$$
\mathcal{P}=

{
(y_i,\widehat{y}_i)
}_{i=1}^{N}.
$$

Không tính metric riêng biệt trên từng batch rồi lấy trung bình đơn giản, vì cách này có thể tạo sai lệch khi các batch có kích thước khác nhau.

Thay vào đó, prediction được ghép lại:

$$
\widehat{\mathbf{y}}=

[
\widehat{y}_1,\ldots,\widehat{y}_N
],
$$

và target tương ứng:

$$
\mathbf{y}=

[
y_1,\ldots,y_N
].
$$

Sau đó MAE, RMSE và $R^2$ được tính một lần trên toàn bộ vector:

$$
M
=

M(\mathbf{y},\widehat{\mathbf{y}}).
$$

Cách aggregation này đảm bảo mỗi observation đóng góp đúng một lần vào metric cuối cùng.

---

## 11. Evaluation trên đơn vị gốc

Nếu target được scale trong quá trình training, prediction phải được inverse-transform trước khi tính metric cuối cùng.

Giả sử:

$$
y'
=

\frac{y-\mu_y}{\sigma_y},
$$

mô hình dự báo:

$$
\widehat{y}'.
$$

Prediction phải được chuyển về đơn vị ban đầu:

$$
\widehat{y}=

\sigma_y\widehat{y}'
+
\mu_y.
$$

Sau đó:

$$
\mathrm{MAE}=

\mathrm{MAE}
(y,\widehat{y}),
$$

$$
\mathrm{RMSE}=

\mathrm{RMSE}
(y,\widehat{y}).
$$

Điều này đảm bảo metric có ý nghĩa thực tế và có thể so sánh giữa các configuration.

---

## 12. Validation và Test Evaluation

Evaluation được thực hiện theo hai giai đoạn.

### Validation

Validation được sử dụng để lựa chọn:

* preprocessing configuration;
* hyperparameters;
* feature subset;
* dimensionality reduction configuration;
* model configuration.

Primary criterion:

$$
P^*
=

\arg\min_P
\mathrm{RMSE}_{\mathrm{val}}(P).
$$

Configuration $P^*$ là configuration được lựa chọn dựa trên validation set.

### Test

Sau khi configuration cuối cùng được cố định, test set được sử dụng để đánh giá khả năng tổng quát hóa:

$$
M_{\mathrm{test}}=

M
\left(
\mathbf{y}_{\mathrm{test}},
\widehat{\mathbf{y}}_{\mathrm{test}}
\right).
$$

Test set không được sử dụng để điều chỉnh preprocessing hoặc hyperparameters.

---

## 13. Evaluation protocol

Toàn bộ evaluation pipeline được tóm tắt:

$$
\boxed{
\begin{aligned}
\mathcal{D}_{\mathrm{train}}
&\rightarrow
\operatorname{fit}(P)
\\
\mathcal{D}_{\mathrm{train}}
&\rightarrow
P
\rightarrow
f_\theta
\\
\mathcal{D}_{\mathrm{val}}
&\rightarrow
P_{\mathrm{train}}
\rightarrow
f_\theta
\rightarrow
\mathrm{RMSE}_{\mathrm{val}}
\\
P^*
&=
\arg\min_P
\mathrm{RMSE}_{\mathrm{val}}
\\
\mathcal{D}_{\mathrm{test}}
&\rightarrow
P^*
\rightarrow
f_{\theta^*}
\rightarrow
{
\mathrm{MAE},
\mathrm{RMSE},
R^2
}.
\end{aligned}
}
$$

Protocol này đảm bảo preprocessing được đánh giá như một thành phần của toàn bộ machine-learning pipeline thay vì đánh giá tách rời khỏi mô hình.

---

## 14. Tiêu chí tổng hợp

Kết quả cuối cùng được phân tích theo ba chiều:

$$
\boxed{
\text{Accuracy}
\quad
\text{vs.}
\quad
\text{Efficiency}
\quad
\text{vs.}
\quad
\text{Information Preservation}
}
$$

Trong đó:

* **Accuracy**: MAE, RMSE và $R^2$;
* **Efficiency**: preprocessing time, training time, inference time và feature count;
* **Information preservation**: explained variance hoặc các chỉ số phù hợp với từng phương pháp.

Do đó, preprocessing method tốt không nhất thiết là phương pháp đạt metric dự báo thấp nhất trong mọi trường hợp. Phương pháp được xem là hiệu quả khi đạt được sự cân bằng hợp lý giữa prediction performance, độ phức tạp và khả năng bảo toàn thông tin.

---

## 15. Liên kết với các phần tiếp theo

Các metric trong mục này là cơ sở để trình bày kết quả định lượng trong [05_results.md](05_results.md).

Kết quả sau đó được tổng hợp thành các phát hiện về:

$$
\text{Preprocessing Method}
\rightarrow
\text{Metric Change}
\rightarrow
\text{Trade-off}
\rightarrow
\text{Finding}.
$$

Các finding này được sử dụng để trả lời câu hỏi nghiên cứu về hiệu quả và điều kiện áp dụng của từng nhóm preprocessing, sau đó được thảo luận sâu hơn trong [Chương 10](../10_discussion/01_comparison.md).

Như vậy, evaluation không chỉ trả lời preprocessing method nào tạo ra prediction tốt hơn, mà còn cung cấp cơ sở định lượng để phân tích **vì sao một phương pháp hiệu quả, chi phí của nó là gì và trong điều kiện nào nên sử dụng phương pháp đó**.
