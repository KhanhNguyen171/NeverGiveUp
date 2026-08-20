# 6.3 Wrapper methods

## Ý tưởng

Wrapper đánh giá trực tiếp subset bằng model validation:

$$S^*=\arg\min_{S:|S|\le k}\mathcal{L}_{val}(M_S)$$

Không thể thử toàn bộ $2^F$ subset khi $F$ lớn, nên dùng forward selection, backward elimination hoặc heuristic search.

## Flow

```text
Subset candidate
      ↓
Train model trên train
      ↓
Evaluate validation
      ↓
Add/remove feature
      ↓
Stop khi loss không cải thiện
```

## Trade-off

Wrapper bám sát mục tiêu cuối nên có thể đạt subset hữu ích hơn filter, nhưng chi phí là số lần train model lớn và dễ overfit validation. Với time series, split phải giữ thứ tự và mọi cửa sổ phải được tạo nhất quán.

Paper không xác nhận wrapper là thành phần chính của empirical pipeline; đây là kiến thức nền để phân biệt taxonomy.