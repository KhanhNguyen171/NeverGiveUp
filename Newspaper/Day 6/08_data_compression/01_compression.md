# 8.1 Mục tiêu compression

## Bài toán

Với raw stream $D$, compressor tạo $C(D)$ nhỏ hơn; decompressor khôi phục $\hat D$. Hai đại lượng nền:

$$CR=\frac{\text{original size}}{\text{compressed size}}$$

và reconstruction error $E(D,\hat D)$.

Mục tiêu là tối ưu cost tổng thể:

$$J=\alpha\,\text{storage}+\beta\,\text{bandwidth}+\gamma E$$

Đây là formulation nền để phân tích trade-off, không phải objective được paper tuyên bố cho mọi phương pháp.

## Lossless và lossy

Lossless yêu cầu $\hat D=D$, phù hợp dữ liệu phải khôi phục chính xác. Lossy cho phép sai số có kiểm soát để đạt CR cao hơn; phải bảo vệ peak, anomaly và feature cần cho downstream model.

## From Paper

Paper đưa compression vào phạm vi preprocessing, đặc biệt cho Edge/IoT nơi bandwidth, storage và energy có giới hạn. Compression thường được áp dụng sau các bước cần dữ liệu đầy đủ/được chuẩn hóa trong DAG thực nghiệm.