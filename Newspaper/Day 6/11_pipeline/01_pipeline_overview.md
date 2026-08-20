# 11.1 Pipeline overview

## Pipeline thực hành

```text
Raw data
  ↓ profile schema/time
Data cleaning
  ↓ missing, outlier, noise
Transformation
  ↓ scale/distribution/stationarity
Feature engineering
  ↓ temporal, lag, rolling
Feature selection/fusion
  ↓ reduce and align
Compression nếu cần
  ↓
AI-ready data
```

Đây là synthesis học tập từ taxonomy và DAG thực nghiệm; không gọi nó là một thuật toán duy nhất do paper đề xuất.

## Nguyên tắc điều khiển

Mỗi node phải có input/output contract, provenance, validation check và policy khi thất bại. Pipeline phải version hóa parameter, đặc biệt imputation, scaling, selector và compression error bound.

## Split trước transform

Với forecasting, chia theo thời gian trước khi fit parameter. Mọi bước dùng target hoặc future window phải được xem như nguy cơ leakage.