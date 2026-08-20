# 1.2 Bài toán nghiên cứu

## Vấn đề

Một time series có thể đồng thời gặp nhiều lỗi: một sensor mất gói tin, một giá trị tăng đột biến, phân phối giữa các biến khác scale, và các timestamp không thẳng hàng. Các lỗi này tương tác với nhau. Chẳng hạn, outlier làm lệch mean và standard deviation; missing làm sai rolling statistic; temporal misalignment làm quan hệ giữa sensor bị hiểu sai.

Vì vậy, câu hỏi không chỉ là “điền NaN bằng gì?”, mà là:

1. Dữ liệu đang có anomaly nào?
2. Anomaly là lỗi hay một sự kiện thật?
3. Phương pháp nào dùng đúng với distribution và temporal dependency?
4. Chất lượng sau preprocessing có giúp downstream model hay làm mất tín hiệu?

## Formulation

Gọi $D$ là dữ liệu quan sát, $P$ là một pipeline preprocessing và $M$ là mô hình downstream. Khi đó:

$$
\hat{y}=M(P(D))
$$

Chất lượng của $P$ phải được đánh giá ở hai tầng:

- **Input quality:** dữ liệu sau xử lý có ít lỗi và còn giữ cấu trúc quan trọng hay không.
- **Output quality:** $M$ dự đoán tốt hơn hay không.

Một pipeline chỉ tối ưu input quality nhưng làm mất peak hoặc quan hệ temporal vẫn có thể làm output quality xấu đi.

## From Paper

Survey được thực hiện vì các kỹ thuật preprocessing thường nằm rời rạc trong nhiều dòng nghiên cứu. Paper hệ thống hóa các nhóm như data cleaning, normalization, feature processing, sensor fusion và compression, sau đó dùng empirical analysis để xem preprocessing tác động thế nào tới LSTM.

## Ranh giới

Paper không đề xuất một mô hình forecasting mới và không tuyên bố một phương pháp duy nhất tối ưu cho mọi time series. Các phương pháp được phân loại theo mục tiêu, kiểu input và khả năng áp dụng; kết quả thực nghiệm chỉ có ý nghĩa trong bối cảnh dataset và thiết kế thí nghiệm tương ứng.