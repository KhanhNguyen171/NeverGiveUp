# 8.3 Lossy compression

## Piecewise approximation

Piecewise Aggregate Approximation chia chuỗi thành đoạn và thay bằng aggregate, thường là mean. Piecewise Linear Approximation biểu diễn mỗi đoạn bằng đường thẳng:

$$\hat{x}(t)=a_it+b_i,\quad t\in segment_i$$

Sai số tối đa hoặc RMSE được dùng làm stopping criterion. Đoạn có biến động mạnh cần nhiều breakpoint hơn.

## Logic

```text
Chọn error bound ε
      ↓
Bắt đầu một segment
      ↓
Mở rộng segment và fit approximation
      ↓
Nếu error > ε: chốt segment
      ↓
Lặp đến hết chuỗi
```

## Trade-off

$\epsilon$ nhỏ giữ chi tiết nhưng CR thấp; $\epsilon$ lớn nén tốt nhưng có thể xóa anomaly và peak. Đánh giá phải đo cả CR, latency và downstream accuracy, không chỉ kích thước file.

Đây là mô tả kiến thức nền của PLA/PAA được paper khảo sát; không phải thuật toán mới do tác giả đề xuất.