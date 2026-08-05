# Self-Attention from Scratch

## Learning Objectives

> Mục tiêu của bài học không phải là __sử dụng API Attention của PyTorch__, mà là __tự xây dựng (from scratch)__ toàn bộ cơ chế Self-Attention để hiểu bản chất toán học và cách Transformer hoạt động.

1. __Implement Scaled Dot-Product Self-Attention from Scratch__
    - Mục tiêu: Xây dựng hoàn chỉnh thuật toán __Scaled Dot-Product Self-Attention__ chỉ bằng NumPy. Cần cài đặt các thành phần:
        - __Query Projection__
        - __Key Projection__
        - __Value Projection__
        - __Dot Product__
        - __Scaling__
        - __Softmax__
        - __Weighted Sum__

2. __Build a Multi-Head Attention Layer__
    - Sau khi hoàn thành Self-Attention cơ bản, bài học mở rộng sang __Multi-Head Attention__. Mỗi head học một loại quan hệ khác nhau giữa các token, thay vì chỉ có một cách nhìn duy nhất. Mục tiêu xây dựng:
        - Chia embedding thành nhiều head
        - Tính attention cho từng head
        - Ghép (Concatenate)
        - Chiếu qua một Linear cuối cùng

3. __Trace the Attention Matrix__
    - Một mục tiêu quan trọng của bài học là hiểu được __Attention Matrix__ biểu diễn điều gì. Thông qua ma trận này có thể quan sát:
        - token nào liên quan với nhau,
        - mô hình học được mối quan hệ nào trong câu,
        - vì sao Attention có khả năng học phụ thuộc xa (long-range dependency).

4. __Hiểu vì sao phải chia cho__ $\sqrt{dk}$
    - Mục tiêu không chỉ biết công thức mà còn hiểu nguyên nhân. Scaling giúp giữ các logits ở phạm vi ổn định trước khi đưa vào Softmax. Nếu không chia:
        - Dot Product sẽ tăng theo số chiều.
        - Giá trị đưa vào Softmax rất lớn.
        - Softmax gần như trở thành One-Hot.
        - Gradient rất nhỏ.
        - Quá trình học trở nên khó khăn.

5. __Apply Causal Mask__
    - Cuối cùng, bài học yêu cầu chuyển Self-Attention thông thường thành Decoder Attention.
    - Đây là cơ chế giúp Agent sinh từng token mà không "nhìn trước đáp án".

---

## The Problem

Các mô hình __RNN/LSTM__ xử lý chuỗi theo từng token một, nên thông tin phải truyền qua nhiều bước trước khi đến các token ở xa.

```
Token1 → Token2 → Token3 → ... → TokenN
```

Điều này dẫn đến hai hạn chế chính:

- __Long-range dependency__: Thông tin từ các token đầu chuỗi dần bị suy giảm khi truyền qua nhiều bước, khiến mô hình khó học mối quan hệ giữa các từ ở xa nhau.
- __Hidden state bottleneck__: Toàn bộ ngữ cảnh của câu phải được nén vào một hidden state có kích thước cố định, làm mất thông tin khi chuỗi dài.

Năm 2014, __Bahdanau Attention__ cho phép decoder nhìn lại toàn bộ encoder thay vì chỉ dựa vào hidden state cuối, nhưng Attention vẫn chỉ là một thành phần bổ sung cho RNN.

Đến năm 2017, bài báo "__Attention Is All You Need__" đưa ra một ý tưởng mới:

> Loại bỏ hoàn toàn RNN và CNN, chỉ sử dụng Attention.

Kết quả là __Self-Attention__ cho phép mỗi token __trực tiếp tương tác với mọi token khác trong cùng một bước tính toán song song__, giúp học tốt các phụ thuộc xa (long-range dependencies) và tăng tốc quá trình huấn luyện trên GPU.

---

## The Concept

### Database Lookup Analogy

Bản chất của __Self-Attention__ có thể được hiểu như một __cơ chế tra cứu (lookup) mềm - soft database lookup__.

Trong cơ sở dữ liệu truyền thống, truy vấn chỉ trả về __một kết quả khớp chính xác__.

```
Query: "capital of France"
        │
 Exact Match
        │
        ▼
      "Paris"
```

Trong Self-Attention, truy vấn không tìm một kết quả duy nhất mà __so sánh với tất cả các Key__, sau đó kết hợp thông tin từ tất cả các Value theo mức độ liên quan.

```
Query
   │
Compare với tất cả Keys
   │
Similarity Scores
   │
Softmax
   │
Weighted Sum của Values
   │
Output
```

Do đó, Attention không thực hiện __hard lookup__ như cơ sở dữ liệu, mà thực hiện __soft lookup__, trong đó mọi token đều có cơ hội đóng góp vào kết quả với trọng số khác nhau.

---

#### Ba thành phần của Self-Attention

Đối với mỗi token, Self-Attention sinh ra ba vector học được:

1. Query (Q)

> Đại diện cho: `"Tôi đang tìm kiếm thông tin gì?"`. Query được dùng để tìm những token phù hợp trong câu.

2. Key (K)

> Đại diện cho: `"Tôi chứa thông tin gì?"`. Key đóng vai trò như "nhãn" để Query so sánh mức độ liên quan.

3. Value (V)

> Đại diện cho: `"Nếu được chọn, tôi sẽ cung cấp thông tin gì?"`. Value là nội dung thực sự được tổng hợp để tạo ra biểu diễn mới của token.

---

#### Cơ chế hoạt động

Giả sử token hiện tại Query là $q_i$. Quá trình Attention diễn ra như sau:

1. So sánh $q_i$ với tất cả Key trong chuỗi.
2. Tính __Attention Score__ bằng Dot Product.
3. Điểm càng lớn → mức độ liên quan càng cao.
4. Softmax chuyển các điểm thành trọng số.
5. Dùng các trọng số này để tính __Weighted Sum__ của tất cả Value.

Có thể biểu diễn đơn giản:

```
Query
   │
Dot Product với tất cả Keys
   │
Attention Scores
   │
Softmax
   │
Attention Weights
   │
Weighted Sum của Values
   │
Output
```

> High score means "this key matches my query." Those scores weight the values. The output is a weighted sum of values.

---

### Q, K, V Computation

Giả sử đầu vào là ma trận embedding

$$X = [x_1, x_2, ..., x_n], \text{ shape: } (n, d)$$

với:
- $n$: số lượng token.
- $d$: kích thước embedding.

Self-Attention học ba ma trận trọng số:

$$W_q \in \mathbb R^{d \times d_k}$$
$$W_k \in \mathbb R^{d \times d_k}$$
$$W_v \in \mathbb R^{d \times d_k}$$

Sau đó chiếu embedding thành ba không gian khác nhau:

$$Q = X @ W_q, \text{ shape: } (n, dk) \text{ each token's query}$$
$$K = X @ W_k, \text{ shape: } (n, dk) \text{ each token's key}$$
$$V = X @ W_v, \text{ shape: } (n, dv) \text{ each token's value}$$

Minh họa cho một token:

```
        Wq
x_i ────[*]─────────► q_i   "What am I looking for?"
 |
        Wk
 └──────[*]───────► k_i     "What do I contain?"
 |
        Wv
 └──────[*]────────► v_i    "What do I offer?"
```

---

### Attention Matrix

Sau khi có toàn bộ Q, K và V cho toàn bộ Tokens, Attention tính ma trận điểm số:

$$Scores = QK^T, \text{ shape: } (n, n)$$

Trong đó:
- Mỗi __hàng__ tương ứng với một __Query__.
- Mỗi __cột__ tương ứng với một __Key__.

```
         k1    k2    k3    k4    k5
   +-----+-----+-----+-----+-----+
q1 | 2.1 | 0.3 | 0.1 | 0.8 | 0.2 | <- how much q1 attends to each key
   +-----+-----+-----+-----+-----+
q2 | 0.4 | 1.9 | 0.7 | 0.1 | 0.3 |
   +-----+-----+-----+-----+-----+
q3 | 0.2 | 0.6 | 2.3 | 0.5 | 0.1 |
   +-----+-----+-----+-----+-----+
q4 | 0.9 | 0.1 | 0.4 | 1.7 | 0.6 |
   +-----+-----+-----+-----+-----+
q5 | 0.1 | 0.3 | 0.2 | 0.5 | 2.0 |
   +-----+-----+-----+-----+-----+
```

Ý nghĩa của một phần tử: $Score(i, j)$ là mức độ token $i$ chú ý đến token $j$

> Each row: one token's attention over the entire sequence.

---

#### Ý nghĩa của Attention Matrix

Đối với từng hàng của ma trận:

1. Một Query so sánh với tất cả Key.
2. Softmax biến các Score thành Attention Weights.
3. Các trọng số này được dùng để tính Weighted Sum của tất cả Value.
4. Kết quả là Context Vector của token đó.

> Mỗi hàng của Attention Matrix mô tả toàn bộ mức độ chú ý của một token đối với tất cả các token còn lại trong chuỗi, từ đó tạo ra biểu diễn ngữ cảnh (context representation) mới cho token đó.

---

### Why Scale?

Sau khi tính Dot Product giữa __Query và Key__, ta thu được ma trận điểm số:

$$Score = QK^T$$

Tuy nhiên, khi số chiều của Query và Key $(d_k)$ tăng lên, giá trị Dot Product cũng tăng theo.

Ví dụ:
- $d_k$ = 8 $\rightarrow$ Scores thường nhỏ.
- $d_k$ = 64 $\rightarrow$ Scores có thể lên đến hàng chục.

Các giá trị quá lớn sẽ làm Softmax bão hòa (saturation).
```
Scores = [15, 12, 18, 10]
   │
Softmax ≈ [0, 0, 1, 0]
```

Khi đó:

- một phần tử có xác suất gần 1,
- các phần tử còn lại gần 0,
- gradient của Softmax trở nên rất nhỏ (gradient vanishing),
- mô hình học kém hiệu quả.

Để khắc phục, Self-Attention chia điểm số cho: $\sqrt{d_k}$ công thức trở thành: $\text{Scaled Scores} = \frac {QK^T} {\sqrt{d_k}}$. Việc Scaling giúp giữ các giá trị đầu vào của Softmax trong phạm vi hợp lý, từ đó tạo ra gradient ổn định và cải thiện quá trình huấn luyện.

---

### Softmax Turns Scores into Weights

Sau khi Scaling, mỗi hàng của ma trận Scores được đưa qua __Softmax__.

```
Raw Scores
[2.1, 0.3, 0.1, 0.8, 0.2]
        │
      Softmax
        │
        ▼
[0.52, 0.09, 0.07, 0.14, 0.08]
```

Đặc điểm của Softmax:

- Chuyển điểm số thành xác suất.
- Mọi giá trị đều nằm trong khoảng [0, 1].
- Tổng các trọng số trên mỗi hàng bằng 1.

Các giá trị này được gọi là __Attention Weights__, biểu thị mức độ mà một token cần chú ý đến từng token khác trong chuỗi.

---

### Weighted Sum of Values

Bước cuối cùng là sử dụng __Attention Weights__ để tổng hợp thông tin từ các Value. Công thức:

$$Output_i = \sum_j Attention_{ij} \times V_j$$

Ví dụ với token đầu tiên:

$$Output_1 = 0.52V_1 + 0.09V_2 + 0.07V_3 + 0.14V_4 + 0.08V_5$$

Điều này có nghĩa:

- Token chú ý nhiều hơn sẽ đóng góp nhiều hơn vào kết quả.
- Token ít liên quan vẫn được sử dụng nhưng với trọng số nhỏ.
- Output là một __Context Vector__, chứa thông tin đã được tổng hợp từ toàn bộ chuỗi theo mức độ quan trọng của từng token.

---

### Full Pipeline

Toàn bộ quy trình của __Scaled Dot-Product Self-Attention__ có thể tóm tắt như sau:

```
Input Embeddings (X)
        │
        ▼
Linear Projection
        │
        ├──► Q
        ├──► K
        └──► V
               │
               ▼
             Q × Kᵀ
               │
               ▼
          Scale (÷ √dk)
               │
               ▼
            Softmax
               │
               ▼
        Attention Weights
               │
               ▼
        Weighted Sum với V
               │
               ▼
            Output
```

Toàn bộ quá trình được biểu diễn bằng một công thức duy nhất:

$$Attention(Q, K, V) = Softmax(\frac {QK^T} {\sqrt{d_k}})V$$

Đây là công thức cốt lõi của __Scaled Dot-Product Self-Attention__, kết hợp đầy đủ các bước: tính độ tương đồng (Dot Product), chuẩn hóa (Scaling), chuyển thành trọng số (Softmax) và tổng hợp thông tin (Weighted Sum).

---

## Build It

### Step 1: Softmax from Scratch

Bước đầu tiên là cài đặt **Softmax** bằng **NumPy**. Trong Self-Attention, Softmax được sử dụng để chuyển **Attention Scores** thành **Attention Weights** (phân phối xác suất).

Để đảm bảo **ổn định số học (Numerical Stability)**, trước khi tính hàm mũ, ta trừ mỗi phần tử cho giá trị lớn nhất trong cùng hàng:

$$\text{shifted} = x - \max(x)$$

Việc này không làm thay đổi kết quả của Softmax nhưng giúp tránh hiện tượng **overflow** khi tính `exp()`.

Công thức Softmax:

$$\text{Softmax}(x_i)=\frac{e^{x_i}}{\sum_{j=1}^{n}e^{x_j}}$$

#### Implementation

```python
import numpy as np

def softmax(x):
    shifted = x - np.max(x, axis=-1, keepdims=True)
    exp_x = np.exp(shifted)
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

logits = np.array([2.0, 1.0, 0.1])

print(f"logits: {logits}")
print(f"softmax: {softmax(logits)}")
print(f"sum: {softmax(logits).sum():.4f}")
```

Kết quả cho thấy Softmax biến logits thành **phân phối xác suất**, trong đó mọi giá trị nằm trong khoảng **(0, 1)** và tổng của toàn bộ xác suất luôn bằng **1**. Đây là bước chuẩn bị để tính **Attention Weights** trong Self-Attention.

---

### Step 2: Scaled Dot-Product Attention

Sau khi có hàm **Softmax**, bước tiếp theo là xây dựng **Scaled Dot-Product Attention** – thành phần cốt lõi của Self-Attention. Hàm này nhận ba ma trận **Query (Q)**, **Key (K)** và **Value (V)**, sau đó trả về **Attention Output** và **Attention Weights**.

#### Implementation

```python
def scaled_dot_product_attention(Q, K, V):
    dk = Q.shape[-1]

    scores = Q @ K.T / np.sqrt(dk)
    weights = softmax(scores)
    output = weights @ V

    return output, weights
```

#### Analysis

- Tính **Attention Scores** bằng tích vô hướng giữa **Q** và **K**, sau đó chia cho $\sqrt{d_k}$.
- Áp dụng **Softmax** để chuyển Scores thành **Attention Weights**.
- Nhân **Attention Weights** với **V** để thu được **Attention Output (Context Vector)**.
- Hàm trả về **Output** và **Attention Weights** để sử dụng và phân tích Attention.

---

### Step 3: Self-Attention Class with Learned Projections

Bước này xây dựng một lớp **SelfAttention** hoàn chỉnh. Lớp sẽ khởi tạo ba ma trận trọng số **\($W_Q$\)**, **\($W_K$\)** và **\($W_V$\)** bằng **Xavier-like initialization**, sau đó chiếu đầu vào thành **Query (Q)**, **Key (K)** và **Value (V)** trước khi tính **Scaled Dot-Product Attention**.

#### Implementation

```python
class SelfAttention:
    def __init__(self, d_model, dk, dv, seed=42):
        rng = np.random.default_rng(seed)

        scale = np.sqrt(2.0 / (d_model + dk))
        self.Wq = rng.normal(0, scale, (d_model, dk))
        self.Wk = rng.normal(0, scale, (d_model, dk))

        scale_v = np.sqrt(2.0 / (d_model + dv))
        self.Wv = rng.normal(0, scale_v, (d_model, dv))

        self.dk = dk

    def forward(self, X):
        Q = X @ self.Wq
        K = X @ self.Wk
        V = X @ self.Wv

        output, weights = scaled_dot_product_attention(Q, K, V)

        return output, weights
```

#### Analysis

- Khởi tạo các ma trận **\($W_Q$\)**, **\($W_K$\)** và **\($W_V$\)** bằng **Xavier-like scaling**.
- Chiếu embedding đầu vào thành **Query (Q)**, **Key (K)** và **Value (V)**.
- Gọi hàm **Scaled Dot-Product Attention** để tính **Attention Output** và **Attention Weights**.

---

### Step 4: Run it on a Sentence

Bước này tạo **embedding giả (fake embeddings)** cho một câu và đưa chúng vào lớp **SelfAttention** để quan sát **Attention Weights**. Mỗi hàng của ma trận Attention cho biết **token hiện tại đang chú ý đến những token nào** trong câu.

#### Implementation

```python
sentence = ["The", "cat", "sat", "on", "the", "mat"]

n_tokens = len(sentence)
d_model = 8
dk = 4
dv = 4

rng = np.random.default_rng(42)
X = rng.normal(0, 1, (n_tokens, d_model))

attn = SelfAttention(d_model, dk, dv, seed=42)
output, weights = attn.forward(X)

print("Attention weights (each row: where that token looks):\n")

print(f"{'':>6}", end="")
for token in sentence:
    print(f"{token:>6}", end="")
print()

for i, token in enumerate(sentence):
    print(f"{token:>6}", end="")
    for j in range(n_tokens):
        w = weights[i][j]
        print(f"{w:6.3f}", end="")
    print()
```

#### Analysis

- Tạo **embedding ngẫu nhiên** cho câu đầu vào.
- Đưa embedding qua lớp **SelfAttention** để tính **Attention Output** và **Attention Weights**.
- In ma trận **Attention Weights**, trong đó **mỗi hàng biểu diễn mức độ một token chú ý đến tất cả các token trong câu**.

---

## Key Term

| **Term**                         | **What people say**                      | **What it actually means**                                                                                                                                                               |
| -------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Query (Q)**                    | *"The question vector"*                  | Là vector được học từ embedding đầu vào, biểu diễn **token đang tìm kiếm thông tin gì**. Query sẽ được so sánh với tất cả Key để xác định mức độ liên quan.                              |
| **Key (K)**                      | *"The label vector"*                     | Là vector được học từ embedding đầu vào, biểu diễn **token chứa thông tin gì**. Key được dùng để so khớp với Query nhằm tính Attention Score.                                            |
| **Value (V)**                    | *"The content vector"*                   | Là vector mang **nội dung thực sự** của token. Sau khi tính Attention Weights, các Value sẽ được tổng hợp thành Context Vector.                                                          |
| **Scaled Dot-Product Attention** | *"The attention formula"*                | Công thức cốt lõi của Self-Attention:  $\text{Softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$. Việc chia cho $\sqrt{d_k}$ giúp tránh hiện tượng **Softmax saturation** khi số chiều lớn.  |
| **Self-Attention**               | *"The token looks at itself and others"* | Cơ chế Attention trong đó **Q, K và V đều được tạo từ cùng một chuỗi đầu vào**, cho phép mỗi token chú ý đến chính nó và tất cả các token khác trong chuỗi.                              |
| **Attention Weights**            | *"How much focus"*                       | Là **phân phối xác suất** thu được sau Softmax trên các Attention Scores. Mỗi trọng số biểu thị mức độ mà một token cần chú ý đến các token khác. Tổng trọng số trên mỗi hàng bằng 1.    |
| **Multi-Head Attention**         | *"Parallel attention"*                   | Chạy **nhiều Self-Attention song song** với các phép chiếu Q, K, V khác nhau, sau đó nối (concatenate) kết quả để tạo biểu diễn giàu thông tin hơn.                                      |
