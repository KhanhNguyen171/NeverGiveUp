# 02. Lossless Compression

## 1. Khái niệm

**Lossless compression** là nhóm phương pháp nén dữ liệu trong đó dữ liệu gốc có thể được khôi phục **chính xác hoàn toàn** sau quá trình giải nén. Với chuỗi thời gian, nếu dữ liệu ban đầu được biểu diễn bởi

$$
\mathcal{X}=

\left\{
(t_i,\mathbf{x}_i)
\right\}_{i=1}^{N},
$$

thì một phép nén lossless có thể được mô tả bởi

$$
\mathcal{Z}=

\mathcal{C}(\mathcal{X}),
$$

và phép giải nén phải thỏa mãn:

$$
\mathcal{D}(\mathcal{Z})=

\mathcal{X}.
$$

Trong đó:

* $\mathcal{X}$ là dữ liệu gốc;
* $\mathcal{Z}$ là biểu diễn sau nén;
* $\mathcal{C}(\cdot)$ là hàm nén;
* $\mathcal{D}(\cdot)$ là hàm giải nén.

Điều kiện

$$
\mathcal{D}(\mathcal{C}(\mathcal{X}))=\mathcal{X}
$$

là đặc trưng cốt lõi phân biệt lossless compression với lossy compression.

Trong preprocessing chuỗi thời gian, lossless compression phù hợp khi dữ liệu gốc phải được bảo toàn, chẳng hạn dữ liệu cần lưu trữ lâu dài, dữ liệu dùng cho kiểm toán, hoặc dữ liệu mà sai số do nén có thể ảnh hưởng đến kết quả phân tích.

---

## 2. Nguyên lý khai thác tính dư thừa

Khả năng nén lossless xuất phát từ **redundancy** trong biểu diễn dữ liệu. Nếu một chuỗi chứa các mẫu lặp lại hoặc các giá trị có xác suất xuất hiện không đồng đều, dữ liệu có thể được biểu diễn bằng số bit nhỏ hơn mà không làm mất thông tin.

Xét một chuỗi rời rạc:

$$
\mathcal{S}=

(s_1,s_2,\ldots,s_N).
$$

Nếu các giá trị $s_i$ có xác suất xuất hiện $p(s_i)$, entropy của nguồn dữ liệu được xác định bởi

$$
H(S)=

-\sum_{s\in\mathcal{A}}
p(s)\log_2 p(s),
$$

với $\mathcal{A}$ là tập các giá trị có thể xuất hiện.

Entropy biểu diễn giới hạn lý thuyết về số bit trung bình cần thiết để mã hóa một symbol khi chỉ xét phân phối xác suất của nguồn. Do đó, lossless compression tìm cách tạo ra biểu diễn có độ dài gần với entropy nhưng vẫn bảo đảm khả năng khôi phục chính xác.

Đối với time series, redundancy có thể xuất hiện dưới nhiều dạng:

* **Value redundancy**: các giá trị giống hoặc gần giống nhau;
* **Temporal redundancy**: các quan sát liên tiếp có quan hệ mạnh theo thời gian;
* **Structural redundancy**: dữ liệu chứa các mẫu hoặc cấu trúc lặp lại;
* **Predictive redundancy**: giá trị hiện tại có thể dự đoán từ các giá trị trước đó.

Vì vậy, thay vì mã hóa trực tiếp từng $\mathbf{x}_i$, một hệ thống có thể khai thác quan hệ giữa các quan sát để giảm số lượng bit cần lưu trữ.

---

## 3. Các chiến lược lossless compression

Lossless compression có thể được tổ chức thành một số chiến lược chính dựa trên loại redundancy được khai thác.

### 3.1. Dictionary-based compression

Dictionary-based methods thay thế các chuỗi hoặc mẫu dữ liệu lặp lại bằng các mã ngắn hơn. Một dictionary lưu ánh xạ giữa các pattern và code tương ứng.

Ví dụ, với chuỗi:

$$
\mathcal{S}=

(A,B,C,A,B,C,A,B,C),
$$

thay vì lưu toàn bộ chuỗi, một dictionary có thể biểu diễn pattern

$$
(A,B,C)
\rightarrow
k,
$$

sau đó lưu các lần xuất hiện của $k$.

Các thuật toán thuộc họ Lempel–Ziv là ví dụ tiêu biểu của dictionary-based compression.

Ưu điểm chính là không yêu cầu mô hình xác suất phức tạp và có thể áp dụng cho nhiều loại dữ liệu. Tuy nhiên, hiệu quả phụ thuộc vào mức độ lặp lại của dữ liệu và kích thước dictionary.

---

### 3.2. Entropy coding

Entropy coding khai thác sự khác biệt về xác suất xuất hiện của các symbol. Các symbol xuất hiện thường xuyên được gán code ngắn hơn, trong khi các symbol ít xuất hiện được gán code dài hơn.

Một ví dụ là **Huffman coding**. Nếu một symbol $s$ có xác suất lớn, độ dài code $l(s)$ có thể được làm nhỏ hơn so với symbol có xác suất thấp.

Độ dài mã trung bình là

$$
L
=

\sum_{s\in\mathcal{A}}
p(s)l(s).
$$

Mục tiêu là tối thiểu hóa $L$ trong khi vẫn bảo đảm mã có thể giải mã duy nhất.

Một hướng khác là **arithmetic coding**, trong đó toàn bộ chuỗi được biểu diễn bằng một khoảng số thực dựa trên xác suất của các symbol. Arithmetic coding có khả năng đạt hiệu suất gần giới hạn entropy hơn trong nhiều trường hợp.

Entropy coding thường được sử dụng như một tầng mã hóa cuối cùng sau khi dữ liệu đã được biến đổi thành một biểu diễn có phân phối thuận lợi hơn.

---

## 4. Khai thác tính phụ thuộc theo thời gian

Đối với time series, mã hóa trực tiếp các giá trị thường không tận dụng được temporal dependency. Một chiến lược quan trọng là trước tiên biến đổi dữ liệu thành **prediction residual** hoặc **difference sequence**.

Giả sử

$$
\mathbf{x}_i=

\hat{\mathbf{x}}_i
+
\mathbf{e}_i,
$$

trong đó:

* $\hat{\mathbf{x}}_i$ là giá trị được dự đoán từ các quan sát trước;
* $\mathbf{e}_i$ là prediction error hoặc residual.

Nếu chuỗi có tính liên tục cao, ta thường có

$$
|\mathbf{e}_i|
\ll
|\mathbf{x}_i|.
$$

Residual khi đó có miền giá trị nhỏ hơn và thường có nhiều giá trị lặp lại hoặc phân phối tập trung hơn. Vì vậy, residual có thể được nén hiệu quả hơn dữ liệu gốc.

Một trường hợp đơn giản là **delta encoding**:

$$
\Delta \mathbf{x}_i=

\mathbf{x}*i-\mathbf{x}*{i-1},
\qquad
i=2,\ldots,N.
$$

Nếu

$$
\mathbf{x}*i\approx\mathbf{x}*{i-1},
$$

thì

$$
|\Delta\mathbf{x}_i|
\approx 0.
$$

Khi đó, thay vì mã hóa trực tiếp $\mathbf{x}_i$, hệ thống mã hóa $\mathbf{x}_1$ cùng với các giá trị $\Delta\mathbf{x}_i$.

Quá trình khôi phục được thực hiện bởi

$$
\mathbf{x}_i=

\mathbf{x}_{i-1}
+
\Delta\mathbf{x}_i.
$$

Vì phép biến đổi không loại bỏ thông tin nên delta encoding có thể được sử dụng như một bước tiền xử lý cho lossless compression.

---

## 5. Compression của timestamp

Trong time series, timestamp thường tạo ra một lượng redundancy đáng kể. Nếu dữ liệu được lấy mẫu đều với khoảng thời gian $\Delta t$, ta có:

$$
t_i
=

t_0+i\Delta t.
$$

Do đó không nhất thiết phải lưu toàn bộ timestamp dưới dạng giá trị độc lập. Có thể lưu:

$$
(t_0,\Delta t,N),
$$

từ đó khôi phục toàn bộ dãy:

$$
t_i=t_0+i\Delta t.
$$

Đối với dữ liệu có sampling interval cố định, cách biểu diễn này loại bỏ redundancy trong timestamp mà không làm mất thông tin.

Trong trường hợp sampling không đều, có thể sử dụng delta timestamp:

$$
\Delta t_i=

t_i-t_{i-1}.
$$

Khi đó dữ liệu có thể được biểu diễn bởi:

$$
\mathcal{X}
\rightarrow
\left(
t_1,
\Delta t_2,\ldots,\Delta t_N,
\mathbf{x}_1,\ldots,\mathbf{x}_N
\right).
$$

Đây là một ví dụ quan trọng cho thấy compression có thể được thực hiện trên cả **temporal structure** và **measurement values**.

---

## 6. Đánh giá lossless compression

Vì lossless compression không cho phép sai số tái tạo, tiêu chí đánh giá tập trung chủ yếu vào hiệu quả nén và chi phí thực thi.

### 6.1. Compression ratio

$$
CR
=

\frac{S_{\mathrm{original}}}
{S_{\mathrm{compressed}}}.
$$

Giá trị $CR>1$ cho biết dữ liệu sau nén nhỏ hơn dữ liệu ban đầu.

Có thể biểu diễn phần trăm tiết kiệm dung lượng:

$$
Saving=

\left(
1-
\frac{S_{\mathrm{compressed}}}
{S_{\mathrm{original}}}
\right)
\times100%.
$$

### 6.2. Reconstruction correctness

Đây là điều kiện bắt buộc:

$$
\mathcal{D}(\mathcal{C}(\mathcal{X}))=

\mathcal{X}.
$$

Trong triển khai thực tế, có thể kiểm tra byte-level equality hoặc equality trên toàn bộ cấu trúc dữ liệu sau khi giải nén.

### 6.3. Computational cost

Ngoài compression ratio, cần đánh giá:

* thời gian nén;
* thời gian giải nén;
* memory usage;
* năng lượng tiêu thụ;
* khả năng xử lý streaming.

Đặc biệt với edge/IoT, computational cost có thể trở thành ràng buộc quan trọng hơn compression ratio.

---

## 7. Ưu điểm và hạn chế

Lossless compression có ưu điểm quan trọng nhất là **không làm thay đổi dữ liệu**. Điều này giúp bảo đảm tính toàn vẹn của dataset và tránh đưa thêm reconstruction error vào các bước phân tích phía sau.

Các ưu điểm chính gồm:

1. Khôi phục dữ liệu chính xác.
2. Không làm thay đổi giá trị quan sát.
3. Phù hợp với dữ liệu cần lưu trữ lâu dài.
4. Có thể kết hợp với prediction, delta encoding và entropy coding.
5. Phù hợp với các pipeline yêu cầu reproducibility.

Tuy nhiên, lossless compression cũng có những hạn chế:

1. Compression ratio bị giới hạn bởi redundancy của dữ liệu.
2. Hiệu quả giảm khi dữ liệu có entropy cao.
3. Một số thuật toán yêu cầu bộ nhớ hoặc thời gian xử lý đáng kể.
4. Không thể chủ động loại bỏ thông tin ít quan trọng để đạt mức nén rất cao.

Do đó, khi yêu cầu giảm dữ liệu cực mạnh và một mức sai số nhất định có thể chấp nhận được, lossy compression thường phù hợp hơn.

---

## 8. Vị trí trong taxonomy của preprocessing

Trong taxonomy của nghiên cứu, lossless compression thuộc nhóm **data compression**, nằm sau các thao tác data cleaning và data transformation, đồng thời có mối liên hệ trực tiếp với preprocessing tại edge.

Có thể khái quát mối quan hệ như sau:

$$
\text{Raw Time Series}
\rightarrow
\text{Cleaning}
\rightarrow
\text{Transformation}
\rightarrow
\boxed{\text{Lossless Compression}}
\rightarrow
\text{Storage / Transmission}
\rightarrow
\text{Feature Engineering / AI}.
$$

Điểm khác biệt quan trọng là lossless compression **không thay đổi semantic content của dữ liệu**. Vì vậy, nếu dữ liệu sau đó cần được sử dụng lại cho nhiều tác vụ AI khác nhau, dạng lossless thường an toàn hơn so với việc áp dụng lossy compression ngay từ đầu.

Trong hệ thống IoT, compression có thể được triển khai ngay tại edge:

$$
\text{Sensor}
\rightarrow
\text{Edge Preprocessing}
\rightarrow
\text{Lossless Compression}
\rightarrow
\text{Network}
\rightarrow
\text{Cloud}.
$$

Cách tiếp cận này giúp giảm lượng dữ liệu truyền nhưng vẫn bảo toàn khả năng khôi phục dữ liệu gốc.

---

## 9. Kết luận

Lossless compression khai thác redundancy trong dữ liệu để giảm kích thước biểu diễn mà không làm mất thông tin. Đối với time series, redundancy không chỉ nằm ở các giá trị lặp lại mà còn xuất hiện trong **temporal dependency**, **regular sampling** và **predictability**. Vì vậy, các kỹ thuật như dictionary coding, entropy coding, delta encoding và predictive coding có thể được kết hợp để đạt hiệu quả nén cao hơn.

Đặc điểm quyết định của nhóm phương pháp này là:

$$
\boxed{
\mathcal{D}(\mathcal{C}(\mathcal{X}))=

\mathcal{X}
}
$$

Do đó, compression ratio, reconstruction correctness và computational overhead là ba nhóm tiêu chí chính cần được xem xét. Lossless compression đặc biệt phù hợp với những pipeline mà dữ liệu gốc phải được bảo toàn, trong khi các ứng dụng chấp nhận sai số để đổi lấy compression ratio cao hơn sẽ được xem xét ở mục **03_lossy_compression.md**.
