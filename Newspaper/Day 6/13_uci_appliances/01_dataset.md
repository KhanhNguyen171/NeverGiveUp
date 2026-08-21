# 01. UCI Appliances Energy Prediction Dataset

## 1. Dataset Overview

Nghiên cứu thực nghiệm trong chương này sử dụng **Appliances Energy Prediction Dataset**, một bộ dữ liệu chuỗi thời gian đa biến được xây dựng từ dữ liệu thực nghiệm trong một ngôi nhà có mức tiêu thụ năng lượng thấp. Bộ dữ liệu được công bố trên **UCI Machine Learning Repository** và được thiết kế cho bài toán hồi quy nhằm dự đoán mức tiêu thụ năng lượng của các thiết bị trong nhà.

Dữ liệu gồm **19,735 quan sát**, được ghi nhận với chu kỳ **10 phút**, trong khoảng thời gian xấp xỉ **4.5 tháng**. Do đó, dữ liệu không chỉ có đặc trưng hồi quy thông thường mà còn chứa cấu trúc phụ thuộc theo thời gian, khiến nó phù hợp để nghiên cứu các bước tiền xử lý dành cho dữ liệu chuỗi thời gian, bao gồm làm sạch dữ liệu, biến đổi, xây dựng đặc trưng theo thời gian và tạo các cửa sổ quan sát cho dự báo.

Trong nghiên cứu này, bộ dữ liệu được xem như một trường hợp thực nghiệm để kiểm chứng pipeline tiền xử lý được trình bày ở các chương trước. Mục tiêu không phải chỉ đạt độ chính xác dự báo cao, mà là đánh giá cách các phương pháp **data preprocessing** được lựa chọn, kết hợp và kiểm soát khi áp dụng lên dữ liệu năng lượng có cấu trúc thời gian.

---

## 2. Nguồn và phương pháp thu thập dữ liệu

Dữ liệu được thu thập từ một ngôi nhà có mức tiêu thụ năng lượng thấp. Các điều kiện nhiệt độ và độ ẩm trong nhà được giám sát bằng mạng cảm biến không dây **ZigBee**. Các nút cảm biến ban đầu truyền dữ liệu với chu kỳ khoảng 3.3 phút, sau đó dữ liệu được tổng hợp thành các khoảng thời gian 10 phút. Mức tiêu thụ năng lượng được ghi nhận với cùng độ phân giải thời gian bằng các công tơ năng lượng m-bus.

Bên cạnh dữ liệu cảm biến trong nhà, nghiên cứu còn sử dụng dữ liệu thời tiết từ trạm khí tượng **Chievres Airport, Belgium**. Các biến thời tiết được ghép với dữ liệu trong nhà thông qua trường thời gian. Một số dữ liệu thời tiết có độ phân giải theo giờ và được nội suy để phù hợp với chu kỳ 10 phút của tập dữ liệu chính.

Cách xây dựng này tạo ra một tập dữ liệu có nhiều nguồn thông tin:

* **Năng lượng:** mức tiêu thụ của thiết bị và đèn;
* **Môi trường trong nhà:** nhiệt độ và độ ẩm tại nhiều khu vực;
* **Môi trường bên ngoài:** nhiệt độ, độ ẩm, áp suất, tốc độ gió, tầm nhìn và điểm sương;
* **Thời gian:** timestamp cho phép khai thác các quy luật chu kỳ;
* **Biến kiểm soát:** `rv1` và `rv2`, được đưa vào nhằm kiểm tra khả năng loại bỏ các thuộc tính không có tính dự báo.

---

## 3. Cấu trúc dữ liệu

Bộ dữ liệu UCI được mô tả là **multivariate time series** và phục vụ bài toán **regression**. Phiên bản dữ liệu được cung cấp trên UCI gồm trường thời gian `date`, biến mục tiêu `Appliances` và các biến giải thích liên quan đến năng lượng, môi trường trong nhà và thời tiết bên ngoài.

Biến mục tiêu của nghiên cứu là:

$$y_t = \mathrm{Appliances}_td$$

trong đó $y_t$ biểu diễn năng lượng tiêu thụ của các thiết bị tại thời điểm $t$, được đo bằng **Wh**.

Các nhóm biến chính có thể được tổ chức như sau:

| Nhóm    | Biến tiêu biểu                                        | Ý nghĩa                                                      |
| ------- | ----------------------------------------------------- | ------------------------------------------------------------ |
| Time    | `date`                                                | Thời điểm quan sát                                           |
| Target  | `Appliances`                                          | Năng lượng thiết bị, Wh                                      |
| Energy  | `lights`                                              | Năng lượng sử dụng cho hệ thống chiếu sáng                   |
| Indoor  | `T1`--`T9`, `RH_1`--`RH_9`                            | Nhiệt độ và độ ẩm tại các khu vực trong nhà                  |
| Outdoor | `T_out`, `RH_out`                                     | Nhiệt độ và độ ẩm bên ngoài                                  |
| Weather | `Press_mm_hg`, `Windspeed`, `Visibility`, `Tdewpoint` | Điều kiện thời tiết                                          |
| Control | `rv1`, `rv2`                                          | Hai biến ngẫu nhiên dùng để kiểm tra thuộc tính không dự báo |

UCI ghi nhận rằng các biến quan sát không có giá trị thiếu trong phiên bản dataset được công bố.

---

## 4. Đặc điểm phù hợp với nghiên cứu tiền xử lý

Điểm quan trọng của dataset không nằm ở kích thước dữ liệu mà ở **cấu trúc phụ thuộc thời gian và tính dị biệt giữa các nhóm biến**.

Thứ nhất, các quan sát được lấy mẫu theo chu kỳ 10 phút:

$$\Delta t = 10\ \mathrm{minutes}$$

Do đó, thứ tự thời gian phải được bảo toàn khi thực hiện chia dữ liệu, xây dựng cửa sổ và đánh giá mô hình. Việc sử dụng random split có thể làm thông tin từ tương lai xuất hiện trong tập huấn luyện, dẫn đến đánh giá không phản ánh đúng bài toán dự báo thực tế.

Thứ hai, các biến có miền giá trị và đơn vị rất khác nhau. Chẳng hạn, nhiệt độ được biểu diễn bằng $^{\circ}\mathrm{C}$, độ ẩm bằng (%), áp suất bằng mm Hg và tốc độ gió bằng m/s. Sự khác biệt về scale này tạo động lực cho bước **scaling** được trình bày trong `04_data_transformation/01_scaling_normalization.md`.

Thứ ba, dataset kết hợp các biến liên tục, biến thời gian và biến ngẫu nhiên. Vì vậy, quá trình tiền xử lý không nên được xem đơn thuần là quá trình biến đổi từng cột độc lập mà cần xem xét **vai trò và ý nghĩa của từng nhóm đặc trưng**.

---

## 5. Biểu diễn bài toán dự báo

Trong nghiên cứu này, dataset được chuyển từ dạng bảng quan sát sang bài toán **sequence-to-one forecasting**.

Với lookback $L$ và horizon $H$, dữ liệu đầu vào được biểu diễn:

$$
\mathbf{X}_{t-L+1:t}
=
\left[
\mathbf{x}_{t-L+1},
\ldots,
\mathbf{x}_{t}
\right]
$$

và mục tiêu:

$$y_{t+H}=

\mathrm{Appliances}_{t+H}.$$

Thiết kế thực nghiệm sử dụng:

$$H=1,d$$

tức dự báo mức tiêu thụ năng lượng **10 phút tiếp theo**. Ba độ dài cửa sổ được xem xét là:

$$L \in {36,72,144}$$

tương ứng với:

* $L=36$: lịch sử 6 giờ;
* $L=72$: lịch sử 12 giờ;
* $L=144$: lịch sử 24 giờ.

Do đó, bài toán có dạng:

$$\boxed{
\mathbf{X}*{t-L+1:t}
\rightarrow
\mathrm{Appliances}*{t+1}
}$$

với mỗi mẫu đầu vào chứa thông tin lịch sử của một khoảng thời gian liên tục.

Cách biểu diễn này là cầu nối trực tiếp giữa dataset gốc và các bước **temporal features**, **lag features**, **rolling features**, **scaling** và **window construction** được trình bày ở các chương trước.

---

## 6. Vai trò của dataset trong nghiên cứu

Dataset được sử dụng như một **case study thực nghiệm** để đánh giá toàn bộ quy trình từ dữ liệu thô đến dữ liệu sẵn sàng cho mô hình AI.

Cụ thể, chương 13 sử dụng dataset để kiểm chứng ba vấn đề chính:

1. **Data quality:** xác định và xử lý các vấn đề liên quan đến timestamp, tính liên tục và chất lượng quan sát.
2. **Representation:** chuyển dữ liệu dạng bảng thành biểu diễn phù hợp với bài toán chuỗi thời gian thông qua các đặc trưng thời gian, lag, rolling và cửa sổ quan sát.
3. **AI readiness:** tạo dữ liệu có cấu trúc, scale và split phù hợp để đưa vào mô hình học máy hoặc deep learning mà không làm rò rỉ thông tin từ tương lai.

Vì vậy, dataset không được xem như một phần độc lập với survey. Nó đóng vai trò **thực nghiệm kiểm chứng** cho taxonomy và pipeline tiền xử lý được xây dựng từ Chương 3 đến Chương 11.

---

## 7. Tóm tắt

**Appliances Energy Prediction Dataset** là một bộ dữ liệu chuỗi thời gian đa biến gồm 19,735 quan sát với độ phân giải 10 phút, kết hợp mức tiêu thụ năng lượng, các phép đo môi trường trong nhà và dữ liệu thời tiết bên ngoài.

Đặc điểm quan trọng nhất của dataset đối với nghiên cứu này là sự tồn tại đồng thời của **temporal dependency**, **heterogeneous feature scales**, **multisource measurements** và **nhiều nhóm đặc trưng có vai trò khác nhau**. Những đặc điểm này khiến dataset trở thành một trường hợp phù hợp để đánh giá một pipeline preprocessing có kiểm soát thay vì chỉ áp dụng các phép biến đổi độc lập trên từng cột.

Trong các mục tiếp theo của Chương 13, dataset này sẽ được sử dụng để trình bày cách áp dụng các nguyên tắc tiền xử lý đã khảo sát trong nghiên cứu, từ **data cleaning**, **transformation**, **feature engineering** đến việc xây dựng dữ liệu cuối cùng cho mô hình dự báo.
