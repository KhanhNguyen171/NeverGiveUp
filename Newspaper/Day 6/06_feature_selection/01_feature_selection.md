# 01. Feature Selection

## 1. Khái niệm Feature Selection

**Feature Selection** là quá trình lựa chọn một tập con các đặc trưng từ tập dữ liệu ban đầu nhằm giữ lại những biến có thông tin hữu ích đối với nhiệm vụ phân tích hoặc dự báo, đồng thời loại bỏ các đặc trưng dư thừa, không liên quan hoặc gây nhiễu.

Với tập đặc trưng ban đầu:

$$X={x_1,x_2,\ldots,x_p}$$

Feature Selection tìm một tập con:

$$X^*\subseteq X$$

sao cho:

$$|X^*|<|X|$$

nhưng vẫn duy trì hoặc cải thiện hiệu quả của mô hình đối với mục tiêu $Y$.

Khác với **Dimensionality Reduction**, Feature Selection giữ nguyên các đặc trưng được chọn và loại bỏ các đặc trưng không cần thiết. Ngược lại, dimensionality reduction tạo ra các biến mới từ tổ hợp của các biến ban đầu.

Ví dụ:

```text
Original Features
      │
      ├── x1 ───────────► Selected
      ├── x2 ───────────► Removed
      ├── x3 ───────────► Selected
      ├── x4 ───────────► Removed
      └── x5 ───────────► Selected
              │
              ▼
       Selected Feature Set
          {x1, x3, x5}
```

---

## 2. Vai trò của Feature Selection trong Preprocessing

Feature Selection nằm sau **Data Cleaning**, **Data Transformation** và **Feature Engineering** trong pipeline nghiên cứu.

```text
Data Cleaning
      │
      ▼
Data Transformation
      │
      ▼
Feature Engineering
      │
      ▼
Feature Selection
      │
      ├── Filter Methods
      ├── Wrapper Methods
      ├── Embedded Methods
      └── Dimensionality Reduction
      │
      ▼
AI-ready Data
```

Các chương trước tập trung vào việc **làm sạch và xây dựng biểu diễn dữ liệu**, trong khi Feature Selection tập trung vào câu hỏi:

> Trong các đặc trưng đã tạo ra, đặc trưng nào thực sự cần thiết cho nhiệm vụ downstream?

Điều này đặc biệt quan trọng đối với dữ liệu chuỗi thời gian vì Feature Engineering có thể tạo ra số lượng lớn đặc trưng từ:

* temporal information;
* lag values;
* rolling statistics;
* trend;
* seasonal components;
* sensor measurements;
* interaction features.

Nếu giữ toàn bộ các đặc trưng, tập dữ liệu có thể trở nên dư thừa và làm tăng độ phức tạp của mô hình.

---

## 3. Mục tiêu của Feature Selection

Feature Selection có bốn mục tiêu chính.

### 3.1. Loại bỏ đặc trưng không liên quan

Một feature không có quan hệ hữu ích với target có thể làm tăng không gian tìm kiếm của mô hình mà không cung cấp thông tin dự báo.

Ví dụ:

$$I(X_j;Y)\approx0$$

với $I$ là mutual information, cho thấy feature $X_j$ chứa rất ít thông tin về $Y$.

---

### 3.2. Loại bỏ đặc trưng dư thừa

Hai hoặc nhiều features có thể chứa thông tin gần như giống nhau.

Ví dụ:

$$corr(X_1,X_2)\approx1$$

Nếu $X_1$ và $X_2$ cung cấp thông tin tương đương, việc giữ cả hai có thể không cần thiết.

Do đó Feature Selection không chỉ tìm feature **relevant**, mà còn phải xem xét **redundancy**.

Một tập feature tốt có thể được mô tả khái quát:

$$\text{Useful Features}=\text{Relevance}-\text{Redundancy}$$

---

### 3.3. Giảm độ phức tạp

Với $p$ features, mô hình phải xử lý vector:

$$X\in\mathbb{R}^{p}$$

Sau Feature Selection:

$$X^*\in\mathbb{R}^{k},\quad k<p$$

Việc giảm từ $p$ xuống $k$ features có thể làm giảm:

* computational cost;
* memory usage;
* training time;
* inference time;
* độ phức tạp của mô hình.

---

### 3.4. Giảm nguy cơ overfitting

Các đặc trưng không liên quan hoặc quá dư thừa có thể làm mô hình học các pattern không mang tính tổng quát.

Feature Selection có thể giúp giới hạn không gian hypothesis:

$$\mathcal{H}(X^*)\subseteq\mathcal{H}(X)$$

Tuy nhiên, Feature Selection **không đảm bảo tự động loại bỏ overfitting**. Nếu quá trình selection sử dụng validation/test information không đúng cách, chính bước selection cũng có thể gây data leakage và tạo ra đánh giá quá lạc quan.

---

# 4. Feature Relevance và Feature Redundancy

Một Feature Selection strategy cần xem xét đồng thời hai thuộc tính:

### Relevance

Feature có liên quan đến target:

$$X_j\rightarrow Y$$

Có thể đánh giá bằng:

* correlation;
* mutual information;
* statistical tests;
* model-based importance.

### Redundancy

Feature chứa thông tin trùng lặp với các feature khác:

$$X_i\approx f(X_j)$$

Một feature có relevance cao nhưng redundancy rất cao vẫn có thể không cần thiết.

Do đó, lựa chọn feature không nên chỉ dựa trên ranking độc lập của từng biến.

---

# 5. Feature Selection và Time Series

Feature Selection đối với time series có những đặc điểm khác so với dữ liệu IID thông thường.

Các features có thể chứa quan hệ thời gian:

$$X_t,X_{t-1},X_{t-2},\ldots,X_{t-L}$$

Trong đó các lag gần nhau thường có tương quan cao.

Ví dụ:

```text
Target: Appliances_t

Lag Features
    │
    ├── Appliances_{t-1}
    ├── Appliances_{t-2}
    ├── Appliances_{t-3}
    ├── ...
    └── Appliances_{t-L}
```

Các lag này có thể vừa **relevant** vừa **redundant**.

Ngoài ra, temporal features có thể biểu diễn cùng một cấu trúc dưới nhiều dạng:

```text
Hour
 ├── hour
 ├── hour_sin
 └── hour_cos

Day
 ├── day_of_week
 ├── dow_sin
 └── dow_cos
```

Vì vậy, Feature Selection trong time series phải bảo đảm rằng việc loại bỏ feature không phá vỡ cấu trúc temporal cần thiết cho forecasting.

---

# 6. Feature Selection và Data Leakage

Đây là một trong những nguyên tắc quan trọng nhất của chương.

Feature Selection phải được **fit trên training data**, không được sử dụng test data để quyết định feature nào được giữ lại.

Pipeline đúng:

```text
Full Dataset
     │
     ▼
Chronological Split
     │
     ├── Train ──► Fit Feature Selection
     │                  │
     │                  ▼
     │             Selected Features
     │
     ├── Validation ──► Transform
     │
     └── Test ────────► Transform
```

Không được thực hiện:

```text
Full Dataset
     │
     ▼
Feature Selection
     │
     ▼
Train / Validation / Test
```

vì thông tin từ validation/test có thể ảnh hưởng đến quyết định lựa chọn feature.

Ví dụ, nếu correlation giữa feature và target được tính trên toàn bộ dataset:

$$corr(X_j,Y)_{\text{all}}$$

thì thống kê này đã sử dụng thông tin từ validation và test.

Thay vào đó:

$$corr(X_j,Y)_{\text{train}}$$

phải được sử dụng để quyết định feature.

Nguyên tắc này kế thừa trực tiếp từ các quy định về **train-only fitting** trong Chương 4.

---

# 7. Feature Selection và Feature Engineering

Feature Selection không thay thế Feature Engineering mà hoạt động **sau Feature Engineering**.

Quan hệ giữa hai bước:

```text
Raw Features
     │
     ▼
Feature Engineering
     │
     ├── Temporal Features
     ├── Lag Features
     ├── Rolling Features
     └── Feature Representation
     │
     ▼
Candidate Feature Set
     │
     ▼
Feature Selection
     │
     ▼
Final Feature Set
```

Feature Engineering mở rộng không gian đặc trưng:

$$X\rightarrow X_{candidate}$$

Feature Selection thu hẹp không gian đó:

$$X_{candidate}\rightarrow X^*$$

Do đó, hai quá trình có vai trò bổ sung:

> **Feature Engineering tạo ra khả năng biểu diễn; Feature Selection xác định biểu diễn nào cần được giữ lại.**

---

# 8. Các nhóm phương pháp Feature Selection

Feature Selection trong nghiên cứu được chia thành ba nhóm chính:

```text
                 Feature Selection
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       Filter        Wrapper       Embedded
          │             │             │
          ▼             ▼             ▼
   Statistical      Model-based    During Training
     Criteria        Search          Selection
```

Ngoài ba nhóm trên, **Dimensionality Reduction** được trình bày riêng trong:

`05_dimensionality_reduction.md`

Các phương pháp cụ thể được triển khai trong các mục tiếp theo:

* `02_filter_methods.md`
* `03_wrapper_methods.md`
* `04_embedded_methods.md`
* `05_dimensionality_reduction.md`

Mục hiện tại chỉ xác định **khung khái niệm và nguyên tắc lựa chọn**, tránh trùng lặp với phần phương pháp chi tiết.

---

# 9. So sánh ba nhóm phương pháp

| Tiêu chí            | Filter          | Wrapper | Embedded               |
| ------------------- | --------------- | ------- | ---------------------- |
| Dựa trên model      | Không           | Có      | Có                     |
| Tốc độ              | Nhanh           | Chậm    | Trung bình             |
| Chi phí tính toán   | Thấp            | Cao     | Trung bình             |
| Xem xét interaction | Hạn chế         | Có      | Có                     |
| Phụ thuộc model     | Thấp            | Cao     | Cao                    |
| Khả năng mở rộng    | Tốt             | Hạn chế | Tốt                    |
| Ví dụ               | Correlation, MI | RFE     | LASSO, Tree Importance |

Không có phương pháp nào luôn vượt trội.

Lựa chọn phụ thuộc vào:

$$\text{Method} = f(\text{Dataset},\text{Task},\text{Model},\text{Cost})$$

---

# 10. Tiêu chí lựa chọn Feature Selection Method

Việc lựa chọn phương pháp cần dựa trên các yếu tố sau.

### 10.1. Kích thước dữ liệu

Với số lượng features lớn, Filter Methods thường phù hợp để loại bỏ nhanh các biến rõ ràng không liên quan trước khi áp dụng các phương pháp đắt hơn.

### 10.2. Loại quan hệ giữa feature và target

Nếu quan hệ chủ yếu tuyến tính, correlation có thể hữu ích.

Nếu quan hệ phi tuyến, mutual information hoặc model-based methods có thể phù hợp hơn.

### 10.3. Mô hình downstream

Nếu feature selection phụ thuộc vào model, cần xem xét sự tương thích giữa selection method và mô hình cuối cùng.

### 10.4. Interpretability

Trong các nghiên cứu cần giải thích mô hình, giữ lại các feature có ý nghĩa vật lý hoặc nghiệp vụ thường quan trọng hơn việc chỉ tối ưu số lượng feature.

### 10.5. Temporal structure

Với time series, cần bảo đảm feature selection không phá vỡ:

* lag dependency;
* seasonal dependency;
* temporal ordering;
* causal availability.

---

# 11. Feature Selection như một bài toán tối ưu

Feature Selection có thể được biểu diễn dưới dạng bài toán tìm subset:

$$X^*=\arg\min_{X'\subseteq X}\mathcal{L}(X')$$

với $\mathcal{L}$ là loss hoặc một objective đánh giá chất lượng của subset.

Một formulation tổng quát hơn có thể cân bằng hiệu năng và số lượng features:

$$X^*=\arg\min_{X'\subseteq X}\left[\mathcal{L}(X')+\lambda|X'|\right]$$

Trong đó:

* $\mathcal{L}(X')$: prediction loss;
* $|X'|$: số lượng features;
* $\lambda$: mức phạt đối với feature complexity.

Khi $\lambda$ tăng, objective ưu tiên subset nhỏ hơn.

Điều này thể hiện bản chất của Feature Selection:

> Không chỉ tìm tập feature cho prediction tốt, mà tìm **tập feature đủ tốt với độ phức tạp hợp lý**.

---

# 12. Đánh giá Feature Selection

Feature Selection không nên được đánh giá chỉ bằng số lượng features bị loại bỏ.

Cần đánh giá ít nhất:

1. **Predictive performance**

   * MAE;
   * RMSE;
   * $R^2$;
   * hoặc metric phù hợp với task.

2. **Feature reduction**

$$Reduction=\frac{p-k}{p}\times100%$$

3. **Computational cost**

   * training time;
   * inference time;
   * memory.

4. **Stability**

Một feature selection method tốt nên tạo ra subset tương đối ổn định khi dữ liệu training thay đổi hợp lý.

5. **Interpretability**

Feature được giữ lại cần có khả năng giải thích đối với domain nếu nghiên cứu yêu cầu.

---

# 13. Quy trình Feature Selection trong nghiên cứu

Quy trình tổng quát:

```text
Feature Engineering
        │
        ▼
Candidate Features
        │
        ▼
Check Data Quality
        │
        ▼
Remove Invalid / Constant Features
        │
        ▼
Filter Methods
        │
        ▼
Redundancy Analysis
        │
        ▼
Wrapper / Embedded Methods
        │
        ▼
Final Feature Set
        │
        ▼
Train Model
        │
        ▼
Evaluate on Validation
        │
        ▼
Locked Test Evaluation
```

Các phương pháp cụ thể trong quy trình này sẽ được trình bày ở các mục tiếp theo thay vì lặp lại trong mục tổng quan.

---

# 14. Nguyên tắc thực hiện

Để bảo đảm Feature Selection nhất quán với toàn bộ pipeline nghiên cứu, các nguyên tắc sau được áp dụng:

* Feature Selection được thực hiện **sau Feature Engineering**.
* Quyết định lựa chọn feature chỉ được học từ **training data**.
* Validation được sử dụng để đánh giá lựa chọn hoặc so sánh configuration, không dùng như một phần của training feature-selection statistics nếu pipeline yêu cầu giữ validation độc lập.
* Test set được giữ độc lập cho đánh giá cuối cùng.
* Không lựa chọn feature chỉ dựa trên correlation nếu quan hệ giữa feature và target có thể phi tuyến.
* Cần phân biệt **feature relevance** và **feature redundancy**.
* Không loại bỏ feature chỉ vì correlation thấp nếu feature có thể chứa quan hệ phi tuyến hoặc temporal information.
* Với time series, phải bảo toàn temporal ordering và tránh future leakage.
* Feature Selection phải được đánh giá bằng hiệu năng downstream, không chỉ bằng số lượng feature giảm.
* Không coi Dimensionality Reduction là Feature Selection thuần túy; hai nhóm được trình bày riêng vì chúng tạo ra biểu diễn dữ liệu khác nhau.

---

# 15. Liên kết với các mục tiếp theo

Mục này thiết lập framework chung cho Chương 6. Các phương pháp cụ thể được triển khai theo thứ tự:

```text
06_feature_selection/
│
├── 01_feature_selection.md
│       │
│       ├── Khái niệm
│       ├── Mục tiêu
│       ├── Relevance / Redundancy
│       └── Framework lựa chọn
│
├── 02_filter_methods.md
│       │
│       └── Statistical / model-independent selection
│
├── 03_wrapper_methods.md
│       │
│       └── Model-based subset search
│
├── 04_embedded_methods.md
│       │
│       └── Selection integrated into model training
│
└── 05_dimensionality_reduction.md
        │
        └── Transformation into lower-dimensional representation
```

Như vậy, **01_feature_selection.md** đóng vai trò định nghĩa vấn đề và nguyên tắc chung; ba mục tiếp theo trình bày các nhóm phương pháp lựa chọn feature; mục cuối phân biệt Feature Selection với Dimensionality Reduction và phân tích các phương pháp giảm chiều.

Sau Chương 6, tập feature đã được kiểm soát về **relevance, redundancy và dimensionality**, tạo đầu vào phù hợp cho **Chương 7 — Sensor Fusion**, nơi các nguồn dữ liệu hoặc cảm biến khác nhau được kết hợp và căn chỉnh theo thời gian.
