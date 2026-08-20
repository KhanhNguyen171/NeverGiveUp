# 13.1 UCI Appliances Energy Prediction

## Phạm vi

Chương này là bài tập chuyển giao nguyên tắc survey sang một dataset khác, không phải kết quả được paper báo cáo. UCI Appliances Energy Prediction là multivariate household energy time series với target `Appliances`, các biến nhiệt độ/độ ẩm trong nhà và biến thời tiết/thời gian.

## Cần kiểm tra trước khi học

- sampling interval và timezone;
- số hàng/feature theo bản phân phối dataset đang dùng;
- missing/reserved values;
- target horizon;
- thứ tự timestamp và duplicate.

Không đưa các con số dataset vào tài liệu nếu chưa lấy từ file nguồn chính thức hoặc metadata đi kèm.

## Hypothesis hợp lý

Năng lượng có thể phụ thuộc time-of-day, weekday, nhiệt độ, độ ẩm và lịch sử. Đây là hypothesis để thiết kế experiment, không phải claim của survey.