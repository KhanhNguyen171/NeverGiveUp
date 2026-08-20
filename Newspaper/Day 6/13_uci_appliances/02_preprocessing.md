# 13.2 Preprocessing cho Appliances

## Pipeline đề xuất

```text
Load + validate timestamp
      ↓
Profile missing/outlier
      ↓
Causal imputation và anomaly flags
      ↓
Train-only scaling
      ↓
Calendar + lag + rolling features
      ↓
Feature selection
      ↓
LSTM/regression baseline
```

Không mặc định cubic spline và EM là tối ưu cho Appliances. Có thể test chúng như candidate, nhưng phải so sánh với baseline và giữ temporal split.

## Target leakage

Nếu dự báo $y_{t+h}$, rolling feature tại $t$ chỉ dùng đến $t$. Không dùng `Appliances` tương lai, centered window hoặc scaler fit từ test. Với missing target, cần quyết định loại sample hay xây task riêng; không impute target một cách vô thức rồi coi đó là ground truth.