# 6.1 Feature selection

## Mục tiêu

Feature selection chọn subset $S\subseteq\{1,...,F\}$ thay vì tạo feature mới. Output là $X_S$, giữ nguyên ngữ nghĩa và thường giữ số chiều nhỏ hơn.

```text
F features
   ↓ relevance + redundancy analysis
S selected features
   ↓
Model training
```

Selection có thể giảm noise, multicollinearity, thời gian huấn luyện và chi phí sensor/edge. Nhưng loại nhầm feature có signal yếu hoặc chỉ hữu ích trong tương tác sẽ làm giảm accuracy.

## Quy trình đúng

1. Chia temporal train/validation/test.
2. Fit selector chỉ trên train.
3. Chọn số feature bằng validation.
4. Khóa subset rồi đánh giá test một lần.

Nếu chọn feature trên toàn bộ dataset, kết quả test bị optimistic.

## From Paper

Paper đưa feature selection và dimensionality reduction vào taxonomy; trong empirical pipeline, source đã xác nhận dùng NCA và Laplacian Scores rồi chọn các feature chung tốt nhất. Số feature cụ thể cần đọc ở bảng kết quả tương ứng, không suy đoán từ tên dataset.