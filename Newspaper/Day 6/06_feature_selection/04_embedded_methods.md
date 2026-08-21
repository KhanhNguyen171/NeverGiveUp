# 04. Embedded Methods

## 1. Khái niệm Embedded Methods

**Embedded Methods** là nhóm phương pháp Feature Selection trong đó quá trình lựa chọn đặc trưng được **tích hợp trực tiếp vào quá trình huấn luyện mô hình**.

Khác với:

* **Filter Methods:** lựa chọn feature độc lập với mô hình;
* **Wrapper Methods:** lựa chọn subset bằng cách huấn luyện và đánh giá nhiều mô hình/subset;

Embedded Methods thực hiện selection ngay trong quá trình tối ưu tham số:

$$X\rightarrow\text{Model Training}\rightarrow\text{Feature Selection}$$

Có thể biểu diễn tổng quát:

$$\theta^*=\arg\min_{\theta}\left[\mathcal{L}(X,Y;\theta)+\lambda\Omega(\theta)\right]$$

Trong đó:

* $\theta$: tham số mô hình;
* $\mathcal{L}$: prediction loss;
* $\Omega(\theta)$: regularization hoặc cơ chế tạo sparsity;
* $\lambda$: mức độ kiểm soát complexity.

Khi một cơ chế embedded tạo ra các tham số bằng hoặc gần bằng $0$, feature tương ứng có thể được xem là ít cần thiết và được loại bỏ.

---

# 2. Vị trí trong Feature Selection Pipeline

Embedded Methods kế thừa candidate feature set từ các bước trước:

```text id="4j8m2k"
Feature Engineering
        │
        ▼
Candidate Features
        │
        ▼
Filter Methods
        │
        ▼
Reduced Candidate Set
        │
        ▼
Wrapper Methods
        │
        ▼
Embedded Methods
        │
        ├── LASSO
        ├── Elastic Net
        ├── Tree-based Importance
        └── Model-specific Selection
        │
        ▼
Selected Feature Set
        │
        ▼
Dimensionality Reduction
```

Thứ tự trên là một **pipeline tham khảo**, không phải yêu cầu bắt buộc. Embedded Methods có thể được áp dụng trực tiếp sau Feature Engineering nếu số lượng feature và computational budget cho phép.

Vai trò của Embedded Methods là tìm một tập feature vừa:

* có khả năng dự báo;
* phù hợp với cấu trúc của estimator;
* có độ phức tạp hợp lý.

---

# 3. Đặc điểm của Embedded Methods

Embedded Methods có ba đặc điểm chính.

### 3.1. Selection gắn với model

Feature importance hoặc feature sparsity được xác định trong quá trình model learning.

Do đó:

$$X^*_{M_1}\neq X^*_{M_2}$$

có thể xảy ra khi hai mô hình có cơ chế học khác nhau.

---

### 3.2. Không cần search toàn bộ subset

Wrapper Methods phải tìm kiếm nhiều subset:

$$X_1,X_2,\ldots,X_k$$

và huấn luyện mô hình tương ứng.

Embedded Methods thay vào đó đưa selection vào objective hoặc cấu trúc model:

$$\mathcal{L}*{total}=\mathcal{L}*{prediction}+\lambda\Omega(\theta)$$

Nhờ vậy, selection có thể được thực hiện đồng thời với parameter learning.

---

### 3.3. Cân bằng performance và complexity

Embedded Methods thường tối ưu đồng thời hai mục tiêu:

$$\min\left(\text{Prediction Loss}+\lambda\cdot\text{Complexity}\right)$$

Khi $\lambda$ tăng, mô hình có xu hướng sử dụng ít feature hơn hoặc tạo ra biểu diễn thưa hơn.

---

# 4. LASSO Regression

**LASSO (Least Absolute Shrinkage and Selection Operator)** là một ví dụ kinh điển của Embedded Feature Selection.

Mô hình Linear Regression:

$$\hat{y}=X\beta$$

được tối ưu với L1 penalty:

$$\hat{\beta}=\arg\min_{\beta}\left[\frac{1}{2n}|Y-X\beta|_2^2+\lambda|\beta|_1\right]$$

trong đó:

$$|\beta|*1=\sum*{j=1}^{p}|\beta_j|$$

L1 regularization khuyến khích một số coefficient trở thành chính xác bằng $0$:

$$\beta_j=0$$

Khi đó feature tương ứng có thể được loại bỏ:

$$\beta_j=0\Rightarrow X_j\notin X^*$$

---

## 4.1. Cơ chế tạo sparsity

Khác với Ridge:

$$\lambda\sum_j\beta_j^2$$

LASSO sử dụng:

$$\lambda\sum_j|\beta_j|$$

Hình học của L1 constraint tạo điều kiện để nghiệm nằm trên các trục tọa độ, dẫn đến một số coefficient bằng $0$.

```text id="a3v6p1"
Feature Coefficients
       │
       ├── β1 ≠ 0 ──► Keep X1
       ├── β2 = 0 ──► Remove X2
       ├── β3 ≠ 0 ──► Keep X3
       └── β4 = 0 ──► Remove X4
```

Do đó LASSO vừa thực hiện:

* parameter estimation;
* regularization;
* feature selection.

---

# 5. Elastic Net

LASSO có thể gặp vấn đề khi các feature có tương quan cao.

Ví dụ:

$$corr(X_1,X_2)\approx1$$

LASSO có thể chọn một feature và loại feature còn lại một cách không ổn định.

**Elastic Net** kết hợp L1 và L2 regularization:

$$\hat{\beta}=\arg\min_{\beta}\left[\frac{1}{2n}|Y-X\beta|_2^2+\lambda_1|\beta|_1+\lambda_2|\beta|_2^2\right]$$

hoặc theo cách parameter hóa phổ biến:

$$\hat{\beta}=\arg\min_{\beta}\left[\frac{1}{2n}|Y-X\beta|_2^2+\lambda\left(\alpha|\beta|_1+(1-\alpha)|\beta|_2^2\right)\right]$$

Trong đó:

$$0\leq\alpha\leq1$$

* $\alpha=1$: LASSO;
* $\alpha=0$: Ridge;
* $0<\alpha<1$: Elastic Net.

Elastic Net đặc biệt hữu ích khi có các nhóm feature tương quan cao.

---

# 6. Tree-based Feature Selection

Các mô hình cây như Decision Tree, Random Forest và Gradient Boosting có thể cung cấp **feature importance** dựa trên mức độ đóng góp của feature vào quá trình phân chia dữ liệu.

Với một feature $X_j$, importance có thể được biểu diễn khái quát:

$$I_j=\sum_{s\in S_j}\Delta\mathcal{L}_s$$

trong đó $S_j$ là tập các split sử dụng feature $X_j$, còn $\Delta\mathcal{L}_s$ là mức cải thiện objective tại split $s$.

Sau khi tính importance:

$$I_1,I_2,\ldots,I_p$$

có thể đặt threshold:

$$I_j<\tau\Rightarrow X_j\text{ removed}$$

hoặc giữ Top-$k$ features.

---

## 6.1. Ưu điểm

Tree-based selection có thể phát hiện:

* nonlinear relationship;
* interaction;
* threshold effects.

Ví dụ:

$$Y=f(X_1,X_2)$$

có thể được mô hình hóa mà không yêu cầu quan hệ tuyến tính giữa feature và target.

---

## 6.2. Hạn chế

Feature importance dựa trên impurity có thể bị ảnh hưởng bởi:

* feature có nhiều possible split points;
* correlated features;
* feature cardinality.

Do đó importance không nên được diễn giải như một thước đo causal importance.

---

# 7. Permutation Importance

**Permutation Importance** đánh giá mức độ quan trọng của feature bằng cách phá vỡ mối liên hệ giữa feature đó và target rồi đo mức suy giảm performance.

Giả sử metric là loss $L$.

Baseline:

$$L_{base}=L(X,Y)$$

Sau khi shuffle feature $X_j$:

$$L_j^{perm}=L(X^{perm}_j,Y)$$

Importance có thể được định nghĩa:

$$I_j=L_j^{perm}-L_{base}$$

Nếu:

$$I_j\gg0$$

việc permutation feature $X_j$ làm performance suy giảm mạnh, cho thấy feature có đóng góp đáng kể cho model.

Permutation importance không phải embedded method theo nghĩa chặt như LASSO, vì nó thường được thực hiện **sau khi model đã được huấn luyện**. Trong pipeline này, nó được xem là một **model-based importance mechanism bổ trợ** cho Embedded Selection.

Điểm phân biệt này cần được giữ rõ để tránh đồng nhất mọi feature importance với Embedded Methods.

---

# 8. Feature Importance và Correlated Features

Khi các feature có tương quan cao:

$$corr(X_1,X_2)\approx1$$

mô hình có thể thay thế $X_1$ bằng $X_2$ mà performance gần như không thay đổi.

Khi đó importance của từng feature riêng lẻ có thể không phản ánh đúng thông tin của cả nhóm.

Ví dụ:

```text id="z2x5n8"
       ┌── X1 ──┐
       │        │
       ├── X2 ──┼──► Model
       │        │
       └── X3 ──┘
          correlated
```

Có thể xảy ra:

$$I(X_1)\ll I(X_2)$$

không phải vì $X_1$ không hữu ích, mà vì $X_2$ đang mang phần lớn thông tin tương tự.

Vì vậy Embedded Selection cần được kết hợp với **redundancy analysis** từ `02_filter_methods.md`.

---

# 9. Embedded Selection trong Time Series

Trong time series, feature set thường bao gồm:

$$X_t={X_t^{raw},X_{t-1},X_{t-2},\ldots,X_{t-L},F_t^{temporal},F_t^{rolling}}$$

Các feature này có dependency mạnh theo thời gian.

Embedded Methods có thể giúp mô hình tự xác định:

* lag nào có đóng góp;
* sensor nào có predictive value;
* rolling statistic nào hữu ích;
* temporal feature nào cần thiết.

Ví dụ với LASSO:

$$\hat{\beta}_{lag_k}=0$$

có thể cho thấy lag $k$ không cần thiết đối với mô hình tuyến tính regularized.

Tuy nhiên, không nên diễn giải:

$$\beta_{lag_k}=0$$

như bằng chứng rằng lag đó không chứa thông tin trong mọi mô hình. Kết quả chỉ phản ánh **mô hình, dữ liệu và regularization configuration cụ thể**.

---

# 10. Temporal Leakage trong Embedded Methods

Embedded Methods phải tuân thủ cùng nguyên tắc temporal isolation với Filter và Wrapper Methods.

Quy trình đúng:

```text id="u5k3d7"
Chronological Split
        │
        ▼
Training Data
        │
        ▼
Fit Embedded Model
        │
        ├── Learn Parameters
        ├── Apply Regularization
        └── Determine Feature Importance
        │
        ▼
Selected Features
        │
        ├── Validation → Transform / Evaluate
        └── Test → Final Evaluation
```

Không được fit LASSO, tree model hoặc bất kỳ embedded selector nào trên toàn bộ dataset trước khi chronological split.

Nếu model được fit trên:

$$D_{train}\cup D_{validation}\cup D_{test}$$

thì feature selection đã sử dụng information từ dữ liệu đánh giá.

Do đó:

$$\boxed{\text{Feature Selection must be fitted using training information only}}$$

---

# 11. Hyperparameter $\lambda$ và Selection

Đối với regularization-based methods, mức penalty quyết định mức độ selection.

Với LASSO:

$$\mathcal{L}*{total}=\mathcal{L}*{prediction}+\lambda|\beta|_1$$

Khi $\lambda$ nhỏ:

$$\lambda\rightarrow0$$

mô hình ưu tiên prediction performance và thường giữ nhiều feature hơn.

Khi $\lambda$ tăng:

$$\lambda\uparrow$$

nhiều coefficient có xu hướng tiến về $0$.

Khái quát:

```text id="p1v7q4"
λ nhỏ
  │
  ▼
Nhiều Features
  │
  │ increase λ
  ▼
Ít Features
  │
  ▼
Sparse Model
```

Do đó $\lambda$ không chỉ là regularization hyperparameter mà còn kiểm soát **feature-selection strength**.

---

# 12. Lựa chọn Hyperparameter mà không Leakage

Không được chọn $\lambda$ bằng test performance.

Quy trình:

```text id="m6c2v9"
Train
  │
  ├── λ1 ──► Validation
  ├── λ2 ──► Validation
  ├── λ3 ──► Validation
  └── λ4 ──► Validation
            │
            ▼
       Select λ*
            │
            ▼
      Lock Configuration
            │
            ▼
       Final Test
```

Với time series, validation phải duy trì temporal ordering.

Sau khi chọn $\lambda^*$ và feature configuration, test set chỉ được sử dụng cho **final evaluation**.

---

# 13. Embedded Methods và Model Complexity

Embedded Selection tạo ra một trade-off giữa prediction performance và model complexity:

$$J=\mathcal{L}_{prediction}+\lambda\Omega(\theta)$$

Nếu regularization quá yếu:

$$\lambda\rightarrow0$$

mô hình có thể giữ quá nhiều feature.

Nếu regularization quá mạnh:

$$\lambda\rightarrow\infty$$

mô hình có thể loại bỏ cả những feature hữu ích.

Do đó cần tìm configuration nằm trong vùng cân bằng:

```text id="v9n2s6"
Prediction Error
      │\
      │ \
      │  \__
      │     \__
      │        \__
      └────────────────► Complexity
             │
             ▼
      Useful Trade-off
```

Mục tiêu không phải là giảm số lượng feature xuống mức nhỏ nhất, mà là đạt **performance tốt với complexity hợp lý**.

---

# 14. Ưu điểm

Embedded Methods có các ưu điểm chính:

### 14.1. Kết hợp selection với training

Không cần xây dựng quá nhiều model độc lập như Wrapper Methods.

### 14.2. Model-aware

Feature được đánh giá trong context của estimator.

### 14.3. Có thể xử lý nonlinear relationship

Đặc biệt với tree-based models.

### 14.4. Chi phí thường thấp hơn Wrapper Search

Selection xảy ra trong hoặc gắn chặt với quá trình training.

### 14.5. Có khả năng kiểm soát complexity

Regularization cho phép cân bằng:

$$\text{fit}\leftrightarrow\text{complexity}$$

---

# 15. Hạn chế

### 15.1. Model-dependent

Feature được chọn phụ thuộc vào estimator và objective.

### 15.2. Không phải mọi importance đều ổn định

Correlated features có thể làm feature importance thay đổi giữa các lần training hoặc các sample khác nhau.

### 15.3. Regularization có thể loại bỏ feature hữu ích

Nếu penalty quá mạnh:

$$\lambda\gg0$$

một số feature có thể bị loại dù chúng có đóng góp nhỏ nhưng thực sự hữu ích.

### 15.4. Feature importance không đồng nghĩa với causality

Một feature quan trọng đối với model không chứng minh rằng feature đó gây ra target.

### 15.5. Khó so sánh trực tiếp giữa các model

Importance từ Random Forest và coefficient từ LASSO không cùng một thang đo và không nên được so sánh trực tiếp.

---

# 16. So sánh Filter, Wrapper và Embedded

| Tiêu chí            | Filter            | Wrapper           | Embedded                          |
| ------------------- | ----------------- | ----------------- | --------------------------------- |
| Model-dependent     | Không             | Có                | Có                                |
| Selection mechanism | Statistical score | Subset evaluation | During / integrated with training |
| Interaction         | Hạn chế           | Có                | Tùy model                         |
| Computational cost  | Thấp              | Cao               | Trung bình                        |
| Scalability         | Cao               | Thấp              | Trung bình–cao                    |
| Regularization      | Không bắt buộc    | Không             | Thường có ở một số phương pháp    |
| Model-specific      | Không             | Có                | Có                                |
| Ví dụ               | Pearson, MI       | SFS, RFE          | LASSO, Elastic Net, Tree-based    |
| Nguy cơ leakage     | Có                | Cao               | Có                                |

Có thể tóm tắt:

$$\text{Filter}\rightarrow\text{Statistical Relevance}$$

$$\text{Wrapper}\rightarrow\text{Subset Performance}$$

$$\text{Embedded}\rightarrow\text{Model-integrated Selection}$$

Ba nhóm phương pháp giải quyết cùng một mục tiêu nhưng ở các mức độ phụ thuộc model khác nhau.

---

# 17. Quy trình áp dụng

Một quy trình Embedded Selection có thể được tổ chức như sau:

```text id="g8v4k2"
Candidate Feature Set
        │
        ▼
Define Estimator
        │
        ▼
Define Selection Mechanism
        │
        ├── L1 / Elastic Net
        ├── Tree Importance
        └── Model-specific Mechanism
        │
        ▼
Train on Training Data
        │
        ▼
Generate Selected Features
        │
        ▼
Validate
        │
        ▼
Lock Configuration
        │
        ▼
Final Test Evaluation
```

Nếu sử dụng regularization, cần lưu:

* penalty type;
* regularization strength;
* estimator configuration;
* selected features;
* training data version;
* validation configuration.

Điều này bảo đảm khả năng tái lập kết quả.

---

# 18. Tiêu chí đánh giá

Embedded Selection cần được đánh giá trên cả **feature reduction** và **downstream performance**.

### 18.1. Feature reduction

$$Reduction=\frac{p-k}{p}\times100%$$

### 18.2. Prediction performance

So sánh:

$$M(X)$$

và:

$$M(X^*)$$

với cùng evaluation protocol.

### 18.3. Stability

Có thể đánh giá feature-selection stability giữa các training runs:

$$Stability(X^*_1,X^*_2)$$

Một subset ổn định hơn thường đáng tin cậy hơn trong các nghiên cứu cần khả năng diễn giải.

### 18.4. Computational cost

Theo dõi:

* training time;
* inference time;
* memory;
* số lượng parameters.

---

# 19. Embedded Methods và Dimensionality Reduction

Embedded Selection vẫn giữ các feature gốc:

$$X^*\subseteq X$$

Trong khi dimensionality reduction tạo ra một representation mới:

$$Z=f(X)$$

với:

$$Z\in\mathbb{R}^{k},\quad k<p$$

Ví dụ:

```text id="b7x3n1"
Original Features
X1 ─┐
X2 ─┤
X3 ─┤──► Dimensionality Reduction ──► Z1
X4 ─┤                                  Z2
X5 ─┘                                  Z3

Embedded Selection:

X1 ─────────► Keep
X2 ─────────► Remove
X3 ─────────► Keep
X4 ─────────► Remove
X5 ─────────► Keep
```

Vì vậy, `05_dimensionality_reduction.md` sẽ không tiếp tục chọn feature dựa trên importance, mà tập trung vào **xây dựng không gian biểu diễn có số chiều thấp hơn**.

---

# 20. Nguyên tắc áp dụng

Embedded Methods trong nghiên cứu được áp dụng theo các nguyên tắc:

1. **Training-only fitting:** selector phải được fit trên training data.
2. **Model awareness:** ghi rõ estimator được sử dụng.
3. **Controlled regularization:** hyperparameter điều khiển selection phải được xác định và đánh giá trên validation.
4. **No test tuning:** test không được dùng để chọn regularization hoặc feature subset.
5. **Temporal integrity:** time series phải giữ chronological ordering.
6. **Importance interpretation:** feature importance chỉ phản ánh đóng góp đối với model, không phải causal effect.
7. **Redundancy awareness:** cần xem xét correlated features trước khi diễn giải importance.
8. **Performance-complexity trade-off:** đánh giá đồng thời prediction performance và số lượng feature.
9. **Reproducibility:** lưu configuration, training data version, selected feature set và evaluation protocol.

---

# 21. Kết nối với các mục trong Chương 6

Toàn bộ Chương 6 được tổ chức theo tiến trình từ **đánh giá độc lập với model → đánh giá theo model → selection trong model → tạo representation mới**:

```text id="n4k7p2"
01 Feature Selection
        │
        ▼
02 Filter Methods
        │
        │ Statistical screening
        ▼
03 Wrapper Methods
        │
        │ Subset + model evaluation
        ▼
04 Embedded Methods
        │
        │ Selection integrated with learning
        ▼
05 Dimensionality Reduction
        │
        │ New lower-dimensional representation
        ▼
Final Feature Representation
```

Trong đó, Embedded Methods là bước cuối của ba nhóm Feature Selection chính trước khi chuyển sang Dimensionality Reduction.

Nếu Filter Methods ưu tiên **tốc độ**, Wrapper Methods ưu tiên **model-specific performance**, thì Embedded Methods tạo ra điểm cân bằng bằng cách **tích hợp feature selection vào quá trình học mô hình**.

Sau khi hoàn tất bước này, `05_dimensionality_reduction.md` sẽ giải quyết một vấn đề khác: khi số lượng feature vẫn lớn hoặc các feature có cấu trúc tương quan cao, thay vì tiếp tục loại bỏ từng feature, có thể chuyển toàn bộ dữ liệu sang một **không gian biểu diễn có số chiều thấp hơn**.
