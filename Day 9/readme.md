# Bag of Words, TF-IDF, And Text Representation.

## 1. Text Representation

__Text Representation__ là quá trình chuyển đổi dữ liệu văn bản thành các vector số để mô hình học máy có thể xử lý. Do tài liệu văn bản có độ dài thay đổi, cần ánh xạ mỗi tài liệu thành một vector có kích thước cố định. Hai phương pháp biểu diễn truyền thống và phổ biến nhất là __Bag of Words (BoW) và TF-IDF__. Chúng đặc biệt hiệu quả trong các bài toán phân loại văn bản, lọc thư rác, phân tích cảm xúc và phân loại chủ đề.

### Bảng 5W1H

| Tiêu chí  | Nội dung                                                                                                                                                                                                          |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **What**  | **Text Representation** là quá trình chuyển đổi văn bản thành vector số để mô hình Machine Learning hoặc Deep Learning có thể xử lý. Đây là bước tiền xử lý quan trọng trong mọi hệ thống NLP.                    |
| **Why**   | Máy tính không thể học trực tiếp từ chuỗi ký tự. Văn bản phải được biểu diễn dưới dạng số để thực hiện các phép toán, tính khoảng cách và huấn luyện mô hình.                                                     |
| **Where** | Được sử dụng trong hầu hết các bài toán NLP như phân loại văn bản, phân tích cảm xúc, phát hiện spam, tìm kiếm thông tin, chatbot và hệ thống gợi ý.                                                              |
| **When**  | Thực hiện sau các bước tiền xử lý văn bản (Tokenization, Lowercase, Stopword Removal, Stemming/Lemmatization) và trước khi đưa dữ liệu vào mô hình học máy.                                                       |
| **Which** | Các phương pháp phổ biến gồm: **One-Hot Encoding**, **Bag of Words (BoW)**, **TF-IDF**, **Word2Vec**, **GloVe**, **FastText**, **BERT Embedding** và các mô hình embedding hiện đại.                              |
| **How**   | Xây dựng một phương pháp ánh xạ từ văn bản sang vector số. Với BoW và TF-IDF, mỗi chiều của vector tương ứng với một từ trong Vocabulary; với Embedding, mỗi chiều biểu diễn đặc trưng ngữ nghĩa của từ hoặc câu. |


## 2. Bag of Words (BoW)

__Bag of Words (BoW)__ là phương pháp biểu diễn văn bản bằng cách __đếm số lần xuất hiện của từng từ trong một tài liệu__, đồng thời __bỏ qua thứ tự xuất hiện của các từ__. Trước tiên, toàn bộ tập dữ liệu được xây dựng thành một __từ điển (Vocabulary)__ gồm các từ duy nhất. Mỗi tài liệu sau đó được biểu diễn thành một vector có độ dài bằng kích thước của Vocabulary, trong đó mỗi phần tử là số lần xuất hiện của từ tương ứng.

| Vocabulary    |  I | love | AI | learning |
| ------------- | -: | ---: | -: | -------: |
| "I love AI"   |  1 |    1 |  1 |        0 |
| "AI learning" |  0 |    0 |  1 |        1 |

Ưu điểm
- Đơn giản, dễ triển khai.
- Vector có ý nghĩa trực quan và dễ giải thích.
- Hiệu quả với các bài toán phân loại văn bản cơ bản.

Hạn chế
- Không xét ngữ cảnh và thứ tự từ.
- Vocabulary lớn tạo vector thưa (Sparse Vector).
- Các từ phổ biến có thể chi phối kết quả.

### bảng 5W1H

| Tiêu chí  | Nội dung                                                                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **What**  | **Bag of Words (BoW)** là phương pháp biểu diễn văn bản bằng cách đếm số lần xuất hiện của từng từ trong tài liệu, đồng thời bỏ qua thứ tự xuất hiện của các từ.                                  |
| **Why**   | Giả định rằng sự xuất hiện của từ quan trọng hơn vị trí của chúng. Phương pháp này đơn giản, dễ triển khai và hiệu quả cho nhiều bài toán phân loại văn bản.                                      |
| **Where** | Được sử dụng trong Spam Detection, Sentiment Analysis, Topic Classification, Document Classification và các mô hình Machine Learning truyền thống như Naive Bayes, Logistic Regression và SVM.    |
| **When**  | Phù hợp khi bài toán chỉ cần biết **từ nào xuất hiện** và **xuất hiện bao nhiêu lần**, không yêu cầu hiểu ngữ nghĩa hoặc ngữ cảnh của câu.                                                        |
| **Which** | Vector BoW có kích thước bằng số lượng từ trong Vocabulary. Mỗi phần tử của vector là số lần xuất hiện của từ tương ứng trong tài liệu.                                                           |
| **How**   | (1) Xây dựng Vocabulary từ toàn bộ tập dữ liệu. (2) Gán chỉ số cho từng từ. (3) Đếm số lần xuất hiện của mỗi từ trong từng tài liệu. (4) Tạo vector đếm (Count Vector) có độ dài bằng Vocabulary. |


## 3. TF-IDF (Term Frequency – Inverse Document Frequency)

__TF-IDF__ là phương pháp cải tiến từ BoW bằng cách __giảm trọng số của các từ xuất hiện ở hầu hết các tài liệu và tăng trọng số của các từ đặc trưng cho từng tài liệu__. Ý tưởng là các từ xuất hiện nhiều trong toàn bộ tập dữ liệu thường mang ít giá trị phân biệt.

TF-IDF được tính theo công thức:

$$\text{TF-IDF}(w,d) = TF(w, d) \times IDF(w)$$

Trong đó:

$$TF(w, d) = \frac {\text{Số lần xuất hiện của w trong d}} {|d|}$$

$$IDF(w) = \log (\frac {N}{d f(w)})$$

Với: 
- $N$: tổng số tài liệu.
- $df(w)$: số tài liệu chứa từ w.

__Đặc điểm:__
- Từ xuất hiện nhiều trong một tài liệu nhưng hiếm trong toàn bộ tập dữ liệu sẽ có trọng số cao.
- Từ xuất hiện trong hầu hết các tài liệu sẽ có trọng số thấp.

__Ưu điểm:__
- Giảm ảnh hưởng của các từ phổ biến.
- Tăng khả năng phân biệt giữa các tài liệu.
- Thường cho kết quả tốt hơn BoW trong các bài toán phân loại văn bản.

__Hạn chế:__
- Vẫn không biểu diễn được ngữ nghĩa và thứ tự từ.
- Không nhận biết được các từ đồng nghĩa hoặc phụ thuộc ngữ cảnh.

### Bảng 5W1H

| Tiêu chí  | Nội dung                                                                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **What**  | **TF-IDF** là phương pháp cải tiến từ BoW bằng cách gán trọng số cho mỗi từ dựa trên mức độ quan trọng của từ trong một tài liệu và trong toàn bộ tập dữ liệu.                                    |
| **Why**   | Các từ xuất hiện ở hầu hết tài liệu (ví dụ: "the", "is", "và") mang ít thông tin phân biệt. TF-IDF giảm trọng số của các từ này và tăng trọng số cho các từ đặc trưng của từng tài liệu.          |
| **Where** | Được sử dụng rộng rãi trong Information Retrieval, Search Engine, Document Ranking, Topic Classification, Sentiment Analysis và nhiều hệ thống NLP truyền thống.                                  |
| **When**  | Sử dụng khi cần cải thiện chất lượng biểu diễn BoW, đặc biệt đối với các tập dữ liệu có nhiều từ phổ biến hoặc nhiều tài liệu.                                                                    |
| **Which** | TF-IDF được tính từ hai thành phần: **Term Frequency (TF)** và **Inverse Document Frequency (IDF)**. Vector thu được vẫn là vector thưa (Sparse Vector) nhưng mang nhiều thông tin hơn BoW.       |
| **How**   | Bước 1: Tính **TF** của mỗi từ trong tài liệu. Bước 2: Tính **IDF** dựa trên số lượng tài liệu chứa từ đó. Bước 3: Nhân TF với IDF để thu được trọng số cuối cùng của mỗi từ trong vector TF-IDF. |


## 4. So sánh BoW và TF-IDF

| Tiêu chí                         | Bag of Words                      | TF-IDF                                                          |
| -------------------------------- | --------------------------------- | --------------------------------------------------------------- |
| Giá trị vector                   | Số lần xuất hiện của từ           | Trọng số TF × IDF                                               |
| Xét tần suất toàn bộ tập dữ liệu | Không                             | Có                                                              |
| Giảm ảnh hưởng từ phổ biến       | Không                             | Có                                                              |
| Vector                           | Sparse                            | Sparse                                                          |
| Khả năng diễn giải               | Cao                               | Cao                                                             |
| Ứng dụng                         | Phân loại văn bản, Spam Detection | Sentiment Analysis, Topic Classification, Information Retrieval |

> BoW và TF-IDF là hai kỹ thuật Text Representation truyền thống nhưng vẫn được sử dụng rộng rãi trong các hệ thống NLP nhờ tính đơn giản, tốc độ xử lý nhanh và khả năng giải thích cao. Đối với các bài toán mà sự xuất hiện của từ quan trọng hơn ngữ cảnh, TF-IDF thường đạt hiệu quả tương đương các mô hình embedding hiện đại trong khi có chi phí tính toán thấp hơn. Tuy nhiên, khi cần biểu diễn ngữ nghĩa, ngữ cảnh hoặc quan hệ giữa các từ, các phương pháp embedding như Word2Vec, FastText, GloVe hoặc BERT sẽ phù hợp hơn.

## Build it

### Step 1. Xây dựng Vocabulary

```python
def build_vocab(docs):
    vocab = {}

    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)

    return vocab
```

**Mục đích**

Xây dựng **Vocabulary** (từ điển từ vựng) từ toàn bộ tập dữ liệu. Mỗi từ duy nhất được gán một **chỉ số (index)** để làm vị trí trong vector Bag of Words hoặc TF-IDF.

**Input**

- `docs`: Danh sách các tài liệu đã được **tokenize**.
- Mỗi tài liệu là một danh sách các từ.

**Giải thích**

- Duyệt lần lượt từng tài liệu (`doc`).
- Duyệt từng từ (`token`) trong tài liệu.
- Nếu từ chưa tồn tại trong `vocab`, thêm từ vào dictionary.
- Chỉ số của từ được gán bằng `len(vocab)`, tức là số lượng từ đã có trước đó.

> **Lưu ý:** Trong ví dụ này, chỉ số được gán theo **thứ tự xuất hiện đầu tiên** của từ trong tập dữ liệu (stable insertion order). Trong khi đó, **scikit-learn** mặc định sắp xếp Vocabulary theo **thứ tự bảng chữ cái** trước khi gán chỉ số.

### Step 2. Xây dựng Bag of Words

```python
def bag_of_words(docs, vocab):
    matrix = [[0] * len(vocab) for _ in docs]

    for i, doc in enumerate(docs):
        for token in doc:
            if token in vocab:
                matrix[i][vocab[token]] += 1

    return matrix
```

**Mục đích**

Chuyển các tài liệu đã tokenize thành **ma trận Bag of Words**, trong đó mỗi tài liệu được biểu diễn bằng một vector đếm số lần xuất hiện của từng từ trong Vocabulary.

**Input**

- `docs`: Danh sách các tài liệu đã tokenize.
- `vocab`: Dictionary `{word: index}` được tạo ở bước trước.

Ví dụ:

```python
docs = [
    ["cat", "sat", "on", "mat"],
    ["cat", "cat", "ran"]
]
```

**Output**

```python
[
    [1, 1, 1, 1, 0],
    [2, 0, 0, 0, 1]
]
```

**Giải thích**

- Mỗi **hàng (row)** biểu diễn một tài liệu.
- Mỗi **cột (column)** tương ứng với một từ trong Vocabulary.
- Giá trị tại vị trí **(i, j)** là số lần từ thứ `j` xuất hiện trong tài liệu thứ `i`.

Trong ví dụ trên:
- Tài liệu 1 chứa từ **"cat"** hai lần nên giá trị bằng **2**.
- Tài liệu 0 không chứa từ **"ran"** nên giá trị bằng **0**.

> **Lưu ý:** Ma trận Bag of Words chỉ lưu **tần suất xuất hiện của từ**, không biểu diễn thứ tự hay ngữ nghĩa của các từ trong câu.

### Bước 3. Tính TF và IDF

```python
import math

def term_frequency(doc_bow, doc_length):
    return [c / doc_length if doc_length else 0 for c in doc_bow]

def document_frequency(bow_matrix):
    df = [0] * len(bow_matrix[0])

    for row in bow_matrix:
        for j, count in enumerate(row):
            if count > 0:
                df[j] += 1
    return df

def inverse_document_frequency(df, n_docs):
    return [math.log((n_docs + 1) / (d + 1)) + 1 for d in df]
```

### Mục đích

Tính **TF (Term Frequency)** và **IDF (Inverse Document Frequency)** để xác định mức độ quan trọng của mỗi từ trước khi tạo vector **TF-IDF**.

### Thành phần

#### 1. Term Frequency (TF)

Đo tần suất xuất hiện của một từ trong một tài liệu.

$$TF(w,d)=\frac{\text{count}(w,d)}{|d|}$$

- `doc_bow`: Vector Bag of Words của một tài liệu.
- `doc_length`: Tổng số từ trong tài liệu.

Kết quả là một vector TF có giá trị trong khoảng **0 → 1**.

---

#### 2. Document Frequency (DF)

Đếm số lượng tài liệu chứa mỗi từ trong Vocabulary.

Ví dụ:

```text
Word "cat" xuất hiện trong 2 tài liệu → DF(cat) = 2
```

DF càng lớn, từ đó càng phổ biến trong toàn bộ tập dữ liệu.

---

#### 3. Inverse Document Frequency (IDF)

Giảm trọng số của các từ xuất hiện trong nhiều tài liệu.

$$IDF(w)=\log\left(\frac{N+1}{DF(w)+1}\right)+1$$

Trong đó:

- $N$: Tổng số tài liệu.
- $DF(w)$: Số tài liệu chứa từ $w$.

### Giải thích

Công thức sử dụng **smoothing**:

- `N + 1` và `DF + 1` tránh trường hợp chia cho 0 khi một từ chưa xuất hiện.
- `+1` sau phép log giúp những từ xuất hiện trong tất cả tài liệu vẫn có **IDF = 1** thay vì **0**, tương tự cách cài đặt mặc định của **scikit-learn**.

> Sau khi tính TF và IDF, trọng số cuối cùng của mỗi từ được tính bằng:
>
> $$TF\text{-}IDF = TF \times IDF$$
>
> Đây là vector đầu vào phổ biến cho các mô hình Machine Learning như Logistic Regression, Naive Bayes và SVM.

## Khi nào nên sử dụng TF-IDF?

TF-IDF vẫn là lựa chọn hiệu quả trong nhiều bài toán NLP truyền thống, đặc biệt khi **sự xuất hiện của từ quan trọng hơn ý nghĩa ngữ cảnh**.

### Trường hợp phù hợp

- **Spam Detection:** Phân loại email hoặc tin nhắn rác dựa trên các từ khóa đặc trưng.
- **Topic Classification:** Phân loại tài liệu theo chủ đề khi mỗi chủ đề có tập từ khóa riêng.
- **Log Anomaly Detection:** Phát hiện bất thường trong log hệ thống thông qua các từ hoặc mẫu xuất hiện bất thường.
- **Tập dữ liệu nhỏ:** Với vài trăm mẫu huấn luyện, TF-IDF kết hợp Logistic Regression hoặc SVM thường đạt hiệu quả tốt mà không cần mô hình tiền huấn luyện.
- **Yêu cầu độ trễ thấp:** TF-IDF kết hợp mô hình tuyến tính có thời gian suy luận rất nhanh (microseconds), nhanh hơn đáng kể so với Transformer Embedding (khoảng 10–100 ms).
- **Yêu cầu khả năng giải thích:** Có thể trực tiếp xem trọng số của từng từ trong mô hình để biết từ nào ảnh hưởng nhiều nhất đến quyết định phân loại.

---

## Hạn chế của TF-IDF

### 1. Không hiểu ngữ nghĩa (Semantic Blindness)

TF-IDF chỉ dựa trên tần suất xuất hiện của từ nên không hiểu ngữ cảnh hoặc quan hệ giữa các từ.

Ví dụ:

```text
"The movie was not good at all."
"The movie was excellent."
```

Hai câu đều chứa các từ như **"the"**, **"movie"**, **"was"**, nhưng mang ý nghĩa trái ngược (tiêu cực và tích cực). TF-IDF không nhận biết được rằng từ **"not"** đã đảo ngược ý nghĩa của **"good"**, do đó cần rất nhiều dữ liệu để mô hình học được quy luật này.

---

### 2. Không xử lý được từ ngoài Vocabulary (Out-of-Vocabulary)

TF-IDF chỉ biểu diễn những từ đã xuất hiện trong quá trình huấn luyện.

Ví dụ:

- Mô hình được huấn luyện trên tập đánh giá phim IMDb.
- Khi gặp một từ mới chưa từng xuất hiện (ví dụ: **"Zoomer-approved"**), TF-IDF sẽ không có đặc trưng tương ứng và không thể biểu diễn từ đó.

Trong khi đó, các phương pháp **Subword Embedding** hoặc **Transformer Embedding** có thể phân tách từ mới thành các đơn vị nhỏ hơn để tiếp tục biểu diễn ngữ nghĩa.

---

### Tổng kết

| Nên dùng TF-IDF khi | Không nên dùng TF-IDF khi |
|---------------------|---------------------------|
| Phân loại văn bản bằng từ khóa | Cần hiểu ngữ nghĩa và ngữ cảnh |
| Tập dữ liệu nhỏ | Văn bản chứa nhiều cách diễn đạt khác nhau |
| Yêu cầu suy luận nhanh | Xuất hiện nhiều từ mới (Out-of-Vocabulary) |
| Cần mô hình dễ giải thích | Cần biểu diễn ngữ nghĩa sâu bằng Embedding hoặc Transformer |

## Hybrid: TF-IDF Weighted Embeddings

Trong các bài toán **Text Classification** với lượng dữ liệu gán nhãn ở mức trung bình, một phương pháp hiệu quả là **kết hợp TF-IDF và Word Embedding**. Ý tưởng là sử dụng **trọng số TF-IDF** để nhấn mạnh các từ quan trọng trước khi tổng hợp các vector embedding của tài liệu.

### Cài đặt

```python
def tfidf_weighted_embedding(doc, tfidf_scores, embedding_table, dim):
    vec = [0.0] * dim
    total_weight = 0.0

    for token in doc:
        if token not in embedding_table or token not in tfidf_scores:
            continue

        weight = tfidf_scores[token]
        emb = embedding_table[token]

        for i in range(dim):
            vec[i] += weight * emb[i]
        total_weight += weight

    if total_weight == 0:
        return vec

    return [v / total_weight for v in vec]
```

### Mục đích

Biểu diễn toàn bộ tài liệu bằng **một vector embedding duy nhất**, trong đó các từ quan trọng (TF-IDF cao) đóng góp nhiều hơn vào vector cuối cùng.

### Input

- `doc`: Danh sách các từ trong tài liệu.
- `tfidf_scores`: Trọng số TF-IDF của từng từ.
- `embedding_table`: Bảng Word Embedding (`word → vector`).
- `dim`: Kích thước của vector embedding.

### Output

Một vector có kích thước `dim`, đại diện cho toàn bộ tài liệu.

### Giải thích

- Duyệt từng từ trong tài liệu.
- Lấy **trọng số TF-IDF** của từ.
- Nhân trọng số với **vector embedding** của từ.
- Cộng dồn các vector theo trọng số.
- Chuẩn hóa bằng tổng trọng số để thu được vector biểu diễn cuối cùng.

Biểu diễn tổng quát:

$$Document=\frac{\sum_{i=1}^{n}TF\text{-}IDF(w_i)\times Embedding(w_i)}{\sum_{i=1}^{n}TF\text{-}IDF(w_i)}$$

---

## Ưu điểm

- Kết hợp được **ý nghĩa ngữ nghĩa** của Word Embedding.
- Giữ được khả năng **nhấn mạnh các từ quan trọng** nhờ TF-IDF.
- Phù hợp cho các bài toán **Sentiment Analysis**, **Topic Classification** và **Intent Classification** với tập dữ liệu dưới khoảng **50.000** mẫu gán nhãn.

## Hạn chế

- Vẫn phụ thuộc vào chất lượng Word Embedding.
- Không mô hình hóa quan hệ ngữ cảnh giữa các từ như Transformer (BERT, RoBERTa,...).
- Hiệu quả giảm khi dữ liệu rất lớn hoặc yêu cầu hiểu ngữ cảnh phức tạp.

## Key Terms

| Thuật ngữ | Cách gọi phổ biến | Ý nghĩa thực tế |
|-----------|-------------------|-----------------|
| **Bag of Words (BoW)** | Word Frequency Vector | Biểu diễn tài liệu bằng **vector số lần xuất hiện của từng từ** trong Vocabulary, bỏ qua thứ tự từ. |
| **Term Frequency (TF)** | Term Frequency | Tần suất xuất hiện của một từ trong một tài liệu, có thể được chuẩn hóa theo độ dài tài liệu. |
| **Document Frequency (DF)** | Document Frequency | Số lượng tài liệu trong tập dữ liệu chứa từ đó ít nhất một lần. |
| **Inverse Document Frequency (IDF)** | Inverse Document Frequency | Trọng số phản ánh mức độ đặc trưng của từ, thường tính bằng công thức `log(N / DF)` (hoặc phiên bản có smoothing). Các từ xuất hiện trong nhiều tài liệu sẽ có IDF thấp. |
| **Sparse Vector** | Mostly Zeros | Vector có kích thước lớn nhưng phần lớn các phần tử bằng **0**, do mỗi tài liệu chỉ chứa một số ít từ trong toàn bộ Vocabulary. |
| **Cosine Similarity** | Vector Angle | Độ đo mức độ tương đồng giữa hai vector bằng **góc giữa chúng**. Sau khi chuẩn hóa L2, giá trị nằm trong khoảng **0–1**: **1** là giống hệt, **0** là không tương đồng (vuông góc). |