# 05. Dimensionality Reduction

## 1. Khái niệm

**Dimensionality Reduction** là nhóm phương pháp biến đổi dữ liệu từ không gian đặc trưng có số chiều cao sang một không gian có số chiều thấp hơn, đồng thời cố gắng giữ lại những thông tin quan trọng đối với mục tiêu phân tích hoặc học máy.

Với dữ liệu ban đầu:

$$X\in\mathbb{R}^{n\times p}$$

trong đó:

* $n$: số quan sát;
* $p$: số features ban đầu.

Dimensionality Reduction xây dựng một representation mới:

$$Z=f(X),\quad Z\in\mathbb{R}^{n\times k}$$

với:

$$k<p$$

Khác với Feature Selection, phương pháp này **không nhất thiết giữ lại các feature gốc**. Các biến mới trong $Z$ thường được tạo ra từ sự kết hợp của nhiều feature ban đầu.

```text
Original Feature Space
X1 ─┐
X2 ─┤
X3 ─┤
X4 ─┤──► Dimensionality Reduction ──► Z1
X5 ─┤                                  Z2
X6 ─┤                                  Z3
... ┘                                  ...
        p dimensions                  k dimensions
                                      k < p
```

Do đó:

$$\text{Feature Selection}\neq\text{Dimensionality Reduction}$$

Feature Selection tìm:

$$X^*\subseteq X$$

trong khi Dimensionality Reduction xây dựng:

$$Z=f(X)$$

---

# 2. Vị trí trong Chương 6

Mục này là bước cuối của Chương 6 và kế thừa trực tiếp từ ba nhóm Feature Selection trước đó:

```text
01 Feature Selection
        │
        ▼
02 Filter Methods
        │
        ▼
03 Wrapper Methods
        │
        ▼
04 Embedded Methods
        │
        ▼
05 Dimensionality Reduction
        │
        ▼
Reduced Representation
```

Ba phương pháp trước chủ yếu trả lời câu hỏi:

> **Feature nào nên được giữ lại?**

Dimensionality Reduction chuyển sang câu hỏi:

> **Có thể biểu diễn toàn bộ thông tin bằng một không gian ít chiều hơn hay không?**

Đây là sự khác biệt quan trọng khi dataset có nhiều feature tương quan hoặc khi việc giữ nguyên feature gốc làm tăng dimensionality và complexity của mô hình.

---

# 3. Feature Selection và Dimensionality Reduction

Hai nhóm phương pháp có thể được phân biệt như sau:

| Đặc điểm          | Feature Selection  | Dimensionality Reduction |
| ----------------- | ------------------ | ------------------------ |
| Kết quả           | Subset feature gốc | Feature mới              |
| Biểu diễn         | $X^*\subseteq X$   | $Z=f(X)$                 |
| Số feature        | Giảm               | Giảm                     |
| Giữ semantic gốc  | Có                 | Có thể mất               |
| Interpretability  | Cao hơn            | Thấp hơn                 |
| Xử lý correlation | Hạn chế            | Tốt                      |
| Ví dụ             | LASSO, RFE         | PCA, SVD, Autoencoder    |

Ví dụ:

$$X={X_1,X_2,X_3,X_4}$$

Feature Selection có thể tạo:

$$X^*={X_1,X_3}$$

Trong khi PCA có thể tạo:

$$Z_1=w_1X_1+w_2X_2+w_3X_3+w_4X_4$$

$$Z_2=v_1X_1+v_2X_2+v_3X_3+v_4X_4$$

Do đó $Z_1,Z_2$ không phải là feature gốc.

---

# 4. Các hướng tiếp cận chính

Dimensionality Reduction có thể được chia thành hai nhóm lớn:

```text
Dimensionality Reduction
        │
        ├── Linear Methods
        │      ├── PCA
        │      └── SVD
        │
        └── Nonlinear Methods
               ├── Kernel PCA
               ├── Autoencoder
               ├── t-SNE
               └── UMAP
```

Các phương pháp này có mục tiêu khác nhau.

* **PCA/SVD:** tìm representation tuyến tính có khả năng giữ variance hoặc cấu trúc năng lượng lớn.
* **Kernel PCA:** mở rộng PCA cho cấu trúc phi tuyến.
* **Autoencoder:** học nonlinear representation thông qua neural network.
* **t-SNE/UMAP:** chủ yếu phục vụ visualization và khám phá cấu trúc dữ liệu.

Do đó không nên sử dụng mọi dimensionality reduction method như những phương pháp tương đương.

---

# 5. Principal Component Analysis

**Principal Component Analysis (PCA)** là phương pháp Dimensionality Reduction tuyến tính phổ biến nhất.

Giả sử dữ liệu sau preprocessing là:

$$X\in\mathbb{R}^{n\times p}$$

Sau khi center:

$$X_c=X-\mu$$

PCA tìm các hướng $w_i$ sao cho variance của projection là lớn nhất.

Với component đầu tiên:

$$w_1=\arg\max_{|w|_2=1}Var(X_cw)$$

Tương đương:

$$w_1=\arg\max_{|w|_2=1}w^T\Sigma w$$

trong đó:

$$\Sigma=\frac{1}{n-1}X_c^TX_c$$

là covariance matrix.

Nghiệm là eigenvector tương ứng với eigenvalue lớn nhất của $\Sigma$:

$$\Sigma w_i=\lambda_iw_i$$

---

# 6. Principal Components

Các eigenvectors:

$$w_1,w_2,\ldots,w_p$$

tạo thành các principal directions.

Dữ liệu được project sang không gian mới:

$$Z=X_cW_k$$

với:

$$W_k=[w_1,w_2,\ldots,w_k]$$

và:

$$k<p$$

Khi đó:

$$Z\in\mathbb{R}^{n\times k}$$

Các component được sắp xếp theo:

$$\lambda_1\geq\lambda_2\geq\cdots\geq\lambda_p$$

Trong PCA, $\lambda_i$ biểu diễn lượng variance được giải thích bởi component thứ $i$.

---

# 7. Explained Variance

Một tiêu chí quan trọng để chọn số lượng components là **explained variance ratio**.

Với component $i$:

$$EVR_i=\frac{\lambda_i}{\sum_{j=1}^{p}\lambda_j}$$

Cumulative explained variance:

$$CEV_k=\frac{\sum_{i=1}^{k}\lambda_i}{\sum_{j=1}^{p}\lambda_j}$$

Có thể chọn $k$ sao cho:

$$CEV_k\geq\tau$$

với $\tau$ là ngưỡng định trước, ví dụ một mức coverage variance phù hợp với mục tiêu nghiên cứu.

```text
Explained Variance
│
│ ●────────────
│   ●
│     ●
│       ●
│         ●
│           ●
└──────────────────► Number of Components
       k
```

Tuy nhiên, explained variance không trực tiếp đảm bảo prediction performance.

Một component giải thích nhiều variance chưa chắc chứa nhiều information nhất đối với target.

---

# 8. PCA và Prediction

PCA là phương pháp **unsupervised**.

Nó tìm:

$$Z=f(X)$$

mà không sử dụng target $Y$ trong objective.

Do đó:

$$\text{High Variance}\not\Rightarrow\text{High Predictive Relevance}$$

Ví dụ, một feature có variance rất lớn nhưng gần như không liên quan đến target vẫn có thể đóng góp mạnh vào principal component.

Vì vậy nếu PCA được sử dụng trước một mô hình supervised, cần đánh giá:

$$M(X)\quad\text{vs.}\quad M(Z)$$

trên validation data.

---

# 9. Singular Value Decomposition

PCA có thể được triển khai thông qua **Singular Value Decomposition (SVD)**.

Với centered matrix:

$$X_c=U\Sigma V^T$$

trong đó:

* $U$: left singular vectors;
* $\Sigma$: singular values;
* $V$: right singular vectors.

Chọn $k$ singular vectors đầu tiên:

$$X_k=U_k\Sigma_kV_k^T$$

Khi đó:

$$Z=U_k\Sigma_k$$

là reduced representation.

SVD đặc biệt hữu ích khi dữ liệu có số chiều lớn và có thể được sử dụng để thực hiện PCA mà không cần tính covariance matrix một cách trực tiếp.

---

# 10. Reconstruction Error

Một tiêu chí khác để đánh giá dimensionality reduction là reconstruction error.

Từ representation $Z$, có thể tái tạo xấp xỉ:

$$\hat{X}=ZW_k^T+\mu$$

Reconstruction error:

$$E=|X-\hat{X}|_F^2$$

PCA với $k$ components tìm một không gian tuyến tính có khả năng tối thiểu hóa reconstruction error trong lớp các linear subspaces có dimension $k$.

Do đó:

$$k\uparrow\Rightarrow E\downarrow$$

nhưng đồng thời:

$$k\uparrow\Rightarrow\text{Dimensionality Reduction}\downarrow$$

Đây chính là trade-off giữa:

$$\text{Information Preservation}\leftrightarrow\text{Compression}$$

---

# 11. Standardization trước PCA

PCA rất nhạy với scale của features.

Ví dụ:

$$X_1\sim[0,1]$$

trong khi:

$$X_2\sim[0,100000]$$

Nếu tính covariance trực tiếp, $X_2$ có thể chi phối principal components chỉ vì scale lớn hơn.

Do đó trong nhiều trường hợp cần chuẩn hóa:

$$X'_j=\frac{X_j-\mu_j}{\sigma_j}$$

trước khi PCA.

Điều này liên kết trực tiếp với:

`04_data_transformation/01_scaling_normalization.md`

và phải tuân thủ cùng nguyên tắc **fit preprocessing trên training data**.

---

# 12. Dimensionality Reduction và Data Leakage

Đây là nguyên tắc quan trọng đối với toàn bộ pipeline.

Quy trình sai:

```text
All Data
   │
   ▼
Fit PCA
   │
   ▼
Transform All Data
   │
   ▼
Train / Validation / Test Split
```

PCA đã sử dụng mean và covariance của validation/test data.

Quy trình đúng:

```text
Chronological Split
        │
        ├── Train
        │     │
        │     ▼
        │   Fit PCA
        │     │
        │     ▼
        │   Transform Train
        │
        ├── Validation
        │     │
        │     ▼
        │   Transform using Train PCA
        │
        └── Test
              │
              ▼
        Transform using Train PCA
```

Với PCA:

$$\mu_{train},W_{train}$$

được học từ training data.

Sau đó:

$$Z_{train}=(X_{train}-\mu_{train})W_{train}$$

$$Z_{val}=(X_{val}-\mu_{train})W_{train}$$

$$Z_{test}=(X_{test}-\mu_{train})W_{train}$$

Không được tính PCA riêng trên validation hoặc test nếu mục tiêu là đánh giá một pipeline đã được fit từ training data.

---

# 13. Dimensionality Reduction cho Time Series

Trong time series, dimensionality reduction phải bảo toàn temporal structure.

Giả sử:

$$X_t\in\mathbb{R}^{p}$$

PCA có thể được áp dụng để tạo:

$$Z_t=W_k^TX_t$$

với:

$$Z_t\in\mathbb{R}^{k},\quad k<p$$

Tuy nhiên, PCA cơ bản không mô hình hóa trực tiếp temporal dependency:

$$X_t\rightarrow X_{t+1}$$

Nó chủ yếu tìm covariance structure giữa các dimensions.

Do đó PCA có thể hữu ích để giảm số lượng sensor hoặc biến tương quan, nhưng không tự động giải quyết:

* temporal dependency;
* lag structure;
* seasonality;
* trend;
* stationarity.

Các vấn đề này đã được xử lý ở các chương trước, đặc biệt trong:

* `04_data_transformation/03_stationarity.md`;
* `04_data_transformation/04_decomposition.md`;
* `05_feature_engineering/02_lag_features.md`;
* `05_feature_engineering/03_rolling_features.md`.

---

# 14. Kernel PCA

PCA chỉ tìm được cấu trúc tuyến tính.

Nếu dữ liệu nằm trên một manifold phi tuyến, có thể sử dụng **Kernel PCA**.

Thay vì thực hiện PCA trực tiếp trên $X$, Kernel PCA sử dụng kernel:

$$K_{ij}=k(x_i,x_j)$$

Ví dụ Gaussian/RBF kernel:

$$K(x_i,x_j)=\exp\left(-\frac{|x_i-x_j|^2}{2\sigma^2}\right)$$

Sau đó thực hiện eigendecomposition trên kernel matrix.

Kernel PCA cho phép mô hình hóa các cấu trúc phi tuyến mà PCA tuyến tính không thể biểu diễn trực tiếp.

Tuy nhiên, chi phí tính toán và độ phức tạp tăng lên khi số lượng observations lớn.

---

# 15. Autoencoder

**Autoencoder** là một neural network học representation có số chiều thấp thông qua hai thành phần:

```text
Input X
   │
   ▼
Encoder
   │
   ▼
Latent Representation Z
   │
   ▼
Decoder
   │
   ▼
Reconstructed X̂
```

Encoder:

$$Z=f_{\theta}(X)$$

Decoder:

$$\hat{X}=g_{\phi}(Z)$$

Mục tiêu:

$$\min_{\theta,\phi}\mathcal{L}(X,\hat{X})$$

Ví dụ với reconstruction loss:

$$\mathcal{L}=\frac{1}{n}\sum_{i=1}^{n}|X_i-\hat{X}_i|_2^2$$

Nếu:

$$dim(Z)=k<p$$

thì latent representation $Z$ là một dạng dimensionality reduction.

---

# 16. PCA và Autoencoder

| Đặc điểm                 | PCA              | Autoencoder      |
| ------------------------ | ---------------- | ---------------- |
| Mapping                  | Linear           | Có thể nonlinear |
| Optimization             | Eigenvalue / SVD | Gradient descent |
| Interpretability         | Tương đối cao    | Thấp hơn         |
| Computational complexity | Thấp hơn         | Cao hơn          |
| Nonlinear structure      | Không            | Có               |
| Reconstruction           | Linear           | Nonlinear        |
| Hyperparameters          | Ít               | Nhiều            |

Autoencoder có khả năng học representation phức tạp hơn nhưng yêu cầu nhiều quyết định hơn:

* architecture;
* latent dimension;
* activation;
* optimizer;
* learning rate;
* regularization;
* training epochs.

Do đó không nên sử dụng Autoencoder chỉ vì số chiều lớn; cần có lý do rõ ràng cho việc cần một nonlinear representation.

---

# 17. t-SNE và UMAP

Các phương pháp như **t-SNE** và **UMAP** thường được sử dụng để trực quan hóa dữ liệu có số chiều cao.

Ví dụ:

$$X\in\mathbb{R}^{n\times p}$$

được ánh xạ thành:

$$Z\in\mathbb{R}^{n\times2}$$

để biểu diễn trên mặt phẳng.

```text
High-dimensional Data
        │
        ▼
    t-SNE / UMAP
        │
        ▼
  2D Representation
        │
        ▼
 Visualization
```

Tuy nhiên, cần phân biệt:

$$\text{Visualization}\neq\text{Production Representation}$$

t-SNE đặc biệt phù hợp cho exploratory visualization hơn là làm preprocessing mặc định cho mô hình dự báo.

UMAP cũng có thể tạo embedding hữu ích cho visualization và một số downstream tasks, nhưng cần đánh giá riêng theo mục tiêu cụ thể.

---

# 18. Lựa chọn số chiều

Việc chọn $k$ là quyết định quan trọng.

Có thể dựa trên:

### Explained variance

$$CEV_k\geq\tau$$

### Reconstruction error

$$E_k\leq\epsilon$$

### Validation performance

$$k^*=\arg\min_k RMSE_{val}(k)$$

Trong nghiên cứu dự báo, tiêu chí cuối cùng đặc biệt quan trọng.

Không nên mặc định rằng:

$$\text{More explained variance}\Rightarrow\text{Better forecasting}$$

Mục tiêu cuối cùng phải được đánh giá bằng downstream task.

---

# 19. Trade-off giữa Compression và Information

Giảm số chiều luôn tạo ra sự đánh đổi.

Nếu $k$ quá nhỏ:

$$k\ll p$$

có nguy cơ mất thông tin.

Nếu $k$ quá lớn:

$$k\approx p$$

lợi ích dimensionality reduction giảm.

Có thể khái quát:

```text
k nhỏ
 │
 ├── Compression cao
 ├── Complexity thấp
 └── Information loss cao
          │
          ▼
       Optimal k
          │
          ▼
k lớn
 │
 ├── Compression thấp
 ├── Complexity cao
 └── Information loss thấp
```

Do đó mục tiêu không phải là tìm $k$ nhỏ nhất mà là tìm **$k$ phù hợp với mục tiêu của hệ thống**.

---

# 20. Dimensionality Reduction và Interpretability

Một hạn chế quan trọng là representation mới thường khó diễn giải.

Ví dụ:

$$Z_1=0.52X_1+0.31X_2-0.44X_3+\cdots$$

$Z_1$ không còn mang semantic trực tiếp như một feature gốc.

Điều này tạo ra trade-off:

$$\text{Compression}\leftrightarrow\text{Interpretability}$$

Trong các bài toán yêu cầu giải thích feature theo domain, Feature Selection có thể phù hợp hơn PCA hoặc Autoencoder.

Ngược lại, khi prediction performance và computational efficiency là ưu tiên chính, reduced representation có thể mang lại lợi ích đáng kể.

---

# 21. Ưu điểm

Dimensionality Reduction có các ưu điểm:

### 21.1. Giảm số chiều

$$p\rightarrow k,\quad k<p$$

### 21.2. Giảm redundancy

Các feature tương quan có thể được biểu diễn trong một số ít components.

### 21.3. Giảm computational complexity

Mô hình downstream có thể hoạt động trên:

$$k\ll p$$

dimensions.

### 21.4. Giảm nguy cơ high-dimensional sparsity

Trong một số bài toán, representation thấp chiều có thể giúp mô hình học dễ hơn.

### 21.5. Hỗ trợ visualization

Có thể chuyển dữ liệu nhiều chiều về 2D hoặc 3D để exploratory analysis.

---

# 22. Hạn chế

### 22.1. Mất thông tin

Nếu:

$$k\ll p$$

một phần information có thể bị loại bỏ.

### 22.2. Giảm interpretability

Components hoặc latent variables thường khó diễn giải hơn feature gốc.

### 22.3. Unsupervised methods có thể bỏ qua target relevance

Đặc biệt với PCA:

$$\text{Variance}\neq\text{Predictive Information}$$

### 22.4. Có thể tăng pipeline complexity

Autoencoder hoặc nonlinear methods yêu cầu nhiều hyperparameters và computational resources.

### 22.5. Leakage risk

Nếu reduction model được fit trên toàn bộ dataset, information từ validation/test sẽ đi vào representation.

---

# 23. So sánh các phương pháp chính

| Method      |           Linear |   Supervised | Mục tiêu chính                           | Interpretability |
| ----------- | ---------------: | -----------: | ---------------------------------------- | ---------------- |
| PCA         |               Có |        Không | Variance preservation                    | Trung bình       |
| SVD         |               Có |        Không | Low-rank representation                  | Trung bình       |
| Kernel PCA  |            Không |        Không | Nonlinear representation                 | Thấp             |
| Autoencoder | Có thể nonlinear | Thường không | Reconstruction / representation learning | Thấp             |
| t-SNE       |            Không |        Không | Visualization                            | Thấp             |
| UMAP        |            Không |        Không | Visualization / embedding                | Thấp             |

Không nên xem các phương pháp này là interchangeable.

Việc lựa chọn phụ thuộc vào mục tiêu:

$$
\text{Goal}\rightarrow
\begin{cases}
\text{Compression} &\rightarrow PCA/SVD\
\text{Nonlinear representation} &\rightarrow Kernel PCA/Autoencoder\
\text{Visualization} &\rightarrow t\text{-SNE/UMAP}
\end{cases}
$$

---

# 24. Quy trình áp dụng

Một pipeline dimensionality reduction phù hợp:

```text
Candidate Features
        │
        ▼
Train / Validation / Test Split
        │
        ▼
Fit Preprocessing on Train
        │
        ▼
Fit Dimensionality Reduction
        │
        ▼
Transform Train
        │
        ├──────────────┐
        ▼              ▼
   Validation         Test
        │              │
        ▼              ▼
   Transform         Transform
   using Train       using Train
   mapping           mapping
        │
        └──────┬───────┘
               ▼
       Downstream Model
               │
               ▼
       Evaluate Performance
```

Các tham số cần lưu gồm:

* method;
* input feature set;
* output dimension $k$;
* fitted transformation;
* training data version;
* validation configuration.

---

# 25. Dimensionality Reduction trong Pipeline nghiên cứu

Dimensionality Reduction không nên được xem là bước bắt buộc sau Feature Selection.

Có ba trường hợp:

### Trường hợp 1: Feature Selection đã đủ

Nếu:

$$p_{selected}\ll p$$

và performance tốt, có thể không cần reduction thêm.

### Trường hợp 2: Features vẫn có redundancy cao

Có thể sử dụng PCA hoặc phương pháp tương tự để tạo representation compact.

### Trường hợp 3: Cần nonlinear representation

Có thể xem xét Kernel PCA hoặc Autoencoder nếu dữ liệu và mục tiêu nghiên cứu phù hợp.

Do đó:

$$\text{Feature Selection}\rightarrow\text{Dimensionality Reduction}$$

là một pipeline khả dụng, nhưng không phải lúc nào cũng là pipeline tối ưu.

---

# 26. Nguyên tắc áp dụng

Dimensionality Reduction trong nghiên cứu được áp dụng theo các nguyên tắc:

1. **Phân biệt rõ selection và transformation:** reduced components không được xem là feature gốc.
2. **Training-only fitting:** mọi transformation phải được fit trên training data.
3. **Không sử dụng test để chọn $k$:** output dimension phải được xác định thông qua training/validation.
4. **Bảo toàn temporal ordering:** với time series, không được phá vỡ chronology.
5. **Đánh giá downstream:** explained variance hoặc reconstruction error không đủ để kết luận về prediction performance.
6. **Kiểm soát interpretability:** cần cân nhắc semantic của representation mới.
7. **Không mặc định PCA:** lựa chọn phương pháp phải dựa trên cấu trúc dữ liệu và mục tiêu.
8. **Reproducibility:** lưu transformation configuration và fitted parameters.
9. **So sánh với baseline:** cần đánh giá reduced representation so với feature space ban đầu hoặc subset từ Feature Selection.

---

# 27. Kết nối với toàn bộ Chương 6

Chương 6 hoàn thành một chuỗi phương pháp từ **loại bỏ feature không cần thiết** đến **xây dựng representation mới**:

```text
                    Feature Space
                         │
                         ▼
              01 Feature Selection
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
         Filter       Wrapper      Embedded
            │            │            │
            └────────────┼────────────┘
                         ▼
                 Selected Features
                         │
                         ▼
             05 Dimensionality Reduction
                         │
                         ▼
                Reduced Representation
                         │
                         ▼
                  Downstream Model
```

Có thể phân biệt bốn cấp độ chính:

$$\text{Filter} \rightarrow \text{Wrapper} \rightarrow \text{Embedded} \rightarrow \text{Representation Reduction}$$

Trong đó:

* **Filter Methods:** xác định feature dựa trên statistical relevance.
* **Wrapper Methods:** xác định subset dựa trên model performance.
* **Embedded Methods:** thực hiện selection trong quá trình model learning.
* **Dimensionality Reduction:** biến đổi feature space thành representation có số chiều thấp hơn.

Như vậy, `05_dimensionality_reduction.md` khép lại Chương 6 bằng cách chuyển từ câu hỏi **“giữ feature nào?”** sang **“biểu diễn dữ liệu như thế nào với số chiều thấp hơn?”**. Kết quả của chương này sẽ được sử dụng làm cơ sở để lựa chọn và tổ chức dữ liệu trong các chương tiếp theo, đặc biệt khi xây dựng pipeline preprocessing và AI-ready data.
