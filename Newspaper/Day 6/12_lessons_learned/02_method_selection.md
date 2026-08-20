# 12.2 Chọn phương pháp

```text
Gap ngắn + signal liên tục → linear/spline
Gap theo chuỗi + multivariate dependency → EM/model-based
Gaussian univariate → Grubbs có kiểm soát
Non-Gaussian/robust → IQR/MAD
Feature nhiều và dư thừa → filter/embedded/PCA
Nhiều sensor → alignment trước fusion
Bandwidth/energy hạn chế → compression có error bound
```

Đây là decision aid, không phải ranking. Trước khi chọn cần profile data và tạo baseline đơn giản. So sánh phải giữ downstream model, split và metric nhất quán.

## Câu hỏi bắt buộc

- Phương pháp giả định distribution nào?
- Nó dùng tương lai không?
- Output có uncertainty/provenance không?
- Chi phí có phù hợp nơi triển khai không?
- Cải thiện input có thực sự cải thiện task không?