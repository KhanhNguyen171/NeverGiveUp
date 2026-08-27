# GloVe, FastText và Subword Embeddings

## 1. Mục tiêu của bài học

Word2Vec đặt nền tảng cho **word embedding** bằng cách học một vector cho mỗi từ. Tuy nhiên, cách biểu diễn này còn ba hạn chế quan trọng:

1. **Word2Vec chỉ học trực tiếp từ các cặp từ**, trong khi trước đó đã có các phương pháp xây dựng embedding bằng cách phân rã ma trận đồng xuất hiện.
2. **Từ chưa từng xuất hiện trong vocabulary (OOV)** không có vector biểu diễn.
3. Khi xây dựng các mô hình ngôn ngữ lớn, vocabulary ở cấp độ từ trở nên quá lớn và không thể bao phủ toàn bộ ngôn ngữ.

Ba hướng phát triển quan trọng giải quyết các vấn đề trên là:

* **GloVe**: học embedding từ ma trận đồng xuất hiện.
* **FastText**: biểu diễn từ bằng các **character n-gram**, cho phép xử lý từ chưa biết.
* **BPE (Byte-Pair Encoding)** và các biến thể: chia văn bản thành các **subword token**, trở thành nền tảng của tokenizer trong thời đại Transformer.

Có thể nhìn quá trình phát triển như sau:

```text
Word2Vec
   │
   ├── Học vector cho từng từ
   │
   ▼
GloVe
   │
   └── Khai thác trực tiếp thống kê đồng xuất hiện
   │
   ▼
FastText
   │
   └── Biểu diễn từ bằng các character n-gram
   │
   ▼
BPE / WordPiece / SentencePiece
   │
   └── Biểu diễn văn bản bằng các subword token
   │
   ▼
Transformer / LLM
```

---

# 2. GloVe — Global Vectors

## 2.1. Ý tưởng

GloVe (**Global Vectors for Word Representation**) xuất phát từ một ý tưởng đơn giản:

> Nếu hai từ thường xuyên xuất hiện trong cùng một ngữ cảnh, vector của chúng nên có quan hệ phù hợp với mức độ đồng xuất hiện đó.

Thay vì cập nhật embedding trực tiếp qua từng cặp training example như Word2Vec, GloVe trước tiên xây dựng một **ma trận đồng xuất hiện**.

Gọi:

$$
X_{ij}
$$

là số lần từ $j$ xuất hiện trong cửa sổ ngữ cảnh của từ $i$.

Khi đó:

$$
X \in \mathbb{R}^{|V| \times |V|}
$$

với $|V|$ là kích thước vocabulary.

Ví dụ:

| Center | Context | Count |
| ------ | ------- | ----: |
| king   | queen   |    20 |
| king   | man     |    15 |
| king   | woman   |    12 |
| queen  | woman   |    25 |

Ma trận này chứa thông tin thống kê toàn cục của corpus.

---

## 2.2. Xây dựng ma trận đồng xuất hiện

Một cách đơn giản để xây dựng $X$ là sử dụng cửa sổ ngữ cảnh.

Với một câu:

```text
the cat sits on the mat
```

và `window = 2`, khi xét từ `cat`, các từ trong vùng lân cận có thể là:

```text
the  cat  sits  on
```

Ta tăng số lần xuất hiện của các cặp:

```text
(cat, the)
(cat, sits)
(cat, on)
```

Có thể giảm trọng số của những từ ở xa bằng khoảng cách:

$$
X_{ij}
\mathrel{+}= \frac{1}{|i-j|}
$$

Do đó, từ càng gần center word thì đóng góp càng lớn.

### Cài đặt

```python
import numpy as np
from collections import Counter


def build_cooccurrence(docs, window=5):
    pair_counts = Counter()
    vocab = {}

    # Build vocabulary
    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)

    # Build co-occurrence counts
    for doc in docs:
        indexed = [vocab[t] for t in doc]

        for i, center in enumerate(indexed):
            start = max(0, i - window)
            end = min(len(indexed), i + window + 1)

            for j in range(start, end):
                if i == j:
                    continue

                distance = abs(i - j)
                pair_counts[(center, indexed[j])] += 1.0 / distance

    return vocab, pair_counts
```

---

# 3. Mục tiêu học của GloVe

GloVe muốn tìm hai ma trận embedding:

$$
W
$$

và

$$
\widetilde{W}
$$

Trong đó:

* $W_i$: vector của từ khi đóng vai trò center word.
* $\widetilde{W}_j$: vector của từ khi đóng vai trò context word.

Mô hình muốn:

$$
W_i^\top \widetilde{W}_j
+
b_i
+
\widetilde{b}_j
\approx
\log X_{ij}
$$

Hay viết dưới dạng hàm loss:

$$
J =
\sum_{i,j}
f(X_{ij})
\left(
W_i^\top \widetilde{W}_j
+
b_i
+
\widetilde{b}_j
-
\log X_{ij}
\right)^2
$$

Ý nghĩa:

> GloVe cố gắng học các vector sao cho tích vô hướng giữa hai vector phản ánh logarithm của mức độ đồng xuất hiện.

---

## 3.1. Vì sao dùng $\log(X_{ij})$?

Tần suất đồng xuất hiện có thể chênh lệch rất lớn.

Ví dụ:

```text
(the, and)      = 100000
(king, queen)   = 500
(king, throne)  = 20
```

Nếu sử dụng trực tiếp $X_{ij}$, những cặp cực kỳ phổ biến sẽ có ảnh hưởng quá lớn.

Sử dụng:

$$
\log X_{ij}
$$

giúp nén phạm vi giá trị.

Ví dụ:

$$
\log(100000)
<
100000
$$

Do đó, các khác biệt quá lớn về frequency được giảm bớt.

---

# 4. Weighting function của GloVe

GloVe tiếp tục sử dụng một weighting function:

$$
f(x)=
\begin{cases}
\left(\dfrac{x}{x_{\max}}\right)^\alpha,
& x < x_{\max},\\[6pt]
1,
& x \geq x_{\max}.
\end{cases}
$$

Trong đó:

* $x = X_{ij}$: số lần đồng xuất hiện.
* $x_{\max}$: ngưỡng frequency.
* $\alpha$: điều khiển mức độ giảm trọng số.

Thông thường:

$$
\alpha = 0.75
$$

### Ý nghĩa trực quan

```text
Frequency thấp
      │
      ▼
Có thể vẫn giữ thông tin
      │
      ▼
Weight tăng dần
      │
      ▼
Frequency rất cao
      │
      ▼
Weight bị giới hạn
```

Mục tiêu là tránh để những cặp từ quá phổ biến như:

```text
the, of, and, to
```

chi phối toàn bộ quá trình học.

---

# 5. Huấn luyện GloVe

Một implementation tối giản:

```python
def glove_train(
    vocab,
    pair_counts,
    dim=16,
    epochs=100,
    lr=0.05,
    x_max=100,
    alpha=0.75,
    seed=0
):
    n = len(vocab)
    rng = np.random.default_rng(seed)

    W = rng.normal(0, 0.1, size=(n, dim))
    W_tilde = rng.normal(0, 0.1, size=(n, dim))

    b = np.zeros(n)
    b_tilde = np.zeros(n)

    for epoch in range(epochs):
        for (i, j), x_ij in pair_counts.items():

            if x_ij < x_max:
                weight = (x_ij / x_max) ** alpha
            else:
                weight = 1.0

            diff = (
                W[i] @ W_tilde[j]
                + b[i]
                + b_tilde[j]
                - np.log(x_ij)
            )

            coef = weight * diff

            grad_W_i = coef * W_tilde[j]
            grad_W_tilde_j = coef * W[i]

            W[i] -= lr * grad_W_i
            W_tilde[j] -= lr * grad_W_tilde_j

            b[i] -= lr * coef
            b_tilde[j] -= lr * coef

    return W + W_tilde
```

Embedding cuối cùng được tạo bằng:

$$
E_i = W_i + \widetilde{W}_i
$$

Việc cộng hai embedding table thường cho biểu diễn tốt hơn so với chỉ sử dụng một bảng.

---

# 6. GloVe và Word2Vec khác nhau như thế nào?

| Đặc điểm      | Word2Vec              | GloVe                              |
| ------------- | --------------------- | ---------------------------------- |
| Cách tiếp cận | Predictive            | Count-based / factorization        |
| Dữ liệu chính | Các training pair     | Ma trận đồng xuất hiện             |
| Thông tin     | Local context         | Global co-occurrence statistics    |
| Objective     | Dự đoán context       | Factorize co-occurrence statistics |
| OOV           | Không xử lý trực tiếp | Không xử lý trực tiếp              |
| Embedding     | Word-level            | Word-level                         |

Điểm quan trọng:

> GloVe không đơn giản là "Word2Vec nhanh hơn". Hai phương pháp bắt đầu từ hai cách nhìn khác nhau về thông tin ngôn ngữ.

Word2Vec:

```text
Context
   ↓
Predict word
   ↓
Update embedding
```

GloVe:

```text
Corpus
   ↓
Co-occurrence matrix X
   ↓
Factorization
   ↓
Embedding
```

---

# 7. FastText — Subword-aware Embeddings

## 7.1. Vấn đề của Word2Vec và GloVe

Word2Vec và GloVe đều có một giả định:

> Mỗi từ có một vector riêng.

Ví dụ:

```text
playing  → vector A
played   → vector B
player   → vector C
```

Nếu từ:

```text
zoomerapproved
```

không xuất hiện trong vocabulary khi training, mô hình không có vector trực tiếp cho nó.

Đây là vấn đề **OOV — Out Of Vocabulary**.

FastText giải quyết bằng cách không xem từ là một đơn vị nguyên khối.

Thay vào đó:

> Một từ được biểu diễn bằng tổng các vector của các character n-gram cấu thành nó.

---

# 8. Character n-gram

Ví dụ với từ:

```text
where
```

FastText thêm boundary markers:

```text
<where>
```

Sau đó lấy các character n-gram, thường trong khoảng:

$$
3 \leq n \leq 6
$$

Ví dụ:

```text
<wh
whe
her
ere
re>

<whe
wher
here
ere>

<wher
where
ere>
```

Ngoài ra, toàn bộ từ cũng có thể được đưa vào biểu diễn:

```text
<where>
```

Do đó, word embedding có thể được mô hình hóa:

$$
v_{\text{where}}
=
\sum_{g \in G(\text{where})} z_g
$$

Trong đó:

* $G(\text{where})$: tập character n-gram.
* $z_g$: vector của n-gram $g$.

---

## 8.1. Cài đặt character n-gram

```python
def char_ngrams(word, n_min=3, n_max=6):
    wrapped = f"<{word}>"
    grams = {wrapped}

    for n in range(n_min, n_max + 1):
        for i in range(len(wrapped) - n + 1):
            grams.add(wrapped[i:i + n])

    return grams
```

Ví dụ:

```python
char_ngrams("where")
```

có thể tạo ra:

```text
{
    "<where>",
    "<wh",
    "whe",
    "her",
    "ere",
    "re>",
    "<whe",
    "wher",
    "here",
    "ere>",
    "<wher",
    "where"
}
```

---

# 9. Tạo vector FastText

Giả sử bảng embedding của các n-gram là:

$$
Z = \{z_g\}
$$

Khi đó:

$$
v_w
=
\sum_{g \in G(w)} z_g
$$

Implementation:

```python
def fasttext_vector(word, ngram_table):
    grams = char_ngrams(word)

    vecs = [
        ngram_table[g]
        for g in grams
        if g in ngram_table
    ]

    if not vecs:
        return None

    return np.sum(vecs, axis=0)
```

Điểm quan trọng là FastText vẫn có thể tạo vector cho một từ chưa từng xuất hiện.

---

# 10. FastText giải quyết OOV như thế nào?

Giả sử training corpus đã xuất hiện:

```text
where
```

nhưng chưa xuất hiện:

```text
whereupon
```

`whereupon` có thể chứa những n-gram đã từng xuất hiện trong các từ khác.

Ví dụ:

```text
<wh
whe
her
ere
...
```

Do đó:

```text
whereupon
       ↓
character n-grams
       ↓
known n-gram vectors
       ↓
sum
       ↓
vector của "whereupon"
```

Đây là điểm khác biệt quan trọng:

```text
Word2Vec / GloVe

unknown word
     ↓
    OOV
     ↓
 no vector


FastText

unknown word
     ↓
character n-grams
     ↓
known pieces
     ↓
compose vector
```

---

# 11. Vì sao FastText hữu ích với morphology?

FastText đặc biệt hữu ích khi các từ có cấu trúc hình thái liên quan.

Ví dụ:

```text
play
playing
played
player
```

Các từ này chia sẻ nhiều character n-gram.

Do đó, mô hình có thể truyền tải thông tin giữa chúng.

Điều này đặc biệt hữu ích với:

* ngôn ngữ có nhiều biến thể hình thái;
* từ hiếm;
* từ mới;
* lỗi chính tả;
* tên riêng;
* neologism.

---

# 12. BPE — Byte-Pair Encoding

## 12.1. Từ word embedding sang tokenizer

Khi Transformer và Language Model phát triển, vấn đề thay đổi.

Không còn chỉ hỏi:

> "Làm sao tạo vector cho một từ?"

Mà hỏi:

> "Làm sao chia toàn bộ văn bản thành một vocabulary có kích thước hữu hạn nhưng vẫn biểu diễn được mọi input?"

Nếu dùng word-level vocabulary:

```text
cat
dog
running
...
```

vocabulary có thể phải chứa hàng trăm nghìn hoặc hàng triệu từ.

Tệ hơn, ngôn ngữ liên tục tạo ra:

```text
từ mới
tên riêng
sai chính tả
biến thể
thuật ngữ mới
```

Do đó cần một đơn vị nhỏ hơn từ:

**subword token**.

---

# 13. Ý tưởng của BPE

BPE bắt đầu từ các đơn vị nhỏ:

```text
character / byte
```

Sau đó lặp lại:

1. Đếm các cặp token liền kề.
2. Tìm cặp xuất hiện nhiều nhất.
3. Gộp cặp đó thành một token mới.
4. Lặp lại cho đến khi đạt số lượng merge mong muốn.

Ví dụ:

```text
l o w
```

Nếu:

```text
(l, o)
```

là cặp phổ biến nhất:

```text
lo w
```

Sau đó:

```text
(lo, w)
```

lại phổ biến:

```text
low
```

BPE học được:

```text
l + o       → lo
lo + w      → low
```

---

# 14. Thuật toán BPE

Giả sử corpus:

```python
corpus = {
    "low": 5,
    "lower": 2,
    "newest": 6,
    "widest": 3
}
```

Ban đầu:

```text
l o w </w>
l o w e r </w>
n e w e s t </w>
w i d e s t </w>
```

Sau mỗi lần merge, vocabulary token thay đổi.

Ví dụ:

```text
l o w
↓
lo w
↓
low
```

Nếu `low` xuất hiện thường xuyên, nó trở thành một token có giá trị.

---

# 15. Cài đặt BPE từ đầu

```python
from collections import Counter


def learn_bpe(corpus, k_merges):
    vocab = Counter()

    for word, freq in corpus.items():
        tokens = tuple(word) + ("</w>",)
        vocab[tokens] = freq

    merges = []

    for _ in range(k_merges):
        pair_freq = Counter()

        for tokens, freq in vocab.items():
            for a, b in zip(tokens, tokens[1:]):
                pair_freq[(a, b)] += freq

        if not pair_freq:
            break

        best = pair_freq.most_common(1)[0][0]
        merges.append(best)

        new_vocab = Counter()

        for tokens, freq in vocab.items():
            new_tokens = []
            i = 0

            while i < len(tokens):
                if (
                    i + 1 < len(tokens)
                    and (tokens[i], tokens[i + 1]) == best
                ):
                    new_tokens.append(tokens[i] + tokens[i + 1])
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1

            new_vocab[tuple(new_tokens)] = freq

        vocab = new_vocab

    return merges
```

Sau khi học merge rules, ta áp dụng chúng vào từ mới:

```python
def apply_bpe(word, merges):
    tokens = list(word) + ["</w>"]

    for a, b in merges:
        new_tokens = []
        i = 0

        while i < len(tokens):
            if (
                i + 1 < len(tokens)
                and tokens[i] == a
                and tokens[i + 1] == b
            ):
                new_tokens.append(a + b)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1

        tokens = new_tokens

    return tokens
```

Ví dụ:

```python
corpus = Counter({
    "low": 5,
    "lower": 2,
    "newest": 6,
    "widest": 3
})

merges = learn_bpe(corpus, k_merges=10)

apply_bpe("lowest", merges)
```

Có thể thu được:

```python
["low", "est</w>"]
```

Điều này cho thấy từ `lowest` không nhất thiết phải tồn tại trong vocabulary.

Nó có thể được phân rã thành:

```text
lowest
  ↓
low + est
```

---

# 16. BPE giải quyết OOV

Đây là một trong những lý do subword tokenizer trở nên quan trọng.

Giả sử vocabulary có:

```text
low
est
ing
tion
```

Một từ mới:

```text
lowest
```

có thể được phân tách:

```text
low + est
```

Một từ khác:

```text
unbelievably
```

có thể được phân tách thành nhiều token nhỏ hơn.

Do đó, mô hình không cần phải biết toàn bộ từ trước.

```text
Unknown word
     ↓
Subword decomposition
     ↓
Known tokens
     ↓
Token IDs
     ↓
Embedding
```

---

# 17. Byte-level BPE

Một biến thể quan trọng là **byte-level BPE**.

Thay vì bắt đầu từ toàn bộ character vocabulary, vocabulary cơ sở có thể bắt đầu từ:

$$
256
$$

byte values.

Ưu điểm:

> Mọi chuỗi text đều có thể được biểu diễn bằng bytes.

Do đó, về nguyên tắc không cần một token `UNK` chỉ vì gặp một ký tự hoàn toàn mới.

Đây là ý tưởng quan trọng trong các tokenizer hiện đại.

---

# 18. BPE và Transformer

Trong thời đại Transformer, BPE không còn chủ yếu là phương pháp học **word embedding**.

Nó là phương pháp xây dựng **tokenizer**.

Pipeline có thể mô tả:

```text
Raw text
   ↓
Tokenizer
   ↓
Subword tokens
   ↓
Token IDs
   ↓
Embedding layer
   ↓
Transformer
```

Ví dụ một tokenizer kiểu GPT-2 có thể biến:

```text
unbelievably tokenized
```

thành các token gần dạng:

```text
un
bel
iev
ably
Ġtoken
ized
```

Ký hiệu:

```text
Ġ
```

trong tokenizer GPT-2 là một quy ước biểu diễn khoảng trắng / ranh giới từ.

Điểm cần nhớ:

> Tokenizer và embedding là hai thành phần khác nhau.

BPE quyết định:

```text
text → token IDs
```

Còn embedding layer quyết định:

```text
token ID → vector
```

---

# 19. BPE, WordPiece và SentencePiece

BPE không phải tokenizer duy nhất.

Các hệ thống phổ biến gồm:

| Phương pháp    | Ý tưởng chính                               |
| -------------- | ------------------------------------------- |
| BPE            | Merge các cặp token phổ biến                |
| WordPiece      | Học subword vocabulary theo objective riêng |
| SentencePiece  | Tokenization trực tiếp trên raw text        |
| Byte-level BPE | BPE bắt đầu từ byte                         |

Có thể khái quát:

```text
Word-level
    ↓
Subword-level
    ↓
Character-level
    ↓
Byte-level
```

Mục tiêu chung là tìm sự cân bằng giữa:

* vocabulary size;
* độ dài chuỗi token;
* khả năng biểu diễn từ hiếm;
* khả năng xử lý input mới.

---

# 20. So sánh GloVe, FastText và BPE

| Đặc điểm             | GloVe                     | FastText             | BPE              |
| -------------------- | ------------------------- | -------------------- | ---------------- |
| Đơn vị chính         | Word                      | Word + n-gram        | Subword          |
| Mục đích             | Word embedding            | Word embedding       | Tokenization     |
| Học từ co-occurrence | Có                        | Không trực tiếp      | Không            |
| Character n-gram     | Không                     | Có                   | Không nhất thiết |
| Xử lý OOV            | Không                     | Có                   | Có               |
| Từ mới               | Hạn chế                   | Tốt                  | Tốt              |
| Morphology           | Hạn chế                   | Tốt                  | Tốt              |
| Transformer          | Không phải lựa chọn chính | Không phải tokenizer | Rất phổ biến     |
| Output               | Word vectors              | Word vectors         | Token sequence   |

Điểm quan trọng nhất:

> **GloVe và FastText là phương pháp học representation; BPE chủ yếu là phương pháp tokenization.**

Không nên xem BPE đơn giản là "một phiên bản FastText".

---

# 21. Khi nào sử dụng phương pháp nào?

## 21.1. GloVe

Chọn GloVe khi:

* cần pretrained word vectors;
* mô hình downstream hoạt động ở cấp độ word;
* vocabulary tương đối ổn định;
* không có yêu cầu cao về OOV.

Ví dụ:

```text
Text
 ↓
Word
 ↓
GloVe 300d
 ↓
Classifier
```

---

## 21.2. FastText

Chọn FastText khi:

* cần xử lý từ hiếm;
* có nhiều từ mới;
* có lỗi chính tả;
* ngôn ngữ có morphology phong phú;
* cần embedding cho các từ chưa xuất hiện trong training vocabulary.

Pipeline:

```text
Word
 ↓
Character n-grams
 ↓
Subword vectors
 ↓
Sum
 ↓
Word vector
```

---

## 21.3. BPE / tokenizer của model

Nếu input đi vào một Transformer pretrained:

> **Không tự ý thay tokenizer của model.**

Tokenizer và model được huấn luyện cùng nhau.

Ví dụ:

```text
Tokenizer vocabulary
        ↕
Embedding matrix
        ↕
Transformer
```

Nếu thay tokenizer, mapping giữa:

```text
token ID ↔ embedding vector
```

không còn tương thích.

Do đó, khi sử dụng model pretrained:

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")
```

nên sử dụng chính tokenizer mà checkpoint cung cấp.

---

# 22. Nếu train Language Model từ đầu

Khi xây dựng một language model từ đầu, quy trình thường là:

```text
Corpus
   ↓
Train tokenizer
   ↓
BPE / WordPiece / SentencePiece
   ↓
Vocabulary
   ↓
Token IDs
   ↓
Train Transformer
```

Tokenizer nên được học trên corpus phù hợp với domain của model.

Một vocabulary quá nhỏ:

```text
nhiều token / từ
```

Một vocabulary quá lớn:

```text
ít token / từ
nhưng embedding matrix lớn
```

Vì vậy cần tìm trade-off phù hợp.

---

# 23. Bản chất của ba phương pháp

Có thể cô đọng toàn bộ bài học thành ba câu:

### GloVe

> **Nhìn vào thống kê đồng xuất hiện toàn cục để học vector cho từ.**

$$
X_{ij}
\rightarrow
\log X_{ij}
\rightarrow
\text{factorization}
\rightarrow
\text{word vectors}
$$

### FastText

> **Nhìn từ như một tập hợp các mảnh character n-gram.**

$$
w
\rightarrow
G(w)
\rightarrow
\sum_{g \in G(w)} z_g
\rightarrow
v_w
$$

### BPE

> **Nhìn văn bản như một chuỗi subword và học cách gộp những mảnh xuất hiện thường xuyên.**

$$
\text{characters / bytes}
\rightarrow
\text{frequent pair merges}
\rightarrow
\text{subword vocabulary}
$$

---

# 24. Tổng kết

Sự phát triển có thể được nhìn theo vấn đề mà mỗi phương pháp giải quyết:

```text
                 Word2Vec
                    │
                    │
           Word-level embedding
                    │
          ┌─────────┴─────────┐
          │                   │
       GloVe              FastText
          │                   │
 Global statistics       Subword n-grams
          │                   │
          │              OOV / morphology
          │
          └─────────┬─────────┘
                    │
                    ▼
             Subword Tokenization
                    │
          ┌─────────┼─────────┐
          │         │         │
         BPE    WordPiece  SentencePiece
          │         │         │
          └─────────┼─────────┘
                    ▼
               Transformer
                    │
                    ▼
                   LLM
```

Ba khái niệm cần phân biệt rõ:

1. **GloVe** — học word embedding từ **co-occurrence statistics**.
2. **FastText** — học word embedding bằng **character n-grams**, giúp xử lý OOV.
3. **BPE** — học **subword vocabulary** bằng cách merge các cặp token phổ biến, là một thành phần quan trọng của tokenizer hiện đại.

---

# 25. Bài tập thực hành

## Bài 1 — Character n-gram

Chạy:

```python
char_ngrams("playing")
char_ngrams("played")
```

Sau đó tính Jaccard similarity:

$$
J(A,B)
=
\frac{|A \cap B|}
{|A \cup B|}
$$

Trong đó:

* $A$: tập n-gram của `playing`;
* $B$: tập n-gram của `played`.

Mục tiêu là quan sát mức độ chia sẻ subword giữa các biến thể hình thái.

---

## Bài 2 — BPE compression

Mở rộng `learn_bpe()` để theo dõi:

```text
number of merges
        ↓
vocabulary size
        ↓
average tokens per word
```

Sau đó quan sát:

> Khi số lượng merge tăng, số token cần thiết để biểu diễn corpus thay đổi như thế nào?

Ban đầu compression thường tăng nhanh vì các chuỗi phổ biến được gộp lại.

---

## Bài 3 — BPE trên Shakespeare

Huấn luyện BPE với khoảng:

```text
1,000 merges
```

trên toàn bộ tác phẩm Shakespeare.

So sánh tokenization giữa:

```text
common words
```

và:

```text
rare words / proper nouns
```

Đo:

$$
\text{Average tokens per word}
=
\frac{\text{Total tokens}}
{\text{Total words}}
$$

So sánh trước và sau khi học BPE.

---

# 26. Key Terms

| Thuật ngữ                | Ý nghĩa thực tế                                                                       |
| ------------------------ | ------------------------------------------------------------------------------------- |
| **Co-occurrence matrix** | Ma trận trong đó $X_{ij}$ biểu diễn mức độ từ $j$ xuất hiện trong ngữ cảnh của từ $i$ |
| **GloVe**                | Phương pháp học word embedding từ thống kê đồng xuất hiện                             |
| **Subword**              | Một phần của từ, có thể là character n-gram hoặc learned token                        |
| **FastText**             | Word embedding sử dụng character n-gram                                               |
| **BPE**                  | Thuật toán lặp lại việc merge các cặp token liền kề phổ biến nhất                     |
| **OOV**                  | Từ không tồn tại trong vocabulary                                                     |
| **Byte-level BPE**       | BPE khởi đầu từ 256 byte cơ bản, giúp biểu diễn mọi input byte sequence               |
| **Tokenizer**            | Thành phần chuyển raw text thành chuỗi token / token IDs                              |
| **Vocabulary**           | Tập các token mà tokenizer hoặc model biết                                            |
| **Embedding**            | Vector liên tục biểu diễn token hoặc word                                             |

---

# 27. Điều cần nhớ

> **Word2Vec:** một từ → một vector.

> **GloVe:** một từ → vector được học từ thống kê đồng xuất hiện toàn cục.

> **FastText:** một từ → tổng vector của các character n-gram.

> **BPE:** một văn bản → chuỗi subword token.

Vì vậy, khi học NLP hiện đại, cần chuyển tư duy từ:

```text
word → vector
```

sang:

```text
text
  ↓
tokenization
  ↓
subword tokens
  ↓
token IDs
  ↓
embedding vectors
  ↓
Transformer
```

Đây chính là cầu nối từ các phương pháp **word embedding cổ điển** như Word2Vec/GloVe/FastText sang kiến trúc **Transformer và Large Language Model**.
