# Khi Freeze các layer đầu của CNN và chỉ Fine-tune các layer sau, ta đang giả định điều gì về đặc trưng học được?

> Khi Freeze các layer đầu của CNN và chỉ Fine‑tune các layer sau, ta đang giả định rằng những đặc trưng nền tảng mà mô hình học được ở các layer đầu là những đặc trưng phổ quát, có thể sử dụng lại cho nhiều bài toán khác nhau. Đây là cách nhiều mô hình thị giác vận hành: phần đầu trích các đặc trưng cơ bản như cạnh, góc, hoa văn; phần sau xử lý các đặc trưng phức tạp hơn tùy theo nhiệm vụ.

## Vì sao khi Fine‑tune mô hình CNN, nhiều người lại Freeze các layer đầu?

Rất nhiều bạn khi làm bài toán Computer Vision đều gặp câu hỏi: “Có cần Fine‑tune toàn bộ mô hình không?”. Đây là lúc khái niệm Freeze layer xuất hiện. Vấn đề thường gặp là: nếu Fine‑tune quá nhiều, mô hình dễ học lệch; nếu Freeze quá nhiều, mô hình khó thích nghi dữ liệu mới.

Để hiểu bản chất, chỉ cần nắm cấu trúc đặc trưng mà CNN học được theo từng tầng.

## Bản chất kỹ thuật: CNN học đặc trưng theo tầng như thế nào?

CNN hoạt động theo nguyên tắc trích xuất đặc trưng theo nhiều cấp độ:

1. Các layer đầu: học các mô hình đơn giản như:
    - edge
    - orientation
    - color contrast
    - brightness
    - simple texture
    - local frequency
    - simple patterns

2. Các layer giữa: học cấu trúc trung gian như chi tiết vật thể.
3. Các layer cuối: học đặc trưng gắn với nhiệm vụ, thường mang tính phân loại.

Khi Freeze các layer đầu và chỉ Fine‑tune các layer sau, ta đang giả định rằng tập dữ liệu mới __không quá khác__ so với tập dữ liệu mà mô hình được huấn luyện ban đầu, ít nhất ở mặt các đặc trưng nền tảng. Vì vậy phần đầu có thể giữ nguyên, chỉ cần điều chỉnh phần cuối để mô hình thích nghi nhiệm vụ mới.

- Tại sao không freeze toàn bộ backbone?
    - vì dataset mới có thể khác, ví dụ ban đầu ImageNet là ảnh cho mèo thì `Domain similarity: cao` feature: `edge, texture, fur, shape` vẫn còn hữu ích ta có thể Freeze nhiều layer và Fine-tune ít layer. Nhưng khi ImageNet là ảnh X-ray thì `Domain similarity: thấp hơn`, mặc dù edge vẫn còn hữu ích nhưng `texture, shape, constrast, semantic patterns` khác đáng kể nên ta có thể freeze ít layer và Fine-tune nhiều hơn.

## Ví dụ minh họa
Nếu bạn dùng một mô hình tiền huấn luyện (pretrained) trên ImageNet để phân loại bệnh trên lá cây:

1. Các layer đầu vẫn hữu ích vì cạnh lá, độ cong, vân màu vẫn là dạng hình học chung.
2. Các layer sau cần điều chỉnh vì mô hình phải nhận biết các mẫu bệnh đặc thù mà ImageNet không có.

Trong trường hợp này, Freeze layer đầu giúp tiết kiệm tài nguyên và giữ sự ổn định của mô hình.

### Ví dụ cho ResNet-18

```
ResNet-18
│
├── Conv1
│    └── Low-level features
│         Edge / Color / Orientation
│
├── Layer1
│    └── Simple patterns
│         Texture / Corners
│
├── Layer2
│    └── Mid-level features
│         Shapes / Local structures
│
├── Layer3
│    └── Higher-level features
│         Object parts
│
├── Layer4
│    └── High-level representation
│         Object-level semantics
│
└── FC
     └── Task-specific classification
```

> CNN không học "object" ngay từ đầu. Nó dần xây dựng representation bằng cách kết hợp các feature ở nhiều cấp độ.

## Khi triển khai dự án AI/ML, quyết định Freeze layer dựa vào điều gì?
Trong môi trường dự án thực tế, mức độ Freeze phụ thuộc vào:

1. Sự khác biệt của domain dữ liệu (ví dụ ảnh vệ tinh → khác xa với ảnh đời thường).
2. Độ lớn của tập dữ liệu (dữ liệu ít thì Freeze nhiều để tránh overfitting).
3. Năng lực phần cứng (Fine‑tune toàn bộ thường tốn tài nguyên lớn).

Thực tế, nhóm Computer Vision thường kiểm thử nhiều cấu hình khác nhau như Freeze 50%, Freeze một vài block, hoặc Fine‑tune toàn bộ để tìm cấu hình ổn nhất.

### Những yếu tố quan trọng khi lựa chọn Freeze layer trong production

> xem Freeze layer như một hyperparameter của transfer learning, được quyết định bởi mức độ khác nhau giữa pretrained representation và target task/data.

#### 1. Domain gap

So sánh: $P_{pretrain}(x)$ vs $P_{target}(x)$. Nếu hai distribution gần nhau thì các feature low-level và mid-level thường có transfer tốt thì ta có thể freeze nhiều layer, ngược lại domain gap lớn, khi đó cần nhiều layer thích nghi nên ta cần freeze ít layer hơn.

> Không nên hiểu đơn giản rằng domain khác → phải unfreeze toàn bộ. Ta vẫn cần thực nghiệm.

#### 2. Dataset size

Đây là trade-off giữa: $Adaptation \leftrightarrow Overfitting$

- Dataset nhỏ mà ta unfreeze toàn bộ ResNet thì model có nhiều freedom để thay đổi representation -> dễ overfit.
    - nên ta cần freeze backbone và unfreeze Classifier. Hoặc Freeze Early blocks và unfreeze Late blocks và Head.

- Dataset lớn ta có nhiều dữ liệu hơn để điều chỉnh representation khi đó `Full Fine-tuning` có thể hợp lý hơn.

#### 3. Validation performance

> Không nên quyết định Freeze 30%, 50% hay 70% chỉ bằng lý thuyết. Phải kiểm chứng bằng validation experiment.

Ví dụ thiết kế experiment:

| Configuration   |        Frozen | Val Accuracy | Val Loss |
| --------------- | ------------: | -----------: | -------: |
| Head only       | 100% backbone |        84.2% |     0.51 |
| Layer4 + Head   |          ~75% |        87.8% |     0.39 |
| Layer3–4 + Head |          ~50% |    **89.1%** | **0.34** |
| Full FT         |            0% |        88.7% |     0.36 |


Kết luận:

```
Freeze 50%
      ↓
best validation performance
      ↓
candidate for production
```

Chứ không phải `"Freeze 50% vì 50% là tiêu chuẩn"` không có một tỷ lệ Freeze cố định cho mọi project.