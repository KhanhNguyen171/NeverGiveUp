# 6.4 Embedded methods

## Cơ chế

Embedded selection xảy ra trong lúc model học. Ví dụ regularization có thể ép trọng số nhỏ:

$$\min_{w}\mathcal{L}(w)+\lambda\|w\|_1$$

$\lambda$ điều khiển trade-off giữa fit và sparsity. Tree-based model dùng split gain hoặc permutation importance để xếp hạng feature.

## Phân tích

Embedded thường rẻ hơn wrapper vì selection và training chung một quy trình, nhưng importance phụ thuộc model và có thể không ổn định khi các feature tương quan. Với neural network, magnitude weight không luôn là thước đo causal importance.

## Quy trình đánh giá

Chọn $\lambda$ trên validation, kiểm tra stability qua nhiều rolling split, rồi retrain model với cấu hình đã khóa. Không dùng test để chọn threshold.

Paper trình bày nhiều nhóm feature selection trong survey nhưng không báo cáo một bảng embedded selection riêng trong các thông tin empirical đã xác nhận.