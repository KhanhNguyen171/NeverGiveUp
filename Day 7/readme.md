# Object Detection — YOLO from Scratch

> Detection is classification plus regression, run at every position in a feature map, then cleaned up with non-maximum suppression.

## Mục tiêu học tập (Learning Objectives)

- Giải thích cơ chế Grid Cell và Anchor Box giúp YOLO biến bài toán phát hiện đối tượng (Object Detection) thành bài toán Dense Prediction, đồng thời mô tả ý nghĩa của từng giá trị trong output tensor.

- Tính toán Intersection over Union (IoU) giữa các bounding box và tự cài đặt thuật toán Non-Maximum Suppression (NMS) từ đầu.
- Xây dựng một YOLO Detection Head tối giản trên một backbone đã được huấn luyện trước (pretrained backbone), bao gồm:
    - Classification Loss
    - Objectness Loss
    - Bounding Box Regression Loss

- Đọc và phân tích các chỉ số đánh giá Object Detection như:
    - Precision@0.5
    - Recall
    - mAP@0.5
    - mAP@0.5:0.95
    - từ đó xác định nên điều chỉnh (tuning) thành phần nào của mô hình tiếp theo.

## Bài toán Object Detection

Trong Computer Vision, Image Classification và Object Detection là hai bài toán hoàn toàn khác nhau.

- Image Classification chỉ trả lời câu hỏi: 
    - "Trong ảnh có đối tượng gì?" => Image -> Dog

- Object Detection phải trả lời đồng thời bốn câu hỏi:
    - Có bao nhiêu đối tượng?
    - Đó là đối tượng gì?
    - Đối tượng nằm ở vị trí nào?
    - Mức độ tin cậy của dự đoán là bao nhiêu? 

        - Dog: Bounding Box = (112,40,280,210) 
        - Cat: Bounding Box = (400,180,560,310)

Thay vì chỉ xuất ra một nhãn (label) cho toàn bộ ảnh, mô hình phải dự đoán một số lượng biến đổi (variable number) các bounding box cùng với nhãn tương ứng của từng đối tượng.

### Trade-off của Bài toán Detection

Object Detection là một trong những bài toán phức tạp nhất của Computer Vision vì mô hình phải học nhiều nhiệm vụ cùng lúc.

Một detector cần đồng thời giải quyết bốn bài toán:
- __Regression__: Dự đoán chính xác vị trí của bounding box. Bounding box càng khớp với vật thể thì IoU càng cao.
    - __(x_center, y_center, width, height)__

- __Classification__: Sau khi xác định được vị trí, mô hình phải phân loại đúng đối tượng.

- __Objectness__: Không phải mọi vùng trong ảnh đều chứa vật thể.
    - Giá trị này gọi là Objectness Score.

- __Duplicate Removal__: Một đối tượng thường được nhiều bounding box dự đoán cùng lúc.
    - Nếu giữ lại tất cả các box, kết quả sẽ xuất hiện nhiều dự đoán trùng lặp cho cùng một vật thể.
    - Do đó cần áp dụng Non-Maximum Suppression (NMS) để chỉ giữ lại bounding box tốt nhất.

Nếu một trong các thành phần trên hoạt động không tốt, hệ thống sẽ gặp các vấn đề như:
- Bỏ sót đối tượng (Miss Detection)
- Phát hiện đối tượng không tồn tại (False Positive)
- Dự đoán sai lớp (Wrong Classification)
- Một vật thể bị dự đoán thành nhiều bounding box khác nhau (Duplicate Detection)

## YOLO (You Only Look Once)

YOLO (You Only Look Once) do Joseph Redmon và cộng sự giới thiệu năm 2016.

Ý tưởng cốt lõi của YOLO là:

> Thực hiện toàn bộ quá trình Object Detection chỉ bằng một lần lan truyền xuôi (single forward pass) của mạng CNN.

Điều này khác biệt với các phương pháp hai giai đoạn (Two-stage Detector) như R-CNN hay Faster R-CNN, vốn phải:

1. Sinh các vùng đề xuất (Region Proposal).
2. Phân loại từng vùng riêng biệt.

YOLO kết hợp tất cả các bước trên trong một mô hình duy nhất.

```
Image
      │
      ▼
 CNN Backbone
      │
      ▼
 Detection Head
      │
      ▼
Bounding Boxes
Objectness Score
Class Probability
```

- Đơn giản hóa pipeline.
- Giảm đáng kể thời gian suy luận (Inference).
- Cho phép xử lý ảnh theo thời gian thực.
- Dễ dàng mở rộng và cải tiến trong các phiên bản sau.

Nhờ đó, YOLO đạt tốc độ xử lý rất cao và có thể chạy theo thời gian thực (Real-Time Detection).

## Khái niệm cốt lõi

### Detection dưới dạng Dense Prediction

Trong bài toán __Image Classification__, mô hình chỉ cần dự đoán một nhãn cho toàn bộ ảnh. Nếu có __C__ lớp, đầu ra chỉ gồm __C__ giá trị (logits hoặc xác suất). Trong khi đó, __YOLO__ coi bài toán Object Detection là một bài toán __Dense Prediction__ (dự đoán dày đặc trên toàn bộ ảnh).

Thay vì dự đoán một nhãn duy nhất, YOLO chia ảnh thành lưới kích thước S × S và tại mỗi ô (Grid Cell) đều thực hiện dự đoán. DO đó đầu ra cảu YOLO có kích thước:

$$S \times S \times B (5 + C)$$

Trong đó:
- $S \times S$ : số ô lưới của ảnh.
- $B$ : số Anchor Box tại mỗi ô.
- $C$ : số lớp cần nhận dạng.

Mỗi Anchor Box dự đoán:
- 4 giá trị: $(t_x,t_y,t_w,t_h)$ (Bounding Box Regression).
- 1 giá trị: Objectness Score.
- C giá trị: xác suất các lớp.

### Grid Cell và Anchor Box

#### Grid Cell

YOLO chia ảnh thành lưới $S \times S$, trong đó mỗi Ground Truth được __gán cho Grid Cell chứa tâm của đối tượng__. Cách biểu diễn này giúp mô hình học vị trí cục bộ thay vì hồi quy trực tiếp trên toàn bộ ảnh.

#### Anchor Box

Mỗi Grid Cell chứa nhiều __Anchor Box__ (Prior Boxes) với các kích thước được định nghĩa trước. Thay vì dự đoán Bounding Box từ đầu, mô hình chỉ học __độ lệch (offset)__ so với Anchor tương ứng, giúp việc hồi quy ổn định và chính xác hơn.

Các mô hình hiện đại thường kết hợp __Feature Pyramid Network (FPN)__ để sử dụng nhiều bộ Anchor ở các mức độ phân giải khác nhau, hỗ trợ phát hiện vật thể đa kích thước.

### Giải mã Bounding Box (Bounding Box Decoding)

Các giá trị dự đoán $(t_x,t_y,t_w,t_h)$ được chuyển sang tọa độ thực theo công thức:

$$x = (\sigma (t_x) + c_x) \times stride$$
$$y = (\sigma (t_y) + c_y) \times stride$$

$$w = a_w e^{t_w}$$
$$h = a_h e^{t_h}$$

Trong đó:
- $\sigma(\cdot)$ giới hạn tâm Bounding Box trong Grid Cell.
- $a_w,a_h$ là kích thước Anchor.
- $stride$ chuyển từ Feature Map sang tọa độ ảnh gốc.

### Intersection over Union (IoU)

IoU là thước đo mức độ chồng lấp giữa Bounding Box dự đoán và Ground Truth:

$$IoU = \frac {|A \cap B|} {|A \cup B|}$$

Giá trị IoU nằm trong khoảng [0, 1]:

- IoU = 1: hai Bounding Box trùng khít.
- IoU = 0: không có phần giao nhau.

IoU được sử dụng để đánh giá Prediction và làm tiêu chí trong __Non-Maximum Suppression (NMS)__.

### Hàm mất mát (YOLO Loss)

YOLO tối ưu đồng thời nhiều nhiệm vụ:

$$L = \lambda_{coord} L_{box} + \lambda_{obj} L_{obj} + \lambda_{noobj} L_{noobj} + \lambda_{cls} L_{cls}$$

Trong đó:
- $L_{box}$: hồi quy Bounding Box.
- $L_{obj}$: dự đoán Objectness cho vùng có vật thể.
- $L_{noobj}$: dự đoán vùng không có vật thể.
- $L_{cls}$: phân loại đối tượng.

Chỉ các Grid Cell chứa đối tượng mới tham gia tính __Box Loss__ và __Classification Loss__, trong khi các ô còn lại chỉ đóng góp vào __No-object Loss__.

Các phiên bản hiện đại thường thay __MSE__ bằng __CIoU/DIoU Loss__ và sử dụng __Focal Loss__ để xử lý mất cân bằng dữ liệu.

### Chỉ số đánh giá (Detection Metrics)

Hiệu năng của mô hình Object Detection thường được đánh giá bằng:

- __Precision@0.5__: tỷ lệ dự đoán đúng trong các dự đoán dương.
- __Recall@0.5__: tỷ lệ đối tượng thực được phát hiện.
- __AP@0.5__: diện tích dưới đường cong Precision–Recall tại IoU = 0.5.
- __mAP@0.5:0.95__: trung bình AP trên các ngưỡng IoU từ 0.50 đến 0.95, là chỉ số chuẩn của COCO.

Diễn giải kết quả:

- __mAP@0.5 cao nhưng mAP@0.5:0.95 thấp__: Bounding Box chưa định vị chính xác, cần cải thiện Box Regression.
- __Precision cao, Recall thấp__: mô hình quá thận trọng, cần điều chỉnh Confidence Threshold hoặc Objectness.
- __Recall cao, Precision thấp__: mô hình tạo nhiều False Positive, cần cải thiện Classification hoặc NMS.

## Build It

### Step 1: IoU

IoU (Intersection over Union) là thước đo mức độ chồng lấp giữa **Bounding Box dự đoán (Prediction)** và **Bounding Box thực (Ground Truth)**. Đây là chỉ số quan trọng trong Object Detection, được sử dụng để:

- Đánh giá chất lượng Bounding Box.
- Gán Anchor Box với Ground Truth trong quá trình huấn luyện.
- Loại bỏ các Bounding Box trùng lặp trong thuật toán **Non-Maximum Suppression (NMS)**.


```python
import numpy as np

def box_iou(boxes_a, boxes_b):
    """
    Compute pairwise IoU between two sets of bounding boxes.

    Parameters
    ----------
    boxes_a : ndarray of shape (N, 4)
        Bounding boxes in (x1, y1, x2, y2) format.

    boxes_b : ndarray of shape (M, 4)
        Bounding boxes in (x1, y1, x2, y2) format.

    Returns
    -------
    ndarray of shape (N, M)
        Pairwise IoU matrix.
    """

    # Coordinates of boxes A
    ax1, ay1, ax2, ay2 = (
        boxes_a[:, 0],
        boxes_a[:, 1],
        boxes_a[:, 2],
        boxes_a[:, 3],
    )

    # Coordinates of boxes B
    bx1, by1, bx2, by2 = (
        boxes_b[:, 0],
        boxes_b[:, 1],
        boxes_b[:, 2],
        boxes_b[:, 3],
    )

    # Intersection coordinates
    inter_x1 = np.maximum(ax1[:, None], bx1[None, :])
    inter_y1 = np.maximum(ay1[:, None], by1[None, :])
    inter_x2 = np.minimum(ax2[:, None], bx2[None, :])
    inter_y2 = np.minimum(ay2[:, None], by2[None, :])

    # Width and height of intersection
    inter_w = np.clip(inter_x2 - inter_x1, 0, None)
    inter_h = np.clip(inter_y2 - inter_y1, 0, None)

    # Intersection area
    inter = inter_w * inter_h

    # Area of boxes
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)

    # Union area
    union = area_a[:, None] + area_b[None, :] - inter

    # IoU
    return inter / np.clip(union, 1e-8, None)
```

### Step 2: Non-Maximum Suppression (NMS)

Non-Maximum Suppression (NMS) là thuật toán dùng để **loại bỏ các Bounding Box dự đoán trùng lặp**, chỉ giữ lại Bounding Box có **Confidence Score** cao nhất cho mỗi đối tượng.

Thuật toán NMS được thực hiện theo các bước:

1. **Sắp xếp** các Bounding Box theo **Confidence Score giảm dần**.
2. **Giữ** Bounding Box có điểm số cao nhất.
3. **Tính IoU** giữa Bounding Box được giữ và các Bounding Box còn lại.
4. **Loại bỏ** các Bounding Box có: $IoU \gt iou\_threshold$
5. Lặp lại cho đến khi không còn Bounding Box nào.

- Sắp xếp Bounding Box: **O(N log N)**.
- Kết quả của thuật toán là **xác định (deterministic)** và có hành vi tương đương `torchvision.ops.nms` khi sử dụng cùng dữ liệu đầu vào.

```python
import numpy as np

def nms(boxes, scores, iou_threshold=0.45):
    """
    Parameters
    ----------
    boxes : ndarray of shape (N, 4)
        Bounding boxes in (x1, y1, x2, y2) format.

    scores : ndarray of shape (N,)
        Confidence scores of each bounding box.

    iou_threshold : float, default=0.45
        IoU threshold for suppressing overlapping boxes.

    Returns
    -------
    ndarray
        Indices of selected bounding boxes.
    """

    order = np.argsort(-scores)
    keep = []

    while len(order) > 0:
        i = order[0]
        keep.append(i)

        if len(order) == 1:
            break

        rest = order[1:]
        ious = box_iou(boxes[[i]], boxes[rest])[0]
        order = rest[ious <= iou_threshold]
    return np.array(keep, dtype=np.int64)
```

### Step 3: Mã hóa và giải mã Bounding Box (Box Encoding & Decoding)

Trong YOLO, mô hình **không dự đoán trực tiếp tọa độ Bounding Box**, mà dự đoán các **offset** $(t_x,t_y,t_w,t_h)$ so với **Anchor Box**. Quá trình này gồm hai bước:

- **Encoding:** chuyển Bounding Box thực thành các giá trị mục tiêu để huấn luyện.
- **Decoding:** chuyển đầu ra của mô hình thành Bounding Box trên ảnh.

```python
import numpy as np

def encode(box_xyxy, cell_x, cell_y, stride, anchor_wh):
    """
    Encode a bounding box into YOLO regression targets.

    Parameters
    ----------
    box_xyxy : ndarray (4,)
        Bounding box in (x1, y1, x2, y2) format.

    cell_x, cell_y : int
        Grid cell coordinates.

    stride : int
        Feature map stride.

    anchor_wh : tuple
        Anchor width and height.

    Returns
    -------
    ndarray (4,)
        Encoded targets (tx, ty, tw, th).
    """

    x1, y1, x2, y2 = box_xyxy

    cx = 0.5 * (x1 + x2)
    cy = 0.5 * (y1 + y2)

    w = x2 - x1
    h = y2 - y1

    tx = cx / stride - cell_x
    ty = cy / stride - cell_y

    tw = np.log(w / anchor_wh[0] + 1e-8)
    th = np.log(h / anchor_wh[1] + 1e-8)

    return np.array([tx, ty, tw, th])


def decode(tx_ty_tw_th, cell_x, cell_y, stride, anchor_wh):

    tx, ty, tw, th = tx_ty_tw_th

    cx = (sigmoid(tx) + cell_x) * stride
    cy = (sigmoid(ty) + cell_y) * stride

    w = anchor_wh[0] * np.exp(tw)
    h = anchor_wh[1] * np.exp(th)

    return np.array([
        cx - w / 2,
        cy - h / 2,
        cx + w / 2,
        cy + h / 2
    ])


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))
```

#### Encoding

Encoding chuyển Bounding Box từ tọa độ ảnh sang các giá trị hồi quy:

- **$(t_x,t_y)$:** độ lệch tâm so với Grid Cell.
- **$(t_w,t_h)$:** tỷ lệ thay đổi kích thước so với Anchor Box.

Các giá trị này được sử dụng làm **Ground Truth** trong quá trình huấn luyện.

#### Decoding

Decoding chuyển đầu ra của mô hình $(t_x,t_y,t_w,t_h)$ thành Bounding Box thực trên ảnh bằng cách:

- Tính tâm Bounding Box từ Grid Cell và `stride`.
- Khôi phục chiều rộng, chiều cao từ Anchor Box bằng hàm mũ (`exp`).
- Chuyển từ tọa độ tâm `(cx, cy, w, h)` sang định dạng `(x1, y1, x2, y2)`.

### Step 4: Xây dựng YOLO Head tối giản (Minimal YOLO Head)

YOLO Head là tầng cuối của mô hình, có nhiệm vụ **chuyển Feature Map từ Backbone thành các dự đoán Object Detection**. Mỗi vị trí trên Feature Map sẽ dự đoán nhiều Anchor Box, mỗi Anchor gồm:

- 4 giá trị Bounding Box: `(tx, ty, tw, th)`
- 1 Objectness Score
- `C` xác suất lớp

```python
import torch
import torch.nn as nn


class YOLOHead(nn.Module):
    def __init__(self, in_c, num_anchors, num_classes):
        super().__init__()

        self.num_anchors = num_anchors
        self.num_classes = num_classes

        self.conv = nn.Conv2d(
            in_channels=in_c,
            out_channels=num_anchors * (5 + num_classes),
            kernel_size=1
        )

    def forward(self, x):
        n, _, h, w = x.shape
        y = self.conv(x)

        y = y.view(n, self.num_anchors, 5 + self.num_classes, h, w)

        y = y.permute(0, 3, 4, 1, 2).contiguous()
        return y
```

Output shape: (N, H, W, num_anchors, 5 + C). The last dimension holds [tx, ty, tw, th, obj, cls_0, ..., cls_{C-1}].

### Step 5: Gán Ground Truth cho Anchor (Ground Truth Assignment)

Trong quá trình huấn luyện, mỗi **Ground Truth Bounding Box** phải được gán cho một **Grid Cell** và một **Anchor Box** chịu trách nhiệm dự đoán. YOLOv2/v3 lựa chọn Anchor có **Shape IoU** lớn nhất với Ground Truth để làm nhãn huấn luyện.

Quá trình gán Ground Truth gồm các bước:

1. **Xác định Grid Cell** chứa tâm của Ground Truth Bounding Box.
2. **Tính Shape IoU** giữa Ground Truth và tất cả Anchor Box.
3. **Chọn Anchor** có Shape IoU lớn nhất.
4. **Mã hóa Bounding Box** thành $(t_x,t_y,t_w,t_h)$.
5. Gán:
   - **Objectness = 1**.
   - **Class Label = 1** theo phương pháp One-Hot Encoding.
6. Đánh dấu Anchor đã được gán trong `has_obj`.


```python
import numpy as np

def assign_targets(boxes_xyxy, classes, anchors, stride, grid_size, num_classes):
    """
    Assign ground-truth boxes to grid cells and anchors.
    """

    num_anchors = len(anchors)

    target = np.zeros(
        (grid_size, grid_size, num_anchors, 5 + num_classes),
        dtype=np.float32,
    )

    has_obj = np.zeros(
        (grid_size, grid_size, num_anchors),
        dtype=bool,
    )

    for box, cls in zip(boxes_xyxy, classes):

        x1, y1, x2, y2 = box

        cx = 0.5 * (x1 + x2)
        cy = 0.5 * (y1 + y2)

        gx = int(cx / stride)
        gy = int(cy / stride)

        bw = x2 - x1
        bh = y2 - y1

        # Shape IoU between GT box and anchors
        ious = np.array([
            (min(bw, aw) * min(bh, ah)) / (bw * bh + aw * ah- min(bw, aw) * min(bh, ah)) for aw, ah in anchors
        ])

        best = int(np.argmax(ious))

        aw, ah = anchors[best]

        target[gy, gx, best, 0] = cx / stride - gx
        target[gy, gx, best, 1] = cy / stride - gy
        target[gy, gx, best, 2] = np.log(bw / aw + 1e-8)
        target[gy, gx, best, 3] = np.log(bh / ah + 1e-8)
        target[gy, gx, best, 4] = 1.0
        target[gy, gx, best, 5 + cls] = 1.0

        has_obj[gy, gx, best] = True

    return target, has_obj
```

Hàm trả về:

- **`target`**: Tensor kích thước $(Grid, Grid, Anchor, 5 + C)$ chứa các giá trị huấn luyện gồm: `(tx, ty, tw, th, objectness, class)`

- **`has_obj`**: Ma trận Boolean xác định Anchor nào được gán với Ground Truth.

---

#### Lưu ý

YOLOv2 và YOLOv3 sử dụng **Shape IoU** để chọn Anchor phù hợp nhất. Các phiên bản mới như **YOLOv5, YOLOv7 và YOLOv8** mở rộng cơ chế này bằng các phương pháp **Task-Aligned Assignment** hoặc **Dynamic-k Matching**, nhưng đều dựa trên nguyên lý lựa chọn Anchor có mức độ phù hợp cao với Ground Truth.

### Step 6: Hàm mất mát YOLO (YOLO Loss)

YOLO là mô hình **đa nhiệm vụ (Multi-task Learning)** nên hàm mất mát được xây dựng từ ba thành phần chính:

- **Bounding Box Regression Loss**
- **Objectness Loss**
- **Classification Loss**

Hàm mất mát của YOLO gồm bốn thành phần:

- **Bounding Box Loss ($L_{box}$):** đo sai số giữa Bounding Box dự đoán và Ground Truth, chỉ tính trên các Anchor chứa đối tượng.

- **Positive Objectness Loss ($L_{obj}^{+}$):** huấn luyện mô hình dự đoán đúng các Anchor có đối tượng.

- **Negative Objectness Loss ($L_{obj}^{-}$):** huấn luyện mô hình dự đoán các Anchor không chứa đối tượng, giúp giảm False Positive.

- **Classification Loss ($L_{cls}$):** đánh giá khả năng phân loại đối tượng, chỉ tính trên các Anchor chứa đối tượng.

Tổng hàm mất mát:

$$
L=\lambda_{coord}L_{box}
+\lambda_{obj}L_{obj}^{+}
+\lambda_{noobj}L_{obj}^{-}
+\lambda_{cls}L_{cls}
$$

```python
import torch
import torch.nn.functional

def yolo_loss(pred, target, has_obj, lambda_coord=5.0, lambda_obj=1.0, lambda_noobj=0.5, lambda_cls=1.0):

    has_obj_t = torch.from_numpy(has_obj).bool()
    target_t = torch.from_numpy(target).float()

    # Bounding box regression loss
    box_pred = pred[..., :4][has_obj_t]
    box_true = target_t[..., :4][has_obj_t]

    loss_box = torch.nn.functional.mse_loss(box_pred, box_true, reduction="sum")

    # Objectness loss
    obj_pred = pred[..., 4]
    obj_true = target_t[..., 4]

    loss_obj_pos = torch.nn.functional.binary_cross_entropy_with_logits( obj_pred[has_obj_t], obj_true[has_obj_t], reduction="sum")

    loss_obj_neg = torch.nn.functional.binary_cross_entropy_with_logits( obj_pred[~has_obj_t], obj_true[~has_obj_t], reduction="sum")

    # Classification loss
    cls_pred = pred[..., 5:][has_obj_t]
    cls_true = target_t[..., 5:][has_obj_t]

    loss_cls = F.binary_cross_entropy_with_logits(
        cls_pred,
        cls_true,
        reduction="sum",
    )

    # Total loss
    total = (lambda_coord * loss_box
        + lambda_obj * loss_obj_pos
        + lambda_noobj * loss_obj_neg
        + lambda_cls * loss_cls
    )

    return total, {
        "box": loss_box.item(),
        "obj_pos": loss_obj_pos.item(),
        "obj_neg": loss_obj_neg.item(),
        "cls": loss_cls.item(),
    }
```

Các hệ số $\lambda$ dùng để cân bằng đóng góp của từng thành phần trong tổng Loss:

| Tham số | Giá trị mặc định | Vai trò |
|---------|:----------------:|----------|
| $\lambda_{coord}$ | 5.0 | Tăng trọng số cho Bounding Box Regression |
| $\lambda_{obj}$ | 1.0 | Trọng số Positive Objectness |
| $\lambda_{noobj}$ | 0.5 | Giảm ảnh hưởng của các Anchor không chứa đối tượng |
| $\lambda_{cls}$ | 1.0 | Trọng số Classification Loss |

Giá trị **$\lambda_{coord}=5$** và **$\lambda_{noobj}=0.5$** được đề xuất từ **YOLOv1** và vẫn là lựa chọn mặc định hợp lý trong nhiều mô hình YOLO hiện nay.

### Step 7: Suy luận (Inference Pipeline)

Trong giai đoạn suy luận (Inference), đầu ra của YOLO Head được chuyển thành các Bounding Box cuối cùng thông qua bốn bước:

1. **Decode Bounding Box:** chuyển các giá trị dự đoán $(t_x,t_y,t_w,t_h)$ thành tọa độ Bounding Box trên ảnh.

2. **Tính Confidence Score:** kết hợp **Objectness Score** và xác suất lớp để đánh giá độ tin cậy của mỗi dự đoán.

3. **Confidence Threshold:** loại bỏ các Bounding Box có Confidence nhỏ hơn ngưỡng (`conf_threshold`) nhằm giảm các dự đoán không đáng tin cậy.

4. **Non-Maximum Suppression (NMS):** loại bỏ các Bounding Box chồng lấp, chỉ giữ lại Bounding Box có Confidence cao nhất cho mỗi đối tượng.


```python
import numpy as np

def postprocess(pred_tensor, anchors, stride, img_size, conf_threshold=0.25, iou_threshold=0.45):
    pred = pred_tensor.detach().cpu().numpy()

    grid_h = pred.shape[1]
    grid_w = pred.shape[2]

    num_anchors = len(anchors)

    boxes = []
    scores = []
    classes = []

    for gy in range(grid_h):
        for gx in range(grid_w):
            for a in range(num_anchors):

                tx, ty, tw, th, obj, *cls = pred[0, gy, gx, a]

                score = sigmoid(obj) * sigmoid(np.array(cls)).max()

                if score < conf_threshold:
                    continue

                cls_idx = int(np.argmax(cls))

                cx = (sigmoid(tx) + gx) * stride
                cy = (sigmoid(ty) + gy) * stride

                w = anchors[a][0] * np.exp(tw)
                h = anchors[a][1] * np.exp(th)

                boxes.append([
                    cx - w / 2,
                    cy - h / 2,
                    cx + w / 2,
                    cy + h / 2,
                ])

                scores.append(float(score))
                classes.append(cls_idx)

    if len(boxes) == 0:
        return (
            np.zeros((0, 4)),
            np.zeros((0,)),
            np.zeros((0,), dtype=int),
        )

    boxes = np.array(boxes)
    scores = np.array(scores)
    classes = np.array(classes)

    keep = nms(boxes, scores, iou_threshold)

    return boxes[keep], scores[keep], classes[keep]
```

Hàm `postprocess()` trả về ba thành phần:

- **`boxes`**: Bounding Box cuối cùng sau NMS.
- **`scores`**: Confidence Score của từng Bounding Box.
- **`classes`**: Nhãn lớp tương ứng.


## Key Terms

| **Thuật ngữ**                              | **Cách gọi phổ biến**      | **Ý nghĩa**                                                                                                                                                     |
| ------------------------------------------ | -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Anchor**                                 | Box Prior                  | Bounding Box mẫu (Prior Box) được định nghĩa trước tại mỗi Grid Cell, mô hình chỉ dự đoán các độ lệch (offset) so với Anchor thay vì dự đoán trực tiếp tọa độ.  |
| **IoU (Intersection over Union)**          | Overlap                    | Thước đo mức độ chồng lấp giữa Bounding Box dự đoán và Ground Truth, được sử dụng để đánh giá chất lượng dự đoán và trong NMS.                                  |
| **NMS (Non-Maximum Suppression)**          | Deduplicate                | Thuật toán loại bỏ các Bounding Box dự đoán trùng lặp bằng cách giữ lại Bounding Box có Confidence cao nhất và loại bỏ các Bounding Box có IoU vượt quá ngưỡng. |
| **Objectness**                             | "Is there something here?" | Điểm số dự đoán xác suất một Anchor tại Grid Cell có chứa đối tượng hay không.                                                                                  |
| **Grid Stride**                            | Downsample Factor          | Tỷ lệ giữa kích thước ảnh đầu vào và Feature Map. Ví dụ, ảnh **416×416** với Feature Map **13×13** có **Stride = 32**.                                          |
| **AP@0.5 (Average Precision @ IoU = 0.5)** | PASCAL VOC AP              | Diện tích dưới đường cong Precision–Recall tại ngưỡng **IoU = 0.5**, được tính riêng cho từng lớp.                                                              |
| **mAP (Mean Average Precision)**           | Mean Average Precision     | Giá trị trung bình của AP trên tất cả các lớp; với COCO còn được tính trên nhiều ngưỡng IoU khác nhau.                                                          |
| **mAP@0.5:0.95**                           | COCO AP                    | Trung bình AP tại các ngưỡng IoU từ **0.50 đến 0.95** (bước nhảy 0.05), là chỉ số đánh giá nghiêm ngặt và phổ biến nhất của bộ dữ liệu COCO.                    |
