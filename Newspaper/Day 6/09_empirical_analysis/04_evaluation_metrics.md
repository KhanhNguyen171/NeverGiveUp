# 9.4 Evaluation metrics

Với target $y_i$ và prediction $\hat y_i$, các metric nền là:

## RMSE

$$RMSE=\sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat y_i)^2}$$

Bình phương làm lỗi lớn bị phạt mạnh; metric cùng đơn vị với target.

## MAE

$$MAE=\frac{1}{n}\sum_{i=1}^{n}|y_i-\hat y_i|$$

MAE phản ánh sai số tuyệt đối trung bình và ít nhạy với một vài lỗi cực lớn hơn RMSE.

## MAPE

$$MAPE=\frac{100}{n}\sum_{i=1}^{n}\left|\frac{y_i-\hat y_i}{y_i}\right|$$

MAPE khó ổn định khi $y_i$ gần 0; vì vậy cần đọc cách paper xử lý target range trước khi diễn giải phần trăm.

## From Paper

Paper denormalize prediction/observation rồi báo cáo RMSE, MAE, MAPE trên CO scale gốc, và lấy average của ba test cuối. Metric chỉ có ý nghĩa trong cùng target, split và preprocessing protocol.