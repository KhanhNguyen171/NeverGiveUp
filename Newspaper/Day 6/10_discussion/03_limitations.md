# 10.3 Limitations và phạm vi diễn giải

## Hạn chế của evidence hiện có

- Empirical comparison dùng một dataset và downstream LSTM; khả năng tổng quát hóa cần được kiểm chứng.
- Complete DAG thay nhiều bước cùng lúc, nên Figure 2 không cô lập được contribution của từng component.
- Survey liệt kê nhiều technique nhưng không phải kỹ thuật nào cũng được test.
- Compression, sensor fusion và nhiều transformation được trình bày ở taxonomy/trade-off, không có nghĩa có benchmark chung trong AirQuality.

## Cách báo cáo thận trọng

Nên viết: “Trong experiment của paper, cấu hình DAG cho lỗi thấp hơn cấu hình tối thiểu.” Không nên viết: “DAG là pipeline tối ưu.”

## Câu hỏi cho nghiên cứu tiếp

Cần rolling-origin evaluation, nhiều dataset, nhiều downstream model, confidence interval, sensitivity theo missing rate và đánh giá latency/energy nếu mục tiêu là edge deployment.