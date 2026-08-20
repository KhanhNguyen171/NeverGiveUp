# 7.1 Sensor fusion

## Bài toán

Có $S$ sensor quan sát cùng hiện tượng nhưng khác sampling rate, noise và độ trễ. Fusion tìm cách tạo thông tin chung từ $x_t^{(1)},...,x_t^{(S)}$ mà vẫn giữ uncertainty và temporal context.

## Ba mức fusion

```text
Data-level: raw aligned signals → combined data
Feature-level: each sensor → features → concatenate/fuse
Decision-level: each model → decisions → combine
```

Data-level giữ thông tin nhiều nhất nhưng yêu cầu alignment tốt. Feature-level cân bằng flexibility và cost. Decision-level chịu mất mát thông tin sớm nhưng dễ mở rộng sensor độc lập.

## Background formulation

Weighted fusion có thể viết:

$$z_t=\sum_{s=1}^{S}w_sx_t^{(s)},\quad \sum_s w_s=1$$

Trọng số phải phản ánh calibration/uncertainty; không nên mặc định bằng nhau.

## From Paper

Sensor fusion được paper đặt trong bối cảnh multivariate IoT và là bước cần thiết trước các kỹ thuật multivariate như EM trong pipeline được mô tả. Air Quality đã có các thuộc tính trong cùng dataset nên không chứng minh một fusion architecture độc lập.