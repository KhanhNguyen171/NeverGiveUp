# 6.5 Dimensionality reduction

## PCA

PCA tạo feature mới bằng phép chiếu:

$$Z=XW$$

Các cột của $W$ là eigenvectors của covariance matrix; giữ $q<F$ components có eigenvalue lớn nhất. Khác feature selection, PCA không giữ nguyên nghĩa từng sensor.

## Flow

```text
Scale train data
      ↓
Estimate covariance
      ↓
Eigen-decomposition / SVD
      ↓
Chọn q components theo validation
      ↓
Project validation/test bằng W đã fit
```

## Trade-off

PCA nén redundancy và thường nhanh, nhưng component khó diễn giải và variance lớn không chắc là predictive signal. Với time series, PCA theo từng thời điểm cũng có thể bỏ qua temporal covariance; dynamic methods cần giả định khác.

**From Paper:** PCA và LDA xuất hiện trong bảng taxonomy như feature extraction. **Không được khẳng định** paper đã dùng PCA trong empirical Air Quality nếu chưa có bảng xác nhận; source map hiện chỉ chắc chắn NCA và Laplacian Scores.