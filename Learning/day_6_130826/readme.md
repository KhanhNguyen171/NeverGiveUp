# Network Depth (số layer) và Width (số neuron mỗi layer) tác động khác nhau như thế nào đến khả năng biểu diễn?

> Khi bắt đầu tìm hiểu về mạng neural, nhiều người thường bối rối trước câu hỏi: “Nên tăng số layer hay tăng số neuron ở mỗi layer để mô hình mạnh hơn?”.
>
> Đây là điểm dễ nhầm lẫn, vì trong các dự án thực tế, việc mở rộng mạng không chỉ liên quan đến “làm mô hình to hơn”, mà còn liên quan đến cách kiến trúc đó biểu diễn được những hàm phức tạp.

## Giải thích dễ hiểu: Depth khác gì Width?
Để hình dung, ta xem mạng neural như một chuỗi các phép biến đổi toán học. Kiến thức này được nói nhiều trong nhóm bài học về Deep Learning (Module 7–8) khi giải thích vai trò của layers và cấu trúc mạng.

### Width (độ rộng)
- Đại diện cho số lượng neuron trong một layer.
- Khi tăng width, mỗi layer có khả năng “nhìn” nhiều chiều thông tin hơn.
- Mạng rộng biểu diễn tốt các quan hệ mang tính “song song”, ví dụ tách nhiều đặc trưng đơn giản cùng lúc.

### Depth (độ sâu)
- Đại diện cho số layer trong mô hình.
- Khi tăng depth, mạng có khả năng tạo ra chuỗi biến đổi phức tạp theo từng tầng.
- Depth giúp mạng biểu diễn các hàm nhiều bước, giống như việc phân tích vấn đề từ đơn giản → kết hợp → thành cấu trúc lớn.

Một cách diễn đạt phổ biến trong lý thuyết:
- Mạng rộng tốt trong việc xử lý đặc trưng đơn giản đồng thời.
- Mạng sâu tốt trong việc biểu diễn các hàm có cấu trúc phân cấp.

### Trong product AI thực tế

> Depth và Width còn liên quan trực tiếp đến khả năng biểu diễn (expressiveness), dữ liệu, latency, memory, khả năng train và chi phí inference.

#### Nhìn từ góc độ toán học

Một MLP có thể viết:

$$h_1 = \sigma (W_1x + b_1)$$
$$h_2 = \sigma (W_2 h_1 + b_2)$$
$$\hat y = f(h_l)$$

Ở đây:

- __Width__ ≈ kích thước vector $h_i$
- __Depth__ ≈ số phép biến đổi liên tiếp $h_1 \rightarrow h_2 \rightarrow ... \rightarrow h_L$

#### Width thực chất đang làm gì?

$$h = \sigma (Wx + b)$$

Nếu hidden layer có: $h \in \mathbb R^{128}$ thì layer tạo ra 128 chiều biểu diễn trung gian, nếu tăng lên 1024 thì model có nhiều "không gian" hơn để lưu và biến đổi thông tin

Và width lớn không đồng nghĩa với model hiểu dữ liệu tốt hơn vì:

- số parameter tăng mạnh;
- memory tăng;
- computation tăng;
- dễ overfit nếu dữ liệu không đủ;
- inference chậm hơn.

#### Depth có một khả năng đặc biệt: Composition

Một mang sâu thực hiện:
$$f(x) = f_L(f_{L-1}(...f_2(f_1(x))))$$

Tức là composition của nhiều hàm, vì vậy Depth cho phép model xây dựng representation theo nhiều bước biến đổi.

## Vì sao Depth thường quan trọng hơn Width?

Lý thuyết từ Universal Approximation cho biết:
- Một mạng có 1 hidden layer và rất nhiều neuron cũng có thể xấp xỉ mọi hàm liên tục.
- Tuy nhiên, để mạng “rất rộng” như vậy đạt được chất lượng tương đương, số neuron cần thiết có thể cực lớn.
Trong khi đó:
- Mạng sâu có thể biểu diễn cùng hàm đó nhưng với ít tham số hơn, nhờ cấu trúc phân tầng.
- Điều này đặc biệt đúng khi xử lý dữ liệu có tính phân cấp như ảnh (Module 9 – Computer Vision) hoặc văn bản (Module 10 – NLP).

Một cách giải thích khác là liên quan đến compositionality, giả sử một hàm có cấu trúc:

$$f(x) = f_3(f_2(f_1(x)))$$

Ta có thể xây dựng nó bằng nhiều transformation nhỏ. Thay vì cố học trực tiếp: $x \rightarrow y$

## Ví dụ thực tế

Giả sử bạn cần xây dựng mô hình nhận diện chữ số viết tay (MNIST).

### Trường hợp tăng Width:
- Cho hidden layer lên 2000–3000 neuron.
- Mạng học được khá nhiều đặc trưng đường thẳng, cong, góc cạnh.
- Nhưng các đặc trưng phức tạp như “cách một đường cong nối với một cạnh” khó biểu diễn hiệu quả chỉ với một tầng rộng.

### Trường hợp tăng Depth:
- Thêm 3–4 layer nhỏ.
- Tầng đầu học các nét cong hoặc thẳng đơn giản.
- Tầng sau ghép chúng thành các hình dạng mang ý nghĩa cao hơn: vòng tròn, móc, góc xiên,...
- Kết quả thường tốt hơn, với ít tham số hơn.

Trong nhiều dự án thực tế, các mô hình như CNN, Transformer đều dựa trên ý tưởng tăng depth để tạo ra biểu diễn có “tính phân cấp”.

## Góc nhìn khi làm dự án AI/ML

Khi thiết kế mô hình cho dự án:

- Width lớn → dễ gây quá khớp nếu dữ liệu không đủ.
- Depth lớn → cần chú ý vấn đề gradient biến mất hoặc nổ (kiến thức thường được học trong phần Deep Learning Layer – Module 7).
- Cả depth và width đều ảnh hưởng đến tài nguyên: bộ nhớ GPU, thời gian huấn luyện và khả năng triển khai.
- Cần xem bài toán có cấu trúc đặc thù không. Ví dụ:

Ảnh thường phù hợp với kiến trúc sâu dạng CNN.
Văn bản phù hợp với các mô hình sâu như Transformer.
Thiết kế tối ưu thường dựa vào thử nghiệm, logging và versioning (những bước phổ biến trong MLOps).

### Trong Transformer, Width và Depth càng rõ

Transformer thường có các tham số như:

- $d_{model}$ → liên quan đến width
- number of layers → depth
- number of attention heads → cấu trúc bên trong width

Transformer không chỉ tăng Width vì mỗi layer thực hiện một Transformation:

$$X_{l+1} = F_l (X_l)$$

Trong transformer:
```
X
 ↓
Self-Attention
 ↓
FFN
 ↓
Residual + Norm
 ↓
X₁
 ↓
Self-Attention
 ↓
FFN
 ↓
...
```

- Tăng depth nghĩa là: model được phép thực hiện thêm nhiều bước reasoning/transformation trên representation.

- Tăng width nghĩa là: mỗi bước transformation có không gian biểu diễn lớn hơn.

> Đây là distinction rất quan trọng.

Depth quá lớn thì model cần phải xử lý:
- Optimization: Gradient phải truyền qua nhiều transformation.
- Training cost Nhiều layer → nhiều computation.
- Inference latency: Các layer thường phải thực hiện tuần tự: $h_{l+1} = f_l(h_l)$ không thể đơn giản bọ qua dependency giữa chúng.

> Depth thường gây ảnh hưởng trực tiếp đến sequential latency.