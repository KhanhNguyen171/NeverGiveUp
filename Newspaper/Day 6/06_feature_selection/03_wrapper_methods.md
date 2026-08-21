# 03. Wrapper Methods

## 1. Khái niệm Wrapper Methods

**Wrapper Methods** là nhóm phương pháp Feature Selection đánh giá một **tập con các đặc trưng thông qua hiệu năng của một mô hình học máy cụ thể**.

Khác với Filter Methods trong `02_filter_methods.md`, Wrapper Methods không đánh giá feature chỉ dựa trên một statistical score độc lập với mô hình. Thay vào đó, chúng thực hiện quá trình:

$$\text{Feature Subset}\rightarrow\text{Train Model}\rightarrow\text{Evaluate Performance}$$

Với tập feature ban đầu:

$$X={X_1,X_2,\ldots,X_p}$$

Wrapper Methods tìm subset:

$$X^*\subseteq X$$

sao cho mô hình $M$ đạt hiệu năng tốt nhất trên tiêu chí đánh giá:

$$X^*=\arg\min_{X'\subseteq X}\mathcal{L}(M(X'),Y)$$

đối với bài toán minimization, hoặc:

$$X^*=\arg\max_{X'\subseteq X}\mathcal{S}(M(X'),Y)$$

đối với metric cần maximization.

Do phải huấn luyện và đánh giá mô hình nhiều lần, Wrapper Methods thường có chi phí tính toán cao hơn Filter Methods.

---

# 2. Vị trí trong Feature Selection Pipeline

Wrapper Methods kế thừa candidate feature set được tạo ra từ các bước trước:

```text id="2b7s8q"
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
        ├── Forward Selection
        ├── Backward Elimination
        └── Recursive Feature Elimination
        │
        ▼
Candidate Optimal Subset
        │
        ▼
Embedded Methods
        │
        ▼
Final Feature Set
```

Cách tổ chức này đặc biệt hữu ích khi số lượng features ban đầu lớn.

Filter Methods có thể nhanh chóng loại bỏ những feature rõ ràng không liên quan, sau đó Wrapper Methods thực hiện tìm kiếm subset trên không gian nhỏ hơn.

Tuy nhiên, đây là một **pipeline lựa chọn**, không phải quy tắc bắt buộc. Trong một số nghiên cứu, Wrapper Methods có thể được áp dụng trực tiếp nếu số lượng feature đủ nhỏ.

---

# 3. Đặc điểm cốt lõi

Wrapper Methods có ba đặc điểm chính.

### 3.1. Model-dependent

Chất lượng của feature subset phụ thuộc vào mô hình được sử dụng:

$$X^*_{M_1}\neq X^*_{M_2}$$

Một subset tối ưu cho Random Forest chưa chắc tối ưu cho Linear Regression hoặc Neural Network.

Do đó, Wrapper Selection phải xác định rõ **estimator** trước khi thực hiện.

---

### 3.2. Đánh giá theo subset

Không chỉ đánh giá:

$$S(X_j,Y)$$

như Filter Methods, Wrapper Methods đánh giá:

$$S(X_1,X_3,X_7,Y)$$

Điều này cho phép phương pháp xem xét phần nào các **interaction giữa features**.

---

### 3.3. Tốn chi phí tính toán

Nếu có $p$ features, số lượng subset khả dĩ là:

$$2^p$$

Do đó, exhaustive search nhanh chóng trở nên không khả thi khi $p$ lớn.

Ví dụ:

$$p=20\Rightarrow2^{20}=1,048,576$$

subsets.

Vì vậy Wrapper Methods thường sử dụng các **heuristic search strategies** thay vì kiểm tra toàn bộ không gian.

---

# 4. Wrapper Methods và Objective Function

Một Wrapper Method cần xác định rõ objective dùng để so sánh các subset.

Ví dụ với bài toán regression:

$$J(X')=RMSE_{val}(X')$$

Mục tiêu:

$$X^*=\arg\min_{X'}J(X')$$

Đối với classification có thể sử dụng:

$$J(X')=1-F1_{val}(X')$$

hoặc một metric phù hợp khác.

Đối với forecasting, metric phải được thống nhất với hệ thống đánh giá của nghiên cứu. Ví dụ:

$$RMSE=\sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2}$$

Feature subset không được lựa chọn dựa trên test performance.

---

# 5. Forward Selection

**Forward Selection** bắt đầu từ một tập feature rỗng hoặc một tập feature nền tảng, sau đó lần lượt thêm feature mang lại cải thiện lớn nhất.

Ban đầu:

$$S_0=\emptyset$$

Ở mỗi bước:

$$x^*=\arg\max_{x\notin S}Score(S\cup{x})$$

Sau đó:

$$S\leftarrow S\cup{x^*}$$

Quá trình dừng khi:

* đạt số lượng feature mong muốn;
* performance không còn cải thiện;
* improvement nhỏ hơn threshold;
* hoặc đạt stopping criterion được xác định trước.

### Ví dụ

```text id="8s7v2d"
Start
  │
  ▼
{}
  │
  ├── +X1 → Score = 0.72
  ├── +X2 → Score = 0.61
  └── +X3 → Score = 0.68
           │
           ▼
         {X1}
           │
           ├── +X2 → Score = 0.78
           ├── +X3 → Score = 0.75
           └── +X4 → Score = 0.73
                    │
                    ▼
                 {X1,X2}
```

Ưu điểm của Forward Selection là đơn giản và thường ít tốn chi phí hơn exhaustive search.

Hạn chế là quyết định ở bước trước có thể ảnh hưởng đến các bước sau. Một feature bị bỏ qua ở giai đoạn đầu có thể trở nên hữu ích khi kết hợp với feature khác.

---

# 6. Backward Elimination

Backward Elimination bắt đầu với toàn bộ feature:

$$S_0=X$$

Sau đó lần lượt loại bỏ feature gây ảnh hưởng ít nhất đến performance.

Ở mỗi bước:

$$x^*=\arg\min_{x\in S}\Delta Score(S\setminus{x})$$

và:

$$S\leftarrow S\setminus{x^*}$$

Quá trình tiếp tục cho đến khi đạt stopping criterion.

```text id="4r6x3p"
{X1,X2,X3,X4,X5}
          │
          ▼
       Remove X4
          │
          ▼
   {X1,X2,X3,X5}
          │
          ▼
       Remove X3
          │
          ▼
     {X1,X2,X5}
```

Backward Elimination có lợi thế khi số lượng feature ban đầu không quá lớn và muốn bắt đầu từ một mô hình đầy đủ.

Hạn chế là chi phí ban đầu cao vì phải huấn luyện mô hình với toàn bộ feature set.

---

# 7. Recursive Feature Elimination

**Recursive Feature Elimination (RFE)** là một chiến lược wrapper có tính đệ quy.

Quy trình:

```text id="8z7m4x"
All Features
     │
     ▼
Train Model
     │
     ▼
Estimate Feature Importance
     │
     ▼
Remove Least Important Features
     │
     ▼
Retrain Model
     │
     ▼
Repeat
     │
     ▼
Selected Features
```

Với feature importance $I_j$, tại mỗi iteration loại bỏ các feature có:

$$I_j\rightarrow\min$$

Sau đó mô hình được huấn luyện lại trên subset mới.

RFE có thể sử dụng với các estimator cung cấp:

* coefficient;
* feature importance;
* hoặc một cơ chế ranking tương đương.

Điểm quan trọng là feature ranking trong RFE phụ thuộc vào estimator.

---

# 8. Sequential Feature Selection

Forward Selection và Backward Elimination có thể được tổng quát thành **Sequential Feature Selection (SFS)**.

### Forward SFS

$$S_{k+1}=S_k\cup{x^*}$$

### Backward SFS

$$S_{k-1}=S_k\setminus{x^*}$$

Trong đó $x^*$ là feature tạo ra subset tốt nhất theo objective.

Sequential methods không tìm kiếm toàn bộ:

$$2^p$$

subsets mà chỉ khám phá một phần không gian.

Đây là sự đánh đổi giữa:

$$\text{Search Cost}\leftrightarrow\text{Subset Optimality}$$

---

# 9. Exhaustive Search

Trong trường hợp số lượng feature rất nhỏ, có thể đánh giá tất cả các subset:

$$\mathcal{P}(X)={X'|X'\subseteq X}$$

và chọn:

$$X^*=\arg\min_{X'\in\mathcal{P}(X)}J(X')$$

Số subset:

$$|\mathcal{P}(X)|=2^p$$

Do đó exhaustive search chỉ thực tế khi $p$ nhỏ.

Ưu điểm:

* không phụ thuộc heuristic search;
* có thể tìm được subset tối ưu theo objective đã định.

Nhược điểm:

* exponential complexity;
* không phù hợp với high-dimensional data.

---

# 10. Cross-Validation trong Wrapper Methods

Vì Wrapper Methods lựa chọn feature dựa trên model performance, việc đánh giá subset cần hạn chế phụ thuộc vào một lần train/validation split.

Một cách tiếp cận là sử dụng cross-validation:

```text id="w7c5u2"
Feature Subset
      │
      ▼
 ┌─────────────┐
 │ Fold 1      │
 │ Fold 2      │
 │ Fold 3      │
 │ ...         │
 └─────────────┘
      │
      ▼
Mean Validation Score
      │
      ▼
Subset Score
```

Ví dụ:

$$Score(S)=\frac{1}{K}\sum_{k=1}^{K}Score_k(S)$$

Tuy nhiên, với **time series**, không nên áp dụng random K-fold như dữ liệu IID nếu nó phá vỡ temporal ordering.

Thay vào đó, có thể sử dụng các chiến lược temporal validation phù hợp như expanding-window hoặc rolling-window evaluation.

---

# 11. Wrapper Methods cho Time Series

Trong time series forecasting, Wrapper Methods phải bảo toàn thứ tự thời gian.

Ví dụ:

$$X_{t-L+1:t}\rightarrow Y_{t+H}$$

Feature selection phải đảm bảo feature subset tại thời điểm dự báo chỉ sử dụng thông tin có sẵn trước hoặc tại thời điểm đó.

Pipeline:

```text id="q3n7fd"
Historical Data
      │
      ▼
Chronological Train / Validation
      │
      ▼
Candidate Feature Subset
      │
      ▼
Train Forecasting Model
      │
      ▼
Temporal Validation
      │
      ▼
Evaluate RMSE / MAE / R²
      │
      ▼
Select Best Subset
```

Không được chọn subset bằng cách tối ưu trực tiếp trên test set.

---

# 12. Data Leakage trong Wrapper Methods

Wrapper Methods có rủi ro leakage cao hơn Filter Methods vì chúng lặp lại quá trình model training và evaluation nhiều lần.

Một quy trình sai:

```text id="4s0x2n"
All Data
   │
   ▼
Try Feature Subset
   │
   ▼
Evaluate on Test
   │
   ▼
Choose Best Subset
```

Nếu lặp lại nhiều subset và chọn subset có test score tốt nhất, test set đã trở thành một phần của quá trình training/selection.

Quy trình đúng:

```text id="q9b3wd"
Train
  │
  ├── Feature Subset A ──► Validation Score
  ├── Feature Subset B ──► Validation Score
  ├── Feature Subset C ──► Validation Score
  └── ...
             │
             ▼
       Select Best Subset
             │
             ▼
        Lock Selection
             │
             ▼
      Final Test Evaluation
```

Test chỉ được sử dụng **sau khi feature subset đã được khóa**.

Đây là nguyên tắc quan trọng kế thừa từ `01_feature_selection.md` và `02_filter_methods.md`.

---

# 13. Wrapper Methods và Feature Interaction

Một ưu điểm quan trọng của Wrapper Methods là khả năng đánh giá feature theo **context của subset**.

Ví dụ:

$$Score(X_1)\approx Score(X_2)\approx0$$

nhưng:

$$Score({X_1,X_2})\gg0$$

thì Filter Method có thể loại bỏ cả hai feature, trong khi Wrapper Method có khả năng phát hiện giá trị của chúng khi kết hợp.

Tuy nhiên, khả năng này phụ thuộc vào estimator và search strategy.

Không thể kết luận rằng Wrapper Methods luôn phát hiện được mọi interaction.

---

# 14. Ưu điểm

### 14.1. Model-aware

Feature subset được đánh giá trực tiếp theo mô hình downstream.

### 14.2. Có thể xem xét interaction

Feature được đánh giá trong context của các feature khác.

### 14.3. Tối ưu theo mục tiêu thực tế

Nếu objective là validation RMSE, Wrapper Method trực tiếp tìm subset giúp giảm RMSE:

$$X^*=\arg\min_X RMSE_{val}(X)$$

Điều này gần với mục tiêu cuối cùng của forecasting hơn so với một statistical score đơn lẻ.

---

# 15. Hạn chế

### 15.1. Chi phí tính toán cao

Mỗi subset yêu cầu train và evaluate model.

Nếu có $m$ subset:

$$Cost\approx m\times Cost(Model\ Training)$$

### 15.2. Model-dependent

Subset tối ưu cho model này có thể không tối ưu cho model khác.

### 15.3. Nguy cơ overfitting selection

Nếu thử quá nhiều subsets trên cùng validation set, quá trình selection có thể dần thích nghi với validation data.

Do đó cần kiểm soát:

* số lần thử;
* search space;
* stopping criteria;
* validation strategy.

### 15.4. Khó mở rộng

Khi $p$ tăng, không gian subset tăng theo:

$$O(2^p)$$

nếu xét exhaustive search.

---

# 16. So sánh Filter và Wrapper

| Tiêu chí            | Filter            | Wrapper           |
| ------------------- | ----------------- | ----------------- |
| Model-dependent     | Không             | Có                |
| Đánh giá feature    | Statistical score | Model performance |
| Interaction         | Hạn chế           | Có khả năng       |
| Computational cost  | Thấp              | Cao               |
| Search subset       | Thường đơn giản   | Có                |
| Model-specific      | Không             | Có                |
| Scalability         | Cao               | Thấp hơn          |
| Data leakage risk   | Có                | Cao hơn           |
| Prediction-oriented | Gián tiếp         | Trực tiếp         |

Có thể khái quát:

$$\text{Filter}\rightarrow\text{Fast Screening}$$

$$\text{Wrapper}\rightarrow\text{Model-aware Selection}$$

Vì vậy, hai nhóm phương pháp có thể được kết hợp thay vì xem chúng là các phương pháp cạnh tranh hoàn toàn.

---

# 17. Khi nào nên sử dụng Wrapper Methods?

Wrapper Methods phù hợp khi:

* số lượng candidate features không quá lớn;
* prediction performance là mục tiêu chính;
* computational budget cho phép nhiều lần huấn luyện;
* mô hình downstream đã được xác định tương đối rõ;
* cần đánh giá interaction giữa các features.

Không nên ưu tiên Wrapper Methods khi:

* số lượng feature cực lớn;
* model training rất đắt;
* dataset có hạn chế nghiêm trọng về computational resources;
* chưa có estimator phù hợp để đánh giá subset.

Trong trường hợp đó, Filter Methods có thể được sử dụng trước để giảm search space.

---

# 18. Quy trình đề xuất

Một pipeline phù hợp cho nghiên cứu:

```text id="j3q7xk"
Candidate Features
        │
        ▼
Filter Screening
        │
        ▼
Reduced Candidate Set
        │
        ▼
Define Estimator
        │
        ▼
Define Temporal Validation
        │
        ▼
Search Feature Subsets
        │
        ├── Forward Selection
        ├── Backward Elimination
        └── RFE
        │
        ▼
Compare Validation Performance
        │
        ▼
Lock Selected Subset
        │
        ▼
Train Final Model
        │
        ▼
Evaluate on Test
```

Trong đó ba thành phần phải được xác định **trước khi chạy selection**:

1. estimator;
2. validation strategy;
3. selection metric.

Điều này giúp giảm khả năng điều chỉnh quy trình selection theo kết quả test.

---

# 19. Tiêu chí dừng

Wrapper search cần stopping criterion rõ ràng.

Có thể dừng khi:

### Đạt số feature mong muốn

$$|S|=k$$

### Không còn cải thiện

$$Score(S_{t+1})-Score(S_t)<\epsilon$$

### Đạt ngân sách tính toán

$$Cost(S)\geq C_{max}$$

### Đạt performance mục tiêu

$$RMSE_{val}\leq\tau$$

Stopping criterion phải được xác định trước hoặc được quản lý như một hyperparameter của experiment.

---

# 20. Đánh giá kết quả

Sau khi chọn subset $X^*$, cần so sánh với baseline sử dụng toàn bộ feature:

$$M(X)\quad\text{vs.}\quad M(X^*)$$

Các tiêu chí:

### Performance

$$\Delta RMSE=RMSE(X^*)-RMSE(X)$$

### Feature reduction

$$Reduction=\frac{p-|X^*|}{p}\times100%$$

### Computational cost

So sánh:

* training time;
* inference time;
* memory consumption.

Một subset tốt không nhất thiết là subset có ít feature nhất. Mục tiêu là tìm **trade-off hợp lý giữa predictive performance và complexity**.

---

# 21. Kết nối với Embedded Methods

Wrapper Methods thực hiện selection **bên ngoài quá trình training của model**:

```text id="3m9k2p"
Feature Subset
      │
      ▼
Train Model
      │
      ▼
Evaluate
      │
      ▼
Choose Subset
      │
      ▼
Repeat
```

Trong khi Embedded Methods thực hiện selection **bên trong quá trình training**:

```text id="m5w8r2"
Features
   │
   ▼
Model Training
   │
   ├── Learn Parameters
   ├── Estimate Importance
   └── Select / Shrink Features
   │
   ▼
Final Model
```

Sự khác biệt này là cơ sở để chuyển sang `04_embedded_methods.md`.

Embedded Methods thường tìm cách đạt được lợi ích của model-aware selection nhưng với chi phí thấp hơn Wrapper Search trong một số trường hợp.

---

# 22. Nguyên tắc áp dụng

Wrapper Methods trong nghiên cứu được áp dụng theo các nguyên tắc:

1. **Model-dependent:** phải xác định rõ estimator dùng để đánh giá subset.
2. **Validation-based:** subset được lựa chọn bằng validation strategy, không bằng test set.
3. **Temporal integrity:** đối với time series, validation phải bảo toàn thứ tự thời gian.
4. **No test leakage:** test set được khóa cho đến khi selection hoàn tất.
5. **Controlled search:** xác định rõ search strategy và stopping criterion.
6. **Computational awareness:** theo dõi chi phí khi số lượng subset tăng.
7. **Performance-complexity trade-off:** không tối ưu performance mà bỏ qua số lượng feature và chi phí.
8. **Model specificity:** subset được chọn cho một estimator không mặc nhiên được xem là tối ưu cho mọi estimator.
9. **Reproducibility:** lưu estimator, validation strategy, metric, search strategy và selected feature set.

---

# 23. Liên kết với các mục tiếp theo

Chương 6 được tổ chức theo mức độ phụ thuộc vào mô hình:

```text id="v6k1q8"
01 Feature Selection
        │
        ▼
02 Filter Methods
        │
        │ Model-independent
        ▼
03 Wrapper Methods
        │
        │ Model-dependent search
        ▼
04 Embedded Methods
        │
        │ Selection during training
        ▼
05 Dimensionality Reduction
        │
        │ Create new lower-dimensional representation
        ▼
Final Feature Representation
```

Trong đó:

* `02_filter_methods.md` tập trung vào **statistical relevance và redundancy**.
* `03_wrapper_methods.md` tập trung vào **model-based subset search**.
* `04_embedded_methods.md` sẽ trình bày các phương pháp thực hiện feature selection ngay trong quá trình học tham số.
* `05_dimensionality_reduction.md` sẽ chuyển sang một cách tiếp cận khác: thay vì chọn các feature gốc, tạo ra một không gian biểu diễn có số chiều thấp hơn.

Do đó, Wrapper Methods là **tầng trung gian giữa statistical screening và model-integrated selection**, giúp đánh giá giá trị của feature subset trực tiếp theo mục tiêu dự báo nhưng phải đánh đổi bằng chi phí tính toán và nguy cơ overfitting trong quá trình selection.
