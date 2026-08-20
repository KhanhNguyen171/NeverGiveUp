# 8.2 Lossless compression

## Delta và entropy coding

Với chuỗi có biến động nhỏ, delta encoding lưu:

$$d_t=x_t-x_{t-1}$$

Các $d_t$ nhỏ thường cần ít bit hơn. Run-length encoding lưu cặp $(value,count)$ cho đoạn lặp. ZIP/deflate kết hợp dictionary và entropy coding.

## Gorilla-style idea

Với floating-point time series, có thể encode XOR giữa bit pattern liên tiếp; khi giá trị gần nhau, XOR có nhiều bit 0 và tiết kiệm storage. Cần giữ đúng format để giải nén không sai số.

## Flow

```text
Validate ordering and type
      ↓
Delta/XOR representation
      ↓
Entropy or dictionary coding
      ↓
Compressed blocks + metadata
```

Metadata phải chứa timestamp origin, sampling interval, schema và version. Nếu mất metadata, file có thể nhỏ nhưng không còn usable.

Paper liệt kê ZIP/deflate và Gorilla trong survey; source không xác nhận benchmark ratio cụ thể trên Air Quality.