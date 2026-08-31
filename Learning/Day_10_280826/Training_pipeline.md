Đây là phần rất quan trọng nếu muốn bài toán **Transformer Encoder Regression cho UCI** đi từ mức “thử nghiệm trên notebook” sang một **training pipeline có tính reproducible và có thể resume**.

Điểm cốt lõi là phải tách:

> **Data → Configuration → Training → Checkpoint → Validation → Experiment Artifact**

thay vì mỗi lần thử nghiệm lại chạy một notebook từ đầu.

---

# 1. Không nên train bằng Notebook

Notebook phù hợp để:

* EDA;
* visualization;
* kiểm tra dữ liệu;
* phân tích kết quả.

Nhưng training chính nên chuyển thành:

```text
project/
│
├── configs/
│   ├── baseline.yaml
│   ├── transformer_l36.yaml
│   └── transformer_l72.yaml
│
├── src/
│   ├── data/
│   ├── models/
│   ├── training/
│   └── evaluation/
│
├── scripts/
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
│
├── experiments/
│   └── ...
│
└── README.md
```

Sau đó chỉ cần:

```bash
python scripts/train.py --config configs/transformer_l36.yaml
```

Training trở thành một **experiment có cấu hình cố định**, thay vì trạng thái nằm trong notebook.

---

# 2. Configuration phải là một phần của Experiment

Không nên hard-code:

```python
hidden_dim = 128
num_layers = 4
lr = 1e-4
batch_size = 64
epochs = 100
```

trong code.

Thay vào đó:

```yaml
model:
  d_model: 128
  n_heads: 4
  num_layers: 3
  dropout: 0.1

training:
  batch_size: 64
  learning_rate: 0.0001
  max_epochs: 100
  weight_decay: 0.0001

data:
  lookback: 36
  horizon: 1

seed: 42
```

Khi đó:

$$
Experiment
=
Configuration
+
Code
+
Data
+
Artifacts
$$

Đây là nền tảng của **reproducibility**.

---

# 3. Artifact cần lưu những gì?

Một checkpoint **không nên chỉ lưu model weights**.

Ví dụ:

```text
experiments/
└── exp_001/
    ├── config.yaml
    ├── model.pt
    ├── checkpoint_last.pt
    ├── checkpoint_best.pt
    ├── optimizer.pt
    ├── scheduler.pt
    ├── scaler_x.pkl
    ├── scaler_y.pkl
    ├── metrics.csv
    ├── history.json
    └── manifest.json
```

Thực tế tốt hơn là gom trạng thái training vào một checkpoint:

```python
torch.save({
    "epoch": epoch,
    "model_state_dict": model.state_dict(),
    "optimizer_state_dict": optimizer.state_dict(),
    "scheduler_state_dict": scheduler.state_dict(),
    "best_val_rmse": best_val_rmse,
    "config": config,
    "random_state": ...,
}, path)
```

---

# 4. Tại sao phải lưu optimizer?

Đây là lỗi rất thường gặp.

Giả sử:

```text
Epoch 1 → 50
```

sau đó dừng.

Nếu chỉ load:

```python
model.load_state_dict(...)
```

rồi tiếp tục:

```text
Epoch 51
```

thì model weights được khôi phục nhưng **optimizer state không được khôi phục**.

Đặc biệt với Adam:

$$
m_t
=
\beta_1m_{t-1}
+
(1-\beta_1)g_t
$$

$$
v_t
=
\beta_2v_{t-1}
+
(1-\beta_2)g_t^2
$$

Optimizer cần:

$$
m_t,v_t
$$

để tiếp tục đúng trajectory.

Do đó:

$$
\boxed{
Resume\ Training
\neq
Load\ Model\ Weights
}
$$

mà phải:

$$
\boxed{
Resume
=
Model
+
Optimizer
+
Scheduler
+
Epoch
+
Training\ State
}
$$

---

# 5. Scheduler cũng phải được lưu

Ví dụ dùng:

```text
CosineAnnealingLR
ReduceLROnPlateau
OneCycleLR
```

thì learning rate tại epoch $n$ phụ thuộc training history.

Nếu restart scheduler:

```text
Epoch 1
```

trong khi model đang ở:

```text
Epoch 50
```

thì learning-rate trajectory bị sai.

Do đó checkpoint cần:

```python
"scheduler_state_dict": scheduler.state_dict()
```

---

# 6. Resume từ epoch n như thế nào?

Ví dụ:

```text
checkpoint_last.pt
```

chứa:

```text
epoch = 37
```

Khi chạy:

```bash
python scripts/train.py \
    --config configs/transformer_l36.yaml \
    --resume experiments/exp_001/checkpoint_last.pt
```

training script:

```python
checkpoint = torch.load(path)

model.load_state_dict(checkpoint["model_state_dict"])
optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
scheduler.load_state_dict(checkpoint["scheduler_state_dict"])

start_epoch = checkpoint["epoch"] + 1
```

sau đó:

```python
for epoch in range(start_epoch, max_epochs + 1):
    train(...)
    validate(...)
    save_checkpoint(...)
```

Như vậy:

```text
Epoch 1 ───────── Epoch 37
                       │
                 checkpoint
                       │
                    crash
                       │
                       ▼
                 resume Epoch 38
```

Không cần train lại từ epoch 1.

---

# 7. Nên có `last` và `best` checkpoint

Hai checkpoint này có mục đích khác nhau.

### `checkpoint_last.pt`

Checkpoint mới nhất:

$$
\theta_{last}
$$

dùng để **resume training**.

Ví dụ máy bị crash tại epoch 73:

```text
checkpoint_last.pt
→ epoch 73
```

---

### `checkpoint_best.pt`

Model có validation performance tốt nhất:

$$
\theta^*
=
\arg\min_{\theta}
RMSE_{val}
$$

dùng để **final evaluation**.

Ví dụ:

```text
Epoch 31 → RMSE 96
Epoch 42 → RMSE 91  ← best
Epoch 73 → RMSE 95
```

thì:

```text
last  = epoch 73
best  = epoch 42
```

Không được nhầm hai khái niệm này.

---

# 8. Chọn epoch như thế nào?

Không nên quyết định:

> “Train đúng 100 epochs vì 100 có vẻ hợp lý.”

Epoch là **training budget**, không phải một đặc tính cố định của dataset.

Có thể sử dụng:

## Early stopping

Theo validation metric:

$$
RMSE_{val}^{(e)}
$$

Nếu không cải thiện trong $P$ epochs:

$$
RMSE_{val}^{(e)}
\geq
RMSE_{best}
$$

thì dừng.

Ví dụ:

```text
patience = 10
```

Nếu 10 epochs liên tiếp không cải thiện:

```text
Epoch 41  best
Epoch 42  worse
...
Epoch 51  worse
             ↓
         stop training
```

---

# 9. Nhưng Early Stopping phải dùng Validation, không Test

Đây là nguyên tắc cực kỳ quan trọng:

```text
TRAIN
   │
   ├── fit model
   └── fit scaler
   │
   ▼
VALIDATION
   │
   ├── early stopping
   ├── hyperparameter selection
   └── model selection
   │
   ▼
TEST
   │
   └── final evaluation ONLY
```

Test không được dùng để quyết định:

* epoch;
* learning rate;
* lookback;
* feature engineering;
* architecture;
* feature selection;
* early stopping.

Nếu làm:

```text
Epoch 10 → test
Epoch 20 → test
Epoch 30 → test
...
```

thì test đã trở thành một phần của training process.

Đó là **test leakage**.

---

# 10. Data leakage trong pipeline này có nhiều tầng

Không chỉ có target leakage.

### Leakage 1 — Scaling

Sai:

```python
scaler.fit(all_data)
```

Đúng:

```text
Train
 ↓
fit scaler
 ↓
transform Train
transform Validation
transform Test
```

$$
\mu_{train},\sigma_{train}
$$

phải được dùng cho tất cả partition.

---

### Leakage 2 — Feature engineering

Ví dụ rolling mean:

$$
MA_t
=
mean(x_{t-w+1},...,x_t)
$$

hợp lệ.

Nhưng:

$$
MA_t
=
mean(x_{t-k},...,x_{t+k})
$$

có thể chứa future.

---

### Leakage 3 — Feature selection

Không được:

```text
Train + Validation + Test
        ↓
feature importance
        ↓
select features
```

Đúng:

```text
Train
  ↓
feature selection
  ↓
Selected features
  ↓
Validation
```

Nếu feature selection sử dụng test performance thì test bị leakage.

---

### Leakage 4 — Hyperparameter tuning

Không được:

```text
L=36 → Test RMSE
L=72 → Test RMSE
L=144 → Test RMSE
```

rồi chọn L tốt nhất.

Đúng:

```text
Train
   ↓
Validation
   ↓
select L
   ↓
LOCK
   ↓
Test
```

---

# 11. Đặc biệt với Time Series: không được random split

Với UCI:

```text
t1 t2 t3 ... t10000 t10001 ...
```

phải giữ chronological order:

```text
Train       Validation       Test
|-------------|---------------|
70%             15%            15%
```

Không:

```python
train_test_split(..., shuffle=True)
```

vì sẽ làm tương lai xuất hiện trong training.

---

# 12. Sliding Window cũng có vấn đề leakage

Giả sử:

$$
L=36,\quad H=1
$$

Window:

```text
X: t1 ... t36
Y: t37
```

Window tiếp:

```text
X: t2 ... t37
Y: t38
```

Nếu chia dataset **sau khi tạo tất cả windows** bằng random split:

```text
Train:
t1 ... t36 → t37

Test:
t2 ... t37 → t38
```

thì train và test chia sẻ phần lớn observations.

Đây là một dạng **temporal contamination**.

Do đó với time series nên:

$$
\boxed{
Split\ Timeline
\rightarrow
Create\ Windows
}
$$

thay vì:

$$
Create\ Windows
\rightarrow
Random\ Split
$$

---

# 13. Artifact nên lưu cả Data Manifest

Để experiment có thể tái lập, nên lưu:

```json
{
  "dataset": "UCI Appliances Energy Prediction",
  "split": {
    "train": "70%",
    "validation": "15%",
    "test": "15%"
  },
  "lookback": 36,
  "horizon": 1,
  "sampling_interval": "10min",
  "feature_set": "selected_v2",
  "scaler": "train_only_standard_scaler",
  "seed": 42
}
```

Quan trọng hơn nữa là version:

```text
data_version
feature_version
model_version
training_version
```

Ví dụ:

```text
DATA-v1
FEATURE-v3
TRANSFORMER-v2
TRAIN-v1
```

Nếu sau này feature engineering thay đổi, bạn biết chính xác model được train bằng representation nào.

---

# 14. Metrics nên lưu thành CSV/JSON

Ví dụ:

```text
epoch,train_loss,val_mae,val_rmse,val_r2,lr
1,0.821,82.4,111.2,0.61,1e-4
2,0.734,79.1,106.7,0.65,1e-4
...
42,0.312,65.1,91.2,0.77,5e-5
```

Từ đây có thể vẽ:

```text
Training Loss
Validation RMSE
Learning Rate
```

mà không cần mở notebook để biết training đã diễn ra thế nào.

---

# 15. Cấu trúc artifact mình khuyến nghị

Với bài UCI của bạn, có thể tổ chức:

```text
experiments/
└── transformer/
    └── exp_001/
        │
        ├── config.yaml
        ├── manifest.json
        │
        ├── checkpoints/
        │   ├── checkpoint_last.pt
        │   └── checkpoint_best.pt
        │
        ├── preprocessing/
        │   ├── x_scaler.pkl
        │   └── y_scaler.pkl
        │
        ├── metrics/
        │   ├── history.csv
        │   └── summary.json
        │
        └── logs/
            └── train.log
```

Đây chính là **experiment artifact**.

---

# 16. Quan trọng nhất: Test phải "LOCK"

Trong toàn bộ quá trình:

```text
                 TRAIN
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
 Feature Selection       Feature Engineering
        │                     │
        └──────────┬──────────┘
                   ▼
             Model Training
                   │
                   ▼
              Validation
                   │
       ┌───────────┴───────────┐
       ▼                       ▼
 Early Stopping          Hyperparameter
                         Selection
       │                       │
       └───────────┬───────────┘
                   ▼
             BEST MODEL
                   │
                   ▼
             ┌───────────┐
             │   TEST    │
             │   LOCK    │
             └───────────┘
                   │
                   ▼
             Final RMSE
             Final MAE
             Final R²
```

Test chỉ mở **một lần ở bước cuối**.

---

# 17. Cách chọn epoch hợp lý cho nghiên cứu

Tôi sẽ không chọn một epoch cố định ngay từ đầu.

Nên đặt:

$$
E_{max}
$$

lớn, ví dụ:

$$
E_{max}=200
$$

và dùng:

$$
patience=15
$$

Khi đó:

$$
e^*
=
\arg\min_e RMSE_{val}(e)
$$

và training dừng khi không có improvement trong $15$ epochs.

Sau đó:

```text
best epoch = e*
```

được lưu trong:

```text
summary.json
```

Ví dụ:

```json
{
  "best_epoch": 47,
  "best_val_rmse": 91.24,
  "test_rmse": 94.81
}
```

**Không được nhìn `test_rmse` để quyết định rằng epoch 47 là tốt.**

---

## 18. Một điểm tinh tế: Resume không được làm thay đổi experiment

Nếu experiment đang chạy:

```text
seed = 42
batch_size = 64
lr = 1e-4
lookback = 36
```

và checkpoint tại epoch 50, resume phải sử dụng **đúng configuration đó**.

Không nên:

```text
checkpoint: lr=1e-4
resume:     lr=5e-5
```

mà không tạo experiment mới.

Nếu muốn thay đổi:

```text
exp_001
   ↓
modify config
   ↓
exp_002
```

Còn:

```text
exp_001
   ↓
resume
```

phải tiếp tục cùng experiment.

---

## 19. Tóm lại kiến trúc training nên là

```text
                config.yaml
                     │
                     ▼
              train.py
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
      DataLoader             Model
          │                     │
          └──────────┬──────────┘
                     ▼
                 Training
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
       Validation          Checkpoint
          │                     │
          ▼                     ▼
   Early Stopping         last / best
          │
          ▼
      Final Model
          │
          ▼
       Test LOCK
```

Và toàn bộ quá trình được mô tả bởi:

$$
\boxed{
Experiment
=
Data\ Version
+
Feature\ Version
+
Config
+
Code\ Version
+
Checkpoint
+
Metrics
}
$$

Đối với bài **Transformer Regression trên UCI**, đây là bước chuyển rất quan trọng từ **“model training”** sang **“controlled scientific experiment”**. Khi kết hợp với phần trước, pipeline nghiên cứu hoàn chỉnh sẽ là:

$$
\boxed{
Data\ Quality
\rightarrow
Feature\ Selection
\rightarrow
Feature\ Engineering
\rightarrow
Lookback\ Selection
\rightarrow
Transformer
\rightarrow
Controlled\ Training
\rightarrow
Ablation
\rightarrow
Test
}
$$

Trong đó **Validation là nơi để ra quyết định**, còn **Test chỉ là nơi để báo cáo kết quả cuối cùng**.
