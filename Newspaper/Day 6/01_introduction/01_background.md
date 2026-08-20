# 1.1 Bối cảnh nghiên cứu

## From Paper

Paper *Time-series data preprocessing: A survey and an empirical analysis* xem preprocessing là một bài toán rộng hơn việc xóa lỗi dữ liệu. Time series xuất hiện trong IoT, công nghiệp, năng lượng, y tế và tài chính; dữ liệu được tạo theo thời gian nên các quan sát không độc lập hoàn toàn. Một giá trị ở thời điểm $t$ có thể phụ thuộc vào lịch sử, mùa vụ, trạng thái hệ thống và các sensor khác.

Dữ liệu thực tế có thể chứa missing instances, outliers, noise, scale khác nhau, high dimensionality và các luồng sensor không đồng bộ. Nếu các vấn đề này truyền thẳng vào mô hình, lỗi preprocessing có thể lan sang dự đoán và làm giảm độ tin cậy của kết luận.

## Kiến thức nền

Có thể mô hình hóa quan sát:

$$
x_t = s_t + n_t
$$

trong đó $s_t$ là tín hiệu hoặc trạng thái cần học, còn $n_t$ là nhiễu. Với dữ liệu nhiều biến, mỗi thời điểm có vector:

$$
\mathbf{x}_t=[x_t^{(1)},x_t^{(2)},...,x_t^{(F)}]
$$

$T$ là số thời điểm và $F$ là số feature. Preprocessing phải bảo toàn càng nhiều thông tin hữu ích của $\{\mathbf{x}_t\}_{t=1}^{T}$ càng tốt.

## Luận điểm chính

Mục tiêu không phải tạo ra dữ liệu “đẹp” bằng mọi giá. Mục tiêu là biến raw time series thành dữ liệu có chất lượng phù hợp với downstream task, đồng thời hạn chế information loss và data leakage.

```text
Raw observations
      ↓
Quality diagnosis
      ↓
Cleaning / transformation / representation
      ↓
AI-ready time series
      ↓
Forecasting, classification or anomaly detection
```

## Key takeaway

Time-series preprocessing là một phần của hệ thống suy luận, không chỉ là bước kỹ thuật trước mô hình.