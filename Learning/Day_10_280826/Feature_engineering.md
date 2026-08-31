Sau **feature selection**, bước tiếp theo không nên chỉ là “tạo thêm feature rồi train”. Với Transformer Regression cho time series, ta nên đặt câu hỏi thực nghiệm:

> **Feature engineering có thực sự tạo ra information hữu ích giúp Transformer học tốt hơn so với representation gốc hay không?**

Điểm quan trọng là phải tách **feature selection** và **feature engineering** thành hai giai đoạn khác nhau.

---

## 1. Hai bài toán khác nhau

### Feature selection

Ta bắt đầu với:

$$
\mathcal{F}
=
\{f_1,f_2,\ldots,f_F\}
$$

và tìm tập con:

$$
\mathcal{F}^{*}\subseteq\mathcal{F}
$$

sao cho:

$$
\mathcal{F}^{*}
=
\text{information cần thiết nhất cho prediction}
$$

Ví dụ:

```text
Raw features
     │
     ├── Temperature
     ├── Humidity
     ├── Pressure
     ├── Hour
     ├── Day
     ├── ...
     └── Random
             │
             ▼
       Feature Selection
             │
             ▼
     Temperature
     Humidity
     Hour
     Day
```

---

### Feature engineering

Bây giờ **không loại bỏ feature nữa**, mà biến đổi/tổ chức lại information:

$$
\mathcal{F}^{*}
\rightarrow
\phi(\mathcal{F}^{*})
$$

Ví dụ:

$$
hour
\rightarrow
\sin(2\pi hour/24)
$$

$$
hour
\rightarrow
\cos(2\pi hour/24)
$$

hoặc:

$$
Temperature_t
\rightarrow
\Delta Temperature_t
=
Temperature_t-Temperature_{t-1}
$$

Mục tiêu là:

> **làm cho predictive structure dễ học hơn đối với model.**

---

# 2. Cách đánh giá đúng nhất: Controlled Experiment

Đây là điểm quan trọng nhất.

Không nên so sánh:

```text
Model A:
Raw features + Transformer nhỏ

Model B:
Engineered features + Transformer lớn
```

vì lúc đó ta không biết improvement đến từ:

* feature engineering;
* model capacity;
* hyperparameter;
* random seed.

Thay vào đó giữ **mọi thứ giống nhau**.

$$
\boxed{
\text{Same Model + Same Data Split + Same Training Protocol}
}
$$

chỉ thay đổi feature representation.

---

# 3. Xây dựng baseline

Sau feature selection, tạo:

$$
X^{raw}
\in
\mathbb{R}^{L\times F}
$$

Train Transformer:

$$
\hat{y}^{raw}
=
f_\theta(X^{raw})
$$

thu được:

$$
RMSE_{raw}
$$

Đây là **baseline**.

---

# 4. Sau đó tạo engineered representation

Ví dụ:

$$
X^{eng}
=
[
X^{raw},
\Delta X,
RollingMean(X),
RollingStd(X),
CyclicTime(X)
]
$$

Transformer:

$$
\hat{y}^{eng}
=
f_\theta(X^{eng})
$$

thu được:

$$
RMSE_{eng}
$$

So sánh:

$$
\Delta RMSE
=
RMSE_{raw}
-
RMSE_{eng}
$$

Nếu:

$$
\Delta RMSE > 0
$$

thì feature engineering cải thiện performance.

Ví dụ:

| Representation        |  MAE |  RMSE | $R^2$ |
| --------------------- | ---: | ----: | ----: |
| Raw selected features | 72.4 | 105.3 |  0.71 |
| + Time features       | 69.1 |  99.8 |  0.74 |
| + Difference          | 67.8 |  96.2 |  0.76 |
| + Rolling statistics  | 66.9 |  94.7 |  0.77 |

Ở đây ta không chỉ biết:

> engineered features tốt hơn.

Mà còn biết:

> **loại engineering nào tạo ra improvement.**

---

# 5. Đặc biệt nên dùng Incremental Feature Engineering

Đừng thêm tất cả engineered features cùng lúc.

Nên xây dựng theo từng nhóm:

$$
\mathcal{F}_0
\rightarrow
\mathcal{F}_1
\rightarrow
\mathcal{F}_2
\rightarrow
\mathcal{F}_3
$$

Ví dụ:

### Baseline

$$
\mathcal{F}_0
=
\text{Selected raw features}
$$

### Experiment 1 — Temporal encoding

$$
\mathcal{F}_1
=
\mathcal{F}_0
+
\{\sin(hour),\cos(hour),\sin(dow),\cos(dow)\}
$$

### Experiment 2 — First-order dynamics

$$
\mathcal{F}_2
=
\mathcal{F}_1
+
\{\Delta x_t\}
$$

### Experiment 3 — Rolling statistics

$$
\mathcal{F}_3
=
\mathcal{F}_2
+
\{\mu_w,\sigma_w,\min_w,\max_w\}
$$

Như vậy có thể đo:

$$
\Delta_1
=
RMSE_0-RMSE_1
$$

$$
\Delta_2
=
RMSE_1-RMSE_2
$$

$$
\Delta_3
=
RMSE_2-RMSE_3
$$

---

# 6. Nhưng có một vấn đề rất quan trọng: Transformer có thể tự học một số feature

Ví dụ bạn tạo:

$$
\Delta x_t=x_t-x_{t-1}
$$

Transformer về lý thuyết có thể tự suy ra một số dạng temporal relationship từ sequence.

Do đó câu hỏi thú vị là:

> **Feature engineering có cung cấp information mới, hay chỉ cung cấp một representation dễ học hơn?**

Đây là distinction rất quan trọng.

Ví dụ:

```text
Raw:
x(t-3), x(t-2), x(t-1), x(t)

        ↓ Transformer

Model tự học temporal relationship
```

so với:

```text
Raw + Δx:
x(t-3), x(t-2), x(t-1), x(t)
Δx(t-2), Δx(t-1), Δx(t)

        ↓ Transformer

Một số relationship được biểu diễn explicit
```

Feature engineering không nhất thiết tạo thêm information mới.

Nó có thể chỉ làm:

$$
\boxed{
\text{Learning problem}
\rightarrow
\text{easier optimization problem}
}
$$

---

# 7. Vì vậy cần đánh giá cả hiệu quả và chi phí

Không nên chỉ nhìn RMSE.

Ví dụ:

| Model      | Features | RMSE | Params | Training time |
| ---------- | -------: | ---: | -----: | ------------: |
| Raw        |       10 |  100 |   500K |         5 min |
| Engineered |       40 |   95 |   500K |         7 min |
| Engineered |      100 | 94.5 |   500K |        15 min |

Feature engineering 100 feature chỉ cải thiện:

$$
100\rightarrow94.5
$$

nhưng computational cost tăng rất nhiều.

Khi đó chưa chắc 100 feature là lựa chọn tốt.

Ta có thể quan tâm đến:

$$
\text{Efficiency}
=
\frac{\text{Performance Gain}}
{\text{Additional Cost}}
$$

---

# 8. Một tiêu chí rất quan trọng: Generalization

Giả sử:

$$
RMSE_{train}
\downarrow
$$

nhưng:

$$
RMSE_{val}
\uparrow
$$

thì feature engineering có thể đang làm model **overfit**.

Ví dụ:

```text
                Train RMSE    Val RMSE

Raw                70           100
Engineered         45           110
```

Engineered model học training data tốt hơn nhưng generalization kém hơn.

Do đó:

> **Feature engineering chỉ được xem là thành công nếu improvement xuất hiện trên validation/test, không phải chỉ training.**

Và với time series, test set nên **LOCK** và chỉ dùng một lần ở cuối.

---

# 9. Cần kiểm tra leakage cho từng engineered feature

Đây là phần đặc biệt quan trọng trong time series.

Ví dụ muốn tạo rolling mean:

$$
MA_t
=
\frac{1}{w}
\sum_{i=0}^{w-1}x_{t-i}
$$

Cái này hợp lệ vì chỉ sử dụng:

$$
x_t,x_{t-1},\ldots
$$

Nhưng nếu vô tình dùng:

$$
MA_t
=
\frac{1}{w}
\sum_{i=-k}^{w-k}x_{t+i}
$$

thì có thể chứa:

$$
x_{t+1},x_{t+2},\ldots
$$

→ **future leakage**.

Đặc biệt phải kiểm tra:

* rolling statistics;
* interpolation;
* normalization;
* aggregation;
* target-derived features;
* lag features;
* resampling.

---

# 10. Một cách đánh giá rất mạnh: Feature Engineering Ablation

Sau khi có engineered feature set:

$$
E=\{e_1,e_2,\ldots,e_k\}
$$

train:

$$
M_{all}
$$

sau đó lần lượt bỏ:

$$
M_{-e_i}
$$

và tính:

$$
\Delta_i
=
RMSE(M_{-e_i})-RMSE(M_{all})
$$

Ví dụ:

| Engineered feature     | $\Delta RMSE$ |
| ---------------------- | ------------: |
| hour sin/cos           |          +5.2 |
| temperature difference |          +2.8 |
| rolling mean           |          +1.1 |
| rolling std            |          +0.2 |
| rolling max            |          −0.1 |

Ta có:

```text
hour encoding        → rất hữu ích
temperature Δ        → hữu ích
rolling mean         → có ích
rolling std          → ít đóng góp
rolling max          → không cần
```

Như vậy sau feature engineering lại có thể thực hiện **feature selection lần 2**.

---

# 11. Một pipeline hoàn chỉnh hơn

Với Transformer time-series regression, mình khuyên tư duy pipeline như sau:

```text
Raw Dataset
     │
     ▼
Data Quality
     │
     ▼
Train / Val / Test Split
     │
     ▼
Feature Selection
     │
     ▼
Selected Raw Features
     │
     ├──────────────► Baseline Transformer
     │                      │
     │                      ▼
     │                   RMSE_raw
     │
     ▼
Feature Engineering
     │
     ├── Temporal
     ├── Lag
     ├── Difference
     ├── Rolling
     └── Domain-specific
     │
     ▼
Engineered Features
     │
     ▼
Same Transformer
     │
     ▼
RMSE_engineered
     │
     ▼
Ablation Study
     │
     ▼
Minimal Useful Representation
```

Và cuối cùng ta muốn tìm:

$$
\boxed{
\mathcal{F}^{*}_{eng}
=
\arg\min_{\mathcal{F}}
RMSE_{val}
}
$$

nhưng đồng thời:

$$
|\mathcal{F}^{*}_{eng}|
\quad\text{nhỏ}
$$

và không có leakage.

---

## 12. Nếu đặt thành một nghiên cứu thực nghiệm

Bạn có thể xây dựng câu hỏi nghiên cứu rất rõ:

> **RQ1:** Feature selection loại bỏ được bao nhiêu information không cần thiết?

> **RQ2:** Feature engineering có cải thiện khả năng dự báo so với selected raw features không?

> **RQ3:** Nhóm feature engineering nào đóng góp nhiều nhất?

> **RQ4:** Feature engineering cải thiện representation hay chỉ làm tăng model capacity?

> **RQ5:** Có thể đạt performance tương đương với một representation nhỏ hơn không?

Từ đó có thể xây dựng 4 model:

$$
M_0 =
Transformer(\mathcal{F}_{raw})
$$

$$
M_1 =
Transformer(\mathcal{F}_{selected})
$$

$$
M_2 =
Transformer(\mathcal{F}_{selected+engineered})
$$

$$
M_3 =
Transformer(\mathcal{F}_{minimal})
$$

và so sánh:

$$
M_0
\rightarrow
M_1
\rightarrow
M_2
\rightarrow
M_3
$$

Đây là cách rất tốt để chứng minh một cách có hệ thống rằng **dữ liệu nào cần thiết → feature nào cần thiết → feature representation nào giúp Transformer học tốt hơn → và cuối cùng có thể giảm dữ liệu/feature mà không làm mất predictive performance**.
