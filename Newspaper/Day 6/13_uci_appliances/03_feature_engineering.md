# 13.3 Feature engineering cho Appliances

## Features

- cyclic hour/day-of-week;
- lag của `Appliances` và sensor quan trọng;
- trailing mean/std/min/max;
- chênh lệch nhiệt độ trong/ngoài;
- energy change $\Delta y_t=y_t-y_{t-1}$.

Với cửa sổ $L$, input cho sequence model là $X_t\in\mathbb{R}^{L\times F'}$. Chọn $L$ theo sampling interval và horizon; không chọn chỉ vì một giá trị phổ biến.

## Đánh giá

Dùng rolling-origin hoặc chronological holdout. Báo cáo MAE/RMSE; dùng MAPE chỉ khi target không gần zero hoặc bổ sung metric ổn định hơn. So sánh raw baseline, cleaning-only, full feature pipeline và ablation từng nhóm feature.