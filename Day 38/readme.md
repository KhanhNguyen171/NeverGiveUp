# Drone, Quay 3D và Định hướng không gian

> Drone giữ thẳng bằng, nghiên và đổi hướng bằng mô hình nào?

![](img/DroneAi.png)

1. __Bài toán thực tế:__ Drone phải biết nó đang nghiên, quay và hướng về đâu trong không gian 3D.

2. __Mô hình hình học:__ Định hướng của Drone được mô tả bằng ma trận quay, Ma trận quay bảo toàn độ dài, góc và định hướng.

3. __Công thức lõi:__ Ma trận quay mô tả định hướng của drone và bảo toàn độ dài, góc và định hướng.

$$R^T R = I$$

$$det R = 1$$

$$n = \frac {u \times v} {||u \times v ||}$$


4. __Minh họa đúng bản chất:__ Các trục, góc quay và mặt phẳng được biểu diễn rõ ràng theo hệ tọa độ.

5. __Ứng dụng mở rộng:__ Mô hình định hướng giúp drone bay chính xác và mang cảm biến hoạt động ổn định.

![Image](https://images.openai.com/static-rsc-4/eebCoBq2qz9HpgZ-J6JMNuLuJtmry4V6-tnvLUADV6vaVysej-z4njHrHvM1X4Jgloi-QbGPNmsCqc8p_P0aDLmZ1vNgPQx_wiITTSMZzqUZpoqVl3K_RCX4cTBaMOxItMWTBnBWtCnYlu0pfOPiCx7kCu7AF-ZN7iJzjFI2tnRh9kfSuyvcDJstdKZNEFZi?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/OhkPdrpgAHtwkuhntgtobHU6WuU9Q__UOmRzvFWKW2Uv35YZNFfH22jihWz9TWFqia4Jq3Y0NbiK2Plvw1RgbpnFgsG_CvTsicWCwrAXqO19WzdfCopRe0hZFeGzOfGD8Xae4vtx9MQbnLY0E8Y7UcG2710WLW9zz-5QBbaBZpVZHoulCqSAwbjgkh1GbyyQ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/U2AuC5GOC3tQaqc7FZNsp00B0we2cbam174Vo5liZ_LOTXFoS8n4kCeiXm4N-pO3f_O1HGCn2oAS_07LWtRk9FFKdT91Ih39DxNyhcBmc82TCPDenbLlx2CxP1V2G9wmmZUgpxUDBEYcrl8Y8bGF9nCi0cp9U5BhxCJizxjP9_MJfm76DMUWa9Bm_58UfHFV?purpose=fullsize)

## Một số thuộc tính

- __Space (Không gian):__ Hệ tọa độ, vector, frame, phép biển đổi cứng trong 3D.

- __Transform (biến đổi):__ Quay, tịnh tiến, ghép biến đổi đồng nhất.
    - Ví dụ: $T = \begin{bmatrix} R & t\\  0& 1 \end{bmatrix}$

- __Metric (đo lường):__ khoảng cách, góc, độ dài, tích vô hướng bảo toàn qua quay.
    - Ví dụ: $||R\bar p|| = ||\bar p ||$

- __Projection (Chiếu):__ Chiếu điểm 3D lên ảnh 2D bằng mô hình camera.
    - Ví dụ: $x'=PX$

- __Curvature (Độ cong):__ Mật cong, địa hình, quỹ đạo có độ cong và hướng pháp tuyến.
    - Ví dụ: $K = \frac {1} {R_c}$

- __Caution (Lưu ý):__ Gimbal lock khi $\theta = \pm 90^\circ$ cần lọc cảm biến (Kalman) để ước lượng ổn định.

---

### Không gian và hệ tọa độ

#### World Frame

Hệ tọa độ cố định dùng để mô tả thế giới bên ngoài.

$$
\mathcal{F}_W = \{x_W,y_W,z_W\}
$$

Một điểm trong không gian:

$$
p_W =
\begin{bmatrix}
x\\y\\z
\end{bmatrix}
$$

---

#### Body Frame

Hệ tọa độ gắn với chính drone.

$$
\mathcal{F}_B = \{x_B,y_B,z_B\}
$$

Khi drone quay, Body Frame quay theo drone.

Đây là điểm rất quan trọng:

> **World Frame mô tả thế giới; Body Frame mô tả trạng thái của drone trong thế giới đó.**

---

#### Coordinate Transformation

Một vector có thể được biểu diễn trong hai hệ tọa độ:

$$
p_W = R_{WB}p_B
$$

Trong đó:

* $p_B$: vector trong Body Frame.
* $p_W$: vector trong World Frame.
* $R_{WB}$: rotation matrix từ Body → World.

---

## Rotation trong không gian 3D

![Image](https://images.openai.com/static-rsc-4/H_kN7u1qShLVvdhTcjD-UKJOu_iUYDQKqYhwMu3LjPQF012eu2_wyygYZsL94_g47MzP5E93Jc5MoRnKbVasNXtGuhdJw8Jy8rULjY2MgsmjZz_MQ4sGREzYKxj0k-xKEjGigINUmB4SHJHzhnXKZHyqdxzxEsvVMClVyyxYuI4WuOMyNbXUiGhTmHAh6Of9?purpose=fullsize)

### Rotation Matrix

Định hướng của drone có thể được biểu diễn bằng ma trận: $R \in SO(3)$ với: $R^TR=I$ và $\det(R)=1$ Tập:

$$
SO(3)
=
\{R\in\mathbb{R}^{3\times3}
\mid R^TR=I,\det(R)=1\}
$$

là **Special Orthogonal Group**, biểu diễn toàn bộ phép quay hợp lệ trong 3D.

---

## Bài toán thực tế

![Image](https://images.openai.com/static-rsc-4/Y3RKFJT8nQRjbzCXFLJbLV3k7knlbUVm647VVzEQ8DdmoIqtV17tR2u-2D6_2PSPDatK6XWfOrpMqpzrTPbRyX2W5KaaENL7sZj3-DfeRdf00O615YliGBlmeKwNu4n3FEHZesaP60SL1pzzQbBc1TE2jN4IiphlYwyNnyo9l5S2dvuh_iYDMGQscjAeAo8R?purpose=fullsize)

Drone chuyển động trong không gian 3D nên không chỉ cần biết đang ở đâu, mà còn phải biết __đang quay như thế nào.__

Trạng thái hình học cơ bản của drone gồm:

- __Position__ - vị trí.
- __Orientation__ - định hướng.
- __Linear velocity__ - vận tốc tịnh tiến.
- __Angular velocity__ - vận tốc quay.

Ba chuyển động quay cơ bản:

- __Roll ($\phi$)__ - nghiêng quanh trục $x$ ($R_x​(\phi)$). 
- __Pitch ($\theta$)__ - nghiêng quanh trục $y$ ($R_y(\theta)$).
- __Yaw ($\psi$)__ - đổi hướng quanh trục $z$ ($R_z(\psi)$).

Core idea:

> Drone giữ thăng bằng thực chất là bài toán ước lượng và điều khiển orientation trong không gian 3D.
>
> Roll, Pitch, Yaw không phải ba chuyển động độc lập hoàn toàn; thứ tự phép quay ảnh hưởng đến orientation cuối cùng.

Dưới đây là hệ thống các chương được tái cấu trúc hoàn chỉnh, nối tiếp chính xác với phần mở đầu của bạn. Nội dung tập trung hoàn toàn vào trọng tâm toán học - hình học - điều khiển, cô đọng và không lan man.

---

## Chương 1: Hệ tọa độ & Phép biến đổi đồng nhất

### 1. Phép biểu diễn không gian & Khái niệm Frame

> "Một vector/điểm đang được biểu diễn trong hệ tọa độ nào, và làm sao chuyển nó sang hệ tọa độ khác?"

Một điểm $p$ trong không gian 3D được biểu diễn qua hai hệ tọa độ chính:

* **World Frame ($\mathcal{F}_W$):** Cố định (Inertial frame).

$$ \mathcal F_W=\{x_W,y_W,z_W\} $$

* **Body Frame ($\mathcal{F}_B$):** Gắn liền với tâm khối lượng của drone.

$$ \mathcal F_B=\{x_B,y_B,z_B\} $$

Quan hệ chuyển đổi vị trí giữa hai hệ tọa độ (Rigid Transformation):

$$p_W = R_{WB} p_B + t_{WB}$$

### 2. Ma trận biến đổi đồng nhất (Rigid Body Transformation)

Biểu diễn gộp cả phép quay $R \in SO(3)$ và phép tịnh tiến $t \in \mathbb{R}^3$ dưới dạng ma trận $4 \times 4$ trong nhóm $SE(3)$ (Homogeneous Transformation): 

$$T_{WB} = \begin{bmatrix} R_{WB} & t_{WB} \\ 0_{1\times3} & 1 \end{bmatrix} \in SE(3)$$

Phép biến đổi nghịch đảo (từ World về Body) (Transformation inverse):

$$T_{WB}^{-1} = \begin{bmatrix} R_{WB}^T & -R_{WB}^T t_{WB} \\ 0_{1\times3} & 1 \end{bmatrix}$$

---

## Chương 2: SO(3) & Biểu diễn Phép quay trong Không gian 3D

> Orientation của drone là một phép quay trong không gian 3D, không đơn giản chỉ là ba góc Roll/Pitch/Yaw.


![Image](https://images.openai.com/static-rsc-4/RUsxS0rKsq7tR1FoS9csDiy4g6aOwMrHVGwgTaCSfvULVMniDIBxYoE7ZATT6V5Axwk7XSkrROBOyQfyCnVqPmB4hkg4GDj_8Msp1oNzQw6pq66ipvr2ECWrIn5TQ5rSrGp2llQ7cnncrHgV7PVckvcxvn0BRLyxIXMWTZN7NYjVUF-6xNBMh6bnSsl6zT2k?purpose=fullsize)

### 1. Ma trận quay & Các tính chất đại số

Tập hợp các ma trận quay $SO(3)$ tuân theo:

$$SO(3) = \{ R \in \mathbb{R}^{3 \times 3} \mid R^T R = I, \det(R) = 1 \}$$

*  **Rotation Matrix:** $ R^TR=I $, $\det(R)=1$
* **Bảo toàn khoảng cách:** $\Vert{}R p\Vert{} = \Vert{}p\Vert{}$
* **Bảo toàn tích vô hướng:** $(R u)^T \cdot (R v) = u^T \cdot v$

#### Euler Angles

$$ R=R_z(\psi)R_y(\theta)R_x(\phi) $$

với:

$$ \phi=\text{Roll} $$ $$ \theta=\text{Pitch} $$ $$ \psi=\text{Yaw} $$

Nhưng không cần khai triển ma trận $3\times3$ dài nếu mục tiêu là hiểu core idea.

Chỉ cần cho các ma trận cơ bản: $ R_x(\phi),\quad R_y(\theta),\quad R_z(\psi) $ và công thức composition.

### 2. Biểu diễn Euler & Hiện tượng Gimbal Lock

> Gimbal Lock là singularity của representation bằng Euler angles, không phải lỗi vật lý của drone.

Chuỗi phép quay theo thứ tự $Z-Y-X$ (Yaw-Pitch-Roll):

$$R_{WB} = R_z(\psi) R_y(\theta) R_x(\phi)$$

Ma trận quay tổng hợp:

$$R_{WB} = \begin{bmatrix}  c\psi c\theta & c\psi s\theta s\phi - s\psi c\phi & c\psi s\theta c\phi + s\psi s\phi \\ s\psi c\theta & s\psi s\theta s\phi + c\psi c\phi & s\psi s\theta c\phi - c\psi s\phi \\ -s\theta & c\theta s\phi & c\theta c\phi  \end{bmatrix}$$

*(với $c \cdot = \cos(\cdot), s \cdot = \sin(\cdot)$)*

> **Điểm kỳ dị (Gimbal Lock):** Khi $\theta = \pm 90^\circ$ (Pitch đứng đứng), trục Roll ($x$) và Yaw ($z$) bị trùng nhau, làm mất $1$ độ tự do quay.

---

## Chương 3: Quaternion & Tối ưu hóa Tính toán Phép quay

> Quaternion là một cách biểu diễn orientation ổn định hơn Euler angles, đặc biệt tránh singularity của Euler representation.

### 1. Định nghĩa Unit Quaternion

Để tránh Gimbal Lock và tối ưu năng lượng tính toán, phép quay được biểu diễn bằng Unit Quaternion $q \in \mathbb{S}^3$:

$$q = \begin{bmatrix} q_0 \\ \mathbf{q}_v \end{bmatrix} = \begin{bmatrix} \cos(\frac{\theta}{2}) \\ \mathbf{u} \sin(\frac{\theta}{2}) \end{bmatrix}, \quad \Vert{}q\Vert{} = 1$$

Với $\mathbf{u} = [u_x, u_y, u_z]^T$ là trục quay đơn vị và $\theta$ là góc quay.

#### Axis-Angle → Quaternion

$$ q= \begin{bmatrix} \cos(\theta/2)\\ u_x\sin(\theta/2)\\ u_y\sin(\theta/2)\\ u_z\sin(\theta/2) \end{bmatrix} $$

### 2. Phép xoay Vector bằng Quaternion

Chuyển đổi điểm $p_B$ từ Body Frame sang World Frame bằng phép nhân Quaternion:

$$p_W = q \otimes p_B \otimes q^*$$

Trong đó $q^* = [q_0, -\mathbf{q}_v]^T$ là Quaternion liên hợp.

---

## Chương 4: Động lực học Drone & Phương trình Chuyển động

> Motor → Thrust → Force/Torque → Angular Motion → Orientation

### 1. Mối liên hệ Lực đẩy & Tốc độ Động cơ

Động cơ thứ $i$ tạo ra lực đẩy $F_i = k_f \Omega_i^2$ và momen xoắn $M_i = k_m \Omega_i^2$.

Hệ phương trình phân phối lực/momen (Motor Mixing Matrix):

$$\begin{bmatrix} T \\ \tau_x \\ \tau_y \\ \tau_z \end{bmatrix} = \begin{bmatrix} k_f & k_f & k_f & k_f \\ 0 & -L k_f & 0 & L k_f \\ -L k_f & 0 & L k_f & 0 \\ k_m & -k_m & k_m & -k_m \end{bmatrix} \begin{bmatrix} \Omega_1^2 \\ \Omega_2^2 \\ \Omega_3^2 \\ \Omega_4^2 \end{bmatrix}$$

#### Force và Torque

Đây mới là trọng tâm:

$$ F=\sum_iF_i $$ $$ \tau=\sum_i r_i\times F_i+\tau_i $$

Từ đó:

$$ F,\tau \rightarrow \text{motion} $$

### 2. Phương trình Newton-Euler 3D

Hệ phương trình vi phân chuyển động toàn phần của Drone trong World Frame:

$$\begin{cases} m \ddot{p}_W = R_{WB} \begin{bmatrix} 0 \\ 0 \\ T \end{bmatrix} - \begin{bmatrix} 0 \\ 0 \\ mg \end{bmatrix} & \text{(Chuyển động tịnh tiến)} \\ I \dot{\omega}_B + \omega_B \times (I \omega_B) = \tau_B & \text{(Chuyển động quay)} \end{cases}$$

Trong đó $I \in \mathbb{R}^{3 \times 3}$ là ma trận momen quán tính của drone, $\omega_B$ là vận tốc góc.

#### Moment of Inertia
$$ I= \begin{bmatrix} I_x&0&0\\ 0&I_y&0\\ 0&0&I_z \end{bmatrix} $$

> $I$ đối với chuyển động quay tương tự vai trò của $m$ đối với chuyển động tịnh tiến.

---

## Chương 5: Ước lượng Trạng thái (IMU Fusion & State Estimation)

### 1. State
Trong hệ thống bay tự động, trạng thái của drone không được quan sát trực tiếp một cách đầy đủ. Một trạng thái $x$ là tập hợp các biến cần thiết để mô tả cấu hình động lực học của hệ thống tại một thời điểm.

Một mô hình trạng thái tổng quát có thể viết:

$$ x= \begin{bmatrix} p_W\\ v_W\\ q_{WB}\\ \omega_B\\ b_a\\ b_g \end{bmatrix} $$

Trong đó:

- $p_W\in\mathbb R^3$: vị trí trong World Frame.
- $v_W\in\mathbb R^3$: vận tốc tuyến tính.
- $q_{WB}$: orientation của Body Frame đối với World Frame.
- $\omega_B\in\mathbb R^3$: vận tốc góc trong Body Frame.
- $b_a$: bias của accelerometer.
- $b_g$: bias của gyroscope.

Do orientation thuộc không gian quay $SO(3)$ nên không thể xem nó đơn giản như một vector Euclidean thông thường. Trong triển khai, orientation thường được biểu diễn bằng rotation matrix hoặc unit quaternion.

Mục tiêu của state estimation là tìm ra: $ \hat{x}_k $ là ước lượng tốt nhất của trạng thái thực: $ x_k $ từ các phép đo cảm biến và trạng thái trước đó.

### 2. Measurement

Cảm biến không quan sát trực tiếp toàn bộ state. Mỗi cảm biến chỉ cung cấp một phép đo liên quan đến một phần của trạng thái.

Mô hình đo tổng quát:

$$ z_k=h(x_k)+v_k $$

Trong đó:

- $z_k$: measurement tại thời điểm $k$.
- $h(\cdot)$: measurement model.
- $x_k$: trạng thái thực.
- $v_k$: measurement noise.

Thông thường giả sử:

$$ v_k\sim\mathcal N(0,R) $$

với $R$ là covariance của measurement noise.

Do đó:

$$ \boxed{ \text{Measurement} = \text{True State} + \text{Noise} } $$

Trong trường hợp phi tuyến:

$$ z_k=h(x_k)+v_k $$

thay vì quan hệ tuyến tính:

$$ z_k=Hx_k+v_k $$

Đây là lý do các bộ lọc như EKF cần xây dựng cả state transition model và measurement model.

### 3. Sensor Noise và Bias

Measurement của IMU không bằng chính xác đại lượng vật lý cần đo.

Một mô hình đơn giản:

$$ z=s+b+n $$

Trong đó:

- $s$: giá trị vật lý thực.
- $b$: sensor bias.
- $n$: random noise.

Hai loại sai số cần phân biệt:

#### Random Noise

Nhiễu biến đổi theo thời gian:

$$ n\sim\mathcal N(0,\Sigma) $$

Nó làm measurement dao động xung quanh giá trị thực.

#### Bias

Sai lệch có xu hướng tồn tại trong một khoảng thời gian:

$$ b\neq0 $$

Bias đặc biệt quan trọng với IMU vì khi vận tốc góc được tích phân để suy ra orientation:

$$ \theta(t) = \theta(0)+ \int_0^t\omega(\tau)d\tau $$

một bias nhỏ trong $\omega$ có thể tạo ra sai số orientation tăng theo thời gian.

Do đó mô hình gyroscope thường được viết:

$$ \omega_m = \omega+b_g+n_g $$

và accelerometer:

$$ a_m = a_{\text{specific}}+b_a+n_a $$

Bias cũng có thể được đưa trực tiếp vào state:

$$ x= [\cdots,b_a,b_g]^T $$

để bộ lọc đồng thời ước lượng cả trạng thái chuyển động và sai số cảm biến.

### 4. Cảm biến IMU & Mô hình Sai số

* **Gyroscope:** Đo vận tốc góc $\omega_B$, tốc độ cập nhật nhanh nhưng bị trôi dài hạn (drift): $\omega_{meas} = \omega + b_g + n_g$.

> Gyro tốt cho chuyển động nhanh nhưng tích phân sai số dẫn đến drift.

* **Accelerometer:** Đo gia tốc $a_B$, chứa trọng lực $g$ giúp xác định mặt phẳng ngang nhưng bị nhiễu do rung động động cơ: $a_{meas} = R_{WB}^T (a_W - g) + b_a + n_a$.

> Accelerometer không đơn giản là "đo gravity"; nó đo specific force, nên khi drone đang tăng tốc, tín hiệu không còn phản ánh riêng gravity.

### 5. Thuật toán Lọc kết hợp (Complementary Filter)

Kết hợp đáp ứng tần số cao của Gyroscope và đáp ứng tần số thấp của Accelerometer:

$$\hat{q}_{k} = \alpha \cdot (q_{k-1} \otimes \Delta q_{gyro}) + (1 - \alpha) \cdot q_{accel}$$

Với $\alpha \approx 0.95 - 0.98$ quyết định độ tin tưởng vào Gyro.

---

## Chương 6: Cấu trúc Vòng điều khiển Thăng bằng (Cascaded Control)

> Drone biết mình đang nghiêng → vậy làm sao nó tự sửa để đứng thẳng?

### Kiến trúc phân cấp (Cascaded Controller)

```
[Vị trí mong muốn p_d] ---> (Position Controller) ---> [Định hướng mong muốn R_d / q_d]
                                                                  |
[Định hướng thực tế q] ----> (Attitude Controller) <---------------
                                      |
                              [Momen quay \tau_B]
                                      |
                           (Motor Mixing Matrix) ---> [Tốc độ góc động cơ \Omega_i]

```

1. **Outer Loop (Vòng Vị trí):** Tần số thấp (~50 Hz), tính toán góc nghiêng (Roll/Pitch) và tổng lực đẩy $T$ dựa trên sai lệch vị trí $\Delta p$.
2. **Inner Loop (Vòng Định hướng):** Tần số cao (400 Hz - 1 kHz), tính toán Momen $\tau_B = [\tau_x, \tau_y, \tau_z]^T$ để triệt tiêu sai lệch định hướng $\Delta q = q^{-1} \otimes q_d$.

#### Open-Loop vs Closed-Loop
Open loop:

$$ u\rightarrow system $$

Closed loop:

$$ u=f(x_d-\hat{x}) $$

Drone giữ thăng bằng là closed-loop control.