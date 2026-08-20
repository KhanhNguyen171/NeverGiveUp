# 6.2 Filter methods

## Cơ chế

Filter chấm điểm feature bằng tiêu chí độc lập với downstream model rồi chọn top-$k$:

$$S=\operatorname{TopK}(q(x_j,y))$$

$q$ có thể là correlation, mutual information, F-test, variance hoặc Laplacian Score.

## Laplacian Score

Với đồ thị similarity giữa các mẫu, trực giác của Laplacian Score là feature tốt giữ các điểm gần nhau trong không gian dữ liệu cũng gần nhau trong giá trị feature. Score thấp thường tốt hơn, nhưng phải theo đúng định nghĩa và normalization của implementation.

## Ưu nhược điểm

Filter nhanh, ít overfit vào một model và phù hợp high-dimensional data. Đổi lại, nó có thể bỏ qua tương tác feature hoặc mục tiêu sequence. Correlation thấp không đồng nghĩa feature vô dụng nếu quan hệ phi tuyến.

## From Paper

Paper liệt kê F-test, Relief/RReliefF, Laplacian Score, NCA và các filter/selection methods. Empirical analysis chọn NCA và Laplacian Scores; không được biến mọi phương pháp trong bảng survey thành phương pháp đã thử.