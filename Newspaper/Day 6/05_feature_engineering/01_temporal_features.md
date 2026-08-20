Có một điểm **rất quan trọng để tránh hallucination**: paper **không có một mục riêng gọi là “Temporal Features” và cũng không đề xuất một bộ temporal-feature engineering như hour/day/week/month, sine/cosine, lag features...**. Trong phần *Feature Engineering*, tác giả định nghĩa feature engineering gồm **feature reduction, transformation và synthesis**, sau đó khảo sát chủ yếu **discretization** và **feature selection**. Khi nói về discretization, tác giả nhấn mạnh rằng các phương pháp thông thường có thể **bỏ qua tính temporal**, và dẫn các phương pháp dành riêng cho time series như SAX, MINIONS và temporal discretization. ([research.chalmers.se][2])

# 01. Temporal Features

## 1. Tổng quan

Trong Time-Series Data, mỗi observation không chỉ mang giá trị của feature mà còn gắn với một vị trí trong trục thời gian.

Có thể biểu diễn một observation dưới dạng:

$$
(x_t,t)
$$

trong đó:

- $x_t$ là giá trị quan sát tại thời điểm $t$.
- $t$ là thông tin về thời gian của observation.

Do đó, preprocessing cho time-series data có một đặc điểm khác biệt so với dữ liệu tabular thông thường:

> Thứ tự và quan hệ theo thời gian có thể chứa thông tin quan trọng đối với downstream task.

Paper nhấn mạnh phạm vi nghiên cứu vào **numerical time-series data** và xây dựng một taxonomy preprocessing rộng, không chỉ giới hạn ở data cleaning mà còn bao gồm feature engineering, sensor fusion và data compression.

Trong taxonomy của paper, Feature Engineering được định nghĩa rộng hơn việc tạo các biến thời gian đơn thuần. Tác giả chia feature engineering thành:

```text
Feature Engineering
│
├── Feature Reduction
├── Feature Transformation
└── Feature Synthesis
```

Do đó, khi đọc phần này cần phân biệt:

* **Temporal information**: thông tin phát sinh từ trục thời gian.
* **Temporal feature engineering**: tạo hoặc biến đổi feature dựa trên cấu trúc thời gian.
* **Time-series-specific preprocessing**: các preprocessing method được thiết kế để không làm mất temporal structure.

Paper chủ yếu tập trung vào vấn đề thứ ba trong phần feature engineering, đặc biệt thông qua **time-series discretization**.

---

# 2. Tại sao Temporal Structure quan trọng?

Time-series data không phải là tập hợp các observation độc lập.

Một sequence có dạng:

$$
X={x_1,x_2,\ldots,x_t,\ldots,x_n}
$$

trong đó thứ tự:

$$
x_1 \rightarrow x_2 \rightarrow \cdots \rightarrow x_n
$$

có ý nghĩa.

Nếu preprocessing phá vỡ thứ tự này, dữ liệu sau preprocessing có thể không còn phản ánh đúng quá trình sinh dữ liệu ban đầu.

Ví dụ:

```text
Original

t1 → t2 → t3 → t4 → t5
10   11   12   15   14
```

Nếu xử lý như dữ liệu tabular độc lập:

```text
12, 10, 14, 11, 15
```

thì distribution có thể vẫn giống nhau nhưng temporal structure đã bị thay đổi.

Điều này đặc biệt quan trọng với các downstream models học từ:

* temporal dependency;
* trend;
* sequence;
* local temporal patterns;
* long-term dependency.

Vì vậy:

$$
\boxed{
Time-Series\ Preprocessing
\neq
Generic\ Tabular\ Preprocessing
}
$$

---

# 3. Temporal Information trong Feature Engineering

Paper định nghĩa Feature Engineering theo phạm vi rộng:

> Feature engineering bao gồm feature reduction, transformation và synthesis, với mục tiêu tạo ra các feature phù hợp nhất với dữ liệu, model và task.

Điểm quan trọng ở đây là:

$$
\text{Feature Quality}=

f(\text{Data},\text{Model},\text{Task})
$$

Do đó không tồn tại một feature representation luôn tốt cho mọi time-series problem.

Một feature có thể:

```text
Tốt cho Model A
      ↓
Không nhất thiết tốt cho Model B
```

hoặc:

```text
Tốt cho Forecasting
      ↓
Không nhất thiết tốt cho Classification
```

---

# 4. Paper có đề xuất Temporal Feature Engineering riêng không?

## Không.

Đây là điểm cần ghi nhớ để tránh hiểu sai paper.

Paper không xây dựng một taxonomy riêng cho:

```text
Hour
Day
Week
Month
Season
Holiday
Lag
Rolling Mean
Rolling Std
Sin/Cos Time Encoding
```

và cũng không đề xuất một thuật toán riêng để tạo những feature này.

Thay vào đó, paper tập trung vào các preprocessing techniques có thể áp dụng cho numerical time-series data và trong phần Feature Engineering khảo sát:

```text
Feature Engineering
│
├── Discretization
│
├── Feature Reduction
│
├── Feature Transformation
└── Feature Selection
```

Trong đó phần được mô tả chi tiết nhất trong context liên quan tới temporal structure là **Discretization**.

---

# 5. Discretization và Temporal Structure

Discretization là quá trình biến đổi continuous feature thành các giá trị discrete.

Có thể biểu diễn:

$$
x\in\mathbb{R}
\rightarrow
x'\in\{b_1,b_2,\ldots,b_k\}
$$

Trong đó:

* $x$ là continuous value.
* $b_i$ là một discrete interval/bin.
* $k$ là số interval.

Mục tiêu là tóm tắt dữ liệu thành các khoảng giá trị trong khi cố gắng hạn chế information loss.

Paper phân loại discretization theo nhiều chiều:

```text
Discretization
│
├── Supervised / Unsupervised
│
├── Top-down / Bottom-up
│
├── Static / Dynamic
│
└── Global / Local
```

Tuy nhiên một vấn đề xuất hiện:

> Nhiều discretization techniques được thiết kế cho dữ liệu nói chung và không trực tiếp mô hình hóa temporal structure.

---

# 6. Vấn đề khi Discretization bỏ qua Temporality

Giả sử time series:

```text
t1   t2   t3   t4   t5
10   11   12   30   31
```

Một phương pháp discretization thông thường có thể chỉ quan tâm đến:

$$
\{10,11,12,30,31\}
$$

và phân chia chúng dựa trên distribution.

Nhưng đối với time series, còn tồn tại information:

$$
10\rightarrow11\rightarrow12\rightarrow30\rightarrow31
$$

Trong đó:

```text
10 → 11 → 12
```

có thể là một temporal progression.

Do đó, nếu preprocessing chỉ xem các observation như những điểm độc lập:

$$
x_i \perp x_j
$$

thì có nguy cơ bỏ qua temporal dependency.

Paper nhấn mạnh chính vấn đề này khi thảo luận về những phương pháp discretization phân tán: một số phương pháp có thể xử lý dữ liệu mà **không xét temporality**.

---

# 7. Time-Series-specific Discretization

Khi temporal information đóng vai trò quan trọng, paper chỉ ra rằng các kỹ thuật discretization dành riêng cho time series có thể phù hợp hơn.

Paper đề cập các hướng như:

```text
Time-Series Discretization
│
├── SAX
├── MINIONS
└── Temporal Discretization
```

Đây là điểm quan trọng:

> Khi temporal structure là một phần quan trọng của information cần bảo toàn, nên xem xét các phương pháp được thiết kế riêng cho time-series data thay vì áp dụng một generic discretization method một cách trực tiếp.

---

# 8. Symbolic Aggregate Approximation — SAX

Paper liệt kê **Symbolic Aggregate Approximation (SAX)** như một kỹ thuật có thể áp dụng cho time-series discretization.

Ý tưởng tổng quát của SAX là biến đổi numerical time series thành một biểu diễn symbolic.

Có thể hình dung:

```text
Numerical Time Series
        │
        ▼
   Transformation
        │
        ▼
Symbolic Representation
```

Ví dụ khái niệm:

```text
Numerical:

1.1  1.2  1.3  2.8  3.0  2.9

        ↓

Symbolic:

 a    a    b    c    c    c
```

Mục tiêu không phải đơn giản là chia từng giá trị độc lập thành bins, mà là tạo một representation phù hợp hơn với cấu trúc của time series.

**Lưu ý:** paper chỉ đưa SAX như một ví dụ về time-series-specific discretization. Không được viết rằng tác giả đề xuất SAX.

---

# 9. MINIONS

Paper cũng đề cập **MINIONS — Multiple Normal Distributions** như một kỹ thuật có thể áp dụng cho time-series discretization.

Điểm cần ghi nhớ là MINIONS được paper sử dụng như một ví dụ trong nhóm phương pháp có khả năng xử lý tính temporal của dữ liệu.

Pipeline khái quát:

```text
Time-Series Data
       │
       ▼
Temporal-aware
Discretization
       │
       ▼
Discrete Representation
```

Paper không đề xuất MINIONS như contribution mới.

Do đó trong README phải phân biệt:

```text
Paper proposes
    ≠
Paper surveys
```

MINIONS thuộc nhóm phương pháp được survey.

---

# 10. Temporal Discretization

Paper còn dẫn một hướng **temporal discretization technique** được đề xuất cho distributed systems.

Điểm khác biệt cơ bản là discretization được thiết kế với awareness về temporal characteristics thay vì hoàn toàn bỏ qua thứ tự thời gian.

Có thể hình dung:

```text
Generic Discretization

Values
  ↓
Distribution
  ↓
Bins
```

so với:

```text
Temporal Discretization

Time-Series
  ↓
Temporal Structure
  ↓
Discretization
  ↓
Time-Series Representation
```

Đây là sự khác biệt quan trọng giữa:

$$
\text{Value-based preprocessing}
$$

và:

$$
\text{Temporal-aware preprocessing}
$$

---

# 11. Temporal Structure và Information Loss

Một mục tiêu quan trọng của preprocessing là giảm complexity nhưng vẫn giữ information hữu ích.

Discretization có lợi ích:

* giảm data complexity;
* giảm data volume;
* làm pattern dễ hiểu hơn;
* có thể phù hợp với các algorithms yêu cầu categorical/discrete input.

Nhưng trade-off là:

$$
\boxed{
Discretization
\rightarrow
Simplification
\rightarrow
Potential\ Information\ Loss
}
$$

Đối với time series, information loss còn có thể liên quan đến:

```text
Value Information
+
Temporal Information
```

Do đó cần xem xét cả hai.

---

# 12. Temporal Information Preservation

Có thể mô hình hóa mục tiêu preprocessing như:

$$
\text{Raw Time Series}
\rightarrow
\text{Transformed Time Series}
$$

với yêu cầu:

$$
I(X')
\approx
I(X)
$$

trong đó $I(\cdot)$ đại diện cho information hữu ích đối với downstream task.

Trong time series, cần quan tâm thêm:

$$
I_{\text{temporal}}
$$

Do đó một transformation tốt không chỉ cần:

$$
\text{Preserve Values}
$$

mà còn cần tránh làm mất:

$$
\text{Temporal Relationships}
$$

---

# 13. Temporal Features và Downstream Model

Temporal representation cuối cùng được sử dụng bởi downstream model.

Trong empirical analysis của paper, tác giả sử dụng **LSTM networks** để đánh giá tác động của các preprocessing techniques lên prediction quality.

Pipeline thực nghiệm có dạng:

```text
Raw AirQuality Dataset
        │
        ▼
Standardized Preprocessing
        │
        ▼
Feature Engineering
        │
        ▼
Feature Selection
        │
        ▼
Discretization / Other Tested Transformation
        │
        ▼
Processed Dataset
        │
        ▼
LSTM
        │
        ▼
Prediction Quality
```

Điểm quan trọng là tác giả không chỉ đánh giá preprocessing dựa trên data quality.

Họ còn đánh giá:

$$
\boxed{
Impact\ on\ AI\ Model
}
$$

tức preprocessing được đánh giá dựa trên ảnh hưởng tới prediction model.

---

# 14. Temporal Features và Empirical Analysis

Trong experimental setup, paper sử dụng:

* AirQuality dataset;
* 9358 instances;
* dữ liệu trung bình theo giờ;
* 15 variables;
* dữ liệu được thu thập trong khoảng March 2004 đến February 2005.

Carbon Monoxide (CO) được chọn làm response variable, các feature còn lại được sử dụng làm predictors.

Paper dùng cùng preprocessing configuration và evaluation strategy giữa các experiment để giảm variation.

Điều này cho phép so sánh:

```text
Preprocessing Method A
        ↓
       LSTM
        ↓
    Performance

Preprocessing Method B
        ↓
       LSTM
        ↓
    Performance
```

thay vì thay đổi đồng thời preprocessing và model.

---

# 15. Một kết quả quan trọng liên quan đến Feature Engineering

Trong experimental analysis, paper cho thấy việc biến đổi feature có thể ảnh hưởng đáng kể đến prediction accuracy.

Đặc biệt với discretization:

```text
Continuous Features
        ↓
Discretization
        ↓
Categorical / Discrete Features
        ↓
LSTM
```

Các tác giả quan sát rằng nhiều discretization techniques làm giảm prediction accuracy.

Điều này được giải thích bởi:

$$
\boxed{
Discretization
\rightarrow
Information\ Loss
\rightarrow
Prediction\ Accuracy\downarrow
}
$$

Tuy nhiên có một ngoại lệ đáng chú ý trong experiment:

> SOM tạo ra một trong những LSTM networks có prediction accuracy tốt nhất trong số các experiment discretization được thực hiện.

Do đó không thể kết luận:

$$
\text{Discretization is always bad}
$$

mà phải kết luận thận trọng hơn:

$$
\boxed{
Effect\ of\ Discretization
depends\ on\ the\ technique
}
$$

---

# 16. Điều paper thực sự muốn nhấn mạnh

Từ phần Feature Engineering và discretization, có thể rút ra một nguyên tắc quan trọng:

> Preprocessing phải được lựa chọn dựa trên data characteristics và downstream task.

Không phải:

```text
Time Series
   ↓
Apply any generic preprocessing
```

mà:

```text
Time Series
   ↓
Understand Temporal Characteristics
   ↓
Select Appropriate Transformation
   ↓
Evaluate Information Preservation
   ↓
Evaluate Downstream Model
```

---

# 17. Temporal Features không đồng nghĩa với Time-Series Preprocessing

Cần phân biệt ba khái niệm:

| Khái niệm                 | Ý nghĩa                                             |
| ------------------------- | --------------------------------------------------- |
| Temporal Feature          | Feature biểu diễn thông tin liên quan đến thời gian |
| Feature Engineering       | Tạo, biến đổi hoặc giảm feature                     |
| Time-Series Preprocessing | Toàn bộ preprocessing pipeline dành cho time-series |

Ví dụ:

```text
hour_sin
hour_cos
day_of_week
lag_1
rolling_mean
```

là các temporal features phổ biến trong thực tế.

Nhưng:

> **Paper này không khảo sát chúng như một nhóm thuật toán riêng.**

Vì vậy không được viết:

> "Tác giả đề xuất sử dụng hour_sin, hour_cos, lag và rolling statistics."

Đó là nội dung ngoài paper.

---

# 18. Temporal Awareness trong Preprocessing

Có thể tổng hợp tư tưởng của phần này:

```text
Generic Data Preprocessing
        │
        ├── Value Distribution
        ├── Feature Distribution
        └── Statistical Properties

Time-Series-aware Preprocessing
        │
        ├── Value Distribution
        ├── Feature Distribution
        ├── Temporal Ordering
        ├── Temporal Dependency
        └── Temporal Patterns
```

Do đó:

$$
\boxed{
Time-Series\ preprocessing=
Generic\ preprocessing
+
Temporal\ Awareness
}
$$

Đây là một cách diễn giải khái quát để hiểu paper, không phải một công thức do tác giả đưa ra.

---

# 19. Edge Computing và Temporal Processing

Một mục tiêu khác của survey là đánh giá khả năng phân phối preprocessing lên Edge.

Paper nhấn mạnh rằng preprocessing tại edge có thể:

* giảm workload của central system;
* giảm lượng dữ liệu cần truyền;
* giảm resource consumption;
* hỗ trợ EdgeAI.

Với time-series data, điều này dẫn tới câu hỏi:

```text
Sensor
  │
  ▼
Edge
  │
  ├── Temporal preprocessing
  ├── Feature transformation
  └── Feature selection
  │
  ▼
Network
  │
  ▼
Cloud / AI
```

Tuy nhiên paper cũng lưu ý rằng việc đánh giá khả năng triển khai các **time-series-specific techniques** lên edge vẫn cần thêm empirical analysis.

---

# 20. Limitations của phần Temporal Features

Đây là phần đặc biệt quan trọng.

Paper có phạm vi rộng nhưng không nhằm xây dựng một hệ thống temporal-feature engineering hoàn chỉnh.

Do đó paper không cung cấp một framework toàn diện cho:

```text
Calendar Features
Lag Features
Rolling Features
Fourier Features
Seasonal Features
Cyclical Encoding
```

Thay vào đó, paper tập trung vào preprocessing taxonomy rộng hơn và đánh giá empirically các nhóm kỹ thuật được lựa chọn.

Một điểm được tác giả trực tiếp chỉ ra là một số phương pháp distributed processing đã **không xét temporality**, và khi temporal information quan trọng thì các time-series discretization methods sẽ phù hợp hơn.

---

# 21. Comparison

| Approach                   |       Temporal Awareness | Mục tiêu chính                  |      Information Loss Risk |
| -------------------------- | -----------------------: | ------------------------------- | -------------------------: |
| Generic Binning            |                     Thấp | Discretization                  |                         Có |
| K-means Discretization     |          Thấp–Trung bình | Clustering-based discretization |                         Có |
| SOM Discretization         | Phụ thuộc representation | Discretization                  |                         Có |
| SAX                        |  Cao hơn cho time series | Symbolic representation         |                         Có |
| MINIONS                    |        Time-series aware | Discretization                  |                         Có |
| Temporal Discretization    |                      Cao | Time-aware discretization       |                         Có |
| Explicit Calendar Features |                        — | Feature synthesis               | Paper không khảo sát riêng |

Bảng này chỉ nhằm định vị các phương pháp được paper đề cập; không phải ranking performance chung.

---

# 22. Flow tổng quát

Có thể tóm tắt phần Temporal Features / Temporal-aware Feature Engineering như sau:

```text
Raw Time-Series
       │
       ▼
Understand Temporal Structure
       │
       ├───────────────┐
       │               │
       ▼               ▼
Generic          Time-Series-specific
Transformation   Transformation
       │               │
       │               ├── SAX
       │               ├── MINIONS
       │               └── Temporal Discretization
       │
       └───────────────┬───────────────┘
                       ▼
                Transformed Data
                       │
                       ▼
              Downstream AI Model
                       │
                       ▼
                 Evaluate Impact
```

---

# 23. Key Takeaways

### 1. Time-series preprocessing phải quan tâm đến temporal structure

Không nên xem time-series data chỉ như một bảng các observation độc lập.

### 2. Paper không đề xuất một bộ Temporal Features riêng

Các feature như:

```text
Hour
Day
Month
Lag
Rolling Mean
Sin/Cos Encoding
```

không phải contribution hoặc taxonomy riêng của paper.

### 3. Paper đặt vấn đề temporal awareness trong Feature Engineering

Đặc biệt khi thảo luận về discretization, paper chỉ ra rằng các phương pháp generic có thể bỏ qua temporality.

### 4. Time-series-specific discretization có thể phù hợp hơn

Paper đề cập:

```text
SAX
MINIONS
Temporal Discretization
```

như những hướng có thể xử lý time-series characteristics.

### 5. Preprocessing phải được đánh giá cùng downstream task

Một transformation không nên chỉ được đánh giá dựa trên data representation.

Cần xem:

$$
\boxed{
Preprocessing
\rightarrow
Data\ Quality
\rightarrow
AI\ Performance
}
$$

### 6. Information loss là trade-off quan trọng

Đặc biệt với discretization:

$$
Simplification
\leftrightarrow
Information\ Preservation
$$

### 7. Temporal awareness là điểm khác biệt quan trọng

Một preprocessing method có thể hoạt động tốt trên generic numerical data nhưng không nhất thiết phù hợp với time-series data.

---

# 24. Kết luận

Phần Feature Engineering của survey cho thấy một vấn đề quan trọng:

> **Feature transformation trên time-series data không thể chỉ dựa vào distribution của các giá trị; trong những trường hợp temporal structure mang information quan trọng, transformation cũng cần xem xét đặc tính của chuỗi thời gian.**

Paper không xây dựng một framework riêng cho việc tạo calendar features hay lag features. Thay vào đó, tác giả khảo sát Feature Engineering trong phạm vi rộng hơn và đặc biệt chỉ ra sự khác biệt giữa generic discretization và các kỹ thuật discretization dành cho time series.

Có thể cô đọng tư tưởng này thành:

$$
\boxed{
Good\ Time-Series\ Preprocessing=Data\ Transformation
+
Temporal\ Awareness
+
Information\ Preservation
}
$$

Trong đó **temporal awareness** không nhất thiết có nghĩa là phải tạo thêm một temporal feature mới. Nó còn có nghĩa là:

> Khi biến đổi dữ liệu, phải đảm bảo phương pháp không vô tình loại bỏ cấu trúc thời gian mà downstream model cần.

```

### Vị trí của file trong Chapter 5

Theo đúng paper, mình khuyên Chapter 5 nên tổ chức theo hướng:

```text
05_feature_engineering/
│
├── 01_temporal_features.md
├── 02_discretization.md
├── 03_feature_reduction.md
├── 04_feature_transformation.md
├── 05_feature_selection.md
└── 06_comparison.md
```

**Nguồn paper:** [Full-text PDF — Tawakuli et al.](https://research.chalmers.se/publication/540495/file/540495_Fulltext.pdf?utm_source=chatgpt.com) | [ScienceDirect article](https://www.sciencedirect.com/science/article/pii/S2307187724000452?utm_source=chatgpt.com)

[1]: https://www.sciencedirect.com/science/article/pii/S2307187724000452?utm_source=chatgpt.com "Survey:Time-series data preprocessing: A survey and an empirical analysis - ScienceDirect"
[2]: https://research.chalmers.se/publication/540495/file/540495_Fulltext.pdf?utm_source=chatgpt.com "Survey: Time-Series Data Preprocessing: A Survey and an Empirical"
