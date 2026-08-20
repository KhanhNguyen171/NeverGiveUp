# 1.4 Đóng góp của paper

## From Paper

Theo abstract và phần mở đầu, paper có hai hướng đóng góp chính:

1. **Survey có hệ thống:** tổng hợp các kỹ thuật preprocessing cho time-series data, mở rộng từ data cleaning sang normalization, feature selection/reduction, sensor fusion, compression và các hướng liên quan đến edge/IoT.
2. **Empirical analysis:** chuẩn hóa một pipeline trên Air Quality dataset, thay từng kỹ thuật trong các category để đánh giá ảnh hưởng tới dữ liệu và tới mô hình LSTM dự đoán Carbon Monoxide.

## Ý nghĩa phương pháp

Đóng góp thực nghiệm không phải là tạo ra một thuật toán imputation mới. Giá trị của nó là cung cấp bằng chứng rằng lựa chọn preprocessing có thể tạo khác biệt đáng kể ở downstream prediction.

## Không nên hiểu sai

Paper không chứng minh rằng cubic spline, EM, Grubbs, IQR hay LSTM luôn tốt nhất. Đây là các thành phần của thiết kế thực nghiệm trên dataset được chọn. Tính tổng quát sang một domain khác cần được kiểm chứng riêng.

## Cách truy xuất

Khi đọc các chương sau, các claim về taxonomy được gắn **From Paper**; công thức tổng quát hoặc cách cài đặt mở rộng được gắn **Background Knowledge**; nhận xét về trade-off được gắn **Interpretation**. Quy ước này thực hiện yêu cầu traceability trong `working_rule.md`.