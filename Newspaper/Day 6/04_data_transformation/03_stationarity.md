# 4.3 Stationarity

## Khái niệm

Một chuỗi yếu stationary nếu kỳ vọng và phương sai không đổi theo thời gian, còn covariance phụ thuộc vào độ trễ chứ không phụ thuộc tuyệt đối vào $t$. Forecasting models thường dễ phân tích hơn khi trend và seasonal structure được xử lý rõ.

## Background Knowledge

Sai phân bậc một:

$$
\Delta x_t=x_t-x_{t-1}
$$

Sai phân mùa vụ chu kỳ $s$:

$$
\Delta_s x_t=x_t-x_{t-s}
$$

Quá sai phân có thể biến noise thành tín hiệu và làm mất long-term structure. Có thể dùng kiểm định như ADF hoặc KPSS, nhưng kiểm định không thay thế hiểu biết domain.

## Flow

```text
Quan sát trend/seasonality
      ↓
Chọn differencing hoặc detrending
      ↓
Kiểm tra residual và invertibility
      ↓
Huấn luyện model
      ↓
Cộng lại trend khi dự đoán
```

## Diễn giải

Stationarity là mục tiêu mô hình hóa, không phải quy tắc bắt buộc cho mọi deep model. Paper khảo sát preprocessing rộng; nó không nên được diễn giải thành tuyên bố rằng mọi pipeline phải stationary hoặc phải dùng differencing.