# 01. Data Compression

## 1. Khái niệm và vai trò

Trong hệ thống thu thập dữ liệu chuỗi thời gian, đặc biệt đối với các hệ thống cảm biến và Internet of Things (IoT), dữ liệu thường được tạo ra liên tục với tần suất cao. Khi số lượng cảm biến, tốc độ lấy mẫu và thời gian quan sát tăng, dung lượng lưu trữ và chi phí truyền tải dữ liệu cũng tăng tương ứng. Vì vậy, **data compression** là một bước tiền xử lý nhằm biểu diễn dữ liệu bằng một dạng có kích thước nhỏ hơn nhưng vẫn duy trì lượng thông tin cần thiết cho các mục đích phân tích tiếp theo.

Trong phạm vi tiền xử lý chuỗi thời gian, nén dữ liệu không chỉ nhằm giảm dung lượng lưu trữ mà còn có thể giảm băng thông truyền thông, chi phí truyền dữ liệu và tải xử lý của hệ thống trung tâm. Tawakuli et al. xem data compression là một nhóm độc lập trong taxonomy tiền xử lý chuỗi thời gian, bên cạnh các nhóm như data cleaning, transformation và sensor fusion. Nghiên cứu cũng nhấn mạnh khả năng thực hiện một số bước tiền xử lý tại **edge**, qua đó giảm lượng dữ liệu cần truyền về hệ thống trung tâm và hỗ trợ các ứng dụng EdgeAI.

Với một chuỗi thời gian

$$
\mathcal{X}=

\left \{
(t_i,\mathbf{x}_i)
\right \}_{i=1}^{N},
$$

trong đó $t_i$ là timestamp và $\mathbf{x}_i$ là vector quan sát tại thời điểm $t_i$, phép nén có thể được xem như một ánh xạ

$$
\mathcal{C}:
\mathcal{X}
\rightarrow
\mathcal{Z},
$$

với $\mathcal{Z}$ là biểu diễn có kích thước nhỏ hơn $\mathcal{X}$. Quá trình giải nén được mô tả bởi

$$
\hat{\mathcal{X}}=

\mathcal{D}(\mathcal{Z}),
$$

trong đó $\hat{\mathcal{X}}$ là dữ liệu được khôi phục.

Mục tiêu của compression vì vậy không đơn thuần là tối thiểu hóa kích thước dữ liệu mà là cân bằng giữa **compression ratio**, **information preservation**, **computational cost** và **downstream utility**.

---

## 2. Mục tiêu của nén dữ liệu chuỗi thời gian

Một phương pháp nén hiệu quả cần đáp ứng đồng thời một số mục tiêu chính.

### 2.1. Giảm kích thước dữ liệu

Compression ratio có thể được biểu diễn khái quát bởi

$$
CR=

\frac{S_{\mathrm{original}}}
{S_{\mathrm{compressed}}},
$$

trong đó $S_{\mathrm{original}}$ và $S_{\mathrm{compressed}}$ lần lượt là kích thước dữ liệu trước và sau nén.

Giá trị $CR$ càng lớn thì mức độ giảm dung lượng càng cao. Tuy nhiên, một compression ratio lớn không nhất thiết đồng nghĩa với một phương pháp tốt nếu dữ liệu bị mất các đặc trưng quan trọng.

### 2.2. Duy trì thông tin của chuỗi thời gian

Đối với dữ liệu phục vụ machine learning hoặc forecasting, mục tiêu quan trọng không phải lúc nào cũng là khôi phục từng giá trị chính xác tuyệt đối. Điều quan trọng hơn là duy trì các đặc trưng có ý nghĩa đối với tác vụ downstream, chẳng hạn như:

* xu hướng;
* tính mùa vụ;
* biến động;
* quan hệ tương quan;
* các sự kiện bất thường;
* cấu trúc phụ thuộc theo thời gian.

Do đó, một phương pháp nén có sai số tái tạo nhỏ nhưng làm mất anomaly hoặc thay đổi cấu trúc temporal dependency vẫn có thể không phù hợp cho phân tích chuỗi thời gian.

### 2.3. Giảm chi phí truyền tải

Trong IoT và sensor networks, dữ liệu thường được thu thập tại edge nhưng được lưu trữ hoặc phân tích tại cloud/server. Nén trước khi truyền cho phép giảm số byte phải truyền qua mạng.

Có thể mô tả chi phí truyền dữ liệu một cách khái quát:

$$
C_{\mathrm{transmission}}
\propto
S_{\mathrm{data}},
$$

do đó việc giảm $S_{\mathrm{data}}$ có thể trực tiếp làm giảm bandwidth và communication overhead.

Đây là một trong những động lực quan trọng để đưa preprocessing và compression từ hệ thống trung tâm xuống edge. Tawakuli et al. chỉ ra rằng phân phối preprocessing tại edge có thể giảm workload của hệ thống trung tâm, giảm mức tiêu thụ tài nguyên và làm cho việc quản lý data lake hiệu quả hơn.

---

## 3. Hai nguyên lý chính: Lossless và Lossy

Data compression trong chuỗi thời gian có thể được phân thành hai nhóm cơ bản: **lossless compression** và **lossy compression**. Đây cũng là cơ sở tổ chức cho hai mục tiếp theo của chương này.

### 3.1. Lossless compression

Lossless compression bảo đảm dữ liệu sau khi giải nén có thể khôi phục chính xác dữ liệu ban đầu:

$$
\mathcal{D}(\mathcal{C}(\mathcal{X}))=

\mathcal{X}.
$$

Không có thông tin quan sát nào bị loại bỏ. Đặc tính này phù hợp với các ứng dụng yêu cầu tính toàn vẹn dữ liệu, lưu trữ dữ liệu gốc hoặc các trường hợp mà sai số dù nhỏ cũng có thể ảnh hưởng đến kết quả phân tích.

Đổi lại, compression ratio thường bị giới hạn bởi mức độ dư thừa của dữ liệu. Với chuỗi thời gian có giá trị liên tục và nhiều biến động, khả năng nén lossless có thể thấp hơn so với dữ liệu có cấu trúc lặp lại mạnh.

### 3.2. Lossy compression

Lossy compression cho phép dữ liệu sau giải nén khác dữ liệu ban đầu:

$$
\mathcal{D}(\mathcal{C}(\mathcal{X}))=

\hat{\mathcal{X}},
\qquad
\hat{\mathcal{X}}\neq\mathcal{X}.
$$

Một hàm mất mát có thể được sử dụng để định lượng sai số tái tạo:

$$
E(\mathcal{X},\hat{\mathcal{X}})=

\frac{1}{N}
\sum_{i=1}^{N}
d(\mathbf{x}_i,\hat{\mathbf{x}}_i),
$$

với $d(\cdot,\cdot)$ là một hàm khoảng cách hoặc sai số.

Lossy compression có khả năng đạt compression ratio cao hơn bằng cách loại bỏ những thành phần được xem là ít quan trọng. Tuy nhiên, việc lựa chọn ngưỡng sai số hoặc thành phần cần loại bỏ phải phụ thuộc vào mục tiêu sử dụng dữ liệu.

---

## 4. Compression trong pipeline tiền xử lý

Compression không nên được xem là một thao tác độc lập với toàn bộ pipeline. Vị trí của nó trong preprocessing có thể ảnh hưởng trực tiếp đến chất lượng dữ liệu và kết quả của các bước phía sau.

Một pipeline khái quát có thể được biểu diễn như:

$$
\text{Raw Data}
\rightarrow
\text{Cleaning}
\rightarrow
\text{Transformation}
\rightarrow
\text{Compression}
\rightarrow
\text{Feature Engineering}
\rightarrow
\text{AI Model}.
$$

Tuy nhiên, thứ tự thực tế phụ thuộc vào mục đích của hệ thống. Trong hệ thống edge, compression có thể được thực hiện ngay sau khi dữ liệu được thu thập và kiểm tra chất lượng cơ bản:

$$
\text{Sensor}
\rightarrow
\text{Quality Check}
\rightarrow
\text{Compression}
\rightarrow
\text{Transmission}
\rightarrow
\text{Central Processing}.
$$

Điểm quan trọng là **không nên nén một cách mù quáng trước khi xác định thông tin nào cần được bảo toàn**. Ví dụ, nếu dữ liệu được sử dụng để phát hiện anomaly, một phép nén quá mạnh có thể làm biến dạng hoặc loại bỏ chính các điểm bất thường mà mô hình cần phát hiện.

---

## 5. Các tiêu chí đánh giá

Đánh giá một phương pháp compression cần xem xét đồng thời cả hiệu quả nén và tác động đến dữ liệu.

### 5.1. Compression ratio

$$CR = \frac{S_{\mathrm{original}}} {S_{\mathrm{compressed}}}$$

Đây là chỉ số trực tiếp phản ánh mức độ giảm kích thước dữ liệu.

### 5.2. Reconstruction error

Với dữ liệu gốc $\mathcal{X}$ và dữ liệu khôi phục $\hat{\mathcal{X}}$, có thể sử dụng các chỉ số như MAE hoặc RMSE:

$$MAE = \frac{1}{N} \sum_{i=1}^{N} |x_i-\hat{x}_i|$$

và

$$RMSE= \sqrt{ \frac{1}{N} \sum_{i=1}^{N} (x_i-\hat{x}_i)^2}$$

Các chỉ số này đặc biệt quan trọng đối với lossy compression.

### 5.3. Computational overhead

Một phương pháp nén có thể đạt compression ratio cao nhưng yêu cầu quá nhiều tài nguyên tính toán. Điều này đặc biệt bất lợi trên thiết bị edge có CPU, memory và năng lượng hạn chế.

Do đó cần đánh giá:

$$\text{Compression Utility}= f(CR, E, T, R)$$

trong đó:

* $CR$: compression ratio;
* $E$: reconstruction error;
* $T$: computational/time overhead;
* $R$: resource consumption.

Không tồn tại một phương pháp tối ưu cho mọi trường hợp; lựa chọn compression phải phụ thuộc vào yêu cầu của ứng dụng.

---

## 6. Ý nghĩa đối với AI và Edge/IoT

Đối với các hệ thống AI xử lý chuỗi thời gian, compression tạo ra một trade-off giữa **data efficiency** và **information preservation**. Dữ liệu nhỏ hơn giúp giảm chi phí lưu trữ và truyền tải, nhưng compression quá mạnh có thể làm thay đổi phân phối dữ liệu hoặc phá vỡ các temporal patterns quan trọng.

Đặc biệt trong EdgeAI, việc xử lý và nén dữ liệu ngay tại nguồn có thể giảm lượng dữ liệu phải truyền đến cloud. Theo survey của Tawakuli et al., edge preprocessing là một hướng quan trọng để giảm tải hệ thống trung tâm, giảm tiêu thụ tài nguyên và hỗ trợ các hệ thống AI phân tán.

Do đó, compression nên được xem là một **resource-aware preprocessing operation**, thay vì chỉ là kỹ thuật giảm kích thước file.

---

## 7. Kết luận

Data compression là một thành phần quan trọng trong preprocessing chuỗi thời gian, đặc biệt khi dữ liệu được tạo ra liên tục bởi sensor và IoT. Mục tiêu của compression là giảm kích thước dữ liệu và chi phí truyền tải trong khi vẫn bảo toàn thông tin cần thiết cho các tác vụ downstream.

Hai hướng cơ bản là **lossless compression**, bảo toàn chính xác dữ liệu gốc, và **lossy compression**, chấp nhận sai số tái tạo để đạt mức nén cao hơn. Việc lựa chọn giữa hai hướng này phụ thuộc vào yêu cầu về tính toàn vẹn dữ liệu, compression ratio, sai số cho phép và tài nguyên tính toán.

Trong cấu trúc của chương này, phần tiếp theo trình bày chi tiết các phương pháp **lossless compression**, sau đó là **lossy compression** và cuối cùng là các vấn đề triển khai compression trong **Edge/IoT**. Cách phân chia này phù hợp với taxonomy preprocessing được Tawakuli et al. đề xuất cho numerical time-series data.

### Tài liệu tham khảo chính

Tawakuli, A., Havers, B., Gulisano, V., Kaiser, D., & Engel, T. (2025). *Survey: Time-Series Data Preprocessing: A Survey and an Empirical Analysis*. **Journal of Engineering Research, 13**(2), 674–711. DOI: [10.1016/j.jer.2024.02.018](https://doi.org/10.1016/j.jer.2024.02.018).
