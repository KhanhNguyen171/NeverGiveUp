# Transfer Learning & Fine-Tuning

## Mục tiêu học tập

* **Phân biệt Feature Extraction và Fine-Tuning**

  * Chọn phương pháp dựa trên:

    * Kích thước dataset.
    * Khoảng cách giữa domain mới và domain pre-trained.
    * Ngân sách tính toán.

* **Feature Extraction**

  * Load **pretrained backbone**.
  * Thay **classifier head** bằng head phù hợp với task mới.
  * **Freeze backbone**, chỉ train classifier head.
  * Mục tiêu: tạo baseline nhanh với chi phí thấp.

* **Progressive Unfreezing**

  * Không mở toàn bộ backbone ngay.
  * Mở dần các layer từ cuối về đầu.
  * Dùng **discriminative learning rates**:

    * Layer đầu → learning rate nhỏ.
    * Layer cuối → learning rate lớn.
  * Vì feature ở đầu mạng thường mang tính **generic**, còn feature ở cuối mang tính **task-specific**.

### Ba lỗi quan trọng khi Fine-Tuning

1. **Feature Drift**

   * Learning rate quá lớn trên các block đã unfrozen.
   * Feature pretrained bị thay đổi quá mạnh → mất lợi ích của pretrained model.

2. **BN Statistics Collapse**

   * Dataset quá nhỏ → BatchNorm ước lượng mean/variance không ổn định.
   * Có thể làm training không ổn định hoặc giảm chất lượng model.

3. **Catastrophic Forgetting**

   * Fine-tuning quá mạnh khiến model quên các representation đã học từ pretraining.
   * Thường liên quan đến learning rate quá lớn hoặc mở quá nhiều layer.

> **Transfer Learning = tận dụng representation đã học.**
>
> **Feature Extraction = freeze backbone, chỉ học head.**
>
> **Fine-Tuning = mở một phần/toàn bộ backbone và cập nhật lại representation với learning rate phù hợp.**


## The Problem

Huấn luyện một **ResNet-50 trên ImageNet** tốn khoảng **2.000 GPU-giờ**, nên rất ít đội ngũ có đủ ngân sách để huấn luyện lại từ đầu cho từng bài toán. Thay vào đó, cách phổ biến là sử dụng **pretrained backbone** và thay bằng **head mới**, sau đó huấn luyện head trên vài trăm đến vài nghìn ảnh của task cụ thể. Đây không chỉ là một cách rút ngắn thời gian.

Trong CNN đã được huấn luyện trên ImageNet, các tầng học biểu diễn theo thứ bậc: **tầng đầu** học cạnh và các bộ lọc giống Gabor; **các tầng tiếp theo** học texture và motif đơn giản; **tầng giữa** học các bộ phận của vật thể; **tầng cuối** học các tổ hợp đặc trưng liên quan đến 1.000 lớp ImageNet. Phần lớn hierarchy đặc trưng ban đầu có thể được chuyển sang các domain như **medical imaging, industrial inspection, satellite data** mà gần như không cần thay đổi, vì các domain này vẫn dựa trên những đặc trưng cơ bản như cạnh và texture. Phần cuối của mạng mới là phần cần điều chỉnh cho task mới.

### Ba lỗi chính khi Transfer Learning

1. **Learning rate quá cao** → phá hỏng pretrained features.
2. **Freeze quá nhiều layer** → model thiếu khả năng học các đặc trưng cần thiết cho domain mới.
3. **BatchNorm statistics bị drift** → running statistics bị lệch theo dataset nhỏ, trong khi phần còn lại của network không được học từ dataset đó.

> Transfer Learning tận dụng phần lớn representation đã được học từ pretrained model; việc quan trọng là xác định **phần nào cần giữ nguyên, phần nào cần fine-tune và kiểm soát learning rate + BatchNorm** để không phá hỏng representation pretrained.


## The Concept

### 1. Feature Extraction vs Fine-Tuning

Có **2 chế độ Transfer Learning**, được lựa chọn dựa trên mức độ tin tưởng vào pretrained features và lượng dữ liệu có.


| Dataset    | Domain       | Cách làm                                                         |
| ---------- | ------------ | ---------------------------------------------------------------- |
| `< 1k` ảnh | Gần ImageNet | Freeze backbone, chỉ train head                                  |
| `1k–10k`   | Gần          | Freeze 2–3 stages đầu, fine-tune phần còn lại                    |
| `10k–100k` | Bất kỳ       | Fine-tune end-to-end với discriminative LR                       |
| `100k+`    | Bất kỳ       | Fine-tune toàn bộ; nếu domain đủ xa, cân nhắc train from scratch |

**Gần ImageNet** chủ yếu là ảnh RGB tự nhiên có nội dung dạng vật thể. **CT y tế, ảnh vệ tinh, microscopy** là các domain xa hơn → pretrained features vẫn hữu ích nhưng cần cho phép nhiều layer thích nghi hơn.

### 2. Vì sao Freezing hoạt động?

Feature mà CNN học từ ImageNet **không chỉ phục vụ 1.000 class**. Chúng chủ yếu biểu diễn các đặc trưng của ảnh tự nhiên:

* **Early layers:** edges, orientation.
* **Middle layers:** textures, contrast patterns, shape primitives.
* **Late layers:** cấu trúc đặc trưng cho task.

Các đặc trưng cơ bản này có tính ổn định trên nhiều domain, nên có thể **freeze backbone** và chỉ train classifier head. Head chỉ học cách kết hợp các feature đã có cho task mới.

### 3. Discriminative Learning Rates

Khi unfreeze, **layer càng sớm → learning rate càng nhỏ**, layer càng muộn → learning rate càng lớn.

$$lr_{stage0}=\frac{base_{lr}}{100}$$

$$lr_{stage1}=\frac{base_{lr}}{10}$$

$$lr_{stage2}=\frac{base_{lr}}{3}$$

$$lr_{stage3}=base_{lr}$$

$$lr_{head}\approx base_{lr}$$

Lý do: **early layers chứa generic features cần được bảo toàn**, còn **late layers chứa task-specific features cần thích nghi mạnh hơn**.

Trong PyTorch, thực hiện bằng **parameter groups** khi truyền parameters vào optimizer.

### 4. Vấn đề BatchNorm

BatchNorm có `running_mean` và `running_var` được tính từ ImageNet. Nếu domain mới có phân phối pixel khác, các statistics này có thể không còn phù hợp.

Ba lựa chọn:

1. **Fine-tune với BN ở train mode:** cho phép cập nhật statistics → phù hợp dataset trung bình, khoảng `>= 5k` examples.
2. **Freeze BN ở eval mode:** giữ ImageNet statistics → phù hợp dataset nhỏ, tránh statistics bị nhiễu.
3. **Thay BN bằng GroupNorm:** loại bỏ vấn đề running statistics → hữu ích khi batch size rất nhỏ.

### 5. Classifier Head

Head thường chỉ gồm **1–3 Linear layers**, có thể thêm Dropout.

Với dataset nhỏ, **một Linear layer thường đủ**. Nếu domain mới xa pretrained domain hơn, có thể dùng:

`Linear → ReLU → Dropout → Linear`

### 6. Layer-wise LR Decay

Đây là phiên bản mượt hơn của discriminative LR, thường dùng trong fine-tuning Transformer.

$$lr_k=base_{lr}\times decay^{(L-k)}$$

Ví dụ `decay = 0.75`, `L = 12`: block đầu tiên chỉ nhận khoảng `0.75^11 ≈ 0.04×` learning rate của head.

### 7. Đánh giá Transfer Learning

Luôn theo dõi **2 accuracy**:

* **Pretrained-only accuracy:** backbone frozen + train head → **mức sàn**.
* **Fine-tuned accuracy:** sau khi fine-tune → **mức trần**.

Nếu:

$$Accuracy_{fine-tuned}<Accuracy_{pretrained-only}$$

→ cần kiểm tra trước tiên **learning rate hoặc BatchNorm**, vì fine-tuning đang làm model tệ hơn baseline pretrained.

## Build It

### Step 1: Load a pretrained backbone and inspect it

```python
import torch
import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights

backbone = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)

print(backbone)
print()
print("classifier head:", backbone.fc)
print("feature dim:", backbone.fc.in_features)
```

> Load ResNet-18 đã pretrained trên ImageNet. `backbone.fc` là classifier head và `in_features` cho biết số chiều feature mà backbone tạo ra. ResNet-18 gồm **stem → layer1 → layer2 → layer3 → layer4 → fc**.

---

### Step 2: Feature Extraction — freeze backbone, thay head

```python
def make_feature_extractor(num_classes=10):
    model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)

    for p in model.parameters():
        p.requires_grad = False

    model.fc = nn.Linear(model.fc.in_features, num_classes)

    return model


model = make_feature_extractor(num_classes=10)

trainable = sum(
    p.numel() for p in model.parameters()
    if p.requires_grad
)

frozen = sum(
    p.numel() for p in model.parameters()
    if not p.requires_grad
)

print(f"trainable: {trainable:>10,}")
print(f"frozen: {frozen:>10,}")
```

> Toàn bộ pretrained backbone được **freeze** bằng `requires_grad=False`. Chỉ `model.fc` được thay mới và train. Vì vậy backbone hoạt động như một **frozen feature extractor**, còn classifier head học cách ánh xạ feature sang `num_classes`.

### Step 3: Discriminative Fine-Tuning

```python
def discriminative_param_groups(model, base_lr=1e-3, decay=0.3):
    stages = [
        ["conv1", "bn1"],
        ["layer1"],
        ["layer2"],
        ["layer3"],
        ["layer4"],
        ["fc"],
    ]

    groups = []

    for i, names in enumerate(stages):
        lr = base_lr * (decay ** (len(stages) - 1 - i))

        params = [
            p for n, p in model.named_parameters()
            if any(n.startswith(k) for k in names)
        ]

        if params:
            groups.append({
                "params": params,
                "lr": lr,
                "name": "_".join(names)
            })

    return groups


model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
model.fc = nn.Linear(model.fc.in_features, 10)

for p in model.parameters():
    p.requires_grad = True

groups = discriminative_param_groups(model)

for g in groups:
    print(
        f"{g['name']:>10s} "
        f"lr={g['lr']:.2e} "
        f"params={sum(p.numel() for p in g['params']):>8,}"
    )
```

> Chia model thành các stage và gán **learning rate khác nhau**. Stage càng gần input → LR càng nhỏ; stage càng gần output → LR càng lớn. Với `decay=0.3`, mỗi stage chỉ train ở **30% LR của stage kế tiếp**. `fc` dùng `base_lr`, `layer4 = 0.3 × base_lr`, còn `conv1` = `0.3^5 × base_lr ≈ 0.00243 × base_lr`.

---

### Step 4: BatchNorm Handling

```python
def freeze_bn_stats(model):
    for m in model.modules():
        if isinstance(
            m,
            (nn.BatchNorm1d, nn.BatchNorm2d, nn.BatchNorm3d)
        ):
            m.eval()

            for p in m.parameters():
                p.requires_grad = False

    return model
```

Gọi sau `model.train()` ở đầu mỗi epoch:

```python
model.train()
freeze_bn_stats(model)
```

> `model.train()` đưa toàn bộ model về training mode, nhưng `freeze_bn_stats()` chuyển riêng các **BatchNorm layers** về `eval()` để giữ nguyên running statistics. Đồng thời freeze cả BN weights, tránh statistics bị thay đổi theo dataset nhỏ.

### Step 5: Minimal End-to-End Fine-Tuning Loop

```python
from torch.optim import SGD
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import CosineAnnealingLR
import torch.nn.functional as F


def fine_tune(model, train_loader, val_loader, device, epochs=5, base_lr=1e-3, freeze_bn=False):
    model = model.to(device)

    groups = discriminative_param_groups(model, base_lr=base_lr)

    optimizer = SGD(
        groups,
        momentum=0.9,
        weight_decay=1e-4,
        nesterov=True,
    )

    scheduler = CosineAnnealingLR(optimizer, T_max=epochs)

    for epoch in range(epochs):
        model.train()

        if freeze_bn:
            freeze_bn_stats(model)

        tr_loss, tr_correct, tr_total = 0.0, 0, 0

        for x, y in train_loader:
            x, y = x.to(device), y.to(device)

            logits = model(x)
            loss = F.cross_entropy(
                logits,
                y,
                label_smoothing=0.1,
            )

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            tr_loss += loss.item() * x.size(0)
            tr_total += x.size(0)
            tr_correct += (
                (logits.argmax(-1) == y).sum().item()
            )

        scheduler.step()
        model.eval()
        va_total, va_correct = 0, 0

        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)

                pred = model(x).argmax(-1)

                va_total += x.size(0)
                va_correct += (pred == y).sum().item()

        print(
            f"epoch {epoch} "
            f"train {tr_loss/tr_total:.3f}/{tr_correct/tr_total:.3f} "
            f"val {va_correct/va_total:.3f}"
        )
    return model
```

> Đây là training loop hoàn chỉnh cho fine-tuning: **forward → loss → backward → optimizer → scheduler → validation**. Optimizer sử dụng discriminative learning rates, SGD với momentum/Nesterov, và `CosineAnnealingLR`. Nếu `freeze_bn=True`, BatchNorm statistics được giữ cố định.

---

### Step 6: Progressive Unfreezing

```python
def progressive_unfreeze_schedule(model):
    stages = ["layer4", "layer3", "layer2", "layer1"]
    yielded = set()

    def start():
        for p in model.parameters():
            p.requires_grad = False
        for p in model.fc.parameters():
            p.requires_grad = True

    def unfreeze(epoch):
        if epoch < len(stages):
            name = stages[epoch]
            yielded.add(name)
            for n, p in model.named_parameters():
                if n.startswith(name):
                    p.requires_grad = True

            return name
        return None
    return start, unfreeze
```

Cách sử dụng:

```python
start, unfreeze = progressive_unfreeze_schedule(model)

start()

for epoch in range(epochs):
    stage = unfreeze(epoch)
```

> Ban đầu chỉ train `fc`, sau đó mỗi epoch mở thêm một stage theo thứ tự **`layer4 → layer3 → layer2 → layer1`**. Cách này giảm **feature drift** vì các layer generic ở đầu mạng chưa bị cập nhật quá sớm.

**Lưu ý quan trọng:** Mỗi khi số lượng parameter trainable thay đổi, cần **rebuild optimizer**; nếu không, các parameter từng bị freeze có thể vẫn giữ optimizer state/moments cũ.

## Key Terms

| Term                        | What people say                 | What it actually means                                                                                        |
| --------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Feature extraction**      | “Freeze and train head”         | Backbone parameters are frozen; only the new classifier head receives gradient.                               |
| **Fine-tuning**             | “Retrain end-to-end”            | All parameters are trainable, usually with a much smaller LR than training from scratch.                      |
| **Discriminative LR**       | “Smaller LR for early layers”   | Optimizer parameter groups where early-stage LR is a fraction of late-stage LR.                               |
| **Layer-wise LR decay**     | “Smooth LR gradient”            | Per-layer LR follows $$lr_k = base_lr \times decay^{(L-k)}$$; common in Transformer fine-tuning.              |
| **Catastrophic forgetting** | “The model lost ImageNet”       | LR quá cao ghi đè pretrained features trước khi task mới được học ổn định.                                    |
| **BN statistics drift**     | “Running mean is wrong”         | `running_mean/var` của BatchNorm được tính trên phân phối khác với task hiện tại, làm giảm accuracy.          |
| **Linear probe**            | “Frozen backbone + linear head” | Đánh giá pretrained representation bằng classifier tuyến tính tốt nhất trên backbone frozen.                  |
| **Catastrophic collapse**   | “Everything predicts one class” | Xảy ra khi fine-tuning với LR đủ cao để phá hỏng features trước khi gradient từ head có thể ổn định việc học. |
