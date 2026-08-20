# Survey: Time-series data preprocessing: A survey and an empirical analysis — 2025

- Link bài báo: https://www.sciencedirect.com/science/article/pii/S2307187724000452?utm_source=chatgpt.com#tbl0005

## Architecture

| Chapter | Directory | Nội dung chính |
|---|---|---|
| 01 | `01_introduction/` | Bối cảnh, vấn đề, motivation, mục tiêu và đóng góp của bài báo |
| 02 | `02_overview/` | Tổng quan nghiên cứu, phạm vi và taxonomy của Time-Series Data Preprocessing |
| 03 | `03_data_cleaning/` | Các phương pháp xử lý Missing Data, Outlier và Noise |
| 04 | `04_data_transformation/` | Scaling, Normalization, Transformation, Stationarity và Decomposition |
| 05 | `05_feature_engineering/` | Xây dựng các đặc trưng từ cấu trúc thời gian của dữ liệu |
| 06 | `06_feature_selection/` | Feature Selection và Dimensionality Reduction |
| 07 | `07_sensor_fusion/` | Kết hợp dữ liệu từ nhiều sensor và xử lý temporal alignment |
| 08 | `08_data_compression/` | Các phương pháp nén Time-Series Data và trade-off giữa compression và information |
| 09 | `09_empirical_analysis/` | Thiết kế thực nghiệm, dataset, preprocessing methods, metrics và kết quả |
| 10 | `10_discussion/` | Phân tích kết quả, so sánh phương pháp, trade-off và limitations |
| 11 | `11_pipeline/` | Xây dựng pipeline preprocessing từ Raw Data đến AI-ready Data |
| 12 | `12_lessons_learned/` | Các nguyên tắc, bài học và kinh nghiệm lựa chọn preprocessing method |
| 13 | `13_uci_appliances/` | Liên hệ các phương pháp trong survey với UCI Appliances Energy Prediction |
| 14 | `14_conclusion/` | Tổng kết những kiến thức và kết luận quan trọng |
| 15 | `references/` | Các tài liệu và nghiên cứu được tham khảo |


```
time-series-data-preprocessing/
│
├── README.md
│
├── 01_introduction/
│   ├── 01_background.md
│   ├── 02_problem.md
│   ├── 03_motivation.md
│   └── 04_contributions.md
│
├── 02_overview/
│   ├── 01_research_scope.md
│   ├── 02_taxonomy.md
│   └── 03_survey_structure.md
│
├── 03_data_cleaning/
│   ├── 01_missing_data.md
│   ├── 02_outlier_detection.md
│   ├── 03_noise_reduction.md
│   └── 04_comparison.md
│
├── 04_data_transformation/
│   ├── 01_scaling_normalization.md
│   ├── 02_transformation.md
│   ├── 03_stationarity.md
│   └── 04_decomposition.md
│
├── 05_feature_engineering/
│   ├── 01_temporal_features.md
│   ├── 02_lag_features.md
│   ├── 03_rolling_features.md
│   └── 04_feature_representation.md
│
├── 06_feature_selection/
│   ├── 01_feature_selection.md
│   ├── 02_filter_methods.md
│   ├── 03_wrapper_methods.md
│   ├── 04_embedded_methods.md
│   └── 05_dimensionality_reduction.md
│
├── 07_sensor_fusion/
│   ├── 01_sensor_fusion.md
│   ├── 02_fusion_levels.md
│   └── 03_temporal_alignment.md
│
├── 08_data_compression/
│   ├── 01_compression.md
│   ├── 02_lossless_compression.md
│   ├── 03_lossy_compression.md
│   └── 04_edge_iot.md
│
├── 09_empirical_analysis/
│   ├── 01_experimental_setup.md
│   ├── 02_dataset.md
│   ├── 03_preprocessing_methods.md
│   ├── 04_evaluation_metrics.md
│   ├── 05_results.md
│   └── 06_findings.md
│
├── 10_discussion/
│   ├── 01_comparison.md
│   ├── 02_tradeoffs.md
│   └── 03_limitations.md
│
├── 11_pipeline/
│   ├── 01_pipeline_overview.md
│   ├── 02_data_cleaning.md
│   ├── 03_transformation.md
│   ├── 04_feature_engineering.md
│   └── 05_ai_ready_data.md
│
├── 12_lessons_learned/
│   ├── 01_key_principles.md
│   ├── 02_method_selection.md
│   └── 03_common_mistakes.md
│
├── 13_uci_appliances/
│   ├── 01_dataset.md
│   ├── 02_preprocessing.md
│   ├── 03_feature_engineering.md
│   └── 04_connection_to_survey.md
│
├── 14_conclusion/
│   └── 01_conclusion.md
│
└── references/
    └── references.md
```
---

# 1. Bối cảnh

**Time-Series Data** xuất hiện trong rất nhiều hệ thống thực tế như cảm biến IoT, năng lượng, tài chính, y tế, giao thông và các hệ thống công nghiệp. Khác với dữ liệu dạng bảng thông thường, Time Series chứa **mối quan hệ phụ thuộc theo thời gian**, khiến việc xử lý dữ liệu trở nên phức tạp hơn.

Dữ liệu thực tế thường không sạch và có thể chứa:

```text
Missing Values
Outliers
Noise
Irregular Sampling
Different Scales
Temporal Misalignment
Redundant Features
High Dimensionality
```

Nếu đưa trực tiếp dữ liệu này vào Machine Learning hoặc Deep Learning, chất lượng dữ liệu có thể trở thành giới hạn lớn đối với hiệu năng của mô hình.

Vì vậy, **Time-Series Data Preprocessing** đóng vai trò là cầu nối:

```text
Raw Time-Series Data
        ↓
Data Preprocessing
        ↓
Clean / Structured Data
        ↓
Machine Learning / Deep Learning
        ↓
Prediction / Classification / Forecasting
```

---

# 2. Nội dung của bài báo

Bài báo **“Time-Series Data Preprocessing: A Survey and an Empirical Analysis”** tập trung hệ thống hóa các phương pháp được sử dụng để xử lý Time-Series Data trước khi đưa vào các hệ thống AI.

Thay vì tập trung vào một thuật toán forecasting cụ thể, bài báo nhìn preprocessing từ nhiều góc độ:

```text
Data Cleaning
      ↓
Data Transformation
      ↓
Feature Engineering
      ↓
Feature Selection
      ↓
Dimensionality Reduction
      ↓
Sensor Fusion
      ↓
Data Compression
      ↓
Machine Learning / AI
```

Do đó, survey cung cấp một cái nhìn tương đối toàn diện về **quá trình biến dữ liệu time series thô thành dữ liệu có thể sử dụng cho các mô hình AI**.

---

# 3. Vì sao tác giả thực hiện bài báo?

Một vấn đề lớn trong lĩnh vực Time-Series Data là các phương pháp preprocessing thường được nghiên cứu **rời rạc**.

Ví dụ:

```text
Research A
    → Missing Value

Research B
    → Outlier Detection

Research C
    → Normalization

Research D
    → Feature Selection

Research E
    → Sensor Fusion
```

Điều này tạo ra một khoảng trống về mặt tổng quan:

> **Có những nhóm preprocessing nào? Chúng giải quyết vấn đề gì? Khi nào nên sử dụng chúng và preprocessing ảnh hưởng như thế nào đến hiệu năng của mô hình?**

Bài báo được thực hiện nhằm **hệ thống hóa những phương pháp này thành một survey có cấu trúc**, đồng thời bổ sung **empirical analysis** để không chỉ mô tả các phương pháp mà còn xem xét tác động thực tế của preprocessing.

---

# 4. Mục đích của README

README này không nhằm sao chép toàn bộ nội dung của paper.

Nó đóng vai trò là **bản đồ kiến trúc của quá trình học bài báo**.

Mỗi chapter được tách thành các file `.md` nhỏ hơn để tập trung vào một nhóm kiến thức cụ thể:

```text
README.md
   │
   ├── Architecture
   │
   ├── Background
   │
   └── Paper Motivation
            │
            ▼
      Chapter 01 → Introduction
            │
            ▼
      Chapter 02 → Overview
            │
            ▼
      Chapter 03 → Data Cleaning
            │
            ▼
      Chapter 04 → Data Transformation
            │
            ▼
      Chapter 05 → Feature Engineering
            │
            ▼
      Chapter 06 → Feature Selection
            │
            ▼
      Chapter 07 → Sensor Fusion
            │
            ▼
      Chapter 08 → Data Compression
            │
            ▼
      Chapter 09 → Empirical Analysis
            │
            ▼
      Chapter 10 → Discussion
            │
            ▼
      Chapter 11 → Practical Pipeline
            │
            ▼
      Chapter 12 → Lessons Learned
            │
            ▼
      Chapter 13 → UCI Appliances
            │
            ▼
      Chapter 14 → Conclusion
```

Mục tiêu cuối cùng của hệ thống tài liệu là giúp người đọc đi từ **hiểu tại sao cần preprocessing** → **hiểu từng nhóm thuật toán** → **hiểu kết quả thực nghiệm** → **biết cách thiết kế một preprocessing pipeline đúng cho bài toán Time Series thực tế**.
