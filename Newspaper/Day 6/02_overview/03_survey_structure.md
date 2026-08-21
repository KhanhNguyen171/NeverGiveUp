# 2.3 Survey Structure

Cấu trúc của survey được xây dựng theo nguyên tắc **từ phạm vi nghiên cứu đến taxonomy, từ taxonomy đến phân tích phương pháp, sau đó chuyển sang đánh giá thực nghiệm và tổng hợp thành pipeline**. Cách tổ chức này nhằm bảo đảm các chương có quan hệ logic với nhau, hạn chế lặp lại nội dung và duy trì trọng tâm vào preprocessing cho numerical time-series data.

Toàn bộ nghiên cứu có thể được mô hình hóa theo chuỗi:

$$
\text{Research Scope}
\rightarrow
\text{Taxonomy}
\rightarrow
\text{Method Analysis}
\rightarrow
\text{Empirical Evaluation}
\rightarrow
\text{Discussion}
\rightarrow
\text{Pipeline}
\rightarrow
\text{Lessons Learned}.
$$

Trong đó, **Chapter 1** xác lập vấn đề nghiên cứu, **Chapter 2** xác định phạm vi và cấu trúc phân loại, **Chapters 3--8** phân tích các nhóm preprocessing, **Chapter 9** đánh giá thực nghiệm, **Chapter 10** tổng hợp trade-offs và limitations, còn **Chapter 11--14** chuyển các kết quả thành pipeline, bài học và kết luận.

---

## 2.3.1 Research organization

Nghiên cứu được chia thành năm tầng nội dung chính:

$$
\mathcal{R}=

{
\mathcal{I},
\mathcal{S},
\mathcal{M},
\mathcal{E},
\mathcal{A}
},
$$

trong đó:

* $\mathcal{I}$ — **Introduction**;
* $\mathcal{S}$ — **Survey and Method Taxonomy**;
* $\mathcal{M}$ — **Method Analysis**;
* $\mathcal{E}$ — **Empirical Analysis**;
* $\mathcal{A}$ — **Application and Synthesis**.

Cấu trúc này giúp phân biệt rõ giữa **khảo sát literature**, **phân tích phương pháp**, **kiểm chứng thực nghiệm** và **xây dựng pipeline áp dụng**.

---

## 2.3.2 Chapter 1 — Introduction

**Chapter 1 – Introduction** xác định bối cảnh và vấn đề nghiên cứu.

Chương này gồm bốn nội dung:

1. **Background** — giới thiệu vai trò của time-series data và preprocessing.
2. **Problem** — xác định các vấn đề khi dữ liệu raw được đưa trực tiếp vào AI/ML systems.
3. **Motivation** — giải thích lý do cần một survey có hệ thống về preprocessing.
4. **Contributions** — xác định những đóng góp và phạm vi của nghiên cứu.

Quan hệ giữa các mục được xây dựng theo:

$$
\text{Background}
\rightarrow
\text{Problem}
\rightarrow
\text{Motivation}
\rightarrow
\text{Contributions}.
$$

Chapter 1 trả lời câu hỏi:

> **Tại sao cần nghiên cứu preprocessing cho time-series data và nghiên cứu này giải quyết khoảng trống nào?**

Chương này không đi sâu vào thuật toán cụ thể. Các phương pháp chỉ được giới thiệu ở mức cần thiết để thiết lập research problem.

---

## 2.3.3 Chapter 2 — Overview

**Chapter 2 – Overview** xác định framework của toàn bộ survey.

Chương gồm:

* `01_research_scope.md`;
* `02_taxonomy.md`;
* `03_survey_structure.md`.

### Research scope

`01_research_scope.md` xác định:

* loại dữ liệu được nghiên cứu;
* mục tiêu preprocessing;
* nhóm kỹ thuật nằm trong phạm vi;
* phạm vi ứng dụng;
* những nội dung nằm ngoài phạm vi.

### Taxonomy

`02_taxonomy.md` tổ chức các phương pháp thành sáu nhóm:

$$
{
\text{Cleaning},
\text{Transformation},
\text{Feature Engineering},
\text{Feature Selection},
\text{Sensor Fusion},
\text{Compression}
}.
$$

### Survey structure

Mục hiện tại xác định cách các nhóm trên được triển khai trong những chương tiếp theo.

Do đó:

$$
\boxed{
\text{Scope}
\rightarrow
\text{Taxonomy}
\rightarrow
\text{Survey Structure}
}
$$

là nền tảng tổ chức cho toàn bộ phần còn lại của nghiên cứu.

---

# 2.3.4 Chapters 3--8 — Method Analysis

Các Chapter 3 đến Chapter 8 là **phần trung tâm của survey**. Mỗi chương tương ứng với một nhóm trong taxonomy.

Mỗi nhóm được phân tích theo cùng một logic:

$$
\text{Definition}
\rightarrow
\text{Methods}
\rightarrow
\text{Mathematical Principle}
\rightarrow
\text{Advantages}
\rightarrow
\text{Limitations}
\rightarrow
\text{Selection Context}.
$$

Việc sử dụng một cấu trúc thống nhất giúp các phương pháp thuộc những nhóm khác nhau có thể được so sánh trên cùng một framework.

---

## 2.3.5 Chapter 3 — Data Cleaning

**Chapter 3 – Data Cleaning** tập trung vào các vấn đề làm suy giảm chất lượng của observations.

Chương gồm:

* `01_missing_data.md`;
* `02_outlier_detection.md`;
* `03_noise_reduction.md`;
* `04_comparison.md`.

Quan hệ nội dung:

$$
\text{Missing Data}
\rightarrow
\text{Outlier Detection}
\rightarrow
\text{Noise Reduction}
\rightarrow
\text{Comparison}.
$$

Chương này trả lời:

> **Làm thế nào phát hiện và xử lý những vấn đề trực tiếp của dữ liệu quan sát?**

`04_comparison.md` đóng vai trò tổng hợp, không mở rộng sang các transformation hoặc feature engineering.

---

## 2.3.6 Chapter 4 — Data Transformation

**Chapter 4 – Data Transformation** chuyển từ vấn đề *data quality* sang vấn đề *data representation*.

Chương gồm:

* `01_scaling_normalization.md`;
* `02_transformation.md`;
* `03_stationarity.md`;
* `04_decomposition.md`.

Logic chính:

$$
\text{Scale}
\rightarrow
\text{Transform}
\rightarrow
\text{Stationarity}
\rightarrow
\text{Decomposition}.
$$

Chương này trả lời:

> **Làm thế nào biến đổi statistical representation của time series để dữ liệu phù hợp hơn với downstream analysis?**

Một ranh giới quan trọng được duy trì: **transformation không đồng nghĩa với feature engineering**. Transformation chủ yếu thay đổi representation của biến hiện có, trong khi feature engineering tạo ra thông tin biểu diễn mới.

---

## 2.3.7 Chapter 5 — Feature Engineering

**Chapter 5 – Feature Engineering** tập trung vào việc khai thác temporal structure.

Chương gồm:

* `01_temporal_features.md`;
* `02_lag_features.md`;
* `03_rolling_features.md`;
* `04_feature_representation.md`.

Logic:

$$
\text{Temporal Context}
\rightarrow
\text{Lag Dependency}
\rightarrow
\text{Rolling Statistics}
\rightarrow
\text{Feature Representation}.
$$

Chương này trả lời:

> **Làm thế nào chuyển temporal information thành các feature có thể sử dụng bởi downstream model?**

Đặc biệt, `04_feature_representation.md` đóng vai trò cầu nối sang **Feature Selection** vì sau khi feature được tạo ra, số lượng và redundancy của chúng có thể tăng đáng kể.

---

## 2.3.8 Chapter 6 — Feature Selection

**Chapter 6 – Feature Selection** giải quyết vấn đề redundancy và dimensionality.

Chương gồm:

* `01_feature_selection.md`;
* `02_filter_methods.md`;
* `03_wrapper_methods.md`;
* `04_embedded_methods.md`;
* `05_dimensionality_reduction.md`.

Cấu trúc:

$$
\text{Feature Selection Problem}
\rightarrow
\begin{cases}
\text{Filter}\
\text{Wrapper}\
\text{Embedded}\
\text{Dimensionality Reduction}
\end{cases}.
$$

Chương trả lời:

> **Sau khi feature được xây dựng, làm thế nào xác định representation có kích thước và thông tin phù hợp cho downstream model?**

Điểm kết nối với Chapter 5 là:

$$
F_{raw}
\rightarrow
F_{engineered}
\rightarrow
F_{selected}.
$$

---

## 2.3.9 Chapter 7 — Sensor Fusion

**Chapter 7 – Sensor Fusion** mở rộng preprocessing từ một data source sang nhiều nguồn dữ liệu.

Chương gồm:

* `01_sensor_fusion.md`;
* `02_fusion_levels.md`;
* `03_temporal_alignment.md`.

Logic:

$$
\text{Multiple Sources}
\rightarrow
\text{Fusion Strategy}
\rightarrow
\text{Temporal Alignment}.
$$

Chương trả lời:

> **Làm thế nào kết hợp nhiều sensor hoặc data sources mà vẫn bảo toàn quan hệ temporal?**

Temporal alignment được tách riêng vì cùng một timestamp hoặc sampling frequency là điều kiện quan trọng để fusion có ý nghĩa.

---

## 2.3.10 Chapter 8 — Data Compression

**Chapter 8 – Data Compression** tập trung vào data efficiency.

Chương gồm:

* `01_compression.md`;
* `02_lossless_compression.md`;
* `03_lossy_compression.md`;
* `04_edge_iot.md`.

Logic:

$$
\text{Compression Problem}
\rightarrow
\begin{cases}
\text{Lossless}\
\text{Lossy}
\end{cases}
\rightarrow
\text{Edge/IoT Constraints}.
$$

Chương trả lời:

> **Làm thế nào giảm storage và communication cost trong khi vẫn duy trì lượng thông tin cần thiết?**

Chương này mở rộng khái niệm preprocessing từ **data quality và model readiness** sang **system efficiency**.

---

# 2.3.11 Chapter 9 — Empirical Analysis

Sau khi hoàn thành survey phương pháp, **Chapter 9 – Empirical Analysis** chuyển từ theoretical analysis sang empirical evaluation.

Chương gồm:

* `01_experimental_setup.md`;
* `02_dataset.md`;
* `03_preprocessing_methods.md`;
* `04_evaluation_metrics.md`;
* `05_results.md`;
* `06_findings.md`.

Cấu trúc thực nghiệm:

$$
\text{Setup}
\rightarrow
\text{Dataset}
\rightarrow
\text{Preprocessing}
\rightarrow
\text{Metrics}
\rightarrow
\text{Results}
\rightarrow
\text{Findings}.
$$

Điểm quan trọng là Chapter 9 **không giới thiệu thêm một taxonomy mới**. Các preprocessing methods được lựa chọn dựa trên taxonomy ở Chapter 2 và được phân tích ở Chapters 3--8.

Nhờ đó:

$$
\text{Taxonomy}
\rightarrow
\text{Method Selection}
\rightarrow
\text{Experiment}
$$

tạo thành một chuỗi có thể truy xuất nguồn gốc rõ ràng.

---

# 2.3.12 Chapter 10 — Discussion

**Chapter 10 – Discussion** tổng hợp kết quả từ survey và empirical analysis.

Chương gồm:

* `01_comparison.md`;
* `02_tradeoffs.md`;
* `03_limitations.md`.

Ba nội dung có quan hệ:

$$
\text{Comparison}
\rightarrow
\text{Trade-offs}
\rightarrow
\text{Limitations}.
$$

### Comparison

So sánh các phương pháp theo những tiêu chí thống nhất:

* data quality;
* information preservation;
* computational cost;
* scalability;
* temporal suitability;
* downstream model performance.

### Trade-offs

Không tồn tại một preprocessing method tối ưu cho mọi trường hợp. Việc lựa chọn thường có dạng:

$$
\text{Performance}
\leftrightarrow
\text{Complexity}
\leftrightarrow
\text{Information Loss}
\leftrightarrow
\text{Resource Cost}.
$$

### Limitations

Phân tích những giới hạn của:

* phương pháp;
* dataset;
* experimental design;
* khả năng generalization;
* assumptions trong preprocessing.

Chapter 10 do đó đóng vai trò chuyển từ câu hỏi **"phương pháp nào tồn tại?"** sang **"khi nào nên sử dụng phương pháp nào?"**

---

# 2.3.13 Chapter 11 — Preprocessing Pipeline

**Chapter 11 – Pipeline** chuyển kết quả survey thành một workflow có thể áp dụng.

Chương gồm:

* `01_pipeline_overview.md`;
* `02_data_cleaning.md`;
* `03_transformation.md`;
* `04_feature_engineering.md`;
* `05_ai_ready_data.md`.

Pipeline tổng quát:

$$
X_{raw}
\rightarrow
X_{clean}
\rightarrow
X_{transformed}
\rightarrow
X_{feature}
\rightarrow
X_{AI-ready}.
$$

Khác với Chapters 3--8, chương này không tiếp tục khảo sát từng phương pháp riêng lẻ. Mục tiêu là xác định **cách các phương pháp được kết hợp trong một preprocessing workflow**.

Một pipeline thực tế phải đồng thời bảo đảm:

* temporal consistency;
* absence of data leakage;
* reproducibility;
* compatibility với downstream model;
* computational feasibility.

---

# 2.3.14 Chapter 12 — Lessons Learned

**Chapter 12 – Lessons Learned** tổng hợp các nguyên tắc lựa chọn phương pháp.

Chương gồm:

* `01_key_principles.md`;
* `02_method_selection.md`;
* `03_common_mistakes.md`.

Cấu trúc:

$$
\text{Principles}
\rightarrow
\text{Method Selection}
\rightarrow
\text{Failure Modes}.
$$

Mục tiêu của chương là chuyển kiến thức từ survey thành các nguyên tắc thực hành.

Một preprocessing strategy tốt không được xác định chỉ bởi độ phức tạp của thuật toán mà bởi mức độ phù hợp giữa:

$$
\text{Data Characteristics}
+
\text{Task Requirements}
+
\text{Model Requirements}
+
\text{System Constraints}.
$$

---

# 2.3.15 Chapter 13 — UCI Appliances Case Study

**Chapter 13 – UCI Appliances** đóng vai trò case study để kết nối framework tổng quát với một numerical time-series dataset cụ thể.

Chương gồm:

* `01_dataset.md`;
* `02_preprocessing.md`;
* `03_feature_engineering.md`;
* `04_connection_to_survey.md`.

Case study được tổ chức theo:

$$
\text{Dataset}
\rightarrow
\text{Preprocessing}
\rightarrow
\text{Feature Engineering}
\rightarrow
\text{Survey Mapping}.
$$

Mục tiêu không phải xây dựng một nghiên cứu forecasting độc lập, mà kiểm chứng khả năng áp dụng taxonomy và pipeline đã xây dựng.

Do đó, các quyết định preprocessing trên UCI Appliances được ánh xạ ngược về taxonomy:

$$
\text{Case Study Decision}
\rightarrow
\text{Taxonomy Category}
\rightarrow
\text{Method Rationale}.
$$

Cách tổ chức này giúp chứng minh rằng taxonomy không chỉ có giá trị cho literature review mà còn có thể được sử dụng để thiết kế preprocessing pipeline trên dữ liệu thực tế.

---

# 2.3.16 Chapter 14 — Conclusion

**Chapter 14 – Conclusion** tổng hợp các kết quả chính của nghiên cứu.

Chương tập trung vào ba câu hỏi:

1. Những nhóm preprocessing chính nào đã được xác định?
2. Những trade-off quan trọng nào xuất hiện khi lựa chọn phương pháp?
3. Những nguyên tắc nào có thể sử dụng để xây dựng AI-ready time-series data?

Kết luận được xây dựng từ:

$$
\text{Survey}
+
\text{Empirical Evidence}
+
\text{Discussion}
+
\text{Case Study}
\rightarrow
\text{Conclusions}.
$$

Chapter 14 không giới thiệu phương pháp mới hoặc mở rộng taxonomy.

---

# 2.3.17 Quan hệ giữa các chương

Toàn bộ nghiên cứu có thể được tóm tắt bằng workflow:

```text
Chapter 1
Introduction
    │
    ▼
Chapter 2
Scope → Taxonomy → Survey Structure
    │
    ▼
┌─────────────────────────────────────────────┐
│              Method Analysis                │
│                                             │
│ Ch.3        Ch.4          Ch.5              │
│ Cleaning → Transformation → Feature Eng.    │
│                                             │
│      ↓                                      │
│ Ch.6 Feature Selection                      │
│      ↓                                      │
│ Ch.7 Sensor Fusion                          │
│      ↓                                      │
│ Ch.8 Data Compression                       │
└─────────────────────────────────────────────┘
    │
    ▼
Chapter 9
Empirical Analysis
    │
    ▼
Chapter 10
Comparison → Trade-offs → Limitations
    │
    ▼
Chapter 11
Preprocessing Pipeline
    │
    ▼
Chapter 12
Lessons Learned
    │
    ▼
Chapter 13
UCI Appliances Case Study
    │
    ▼
Chapter 14
Conclusion
```

Cấu trúc này tạo ra ba tầng logic chính:

$$
\boxed{
\begin{aligned}
\text{Tầng 1:}&\quad
\text{Define the Problem}
[2mm]
\text{Tầng 2:}&\quad
\text{Analyze and Evaluate Methods}
[2mm]
\text{Tầng 3:}&\quad
\text{Synthesize and Apply}
\end{aligned}
}
$$

**Tầng 1** gồm Chapters 1--2, xác định vấn đề, phạm vi và taxonomy.

**Tầng 2** gồm Chapters 3--10, phân tích phương pháp, đánh giá thực nghiệm và thảo luận trade-offs.

**Tầng 3** gồm Chapters 11--14, chuyển kiến thức thành pipeline, lessons learned, case study và kết luận.

Như vậy, cấu trúc survey không chỉ là cách sắp xếp các chương mà còn phản ánh **chuỗi lập luận khoa học của nghiên cứu**:

$$
\boxed{
\text{Why}
\rightarrow
\text{What}
\rightarrow
\text{How}
\rightarrow
\text{How Well}
\rightarrow
\text{When}
\rightarrow
\text{How to Apply}
}
$$

Trong đó:

* **Why** — tại sao preprocessing cần được nghiên cứu;
* **What** — những nhóm preprocessing nào tồn tại;
* **How** — các phương pháp hoạt động như thế nào;
* **How Well** — chúng hoạt động hiệu quả đến đâu;
* **When** — khi nào nên lựa chọn từng phương pháp;
* **How to Apply** — làm thế nào kết hợp chúng thành một preprocessing pipeline thực tế.

Đây là nguyên tắc xuyên suốt của survey và là cơ sở để bảo đảm sự liên kết giữa **taxonomy, method analysis, empirical analysis và pipeline construction**.
