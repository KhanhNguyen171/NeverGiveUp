# 9.3 Preprocessing methods trong thí nghiệm

## Pipeline được paper mô tả

```text
Reserved value -200
        ↓ replace with NaN
Outlier detection per feature
        ↓ Grubbs nếu Gaussian, IQR otherwise
Outlier replacement
        ↓ Cubic Spline Interpolation
Missing pattern analysis
        ↓ isolated vs sequence missing
Missing imputation
        ↓ Cubic Spline hoặc EM
Feature selection
        ↓ NCA + Laplacian Scores, chọn feature chung tốt
LSTM regression
```

## Logic từng bước

1. **Chuẩn hóa missing marker:** `-200` không bị đưa vào mean/std như observation thật.
2. **Phát hiện outlier:** Grubbs dùng cho feature có phân phối Gaussian; IQR dùng khi không phù hợp giả định đó.
3. **Thay outlier:** cubic spline ước lượng giá trị trơn từ các điểm xung quanh.
4. **Phân biệt missing:** isolated missing và sequence missing có cấu trúc khác, nên dùng cubic spline cho điểm đơn lẻ và Expectation Maximization (EM) cho đoạn liên tiếp.
5. **Selection:** NCA và Laplacian Scores cung cấp hai góc nhìn selection; paper chọn các feature xuất hiện chung trong nhóm tốt.

## Traceability

Đây là pipeline cụ thể cho dataset và experiment, không phải thứ tự bắt buộc cho mọi hệ thống. Paper nói các category không có trong DAG, như compression, được áp dụng sau feature selection như bước preprocessing tiếp theo nếu cần.