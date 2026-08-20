# 2.3 Cách đọc survey

Paper được học theo ba lớp:

1. **Problem layer:** missing, outlier, noise, scale, dimension và alignment.
2. **Method layer:** thuật toán, giả định, input/output, độ phức tạp và trade-off.
3. **Evidence layer:** empirical setup, metric, bảng kết quả và giới hạn suy luận.

```text
Problem
  ↓
Method and assumptions
  ↓
Preprocessed data
  ↓
Downstream evaluation
  ↓
Decision about applicability
```

Các chương 4–8 của workspace là các learning chapters được tổ chức lại từ taxonomy; chúng không nhất thiết là heading nguyên văn của PDF. Chương 9–10 tập trung vào evidence và interpretation. Chương 13 chuyển nguyên tắc sang UCI Appliances Energy Prediction và phải được đọc như application exercise, không phải kết quả mới của paper.

## Quy tắc citation

Claim về paper phải kèm section, figure, table hoặc mô tả “phần empirical analysis”. Claim nền dùng nhãn **Background Knowledge**. Khi PDF không nêu rõ, dùng câu “Paper không mô tả rõ...” thay vì suy đoán.