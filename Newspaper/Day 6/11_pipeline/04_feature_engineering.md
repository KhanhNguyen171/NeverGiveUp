# 11.4 Feature engineering node

## Input/output

Input là chuỗi đã clean và transform. Output là $X_t\in\mathbb{R}^{L\times F'}$, trong đó $F'$ gồm raw sensors và feature temporal/lag/rolling đã được chọn.

## Kiểm tra

- lag chỉ lấy quá khứ;
- rolling window không centered trong causal task;
- calendar dùng timezone đúng;
- số feature không tăng ngoài budget;
- feature tạo từ imputed value có provenance.

## Tương tác với selection

Tạo feature trước rồi selection cho phép selector đánh giá temporal representation, nhưng làm search space lớn. Tạo quá ít feature làm model tự gánh toàn bộ cấu trúc; tạo quá nhiều gây redundancy. Chọn bằng validation temporal, không chọn bằng test.