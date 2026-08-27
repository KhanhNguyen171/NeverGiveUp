# Chương 1 — Adaptive Subdivision: Chia nhỏ nơi phức tạp

## 1.1. Ý tưởng trực quan

Hãy tưởng tượng ta có một hình dạng rất phức tạp:

```text
                  ╭──────╮
              ╭───╯      ╰──╮
           ╭──╯              ╰─╮
───────────╯                    ╰────
```

Nếu muốn biểu diễn hình này bằng các đoạn thẳng, ta có hai lựa chọn.

**Cách 1 — Chia đều**

```text
|----|----|----|----|----|----|----|----|
```

Mọi nơi đều được chia nhỏ như nhau.

Vấn đề là những vùng gần như thẳng không cần quá nhiều điểm:

```text
───────────────
```

Trong khi vùng cong mạnh lại cần rất nhiều điểm:

```text
       ╭────╮
     ╭─╯    ╰─╮
```

Vậy thay vì chia đều, ta đặt câu hỏi:

> **"Chỗ nào phức tạp thì có cần chia nhỏ hơn không?"**

Đây chính là ý tưởng của **Adaptive Subdivision**.

```text
Vùng đơn giản
──────────────
      ↓
    giữ nguyên

Vùng phức tạp
────╭────╮────
    ↓
  chia nhỏ
```

---

## 1.2. Từ "chia nhỏ" đến "chia nhỏ có chọn lọc"

Subdivision thông thường:

```text
        ┌───────────────┐
        │               │
        │     Shape     │
        │               │
        └───────────────┘
                 ↓
        chia tất cả như nhau
                 ↓
        ┌───┬───┬───┬───┐
        ├───┼───┼───┼───┤
        ├───┼───┼───┼───┤
        └───┴───┴───┴───┘
```

Adaptive Subdivision:

```text
        ┌───────────────┐
        │               │
        │    complex    │
        │       ╭──╮    │
        │       ╰──╯    │
        └───────────────┘
                 ↓
        kiểm tra từng vùng
                 ↓
       ┌─────────┬─┬─┬─┐
       │         │ │ │ │
       │ simple  ├─┼─┼─┤
       │         │ │ │ │
       └─────────┴─┴─┴─┘
```

Ta không cần độ phân giải cao ở mọi nơi.

Điều quan trọng là:

$$
\boxed{
\text{Simple region} \rightarrow \text{coarse}
}
$$

$$
\boxed{
\text{Complex region} \rightarrow \text{fine}
}
$$

---

## 1.3. Làm sao biết một vùng "phức tạp"?

Đây là phần quan trọng nhất của Adaptive Subdivision.

Giả sử ta đang xét một vùng $R$.

Ta cần một cách để trả lời:

> **"Vùng này đã đủ chính xác chưa?"**

Ta có thể tính một đại lượng biểu diễn sai số:

$$
E(R)
$$

Trong đó $E(R)$ càng lớn nghĩa là vùng đó càng khó xấp xỉ.

Ta đặt một ngưỡng:

$$
\varepsilon
$$

Sau đó:

$$
\boxed{
E(R)\leq\varepsilon
\Rightarrow
\text{dừng}
}
$$

và:

$$
\boxed{
E(R)>\varepsilon
\Rightarrow
\text{chia nhỏ tiếp}
}
$$

Có thể hình dung rất đơn giản:

```text
              Một vùng
                 │
                 ▼
           "Đã đủ chính xác?"
             /          \
           YES           NO
            │             │
            ▼             ▼
           STOP       SUBDIVIDE
                          │
                    ┌─────┴─────┐
                    ▼           ▼
                  vùng con    vùng con
```

Đây chính là **adaptive loop**.

---

## 1.4. Ví dụ với một đường cong

Giả sử ta có:

```text
A────────────────────B
```

Nhưng đường cong thật lại là:

```text
A──────╭──────╮──────B
       ╰──────╯
```

Nếu dùng đoạn thẳng $AB$, sai số khá lớn.

Ta chia đôi:

```text
A────────M────────B
```

Bây giờ kiểm tra hai đoạn:

```text
A──────M
```

và:

```text
M──────B
```

Có thể đoạn thứ nhất gần như thẳng:

```text
A────────M
   ↑
 đơn giản
```

→ **Dừng.**

Nhưng đoạn thứ hai vẫn cong:

```text
M───────╭────B
        ↑
     phức tạp
```

→ **Chia tiếp.**

Cuối cùng:

```text
A────M────N──P──Q────B
```

Ta có nhiều điểm ở vùng cong và ít điểm ở vùng thẳng.

Đây là điểm quan trọng nhất cần nhớ:

> **Adaptive Subdivision không cố làm mọi nơi thật chi tiết. Nó chỉ tăng độ chi tiết ở nơi cần thiết.**

---

## 1.5. Adaptive Subdivision có thể tạo thành một "cây"

Mỗi lần chia một vùng thành các vùng nhỏ hơn, ta có thể hình dung như một cây:

```text
                         R
                    /    |    \
                  R₁     R₂     R₃
                 / \           / \
               R₄  R₅        R₆  R₇
```

Một nhánh có thể dừng sớm:

```text
R
├── R₁ → STOP
├── R₂
│   ├── R₄ → STOP
│   └── R₅ → STOP
└── R₃
    ├── R₆
    │   ├── ...
    │   └── ...
    └── R₇ → STOP
```

Điều này giải thích tại sao gọi là **adaptive**:

Không phải mọi vùng đều đi qua cùng số lần subdivision.

---

## 1.6. Tại sao không chia tất cả thật nhỏ?

Giả sử ta có:

```text
100 vùng
```

Nhưng chỉ có:

```text
10 vùng phức tạp
```

Nếu chia tất cả:

```text
100 vùng
     ↓
100 × nhiều phép tính
```

Trong khi adaptive subdivision có thể làm:

```text
90 vùng đơn giản
     ↓
giữ nguyên

10 vùng phức tạp
     ↓
chia nhỏ
```

Ta tiết kiệm được computation.

Do đó có một nguyên tắc rất quan trọng:

$$
\boxed{
\text{Không phải mọi vùng đều đáng để đầu tư cùng một lượng computation.}
}
$$

---

## 1.7. Nhưng Adaptive Subdivision cũng có giới hạn

Có một vấn đề:

> Nếu không gian có quá nhiều chiều, số vùng có thể tăng rất nhanh.

Ví dụ mỗi chiều chia thành $2$ phần.

### 1 chiều

$$
2
$$

### 2 chiều

$$
2^2=4
$$

### 3 chiều

$$
2^3=8
$$

### 10 chiều

$$
2^{10}=1024
$$

Nếu tiếp tục subdivision nhiều level, số vùng tăng cực nhanh:

$$
N\propto 2^{dL}
$$

với:

* $d$: số chiều;
* $L$: số level subdivision.

Đây là một trong những lý do các phương pháp dựa trên sampling trở nên hấp dẫn trong không gian nhiều chiều.

---

# Chương 2 — Monte Carlo Integration: Ném điểm ngẫu nhiên để tính

## 2.1. Một cách tiếp cận hoàn toàn khác

Giả sử ta có một hình rất khó tính diện tích:

```text
┌────────────────────────┐
│         ╭──╮           │
│      ╭──╯  ╰──╮        │
│    ╭─╯        ╰─╮      │
│────╯            ╰──────│
└────────────────────────┘
```

Ta có thể cố tìm chính xác biên của hình.

Nhưng có một ý tưởng khác:

> **Nếu không tính được trực tiếp, hãy lấy thật nhiều mẫu và dùng thống kê để ước lượng.**

Ta chọn một vùng bao quanh hình:

```text
┌────────────────────────┐
│                        │
│         SHAPE          │
│                        │
└────────────────────────┘
```

Sau đó "ném" các điểm ngẫu nhiên:

```text
┌────────────────────────┐
│ •       •      •       │
│       • ╭──╮           │
│   • ╭──╯  ╰──╮   •     │
│ •  ╭╯   •    ╰─╮       │
│────╯            ╰──•───│
│      •          •      │
└────────────────────────┘
```

Mỗi điểm chỉ cần trả lời:

```text
Điểm này ở trong hay ngoài?
```

---

## 2.2. Từ điểm ngẫu nhiên đến diện tích

Giả sử:

$$
N=1000
$$

điểm được ném vào bounding box.

Trong đó:

$$
N_{\text{inside}}=750
$$

điểm nằm bên trong hình.

Khi đó tỷ lệ điểm bên trong là:

$$
\frac{N_{\text{inside}}}{N}
=
\frac{750}{1000}
=
0.75
$$

Nếu bounding box có diện tích:

$$
A_{\text{box}}=100
$$

thì ta ước lượng:

$$
A_{\text{shape}}
\approx
100\times0.75
=
75.
$$

Công thức tổng quát:

$$
\boxed{
A
\approx
A_{\text{box}}
\frac{N_{\text{inside}}}{N}
}
$$

Điều thú vị là:

> Ta **không cần biết chính xác hình dạng bên trong** để ước lượng diện tích.

---

## 2.3. Ví dụ kinh điển: tính $\pi$

Đây là ví dụ rất dễ hình dung.

Ta đặt một đường tròn bên trong hình vuông:

```text
        ┌─────────────┐
        │   •     •   │
        │    ╭───╮    │
        │ • ╱     ╲ • │
        │  │       │  │
        │ • ╲     ╱ • │
        │    ╰───╯    │
        │   •     •   │
        └─────────────┘
```

Hình vuông có diện tích:

$$
4
$$

Đường tròn bán kính $1$ có diện tích:

$$
\pi
$$

Do đó:

$$
\frac{\pi}{4}
=
\frac{N_{\text{inside}}}{N}.
$$

Suy ra:

$$
\boxed{
\pi
\approx
4
\frac{N_{\text{inside}}}{N}
}
$$

Ví dụ:

$$
N=1,000,000
$$

và:

$$
N_{\text{inside}}=785,398
$$

thì:

$$
\pi
\approx
4\frac{785398}{1000000}
\approx
3.141592.
$$

Ta vừa ước lượng $\pi$ bằng cách **ném điểm**.

---

## 2.4. Nhưng tại sao cách này lại liên quan đến tích phân?

Đây là bước chuyển quan trọng.

Giả sử ta cần tính:

$$
I=\int_D f(x)\,dx.
$$

Thay vì tính toàn bộ tích phân trực tiếp, ta lấy các điểm:

$$
X_1,X_2,\ldots,X_N.
$$

Tại mỗi điểm:

$$
f(X_1),f(X_2),\ldots,f(X_N).
$$

Sau đó lấy trung bình:

$$
\frac{1}{N}
\sum_{i=1}^{N}f(X_i).
$$

Nếu $X_i$ được lấy đều trên $D$, ta có:

$$
\boxed{
\hat I_N
=
V_D
\frac{1}{N}
\sum_{i=1}^{N}f(X_i)
}
$$

Trong đó:

$$
V_D
$$

là thể tích/diện tích của miền $D$.

Có thể nhớ bằng workflow:

```text
Tích phân khó
     │
     ▼
Chọn miền D
     │
     ▼
Lấy random samples
     │
     ▼
Tính f(Xᵢ)
     │
     ▼
Lấy average
     │
     ▼
Ước lượng tích phân
```

---

## 2.5. Trực giác về "average"

Đây là điểm người mới thường khó hiểu.

Giả sử hàm:

```text
f(x)

      ╭────╮
      │    ╰────
──────╯──────────── x
```

Thay vì tính diện tích chính xác dưới đường cong, ta hỏi:

> **Nếu lấy rất nhiều điểm ngẫu nhiên trên trục $x$, giá trị trung bình của $f(x)$ khoảng bao nhiêu?**

Nếu trung bình là:

$$
\bar f
$$

và độ dài miền là:

$$
L,
$$

thì:

$$
\text{Area}
\approx
L\bar f.
$$

Monte Carlo về bản chất đang biến:

```text
diện tích dưới đường cong
```

thành:

```text
chiều rộng × giá trị trung bình
```

---

## 2.6. Tại sao cần rất nhiều điểm?

Nếu chỉ lấy:

```text
• • • • •
```

kết quả có thể khá sai.

Nếu lấy:

```text
• • • • • • • • • • • • • • • •
```

kết quả ổn định hơn.

Nếu lấy:

```text
10 triệu điểm
```

ước lượng thường tốt hơn nữa.

Sai số Monte Carlo giảm xấp xỉ:

$$
\boxed{
O\left(\frac{1}{\sqrt N}\right)
}
$$

Điều này có một hệ quả rất quan trọng.

Nếu muốn sai số giảm:

$$
10\times
$$

thì cần khoảng:

$$
100\times
$$

số mẫu.

```text
100 samples
     ↓
10,000 samples
     ↓
~ giảm sai số 10 lần
```

Vì vậy Monte Carlo **dễ triển khai nhưng không hội tụ nhanh**.

---

## 2.7. Vì sao Monte Carlo hữu ích trong nhiều chiều?

Hãy tưởng tượng ta muốn chia một không gian:

```text
1D → đoạn
2D → lưới
3D → khối
10D → ???
```

Trong 10 chiều, việc xây một lưới đầy đủ rất nhanh trở nên đắt đỏ.

Monte Carlo không cần xây toàn bộ lưới.

Nó chỉ cần:

```text
X₁
X₂
X₃
...
Xₙ
```

Sau đó đánh giá từng điểm.

Đây là lý do Monte Carlo đặc biệt hữu ích khi bài toán có **nhiều chiều**.

---

# 3. Hai ý tưởng nhìn cạnh nhau

Đây là phần nên giữ lại trong báo cáo vì nó giúp người đọc kết nối hai chương.

### Adaptive Subdivision

```text
          DOMAIN
             │
             ▼
       Chia thành vùng
             │
             ▼
      Kiểm tra độ phức tạp
             │
       ┌─────┴─────┐
       ▼           ▼
     EASY        HARD
       │           │
      STOP      CHIA TIẾP
```

Tư duy:

> **"Chỗ nào khó thì zoom vào."**

---

### Monte Carlo

```text
          DOMAIN
             │
             ▼
       Random Sampling
             │
             ▼
       • • • • • • •
             │
             ▼
       Evaluate f(Xᵢ)
             │
             ▼
          Average
             │
             ▼
          Estimate
```

Tư duy:

> **"Không cần hiểu toàn bộ, hãy lấy đủ mẫu để ước lượng."**

---

# 4. Điểm chung quan trọng nhất

Hai phương pháp tưởng như rất khác nhau nhưng có một tư tưởng chung:

$$
\boxed{
\text{Không nên tiêu tốn computation giống nhau ở mọi nơi.}
}
$$

Adaptive Subdivision:

$$
\boxed{
\text{Complex region}
\rightarrow
\text{more subdivision}
}
$$

Monte Carlo:

$$
\boxed{
\text{More samples}
\rightarrow
\text{better estimate}
}
$$

Và khi kết hợp tư tưởng thích nghi với Monte Carlo:

```text
Random samples
      ↓
Đánh giá uncertainty
      ↓
Tìm vùng chưa chắc chắn
      ↓
Lấy thêm samples
      ↓
Ước lượng lại
```

ta có tư tưởng **Adaptive Sampling**.

---

# 5. So sánh để ghi nhớ

|               | Adaptive Subdivision                       | Monte Carlo                         |
| ------------- | ------------------------------------------ | ----------------------------------- |
| Hình dung     | Zoom vào vùng khó                          | Ném điểm ngẫu nhiên                 |
| Cách làm      | Chia nhỏ                                   | Lấy mẫu                             |
| Tập trung vào | Độ phân giải                               | Số lượng mẫu                        |
| Quyết định    | Có chia tiếp không?                        | Lấy thêm mẫu không?                 |
| Sai số        | Sai số cục bộ                              | Sai số thống kê                     |
| Điểm mạnh     | Hình học/cấu trúc có vùng phức tạp rõ ràng | Tích phân và không gian nhiều chiều |
| Điểm yếu      | Có thể bùng nổ số vùng                     | Hội tụ chậm $O(N^{-1/2})$         |

---

# 6. Ý tưởng cần nhớ sau hai chương

Không cần nhớ hàng loạt công thức. Chỉ cần giữ lại **hai hình ảnh**:

```text
Adaptive Subdivision

        ┌─────────────┐
        │             │
        │     ╭─╮     │
        │    ╱   ╲    │
        │   ╱     ╲   │
        └─────────────┘
              ↓
       "Zoom chỗ khó"
```

và:

```text
Monte Carlo

        ┌─────────────┐
        │ •    •   •  │
        │    • ╭─╮    │
        │ •   ╱ •╲ •  │
        │   •╲   ╱    │
        │ •    •   •  │
        └─────────────┘
              ↓
        "Ném điểm + đếm"
```

Từ đó có thể cô đọng thành:

$$
\boxed{
\text{Adaptive Subdivision}
=
\text{chia nhỏ nơi phức tạp}
}
$$

$$
\boxed{
\text{Monte Carlo}
=
\text{lấy mẫu để ước lượng}
}
$$

và tư tưởng chung:

$$
\boxed{
\text{Efficient computation}
=
\text{đưa tài nguyên tính toán đến nơi cần thiết}
}
$$

Đây nên là **xương sống của hai chương**; các phần toán học phía sau chỉ dùng để giải thích *tại sao* hai ý tưởng trên hoạt động, thay vì biến báo cáo thành một chương thuần toán.
