# ConvNext

A ConvNet for the 2020s — Zhuang Liu, Hanzi Mao, Chao-Yuan Wu, Christoph Feichtenhofer, Trevor Darrell, Saining Xie, CVPR 2022.

- arXiv: [A ConvNet for the 2020s – arXiv](https://arxiv.org/abs/2201.03545?utm_source=chatgpt.com)
- PDF chính thức CVPR: [CVPR OpenAccess PDF](https://openaccess.thecvf.com/content/CVPR2022/html/Liu_A_ConvNet_for_the_2020s_CVPR_2022_paper.html?utm_source=chatgpt.com)
- IEEE: [IEEE Xplore – A ConvNet for the 2020s](https://doi.org/10.1109/CVPR52688.2022.01167?utm_source=chatgpt.com)
- Official GitHub: [facebookresearch/ConvNeXt](https://github.com/facebookresearch/ConvNeXt?utm_source=chatgpt.com)

![](img/convnext.drawio.png)

---

# 1. Bức tranh toàn bộ paper

Trước khi đi từng section, cần nắm flow nghiên cứu:

```text
                    VẤN ĐỀ
                       │
                       ▼
        Vision Transformer vượt CNN
                       │
                       ▼
       "Transformer thật sự tốt hơn CNN?"
                       │
                       ▼
             Chọn ResNet làm baseline
                       │
                       ▼
        ┌──────────────────────────────┐
        │      MODERNIZE RESNET        │
        └──────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
     Training       Macro         Micro
     Techniques     Design        Design
          │            │            │
          └────────────┼────────────┘
                       ▼
                  ConvNeXt
                       │
          ┌────────────┼─────────────┐
          ▼            ▼             ▼
       ImageNet       COCO        ADE20K
          │            │             │
          └────────────┼─────────────┘
                       ▼
                  CONCLUSION
```

Điểm quan trọng: **paper không chỉ đề xuất model**.

Nó là một **quá trình nghiên cứu ablation có hệ thống** để trả lời:

> Những yếu tố nào thực sự tạo nên khoảng cách giữa CNN hiện đại và Vision Transformer?

---

# 2. Section 1 — Introduction

## Dịch ý chính

Đầu những năm 2020, Vision Transformer (ViT) nhanh chóng vượt qua ConvNet trong image classification. Tuy nhiên, vanilla ViT gặp khó khăn khi áp dụng vào các bài toán vision tổng quát như object detection và semantic segmentation.

Hierarchical Transformer, tiêu biểu là Swin Transformer, giải quyết vấn đề này bằng cách đưa trở lại một số **inductive bias của CNN**.

Từ đó tác giả đặt câu hỏi:

> Nếu chính Transformer phải sử dụng những ưu điểm vốn có của CNN, vậy liệu sự vượt trội của Transformer có thực sự đến từ Transformer hay không?

Paper quyết định kiểm tra bằng cách:

```text
ResNet
   ↓
từng bước hiện đại hóa
   ↓
ConvNeXt
```

Tác giả nhấn mạnh rằng ConvNeXt được xây dựng **hoàn toàn từ các module CNN tiêu chuẩn**, không sử dụng self-attention. ([arXiv][1])

### Ý tưởng nghiên cứu

```text
Không hỏi:

"Transformer có tốt hơn CNN không?"

Mà hỏi:

"Modern CNN có thể tốt đến đâu?"
```

Đây là câu hỏi nghiên cứu thực sự của paper.

---

# 3. Section 2 — Related Work

Phần này đặt ConvNeXt vào lịch sử phát triển của vision backbone.

Có thể chia thành:

```text
CNN
│
├── AlexNet
├── VGG
├── Inception
├── ResNet
├── ResNeXt
│
└──────────────┐
               │
               ▼
        Vision Transformer
               │
               ├── ViT
               └── Swin Transformer
```

Paper đặc biệt quan tâm tới **Swin Transformer** vì Swin có kiến trúc hierarchical và có thể hoạt động như một backbone tổng quát cho detection/segmentation.

Do đó:

```text
ResNet  ←────────────→  Swin Transformer
             ↑
        ConvNeXt nằm ở đây
```

ConvNeXt cố gắng lấy những design principle tốt của Transformer nhưng vẫn giữ **pure convolution**.

---

# 4. Section 3 — ConvNeXt

Đây là **phần quan trọng nhất của paper**.

Cấu trúc:

```text
3. ConvNeXt
│
├── 3.1 Training Techniques
├── 3.2 Macro Design
├── 3.3 ResNeXt-ify
├── 3.4 Inverted Bottleneck
├── 3.5 Large Kernel Sizes
└── 3.6 Micro Design
```

---

# 5. 3.1 — Training Techniques

Đầu tiên tác giả **không thay architecture**.

Họ lấy ResNet và áp dụng training recipe hiện đại.

Mục đích:

```text
ResNet cũ
   ↓
Modern training recipe
   ↓
Modern ResNet baseline
```

Điều này cực kỳ quan trọng.

Nếu làm:

```text
Old ResNet + old training
          vs
Swin + modern training
```

thì comparison không công bằng.

Do đó tác giả trước tiên phải hỏi:

> Khi ResNet được train bằng recipe hiện đại, nó còn kém bao nhiêu?

---

# 6. 3.2 — Macro Design

Sau khi có baseline tốt hơn, tác giả thay đổi **cấu trúc cấp cao**.

## ResNet

Kiểu truyền thống:

```text
Input
  ↓
Stem
  ↓
Stage 1
  ↓
Stage 2
  ↓
Stage 3
  ↓
Stage 4
  ↓
Classifier
```

ConvNeXt tiến gần cách tổ chức của hierarchical Transformer.

### Stem

Thay:

```text
7×7 Conv, stride 2
        ↓
Max Pool
```

bằng:

```text
4×4 Conv, stride 4
```

Do đó:

```text
224×224
   ↓
56×56
```

Tức là giảm spatial resolution **4 lần ngay từ đầu**.

---

# 7. 3.3 — ResNeXt-ify

Đây là bước rất quan trọng.

ResNeXt đưa ra ý tưởng:

> Tách convolution thành nhiều nhóm để tăng cardinality và hiệu quả biểu diễn.

ConvNeXt tiếp tục ý tưởng này tới mức:

```text
Depthwise Conv
```

Với standard convolution:

$$Y_{o} = \sum_{i} W_{o,i} * X_i$$

Một output channel kết hợp **tất cả input channels**.

Trong depthwise convolution:

$$Y_i = W_i * X_i$$

Mỗi channel được xử lý độc lập.

Sau đó dùng `1×1 Conv` để trộn thông tin giữa các channels.

Do đó:

```text
Depthwise Conv
       ↓
Spatial Mixing
       ↓
1×1 Conv
       ↓
Channel Mixing
```

Đây là một insight rất lớn của ConvNeXt.

---

# 8. 3.4 — Inverted Bottleneck

ResNet bottleneck:

```text
C
 ↓
C/4
 ↓
C
```

ConvNeXt:

```text
C
 ↓
4C
 ↓
C
```

Ví dụ:

```text
96
 ↓
384
 ↓
96
```

Về mặt ý tưởng:

$$X \in \mathbb{R}^{C}$$

được mở rộng:

$$X' \in \mathbb{R}^{4C}$$

sau đó projection:

$$X'' \in \mathbb{R}^{C}$$

Tại sao?

Bởi vì Transformer cũng thường sử dụng:

$$C \rightarrow 4C \rightarrow C$$

trong MLP.

Do đó ConvNeXt block bắt đầu có hình dạng rất giống Transformer:

```text
Transformer:

Token
 ↓
MLP expansion
C → 4C
 ↓
Activation
 ↓
Projection
4C → C
```

ConvNeXt:

```text
Feature Map
 ↓
Depthwise Conv
 ↓
1×1 Conv
C → 4C
 ↓
GELU
 ↓
1×1 Conv
4C → C
```

---

# 9. 3.5 — Large Kernel Sizes

CNN truyền thống:

$$3\times3$$

ConvNeXt:

$$7\times7$$

Tác dụng chính:

$$\text{larger kernel}
\Rightarrow
\text{larger receptive field}$$

Ví dụ:

```text
3×3

□ □ □
□ X □
□ □ □
```

so với:

```text
7×7

□ □ □ □ □ □ □
□ □ □ □ □ □ □
□ □ X □ □ □ □
□ □ □ □ □ □ □
□ □ □ □ □ □ □
□ □ □ □ □ □ □
□ □ □ □ □ □ □
```

Nhưng dùng `7×7 standard convolution` sẽ tốn kém.

Vì vậy ConvNeXt kết hợp:

$$7\times7 + Depthwise\ Conv$$

để giữ chi phí hợp lý.

---

# 10. 3.6 — Micro Design

Đây là bước cuối cùng.

ConvNeXt thay đổi các thành phần nhỏ bên trong block.

### ReLU → GELU

ReLU:

$$f(x)=\max(0,x)$$

GELU:

$$\operatorname{GELU}(x)=x\Phi(x)$$

GELU được sử dụng phổ biến trong Transformer.

---

### BatchNorm → LayerNorm

CNN truyền thống:

```text
Conv
 ↓
BatchNorm
 ↓
ReLU
```

ConvNeXt:

```text
Depthwise Conv
 ↓
LayerNorm
 ↓
Linear
 ↓
GELU
 ↓
Linear
```

LayerNorm hoạt động trên feature dimension của từng sample thay vì phụ thuộc trực tiếp vào batch statistics như BatchNorm.

---

# 11. ConvNeXt Block hoàn chỉnh

Sau tất cả các bước trên, block cuối cùng có thể hiểu như:

```text
                         ┌──────────────────────┐
                         │                      │
Input ───────────────────┼──────────────────┐   │
                         │                  │   │
                         ▼                  │   │
                  7×7 Depthwise Conv        │   │
                         │                  │   │
                         ▼                  │   │
                     LayerNorm              │   │
                         │                  │   │
                         ▼                  │   │
                  1×1 Conv / Linear         │   │
                         │                  │   │
                         ▼                  │   │
                       4×C                  │   │
                         │                  │   │
                         ▼                  │   │
                        GELU                │   │
                         │                  │   │
                         ▼                  │   │
                     1×1 Conv               │   │
                         │                  │   │
                         ▼                  │   │
                       C                    │   │
                         │                  │   │
                    Layer Scale             │   │
                         │                  │   │
                      DropPath              │   │
                         │                  │   │
                         └──────► Add ◄─────┘   │
                                │               │
                                ▼               │
                              Output            │
```

Có thể viết ngắn gọn:

$$X
\rightarrow
DWConv_{7\times7}
\rightarrow
LN
\rightarrow
PWConv
\rightarrow
GELU
\rightarrow
PWConv
\rightarrow
LS
\rightarrow
DropPath
\rightarrow
+X$$

Đây chính là kiến trúc bạn nên nhớ.

---

# 12. Tại sao ConvNeXt nhìn giống Transformer?

So sánh trực tiếp:

| Transformer      | ConvNeXt         |
| ---------------- | ---------------- |
| Token mixing     | Depthwise Conv   |
| Channel mixing   | Pointwise Conv   |
| MLP              | 1×1 → GELU → 1×1 |
| LayerNorm        | LayerNorm        |
| Residual         | Residual         |
| Stochastic Depth | DropPath         |

Vì vậy có thể hiểu:

```text
             Transformer
                  │
       ┌──────────┴──────────┐
       │                     │
 Spatial/Token mixing    Channel mixing
       │                     │
       ▼                     ▼
  Self-Attention            MLP


             ConvNeXt
                  │
       ┌──────────┴──────────┐
       │                     │
    Spatial mixing       Channel mixing
       │                     │
       ▼                     ▼
 Depthwise Conv              1×1 Conv
```

**Nhưng ConvNeXt vẫn hoàn toàn là CNN.**

Đây chính là đóng góp về mặt thiết kế của paper. ([arXiv][1])

---

# 13. Ablation Study — phần quan trọng nhất để học

Đây là phần bạn **không nên chỉ đọc kết quả cuối cùng**.

Tác giả không nói:

> "Chúng tôi thử ConvNeXt và nó tốt."

Mà hỏi:

> **Từng thay đổi đóng góp bao nhiêu?**

Flow:

```text
ResNet-50
   │
   ├── + Training Techniques
   │
   ▼
ResNet-50*
   │
   ├── + Macro Design
   │
   ▼
Modern ConvNet
   │
   ├── + ResNeXt-ify
   │
   ▼
Depthwise ConvNet
   │
   ├── + Inverted Bottleneck
   │
   ▼
Transformer-like block
   │
   ├── + Large Kernel
   │
   ▼
Large-kernel ConvNet
   │
   ├── + Micro Design
   │
   ▼
ConvNeXt
```

Điều này cho phép tác giả **tách riêng contribution của từng design choice**.

---

# 14. Ablation không chỉ hỏi "accuracy bao nhiêu?"

Cần đọc Ablation theo ba câu hỏi:

### Câu hỏi 1

**Thay đổi nào giúp accuracy tăng?**

Ví dụ:

```text
Baseline
   ↓
+ Large Kernel
   ↓
Accuracy ↑
```

=> large kernel có contribution tích cực.

### Câu hỏi 2

**Thay đổi nào giúp efficiency?**

Một kiến trúc có thể:

$$Accuracy \uparrow$$

nhưng:

$$FLOPs \uparrow\uparrow$$

thì chưa chắc tốt.

Do đó cần nhìn:

* Accuracy
* FLOPs
* Parameters
* Throughput

### Câu hỏi 3

**Có phải tất cả thay đổi đều cần thiết không?**

Không nhất thiết.

Một số thay đổi có contribution nhỏ khi đứng riêng nhưng trở nên hữu ích khi kết hợp với các thay đổi khác.

Đây là lý do phải đọc **ablation theo chuỗi**, không đọc từng dòng độc lập.

---

# 15. Section 4 — Experiments

Sau khi ConvNeXt được xây dựng, paper kiểm tra nó trên nhiều task.

```text
ConvNeXt
   │
   ├── ImageNet
   │      └── Classification
   │
   ├── COCO
   │      └── Object Detection
   │
   └── ADE20K
          └── Semantic Segmentation
```

Điều này rất quan trọng.

Nếu ConvNeXt chỉ tốt trên ImageNet thì chưa đủ để chứng minh nó là **general-purpose visual backbone**.

Paper kiểm tra cả:

$$Classification$$

$$Detection$$

$$Segmentation$$

và báo cáo ConvNeXt cạnh tranh mạnh với các Transformer backbone. ([arXiv][1])

---

# 16. ImageNet — Classification

Task:

$$Image \rightarrow Class$$

Ví dụ:

```text
224×224×3
     ↓
ConvNeXt
     ↓
Global Average Pooling
     ↓
Linear
     ↓
1000 classes
```

Metric chính:

$$Top\text{-}1\ Accuracy$$

Kết quả nổi bật nhất của paper là ConvNeXt-L đạt **87.8% Top-1 accuracy trên ImageNet**. ([arXiv][1])

Điều này cho thấy pure ConvNet có thể đạt performance rất cao mà không cần self-attention.

---

# 17. COCO — Object Detection

Ở detection, ConvNeXt không hoạt động như một classifier độc lập.

Nó đóng vai trò:

```text
Input Image
     ↓
ConvNeXt Backbone
     ↓
Multi-scale Features
     ↓
Detection Head
     ↓
Bounding Boxes + Classes
```

Mục tiêu:

$$Image
\rightarrow
{(bbox_i,class_i)}_{i=1}^{N}$$

Điểm quan trọng:

> ConvNeXt có thể trở thành **backbone tổng quát**, chứ không chỉ là ImageNet classifier.

Paper báo cáo ConvNeXt vượt Swin Transformer ở các thiết lập detection được đánh giá. ([arXiv][1])

---

# 18. ADE20K — Semantic Segmentation

Segmentation yêu cầu dự đoán class cho **từng pixel**:

$$X \rightarrow Y$$

với:

$$Y \in \mathbb{R}^{H\times W}$$

Flow:

```text
Image
 ↓
ConvNeXt Backbone
 ↓
Feature Pyramid
 ↓
Segmentation Head
 ↓
Pixel-wise prediction
```

Điều này tiếp tục kiểm tra khả năng giữ thông tin spatial của ConvNeXt.

---

# 19. Scaling — tại sao ConvNeXt có nhiều phiên bản?

Paper không chỉ tạo một model.

Nó tạo một family:

```text
ConvNeXt-T
ConvNeXt-S
ConvNeXt-B
ConvNeXt-L
ConvNeXt-XL
```

Ý tưởng:

$$Model\ Capacity \uparrow
\Rightarrow
Performance \uparrow$$

nhưng đồng thời:

$$Parameters \uparrow$$

$$FLOPs \uparrow$$

Do đó cần kiểm tra **scalability**.

Đây cũng là một trong những điểm paper muốn chứng minh: ConvNet hiện đại không chỉ hiệu quả ở model nhỏ mà còn scale tốt lên model lớn. ([arXiv][1])

---

# 20. Toàn bộ logic của paper

Nếu phải ghi lại paper vào một trang note, tôi sẽ giữ đúng flow này:

```text
                    A ConvNet for the 2020s
                              │
                              ▼
                    Problem: ViT > CNN?
                              │
                              ▼
                         ResNet Baseline
                              │
                              ▼
                   3.1 Training Techniques
                              │
                              ▼
                      3.2 Macro Design
                              │
                              ▼
                     3.3 ResNeXt-ify
                              │
                              ▼
                  3.4 Inverted Bottleneck
                              │
                              ▼
                   3.5 Large Kernel Size
                              │
                              ▼
                       3.6 Micro Design
                              │
                              ▼
                          ConvNeXt
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
           ImageNet          COCO           ADE20K
         Classification     Detection      Segmentation
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                         Conclusion
```

---

# 21. Điều thực sự cần học từ ConvNeXt

Đừng học ConvNeXt theo kiểu:

> "`ConvNeXt` = 7×7 Conv + LayerNorm + GELU."

Như vậy mới chỉ học thuộc architecture.

Điều paper thực sự muốn truyền đạt là:

### ① CNN không nhất thiết đã lỗi thời

Khoảng cách giữa CNN và Transformer **không đơn giản là do self-attention**.

### ② Training recipe rất quan trọng

Phải có baseline công bằng trước khi kết luận architecture nào tốt hơn.

### ③ Spatial mixing và channel mixing có thể tách biệt

```text
Depthwise Conv → spatial
1×1 Conv       → channel
```

### ④ CNN có thể áp dụng các design principle của Transformer

```text
LayerNorm
GELU
Inverted Bottleneck
Large receptive field
Stochastic Depth
```

mà vẫn giữ convolution.

### ⑤ Ablation mới là phần chứng minh

Paper không chỉ đưa ra một architecture tốt; tác giả **từng bước chứng minh tại sao architecture đó tốt**.

Đó là điểm rất đáng học nếu bạn đang học cách **đọc một paper Deep Learning theo hướng nghiên cứu**.

[1]: https://arxiv.org/abs/2201.03545 "[2201.03545] A ConvNet for the 2020s"
