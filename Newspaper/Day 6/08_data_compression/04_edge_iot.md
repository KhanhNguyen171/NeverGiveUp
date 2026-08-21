# 04. Compression in Edge and IoT Systems

## 1. Bối cảnh Edge/IoT

Trong hệ thống Internet of Things (IoT), dữ liệu thường được tạo ra liên tục từ nhiều sensor với tần suất lấy mẫu cao. Với $M$ sensor, mỗi sensor $m$ tạo ra một tập dữ liệu:

$$
\mathcal{D}^{(m)}=

\left \{
\left(
t_i^{(m)},
\mathbf{x}_i^{(m)}
\right)
\right \}_{i=1}^{N_m},
\qquad
m=1,\ldots,M.
$$

Khi $N_m$ và $M$ tăng, tổng lượng dữ liệu cần truyền và lưu trữ tăng theo:

$$
S_{\mathrm{total}}
\propto
\sum_{m=1}^{M}N_mF_m,
$$

trong đó $F_m$ là số chiều dữ liệu của sensor $m$.

Nếu toàn bộ dữ liệu được truyền trực tiếp từ sensor đến cloud, hệ thống phải chịu đồng thời:

* communication overhead;
* bandwidth consumption;
* storage overhead;
* processing workload;
* energy consumption.

Vì vậy, kiến trúc **Edge Computing** đưa một phần xử lý đến gần nơi dữ liệu được sinh ra. Trong kiến trúc này, compression trở thành một cơ chế quan trọng để giảm dữ liệu trước khi truyền đến tầng cloud hoặc server trung tâm.

---

## 2. Vị trí của compression trong Edge/IoT pipeline

Một pipeline Edge/IoT có thể được mô tả:

$$
\text{Sensor}
\rightarrow
\text{Edge Device}
\rightarrow
\text{Network}
\rightarrow
\text{Cloud}
\rightarrow
\text{AI Application}.
$$

Thay vì truyền toàn bộ dữ liệu:

$$
\mathcal{X}_{\mathrm{raw}}
\rightarrow
\text{Network},
$$

edge device có thể thực hiện:

$$
\mathcal{X}*{\mathrm{raw}}
\rightarrow
\mathcal{X}*{\mathrm{clean}}
\rightarrow
\mathcal{Z}
\rightarrow
\text{Network},
$$

với

$$
|\mathcal{Z}|
\lt
|\mathcal{X}_{\mathrm{clean}}|.
$$

Trong đó $\mathcal{Z}$ là representation sau compression.

Cách tiếp cận này chuyển một phần computational cost từ cloud sang edge để đổi lấy việc giảm communication cost. Vì truyền dữ liệu thường là một thành phần đáng kể của chi phí và năng lượng trong hệ thống IoT, compression tại edge có thể mang lại lợi ích đáng kể.

---

## 3. Edge preprocessing

Trong kiến trúc truyền thống, preprocessing thường được thực hiện tập trung:

$$
\text{Sensor}
\rightarrow
\text{Cloud}
\rightarrow
\text{Preprocessing}
\rightarrow
\text{AI}.
$$

Trong edge computing, một phần preprocessing được thực hiện trước khi dữ liệu được truyền:

$$
\text{Sensor}
\rightarrow
\boxed{\text{Edge Preprocessing}}
\rightarrow
\text{Cloud}
\rightarrow
\text{AI}.
$$

Các thao tác có thể được thực hiện tại edge gồm:

* data validation;
* missing-value handling;
* filtering;
* aggregation;
* transformation;
* feature extraction;
* compression.

Compression trong trường hợp này không phải một thao tác độc lập mà là một thành phần của **distributed preprocessing pipeline**.

Nghiên cứu survey về time-series preprocessing của Tawakuli et al. cũng xem preprocessing tại edge là một hướng quan trọng nhằm giảm workload của hệ thống trung tâm và hỗ trợ xử lý dữ liệu gần nguồn sinh dữ liệu.

---

## 4. Lợi ích của compression tại edge

### 4.1. Giảm bandwidth

Giả sử dữ liệu gốc có kích thước $S_{\mathrm{raw}}$ và dữ liệu sau nén có kích thước $S_{\mathrm{comp}}$.

Compression ratio:

$$
CR
=

\frac{S_{\mathrm{raw}}}
{S_{\mathrm{comp}}}.
$$

Khi $CR>1$, lượng dữ liệu cần truyền giảm theo:

$$
S_{\mathrm{transmitted}}=

\frac{S_{\mathrm{raw}}}{CR}.
$$

Do đó, compression có thể trực tiếp giảm network traffic.

---

### 4.2. Giảm communication cost

Nếu chi phí truyền dữ liệu tỷ lệ với số byte được truyền:

$$
C_{\mathrm{comm}}=

c_{\mathrm{byte}}
S_{\mathrm{transmitted}},
$$

thì sau compression:

$$
C_{\mathrm{comm}}=

c_{\mathrm{byte}}
\frac{S_{\mathrm{raw}}}{CR}.
$$

Với $CR$ càng lớn, communication cost càng giảm.

Điều này đặc biệt có ý nghĩa đối với hệ thống có bandwidth hạn chế hoặc chi phí truyền dữ liệu cao.

---

### 4.3. Giảm storage requirement

Dữ liệu được nén trước khi lưu trữ tại edge hoặc cloud cũng làm giảm storage requirement:

$$
S_{\mathrm{storage}}
\approx
S_{\mathrm{compressed}}.
$$

Đối với các hệ thống sensor hoạt động liên tục trong thời gian dài, lợi ích này có thể tích lũy đáng kể.

---

### 4.4. Giảm workload của hệ thống trung tâm

Nếu edge có thể loại bỏ redundancy trước khi truyền, cloud không cần tiếp nhận và xử lý toàn bộ dữ liệu thô.

Do đó:

$$
\text{Edge computation}
\uparrow
\quad\Longrightarrow\quad
\text{Cloud workload}
\downarrow.
$$

Đây là một trade-off quan trọng của edge preprocessing.

---

## 5. Trade-off giữa computation và communication

Compression tại edge không miễn phí. Edge device phải thực hiện thêm computation để tạo ra compressed representation.

Có thể mô hình hóa tổng chi phí:

$$
C_{\mathrm{total}}=

C_{\mathrm{compression}}
+
C_{\mathrm{transmission}}.
$$

Không nén:

$$
C_{\mathrm{raw}}=

C_{\mathrm{transmission}}^{\mathrm{raw}}.
$$

Có nén:

$$
C_{\mathrm{compressed}}=

C_{\mathrm{compression}}
+
C_{\mathrm{transmission}}^{\mathrm{compressed}}.
$$

Compression chỉ thực sự có lợi khi:

$$
C_{\mathrm{compression}}
+
C_{\mathrm{transmission}}^{\mathrm{compressed}}
<
C_{\mathrm{transmission}}^{\mathrm{raw}}.
$$

Vì vậy, không nên mặc định rằng compression luôn tốt hơn. Nếu thuật toán quá phức tạp, computational overhead tại edge có thể lớn hơn lợi ích thu được từ việc giảm communication.

---

## 6. Năng lượng trong hệ thống IoT

Đối với thiết bị IoT chạy bằng pin, energy consumption là một constraint quan trọng.

Có thể biểu diễn năng lượng tổng quát:

$$
E_{\mathrm{total}}=

E_{\mathrm{compute}}
+
E_{\mathrm{communication}}
+
E_{\mathrm{storage}}.
$$

Compression làm:

$$
E_{\mathrm{compute}}
\uparrow,
$$

nhưng đồng thời có thể làm:

$$
E_{\mathrm{communication}}
\downarrow.
$$

Mục tiêu của compression tại edge là đạt:

$$
\Delta E_{\mathrm{communication}}
\gt
\Delta E_{\mathrm{compute}}.
$$

Do đó, thuật toán compression phù hợp cho IoT không nhất thiết là thuật toán có compression ratio cao nhất, mà là thuật toán đạt được **energy-efficient compression**.

---

## 7. Lựa chọn Lossless hay Lossy tại Edge

Hai nhóm compression có đặc điểm khác nhau trong Edge/IoT.

| Tiêu chí             | Lossless             | Lossy                    |
| -------------------- | -------------------- | ------------------------ |
| Khôi phục dữ liệu    | Chính xác            | Xấp xỉ                   |
| Reconstruction error | $0$                  | $\gt 0$                     |
| Compression ratio    | Thường thấp hơn      | Thường cao hơn           |
| Information loss     | Không                | Có kiểm soát             |
| Computational cost   | Phụ thuộc thuật toán | Phụ thuộc thuật toán     |
| Phù hợp              | Dữ liệu cần toàn vẹn | Dữ liệu chấp nhận sai số |
| Downstream risk      | Thấp hơn             | Cao hơn                  |

Lossless compression phù hợp khi dữ liệu gốc cần được bảo toàn:

$$
\hat{\mathcal{X}}=\mathcal{X}.
$$

Lossy compression phù hợp khi có thể xác định một distortion bound:

$$
D(\mathcal{X},\hat{\mathcal{X}})
\leq
D_{\max}.
$$

Trong thực tế, lựa chọn này phải dựa trên yêu cầu của downstream task thay vì chỉ dựa trên compression ratio.

---

## 8. Compression-aware AI pipeline

Trong các hệ thống EdgeAI, dữ liệu không nhất thiết phải được khôi phục hoàn toàn trước khi đưa vào mô hình.

Một pipeline có thể được thiết kế:

$$
\text{Sensor}
\rightarrow
\text{Compression}
\rightarrow
\text{Transmission}
\rightarrow
\text{AI}.
$$

Hoặc:

$$
\text{Sensor}
\rightarrow
\text{Compression}
\rightarrow
\text{Transmission}
\rightarrow
\text{Decompression}
\rightarrow
\text{AI}.
$$

Pipeline thứ hai phù hợp khi AI model yêu cầu dữ liệu ở representation ban đầu.

Trong trường hợp đó:

$$
\hat{\mathcal{X}}=\mathcal{D}(\mathcal{C}(\mathcal{X}))
$$

sẽ trở thành input cho model.

Một tiêu chí quan trọng là sự thay đổi của downstream performance:

$$
\Delta M= M(\mathcal{X})

M(\hat{\mathcal{X}}).
$$

Compression được xem là phù hợp nếu:

$$
|\Delta M|
\leq
\delta,
$$

với $\delta$ là mức suy giảm hiệu năng có thể chấp nhận.

Điều này cho thấy compression trong hệ thống AI nên được đánh giá theo **task-aware compression**, thay vì chỉ dựa vào reconstruction error.

---

## 9. Compression trong multi-sensor IoT

Trong hệ thống có nhiều sensor, mỗi sensor có thể có:

* sampling rate khác nhau;
* dimensionality khác nhau;
* noise level khác nhau;
* bandwidth requirement khác nhau;
* mức độ quan trọng khác nhau đối với downstream task.

Với:

$$
\mathcal{D}^{(m)}=

\left \{
\left(
t_i^{(m)},
\mathbf{x}_i^{(m)}
\right)
\right \}_{i=1}^{N_m},
$$

có thể áp dụng compression riêng cho từng sensor:

$$
\mathcal{Z}^{(m)}=

\mathcal{C}^{(m)}
\left(
\mathcal{D}^{(m)}
\right).
$$

Điều này cho phép lựa chọn compression strategy phù hợp với đặc tính của từng nguồn dữ liệu.

Sau đó các representation có thể được truyền về hệ thống trung tâm để thực hiện sensor fusion:

$$
\left \{
\mathcal{Z}^{(1)},
\ldots,
\mathcal{Z}^{(M)}
\right \}
\rightarrow
\text{Fusion}.
$$

Tuy nhiên, compression có thể làm thay đổi timestamp, precision hoặc temporal resolution. Vì vậy, compression trong multi-sensor systems cần được thiết kế tương thích với bước **temporal alignment** và **sensor fusion** được trình bày ở chương 7.

---

## 10. Những ràng buộc khi triển khai

Compression tại edge phải thỏa mãn nhiều constraint đồng thời.

### Resource constraint

$$
C_{\mathrm{compute}}
\leq
C_{\mathrm{edge}}.
$$

### Memory constraint

$$
M_{\mathrm{required}}
\leq
M_{\mathrm{available}}.
$$

### Latency constraint

$$
T_{\mathrm{compression}}
+
T_{\mathrm{transmission}}
\leq
T_{\max}.
$$

### Accuracy constraint

Đối với lossy compression:

$$
D
\leq
D_{\max}.
$$

### Energy constraint

$$
E_{\mathrm{total}}
\leq
E_{\max}.
$$

Một phương pháp compression chỉ phù hợp khi đồng thời thỏa mãn các constraint quan trọng của hệ thống.

---

## 11. Nguyên tắc thiết kế

Từ góc nhìn preprocessing pipeline, có thể rút ra một số nguyên tắc.

### Nguyên tắc 1: Compression phải phụ thuộc vào mục tiêu sử dụng

Không nên chọn phương pháp chỉ dựa trên compression ratio. Dữ liệu phục vụ anomaly detection, forecasting và classification có thể có yêu cầu bảo toàn thông tin khác nhau.

### Nguyên tắc 2: Ưu tiên compression có chi phí phù hợp với edge

Thiết bị edge thường có CPU, memory và năng lượng hạn chế. Vì vậy, thuật toán cần cân bằng giữa compression efficiency và computational overhead.

### Nguyên tắc 3: Kiểm soát information loss

Đối với lossy compression, cần xác định trước distortion hoặc error tolerance:

$$
D
\leq
D_{\max}.
$$

### Nguyên tắc 4: Đánh giá downstream task

Nếu dữ liệu được sử dụng cho AI, cần đánh giá cả:

$$
\text{Data Fidelity}
\quad\text{và}\quad
\text{Model Performance}.
$$

### Nguyên tắc 5: Bảo toàn temporal semantics

Compression không nên làm mất hoặc làm sai lệch các thông tin cần thiết cho:

* temporal ordering;
* timestamp;
* sampling interval;
* temporal dependency;
* event boundaries.

Điều này đặc biệt quan trọng đối với time-series forecasting và sensor fusion.

---

## 12. Vị trí trong tổng thể nghiên cứu

Trong taxonomy của nghiên cứu, data compression đóng vai trò giảm **storage and communication burden** sau khi dữ liệu đã được làm sạch và biến đổi.

Có thể khái quát:

$$
\boxed{
\text{Data Cleaning}
\rightarrow
\text{Data Transformation}
\rightarrow
\text{Feature Engineering}
\rightarrow
\text{Feature Selection}
\rightarrow
\text{Compression}
\rightarrow
\text{AI-ready Data}
}
$$

Trong khi đó, đối với hệ thống IoT phân tán:

$$
\boxed{
\text{Sensors}
\rightarrow
\text{Edge Preprocessing}
\rightarrow
\text{Compression}
\rightarrow
\text{Communication}
\rightarrow
\text{Central/Cloud AI}
}
$$

Hai góc nhìn này bổ sung cho nhau. Góc nhìn thứ nhất tập trung vào **data preprocessing**, còn góc nhìn thứ hai tập trung vào **system-level efficiency**.

Do đó, compression là điểm giao giữa preprocessing và system optimization.

---

## 13. Kết luận

Trong Edge/IoT, compression không chỉ là kỹ thuật giảm kích thước dữ liệu mà là một cơ chế để tối ưu toàn bộ pipeline thu thập, truyền tải, lưu trữ và phân tích dữ liệu.

Lợi ích chính có thể được khái quát:

$$
\text{Compression}
\rightarrow
\begin{cases}
\downarrow\ \text{Bandwidth}\
\downarrow\ \text{Storage}\
\downarrow\ \text{Communication Cost}\
\downarrow\ \text{Cloud Workload}
\end{cases}
$$

nhưng đồng thời tạo ra chi phí:

$$
\text{Compression}
\rightarrow
\begin{cases}
\uparrow\ \text{Edge Computation}\
\uparrow\ \text{Processing Latency}\
\uparrow\ \text{Energy Consumption}\
\text{Potential Information Loss}
\end{cases}
$$

Vì vậy, bài toán thực tế không phải là tối đa hóa compression ratio mà là tìm một điểm cân bằng giữa **data fidelity, compression efficiency, computational cost, communication cost và downstream performance**.

Trong toàn bộ chương 8, ba lớp nội dung được liên kết theo thứ tự:

$$
\text{Compression}
\rightarrow
\text{Lossless}
\rightarrow
\text{Lossy}
\rightarrow
\text{Edge/IoT}.
$$

Trong đó, hai mục giữa tập trung vào cơ chế và đặc tính của từng loại compression, còn mục này đặt compression vào bối cảnh triển khai thực tế, nơi giới hạn về tài nguyên, bandwidth, latency và energy quyết định phương pháp nào thực sự phù hợp.
