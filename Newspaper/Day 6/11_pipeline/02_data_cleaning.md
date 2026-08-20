# 11.2 Data cleaning node

## Algorithmic flow

```text
Parse timestamp and schema
      ↓
Map reserved markers → NaN
      ↓
Profile missing pattern
      ↓
Detect outlier per feature/context
      ↓
Validate anomaly với domain
      ↓
Impute hoặc giữ cờ anomaly
```

Không được tự động xóa mọi extreme value: sensor failure và event thật có thể có cùng hình dạng. Với isolated gap, interpolation phù hợp khi signal liên tục; với sequence gap, cần model multivariate/temporal và phải báo uncertainty.

## Output contract

Ngoài giá trị đã xử lý, nên giữ `was_missing`, `was_outlier`, method và timestamp. Nhờ đó downstream có thể đánh giá liệu model dựa quá nhiều vào dữ liệu ước lượng hay không.

## Liên hệ paper

DAG của paper thay reserved `-200`, dùng Grubbs/IQR, cubic spline và EM theo missing pattern. Đây là template tham khảo cho AirQuality, không phải policy bắt buộc.