# 1. Experiments

Sau khi tác giả đã xây dựng **ConvNeXt** và dùng Ablation Study để chứng minh từng thay đổi có tác dụng, Section 4 chuyển sang câu hỏi quan trọng hơn:

> **ConvNeXt có thực sự hoạt động tốt trên các bài toán Computer Vision khác nhau hay chỉ tốt trên ImageNet?**

Vì vậy, tác giả đánh giá ConvNeXt trên 3 nhóm task:

```text
                    ConvNeXt
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      ImageNet        COCO        ADE20K
          │            │            │
          ▼            ▼            ▼
   Classification   Detection   Segmentation
```

---

# 1.1. ImageNet Classification

## Mục tiêu

Đầu tiên, ConvNeXt được đánh giá trên **ImageNet-1K** cho bài toán image classification.

Input:

$$X\in\mathbb{R}^{224\times224\times3}$$

Output:

$$\hat{y}\in\mathbb{R}^{1000}$$

Flow:

```text
Image
  │
  ▼
ConvNeXt Stem
  │
  ▼
Stage 1
  │
  ▼
Stage 2
  │
  ▼
Stage 3
  │
  ▼
Stage 4
  │
  ▼
Global Average Pooling
  │
  ▼
Linear Classifier
  │
  ▼
1000 Classes
```

---

## Metric

Metric chính là **Top-1 Accuracy**:

$$Accuracy=
\frac{\text{Số dự đoán đúng}}
{\text{Tổng số mẫu}}$$

Ví dụ:

```text
1000 images
↓
850 dự đoán đúng
↓
Top-1 Accuracy = 85%
```

Ngoài accuracy, paper còn quan tâm đến:

* Parameters
* FLOPs
* Throughput

Bởi vì một model tốt không chỉ cần chính xác mà còn phải có hiệu quả tính toán hợp lý.

---

# 1.1.1. So sánh với các backbone khác

Paper không chỉ so ConvNeXt với ResNet.

Các nhóm được so sánh gồm:

```text
CNN
│
├── ResNet
├── ResNeXt
└── ConvNeXt

Transformer
│
├── ViT
└── Swin Transformer
```

Mục tiêu là xem:

$$\text{ConvNeXt}
\quad vs \quad
\text{Swin Transformer}$$

trong các mức model khác nhau.

---

# 1.1.2. Kết quả quan trọng

Kết quả nổi bật nhất:

$$\boxed{\text{ConvNeXt-L: 87.8\% Top1}}$$

trên ImageNet-1K.

Điều này đặc biệt đáng chú ý vì ConvNeXt:

* Không sử dụng self-attention.
* Không sử dụng Transformer block.
* Không sử dụng Q/K/V.
* Vẫn là một **pure ConvNet**.

Nói cách khác:

```text
Swin Transformer
       │
   Attention
       │
       ▼
High accuracy


ConvNeXt
       │
   Convolution
       │
       ▼
High accuracy
```

Do đó kết quả này hỗ trợ giả thuyết ban đầu của paper:

> **Một CNN được thiết kế và huấn luyện đúng cách vẫn có thể cạnh tranh với hierarchical Transformer.**

---

# 1.1.3. Scaling

Một điểm quan trọng khác là ConvNeXt không chỉ có một model.

Paper xây dựng nhiều kích thước:

```text
ConvNeXt-T
      ↓
ConvNeXt-S
      ↓
ConvNeXt-B
      ↓
ConvNeXt-L
      ↓
ConvNeXt-XL
```

Trong đó:

```text
T = Tiny
S = Small
B = Base
L = Large
XL = X-Large
```

Khi model lớn hơn:

$$Depth \uparrow$$

hoặc:

$$Width \uparrow$$

thì:

$$Parameters \uparrow$$

$$FLOPs \uparrow$$

và thường:

$$Accuracy \uparrow$$

Đây là **model scaling**.

---

# 1.1.4. Tại sao scaling quan trọng?

Nếu một architecture chỉ tốt ở model nhỏ thì khả năng ứng dụng sẽ hạn chế.

Paper muốn chứng minh:

$$\boxed{
ConvNeXt\ scales\ well
}$$

Tức là:

```text
Tiny
 │
 ├── Efficient
 │
 ▼
Base
 │
 ├── Strong
 │
 ▼
Large
 │
 └── Very high accuracy
```

Điều này khiến ConvNeXt trở thành một **family of backbones**, chứ không chỉ là một model đơn lẻ.

---

# 1.2. Object Detection

Sau ImageNet classification, tác giả kiểm tra ConvNeXt trên **COCO object detection**.

Đây là bước quan trọng vì classification chỉ yêu cầu:

$$Image\rightarrow Class$$

Trong khi detection cần:

$$Image
\rightarrow
{Bounding\ Boxes + Classes}$$

Ví dụ:

```text
Input Image
     │
     ▼
ConvNeXt Backbone
     │
     ▼
Multi-scale Features
     │
     ▼
Detection Head
     │
     ├── Bounding Box
     └── Class
```

---

# 1.2.1. ConvNeXt đóng vai trò gì?

Ở đây ConvNeXt không phải toàn bộ detector.

Nó đóng vai trò:

$$\boxed{Backbone}$$

Nhiệm vụ:

$$Image
\rightarrow
Feature\ Maps$$

Ví dụ:

```text
Image
 │
 ▼
ConvNeXt
 │
 ├── C1
 ├── C2
 ├── C3
 └── C4
      │
      ▼
Detection Head
```

Các feature map ở nhiều resolution giúp detector phát hiện:

* object lớn
* object vừa
* object nhỏ.

---

# 1.2.2. Metric: AP / mAP

Metric quan trọng của COCO là **Average Precision (AP)**.

Có thể hiểu đơn giản:

$$AP = \int_0^1 Precision(Recall),dRecall$$

COCO thường tổng hợp AP trên nhiều mức IoU.

Ví dụ:

$$AP_{50}$$

sử dụng:

$$IoU=0.5$$

Trong khi metric COCO chính:

$$AP$$

được tính trung bình trên nhiều ngưỡng IoU.

---

# 1.2.3. Kết quả có ý nghĩa gì?

Nếu ConvNeXt tốt trên ImageNet nhưng kém trên COCO, chúng ta chỉ có thể nói:

> ConvNeXt là classifier tốt.

Nhưng kết quả detection mạnh cho thấy:

$$\boxed{
ConvNeXt\ là\ backbone\ tổng\ quát
}$$

có thể cung cấp feature tốt cho detection.

Đây là một bước quan trọng để chứng minh ConvNeXt không chỉ là một ImageNet model.

---

# 1.3. Semantic Segmentation

Tiếp theo là **ADE20K semantic segmentation**.

Khác với classification:

```text
Image
 ↓
1 class
```

segmentation cần:

```text
Image
 ↓
Class của từng pixel
```

Toán học:

$$X\in\mathbb{R}^{H\times W\times3}$$

Output:

$$Y\in\mathbb{R}^{H\times W\times C}$$

Trong đó mỗi pixel có một probability distribution trên (C) classes.

---

# 1.3.1. Flow

```text
Input Image
      │
      ▼
ConvNeXt Backbone
      │
      ▼
Multi-scale Features
      │
      ▼
Segmentation Decoder
      │
      ▼
Pixel-wise Prediction
      │
      ▼
H × W × Classes
```

Ví dụ:

```text
       Input
         │
         ▼
 ┌─────────────────┐
 │    ConvNeXt     │
 └─────────────────┘
         │
    ┌────┼────┐
    ▼    ▼    ▼
   C1    C2   C3/C4
    │    │    │
    └────┼────┘
         ▼
      Decoder
         │
         ▼
   Pixel Classes
```

---

# 1.3.2. Metric: mIoU

Metric chính:

$$mIoU$$

IoU của một class:

$$IoU=
\frac{|Prediction\cap GroundTruth|}
{|Prediction\cup GroundTruth|}$$

Sau đó lấy trung bình trên tất cả classes:

$$mIoU=
\frac{1}{C}
\sum_{c=1}^{C}IoU_c$$

Ví dụ:

```text
Class       IoU
───────────────
Person      0.75
Car         0.82
Road        0.90
Building    0.78
```

thì:

$$mIoU=
\frac{0.75+0.82+0.90+0.78}{4}$$

---

# 1.3.3. Vì sao segmentation là bài test quan trọng?

Segmentation yêu cầu feature phải giữ được **spatial information**.

Classification:

```text
Cat
```

không cần biết chính xác pixel nào là mắt, tai, chân.

Nhưng segmentation cần:

```text
Pixel 1 → sky
Pixel 2 → building
Pixel 3 → road
Pixel 4 → person
...
```

Do đó nếu ConvNeXt vẫn đạt kết quả mạnh ở segmentation, nó cho thấy feature hierarchy của nó đủ tốt để phục vụ các task spatially dense.

---

# 2. Nhìn toàn bộ Section 4

Ta có:

```text
                    ConvNeXt
                       │
                       ▼
                General Backbone
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
      ImageNet        COCO        ADE20K
          │            │            │
          ▼            ▼            ▼
   Classification   Detection   Segmentation
          │            │            │
      Top-1 Acc        AP          mIoU
```

Đây chính là logic thực nghiệm của paper:

### Classification

Kiểm tra:

> ConvNeXt có học representation tốt không?

### Detection

Kiểm tra:

> Representation đó có hữu ích cho object localization không?

### Segmentation

Kiểm tra:

> Representation đó có giữ đủ spatial information không?

Nếu cả ba đều tốt:

$$\boxed{
ConvNeXt \approx General\ Purpose\ Vision\ Backbone
}$$

---

# 3. Điều paper thực sự chứng minh

Sau Section 3 và Section 4, lập luận của tác giả có thể viết thành chuỗi:

```text
ResNet
  │
  │ Modern training
  ▼
Strong ResNet baseline
  │
  │ Modernize architecture
  ▼
ConvNeXt
  │
  ├───────────────┐
  ▼               ▼
ImageNet       Downstream Tasks
  │               │
  ▼               ├── Detection
High Accuracy    └── Segmentation
  │
  ▼
Competitive with
Swin Transformer
```

Vì vậy, **đóng góp của paper không đơn giản là "ConvNeXt đạt accuracy cao"**.

Đóng góp lớn hơn là:

> **Bằng một chuỗi ablation có hệ thống, tác giả cho thấy nhiều design choice được xem là đặc trưng của Transformer có thể được chuyển hóa thành các thiết kế CNN tương ứng, và một pure ConvNet được hiện đại hóa như vậy có thể đạt hiệu năng cạnh tranh trên cả classification lẫn downstream vision tasks.**
