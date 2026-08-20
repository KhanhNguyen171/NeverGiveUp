# 9.1 Experimental setup

## From Paper

Mục tiêu empirical analysis là đánh giá preprocessing ở hai tầng: input quality và output quality. Output quality được đo bằng việc huấn luyện LSTM dự đoán nồng độ Carbon Monoxide (CO) trên AirQuality dataset.

Pipeline được chuẩn hóa bằng cách giữ các bước mặc định, rồi thay kỹ thuật ở category đang được đánh giá. Đây là thiết kế controlled comparison: thay một nhóm xử lý trong khi các nhóm còn lại giữ nguyên để giảm biến thiên giữa thí nghiệm.

## Downstream model

Paper dùng LSTM vì đây là recurrent model có memory để xử lý sequential data và long-term dependency. Architecture được mô tả gồm sequence input layer, LSTM layer 200 hidden units, fully connected layer và regression output layer. Optimizer là Adam, initial learning rate $0.005$, tối đa 100 full passes qua dataset. Thực nghiệm chạy bằng MATLAB R2020b.

## Metrics

Mỗi experiment được lặp ít nhất ba lần; paper trình bày average của ba test cuối. Dự đoán và observation được denormalize trước khi báo cáo để metric ở scale CO gốc. Đây là chi tiết quan trọng: so sánh metric sau normalization mà không inverse transform có thể gây khó diễn giải.

## Giới hạn suy luận

LSTM ở đây là evaluator downstream, không phải contribution forecasting mới. Kết quả đo hiệu quả của cả cấu hình preprocessing + LSTM trên dataset này.