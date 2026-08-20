# 4.4 Decomposition

## Mô hình

Một decomposition thường tách chuỗi thành trend, seasonal và residual:

$$x_t=T_t+S_t+R_t$$

hoặc multiplicative:

$$x_t=T_tS_tR_t$$

Trong đó $T_t$ mô tả biến động dài hạn, $S_t$ chu kỳ lặp và $R_t$ phần còn lại.

## Thuật toán logic

```text
Xác định chu kỳ hoặc tần số
      ↓
Ước lượng trend
      ↓
Ước lượng seasonal component
      ↓
Tính residual
      ↓
Dùng component phù hợp làm feature hoặc input
```

Moving-average decomposition dễ hiểu nhưng chịu ảnh hưởng biên; STL linh hoạt hơn nhưng cần chọn seasonal period. Fourier/wavelet decomposition cung cấp biểu diễn miền tần số nhưng khó giải thích hơn.

## Trade-off

Decomposition giúp model học từng cấu trúc riêng, nhưng thêm hyperparameter và nguy cơ leakage nếu dùng thông tin tương lai để ước lượng component. Paper liệt kê decomposition như một hướng transformation; source không xác nhận decomposition là một bước trong DAG empirical Air Quality.