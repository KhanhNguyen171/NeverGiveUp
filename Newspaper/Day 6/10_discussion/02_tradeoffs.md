# 10.2 Trade-offs

## Accuracy và information preservation

Smoothing có thể giảm noise nhưng xóa peak. Imputation tạo continuity nhưng đưa giá trị ước lượng vào dataset. Compression giảm storage nhưng lossy error có thể làm mất anomaly. Vì vậy cần lưu provenance và đánh giá signal quan trọng sau mỗi bước.

## Complexity và deployability

Mean/IQR/linear interpolation chạy nhẹ, phù hợp edge. EM, wrapper selection hoặc deep imputation khai thác dependency tốt hơn nhưng cần CPU/RAM và validation. Trong IoT, latency và energy có thể quan trọng ngang RMSE.

## Generalization

Kết quả của paper là end-to-end comparison trên AirQuality với LSTM. Chúng chứng minh tác động trong context đó; việc chọn phương pháp cho dataset khác cần kiểm tra distribution, sampling, missing mechanism và target.

## Causal integrity

Mọi statistic, selector và transform phải fit theo thời gian. Backward fill, centered rolling, interpolation qua boundary hoặc global normalization có thể làm test score lạc quan.