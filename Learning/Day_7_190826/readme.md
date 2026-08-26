# Feature Extraction & Feature Learning

Đây là hai khái niệm rất dễ bị trộn lẫn:

* **Feature Extraction**: biến dữ liệu ban đầu thành các đặc trưng có dạng phù hợp hoặc giàu thông tin hơn.
* **Feature Learning**: để mô hình **tự học representation** từ dữ liệu thay vì con người thiết kế đặc trưng.

Điểm quan trọng nhất:

> **Feature Extraction thường xác định representation bằng một quy tắc/thuật toán đã chọn; Feature Learning học representation từ dữ liệu thông qua objective của mô hình.**

Trong tài liệu pipeline của bạn, phần feature engineering cho LSTM/Transformer cũng cố ý giữ raw multivariate signal và chỉ bổ sung temporal context tối thiểu, để sequence model tự học temporal representation. 

---

## 1. Feature là gì?

Giả sử một mẫu dữ liệu:

$$
x_i = [x_{i1},x_{i2},\ldots,x_{id}]
$$

Trong đó mỗi \(x_{ij}\) là một **feature**.

Ví dụ dữ liệu nhà ở:

$$
x=
[
\text{area},
\text{bedrooms},
\text{age},
\text{location}
]
$$

Ta có thể biến đổi thành representation mới:

$$
z=\phi(x)
$$

với

$$
z=[z_1,z_2,\ldots,z_k].
$$

Mục tiêu của \(\phi\) là tạo representation giúp mô hình dễ học hơn.

---

# 2. Feature Extraction

Feature extraction là quá trình:

$$
\boxed{x \rightarrow z=\phi(x)}
$$

trong đó \(\phi\) thường được xác định bởi **quy tắc hoặc thuật toán có sẵn**.

### Ví dụ 1 — PCA

Dữ liệu ban đầu:

$$
X\in\mathbb{R}^{N\times d}
$$

PCA tìm các hướng có phương sai lớn nhất và chiếu dữ liệu:

$$
Z= XW_k
$$

với

$$
W_k\in\mathbb{R}^{d\times k},
\qquad k<d.
$$

Ví dụ:

$$
100\text{ features}
\rightarrow
10\text{ principal components}.
$$

Đây là **feature extraction**, vì representation mới được tạo bằng phép biến đổi PCA.

---

### Ví dụ 2 — Text

Một email:

```text
"Free money now"
```

có thể được chuyển thành:

$$
x=
[
0,1,1,0,\ldots
]
$$

bằng **Bag-of-Words**.

Hoặc:

$$
x_j=
TFIDF(term_j,document)
$$

bằng TF-IDF.

Tài liệu AI-Ex của bạn cũng dùng đúng pipeline này: văn bản → preprocessing → BoW/TF-IDF → vector có thể có hàng nghìn chiều → SVM. 

Đây là extraction/vectorization, **chưa phải deep feature learning**.

---

# 3. Feature Learning

Feature learning đi xa hơn:

$$
\boxed{x \rightarrow f_\theta(x)}
$$

Representation được tạo bởi một mô hình có tham số \(\theta\), và \(\theta\) được học từ dữ liệu.

Ví dụ neural network:

$$
x
\rightarrow
h_1
\rightarrow
h_2
\rightarrow
h_3
\rightarrow
\hat y
$$

Trong đó:

$$
h_1=f_{\theta_1}(x)
$$

$$
h_2=f_{\theta_2}(h_1)
$$

Các \(h_i\) chính là **learned features / representations**.

Mô hình không được nói trước:

> "Feature quan trọng là cạnh, texture, hình dạng..."

Mà tự học những representation hữu ích cho objective.

---

# 4. Khác biệt cốt lõi

|                               | Feature Extraction                            | Feature Learning              |
| ----------------------------- | --------------------------------------------- | ----------------------------- |
| Representation                | Được tạo bằng quy tắc/thuật toán              | Được học từ dữ liệu           |
| Con người thiết kế            | Nhiều hơn                                     | Ít hơn                        |
| Ví dụ                         | PCA, TF-IDF, HOG                              | CNN, Autoencoder, Transformer |
| Có tham số học?               | Có thể có, nhưng không nhất thiết task-driven | Có                            |
| Representation phụ thuộc task | Thường thấp hơn                               | Thường cao                    |
| Deep Learning                 | Có thể dùng                                   | Thành phần cốt lõi            |

Một cách nhìn đơn giản:

$$
\text{Classical ML}
:
x
\xrightarrow{\text{feature engineering}}
z
\xrightarrow{\text{model}}
\hat y
$$

Trong DL:

$$
x
\xrightarrow{\text{feature learning}}
z
\xrightarrow{\text{prediction}}
\hat y
$$

---

# 5. Feature Extraction trong Classical ML

Classical ML thường phụ thuộc nhiều vào chất lượng feature.

Ví dụ bài toán spam:

$$
\text{Email}
\rightarrow
\text{clean text}
\rightarrow
TFIDF
\rightarrow
\mathbf{x}
\rightarrow
SVM
$$

TF-IDF:

$$
TFIDF(t,d)
=
TF(t,d)\times IDF(t)
$$

sau đó:

$$
\mathbf{x}_d
=
[
TFIDF(t_1,d),
\ldots,
TFIDF(t_V,d)
].
$$

SVM học decision boundary:

$$
f(x)=w^Tx+b.
$$

Ở đây:

* TF-IDF tạo representation.
* SVM học classifier.

Đó là pipeline **feature extraction → supervised learning**. Tài liệu của bạn cũng mô tả email sau vectorization có thể trở thành vector hàng nghìn chiều để SVM xử lý. 

---

# 6. Feature Extraction không chỉ là giảm chiều

Một lỗi thường gặp là đồng nhất:

$$
\text{Feature Extraction}
=
\text{Dimensionality Reduction}.
$$

Không đúng.

Feature extraction rộng hơn.

Ví dụ:

### PCA

$$
100D\rightarrow10D
$$

→ extraction + dimensionality reduction.

### TF-IDF

$$
text
\rightarrow
10,000D
$$

→ extraction nhưng **không giảm chiều**, thậm chí tạo representation rất cao chiều.

### Image HOG

$$
image
\rightarrow
gradient/orientation\ features
$$

→ extraction.

Vì vậy:

$$
\boxed{
\text{Dimensionality Reduction}
\subset
\text{Feature Extraction}
}
$$

theo cách phân loại thông dụng.

---

# 7. Feature Learning trong Deep Learning

Deep Learning thay đổi pipeline.

Thay vì:

```text
Raw data
   ↓
Human-designed features
   ↓
ML model
```

ta có:

```text
Raw data
   ↓
Neural network
   ↓
Learned representation
   ↓
Prediction
```

Ví dụ MLP:

$$
h_1=\sigma(W_1x+b_1)
$$

$$
h_2=\sigma(W_2h_1+b_2)
$$

$$
\hat y=W_3h_2+b_3.
$$

Các hidden states:

$$
h_1,h_2
$$

là learned representations.

Gradient từ loss:

$$
\nabla_\theta\mathcal L
$$

được dùng để cập nhật toàn bộ representation.

Do đó feature learning gắn trực tiếp với optimization.

---

# 8. CNN: Feature Learning trên ảnh

CNN là ví dụ điển hình.

Input:

$$
X\in\mathbb{R}^{H\times W\times C}.
$$

Convolution:

$$
Y_{i,j}
=
\sum_{u,v,c}
K_{u,v,c}
X_{i+u,j+v,c}.
$$

Kernel \(K\) **được học**.

Ở các layer đầu:

$$
image
\rightarrow
edges
\rightarrow
textures
\rightarrow
parts
\rightarrow
objects.
$$

Không nên hiểu đây là quy tắc cứng rằng mọi CNN luôn học đúng chuỗi trên; đó là cách trực quan hóa hierarchical representation.

Điểm quan trọng:

$$
K
\leftarrow
\text{gradient descent}.
$$

Do đó convolution filters là **learned features**.

---

# 9. Transformer: Feature Learning trong không gian token

Với text:

$$
tokens
\rightarrow
embeddings
\rightarrow
Transformer
\rightarrow
contextual representations.
$$

Embedding ban đầu:

$$
x_i\rightarrow e_i\in\mathbb R^d.
$$

Self-attention:

$$
Q=XW_Q,\qquad
K=XW_K,\qquad
V=XW_V
$$

và

$$
Attention(Q,K,V)
=
softmax
\left(
\frac{QK^T}{\sqrt{d_k}}
\right)V.
$$

Output representation của token phụ thuộc vào **context**.

Ví dụ cùng một token:

```text
bank
```

có representation khác nhau trong:

```text
river bank
```

và:

```text
bank account
```

Đây là điểm rất quan trọng:

> Classical feature extraction thường tạo feature tương đối cố định; Transformer tạo **contextual representation** phụ thuộc vào toàn bộ input context.

---

# 10. Các mô hình lớn

Với Large Language Models, feature learning xảy ra ở quy mô lớn hơn.

Có thể hình dung:

$$
x
\rightarrow
Embedding
\rightarrow
Transformer\ layers
\rightarrow
Hidden\ states
\rightarrow
LM\ head
$$

Một hidden state:

$$
h_i^{(l)}\in\mathbb R^d
$$

là representation của token \(i\) tại layer \(l\).

Các representation này có thể chứa nhiều loại thông tin khác nhau:

* lexical information
* syntactic information
* semantic information
* contextual information
* task-relevant patterns

Nhưng cần phân biệt:

$$
\boxed{
\text{hidden state}
\neq
\text{feature thủ công}
}
$$

Hidden state là kết quả của quá trình học representation.

---

# 11. Embedding là gì trong hệ thống này?

Embedding là một dạng representation:

$$
f:x\rightarrow\mathbb R^d.
$$

Ví dụ:

```text
"cat"
   ↓
[0.12, -0.37, ..., 0.81]
```

Điểm quan trọng không phải từng số có ý nghĩa độc lập.

Điều quan trọng là **quan hệ hình học giữa các vector**.

Ví dụ:

$$
sim(e_{cat},e_{dog})
>
sim(e_{cat},e_{car})
$$

nếu embedding đã học semantic structure phù hợp.

Embedding xuất hiện ở:

* NLP
* recommendation
* computer vision
* multimodal models
* retrieval
* LLMs

---

# 12. Feature Extraction vs Feature Learning trong một pipeline thực tế

Có thể có cả hai.

Ví dụ:

```text
Raw image
   ↓
Resize / Normalize
   ↓
CNN
   ↓
Learned feature representation
   ↓
Classifier
```

Ở đây:

### Extraction/preprocessing

$$
image
\rightarrow
resize/normalize
$$

### Feature learning

$$
X
\rightarrow
CNN_\theta(X)
$$

### Prediction

$$
z
\rightarrow
classifier(z).
$$

Không nên gọi mọi phép biến đổi dữ liệu là feature learning.

---

# 13. Với Time Series

Đây là phần rất quan trọng.

Giả sử:

$$
X_t\in\mathbb R^F
$$

và ta lấy sequence:

$$
X_{t-L+1:t}
$$

sau đó đưa vào LSTM:

$$
h_t,c_t
=
LSTM_\theta(X_t,h_{t-1},c_{t-1}).
$$

LSTM tự học temporal representation:

$$
X_{t-L+1:t}
\rightarrow
H
\rightarrow
z
\rightarrow
\hat y_{t+H}.
$$

Vì vậy không nhất thiết phải biến dữ liệu thành hàng trăm:

$$
lag_1,lag_2,\ldots,lag_{1000}.
$$

Trong pipeline của bạn, tài liệu `FEATURES-v1` explicitly chọn hướng:

$$
\boxed{
raw\ multivariate\ signal
+
minimal\ temporal\ context
+
sequence\ model\ tự\ học\ temporal\ representation
}
$$

và tránh manual lag explosion, rolling aggregates, PCA và polynomial interactions ở baseline. 

Đây là một quyết định **feature representation**, không đơn thuần là preprocessing.

---

# 14. Vấn đề lớn nhất: Data Leakage

Feature extraction/feature engineering có thể gây leakage.

Ví dụ bạn có:

```text
Train
Validation
Test
```

Không được:

$$
fit\ feature\ transformation
$$

trên toàn bộ dataset nếu transformation sử dụng thông tin từ distribution của validation/test.

Ví dụ StandardScaler:

$$
\mu=\frac1N\sum_i x_i
$$

Nếu tính $\mu$ trên:

$$
Train+Validation+Test
$$

thì test đã tham gia vào quá trình tạo representation.

Đúng hơn:

$$
\mu_{train}
=
\frac1{N_{train}}
\sum_{i\in Train}x_i.
$$

Sau đó:

$$
x'=
\frac{x-\mu_{train}}{\sigma_{train}}.
$$

Trong pipeline của bạn, Phase 6 cũng được thiết kế **trước** train/validation/test split và không fit scaler; scaling thuộc phase sau. 

---

# 15. Feature Explosion

Một vấn đề khác:

$$
d\rightarrow d'
$$

với

$$
d'\gg d.
$$

Ví dụ time series:

```text
temperature
humidity
lights
pressure
...
```

Nếu tạo:

```text
lag 1
lag 2
...
lag 100
```

cho 30 variables:

$$
30\times100=3000
$$

features.

Hậu quả:

* memory tăng
* training chậm
* noise tăng
* multicollinearity
* overfitting
* pipeline phức tạp

Đây chính là lý do tài liệu pipeline của bạn tránh **manual lag explosion** cho LSTM/Transformer. 

---

# 16. Representation không phù hợp với model

Không có feature representation tốt một cách tuyệt đối.

Representation phải phù hợp với:

$$
\boxed{
Data
+
Task
+
Model
}
$$

Ví dụ:

### Tabular + Linear Model

Thường cần feature engineering rõ ràng:

$$
x\rightarrow engineered\ features\rightarrow Linear/Logistic.
$$

### Image + CNN

Không cần tự tạo hàng nghìn edge features:

$$
image\rightarrow CNN.
$$

### Text + SVM

TF-IDF thường là representation hợp lý:

$$
text\rightarrow TFIDF\rightarrow SVM.
$$

### Text + Transformer

Không cần TF-IDF làm input chính:

$$
text\rightarrow tokenizer\rightarrow embeddings\rightarrow Transformer.
$$

---

# 17. Feature Learning cũng có vấn đề

Không phải cứ để neural network tự học feature là tốt.

Các vấn đề chính:

### 1. Data quality

Nếu:

$$
X\rightarrow noisy/incorrect
$$

thì model có thể học representation chứa noise.

---

### 2. Objective mismatch

Model học:

$$
\theta^*
=
\arg\min_\theta\mathcal L_{train}.
$$

Representation được tối ưu để phục vụ objective đó.

Nếu objective không phù hợp downstream task, representation có thể không hữu ích.

---

### 3. Overfitting

Model quá mạnh có thể học:

$$
\text{signal}+\text{noise}.
$$

Khi đó:

$$
L_{train}\downarrow
$$

nhưng:

$$
L_{test}\uparrow.
$$

---

### 4. Distribution shift

Representation học từ:

$$
P_{train}(X)
$$

nhưng deployment lại có:

$$
P_{test}(X)\neq P_{train}(X).
$$

Đây là vấn đề rất quan trọng với production ML.

---

# 18. Một cách phân loại rất hữu ích

Khi gặp một kỹ thuật mới, hãy hỏi nó thuộc tầng nào:

```text
Raw Data
   │
   ├── Cleaning
   │
   ├── Transformation
   │
   ├── Feature Extraction
   │
   ├── Feature Learning
   │
   └── Prediction
```

Ví dụ:

| Kỹ thuật                 | Vai trò                 |
| ------------------------ | ----------------------- |
| Missing-value imputation | Data preprocessing      |
| StandardScaler           | Transformation          |
| PCA                      | Feature extraction      |
| TF-IDF                   | Feature extraction      |
| HOG                      | Feature extraction      |
| CNN filters              | Feature learning        |
| LSTM hidden state        | Feature learning        |
| Transformer hidden state | Feature learning        |
| Word embedding học được  | Feature learning        |
| Hand-crafted lag         | Feature engineering     |
| Learned embedding        | Representation learning |

---

# 19. Mental model quan trọng nhất

Bạn có thể nhớ theo 3 câu:

### Classical ML

$$
\boxed{
Human\ designs\ representation
\rightarrow
Model\ learns\ decision\ function
}
$$

### Deep Learning

$$
\boxed{
Model\ learns\ representation
+
decision\ function
}
$$

### Large Models

$$
\boxed{
Pretraining
\rightarrow
general\ representation
\rightarrow
downstream\ adaptation
}
$$

Do đó, lịch sử phát triển có thể nhìn như:

```text
Hand-crafted Features
        ↓
Feature Extraction
        ↓
Representation Learning
        ↓
Deep Representation Learning
        ↓
Large-scale Pretrained Representations
```

**Điểm cốt lõi:** Feature Engineering/Extraction quyết định **ta đưa thông tin vào không gian nào**; Feature Learning quyết định **mô hình tự xây dựng không gian biểu diễn nào từ dữ liệu**. Với ML cổ điển, phần đầu thường do con người đảm nhiệm nhiều hơn; với DL và mô hình lớn, phần này được chuyển mạnh sang quá trình học của mô hình.
