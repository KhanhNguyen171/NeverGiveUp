# CNNs & Vision Transformer.

> CNN có xu hướng ưu tiên các đặc trưng cục bộ và cấu trúc của object; 
>
> ViT có khả năng mô hình hóa quan hệ toàn cục giữa object, background và các vùng khác của ảnh.
>
> CNN ưu tiên local/object; ViT mô hình hóa global/object + background

## Đặc điểm

- CNN sử dụng convolution:

$$ y_{i,j} = \sum_{u,v} K_{u,v}x_{i+u,j+v} $$

Mỗi neuron ban đầu chỉ nhìn một receptive field cục bộ. Qua nhiều layer, receptive field tăng lên và thông tin từ những vùng xa nhau có thể được kết hợp.

- Trong ViT, ảnh được chia thành patch:

$$ X \rightarrow \{x_1,x_2,\ldots,x_N\} $$

sau đó self-attention trực tiếp tính quan hệ giữa các patch:

$$ \operatorname{Attention}(Q,K,V) = \operatorname{softmax} \left( \frac{QK^T}{\sqrt{d}} \right)V $$

Do đó một patch có thể tương tác với nhiều patch khác ngay trong một attention layer.

Khó khăn của project: nếu thấy ViT chú ý đến background nhiều hơn CNN, không thể ngay lập tức kết luận:

> “Đó là vì Transformer hiểu global context.”

Có thể nguyên nhân là dataset, augmentation, pretraining, resolution, số lượng tham số hoặc cách visualization.

---

> ViT cũng chia ảnh thành các vùng nhỏ (patch). Điểm quyết định nó là “local” hay “global” không nằm ở việc chia patch, mà nằm ở cách các patch tương tác với nhau sau khi được tạo ra.

1. __CNN: local nằm ở chính phép convolution__

Giả sử ảnh là:

$$ X \in \mathbb{R}^{H\times W} $$

Một kernel $3\times3$ tại vị trí $(i,j)$ chỉ nhìn:

$$ \begin{bmatrix} x_{i-1,j-1} & x_{i-1,j} & x_{i-1,j+1}\\ x_{i,j-1} & x_{i,j} & x_{i,j+1}\\ x_{i+1,j-1} & x_{i+1,j} & x_{i+1,j+1} \end{bmatrix} $$

Tức là:

$$ y_{i,j}=f(x_{\text{local neighborhood}}) $$

Nó không thể trực tiếp lấy thông tin từ một vùng rất xa trong cùng phép convolution.

2. __ViT: Global nằm ở Self-Attention__

> ViT cũng chia patch — nhưng patch không phải receptive field cuối cùng

Giả sử ảnh: $ 224\times224 $ được chia thành patch: $ 16\times16 $ ta có: $ 14\times14=196 $ patch. Ta nhận được: $ X=[x_1,x_2,\ldots,x_{196}] $ Mỗi $x_i$ đúng là local region. Cho đến đây, ViT hoàn toàn local. Nhưng sau đó mới xuất hiện khác biệt.

> Nhưng đây chưa phải phần tạo ra global context.

Patch embedding biến: $ x_i \rightarrow z_i $ và tạo sequence: $ Z= [z_1,z_2,\ldots,z_N] $ Trong ViT, patch embedding có thể được implement bằng convolution với: $ kernel\_size=patch\_size $ và $ stride=patch\_size $.

> Globak xuất hiện ở Self-Attention

Với một token $z_i$, self-attention tính:

$$ q_i=W_Qz_i $$

và so sánh nó với tất cả token:

$$ K= \begin{bmatrix} k_1\\ k_2\\ \vdots\\ k_N \end{bmatrix} $$

Attention:

$$ \operatorname{Attention}(q_i,K,V) = \operatorname{softmax} \left( \frac{q_iK^T}{\sqrt d} \right)V $$

Ở đây:

$$ q_iK^T = [q_i k_1^T,\ q_i k_2^T,\ldots,q_i k_N^T] $$

Nghĩa là: __Patch $i$ có thể trực tiếp tương tác với patch 1, patch 2, ..., patch $N$.__ Không cần phải đi qua một chuỗi convolution layer để truyền thông tin.

---

### Bảng so sánh

|                          | CNN                | ViT                                   |
| ------------------------ | ------------------ | ------------------------------------- |
| Input                    | Pixel/feature map  | Patch/token                           |
| Đơn vị xử lý ban đầu     | Local neighborhood | Local patch                           |
| Operator                 | Convolution        | Self-attention                        |
| Một đơn vị tương tác với | Vùng lân cận       | Có thể với toàn bộ token              |
| Global interaction       | Qua nhiều layer    | Có thể ngay trong một attention layer |
| Inductive bias           | Locality mạnh      | Ít locality prior hơn                 |

> CNN chia sẻ kernel trên các vùng cục bộ và xây dựng receptive field lớn dần qua các layer; ViT cũng bắt đầu bằng các patch cục bộ, nhưng self-attention cho phép mỗi patch trực tiếp trao đổi thông tin với các patch khác trong sequence.