# 8.4 Compression trong Edge/IoT

## Vị trí xử lý

```text
Sensor → Edge preprocessing/compression → Network → Cloud/model
```

Đẩy compression về edge giảm bandwidth nhưng tiêu tốn CPU, RAM và pin tại edge. Đẩy về cloud giữ edge nhẹ nhưng truyền raw data đắt hơn.

## Quyết định kỹ thuật

Cần xác định:

- latency budget;
- energy budget;
- loss bound cho từng feature;
- anomaly có cần giữ nguyên không;
- có thể giải nén trước model hay model nhận compressed representation;
- behavior khi packet/block hỏng.

## From Paper

Paper nhấn mạnh các giải pháp hướng edge và trade-off resource. Tuy nhiên paper không cung cấp một kết quả compression ratio/latency thống nhất để kết luận phương pháp nào tối ưu.

## Nguyên tắc

Compression phải là một ràng buộc có kiểm soát, không phải bước cuối làm mất khả năng tái lập dữ liệu. Lưu schema, version, error bound và provenance cùng block nén để downstream pipeline có thể kiểm toán.