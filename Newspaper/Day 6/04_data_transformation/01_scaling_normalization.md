# 4.1 Scaling và normalization

## Mục tiêu

Scaling đưa các feature về miền hoặc độ lớn dễ xử lý hơn. Với vector dữ liệu $\mathbf{x}_t$, phép biến đổi theo từng feature là $z_t=g(x_t)$. Nó không tự sửa missing/outlier; nó chỉ thay đổi biểu diễn số.

## Background Knowledge

**Min-max scaling**:

$$z_t=\frac{x_t-x_{min}}{x_{max}-x_{min}}$$

Output thường nằm trong $[0,1]$. **Z-score**:

$$z_t=\frac{x_t-\mu}{\sigma}$$

với $\mu,\sigma$ phải được ước lượng từ train set trong forecasting. **Robust scaling** thay mean/std bằng median và IQR, ít nhạy với extreme values.

## Flow

```text
Train feature
  ↓ estimate parameters
Scale train
  ↓ reuse same parameters
Scale validation/test
  ↓
Model input
```

Nếu fit $x_{min},x_{max}$ trên toàn bộ dữ liệu, thông tin tương lai có thể đi vào train. Nếu $x_{max}=x_{min}$, feature hằng phải được xử lý riêng.

## Trade-off

Min-max giữ thứ tự và range nhưng nhạy với outlier. Z-score thuận tiện cho nhiều mô hình nhưng phụ thuộc distribution. Robust scaling ổn định hơn khi có outlier nhưng diễn giải scale kém trực quan. Paper liệt kê và khảo sát các normalization techniques; không có cơ sở để nói một kỹ thuật tốt nhất trong mọi dataset.