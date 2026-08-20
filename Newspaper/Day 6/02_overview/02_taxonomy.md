# 2.2 Taxonomy của preprocessing

## Cấu trúc khái niệm

Taxonomy có thể đọc theo câu hỏi mà mỗi nhóm trả lời:

| Nhóm | Câu hỏi | Ví dụ |
|---|---|---|
| Data cleaning | Quan sát nào thiếu, sai hoặc nhiễu? | interpolation, EM, IQR |
| Normalization/transformation | Các biến có scale/distribution phù hợp chưa? | min-max, z-score, Box-Cox |
| Feature engineering | Có thể biểu diễn temporal context thế nào? | lag, rolling, calendar |
| Feature selection/reduction | Feature nào cần giữ? | NCA, Laplacian Score, PCA |
| Sensor fusion | Nhiều nguồn được căn chỉnh và kết hợp ra sao? | data/feature/decision fusion |
| Compression | Có thể giảm storage/bandwidth với sai số chấp nhận được không? | PLA, Gorilla, ZIP |

## Logic phân loại

Một phương pháp được phân loại theo mục tiêu chính, không theo việc nó có thể dùng ở nhiều bước. Ví dụ rolling mean vừa là feature engineering vừa có thể được dùng để smoothing; trong tài liệu này nó được giải thích theo mục tiêu đang xét.

## From Paper

Bảng phương pháp của paper phân biệt input univariate/multivariate và đánh dấu technique nào được test. Đây là điểm quan trọng: taxonomy và empirical analysis có giao nhau nhưng không trùng nhau.

## Interpretation

Taxonomy giúp tránh lỗi “một công thức cho mọi vấn đề”. Chọn phương pháp phải bắt đầu từ data-generating process, downstream task và resource budget.