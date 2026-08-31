Trong **Transformer cho bài toán Time Series Regression**, *sliding window* là bước biến một chuỗi thời gian dài thành nhiều **sample có độ dài cố định** để Transformer có thể xử lý.

Điểm quan trọng nhất là:

> **Transformer không trực tiếp học từ toàn bộ chuỗi thời gian dài. Ta cắt chuỗi thành các cửa sổ (window), mỗi window là một sample đầu vào và đi kèm một target cần dự đoán.**

---

# 1. Bài toán Time Series Regression

Giả sử ta có chuỗi thời gian:

$$
x_1,x_2,x_3,\ldots,x_T
$$

và muốn dự đoán giá trị tương lai:

$$
y_{t+H}
$$

Trong đó:

* $t$: thời điểm hiện tại
* $H$: prediction horizon
* $y_{t+H}$: giá trị cần dự đoán trong tương lai.

Ví dụ:

> Dùng dữ liệu **6 giờ vừa qua** để dự đoán lượng điện tiêu thụ **10 phút tiếp theo**.

Nếu dữ liệu được ghi nhận mỗi 10 phút:

$$
6\text{ giờ} = 36 \text{ time steps}
$$

Do đó:

$$
L=36
$$

và:

$$
H=1
$$

---

# 2. Sliding Window là gì?

Giả sử chuỗi đơn giản:

```text
t1  t2  t3  t4  t5  t6  t7  t8  t9  t10
10  12  15  13  18  20  22  25  24  27
```

Ta chọn:

* `window_size = 4`
* `horizon = 1`

Window đầu tiên:

```text
Input
[t1, t2, t3, t4]
 10  12  15  13
             ↓
           Target
             t5
             18
```

Window tiếp theo dịch sang phải **một bước**:

```text
Input
[t2, t3, t4, t5]
 12  15  13  18
             ↓
           Target
             t6
             20
```

Tiếp tục:

```text
[t3, t4, t5, t6] → t7
[t4, t5, t6, t7] → t8
[t5, t6, t7, t8] → t9
...
```

Đó chính là **Sliding Window**.

---

# 3. Công thức tổng quát

Cho chuỗi:

$$
X = [x_1,x_2,\ldots,x_T]
$$

với:

* $L$: lookback/window size
* $H$: prediction horizon.

Sample thứ $i$ được tạo bởi:

$$
X^{(i)}
=
[x_i,x_{i+1},\ldots,x_{i+L-1}]
$$

Target:

$$
y^{(i)} = y_{i+L-1+H}
$$

Ví dụ:

$$
L=4,\quad H=1
$$

thì:

$$
X^{(1)}=[x_1,x_2,x_3,x_4]
$$

và:

$$
y^{(1)}=y_5
$$

Sample thứ hai:

$$
X^{(2)}=[x_2,x_3,x_4,x_5]
$$

và:

$$
y^{(2)}=y_6
$$

---

# 4. Tại sao Transformer cần Sliding Window?

Transformer nhận input dạng:

$$
X \in \mathbb{R}^{B\times L\times F}
$$

Trong đó:

* $B$: batch size
* $L$: số time steps trong một window
* $F$: số features tại mỗi time step.

Ví dụ:

```text
Batch = 64
Lookback = 36
Features = 31
```

thì input Transformer có shape:

$$
X\in\mathbb{R}^{64\times36\times31}
$$

Có thể hiểu:

```text
Batch
│
├── Sample 1
│   ├── t1  → 31 features
│   ├── t2  → 31 features
│   ├── ...
│   └── t36 → 31 features
│
├── Sample 2
│   ├── t2
│   ├── t3
│   ├── ...
│   └── t37
│
└── ...
```

Transformer sẽ dùng **36 time steps** để học quan hệ temporal:

$$
x_{t-35},...,x_{t}
\rightarrow
\hat y_{t+1}
$$

---

# 5. Sliding Window thực chất đang làm gì?

Có thể xem nó như một phép biến đổi:

$$
\boxed{
\text{Long Time Series}
\rightarrow
\text{Fixed-Length Sequences}
}
$$

Ví dụ chuỗi có 10,000 timestamps:

```text
x1 x2 x3 x4 x5 x6 ... x9999 x10000
```

Transformer không nhất thiết nhận:

```text
[x1, x2, ..., x10000]
```

mà Dataset biến thành:

```text
Sample 1: x1   → x36   → y37
Sample 2: x2   → x37   → y38
Sample 3: x3   → x38   → y39
...
Sample N: x9964 → x9999 → y10000
```

Với:

$$
L=36,\quad H=1
$$

số sample lý thuyết là:

$$
N=T-L-H+1
$$

Nếu:

$$
T=10000
$$

thì:

$$
N=10000-36-1+1=9964
$$

---

# 6. Window size chính là "Transformer nhìn lại bao xa"

Đây là một khái niệm rất quan trọng.

Giả sử:

$$
L=36
$$

thì Transformer chỉ nhìn:

$$
36\text{ time steps}
$$

quá khứ để dự đoán target.

Nếu sampling = 10 phút:

$$
36\times10=360\text{ phút}=6\text{ giờ}
$$

Vì vậy:

```text
Lookback = 36
       ↓
Transformer nhìn 6 giờ quá khứ
       ↓
dự đoán
       ↓
10 phút tiếp theo
```

Nếu:

$$
L=72
$$

thì:

```text
72 × 10 phút = 12 giờ
```

Nếu:

$$
L=144
$$

thì:

```text
144 × 10 phút = 24 giờ
```

Do đó có thể xem:

> **Lookback là receptive field theo chiều thời gian của mô hình.**

---

# 7. Window size ảnh hưởng đến Transformer như thế nào?

Đây là điểm đặc biệt quan trọng hơn so với CNN/RNN.

Self-Attention có độ phức tạp theo chiều sequence khoảng:

$$
O(L^2)
$$

Do đó:

### Window = 36

$$
36^2=1296
$$

attention interactions.

### Window = 144

$$
144^2=20736
$$

Tăng lên:

$$
\frac{144^2}{36^2}=16
$$

lần.

Vì vậy tăng:

```text
L = 36 → 144
```

không đơn giản là:

```text
gấp 4 dữ liệu
```

mà attention computation có thể tăng khoảng:

```text
4² = 16 lần
```

Đây là một trong những lý do sliding window phải được thiết kế cẩn thận khi xây dựng Transformer cho time series.

---

# 8. Input của Transformer không phải chỉ là target

Giả sử mỗi timestamp có nhiều feature:

```text
timestamp
    │
    ├── temperature
    ├── humidity
    ├── pressure
    ├── hour_sin
    ├── hour_cos
    ├── ...
    └── Appliances
```

Tại mỗi thời điểm:

$$
x_t\in\mathbb{R}^{F}
$$

Sliding window tạo:

$$
X_t=
\begin{bmatrix}
x_{t-L+1}\\
x_{t-L+2}\\
\vdots\\
x_t
\end{bmatrix}
\in\mathbb{R}^{L\times F}
$$

Sau đó:

$$
X_t
\rightarrow
\text{Transformer}
\rightarrow
\hat y_{t+H}
$$

Ví dụ:

$$
X_t\in\mathbb{R}^{36\times31}
$$

Transformer nhận 36 vectors, mỗi vector có 31 features.

---

# 9. Sliding Window và Temporal Order

Một điều rất quan trọng:

**Không được shuffle time series trước khi tạo window.**

Chuỗi phải giữ:

```text
t1 → t2 → t3 → t4 → ...
```

Bởi vì:

$$
x_t
$$

có ý nghĩa phụ thuộc vào vị trí thời gian.

Ví dụ:

```text
[t1, t2, t3, t4]
```

khác hoàn toàn:

```text
[t4, t2, t1, t3]
```

Transformer có thể sử dụng positional encoding để biết vị trí:

$$
X' = X + PE
$$

Nhưng positional encoding **không khôi phục được thứ tự nếu ta đã phá vỡ temporal ordering trong Dataset**.

---

# 10. Một vấn đề rất dễ sai: Data Leakage

Giả sử ta chia:

```text
Train | Validation | Test
```

thì **không nên tạo sliding window trên toàn bộ dataset rồi mới chia** một cách ngây thơ.

Ví dụ:

```text
Train                 Validation
───────────────────────────────
t1 ... t100            t101 ...
```

Nếu tạo window trước:

```text
[t66 ... t101]
```

thì sample này chứa:

```text
t66 ... t100 → Train
t101         → Validation
```

Tùy cách định nghĩa sample/target, điều này có thể làm ranh giới split trở nên khó kiểm soát và gây leakage.

Cách an toàn là:

```text
Raw chronological data
          │
          ↓
Train / Validation / Test
          │
          ↓
Create windows
          │
          ↓
Dataset
```

và đặc biệt:

> **Scaler phải được fit trên Train trước, sau đó dùng scaler đó cho Validation/Test.**

---

# 11. Có một nuance quan trọng ở ranh giới Train/Validation

Trong forecasting thực tế, có một câu hỏi tinh tế:

> Sample validation có được sử dụng các observation nằm trước thời điểm validation hay không?

Ví dụ:

```text
Train
t1 ... t100

Validation
t101 ... t120
```

Muốn dự đoán:

$$
y_{101}
$$

thì về mặt forecasting thực tế, ta hoàn toàn có thể sử dụng:

$$
x_{65},...,x_{100}
$$

vì đây là lịch sử đã tồn tại trước validation.

Do đó có hai cách thiết kế:

### Strict split

Window validation chỉ sử dụng dữ liệu validation:

```text
Validation sample:
[t101 ... t136] → y137
```

### Historical-context split

Validation được phép sử dụng lịch sử Train:

```text
[t65 ... t100] → y101
```

Cách thứ hai thường phản ánh **deployment forecasting** tốt hơn, nhưng cần thiết kế Dataset/split rõ ràng để tránh sử dụng thông tin tương lai.

---

# 12. Sliding Window với nhiều bước dự đoán

Không phải lúc nào cũng:

$$
H=1
$$

Ta có thể dự đoán nhiều bước:

$$
[x_{t-L+1},...,x_t]
\rightarrow
[y_{t+1},y_{t+2},...,y_{t+H}]
$$

Ví dụ:

```text
36 time steps
       ↓
 Transformer
       ↓
next 6 time steps
```

Khi đó:

$$
Y_t=
[y_{t+1},...,y_{t+6}]
$$

và output:

$$
\hat Y_t\in\mathbb{R}^{6}
$$

Đây gọi là **multi-step forecasting**.

Trong khi:

$$
\hat y_{t+1}
$$

là **single-step forecasting**.

---

# 13. Hình dung toàn bộ pipeline

Có thể nhớ pipeline bằng sơ đồ:

```text
Raw Time Series
─────────────────────────────────────────────→ time

t1  t2  t3  t4  t5  t6  t7  t8  ...

        Sliding Window
             ↓

[t1 t2 t3 t4] → y5
    [t2 t3 t4 t5] → y6
        [t3 t4 t5 t6] → y7
            [t4 t5 t6 t7] → y8
                    ...

             ↓

       Tensor Dataset

X.shape = [N, L, F]
Y.shape = [N, 1]

             ↓

        Transformer

[B, L, F]
    ↓
Input Projection
    ↓
Positional Encoding
    ↓
Transformer Encoder
    ↓
Pooling / Last Token
    ↓
Regression Head
    ↓
ŷ
```

---

# 14. Liên hệ trực tiếp với Transformer Regression

Một kiến trúc đơn giản:

$$
X\in\mathbb{R}^{B\times L\times F}
$$

đầu tiên project feature:

$$
Z=XW_e+b_e
$$

với:

$$
Z\in\mathbb{R}^{B\times L\times d_{\text{model}}}
$$

Sau đó thêm positional information:

$$
Z'=Z+PE
$$

rồi:

$$
Z'
\rightarrow
\text{Transformer Encoder}
\rightarrow
H
$$

Cuối cùng lấy representation:

$$
h_t = H[:, -1, :]
$$

và regression head:

$$
\hat y = h_tW_o+b_o
$$

Toàn bộ bài toán:

$$
\boxed{
X_{t-L+1:t}
\rightarrow
\text{Transformer}
\rightarrow
\hat y_{t+H}
}
$$

---

# 15. Ba tham số cần phân biệt

Khi xây dựng sliding window, đừng nhầm ba khái niệm:

| Tham số          | Ý nghĩa                       |
| ---------------- | ----------------------------- |
| **Lookback $L$** | Nhìn lại bao nhiêu time steps |
| **Stride $S$**   | Window dịch bao nhiêu bước    |
| **Horizon $H$**  | Dự đoán xa bao nhiêu bước     |

Ví dụ:

$$
L=36,\quad S=1,\quad H=1
$$

nghĩa là:

```text
36 bước quá khứ
      ↓
dự đoán 1 bước tương lai
      ↓
window dịch 1 bước
```

Nếu:

$$
S=6
$$

thì:

```text
Window 1: t1  → t36
Window 2: t7  → t42
Window 3: t13 → t48
```

Số sample giảm nhưng các window ít overlap hơn.

---

## 16. Ý tưởng cốt lõi cần nhớ

Có thể cô đọng toàn bộ sliding window cho Transformer Time Series Regression thành:

$$
\boxed{
\text{Sliding Window}
=
\text{chuyển chuỗi thời gian}
\rightarrow
\text{các sequence có độ dài cố định}
}
$$

Mỗi sample có dạng:

$$
\boxed{
X_t=[x_{t-L+1},...,x_t]
\quad\rightarrow\quad
y_{t+H}
}
$$

Sau khi tạo window:

$$
\boxed{
X\in\mathbb{R}^{N\times L\times F}
}
$$

Transformer xử lý **chiều $L$ như sequence dimension**, trong đó mỗi timestamp là một token/vector feature:

```text
                    Transformer
                        │
                        ↓
t-L+1 ──┐
t-L+2 ──┤
t-L+3 ──┤──→ Self-Attention ──→ Temporal representation
  ...   │
t-1   ──┤
t     ──┘
                        │
                        ↓
                     ŷ(t+H)
```

**Nói ngắn gọn:** Sliding window quyết định **Transformer được phép nhìn bao nhiêu lịch sử**, còn `horizon` quyết định **mô hình phải dự đoán xa bao nhiêu về tương lai**. Đây là một trong những thiết kế quan trọng nhất của bài toán Transformer Time Series Regression.
