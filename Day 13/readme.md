# Word Emdbeddings - Word2Vec From Scartch

## The Problem
- TF-IDF biểu diễn mỗi từ độc lập → biết `dog` và `puppy` là hai từ khác nhau nhưng __không biết chúng gần nghĩa nhau__.

- Vì vậy, classifier học từ `dog` khó tự tổng quát sang `puppy`.

- Việc liệt kê synonym không giải quyết tốt với:
    - từ hiếm,
    - domain jargon,
    - ngôn ngữ mới.

## Word2Vec Giải quyết thế nào?

Word2Vec học __dense vector representation__ cho mỗi từ dựa trên __ngữ cảnh xuất hiện của nó__:

$$\text{Similar Context } \Rightarrow \text{ Similar vectors}$$

Do đó:

$$v_{dog} \approx v_{puppy}$$

và các quan hệ ngữ nghĩa có thể xuất hiện dưới dạng __geometry trong vector space__, ví dụ:

$$v_{king} - v_{man}  + v_{woman} \approx v_{queen}$$

> A word is the company it keeps.

Word2Vec dùng một __mạng neural 2-layer rất đơn giản__, train trên lượng text lớn để học quan hệ giữa word và context, từ đó hình thành không gian embedding có cấu trúc ngữ nghĩa.

## The Concept

### 1. Distributional Hypothesis

> “You shall know a word by the company it keeps.”

Nếu hai từ xuất hiện trong ngữ cảnh tương tự, chúng có khả năng có ý nghĩa tương tự.

### 2. Hai cách học

#### Skip-gram

$$\text{center word } \rightarrow \text{ surrounding workds}$$

Ví dụ:

`cat → the, sat, on`

- Train chậm hơn.
- Xử lý __rare words__ tốt hơn.
- Trở thành cách dùng phổ biến.

#### CBOW

$$\text{surrounding workds } \rightarrow \text{ center word}$$

`(the, sat, on) → cat`

### 3. Kiến trúc

```
one-hot(center)
      │
      ▼
      W
      │
      ▼
hidden (d-dim)  ← Word Embedding
      │
      ▼
      W'
      │
      ▼
softmax(vocabulary)
```

- Input: __one-hot vector__ trên vocabulary.
- Hidden layer: __không có nonlinearity__.
- Output: __softmax__ trên toàn vocabulary.
- Sau training, __bỏ output layer__.
- Trọng số của hidden layer _W_ chính là __word embeddings__.

### 4. Negative Sampling

Softmax trên vocabulary lớn, ví dụ __100k từ__, rất tốn chi phí.

Word2Vec thay bằng __binary classification__:

> Context word có xuất hiện gần center word không?

```
(center, real context)    → 1
(center, negative word)   → 0
```

Chỉ lấy một số __negative samples__ thay vì tính softmax trên toàn bộ vocabulary.

$$\text{Context similarity } \rightarrow \text{ Word vectors } \rightarrow \text{ Semantic geometry}$$

## Built It

### Step 1: Training Pairs from a Corpus

```python
def skipgram_pairs(docs, window=2):
    pairs = []

    for doc in docs:
        for i, center in enumerate(doc):
            start = max(0, i - window)
            end = min(len(doc), i + window + 1)

            for j in range(start, end):
                if i == j:
                    continue

                pairs.append((center, doc[j]))

    return pairs
```

#### Example

```python
>>> skipgram_pairs(
...     [["the", "cat", "sat", "on", "mat"]],
...     window=2
... )

[
    ("the", "cat"),
    ("the", "sat"),
    ("cat", "the"),
    ("cat", "sat"),
    ("cat", "on"),
    ("sat", "the"),
    ("sat", "cat"),
    ("sat", "on"),
    ("sat", "mat"),
    ...
]
```

Mỗi cặp: `(center, context)` là một **positive training example**: hai từ xuất hiện trong cùng một cửa sổ ngữ cảnh.

### Step 2: Embedding Tables

Word2Vec sử dụng **hai embedding tables**:

* $W$: **center-word embedding table** — bảng embedding chính được giữ lại sau training.
* $W'$: **context-word table** — bảng embedding của context, thường được loại bỏ sau training.

```python
import numpy as np

def init_embeddings(vocab_size, dim, seed=0):
    rng = np.random.default_rng(seed)

    W = rng.normal(0, 0.1, size=(vocab_size, dim))
    W_prime = rng.normal(0, 0.1, size=(vocab_size, dim))

    return W, W_prime
```

#### Shape

Với: $V = 10{,}000,\qquad d = 100$ thì: $W,W' \in \mathbb{R}^{V\times d}$ Mỗi **row** tương ứng với một word vector.

#### Key Idea

```text
Center word ──→ W ──→ word embedding
Context word ──→ W' ──→ context embedding
```

Hai ma trận được khởi tạo bằng **giá trị ngẫu nhiên nhỏ** và được cập nhật trong quá trình training.

Sau training:

$$\boxed{W = \text{Word Embeddings}}$$

Trong thực hành học từ đầu, có thể dùng vocabulary nhỏ và embedding dimension nhỏ để dễ quan sát geometry.

### Step 3: Negative Sampling Objective

Với mỗi **positive pair** $(center, context)$, lấy $k$ từ ngẫu nhiên trong vocabulary làm **negative samples**.

Mục tiêu:

$$
W[center]\cdot W'[context] \rightarrow \text{high}
$$

$$
W[center]\cdot W'[negative] \rightarrow \text{low}
$$

#### Sigmoid

```python
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))
```

#### Training a Pair

```python
def train_pair(W, W_prime, center_idx, context_idx, negative_indices, lr):
    v_c = W[center_idx]
    u_pos = W_prime[context_idx]
    u_negs = W_prime[negative_indices]

    pos_score = sigmoid(v_c @ u_pos)
    neg_scores = sigmoid(u_negs @ v_c)

    grad_center = (pos_score - 1) * u_pos

    for i, u in enumerate(u_negs):
        grad_center += neg_scores[i] * u

    W_prime[context_idx] -= lr * (pos_score - 1) * v_c

    for i, neg_idx in enumerate(negative_indices):
        W_prime[neg_idx] -= lr * neg_scores[i] * v_c

    W[center_idx] -= lr * grad_center
```

#### Objective

Negative sampling biến bài toán thành **binary classification**:

* Positive pair → muốn $\sigma(score)\rightarrow1$.
* Negative pair → muốn $\sigma(score)\rightarrow0$.

Loss tương ứng:

$$\mathcal{L}= -\log\sigma(v_c^\top u_{pos}) \sum_{i=1}^{k}\log\sigma(-v_c^\top u_{neg_i})$$

Gradient được truyền vào **cả hai embedding tables** $W$ và $W'$.

> **Core idea:** tăng dot product cho cặp $(center, context)$ thật và giảm dot product cho các cặp negative.

### Step 4: Train on a Toy Corpus

```python
def train(docs, dim=16, window=2, k_neg=5, epochs=100, lr=0.05, seed=0):
    vocab = build_vocab(docs)
    vocab_size = len(vocab)

    rng = np.random.default_rng(seed)
    W, W_prime = init_embeddings(vocab_size, dim, seed=seed)

    pairs = skipgram_pairs(docs, window=window)

    for epoch in range(epochs):
        rng.shuffle(pairs)

        for center, context in pairs:
            c_idx = vocab[center]
            ctx_idx = vocab[context]

            negs = rng.integers(0, vocab_size, size=k_neg)

            negs = [n for n in negs if n != ctx_idx and n != c_idx]

            train_pair(W, W_prime, c_idx, ctx_idx, negs, lr)

    return vocab, W
```

#### Training Flow

```text
Corpus
  ↓
Build vocabulary
  ↓
Create (center, context) pairs
  ↓
Sample negative words
  ↓
Train with negative sampling
  ↓
Update W and W'
  ↓
Return W as word embeddings
```

Sau đủ nhiều epochs, các từ xuất hiện trong **ngữ cảnh tương tự** sẽ có center embeddings tương tự.

* **Toy corpus:** hiệu ứng xuất hiện yếu.
* **Corpus rất lớn:** cấu trúc ngữ nghĩa trong embedding space rõ ràng hơn.

### Step 5: The Analogy Trick

Word2Vec có thể tìm từ gần nhất với một vector bằng **cosine similarity**.

```python
def nearest(vocab, W, target_vec, topk=5, exclude=None):
    exclude = exclude or set()

    inv_vocab = {i: w for w, i in vocab.items()}

    norms = np.linalg.norm(W, axis=1, keepdims=True) + 1e-9
    W_norm = W / norms

    target = target_vec / (np.linalg.norm(target_vec) + 1e-9)

    sims = W_norm @ target
    order = np.argsort(-sims)

    out = []

    for i in order:
        if i in exclude:
            continue
        out.append((inv_vocab[i], float(sims[i])))
        if len(out) == topk:
            break

    return out
```

#### Analogy

Tạo vector bằng phép toán: $v = W[b] - W[a] + W[c]$ Sau đó tìm các từ có vector gần $v$ nhất.

```python
def analogy(vocab, W, a, b, c, topk=5):
    v = W[vocab[b]] - W[vocab[a]] + W[vocab[c]]
    return nearest(vocab, W, v, topk=topk, exclude={vocab[a], vocab[b], vocab[c]})
```

Ví dụ:

```text
man → king
woman → ?
```

Ta tính: $v_{king} - v_{man} + v_{woman} \approx v_{queen}$

Kết quả có thể là:

```text
queen       0.71
monarch     0.62
princess    0.59
...
```

#### Ý nghĩa

Word2Vec không **hiểu trực tiếp** khái niệm royalty. Phép analogy xuất hiện vì các quan hệ giữa từ có thể được biểu diễn như **hướng trong vector space**.

$$\boxed{king - man + woman \approx queen}$$

## When Word2Vec Still Wins in 2026

* **Lightweight domain-specific retrieval:** Train trên corpus chuyên ngành để tạo vector đặc thù với chi phí thấp.
* **Analogy-style feature engineering:** Có thể tạo các vector quan hệ và thao tác trực tiếp trên không gian embedding.
* **Interpretability:** Embedding nhỏ như 100d dễ trực quan hóa bằng PCA hoặc t-SNE để quan sát các cluster.
* **On-device inference:** Lookup embedding chỉ cần lấy một row từ ma trận, phù hợp khi không có GPU.

## Where Word2Vec Fails

### 1. Polysemy

Word2Vec tạo **một vector cố định cho mỗi từ**.

Ví dụ:

```text
bank → river bank
bank → financial bank
```

Cả hai nghĩa đều dùng chung một vector: $v_{bank}$ Do đó classifier phía sau không thể phân biệt hai sense chỉ từ vector này.

**Contextual embeddings** như ELMo và BERT giải quyết bằng cách tạo vector khác nhau cho mỗi lần xuất hiện, dựa trên context.

$$\boxed{\text{Word2Vec: static} \rightarrow \text{BERT: contextual}}$$

### 2. Out-of-Vocabulary (OOV)

Nếu một từ **không xuất hiện trong training data**, Word2Vec không có embedding cho từ đó và không có fallback.

**fastText** giải quyết vấn đề này bằng **subword composition**.

$$\boxed{\text{Word2Vec} \rightarrow \text{static + word-level}}$$

$$\boxed{\text{fastText} \rightarrow \text{subword-level}}$$

## Thuật ngữ chính — Word2Vec

| Thuật ngữ                | What people say | Ý nghĩa thực sự                                                                              |
| ------------------------ | ------------------------- | -------------------------------------------------------------------------------------------- |
| **Word embedding**       | Từ dưới dạng vector       | Biểu diễn dày, có số chiều thấp (thường 100–300 chiều), được học từ ngữ cảnh.                |
| **Skip-gram**            | Kỹ thuật của Word2Vec     | Dự đoán các từ ngữ cảnh từ một từ trung tâm. Chậm hơn CBOW nhưng tốt hơn với các từ hiếm.    |
| **Negative sampling**    | Thủ thuật huấn luyện      | Thay softmax trên toàn bộ vocabulary bằng bài toán phân loại nhị phân với (k) từ ngẫu nhiên. |
| **Static embedding**     | Một vector cho mỗi từ     | Một từ luôn có cùng một vector, bất kể ngữ cảnh; không xử lý tốt hiện tượng đa nghĩa.        |
| **Contextual embedding** | Vector phụ thuộc ngữ cảnh | Mỗi lần xuất hiện của từ có một vector khác nhau dựa trên các từ xung quanh.                 |
| **OOV**                  | Từ ngoài vocabulary       | Từ không xuất hiện trong dữ liệu huấn luyện; Word2Vec không thể tạo vector cho từ này.       |
