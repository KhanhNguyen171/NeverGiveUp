# 4. Ablation Study — Vì sao từng thay đổi của ConvNeXt có tác dụng?

Ablation Study của paper có mục đích trả lời:

> **Từ một ResNet hiện đại, những thay đổi nào thực sự tạo ra ConvNeXt mạnh?**

Không nên nhìn ConvNeXt như một kiến trúc xuất hiện hoàn chỉnh ngay từ đầu. Hãy nhìn quá trình:

```text
ResNet-50
   │
   ▼
+ Modern Training
   │
   ▼
+ Macro Design
   │
   ▼
+ ResNeXt-ify
   │
   ▼
+ Inverted Bottleneck
   │
   ▼
+ Large Kernel
   │
   ▼
+ Micro Design
   │
   ▼
ConvNeXt
```

Mỗi bước là một **hypothesis** được kiểm chứng bằng thực nghiệm.

---

# 4.1. Baseline: ResNet hiện đại

Điểm xuất phát không phải ResNet-50 nguyên bản.

Tác giả trước tiên áp dụng training recipe hiện đại:

```text
Original ResNet
      ↓
Modern Training Techniques
      ↓
ResNet-50 baseline
```

Điều này rất quan trọng về phương pháp nghiên cứu.

Nếu ConvNeXt tốt hơn một ResNet được train bằng recipe cũ thì chưa thể kết luận:

$$\text{Architecture}_{ConvNeXt}

\gt

\text{Architecture}_{ResNet}$$

vì sự khác biệt có thể đến từ training.

Do đó tác giả cố gắng tạo:

$$\boxed{\text{Fair Baseline}}$$

trước khi thay đổi architecture.

---

# 4.2. Macro Design

Bước đầu tiên là thay đổi **kiến trúc ở cấp độ toàn mạng**.

ConvNeXt học cách tổ chức stage từ hierarchical Transformer.

Kiến trúc có dạng:

```text
Input
  │
  ▼
4×4 Conv / stride 4
  │
  ▼
Stage 1
  │
  ▼
Downsample
  │
  ▼
Stage 2
  │
  ▼
Downsample
  │
  ▼
Stage 3
  │
  ▼
Downsample
  │
  ▼
Stage 4
```

Spatial resolution:

$$224
\rightarrow
56
\rightarrow
28
\rightarrow
14
\rightarrow
7$$

### Ý nghĩa

Thay đổi này làm ConvNeXt có cấu trúc gần với Swin:

```text
ResNet                  Swin / ConvNeXt
   │                          │
Stem                       Patch Embedding
   │                          │
Stage 1                    Stage 1
   ↓                          ↓
Stage 2                    Stage 2
   ↓                          ↓
Stage 3                    Stage 3
   ↓                          ↓
Stage 4                    Stage 4
```

**Kết luận:** cách tổ chức macro architecture hiện đại đã giúp CNN cải thiện đáng kể.

---

# 4.3. ResNeXt-ify

Tiếp theo tác giả hỏi:

> Có cần standard convolution không?

ResNeXt cho thấy việc tăng **cardinality** có thể giúp CNN hiệu quả hơn.

ConvNeXt đi tới extreme:

$$\boxed{\text{Depthwise Convolution}}$$

Thay vì:

$$Y_o = \sum_i W_{o,i} * X_i$$

depthwise convolution:

$$Y_i = W_i * X_i$$

Tức là mỗi channel có kernel riêng.

```text
Standard Conv

X1 ─┐
X2 ─┼──► Conv ──► Y1
X3 ─┘

X1 ─┐
X2 ─┼──► Conv ──► Y2
X3 ─┘
```

Trong depthwise:

```text
X1 ──► Conv1 ──► Y1
X2 ──► Conv2 ──► Y2
X3 ──► Conv3 ──► Y3
```

Sau đó:

```text
Depthwise Conv
      ↓
1×1 Conv
      ↓
Channel Mixing
```

### Insight

Depthwise convolution tách:

$$\text{Spatial Mixing}$$

khỏi:

$$\text{Channel Mixing}$$

Đây là một ý tưởng rất gần với cách Transformer phân tách **token mixing** và **channel mixing**.

---

# 4.4. Inverted Bottleneck

Bước tiếp theo là một thay đổi rất đáng chú ý.

ResNet:

$$C\rightarrow C/4\rightarrow C$$

ConvNeXt:

$$\boxed{C\rightarrow4C\rightarrow C}$$

Ví dụ:

```text
96
 ↓
384
 ↓
96
```

Đây chính là cấu trúc expansion–projection quen thuộc trong MLP của Transformer.

### Transformer

$$X
\rightarrow
Linear(C,4C)
\rightarrow
GELU
\rightarrow
Linear(4C,C)$$

### ConvNeXt

$$X
\rightarrow
DWConv
\rightarrow
Linear(C,4C)
\rightarrow
GELU
\rightarrow
Linear(4C,C)$$

Vì vậy ConvNeXt block bắt đầu có hình dạng:

```text
Spatial Mixing
      ↓
Channel Expansion
      ↓
Non-linearity
      ↓
Channel Projection
```

### Insight

Đây là lúc ConvNeXt bắt đầu **trông rất giống Transformer block**, nhưng spatial mixing vẫn được thực hiện bằng convolution.

---

# 4.5. Large Kernel Size

CNN truyền thống thường dựa vào:

$$3\times3$$

ConvNeXt thử:

$$5\times5,\quad7\times7,\quad9\times9$$

và nhận thấy **large kernel** có lợi.

Cuối cùng:

$$\boxed{7\times7\ Depthwise\ Conv}$$

được lựa chọn.

---

## Tại sao large kernel quan trọng?

Receptive field của convolution tăng theo kernel.

Ví dụ:

```text
3×3

[ . . . ]
[ . X . ]
[ . . . ]
```

Trong khi:

```text
7×7

[ . . . . . . . ]
[ . . . . . . . ]
[ . . . X . . . ]
[ . . . . . . . ]
[ . . . . . . . ]
[ . . . . . . . ]
[ . . . . . . . ]
```

Mỗi output có thể nhìn thấy phạm vi spatial lớn hơn.

Nhưng:

$$7\times7\ \text{Standard Conv}$$

rất đắt.

ConvNeXt giải quyết bằng:

$$7\times7\ \text{Depthwise Conv}$$

nên số tham số chỉ xấp xỉ:

$$7^2C=49C$$

thay vì:

$$7^2C^2=49C^2$$

của standard convolution.

Đây là lý do **large kernel + depthwise convolution** là một cặp thiết kế rất hợp lý.

---

# 4.6. Micro Design

Sau macro architecture, tác giả tiếp tục tối ưu **bên trong block**.

Các thay đổi quan trọng:

```text
BatchNorm
    ↓
LayerNorm

ReLU
    ↓
GELU
```

Và sử dụng:

```text
Layer Scale
    +
Stochastic Depth
```

Block trở thành:

```text
Input
 │
 ▼
7×7 DWConv
 │
 ▼
LayerNorm
 │
 ▼
1×1 Conv
 │
 ▼
4C
 │
 ▼
GELU
 │
 ▼
1×1 Conv
 │
 ▼
C
 │
 ▼
Layer Scale
 │
 ▼
DropPath
 │
 ▼
Residual Add
```

---

# 4.7. Vì sao LayerNorm?

BatchNorm phụ thuộc vào batch statistics.

LayerNorm thì chuẩn hóa theo feature dimension.

Với một vector feature:

$$x=(x_1,\ldots,x_C)$$

LayerNorm tính:

$$\mu=\frac{1}{C}\sum_{i=1}^{C}x_i$$

$$\sigma^2=
\frac{1}{C}
\sum_{i=1}^{C}(x_i-\mu)^2$$

Sau đó:

$$\hat{x}_i=
\frac{x_i-\mu}
{\sqrt{\sigma^2+\epsilon}}$$

và:

$$y_i=\gamma_i\hat{x}_i+\beta_i$$

Điều này làm ConvNeXt có normalization gần với Transformer hơn.

---

# 4.8. Vì sao GELU?

ReLU:

$$ReLU(x)=\max(0,x)$$

GELU:

$$GELU(x)=x\Phi(x)$$

GELU không cắt hoàn toàn các giá trị âm như ReLU mà tạo một activation mềm hơn.

Transformer sử dụng GELU rất phổ biến, nên ConvNeXt đưa nó vào để kiểm tra:

> Liệu activation hiện đại của Transformer có giúp CNN không?

Kết quả cho thấy các micro-design này giúp hoàn thiện ConvNeXt.

---

# 4.9. Layer Scale

Một thành phần nhỏ nhưng quan trọng.

Output của residual branch có thể được scale:

$$y=\gamma F(x)+x$$

với:

$$\gamma\in\mathbb{R}^{C}$$

và (\gamma) được học trong quá trình training.

Thay vì:

$$y=F(x)+x$$

ta có:

$$\boxed{y=\gamma\odot F(x)+x}$$

Điều này giúp kiểm soát magnitude của residual branch và hỗ trợ training mạng sâu.

---

# 4.10. DropPath / Stochastic Depth

ConvNeXt cũng sử dụng stochastic depth.

Ý tưởng:

```text
Training:

Input ────────────────┐
                      │
Input → Block → Drop ─┴─► Output
```

Một số residual branch được bỏ qua ngẫu nhiên trong training.

Về mặt kỳ vọng:

$$y=x+\text{DropPath}(F(x))$$

Điều này giúp regularization và giảm overfitting.

---

# 5. Kết quả của Ablation — phải đọc như thế nào?

Đừng chỉ nhìn:

```text
ConvNeXt = X%
```

Hãy đọc theo **incremental improvement**:

```text
Baseline
   │
   │ + Training
   ▼
Improved Baseline
   │
   │ + Macro Design
   ▼
Better CNN
   │
   │ + Depthwise Conv
   ▼
More Efficient CNN
   │
   │ + Inverted Bottleneck
   ▼
Transformer-like CNN
   │
   │ + Large Kernel
   ▼
Large-Receptive-Field CNN
   │
   │ + Micro Design
   ▼
ConvNeXt
```

Mỗi bước trả lời một câu hỏi nghiên cứu riêng.

---

# 6. Điều quan trọng nhất của Ablation

Có thể gom các thay đổi thành **3 tầng**:

### Tầng 1 — Macro

```text
Stem
Stage ratio
Downsampling
```

→ quyết định **hình dạng tổng thể của network**.

### Tầng 2 — Block

```text
Depthwise Conv
Inverted Bottleneck
Large Kernel
```

→ quyết định **cách feature được trộn**.

### Tầng 3 — Micro

```text
LayerNorm
GELU
Layer Scale
DropPath
```

→ quyết định **cách block được tối ưu và train**.

Do đó:

$$\boxed{
ConvNeXt=

Macro
+
Block
+
Micro
+
Modern\ Training
}$$

---

# 7. Từ Ablation → ConvNeXt hoàn chỉnh

Sau toàn bộ quá trình:

```text
                    ResNet
                       │
                       ▼
              Modern Training
                       │
                       ▼
                Macro Design
                       │
                       ▼
                 Depthwise Conv
                       │
                       ▼
             Inverted Bottleneck
                       │
                       ▼
                 7×7 Kernel
                       │
                       ▼
              LayerNorm + GELU
                       │
                       ▼
              Layer Scale + DropPath
                       │
                       ▼
                   ConvNeXt
```

Và block cuối:

```text
             ┌───────────────────────┐
             │                       │
             │      Residual         │
             │         │             │
Input ───────┼─────────┼─────────────┤
  │          │         │             │
  ▼          │         │             │
7×7 DWConv   │         │             │
  ↓          │         │             │
LayerNorm    │         │             │
  ↓          │         │             │
1×1 Conv     │         │             │
  ↓          │         │             │
4C           │         │             │
  ↓          │         │             │
GELU         │         │             │
  ↓          │         │             │
1×1 Conv     │         │             │
  ↓          │         │             │
C            │         │             │
  ↓          │         │             │
Layer Scale  │         │             │
  ↓          │         │             │
DropPath ────┘         │             │
             └──────► Add ◄──────────┘
                       │
                       ▼
                    Output
```
