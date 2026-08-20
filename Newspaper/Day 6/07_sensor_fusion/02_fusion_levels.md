# 7.2 Fusion levels và lựa chọn

| Level | Input | Output | Rủi ro chính |
|---|---|---|---|
| Data | raw sensor streams | joint aligned stream | lệch timestamp, missing tăng |
| Feature | representations của từng sensor | feature vector | mất tương tác raw |
| Decision | predictions/decisions | fused decision | uncertainty bị nén |

## Logic lựa chọn

- Chọn **data-level** khi sensor cùng semantics, cùng clock và cần tương tác vật lý.
- Chọn **feature-level** khi mỗi sensor cần encoder riêng hoặc có sampling khác.
- Chọn **decision-level** khi sensor độc lập, mạng không ổn định hoặc cần failover.

## Đánh giá

Không chỉ đo accuracy. Cần đo latency, bandwidth, missing robustness, calibration và khả năng hoạt động khi một sensor mất. Paper nhấn mạnh edge/IoT làm resource cost trở thành tiêu chí, nhưng không cung cấp một ranking phổ quát giữa ba level.