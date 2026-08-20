# 9.5 Kết quả thực nghiệm

## So sánh complete DAG với preprocessing tối thiểu

Paper báo cáo hai thí nghiệm trực quan trong Figure 2: LSTM huấn luyện trên dữ liệu qua DAG preprocessing đầy đủ và LSTM huấn luyện trên dữ liệu gần nguyên bản, chỉ dùng cubic spline để loại NaN.

Giá trị trung bình của ba test cuối:

| Cấu hình | RMSE | MAE | MAPE |
|---|---:|---:|---:|
| Complete DAG | 0.32 | 0.23 | 25.26% |
| Minimum preprocessing | 0.60 | 0.45 | 51.41% |

Paper nêu mức giảm lỗi xấp xỉ $46.66\%$ RMSE, $48.88\%$ MAE và $50.87\%$ MAPE khi dùng dữ liệu qua DAG. Các phần trăm này là comparison trong AirQuality/LSTM experiment, không phải universal ranking.

## Phân tích logic

DAG không chỉ điền missing. Nó thay outlier, phân biệt missing pattern và selection feature. Vì vậy kết quả cho thấy **pipeline phối hợp** có tác động lớn hơn cấu hình chỉ loại NaN; không thể từ bảng này tách riêng đóng góp nhân quả của từng bước.

Các prediction/observation giữa hai plot có thể khác vì complete pipeline đã thay outlier và thực hiện nhiều preprocessing khác.