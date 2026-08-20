# 9.6 Findings và mức độ chắc chắn

## Kết luận được hỗ trợ

1. Preprocessing đầy đủ theo DAG cho kết quả LSTM tốt hơn cấu hình tối thiểu trong experiment được minh họa.
2. Input quality và output quality cần đánh giá cùng nhau; một detector outlier tốt chưa đủ nếu downstream prediction không cải thiện.
3. Missing isolated và missing sequence được xử lý khác nhau trong thiết kế của paper.
4. Preprocessing order và default steps được kiểm soát để so sánh các category.

## Không được kết luận

- Không thể nói cubic spline luôn tốt hơn mọi imputation.
- Không thể nói NCA hoặc Laplacian Score luôn tốt hơn wrapper/embedded methods.
- Không thể nói LSTM là model tốt nhất cho mọi preprocessing task.
- Không thể suy rộng các phần trăm trên sang UCI Appliances hoặc domain khác.

## Missing evidence cần ghi chú

Source hiện không đủ căn cứ để khẳng định một ablation hoàn chỉnh loại từng component với confidence interval. Vì vậy, so sánh Figure 2 nên được gọi là end-to-end pipeline comparison, không gọi là causal ablation.