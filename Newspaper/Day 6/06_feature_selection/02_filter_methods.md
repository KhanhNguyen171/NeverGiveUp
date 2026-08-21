# 02. Filter Methods

## 1. Khái niệm

**Filter Methods** là nhóm phương pháp Feature Selection đánh giá đặc trưng dựa trên các thuộc tính thống kê của dữ liệu mà **không phụ thuộc trực tiếp vào mô hình học máy downstream**.

Với tập đặc trưng:

$$X={X_1,X_2,\ldots,X_p}$$

và target $Y$, Filter Methods tính một **score** cho từng feature:

$$S_j=f(X_j,Y)$$

Sau đó lựa chọn các feature có score phù hợp với tiêu chí đã xác định:

$$X^*={X_j:S_j\geq\tau}$$

hoặc chọn $k$ features có score cao nhất:

$$X^*=\operatorname{TopK}(S_1,S_2,\ldots,S_p)$$

Điểm quan trọng của Filter Methods là quá trình lựa chọn được thực hiện **trước và độc lập với quá trình huấn luyện mô hình**.

Do đó, phương pháp này thường có chi phí tính toán thấp và phù hợp để xử lý tập dữ liệu có số lượng features lớn.

---

## 2. Vị trí trong Feature Selection Pipeline

Trong Chương 6, Filter Methods được đặt sau phần khái niệm tổng quát ở `01_feature_selection.md` và trước Wrapper Methods, Embedded Methods.

```text id="6b5b3a"
Feature Engineering
        │
        ▼
Candidate Feature Set
        │
        ▼
01 Feature Selection
        │
        ▼
02 Filter Methods
        │
        ├── Correlation
        ├── Statistical Tests
        ├── Mutual Information
        └── Other Relevance Scores
        │
        ▼
Reduced Candidate Set
        │
        ├───────────────┐
        ▼               ▼
03 Wrapper        04 Embedded
        │               │
        └───────┬───────┘
                ▼
      Final Feature Set
                │
                ▼
05 Dimensionality Reduction
```

Trong pipeline này, Filter Methods có thể được sử dụng như **bước sàng lọc ban đầu** trước các phương pháp có chi phí tính toán cao hơn.

Tuy nhiên, Filter Methods không nhất thiết phải luôn đứng đầu toàn bộ pipeline. Thứ tự thực tế phụ thuộc vào loại dữ liệu và mục tiêu nghiên cứu.

---

# 3. Đặc điểm của Filter Methods

Filter Methods có ba đặc điểm chính.

### 3.1. Model-independent

Feature được đánh giá dựa trên dữ liệu:

$$X_j\rightarrow Y$$

thay vì dựa trên performance của một mô hình cụ thể.

Do đó, cùng một Filter Method có thể được sử dụng trước nhiều mô hình khác nhau.

---

### 3.2. Chi phí tính toán thấp

Phần lớn các phương pháp thực hiện phép tính riêng hoặc gần riêng cho từng feature:

$$S_j=f(X_j,Y),\quad j=1,\ldots,p$$

Vì vậy chúng thường có khả năng mở rộng tốt khi $p$ lớn.

---

### 3.3. Không trực tiếp tối ưu prediction performance

Một feature có statistical score cao chưa chắc giúp mô hình cuối cùng đạt hiệu năng cao nhất.

Điều này xảy ra vì Filter Methods thường đánh giá:

$$X_j\leftrightarrow Y$$

trong khi mô hình thực tế có thể khai thác:

$$f(X_1,X_2,\ldots,X_p)\rightarrow Y$$

Do đó Filter Methods chủ yếu đo **relevance**, trong khi interaction giữa nhiều features có thể chưa được phản ánh đầy đủ.

---

# 4. Correlation-based Selection

Correlation là một trong những Filter Methods phổ biến nhất đối với dữ liệu số.

## 4.1. Pearson Correlation

Pearson correlation đo mức độ quan hệ tuyến tính giữa feature $X$ và target $Y$:

$$r_{XY}=\frac{\operatorname{Cov}(X,Y)}{\sigma_X\sigma_Y}$$

với:

$$-1\leq r_{XY}\leq1$$

Giá trị $|r_{XY}|$ càng lớn thì quan hệ tuyến tính càng mạnh.

Có thể sử dụng ngưỡng:

$$|r_{XY}|\geq\tau$$

để giữ lại feature.

Ví dụ:

```text id="r4b8i0"
Feature       |r|       Decision
--------------------------------
X1            0.82      Keep
X2            0.07      Remove
X3            0.64      Keep
X4            0.03      Remove
```

Tuy nhiên, correlation thấp **không đồng nghĩa** với feature không có predictive information.

Ví dụ một quan hệ phi tuyến:

$$Y=X^2$$

có thể có Pearson correlation gần bằng 0 trong một số phân phối đối xứng, mặc dù $X$ hoàn toàn xác định $Y$.

---

## 4.2. Spearman Correlation

Spearman correlation dựa trên **rank** của dữ liệu thay vì giá trị gốc.

Nó phù hợp hơn khi quan hệ giữa hai biến mang tính **monotonic** nhưng không nhất thiết tuyến tính.

Có thể biểu diễn:

$$\rho_s=\operatorname{corr}(\operatorname{rank}(X),\operatorname{rank}(Y))$$

So với Pearson:

| Method             | Quan hệ phát hiện  |
| ------------------ | ------------------ |
| Pearson            | Linear             |
| Spearman           | Monotonic          |
| Mutual Information | General dependency |

Do đó, Spearman có thể bổ sung cho Pearson khi dữ liệu không đáp ứng tốt giả định tuyến tính.

---

# 5. Correlation giữa các Features

Correlation không chỉ được sử dụng giữa feature và target.

Nó còn được sử dụng để phát hiện **feature redundancy**:

$$corr(X_i,X_j)\rightarrow1$$

hoặc:

$$|corr(X_i,X_j)|\geq\tau_{red}$$

Nếu hai features có correlation rất cao, một trong chúng có thể được loại bỏ tùy theo:

* interpretability;
* domain meaning;
* missingness;
* stability;
* relationship với target.

Ví dụ:

```text id="nq2l9g"
X1 ──────────────► Y
 │
 │ high correlation
 ▼
X2 ──────────────► Y

X1 ≈ X2
```

Không nên giữ cả hai chỉ vì cả hai đều có relevance cao nếu chúng cung cấp gần như cùng một thông tin.

Điều này liên kết trực tiếp với nguyên tắc **relevance + redundancy** đã được xác định trong `01_feature_selection.md`.

---

# 6. Statistical Tests

Một nhóm Filter Methods khác sử dụng kiểm định thống kê để đánh giá sự phụ thuộc giữa feature và target.

Phương pháp được lựa chọn tùy thuộc vào loại biến.

### 6.1. Numerical Feature

Với numerical feature và target, có thể sử dụng các kiểm định hoặc thống kê phù hợp với giả định phân phối và loại bài toán.

### 6.2. Categorical Feature

Với categorical feature, có thể sử dụng **Chi-square test** để kiểm tra sự phụ thuộc giữa feature và target categorical.

Giả thuyết:

$$H_0:X\perp Y$$

$$H_1:X\not\perp Y$$

Nếu:

$$p\text{-value}<\alpha$$

thì bác bỏ $H_0$ và xem feature có bằng chứng thống kê về sự phụ thuộc với target.

Tuy nhiên, **statistical significance không đồng nghĩa với predictive usefulness**. Với dataset rất lớn, một hiệu ứng rất nhỏ cũng có thể tạo ra $p$-value rất nhỏ.

Do đó, p-value không nên được sử dụng như tiêu chí duy nhất.

---

# 7. Mutual Information

**Mutual Information (MI)** đo lượng thông tin mà một biến chứa về biến khác.

Đối với feature $X$ và target $Y$:

$$I(X;Y)=\sum_{x,y}p(x,y)\log\frac{p(x,y)}{p(x)p(y)}$$

Đối với biến liên tục, MI được biểu diễn dưới dạng entropy:

$$I(X;Y)=H(X)-H(X|Y)$$

Nếu:

$$I(X;Y)=0$$

thì $X$ và $Y$ độc lập về mặt thống kê.

MI có ưu điểm quan trọng so với Pearson correlation:

> Nó có thể phát hiện các quan hệ phi tuyến mà correlation không phản ánh được.

Ví dụ:

$$Y=X^2$$

có thể có:

$$corr(X,Y)\approx0$$

nhưng:

$$I(X;Y)>0$$

Do đó MI đặc biệt hữu ích khi quan hệ giữa feature và target không được giả định là tuyến tính.

---

# 8. Variance Threshold

**Variance Threshold** loại bỏ các feature có variance quá thấp.

Với feature $X_j$:

$$Var(X_j)<\tau$$

thì feature có thể được loại bỏ.

Ví dụ:

```text id="m15x0u"
Feature X1:
[1, 1, 1, 1, 1, 1]
Var(X1) = 0
       │
       ▼
    Remove
```

Phương pháp này không sử dụng target:

$$S_j=Var(X_j)$$

Do đó nó chỉ phát hiện các feature gần như constant, không trực tiếp đánh giá predictive relevance.

Variance Threshold phù hợp như một bước preprocessing đơn giản trước các phương pháp Feature Selection khác.

---

# 9. Univariate Feature Selection

Các Filter Methods có thể được tổ chức thành **univariate selection**, trong đó từng feature được đánh giá độc lập:

$$S_j=f(X_j,Y)$$

Sau đó:

$$X^*=\operatorname{TopK}(S_j)$$

Ưu điểm:

* đơn giản;
* nhanh;
* dễ mở rộng;
* dễ diễn giải.

Nhược điểm:

* không trực tiếp xem xét interaction;
* có thể giữ nhiều feature redundant;
* có thể bỏ qua feature chỉ hữu ích khi kết hợp với feature khác.

Ví dụ:

$$Y=X_1\oplus X_2$$

Trong trường hợp này, từng feature riêng lẻ có thể không thể hiện relevance mạnh, nhưng cặp $(X_1,X_2)$ lại có predictive information.

Do đó univariate Filter Methods không thể thay thế hoàn toàn Wrapper hoặc Embedded Methods.

---

# 10. Feature Selection cho Time Series

Trong time series, Filter Methods phải được áp dụng thận trọng vì các quan sát không độc lập theo thời gian.

Ví dụ với lag features:

$$X_{t-1},X_{t-2},\ldots,X_{t-L}$$

ta có thể tính:

$$corr(X_{t-k},Y_t)$$

để đánh giá relevance của từng lag.

Kết quả có thể tạo ra một profile:

```text id="l2r4k6"
Correlation
    │
1.0 ┤ ●
    │   ●
0.5 ┤      ●
    │         ●
0.0 ┤             ●────
    └───────────────────► Lag
       1  2  3  4  ... L
```

Điều này có thể hỗ trợ xác định các lag quan trọng.

Tuy nhiên, correlation giữa lag và target phải được tính **chỉ trên training period** trong bài toán forecasting.

Không được sử dụng toàn bộ chuỗi trước khi chronological split.

---

# 11. Filter Methods và Temporal Leakage

Đối với time series, quy tắc quan trọng là:

$$\boxed{\text{Fit Filter Selection on Training Data Only}}$$

Pipeline đúng:

```text id="c2e5qj"
Chronological Split
       │
       ├── Train
       │     │
       │     ▼
       │  Calculate Score
       │     │
       │     ▼
       │  Select Features
       │
       ├── Validation
       │     │
       │     ▼
       │  Apply Selected Set
       │
       └── Test
             │
             ▼
        Apply Selected Set
```

Ví dụ với correlation:

$$r_j^{train}=corr(X_j^{train},Y^{train})$$

Không được dùng:

$$r_j^{all}=corr(X_j^{all},Y^{all})$$

để quyết định feature selection.

Đây là nguyên tắc kế thừa từ **03_stationarity.md** và toàn bộ quy định về chronological processing của nghiên cứu.

---

# 12. Ưu điểm

Filter Methods có các ưu điểm chính:

### 12.1. Nhanh

Không cần train model cho từng subset feature:

$$Cost_{filter}\ll Cost_{wrapper}$$

trong nhiều trường hợp.

### 12.2. Model-independent

Một bộ feature được chọn có thể sử dụng cho nhiều mô hình.

### 12.3. Khả năng mở rộng

Phù hợp với dataset có hàng trăm, hàng nghìn hoặc nhiều hơn features.

### 12.4. Dễ kiểm tra

Score của từng feature có thể được lưu và phân tích trực tiếp.

---

# 13. Hạn chế

### 13.1. Không tối ưu trực tiếp cho model

Feature có score cao chưa chắc tạo ra performance tốt nhất.

### 13.2. Khó phát hiện interaction

Univariate score không phản ánh đầy đủ quan hệ:

$$f(X_i,X_j)\rightarrow Y$$

### 13.3. Có thể giữ feature redundant

Nếu $X_1$ và $X_2$ đều có relevance cao:

$$I(X_1;Y)\gg0$$

$$I(X_2;Y)\gg0$$

nhưng:

$$I(X_1;X_2)\gg0$$

thì ranking độc lập có thể giữ cả hai.

### 13.4. Phụ thuộc vào statistical assumptions

Một số statistical tests yêu cầu điều kiện nhất định về phân phối, independence hoặc loại biến.

Do đó kết quả cần được diễn giải trong bối cảnh của dataset.

---

# 14. Quy trình áp dụng

Filter Methods trong pipeline có thể được triển khai theo các bước:

```text id="r8qz3d"
Candidate Features
       │
       ▼
Remove Constant / Near-constant Features
       │
       ▼
Check Feature-Target Relevance
       │
       ├── Pearson / Spearman
       ├── Statistical Tests
       └── Mutual Information
       │
       ▼
Check Feature-Feature Redundancy
       │
       ▼
Select Candidate Subset
       │
       ▼
Validation
       │
       ▼
Wrapper / Embedded Selection
```

Mục tiêu của bước này là **thu hẹp không gian feature**, không nhất thiết phải tạo ra final feature set ngay lập tức.

---

# 15. Tiêu chí lựa chọn phương pháp

| Trường hợp                 | Phương pháp phù hợp               |
| -------------------------- | --------------------------------- |
| Feature gần constant       | Variance Threshold                |
| Quan hệ tuyến tính         | Pearson                           |
| Quan hệ monotonic          | Spearman                          |
| Quan hệ phi tuyến          | Mutual Information                |
| Categorical dependency     | Chi-square / statistical test     |
| Feature redundancy         | Correlation / dependency analysis |
| Dataset rất nhiều features | Filter Methods                    |
| Cần xét interaction        | Wrapper / Embedded                |

Có thể kết hợp nhiều Filter Methods thay vì phụ thuộc vào một score duy nhất.

Ví dụ:

$$Score(X_j)=f(\text{MI},|\rho|,\text{variance})$$

Tuy nhiên, cách kết hợp phải được xác định trước và đánh giá trên validation data để tránh lựa chọn tùy ý.

---

# 16. Đánh giá Filter Selection

Sau khi chọn feature, cần kiểm tra:

### Feature reduction

$$R=\frac{p-k}{p}\times100%$$

### Predictive performance

So sánh mô hình sử dụng:

$$X$$

với mô hình sử dụng:

$$X^*$$

Các metric phải được giữ nhất quán với **09_empirical_analysis/04_evaluation_metrics.md**.

Đối với forecasting, cần đặc biệt xem xét:

* MAE;
* RMSE;
* $R^2$.

Nếu giảm đáng kể số lượng features nhưng performance validation suy giảm mạnh, ngưỡng selection có thể quá nghiêm ngặt.

Ngược lại, nếu giảm nhiều features mà performance gần như không thay đổi, các features bị loại có khả năng chứa thông tin dư thừa hoặc đóng góp thấp.

---

# 17. Kết nối với Wrapper và Embedded Methods

Filter Methods tạo ra **candidate subset** cho các phương pháp tiếp theo:

```text id="j5m0w8"
Filter
  │
  │ Fast screening
  ▼
Candidate Subset
  │
  ├───────────────┐
  ▼               ▼
Wrapper        Embedded
  │               │
  └───────┬───────┘
          ▼
   Final Evaluation
```

Sự khác biệt cốt lõi:

* **Filter:** đánh giá feature độc lập với model.
* **Wrapper:** đánh giá subset dựa trên performance của model.
* **Embedded:** thực hiện selection ngay trong quá trình training.

Vì vậy, Filter Methods thường phù hợp để **sàng lọc ban đầu**, trong khi `03_wrapper_methods.md` sẽ tập trung vào việc tìm subset thông qua quá trình huấn luyện và đánh giá mô hình.

---

# 18. Nguyên tắc tổng quát

Filter Methods trong nghiên cứu được áp dụng theo các nguyên tắc:

1. **Training-only:** mọi statistical score dùng cho selection phải được tính từ training data.
2. **Relevance:** đánh giá quan hệ giữa feature và target.
3. **Redundancy:** kiểm tra sự trùng lặp giữa các features.
4. **Method matching:** lựa chọn statistical criterion phù hợp với loại dữ liệu và dạng quan hệ.
5. **No single-score assumption:** không coi một statistical measure là bằng chứng đầy đủ về predictive usefulness.
6. **Temporal awareness:** giữ nguyên thứ tự thời gian và không sử dụng future information.
7. **Validation-based evaluation:** đánh giá subset bằng downstream performance trên validation.
8. **Test isolation:** test set chỉ được sử dụng cho đánh giá cuối cùng.
9. **Interpretability:** ưu tiên feature có ý nghĩa domain khi các lựa chọn có performance tương đương.

Như vậy, **Filter Methods là tầng sàng lọc thống kê trong Feature Selection pipeline**. Phương pháp này giúp giảm nhanh các feature không liên quan, constant hoặc dư thừa trước khi chuyển sang các phương pháp có tính model-dependent cao hơn. Trên cơ sở candidate subset này, **03_wrapper_methods.md** sẽ tiếp tục xem xét việc lựa chọn feature thông qua trực tiếp performance của mô hình.
