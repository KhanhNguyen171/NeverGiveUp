# 11.3 Transformation node

## Quy trình

1. Fit scale/transform parameter trên train.
2. Lưu parameter cùng schema version.
3. Apply cùng phép biến đổi cho validation/test/live stream.
4. Inverse-transform prediction trước khi báo cáo metric vật lý.
5. Kiểm tra range, NaN mới và overflow.

## Phân tích

Transformation thay đổi numerical geometry, không thay thế data cleaning. Nếu outlier chưa xử lý, min-max và z-score có thể bị kéo lệch. Nếu target được transform, loss và metric phải được diễn giải đúng scale.

## Forecasting constraint

Một rolling statistic phải là trailing window; một decomposition phải được fit causal hoặc chỉ dùng history tại thời điểm dự báo. Đây là kiến thức pipeline bổ sung để bảo vệ validity.