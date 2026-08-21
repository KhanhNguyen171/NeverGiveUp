# 03. Lossy Compression

## 1. Khái niệm

**Lossy compression** là nhóm phương pháp nén cho phép loại bỏ một phần thông tin của dữ liệu nhằm đạt được mức giảm kích thước lớn hơn so với lossless compression. Sau khi giải nén, dữ liệu thu được chỉ là một xấp xỉ của dữ liệu ban đầu.

Với chuỗi thời gian

$$
\mathcal{X}=

\left\{
(t_i,\mathbf{x}_i)
\right\}_{i=1}^{N},
$$

quá trình lossy compression có thể được biểu diễn bởi

$$
\mathcal{Z}=

\mathcal{C}(\mathcal{X}),
$$

và

$$
\hat{\mathcal{X}}=

\mathcal{D}(\mathcal{Z}),
$$

trong đó

$$
\hat{\mathcal{X}}
\neq
\mathcal{X}
$$

nói chung.

Khác với lossless compression, mục tiêu của lossy compression không phải là khôi phục chính xác từng giá trị mà là tìm một biểu diễn nhỏ hơn nhưng vẫn bảo toàn **thông tin có ý nghĩa đối với tác vụ downstream**.

Có thể mô hình hóa bài toán compression như một bài toán tối ưu:

$$
\min_{\mathcal{C},\mathcal{D}}
\quad
E(\mathcal{X},\hat{\mathcal{X}})
$$

subject to

$$
S_{\mathrm{compressed}}
\leq
B,
$$

trong đó $E(\cdot)$ là reconstruction error và $B$ là giới hạn kích thước dữ liệu cho phép.

Do đó, lossy compression tạo ra một trade-off cơ bản:

$$
\boxed{
\text{Compression Ratio}
;\longleftrightarrow;
\text{Information Loss}
}
$$

Mức nén càng cao thường đi kèm với mức sai lệch tái tạo càng lớn.

---

## 2. Nguyên lý của lossy compression

Lossy compression thường gồm hai bước:

$$
\mathcal{X}
\xrightarrow{\mathcal{C}}
\mathcal{Z}
\xrightarrow{\mathcal{D}}
\hat{\mathcal{X}}.
$$

Trong bước compression, các thành phần được xem là ít quan trọng hoặc có mức redundancy cao được loại bỏ hoặc biểu diễn với độ chính xác thấp hơn.

Trong bước decompression, dữ liệu được tái tạo từ biểu diễn $\mathcal{Z}$.

Một formulation tổng quát có thể viết:

$$
\mathcal{Z}=

Q(T(\mathcal{X})),
$$

trong đó:

* $T(\cdot)$ là phép biến đổi dữ liệu;
* $Q(\cdot)$ là phép lượng tử hóa hoặc giảm độ chính xác;
* $\mathcal{Z}$ là representation sau compression.

Dữ liệu khôi phục là:

$$
\hat{\mathcal{X}}=

T^{-1}(\mathcal{D}(\mathcal{Z})).
$$

Điểm quan trọng là loss không nhất thiết được phân bố đồng đều trên toàn bộ dữ liệu. Một phương pháp có thể ưu tiên bảo toàn các thành phần quan trọng như trend hoặc các biến động lớn, trong khi cho phép sai số lớn hơn ở những vùng ít quan trọng.

---

## 3. Các hướng tiếp cận chính

Lossy compression cho time series có thể khai thác nhiều loại redundancy khác nhau. Các hướng phổ biến gồm **quantization**, **transform-based compression**, **approximation/summarization** và **model-based compression**.

### 3.1. Quantization

Quantization giảm số lượng mức giá trị có thể biểu diễn bằng cách ánh xạ giá trị liên tục vào một tập mức rời rạc.

Với giá trị $x$, phép lượng tử hóa có thể được biểu diễn:

$$
\hat{x}=

Q(x).
$$

Một dạng đơn giản là uniform quantization:

$$
Q(x)=

\Delta
\cdot
\operatorname{round}
\left(
\frac{x}{\Delta}
\right),
$$

trong đó $\Delta$ là quantization step.

Sai số lượng tử hóa là:

$$
e_q=

x-\hat{x}.
$$

Khi $\Delta$ tăng, số lượng mức biểu diễn giảm và khả năng nén tăng, nhưng reconstruction error cũng tăng.

Đối với sensor data, quantization đặc biệt hữu ích khi độ chính xác tuyệt đối của phép đo không cần thiết cho downstream task. Ví dụ, nếu biến cảm biến chỉ cần độ chính xác đến một ngưỡng nhất định để dự báo, việc lưu toàn bộ precision của giá trị ban đầu có thể tạo ra redundancy không cần thiết.

---

## 4. Transform-based compression

Một hướng tiếp cận khác là chuyển dữ liệu từ miền thời gian sang một representation khác trong đó năng lượng hoặc thông tin được tập trung vào một số lượng nhỏ thành phần.

Với một chuỗi

$$
\mathbf{x}=

[x_1,x_2,\ldots,x_N]^T,
$$

có thể áp dụng một phép biến đổi:

$$
\mathbf{z}=

T\mathbf{x}.
$$

Nếu chỉ một số nhỏ thành phần của $\mathbf{z}$ mang phần lớn thông tin, các thành phần có magnitude nhỏ có thể được loại bỏ hoặc lượng tử hóa mạnh hơn.

Sau compression:

$$
\hat{\mathbf{z}}=

Q(\mathbf{z}),
$$

và dữ liệu được tái tạo bởi:

$$
\hat{\mathbf{x}}=

T^{-1}\hat{\mathbf{z}}.
$$

Một số transform có thể được sử dụng cho time-series compression, chẳng hạn:

* Discrete Fourier Transform (DFT);
* Discrete Cosine Transform (DCT);
* Wavelet Transform.

### 4.1. Fourier-based representation

DFT biểu diễn chuỗi dưới dạng các thành phần tần số:

$$
X_k=

\sum_{n=0}^{N-1}
x_n
e^{-j2\pi kn/N}.
$$

Nếu tín hiệu chủ yếu chứa một số thành phần tần số, các coefficient còn lại có thể có magnitude nhỏ và được loại bỏ hoặc lượng tử hóa.

Cách tiếp cận này phù hợp hơn với các tín hiệu có cấu trúc frequency-domain rõ ràng.

### 4.2. Wavelet-based representation

Wavelet transform biểu diễn dữ liệu ở nhiều mức độ phân giải khác nhau. Điều này đặc biệt hữu ích đối với các chuỗi chứa cả biến động chậm và biến động cục bộ.

Một biểu diễn wavelet có thể được viết khái quát:

$$
\mathbf{x}
\rightarrow
{
\mathbf{a}_J,
\mathbf{d}_J,
\ldots,
\mathbf{d}_1
},
$$

trong đó $\mathbf{a}_J$ là approximation coefficients và $\mathbf{d}_j$ là detail coefficients tại scale $j$.

Các coefficient nhỏ có thể được loại bỏ:

$$
\hat{d}_{j,k}=

\begin{cases}
d_{j,k}, & |d_{j,k}|>\lambda,\\
0, & |d_{j,k}|\leq\lambda.
\end{cases}
$$

Sau đó dữ liệu được tái tạo từ các coefficient còn lại.

---

## 5. Piecewise approximation

Một chiến lược quan trọng đối với time series là thay thế một đoạn dữ liệu bằng một mô hình đơn giản hơn.

Thay vì lưu toàn bộ:

$$
x_t,x_{t+1},\ldots,x_{t+L-1},
$$

có thể xấp xỉ đoạn dữ liệu bởi một hàm:

$$
\hat{x}(t)=

f(t;\boldsymbol{\theta}).
$$

Ví dụ, với piecewise constant approximation:

$$
\hat{x}_t=

\mu,
$$

trong một segment.

Với piecewise linear approximation:

$$
\hat{x}_t=

a t+b.
$$

Một đoạn dài có thể vì vậy được biểu diễn bằng một số nhỏ tham số:

$$
(a,b,t_{\mathrm{start}},t_{\mathrm{end}}).
$$

Đây là cơ chế quan trọng của nhiều phương pháp **time-series approximation** và **data reduction**.

Tuy nhiên, số lượng segment cần thiết phụ thuộc vào độ phức tạp của tín hiệu. Chuỗi càng biến động mạnh thì càng cần nhiều segment để duy trì reconstruction error dưới ngưỡng cho phép.

---

## 6. Model-based compression

Thay vì lưu toàn bộ dữ liệu, model-based compression lưu các tham số của một mô hình có khả năng tái tạo hoặc dự đoán chuỗi.

Giả sử:

$$
x_t=

f(x_{t-1},\ldots,x_{t-p};\boldsymbol{\theta})
+
\epsilon_t.
$$

Nếu mô hình $f$ mô tả tốt chuỗi, dữ liệu có thể được biểu diễn bằng:

$$
\mathcal{Z}=

{
\boldsymbol{\theta},
\text{residual information}
}.
$$

Một ví dụ đơn giản là mô hình autoregressive:

$$
x_t=

c+
\sum_{k=1}^{p}
\phi_kx_{t-k}
+
\epsilon_t.
$$

Thay vì lưu toàn bộ chuỗi với độ phân giải ban đầu, hệ thống có thể lưu mô hình cùng residual hoặc một representation rút gọn.

Ưu điểm của hướng tiếp cận này là có thể đạt compression ratio cao đối với các chuỗi có cấu trúc dự đoán mạnh. Tuy nhiên, hiệu quả phụ thuộc vào khả năng của mô hình trong việc biểu diễn dữ liệu.

---

## 7. Error-bounded compression

Trong nhiều ứng dụng khoa học và IoT, không cần yêu cầu dữ liệu khôi phục giống hoàn toàn dữ liệu gốc. Thay vào đó, có thể đặt một ngưỡng sai số:

$$
|x_i-\hat{x}_i|
\leq
\epsilon,
\qquad
\forall i,
$$

trong đó $\epsilon$ là error bound.

Khi đó bài toán compression trở thành:

$$
\min
S_{\mathrm{compressed}}
$$

subject to

$$
\max_i
|x_i-\hat{x}_i|
\leq
\epsilon.
$$

Đây là formulation quan trọng vì nó biến information loss thành một constraint có thể kiểm soát.

Có thể sử dụng các dạng error bound khác nhau:

### Absolute error

$$
|x_i-\hat{x}_i|
\leq
\epsilon.
$$

### Relative error

$$
\frac{|x_i-\hat{x}_i|}
{|x_i|}
\leq
\epsilon.
$$

### Norm-based error

$$
|\mathbf{x}-\hat{\mathbf{x}}|_2
\leq
\epsilon.
$$

Việc lựa chọn error criterion phải phù hợp với ý nghĩa của biến và downstream application.

---

## 8. Compression và downstream AI

Trong nghiên cứu machine learning, reconstruction error không phải lúc nào cũng là tiêu chí cuối cùng. Điều quan trọng hơn là compression có làm suy giảm hiệu quả của mô hình hay không.

Gọi $f$ là mô hình AI và $M$ là evaluation metric. Khi đó có thể so sánh:

$$
M(f,\mathcal{X})
$$

với

$$
M(f,\hat{\mathcal{X}}).
$$

Nếu

$$
|M(f,\mathcal{X})-M(f,\hat{\mathcal{X}})|
$$

nhỏ, compression có thể được xem là ít ảnh hưởng đến downstream task.

Do đó, một phương pháp lossy compression nên được đánh giá ở **hai tầng**:

1. **Data-level evaluation**: reconstruction error và compression ratio.
2. **Task-level evaluation**: tác động đến forecasting, classification, anomaly detection hoặc các tác vụ AI khác.

Điều này đặc biệt quan trọng đối với time series vì một sai số nhỏ về giá trị có thể gây ra sai lệch lớn tại các điểm quan trọng như peak, change point hoặc anomaly.

---

## 9. Trade-off giữa compression và information loss

Đặc trưng cốt lõi của lossy compression là trade-off:

$$
CR
\uparrow
\quad\Longrightarrow\quad
E_{\mathrm{reconstruction}}
\uparrow
$$

trong nhiều trường hợp.

Có thể biểu diễn mối quan hệ này bằng một bài toán rate-distortion:

$$
\min
D(\mathcal{X},\hat{\mathcal{X}})
$$

subject to

$$
R
\leq
R_{\max},
$$

trong đó:

* $D$ là distortion;
* $R$ là số bit hoặc rate cần thiết để biểu diễn dữ liệu;
* $R_{\max}$ là ngân sách lưu trữ hoặc truyền tải.

Một cách nhìn tương đương là:

$$
\boxed{
\text{Compression}=

\text{Rate}
\leftrightarrow
\text{Distortion}
}
$$

Khi ngân sách truyền tải hoặc lưu trữ bị giới hạn, cần lựa chọn mức distortion có thể chấp nhận được thay vì tối đa hóa compression ratio một cách độc lập.

---

## 10. Ưu điểm và hạn chế

### Ưu điểm

Lossy compression có một số ưu điểm quan trọng:

1. Có thể đạt compression ratio cao hơn lossless compression.
2. Giảm đáng kể storage requirement.
3. Giảm bandwidth khi truyền dữ liệu sensor.
4. Có thể kiểm soát mức sai số thông qua quantization hoặc error bound.
5. Phù hợp với các hệ thống edge/IoT có tài nguyên và bandwidth hạn chế.

### Hạn chế

Tuy nhiên, lossy compression cũng tạo ra các rủi ro:

1. Dữ liệu gốc không thể được khôi phục chính xác.
2. Reconstruction error phụ thuộc vào mức độ nén.
3. Các anomaly hoặc extreme events có thể bị biến dạng.
4. Temporal patterns có thể bị thay đổi.
5. Compression có thể làm suy giảm hiệu năng downstream AI.
6. Việc lựa chọn error bound phụ thuộc vào từng ứng dụng.

Vì vậy, lossy compression chỉ nên được áp dụng khi **mức thông tin bị mất có thể được định lượng và chấp nhận**.

---

## 11. Lossless và lossy trong cùng một pipeline

Hai loại compression không nhất thiết loại trừ nhau. Một pipeline có thể kết hợp nhiều tầng compression.

Ví dụ:

$$
\text{Raw Data}
\rightarrow
\text{Transformation}
\rightarrow
\text{Lossy Reduction}
\rightarrow
\text{Lossless Encoding}
\rightarrow
\text{Transmission}.
$$

Tầng lossy giảm lượng thông tin cần biểu diễn bằng cách loại bỏ các thành phần ít quan trọng, trong khi tầng lossless tiếp tục mã hóa representation còn lại một cách hiệu quả mà không gây thêm mất mát.

Cách tiếp cận này cho phép tách biệt hai mục tiêu:

$$
\text{Lossy stage}
\rightarrow
\text{control distortion},
$$

và

$$
\text{Lossless stage}
\rightarrow
\text{remove remaining redundancy}.
$$

Tuy nhiên, việc kết hợp phải được thiết kế dựa trên downstream task và resource constraints.

---

## 12. Vị trí trong pipeline preprocessing

Trong hệ thống time-series preprocessing, lossy compression có thể được đặt sau các bước làm sạch và biến đổi cơ bản:

$$
\text{Raw Time Series}
\rightarrow
\text{Data Cleaning}
\rightarrow
\text{Transformation}
\rightarrow
\boxed{\text{Lossy Compression}}
\rightarrow
\text{Feature Engineering}
\rightarrow
\text{AI Model}.
$$

Trong hệ thống Edge/IoT, một pipeline khác có thể là:

$$
\text{Sensor}
\rightarrow
\text{Edge Cleaning}
\rightarrow
\text{Lossy Compression}
\rightarrow
\text{Network}
\rightarrow
\text{Cloud/AI}.
$$

Trong trường hợp này, compression ratio càng cao thì lượng dữ liệu truyền càng thấp, nhưng cần bảo đảm rằng distortion vẫn nằm trong giới hạn chấp nhận được của ứng dụng.

Do đó, compression không nên được đánh giá chỉ bằng kích thước dữ liệu sau nén. Một pipeline phù hợp cần đồng thời xem xét:

$$
\boxed{
\text{Compression Ratio}
+
\text{Distortion}
+
\text{Computational Cost}
+
\text{Downstream Performance}
}
$$

---

## 13. Kết luận

Lossy compression giảm kích thước dữ liệu bằng cách chấp nhận một mức mất mát thông tin có kiểm soát. Khác với lossless compression, mục tiêu không phải là bảo toàn từng giá trị mà là duy trì representation đủ tốt cho mục đích phân tích.

Đối với time series, các hướng tiếp cận quan trọng gồm **quantization**, **transform-based compression**, **piecewise approximation**, **model-based compression** và **error-bounded compression**. Điểm chung của chúng là tìm cách loại bỏ hoặc giảm độ chính xác của những thành phần được xem là ít quan trọng.

Trong bối cảnh AI và Edge/IoT, tiêu chí lựa chọn không nên chỉ là:

$$
\max CR,
$$

mà cần tối ưu đồng thời:

$$
\max CR
\quad
\text{subject to}
\quad
D\leq D_{\max},
\quad
\Delta M\leq\Delta M_{\max},
$$

trong đó $D$ là distortion và $\Delta M$ là mức suy giảm của downstream metric.

Như vậy, **lossy compression phù hợp khi hệ thống có giới hạn về storage, bandwidth hoặc năng lượng nhưng vẫn có thể xác định rõ mức thông tin được phép mất**. Đây cũng là cơ sở để chuyển sang mục tiếp theo, trong đó compression được xem xét trong bối cảnh **Edge/IoT**, nơi các ràng buộc về tài nguyên, truyền thông và thời gian xử lý trở nên đặc biệt quan trọng.
