# 9.2 Dataset và target

## From Paper

Empirical analysis sử dụng AirQuality dataset, một multivariate sensor time series có các thuộc tính chất lượng không khí và đáp ứng CO. Dataset có các giá trị reserved value `-200`; pipeline thay chúng bằng `NaN` để biến mã đặc biệt thành trạng thái missing có thể xử lý thống nhất.

Paper đánh giá LSTM dự đoán Carbon Monoxide CO. Vì dữ liệu có nhiều thuộc tính, nó phù hợp để minh họa missing multivariate, outlier theo feature và feature selection.

## Data contract

Một record cần có:

```text
Timestamp + sensor features + CO target
```

Trước preprocessing cần kiểm tra kiểu số, thứ tự timestamp, duplicate, reserved values và tỷ lệ missing. Không được coi `-200` là một phép đo vật lý hợp lệ nếu dataset định nghĩa nó là reserved missing marker.

## Những gì không được suy đoán

Số dòng, số feature, khoảng thời gian, split và tỷ lệ missing phải được lấy từ bảng dataset/experimental section của PDF nếu cần ghi số cụ thể. Chương này không tự điền các con số đó từ trí nhớ hoặc từ dataset khác.

## Transfer warning

AirQuality không phải UCI Appliances Energy Prediction. Hai dataset đều có sensor/time structure nhưng không thể gán nguyên pipeline hay kết quả của AirQuality sang Appliances mà không chạy lại thực nghiệm.