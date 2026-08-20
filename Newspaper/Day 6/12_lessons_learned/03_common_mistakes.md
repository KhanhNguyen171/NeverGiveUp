# 12.3 Common mistakes

- Fit scaler trên toàn bộ dataset.
- Dùng backward fill hoặc centered rolling trong forecasting mà không phân tích leakage.
- Xóa outlier thật chỉ vì nó hiếm.
- Dùng mean cho block missing dài.
- Chọn feature bằng test score.
- Gọi mọi technique trong survey là proposed method.
- Gọi một end-to-end comparison là ablation từng component.
- Báo cáo MAPE khi target gần zero mà không cảnh báo.
- Nén lossy mà không đo downstream accuracy.
- Ghi số liệu không có table/figure/section truy xuất.

## Nguyên tắc sửa

Mỗi lỗi đều quay về một câu hỏi: dữ liệu nào được phép dùng tại thời điểm $t$, giả định nào đang được đưa vào, và bằng chứng nào chứng minh bước xử lý có ích?