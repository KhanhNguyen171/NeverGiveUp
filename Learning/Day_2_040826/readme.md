# Loss Landscapes & Implicit Regularization of SGD
SGD (Stochastic Gradient Descent) không chỉ là một thuật toán tối ưu đơn thuần mà bản thân nó có một "lực ẩn" giúp mô hình tổng quát hóa tốt hơn (Implicit Bias).

- __Nội dung__: Phân tích hình học của không gian tổn thất (Loss Landscape) — mối liên hệ giữa độ phẳng của nghiệm cục bộ (_Flat Minima_) và khả năng Generalization.

- __Mở rộng vấn đề__: Tại sao SGD lại tự động tìm đến các Flat Minima thay vì Sharp Minima? Mối liên hệ giữa _Edge of Stability_ (khi Learning Rate lớn làm Loss dao động ở vùng biên) và tốc độ hội tụ của mô hình.

## Roadmap

1. Geometry của Loss Landscape
2. Hessian Spectrum và Curvature
3. Flat Minima vs Sharp Minima
4. SGD Noise như một quá trình Langevin Dynamics
5. Implicit Regularization của SGD
6. Learning Rate và Noise Scale
7. Edge of Stability (EoS)
8. Large Batch vs Small Batch
9. Generalization Theory

---

## Loss Landscape là gì?

Loss Landscape là hình học của hàm mất mát (Loss Function) trong không gian tham số (parameter space). Nó mô tả cách giá trị của hàm loss thay đổi khi các trọng số (weights) của mô hình thay đổi. Về mặt toán học:

$$L: \mathbb R^d \rightarrow \mathbb R$$

Trong đó:
- $d$: số lượng tham số của mô hình.
- $\theta \in \mathbb R^d$: vector chứa toàn bộ weights.
- $L(\theta)$: giá trị loss tương ứng với bộ weight đó.

Cụ thể hơn: $\theta \rightarrow L(\theta)$. Mỗi điểm trong không gian tham số tương ứng với một giá trị loss.

### Thành phần của Loss Landscape

Loss Landscape thường bao gồm:

- __Global Minimum__: điểm có loss nhỏ nhất.
    - Điểm có Loss nhỏ nhất trên toàn bộ Landscape.
    - Thường không thể tìm chính xác trong Deep Learning.

- __Local Minimum__: điểm thấp hơn các vùng lân cận nhưng không phải thấp nhất toàn cục.
    - Loss nhỏ hơn mọi điểm lân cận.
    - Có thể tồn tại rất nhiều trong mạng sâu.

- __Saddle Point__: gradient bằng 0 nhưng không phải cực tiểu.
    - Điểm có $\nabla L =0$ nhưng Hessian có cả eigenvalue dương và âm.
    - Đây không phải cực tiểu mà là giao điểm giữa hướng đi lên và đi xuống.

- __Flat Region__: vùng có độ cong nhỏ, loss thay đổi chậm.
    - Hessian có eigenvalue nhỏ.
    - Loss thay đổi chậm khi thay đổi tham số.
    - Thường liên quan đến khả năng tổng quát hóa tốt.

- __Sharp Region__: vùng có độ cong lớn, loss thay đổi nhanh.
    - Hessian có eigenvalue lớn.
    - Loss tăng nhanh khi thay đổi tham số.
    - Nhạy với nhiễu và perturbation.

### Vai trò trong Deep Learning

Loss Landscape quyết định:

- Quá trình __optimizer__ (SGD, Adam,...) di chuyển như thế nào.
- Mô hình hội tụ đến loại nghiệm nào (__Flat Minima__ hay __Sharp Minima__).
- Khả năng __generalization__ của mô hình sau khi huấn luyện.
- Độ ổn định của quá trình tối ưu.

> Loss Landscape là "bản đồ" của hàm mất mát trong không gian tham số, quyết định đường đi của optimizer và chất lượng nghiệm cuối cùng mà mô hình tìm được.

## 1. Geometry của Loss Landscape

Geometry của Loss Landscape là nghiên cứu hình dạng hình học của hàm mất mát trong không gian tham số (Parameter Space). Mỗi bộ trọng số của mô hình tương ứng với một điểm tỏng không gian tham số.

- 2 tham số $\rightarrow$ không gian 2D.
- 100 tham số $\rightarrow$ không gian 100D.
- 100 triệu tham số $\rightarrow$ không gian $10^8$ chiều.

__Loss Surface__: Nếu mỗi điểm $\theta$ có một giá trị Loss thì tập hợp tất cả các điểm tạo thành một Loss Surface. Bề mặt này bao gồm nhiều vùng hình học khác nhau:

- Basin (thung lũng)
- Ridge (sống núi)
- Valley (rãnh)
- Plateau (vùng phẳng)
- Saddle Point
- Local Minimum
- Global Minimum

__Curvature__: Gradient chỉ cho biết hướng đi, còn Curvature (độ cong) cho biết hình dạng của bề mặt. Curvature được mô tả bởi Hessian:

$$H = \nabla^2 L(\theta)$$

Hessian chứa thông tin về độ cong theo mọi hướng trong không gian tham số. Hessian Eigenvalues giả sử Hessian có các trị riêng: $\lambda_1, \lambda_2, ..., \lambda_d$ Các eigenvalue mô tả độ cong theo từng bước:

- $\lambda \gt 0$: cong lên (vùng cực tiểu cục bộ). Loss tăng khi rời khỏi nghiệm.
- $\lambda \lt 0$: cong xuống (vùng cực đại theo hướng đó). Tồn tại hướng làm Loss tiếp tục giảm.
- $\lambda \approx 0$: gần như phẳng. Loss thay đổi rất ít khi thay đổi tham số theo hướng đó.

Giá trị tuyệt đối của eigenvalue càng lớn thì độ cong càng lớn.

## 2. Hessian Spectrum và Curvature

### 2.1 Hessian là gì?

Gradient chỉ cho biết __hướng giảm của hàm Loss__, nhưng __không cho biết bề mặt cong như thế nào__.

Để mô tả hình học cục bộ của Loss Landscape, sử dụng __Hessian Matrix__.

$$H(\theta) = \nabla^2 L(\theta)$$

Trong đó:

$$H_{ij} = \frac {\partial^2 L} {\partial \theta_i \partial \theta_j}$$

Hessian là ma trận đạo hàm bậc hai, mô tả __độ cong (Curvature)__ của hàm Loss quanh một điểm $\theta$.

### 2.2 Curvature

Curvature là tốc độ thay đổi của Gradient.

Nếu khai triển Taylor bậc hai quanh nghiệm $\theta^*$:

$$L(\theta) \approx L(\theta^*) + \frac {1} {2} (\theta - \theta^*)^T H(\theta - \theta^*)$$

Ta thấy:
- Gradient quyết định hướng di chuyển.
- Hessian quyết định hình dạng của bề mặt quanh nghiệm.

Do đó Curvature là tính chất hình học cục bộ của Loss Landscape.

### 2.3 Hessian Spectrum

Hessian Spectrum là __tập hợp tất cả các eigenvalue của Hessian__.

Giả sử

$$H = Q \Lambda Q^T$$

Với:

$$\Lambda = diag(\lambda_1, \lambda_2, ..., \lambda_d)$$

Thì

$$\{\lambda_1, \lambda_2, ..., \lambda_d \}$$

được gọi là __Hessian Spectrum__.

Spectrum mô tả độ cong theo từng hướng trong không gian tham số.

## 3. Flat Minima vs Sharp Minima

### 3.1 Flat Minima

__Flat Minimum__ là nghiệm mà __Loss thay đổi rất ít khi tham số bị nhiễu nhỏ__. Về mặt toán học, nế một nhiễu nhỏ $\delta$: $L(\theta + \delta_ \approx L(\theta)$ thì nghiệm được xem là __Flat__.

Đặc điểm:
- Hessian có các eigenvalue nhỏ.
- Curvature thấp.
- Basin rộng.
- Ít nhạy với nhiễu hoặc perturbation của trọng số.
- Thường cho khả năng __generalization__ tốt hơn.

### 3.2 Sharp Minima

__Sharp Minimum__ là nghiệm mà __Loss tăng nhanh khi tham số thay đổi một lượng rất nhỏ__. Tức là: $L(\theta + \delta) \gg L(\theta)$ ngay cả khi $\delta$ rất nhỏ.

Đặc điểm:

- Hessian có một hoặc nhiều eigenvalue lớn.
- Curvature cao.
- Basin hẹp.
- Nhạy với perturbation của trọng số.
- Thường kém ổn định hơn đối với dữ liệu chưa thấy.

> Flat Minima không phải lúc nào cũng đảm bảo generalization tốt hơn. Các nghiên cứu như của Quoc V. Le và Laurent Dinh đã chỉ ra rằng khái niệm flatness phụ thuộc vào cách biểu diễn tham số (reparameterization). Vì vậy, trong nghiên cứu hiện đại, Flat Minima được xem là một chỉ báo hữu ích, không phải điều kiện đủ cho khả năng tổng quát hóa.

## 4. SGD Noise như một quá trình Langevin Dynamics

Gradient của SGD không được tính trên toàn bộ dataset mà chỉ trên một mini-batch. Vì vậy, gradient thu được chỉ là một xấp xỉ của gradient thật:

$$g(\theta) = \nabla L(\theta) + \xi$$

Trong đó:
- $\nabla L(\theta)$: gradient của toàn bộ dữ liệu.
- $\xi$: nhiễu ngẫu nhiên (stochastic noise) do lấy mẫu mini-batch.

Do đó, quy tắc cập nhật của SGD trở thành:

$$\theta_{t+1} = \theta_t - \eta (\nabla L(\theta_t) + \xi_t)$$

Khác với Gradient Descent, SGD luôn chứa một thành phần ngẫu nhiên trong mỗi bước cập nhật.

### Liên hệ với langevin Dynamics

Khi __learning rate nhỏ__ và __batch size đủ lớn__, động lực học của SGD có thể được xấp xỉ bởi __Stochastic Differential Equation (SDE)__:

$$d\theta = - \nabla L(\theta) dt + \sqrt{2D} dW_t$$

trong đó:

- Thành phần $-\nabla L(\theta)$ kéo tham số đi về vùng có loss thấp.
- Thành phần $dW_t$ là __Brownian Motion__, biểu diễn nhiễu ngẫu nhiên.
- $D$ là hệ số khuếch tán (diffusion coefficient), phụ thuộc vào learning rate và batch size.

Mô hình này chính là __Langevin Dynamics__.

### Ý nghĩa
Nhờ thành phần nhiễu, SGD không chỉ đi theo hướng giảm loss mà còn __dao động quanh nghiệm__, giúp:

- thoát khỏi các vùng cực tiểu hẹp (Sharp Minima),
- khám phá nhiều vùng nghiệm hơn,
- có xu hướng hội tụ đến các __Flat Minima__.

Đây là cơ sở lý thuyết của __Implicit Regularization__ trong SGD.