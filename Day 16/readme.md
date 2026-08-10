# Positional Encoding - Sinusoidal, RoPE, ALiBi

## The Problem 

Scaled dot-product attention **không nhận biết thứ tự**. Ma trận attention:

$$\operatorname{softmax}\left(\frac{QK^T}{\sqrt d}\right)V$$

được tính từ **độ tương đồng giữa từng cặp token**. Khi xáo trộn các hàng của $X$, các hàng đầu ra cũng chỉ bị xáo trộn tương ứng. Bản thân attention **không chứa thông tin về vị trí**.

Vì vậy:

> `"The cat sat on the mat"` và `"mat the on sat cat the"` có thể tạo ra cùng các biểu diễn tương ứng nếu không có positional signal.

Điều này nghiêm trọng với ngôn ngữ, code, audio, video — nơi **thứ tự mang ý nghĩa**.

### Cách giải quyết

Cần **đưa thông tin vị trí vào embedding hoặc attention**. Có ba hướng chính:

1. **Absolute Sinusoidal — Vaswani (2017)**
   Cộng $sin/\cos$ theo vị trí vào embedding. Không cần học tham số vị trí nhưng extrapolation kém khi vượt độ dài đã huấn luyện.

2. **RoPE — Rotary Position Embeddings (Su, 2021)**
   Xoay vector (Q,K) theo góc phụ thuộc vào vị trí. Thông tin **vị trí tương đối** được mã hóa trực tiếp trong dot product.

3. **ALiBi — Attention with Linear Biases (Press, 2022)**
   Không thêm positional embedding. Thay vào đó, cộng **linear bias theo khoảng cách vị trí** trực tiếp vào attention score. Có khả năng extrapolate độ dài tốt.

**Tóm lại:** Attention tự thân là **permutation-invariant**, nên cần positional information để mô hình phân biệt thứ tự. Ba cách trên khác nhau ở **cách chúng định nghĩa và đưa thông tin vị trí vào attention**.

## Concept — Khái niệm

### 1. Absolute Sinusoidal

Tạo trước ma trận vị trí cố định:

$$PE \in \mathbb{R}^{\text{max len} \times d_{model}}$$

$$PE[pos,2i]=\sin\left(\frac{pos}{10000^{2i/d_{model}}}\right)$$

$$PE[pos,2i+1]=\cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)$$

Sau đó:

$$X'=X+PE[:N]$$

Mỗi dimension sử dụng một **tần số sinusoid khác nhau**. Mô hình đọc vị trí thông qua **pattern pha (phase pattern)**.

**Hạn chế:** nếu chỉ xây dựng `max_len`, mô hình không được cung cấp thông tin về các vị trí vượt quá độ dài đó.

---

### 2. RoPE — Rotary Position Embeddings

RoPE **không xoay embedding (X)** mà xoay trực tiếp **(Q) và (K)**.

Với mỗi cặp dimension ((2i,2i+1)):

$$
\begin{bmatrix} 
q'_{2i} \\
q'_{2i+1}
\end{bmatrix}
=
\begin{bmatrix}
\cos(\text{pos}\cdot\theta_i) & -\sin(\text{pos}\cdot\theta_i) \\
\sin(\text{pos}\cdot\theta_i) & \cos(\text{pos}\cdot\theta_i)
\end{bmatrix}
\begin{bmatrix}
q_{2i} \\ 
q_{2i+1}
\end{bmatrix}
$$

trong đó:

$$\theta_i=base^{-2i/d_{head}}$$

với `base = 10000` mặc định.

Áp dụng phép xoay tương tự cho (K). Khi đó:

$$q'_m\cdot k'_n$$

trở thành hàm của **(m-n)**.

**Ý nghĩa cốt lõi:** attention score phụ thuộc vào **khoảng cách tương đối** giữa hai token, dù phép xoay ban đầu sử dụng vị trí tuyệt đối.

---

### 3. ALiBi — Attention with Linear Biases

Không thêm positional embedding. Thay vào đó, thêm bias trực tiếp vào attention score:

$$score_{i,j}= \frac{q_i\cdot k_j}{\sqrt d} m_h|i-j|$$

Trong đó (m_h) là **slope riêng của từng attention head**.

* Token càng gần → penalty càng nhỏ.
* Token càng xa → penalty càng lớn.

Vì vậy ALiBi đưa thông tin vị trí **trực tiếp vào attention score** thay vì embedding.

**Điểm chính:** ALiBi không tạo positional embedding và không có chi phí huấn luyện thêm đáng kể theo mô tả trong tài liệu.

## What to pick in 2026 — Nên chọn gì?

| Variant                 | Extrapolation     | Training cost   | Used by                                           |
| ----------------------- | ----------------- | --------------- | ------------------------------------------------- |
| **Absolute sinusoidal** | Poor              | Free            | Original Transformer, early BERT                  |
| **Learned absolute**    | Poor              | Tiny            | GPT-2, GPT-3                                      |
| **RoPE**                | Good with scaling | Free            | Llama 2/3/4, Qwen 2/3, Mistral, DeepSeek-V3, Kimi |
| **RoPE + YaRN**         | Excellent         | Fine-tune stage | Qwen2-1M, Llama 3.1 128K                          |
| **ALiBi**               | Excellent         | Free            | BLOOM, MPT, Baichuan                              |

### Vì sao RoPE thắng?

RoPE được ưu tiên vì:

* **Không thay đổi kiến trúc attention**.
* Mã hóa **relative position** trực tiếp trong $Q,K$.
* `base` là một hyperparameter cho phép điều chỉnh khả năng **long-context**.

Với long-context, các biến thể như **NTK-aware, YaRN, LongRoPE** mở rộng khả năng của RoPE mà không cần huấn luyện lại từ đầu.

> **2026: RoPE là lựa chọn mặc định cho Transformer hiện đại; RoPE + scaling như YaRN được dùng khi cần context dài.**

## Build It

Đây là bản `.md` gọn, giữ nguyên code và phần phân tích ngay bên dưới:

### Step 1: Sinusoidal Encoding

```python
def sinusoidal(N, d):
    pe = [[0.0] * d for _ in range(N)]
    for pos in range(N):
        for i in range(d // 2):
            theta = pos / (10000 ** (2 * i / d))
            pe[pos][2 * i] = math.sin(theta)
            pe[pos][2 * i + 1] = math.cos(theta)
    return pe
```

Thêm positional encoding vào embedding matrix trước attention layer đầu tiên:

```python
X_prime = X + PE[:N]
```

#### Phân tích

* `N`: số lượng vị trí/token.
* `d`: kích thước embedding.
* Mỗi cặp dimension `(2i, 2i+1)` sử dụng `sin` và `cos` với tần số khác nhau.
* `PE[pos]` biểu diễn thông tin vị trí của token tại `pos`.
* `X + PE` đưa thông tin vị trí vào embedding trước khi tính attention.

### Step 2: RoPE Applied to Q, K

RoPE operates directly on **Q and K**:

```python
def apply_rope(x, pos, base=10000):
    d = len(x)
    out = list(x)
    for i in range(d // 2):
        theta = pos / (base ** (2 * i / d))
        c, s = math.cos(theta), math.sin(theta)
        a, b = x[2 * i], x[2 * i + 1]
        out[2 * i] = a * c - b * s
        out[2 * i + 1] = a * s + b * c
    return out
```

Áp dụng cùng hàm cho:

```python
Q_m = apply_rope(Q_m, m)
K_n = apply_rope(K_n, n)
```

#### Phân tích

* RoPE **không thay đổi embedding (X)**; nó xoay trực tiếp $Q$ và $K$.
* Mỗi cặp dimension được xoay một góc phụ thuộc vào vị trí `pos`.
* Khi tính:

$$Q'_m \cdot K'_n$$

dot product xuất hiện thành phần phụ thuộc vào:

$$(m-n)\theta_i$$

* Vì vậy attention score có thể biểu diễn **relative position** giữa token ở vị trí $m$ và $n$.
* Điểm cốt lõi: **cùng một phép xoay cho Q và K biến thông tin vị trí tuyệt đối thành quan hệ vị trí tương đối trong attention.**

### Step 3: ALiBi Slopes and Bias

```python
def alibi_bias(n_heads, seq_len):
    # slope_h = 2 ** (-8 * h / n_heads) for h = 1..n_heads
    slopes = [2 ** (-8 * (h + 1) / n_heads) for h in range(n_heads)]
    bias = []
    for m in slopes:
        row = [[-m * abs(i - j) for j in range(seq_len)] for i in range(seq_len)]
        bias.append(row)
    return bias
```

Thêm `bias[h]` vào ma trận attention score `(seq_len, seq_len)` của head `h`, sau đó thực hiện `softmax`.

#### Phân tích

* `slopes`: mỗi attention head có một slope riêng.
* `-m * abs(i - j)`: token càng xa nhau → bias càng âm.
* Bias được thêm **trực tiếp vào attention scores**, trước `softmax`.
* ALiBi không thêm positional embedding; nó đưa thông tin khoảng cách trực tiếp vào attention.

---

### Step 4: Verify Relative-Distance Property of RoPE

Chọn hai vector ngẫu nhiên `a`, `b`.

* Xoay chúng tại `(pos_a, pos_b)`.
* Sau đó xoay lại tại `(pos_a + k, pos_b + k)`.
* Hai dot product phải bằng nhau trong sai số floating-point.

#### Phân tích

Điều này kiểm chứng tính chất cốt lõi của RoPE:

$$(pos_a+k)-(pos_b+k)=pos_a-pos_b$$

Do đó attention chỉ phụ thuộc vào **khoảng cách tương đối**, không phụ thuộc vào **absolute offset**.

## Key Terms

| Term                    | What people say               | What it actually means                                                                       |
| ----------------------- | ----------------------------- | -------------------------------------------------------------------------------------------- |
| **Positional encoding** | “Tells attention about order” | Any signal added to embeddings or attention that encodes position.                           |
| **Sinusoidal**          | “The original one”            | sin/cos at geometric frequencies added to embeddings; doesn’t extrapolate.                   |
| **RoPE**                | “Rotary embeddings”           | Rotate $Q,K$ by position-dependent angle; dot product encodes relative distance.             |
| **ALiBi**               | “Linear bias trick”           | Add $-m\cdot\lvert i-j\rvert$ to attention scores; no embedding needed, great extrapolation. |
| **base**                | “RoPE’s knob”                 | The frequency scaler in RoPE; increase to extend context at inference.                       |
| **NTK-aware**           | “A RoPE scaling trick”        | Rescale `base` so high-frequency dimensions aren’t squeezed when context expands.            |
| **YaRN**                | “The fancy one”               | Per-dimension interpolation + extrapolation that preserves attention entropy.                |
| **Extrapolation**       | “Works beyond trained length” | Khả năng positional scheme hoạt động ở độ dài vượt quá context length đã được huấn luyện.    |

