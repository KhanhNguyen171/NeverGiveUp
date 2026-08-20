# 2.1 Phạm vi survey

## From Paper

Đối tượng là preprocessing cho dữ liệu số dạng time series, đặc biệt trong bối cảnh multivariate sensing và IoT. Paper khảo sát các nhóm kỹ thuật xử lý anomaly và biến đổi biểu diễn trước khi dùng cho AI.

Phạm vi gồm:

```text
Missing data / outliers / noise
          ↓
Normalization and transformation
          ↓
Feature selection and reduction
          ↓
Sensor fusion and temporal alignment
          ↓
Compression and edge processing
```

Survey không đồng nhất toàn bộ các nhóm trên với một thuật toán duy nhất. Mỗi category có input type, assumptions, mục tiêu và chi phí khác nhau.

## Tiêu chí đọc một phương pháp

Với phương pháp $P$, cần ghi nhận:

- input univariate, multivariate hay dependent;
- phương pháp dựa vào global distribution hay local temporal context;
- output có cùng số chiều hay giảm chiều;
- có giữ nguyên thứ tự thời gian không;
- chi phí tính toán và yêu cầu bộ nhớ;
- rủi ro information loss hoặc leakage.

## Giới hạn phạm vi

Các kết quả empirical của paper không đại diện cho toàn bộ category. Một technique được liệt kê trong survey không có nghĩa nó đã được test trong Air Quality experiment.