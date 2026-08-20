# 12.1 Key principles

1. Preprocessing rộng hơn data cleaning.
2. Phải phân biệt missing, outlier và noise trước khi xử lý.
3. Method selection phụ thuộc missing pattern, distribution, temporal dependency và resource.
4. Detection không đồng nghĩa removal.
5. Input quality phải được kiểm tra cùng downstream output quality.
6. Mọi claim thực nghiệm phải gắn dataset, metric và context.
7. Edge/IoT cần tính cả bandwidth, energy, latency và storage.
8. Provenance giúp phát hiện information loss và audit pipeline.

## From Paper và Background

Các nguyên tắc đầu phản ánh taxonomy/empirical analysis của paper. Quy tắc fit transform trên train và tránh future leakage là background engineering cần thiết để triển khai kết quả một cách hợp lệ.