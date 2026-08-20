# 7.3 Temporal alignment

## Vấn đề

Hai sensor có timestamp $t_i^{(a)}$ và $t_j^{(b)}$ không nhất thiết đo cùng instant. Nếu ghép theo row index, một event ở sensor A có thể bị ghép với trạng thái khác ở B.

## Flow

```text
Raw timestamps + timezone
      ↓ normalize clock
Chọn grid hoặc tolerance Δ
      ↓ resample / nearest / interpolation
Đánh dấu confidence và missing
      ↓
Fused time index
```

Nearest-neighbor join dùng điểm gần nhất nếu $|t_i-t_j|\le\Delta$. Resampling/interpolation tạo giá trị tại grid nhưng thêm giả định về tín hiệu. Clock drift và latency truyền dẫn cần được đo, không thể sửa chỉ bằng sort timestamp.

## Cảnh báo leakage

Interpolation centered hoặc alignment bằng dữ liệu sau thời điểm dự báo có thể đưa tương lai vào input. Cần giữ cờ provenance để phân biệt observation thật và giá trị ước lượng.

Paper đề cập temporal alignment như challenge của sensor fusion; exact tolerance/window cho empirical Air Quality không được source xác nhận.