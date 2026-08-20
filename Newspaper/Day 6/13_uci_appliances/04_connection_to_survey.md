# 13.4 Liên hệ với survey

| Survey concept | Appliances application |
|---|---|
| Missing data | kiểm tra gap và impute theo pattern |
| Outlier | phân biệt lỗi sensor với đỉnh tiêu thụ thật |
| Transformation | scale features khác đơn vị |
| Feature engineering | calendar, lag, rolling |
| Feature selection | giảm sensor dư thừa |
| Sensor fusion | căn chỉnh nhiệt độ/độ ẩm/thời tiết |
| Compression | cân nhắc edge energy monitoring |

## Kết luận phạm vi

Paper cung cấp taxonomy và bằng chứng trên AirQuality; chương này chỉ thiết kế cách áp dụng nguyên tắc. Mọi kết quả trên Appliances phải được chạy và báo cáo riêng, không được sao chép RMSE/MAE/MAPE hoặc gọi pipeline AirQuality là optimum cho dataset này.