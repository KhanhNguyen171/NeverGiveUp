# Learning Mechanics: Hướng tới một lý thuyết khoa học về Deep Learning

> **Dựa trên:** *There Will Be a Scientific Theory of Deep Learning*
> **arXiv:** [2604.21691](https://arxiv.org/pdf/2604.21691)

---

## 1. Luận điểm trung tâm

Deep Learning đã đạt được những thành công vượt trội về mặt thực nghiệm, nhưng quá trình phát triển vẫn phụ thuộc nhiều vào thực nghiệm, mở rộng quy mô mô hình và tìm kiếm hyperparameter. Chúng ta có thể huấn luyện những mô hình ngày càng lớn, nhưng vẫn chưa có một lý thuyết thống nhất có khả năng dự đoán **mạng neural học như thế nào** từ kiến trúc, dữ liệu, khởi tạo và phương pháp tối ưu.

Luận điểm trung tâm của bài báo là:

$$
\boxed{
\text{Deep Learning nên được nghiên cứu như một hệ động lực được chi phối bởi các quy luật toán học có thể khám phá.}
}
$$

Các tác giả gọi chương trình nghiên cứu này là **Learning Mechanics** — **cơ học của quá trình học**.

Mục tiêu không phải chủ yếu là đề xuất thêm một kiến trúc neural network mới, mà là tìm hiểu phép biến đổi:

$$
(\mathcal{A},\mathcal{D},\mathcal{I},\mathcal{O})
\longrightarrow
\mathcal{T}
\longrightarrow
(\Theta,\mathcal{R},\mathcal{P}),
$$

trong đó:

* $\mathcal{A}$: kiến trúc;
* $\mathcal{D}$: dữ liệu huấn luyện;
* $\mathcal{I}$: phương pháp khởi tạo;
* $\mathcal{O}$: thuật toán tối ưu;
* $\mathcal{T}$: động lực học trong quá trình học;
* $\Theta$: các tham số sau huấn luyện;
* $\mathcal{R}$: biểu diễn được học;
* $\mathcal{P}$: hiệu năng đạt được.

Câu hỏi khoa học cốt lõi trở thành:

> **Liệu chúng ta có thể suy ra các quy luật toán học dự đoán động lực học và kết quả học của neural network, thay vì chỉ quan sát chúng sau khi huấn luyện hay không?**

---

# 2. Từ Deep Learning Engineering đến Learning Mechanics

Quy trình Deep Learning truyền thống có thể mô tả:

```text
Kiến trúc
    ↓
Huấn luyện
    ↓
Đánh giá
    ↓
Điều chỉnh hyperparameter
    ↓
Mô hình tốt hơn
```

Cách tiếp cận này cực kỳ hiệu quả về mặt kỹ thuật, nhưng phần lớn vẫn mang tính thực nghiệm.

Learning Mechanics đề xuất một góc nhìn khác:

```text
Kiến trúc
      +
Dữ liệu
      +
Khởi tạo
      +
Bộ tối ưu
      ↓
Động lực học học
      ↓
Hình thành biểu diễn
      ↓
Tiến hóa tham số
      ↓
Khả năng tổng quát hóa
```

Mục tiêu là tìm một mô tả có số chiều thấp hơn cho quá trình vốn diễn ra trong không gian tham số cực kỳ lớn.

Gọi

$$
\theta_t
$$

là toàn bộ tham số của mạng tại thời điểm $t$. Với gradient descent:

$$
\theta_{t+1}
=
\theta_t
-
\eta
\nabla_\theta
\mathcal{L}(\theta_t).
$$

Phương trình này rất đơn giản, nhưng số lượng tham số có thể lên tới hàng triệu hoặc hàng tỷ.

Do đó, một lý thuyết khoa học không nhất thiết phải theo dõi từng tham số riêng lẻ. Thay vào đó, nó cần tìm những đại lượng vĩ mô tuân theo các quy luật đơn giản:

$$
\boxed{
\text{Động lực học vi mô của tham số}
\longrightarrow
\text{Quy luật học vĩ mô}
}
$$

Điều này tương tự **cơ học thống kê**, nơi hành vi của một hệ gồm rất nhiều hạt được mô tả thông qua một số đại lượng vĩ mô như nhiệt độ, áp suất hoặc entropy.

---

# 3. Chiến lược lý thuyết của bài báo

Bài báo tập hợp bằng chứng cho Learning Mechanics thông qua một chuỗi hướng tiếp cận:

$$
\boxed{
\text{Mô hình giải được}
\rightarrow
\text{Các giới hạn đơn giản hóa}
\rightarrow
\text{Quy luật thực nghiệm}
\rightarrow
\text{Lý thuyết hyperparameter}
\rightarrow
\text{Tính phổ quát}
}
$$

Mỗi hướng trả lời một câu hỏi khác nhau:

| Hướng tiếp cận           | Mục tiêu                                |
| ------------------------ | --------------------------------------- |
| Mô hình giải được        | Thu được kết quả toán học chính xác     |
| Các giới hạn             | Đơn giản hóa mạng rất rộng hoặc rất sâu |
| Quy luật thực nghiệm     | Tìm các quy luật vĩ mô ổn định          |
| Lý thuyết hyperparameter | Dự đoán hành vi khi quy mô thay đổi     |
| Tính phổ quát            | Tìm hành vi chung giữa nhiều kiến trúc  |

Đây là cấu trúc lý luận quan trọng nhất của bài báo.

---

# 4. Mô hình giải được I: Deep Linear Network

Deep Linear Network có dạng:

$$
f(x)
=
W_LW_{L-1}\cdots W_2W_1x.
$$

Mặc dù mạng tuyến tính theo $x$, nó không tuyến tính theo các tham số vì các ma trận được nhân với nhau.

Ví dụ:

$$
f(x)
=
W_3W_2W_1x.
$$

Điều này khiến Deep Linear Network phức tạp hơn linear regression nhưng vẫn đủ đơn giản để phân tích toán học.

Nó cho phép nghiên cứu:

* động lực học tối ưu;
* implicit bias;
* tương tác giữa các layer;
* động lực học singular value;
* quá trình học các cấu trúc hạng thấp.

---

## 4.1 Greedy Low-Rank Learning

Giả sử phép biến đổi mục tiêu có phân rã SVD:

$$
M^\star
=
U\Sigma V^\top,
$$

với

$$
\Sigma
=
\operatorname{diag}
(\sigma_1,\sigma_2,\ldots,\sigma_r),
\qquad
\sigma_1\geq\sigma_2\geq\cdots\geq\sigma_r.
$$

Mạng không nhất thiết học tất cả các hướng singular cùng lúc.

Thay vào đó, những mode có singular value lớn thường được học trước:

$$
\sigma_1
\rightarrow
\sigma_2
\rightarrow
\sigma_3
\rightarrow
\cdots.
$$

Hiện tượng này được gọi là **Greedy Low-Rank Learning**.

Ý nghĩa quan trọng là:

$$
\boxed{
\text{Bản thân quá trình tối ưu tạo ra sự ưu tiên đối với một số biểu diễn.}
}
$$

Do đó, nghiệm cuối cùng không chỉ được quyết định bởi hàm loss.

**Quỹ đạo tối ưu cũng đóng vai trò quyết định.**

---

# 5. Mô hình giải được II: Neural Tangent Kernel

Một cách đơn giản hóa quan trọng khác là tuyến tính hóa neural network xung quanh điểm khởi tạo.

Cho:

$$
f(x;\theta)
$$

là một neural network được khởi tạo tại $\theta_0$.

Khai triển Taylor bậc nhất:

$$
f(x;\theta)
\approx
f(x;\theta_0)
+
\nabla_\theta f(x;\theta_0)^\top
(\theta-\theta_0).
$$

Đặt:

$$
\phi(x)
=
\nabla_\theta f(x;\theta_0).
$$

Khi đó:

$$
f(x;\theta)
\approx
f(x;\theta_0)
+
\phi(x)^\top(\theta-\theta_0).
$$

Từ đó định nghĩa **Neural Tangent Kernel — NTK**:

$$
\boxed{
K(x,x')
=
\nabla_\theta f(x;\theta_0)^\top
\nabla_\theta f(x';\theta_0)
}
$$

Trong các giới hạn về độ rộng thích hợp, quá trình huấn luyện neural network có thể tiến gần tới kernel regression.

Về mặt khái niệm:

$$
\boxed{
\text{Neural Network}
\longrightarrow
\text{Kernel Method}
}
$$

Điều này tạo ra một mô hình toán học rất thuận lợi để phân tích động lực học học.

---

# 6. Giới hạn của NTK

NTK mạnh chính bởi vì network gần như không thay đổi nhiều so với trạng thái khởi tạo.

Đặt:

$$
\Delta\theta
=
\theta_t-\theta_0.
$$

Trong **lazy regime**:

$$
\Delta\theta\approx 0.
$$

Do đó:

$$
\nabla_\theta f(x;\theta_t)
\approx
\nabla_\theta f(x;\theta_0).
$$

Biểu diễn gần như được giữ cố định.

Vì vậy:

$$
\boxed{
\text{NTK}
\Rightarrow
\text{tính khả giải về mặt toán học}
}
$$

nhưng nhìn chung:

$$
\boxed{
\text{NTK}
\not\Rightarrow
\text{giải thích đầy đủ quá trình học feature}
}
$$

Đây là một thách thức quan trọng.

Một lý thuyết hoàn chỉnh phải giải thích không chỉ trường hợp network gần như giữ nguyên representation, mà cả trường hợp network thực sự **thay đổi representation để học feature mới**.

---

# 7. Lazy Learning và Rich Feature Learning

Các mạng nonlinear cho thấy ít nhất hai chế độ học khác nhau.

## 7.1 Lazy Regime

Tham số vẫn gần với trạng thái khởi tạo:

$$
\|\theta_t-\theta_0\|
\ll
\|\theta_0\|.
$$

Network chủ yếu thay đổi hàm đầu ra trong khi representation gần như cố định.

Chế độ này có quan hệ chặt chẽ với kernel method.

---

## 7.2 Rich Regime

Tham số thay đổi đáng kể:

$$
\|\theta_t-\theta_0\|
=
O(1),
$$

và representation thay đổi:

$$
h_t(x)
\neq
h_0(x).
$$

Network thực sự học feature.

Có thể tóm tắt:

$$
\boxed{
\text{Lazy Learning}
\approx
\text{Fitting hàm với feature gần cố định}
}
$$

trong khi:

$$
\boxed{
\text{Rich Learning}
\approx
\text{Học feature}
+
\text{Fitting hàm}
}
$$

Việc hiểu sự chuyển tiếp giữa hai chế độ này là một trong những bài toán trung tâm của Learning Mechanics.

---

# 8. Các giới hạn toán học

Mạng neural hiện đại có số lượng tham số rất lớn.

Một chiến lược quan trọng là nghiên cứu các giới hạn có kiểm soát.

## 8.1 Infinite Width

Cho độ rộng mạng là $n$.

Thay vì xét $n$ hữu hạn, xét:

$$
n\rightarrow\infty.
$$

Thay vì theo dõi từng neuron:

$$
w_1,w_2,\ldots,w_n,
$$

ta có thể nghiên cứu một phân phối:

$$
\rho_t(w).
$$

Do đó:

$$
\boxed{
\text{Động lực học từng neuron}
\longrightarrow
\text{Động lực học của toàn bộ quần thể}
}
$$

Đây là tư tưởng tương tự giới hạn nhiệt động lực học trong vật lý thống kê.

---

## 8.2 Infinite Depth

Xét một residual network:

$$
x_{l+1}
=
x_l
+
\frac{1}{L}f(x_l,\theta_l).
$$

Khi:

$$
L\rightarrow\infty,
$$

mạng rời rạc có thể tiến tới một hệ động lực liên tục:

$$
\frac{dx(t)}{dt}
=
f(x(t),\theta(t)).
$$

Do đó:

$$
\boxed{
\text{Deep Residual Network}
\longrightarrow
\text{Hệ động lực liên tục}
}
$$

Điều này cho phép sử dụng các công cụ của dynamical systems để nghiên cứu neural network.

---

# 9. Các quy luật thực nghiệm

Một lý thuyết khoa học phải giải thích được những quy luật ổn định xuất hiện trong thực nghiệm.

Một nhóm quan trọng là **scaling laws**.

Ví dụ:

$$
L(C)
\propto
C^{-\alpha},
$$

trong đó:

* $L$: test loss;
* $C$: lượng compute;
* $\alpha$: số mũ scaling.

Tương tự:

$$
L(N)
\propto
N^{-\alpha_N},
$$

và:

$$
L(D)
\propto
D^{-\alpha_D},
$$

mô tả sự phụ thuộc của loss vào model size $N$ và dataset size $D$.

Điểm quan trọng không chỉ là quan sát thấy power law.

Câu hỏi sâu hơn là liệu ta có thể dự đoán:

$$
\boxed{
\alpha
=
f(
\text{kiến trúc},
\text{dữ liệu},
\text{optimizer},
\text{chế độ huấn luyện}
)
}
$$

từ những nguyên lý cơ bản hay không.

---

# 10. Edge of Stability

Một ví dụ khác về quy luật vĩ mô liên quan đến Hessian.

Định nghĩa:

$$
H(\theta)
=
\nabla_\theta^2\mathcal{L}(\theta).
$$

Eigenvalue lớn nhất của Hessian là:

$$
\lambda_{\max}(H).
$$

Trong gradient descent với learning rate $\eta$, một hiện tượng đáng chú ý là:

$$
\boxed{
\lambda_{\max}(H)
\approx
\frac{2}{\eta}
}
$$

trong những giai đoạn quan trọng của quá trình huấn luyện.

Hiện tượng này được gọi là **Edge of Stability**.

Ý nghĩa là một quá trình tối ưu có hàng triệu hoặc hàng tỷ tham số có thể được mô tả thông qua một đại lượng vĩ mô:

$$
\theta
\longrightarrow
H(\theta)
\longrightarrow
\lambda_{\max}(H).
$$

Đây chính xác là loại quy luật mà Learning Mechanics muốn giải thích.

---

# 11. Neural Collapse

Một hiện tượng quan trọng khác xuất hiện trong hình học của representation.

Cho:

$$
h_i
$$

là representation của sample $i$, và:

$$
\mu_c
=
\frac{1}{N_c}
\sum_{i:y_i=c}h_i
$$

là representation trung bình của class $c$.

Ở cuối quá trình huấn luyện, có thể xuất hiện:

$$
h_i
\approx
\mu_c,
\qquad
y_i=c.
$$

Do đó:

$$
\operatorname{Var}(h_i\mid y_i=c)
\rightarrow
0.
$$

Các representation cùng class tập trung lại, trong khi class means có xu hướng trở nên có cấu trúc hình học rất đều và tách biệt.

Điều quan trọng là cấu trúc này không nhất thiết được quy định trực tiếp bởi architecture.

Nó xuất hiện từ quá trình học:

$$
\boxed{
\text{Training}
\rightarrow
\text{Hình học có cấu trúc của representation}
}
$$

Neural Collapse vì vậy là bằng chứng rằng representation được học có thể tuân theo các quy luật toán học mang tính phổ quát.

---

# 12. Symmetry và Conservation Laws

Neural network chứa nhiều đối xứng trong không gian tham số.

Ví dụ, một số phép rescaling giữa các layer có thể giữ nguyên hàm mà network biểu diễn.

Những đối xứng này có thể dẫn tới các đại lượng được bảo toàn trong quá trình tối ưu.

Đối với Deep Linear Network, các đại lượng dạng:

$$
W_\ell W_\ell^\top
-
W_{\ell+1}^\top W_{\ell+1}
$$

có thể được bảo toàn dưới động lực học thích hợp:

$$
\frac{d}{dt}
\left(
W_\ell W_\ell^\top
-
W_{\ell+1}^\top W_{\ell+1}
\right)
=
0.
$$

Từ đó xuất hiện mối liên hệ:

$$
\boxed{
\text{Đối xứng}
\longrightarrow
\text{Định luật bảo toàn}
\longrightarrow
\text{Động lực học học}
}
$$

Đây là một connection trực tiếp với cách vật lý sử dụng symmetry để tìm conservation laws.

---

# 13. Scaling của Hyperparameter

Một lý thuyết hoàn chỉnh không chỉ phải giải thích network học gì, mà còn phải giải thích cách hyperparameter thay đổi khi mô hình được scale.

Giả sử width thay đổi:

$$
d
\rightarrow
kd.
$$

Trong cách tiếp cận thông thường, ta có thể phải tìm lại learning rate tối ưu:

$$
\eta^\star(d)
\rightarrow
\eta^\star(kd).
$$

Điều này gây ra vấn đề lớn khi huấn luyện các mô hình lớn.

Các lý thuyết parameterization như **Maximal Update Parameterization — μP** tìm cách lựa chọn scaling để động lực học có ý nghĩa được duy trì khi width thay đổi.

Một dạng scaling tổng quát:

$$
\eta
=
\eta_0d^c.
$$

Mục tiêu là lựa chọn scaling sao cho các đại lượng quan trọng vẫn có giới hạn tốt khi:

$$
d\rightarrow\infty.
$$

Từ đó có thể hướng tới:

$$
\boxed{
\text{Tuning trên mô hình nhỏ}
\longrightarrow
\text{Chuyển hyperparameter sang mô hình lớn}
}
$$

Đây là ví dụ rõ ràng về việc lý thuyết có thể tạo ra lợi ích trực tiếp cho thực hành.

---

# 14. Tính phổ quát giữa các kiến trúc

Bài báo đặt ra một câu hỏi sâu hơn.

Nếu:

$$
\text{CNN}
\neq
\text{ResNet}
\neq
\text{Transformer}
\neq
\text{U-Net},
$$

tại sao chúng vẫn có thể xuất hiện những hành vi học tương tự?

Câu trả lời không phải là các architecture này giống nhau.

Thay vào đó, các kiến trúc khác nhau ở cấp độ vi mô có thể tạo ra những quy luật tương tự ở cấp độ vĩ mô:

$$
\boxed{
\text{Kiến trúc vi mô khác nhau}
\longrightarrow
\text{Quy luật vĩ mô chung}
}
$$

Đây là ý tưởng về **universality — tính phổ quát**.

Những hiện tượng có thể mang tính phổ quát gồm:

* scaling laws;
* hình học representation;
* feature learning;
* các hiện tượng tối ưu;
* cấu trúc representation cuối cùng.

---

# 15. CNN, Transformer và U-Net

Các architecture như CNN, ResNet, Transformer và U-Net trong bài báo **không phải kiến trúc mới được đề xuất**.

Chúng được sử dụng như những hệ thống thực nghiệm để kiểm tra tính phổ quát.

Câu hỏi là:

$$
\text{Architecture có quyết định tất cả hay không?}
$$

Bằng chứng được trình bày cho thấy:

$$
\boxed{
\text{Architecture quan trọng}
\quad\text{nhưng}\quad
\text{Architecture không phải toàn bộ lời giải thích}.
}
$$

Behavior cuối cùng còn phụ thuộc vào:

$$
\mathcal{A},
\mathcal{D},
\mathcal{I},
\mathcal{O},
\mathcal{S},
$$

trong đó $\mathcal{S}$ biểu diễn quy mô mô hình.

---

# 16. Universal Representation

Một khả năng mạnh hơn là các mạng khác nhau nhưng cùng giải một bài toán có thể học những representation tương tự nhau.

Cho:

$$
h_A(x)
$$

và

$$
h_B(x)
$$

là representation của hai mô hình khác nhau.

Ngay cả khi:

$$
\mathcal{A}_A
\neq
\mathcal{A}_B,
$$

representation có thể ngày càng tương đồng khi quy mô và hiệu năng tăng:

$$
h_A(x)
\approx
T(h_B(x)),
$$

với $T$ là một phép biến đổi thích hợp.

Điều này dẫn tới **Platonic Representation Hypothesis**:

> Các mô hình có hiệu năng cao, được huấn luyện trên cùng một cấu trúc dữ liệu, có thể hội tụ về những representation tương tự nhau.

Nếu hiện tượng này có tính phổ quát, nó cho thấy representation không chỉ được quyết định bởi architecture mà còn chịu ảnh hưởng mạnh từ cấu trúc của dữ liệu.

---

# 17. Dữ liệu là một thành phần nền tảng

Một lý thuyết về Deep Learning không thể chỉ tập trung vào model.

Dữ liệu được sinh ra từ một phân phối:

$$
x\sim P_{\mathrm{data}}.
$$

Dữ liệu tự nhiên thường chứa:

* cấu trúc chiều thấp;
* tính phân cấp;
* tính thưa;
* tính tổ hợp;
* tương quan đa tỉ lệ;
* phân phối heavy-tailed;
* power-law.

Do đó quá trình học phải được nhìn nhận như:

$$
\boxed{
\text{Kiến trúc}
+
\text{Tối ưu}
+
\text{Cấu trúc dữ liệu}
\longrightarrow
\text{Hành vi được học}
}
$$

Đây là một phần quan trọng để giải thích tại sao các architecture khác nhau vẫn có thể học những hàm hoặc representation tương tự.

---

# 18. Learning Mechanics và Mechanistic Interpretability

Bài báo liên hệ Learning Mechanics với **Mechanistic Interpretability**.

Mechanistic Interpretability hỏi:

> **Mạng đã học được gì?**

Learning Mechanics hỏi:

> **Tại sao mạng học được điều đó và thông qua động lực học nào?**

Hai hướng nghiên cứu bổ sung cho nhau.

Có thể hình dung:

$$
\text{Dữ liệu}
\rightarrow
\text{Tối ưu}
\rightarrow
\text{Feature}
\rightarrow
\text{Circuit}
\rightarrow
\text{Behavior}.
$$

Mechanistic Interpretability chủ yếu nghiên cứu phần:

$$
\text{Feature}
\rightarrow
\text{Circuit}
\rightarrow
\text{Behavior}.
$$

Learning Mechanics muốn giải thích phần:

$$
\text{Dữ liệu}
+
\text{Kiến trúc}
+
\text{Tối ưu}
\rightarrow
\text{Feature}.
$$

Do đó:

$$
\boxed{
\text{Learning Mechanics}
+
\text{Mechanistic Interpretability}
}
$$

có thể tạo thành một framework vừa giải thích **vì sao network học**, vừa giải thích **network đã học cơ chế gì**.

---

# 19. Một lý thuyết khoa học về Deep Learning cần giải thích điều gì?

Có thể hình dung mục tiêu của theory theo các cấp độ.

### Cấp độ 1 — Optimization

Giải thích:

$$
\theta_0
\rightarrow
\theta_t.
$$

Các tham số tiến hóa như thế nào?

### Cấp độ 2 — Representation

Giải thích:

$$
h_0(x)
\rightarrow
h_t(x).
$$

Feature hữu ích hình thành như thế nào?

### Cấp độ 3 — Function

Giải thích:

$$
f_0(x)
\rightarrow
f_t(x).
$$

Hàm ánh xạ input-output thay đổi như thế nào?

### Cấp độ 4 — Generalization

Giải thích:

$$
\mathcal{L}_{\mathrm{train}}
\rightarrow
\mathcal{L}_{\mathrm{test}}.
$$

Tại sao mô hình tổng quát hóa?

### Cấp độ 5 — Universality

Giải thích tại sao các quy luật tương tự xuất hiện xuyên qua:

$$
\text{architecture}
\times
\text{dataset}
\times
\text{scale}.
$$

Một lý thuyết trưởng thành cuối cùng phải liên kết được cả năm cấp độ.

---

# 20. Bức tranh lý thuyết hiện tại

Bài báo không cho rằng một lý thuyết hiện có đã giải thích toàn bộ Deep Learning.

Thay vào đó, nhiều lý thuyết khác nhau đang giải thích những chế độ khác nhau:

```text
                         Deep Learning
                              │
             ┌────────────────┼────────────────┐
             │                │                │
      Deep Linear           NTK          Mean-Field
             │                │                │
      Động lực chính xác   Lazy regime   Infinite width
             │                │                │
             └────────────────┼────────────────┘
                              │
                    Rich Feature Learning
                              │
                    Nonlinear Networks
                              │
                   Natural Data + Scale
                              │
                         ??? Theory ???
```

Khoảng trống lớn nhất là một framework đồng thời xử lý được:

$$
\boxed{
\text{phi tuyến}
+
\text{feature learning}
+
\text{depth}
+
\text{width}
+
\text{natural data}
+
\text{tối ưu thực tế}.
}
$$

Đây chính là bài toán mở trung tâm mà bài báo muốn thúc đẩy.

---

# 21. Thực chất bài báo đang đề xuất điều gì?

Cần phân biệt rõ đóng góp của bài báo với một paper Machine Learning thông thường.

Bài báo **không đề xuất**:

$$
\boxed{
\text{Kiến trúc mới}
\rightarrow
\text{Benchmark mới}
\rightarrow
\text{Accuracy cao hơn}
}
$$

Thay vào đó, nó đề xuất một **chương trình nghiên cứu**:

$$
\boxed{
\text{Deep Learning}
\rightarrow
\text{Learning Mechanics}
\rightarrow
\text{Scientific Theory}
}
$$

Các bằng chứng được tổng hợp từ:

$$
\begin{aligned}
&\text{Deep Linear Networks},\\
&\text{Neural Tangent Kernel},\\
&\text{Mean-Field Limits},\\
&\text{Lazy/Rich Dynamics},\\
&\text{Scaling Laws},\\
&\text{Edge of Stability},\\
&\text{Neural Collapse},\\
&\text{Conservation Laws},\\
&\text{μP},\\
&\text{Universality}.
\end{aligned}
$$

Đây không phải những kết quả hoàn toàn độc lập.

Chúng được trình bày như các bằng chứng cho thấy quá trình huấn luyện neural network có **cấu trúc lặp lại và có thể mô tả bằng toán học**.

---

# 22. Góc nhìn thống nhất

Toàn bộ các ý tưởng chính của bài báo có thể quy về framework:

$$
\boxed{
\begin{array}{c}
\text{Kiến trúc}\\
\mathcal{A}
\end{array}
+
\begin{array}{c}
\text{Dữ liệu}\\
\mathcal{D}
\end{array}
+
\begin{array}{c}
\text{Khởi tạo}\\
\mathcal{I}
\end{array}
+
\begin{array}{c}
\text{Optimizer}\\
\mathcal{O}
\end{array}
}
$$

$$
\Downarrow
$$

$$
\boxed{
\text{Động lực học học}
}
$$

$$
\Downarrow
$$

$$
\begin{array}{ccc}
\text{Weights} & \text{Representation} & \text{Function}\\
\Theta & \mathcal{R} & f
\end{array}
$$

$$
\Downarrow
$$

$$
\boxed{
\text{Generalization}
}
$$

Learning Mechanics tìm cách xây dựng một lý thuyết:

$$
\mathcal{T}
=
\mathcal{T}
(
\mathcal{A},
\mathcal{D},
\mathcal{I},
\mathcal{O}
)
$$

sao cho:

$$
\mathcal{T}
\Rightarrow
\text{các quy luật có khả năng dự đoán}.
$$

Mục tiêu không phải mô phỏng chính xác từng bước cập nhật của từng parameter, mà là dự đoán những **đại lượng quan sát vĩ mô quan trọng**.

---

# 23. Các nguyên lý cốt lõi cần ghi nhớ

## Nguyên lý 1 — Optimization là một phần của quá trình học

Nghiệm được học không chỉ phụ thuộc vào:

$$
\mathcal{L}(\theta)
$$

mà còn phụ thuộc vào quỹ đạo tối ưu:

$$
\theta_0
\xrightarrow{\text{optimizer}}
\theta_1
\xrightarrow{}
\cdots
\xrightarrow{}
\theta_T.
$$

Do đó:

$$
\boxed{
\text{Objective}
\neq
\text{Learning Dynamics}.
}
$$

---

## Nguyên lý 2 — Feature Learning khác fundamentally với Kernel Fitting

$$
\text{Lazy}
\Rightarrow
\text{feature gần cố định},
$$

trong khi:

$$
\text{Rich}
\Rightarrow
\text{feature được học}.
$$

Một theory hoàn chỉnh phải giải thích cả hai.

---

## Nguyên lý 3 — Scaling tạo ra cấu trúc lý thuyết

Các giới hạn:

$$
n\rightarrow\infty,
\qquad
L\rightarrow\infty
$$

có thể biến một neural network khó phân tích thành một hệ thống có thể nghiên cứu bằng toán học.

---

## Nguyên lý 4 — Hệ phức tạp có thể xuất hiện quy luật đơn giản

Ví dụ:

$$
L\propto C^{-\alpha},
$$

$$
\lambda_{\max}(H)\approx\frac{2}{\eta},
$$

và hình học Neural Collapse.

Điều này cho thấy động lực học hàng triệu chiều có thể chứa cấu trúc hiệu dụng với số chiều thấp hơn nhiều.

---

## Nguyên lý 5 — Architecture quan trọng nhưng không đủ

Hành vi được học phụ thuộc đồng thời vào:

$$
\boxed{
\mathcal{A}
+
\mathcal{D}
+
\mathcal{I}
+
\mathcal{O}
+
\mathcal{S}
}
$$

chứ không chỉ architecture.

---

## Nguyên lý 6 — Có thể tồn tại tính phổ quát

Các architecture khác nhau có thể xuất hiện những hành vi vĩ mô tương tự:

$$
\text{CNN}
\sim
\text{ResNet}
\sim
\text{Transformer}
\sim
\text{U-Net}.
$$

Không phải vì chúng giống nhau về mặt toán học, mà vì một số quy luật của quá trình học có thể mang tính phổ quát.

---

# 24. Kết luận

Thông điệp sâu nhất của bài báo là một **sự thay đổi góc nhìn khoa học**.

Deep Learning truyền thống thường đặt câu hỏi:

$$
\boxed{
\text{Kiến trúc nào có performance tốt nhất?}
}
$$

Learning Mechanics đặt câu hỏi:

$$
\boxed{
\text{Những quy luật toán học nào quyết định cách một kiến trúc học?}
}
$$

Hai câu hỏi này có mục tiêu khác nhau.

Câu hỏi thứ nhất thúc đẩy **kỹ thuật xây dựng mô hình tốt hơn**.

Câu hỏi thứ hai hướng tới **một lý thuyết khoa học về Deep Learning**.

Bài báo cho rằng chúng ta đã có nhiều mảnh ghép quan trọng:

$$
\boxed{
\begin{aligned}
&\text{Deep Linear Dynamics}\\
&+\text{NTK}\\
&+\text{Mean-Field Theory}\\
&+\text{Lazy/Rich Dynamics}\\
&+\text{Scaling Laws}\\
&+\text{Edge of Stability}\\
&+\text{Neural Collapse}\\
&+\text{Conservation Laws}\\
&+\text{μP}\\
&+\text{Universality}
\end{aligned}
}
$$

Thách thức hiện tại là hợp nhất các kết quả riêng lẻ này thành một framework có khả năng giải thích Deep Learning thực tế.

Mục tiêu cuối cùng là:

$$
\boxed{
\text{Kiến trúc}
+
\text{Dữ liệu}
+
\text{Tối ưu}
\overset{\text{Learning Mechanics}}{\longrightarrow}
\text{Các quy luật học có khả năng dự đoán}
}
$$

Một lý thuyết hoàn chỉnh sẽ không chỉ cho biết **mô hình học được gì**, mà còn phải giải thích:

$$
\boxed{
\text{học cái gì},
\qquad
\text{học như thế nào},
\qquad
\text{khi nào tổng quát hóa},
\qquad
\text{và tại sao các architecture khác nhau có thể xuất hiện hành vi tương tự}.
}
$$

Đó chính là chương trình nghiên cứu mà *There Will Be a Scientific Theory of Deep Learning* muốn truyền tải đến người đọc.
