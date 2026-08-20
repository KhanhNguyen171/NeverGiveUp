# 4.2 Transformation và thay đổi phân phối

## Vấn đề

Nhiều feature có skewness lớn hoặc variance thay đổi theo mức tín hiệu. Một transformation $g$ có thể làm distribution cân đối hơn, nhưng cũng có thể làm mất ý nghĩa vật lý nếu dùng không phù hợp.

## Background Knowledge

Log transform:

$$z=\log(x+c),\quad c> -\min(x)$$

giảm ảnh hưởng của giá trị lớn. Box-Cox cho $x>0$:

$$
z(\lambda)=
\begin{cases}
\frac{x^\lambda-1}{\lambda},&\lambda\ne0\\
\log x,&\lambda=0
\end{cases}
$$

$\lambda$ được chọn theo tiêu chí thống kê trên train. Với dữ liệu có số âm, cần dịch miền hoặc chọn Yeo-Johnson; không được áp dụng log trực tiếp.

## Logic thuật toán

```text
Kiểm tra miền giá trị và skewness
      ↓
Chọn họ transformation
      ↓
Ước lượng parameter trên train
      ↓
Biến đổi train/validation/test nhất quán
      ↓
Inverse transform prediction
```

## From Paper và giới hạn claim

Paper đưa normalization/transformation vào taxonomy và thảo luận vai trò của scale, nhưng source không xác nhận một benchmark độc lập để xếp hạng log, Box-Cox hay các biến đổi khác. Vì vậy công thức trên là kiến thức nền dùng để học thuật toán, không phải công thức được gán riêng cho empirical result.