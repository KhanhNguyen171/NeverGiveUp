# 1.3 Motivation và research gap

## From Paper

Động lực trung tâm của paper là thiếu một cái nhìn hợp nhất về preprocessing cho time series. Nghiên cứu về missing data, outlier, feature selection hoặc compression thường giải quyết từng vấn đề riêng. Trong hệ thống IoT, các vấn đề này lại xuất hiện cùng nhau và ảnh hưởng đồng thời tới lưu trữ, truyền dữ liệu và mô hình AI.

## Phân tích logic

Nếu chỉ xử lý một lớp lỗi, pipeline có thể vẫn thất bại:

```text
Chỉ impute missing
      ↓
Outlier còn tồn tại
      ↓
Statistics và model bị lệch
```

Ngược lại, xử lý quá mạnh cũng nguy hiểm:

```text
Aggressive smoothing / deletion
      ↓
Peak và anomaly thật bị mất
      ↓
Model học tín hiệu sai
```

Do đó cần một survey trả lời đồng thời: phương pháp giải quyết vấn đề gì, yêu cầu giả định nào, tốn tài nguyên ra sao và nên đánh giá bằng tiêu chí nào.

## Phân biệt claim

- **Paper states:** preprocessing bao phủ nhiều thách thức chất lượng dữ liệu, không giới hạn ở data cleaning.
- **Interpretation:** giá trị của survey nằm ở khả năng đặt các phương pháp vào cùng một pipeline và cùng ngôn ngữ so sánh.
- **Background:** trong forecasting, mọi phép biến đổi phải được fit trên phần train để tránh nhìn thấy tương lai.

## Research gap được xử lý

Paper kết hợp taxonomy với empirical analysis. Taxonomy trả lời “có những nhóm phương pháp nào”; empirical analysis kiểm tra “một pipeline preprocessing cụ thể ảnh hưởng thế nào tới dự đoán CO bằng LSTM”.