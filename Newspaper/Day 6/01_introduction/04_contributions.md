# 1.4. Đóng góp của nghiên cứu

Dựa trên bối cảnh được trình bày ở Mục `01_background.md`, các vấn đề được xác định ở Mục `02_problem.md` và những động lực nghiên cứu ở Mục `03_motivation.md`, nghiên cứu này tập trung vào việc **hệ thống hóa, phân loại, phân tích và kiểm chứng các phương pháp preprocessing cho dữ liệu chuỗi thời gian**, với mục tiêu xây dựng một cơ sở có cấu trúc để lựa chọn phương pháp phù hợp cho các hệ thống AI.

Các đóng góp chính của nghiên cứu được tổ chức thành các nhóm sau.

## 1.4.1. Xây dựng taxonomy cho time-series data preprocessing

Nghiên cứu xây dựng một taxonomy có cấu trúc để tổ chức các kỹ thuật preprocessing theo chức năng và mục tiêu xử lý.

Taxonomy bao gồm các nhóm chính:

$$
\mathcal{P}=

{
\mathcal{C},
\mathcal{T},
\mathcal{F},
\mathcal{S},
\mathcal{U},
\mathcal{K}
},
$$

trong đó:

* $\mathcal{C}$: **Data Cleaning**;
* $\mathcal{T}$: **Data Transformation**;
* $\mathcal{F}$: **Feature Engineering**;
* $\mathcal{S}$: **Feature Selection**;
* $\mathcal{U}$: **Sensor Fusion**;
* $\mathcal{K}$: **Data Compression**.

Cấu trúc này được sử dụng làm khung tổ chức cho các Chương 3--8, giúp duy trì sự nhất quán giữa việc mô tả phương pháp, phân tích ưu nhược điểm và đánh giá khả năng áp dụng.

---

## 1.4.2. Phân tích các phương pháp theo vấn đề dữ liệu và mục tiêu xử lý

Thay vì chỉ mô tả thuật toán, nghiên cứu phân tích mỗi nhóm preprocessing dựa trên mối quan hệ:

$$
\text{Data Problem}
\rightarrow
\text{Preprocessing Method}
\rightarrow
\text{Data Effect}
\rightarrow
\text{Downstream Impact}.
$$

Cách tiếp cận này cho phép xác định:

* vấn đề dữ liệu mà phương pháp giải quyết;
* nguyên lý hoạt động của phương pháp;
* điều kiện mà phương pháp phù hợp;
* tác động lên cấu trúc và phân phối dữ liệu;
* chi phí tính toán;
* nguy cơ làm mất thông tin;
* khả năng ảnh hưởng đến mô hình downstream.

Nhờ đó, preprocessing được xem như một quá trình ra quyết định thay vì một danh sách các kỹ thuật độc lập.

---

## 1.4.3. Hệ thống hóa các trade-off trong preprocessing

Nghiên cứu xác định rằng lựa chọn preprocessing luôn tồn tại các trade-off giữa chất lượng dữ liệu, lượng thông tin được bảo toàn và chi phí tính toán.

Một cách khái quát, mục tiêu của preprocessing có thể được biểu diễn:

$$\max_{\mathcal{P}} \quad Q_{\mathrm{data}} + \lambda Q_{\mathrm{downstream}}- \alpha C_{\mathrm{compute}} \beta L_{\mathrm{information}}$$

trong đó:

* $Q_{\mathrm{data}}$ biểu diễn chất lượng dữ liệu;
* $Q_{\mathrm{downstream}}$ biểu diễn tác động tích cực đến nhiệm vụ downstream;
* $C_{\mathrm{compute}}$ biểu diễn computational cost;
* $L_{\mathrm{information}}$ biểu diễn information loss;
* $\lambda$, $\alpha$ và $\beta$ là các trọng số phụ thuộc vào bài toán.

Biểu thức trên không được sử dụng như một objective function thực nghiệm duy nhất mà đóng vai trò mô hình hóa khái niệm cho quá trình lựa chọn phương pháp.

Các trade-off này được phân tích tổng hợp ở Chương 10.

---

## 1.4.4. Xây dựng nguyên tắc preprocessing bảo toàn temporal integrity

Nghiên cứu nhấn mạnh rằng preprocessing time series phải bảo toàn thông tin về thứ tự và quan hệ thời gian.

Đối với bài toán forecasting:

$$X_{t-L+1:t} \rightarrow Y_{t+H}$$

các phép biến đổi phải đảm bảo rằng dữ liệu được sử dụng để xây dựng $X_{t-L+1:t}$ không chứa thông tin từ thời điểm sau $t$.

Từ nguyên tắc này, nghiên cứu đưa ra yêu cầu kiểm soát:

* temporal ordering;
* timestamp consistency;
* missing temporal intervals;
* lag construction;
* rolling-window construction;
* train/validation/test boundaries;
* preprocessing parameters.

Nguyên tắc này trở thành một tiêu chí xuyên suốt khi xây dựng pipeline ở Chương 11 và khi triển khai trường hợp UCI Appliances ở Chương 13.

---

## 1.4.5. Hệ thống hóa nguyên tắc chống data leakage

Một đóng góp phương pháp luận quan trọng là đưa **data leakage prevention** thành một yêu cầu xuyên suốt của preprocessing pipeline.

Với tập huấn luyện $D_{\mathrm{train}}$, tham số preprocessing được xác định:

$$\theta_{\mathrm{prep}}= \operatorname{Fit}(D_{\mathrm{train}})$$

Sau đó, cùng tham số này được sử dụng để biến đổi các tập dữ liệu còn lại:

$$D_i'= \operatorname{Transform} (D_i;\theta_{\mathrm{prep}}), \qquad i\in{\mathrm{val},\mathrm{test}}.$$

Nguyên tắc này được áp dụng đặc biệt cho các phương pháp có bước học tham số từ dữ liệu như scaling, normalization, imputation, feature selection và các phép biến đổi thống kê.

Qua đó, nghiên cứu phân biệt rõ giữa:

$$
\text{Preprocessing}
\neq
\text{Information Leakage}.
$$

Một preprocessing method chỉ được xem là hợp lệ trong pipeline thực nghiệm khi cách áp dụng nó không sử dụng thông tin mà mô hình không thể biết tại thời điểm dự báo.

---

## 1.4.6. Xây dựng preprocessing pipeline từ dữ liệu thô đến AI-ready data

Từ taxonomy và các nguyên tắc đã phân tích, nghiên cứu xây dựng một pipeline khái quát:

$$
X_{\mathrm{raw}}
\rightarrow
\mathcal{C}
\rightarrow
\mathcal{T}
\rightarrow
\mathcal{F}
\rightarrow
\mathcal{S}
\rightarrow
X_{\mathrm{AI}}.
$$

Trong những hệ thống có nhiều nguồn dữ liệu hoặc giới hạn tài nguyên, pipeline có thể mở rộng:

$$
X_{\mathrm{raw}}
\rightarrow
\mathcal{C}
\rightarrow
\mathcal{T}
\rightarrow
\mathcal{F}
\rightarrow
\mathcal{S}
\rightarrow
\mathcal{U}
\rightarrow
\mathcal{K}
\rightarrow
X_{\mathrm{AI}}.
$$

Pipeline được trình bày ở Chương 11 không nhằm áp đặt một thứ tự cố định cho mọi bài toán. Thay vào đó, nó cung cấp một framework để xác định bước nào cần thiết, bước nào có thể bỏ qua và thứ tự nào phù hợp với đặc tính của dữ liệu.

---

## 1.4.7. Đánh giá thực nghiệm tác động của preprocessing

Nghiên cứu không chỉ dừng ở tổng hợp lý thuyết mà còn xây dựng một experimental framework để đánh giá tác động của preprocessing đối với dữ liệu và mô hình downstream.

Quy trình đánh giá tổng quát:

$$
X_{\mathrm{raw}}
\xrightarrow{\mathcal{P}_i}
X_i
\xrightarrow{\mathcal{M}}
\hat{Y}_i
\rightarrow
\mathcal{E}_i,
$$

trong đó:

* $\mathcal{P}_i$ là preprocessing configuration thứ $i$;
* $X_i$ là dữ liệu sau preprocessing;
* $\mathcal{M}$ là mô hình downstream;
* $\hat{Y}_i$ là dự đoán;
* $\mathcal{E}_i$ là kết quả đánh giá.

Chương 9 sử dụng framework này để so sánh các cấu hình preprocessing dựa trên các tiêu chí phù hợp, thay vì đánh giá phương pháp chỉ dựa trên đặc tính lý thuyết.

---

## 1.4.8. Kết nối khảo sát lý thuyết với bộ dữ liệu UCI Appliances Energy Prediction

Nghiên cứu sử dụng **UCI Appliances Energy Prediction** như một case study để kết nối taxonomy lý thuyết với một pipeline preprocessing thực tế.

Case study được sử dụng để minh họa quá trình:

$$
\text{Raw Sensor Data}
\rightarrow
\text{Cleaning}
\rightarrow
\text{Transformation}
\rightarrow
\text{Feature Engineering}
\rightarrow
\text{Feature Selection}
\rightarrow
\text{AI-ready Time Series}.
$$

Việc lựa chọn case study này cho phép kiểm tra các nguyên tắc đã trình bày trong các chương trước trên dữ liệu cảm biến năng lượng có cấu trúc thời gian và nhiều biến ngoại sinh.

Chi tiết về dataset, preprocessing và feature engineering được trình bày ở Chương 13, trong khi kết quả thực nghiệm tương ứng được liên kết với framework đánh giá ở Chương 9.

---

## 1.4.9. Đề xuất nguyên tắc lựa chọn phương pháp preprocessing

Cuối cùng, nghiên cứu tổng hợp các phân tích thành một tập nguyên tắc hỗ trợ lựa chọn preprocessing method.

Quá trình lựa chọn được định hướng bởi:

$$
\text{Method Selection}=

f(
\text{Data Characteristics},
\text{Task},
\text{Constraints},
\text{Downstream Model}
).
$$

Trong đó cần xem xét:

1. **Đặc tính dữ liệu:** missingness, noise, outliers, distribution, stationarity và temporal dependency.
2. **Mục tiêu bài toán:** forecasting, classification, regression hoặc anomaly detection.
3. **Đặc tính mô hình:** độ nhạy với scale, dimensionality và distribution.
4. **Ràng buộc hệ thống:** computation, memory, storage, bandwidth và latency.
5. **Yêu cầu thông tin:** mức độ cần bảo toàn temporal structure và domain-specific signals.
6. **Tính hợp lệ thực nghiệm:** tránh data leakage và đảm bảo preprocessing được áp dụng nhất quán giữa các tập dữ liệu.

Các nguyên tắc này được tổng hợp trong Chương 12 dưới dạng những bài học và quy tắc lựa chọn phương pháp, đồng thời được minh họa bằng pipeline UCI Appliances ở Chương 13.

---

## 1.4.10. Phạm vi đóng góp

Các đóng góp của nghiên cứu tập trung vào **hệ thống hóa và phân tích phương pháp preprocessing**, không nhằm đề xuất một thuật toán AI mới hoặc một mô hình forecasting mới. Trọng tâm nằm ở lớp dữ liệu trước mô hình:

$$
\boxed{
\text{Raw Data}
\rightarrow
\text{Preprocessing}
\rightarrow
\text{AI-ready Data}
}
$$

Do đó, giá trị chính của nghiên cứu là cung cấp một cách tiếp cận có cấu trúc để:

* hiểu các vấn đề thường gặp của time-series data;
* lựa chọn preprocessing method theo đặc tính dữ liệu;
* kiểm soát temporal integrity và data leakage;
* phân tích trade-off giữa data quality, information preservation và computational cost;
* xây dựng preprocessing pipeline có khả năng tái sử dụng;
* và kiểm chứng các nguyên tắc trên một case study thực tế.

Các đóng góp này tạo thành cầu nối giữa **khảo sát lý thuyết** ở Chương 2--8, **đánh giá thực nghiệm** ở Chương 9, **phân tích và tổng hợp** ở Chương 10--12 và **case study UCI Appliances Energy Prediction** ở Chương 13. Vì vậy, Mục `01_background.md` → `02_problem.md` → `03_motivation.md` → `04_contributions.md` hoàn thành phần cơ sở của Chương 1 và tạo tiền đề trực tiếp cho việc xác định **research scope và taxonomy** trong Chương 2.
