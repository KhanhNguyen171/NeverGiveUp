Ta ôn một chút về checkpoint, script, real-time monitoring, log, xây dựng một quy trình training tự động không cần phải tự control theo jupyter notebook.

Mục tiêu

```
Config
  ↓
Training Script
  ↓
Training Loop
  ├── Checkpoint
  ├── Logging
  └── Real-time Monitoring
  ↓
Resume / Stop / Continue
```

## 1. Checkpoint

Checkpoint là snapshot của training state tại một thời điểm. Model weights giúp khôi phục model; training checkpoint giúp khôi phục quá trình training.

Với PyTorch, tối thiểu nên lưu:

```
checkpoint/
├── epoch
├── model_state
├── optimizer_state
├── scheduler_state
├── loss
├── metrics
└── training_config
```

Có thể duy trì

```
latest.pt    # checkpoint mới nhất
best.pt      # model tốt nhất
```

Mục đích: không phải train lại từ đầu khi crash, restart hoặc training kéo dài nhiều ngày.

### Một số phiên bản checkpoint

- `latest checkpoint`: Checkpoint mới nhất.
- `best checkpoint`: Lưu model đạt metric validation tốt nhất.
- `Periodic checkpoint`: Lưu định kỳ hoặc theo step
    - dùng khi training rất lâu, muốn roll back, muốn phân tích model theo từng giai đoạn.
    - Không nhất thiết phải giữ tất cả; production thường dùng retention policy để xóa checkpoint cũ.
- `Final checkpoint`: Sau khi training hoàn tất:
    - Nó đại diện cho trạng thái cuối cùng của training.

### Model checkpoint vs Training checkpoint

- Model checkpoint:
    - để: `Inference`, `Evaluation`, `Deployment` -> không chứa `optimizer`
- Training checkppoint
    - model: `optimizer`, `scheduler`, `epoch`, `step`, `metrics`, `config` -> dùng để `resume training`

## 2. Script

Thay vì chạy từng cell trong Jupyter, chuyển training thành executable script:

```
project/
├── configs/
│   └── config.yaml
├── src/
│   ├── model.py
│   ├── dataset.py
│   ├── trainer.py
│   ├── checkpoint.py
│   └── logger.py
├── scripts/
│   └── train.py
└── outputs/
```

```
run:

python scripts/train.py
```

Script tự đọc config, khởi tạo model → train → validate → log → checkpoint.

## 3. real-time monitoring

Theo dõi training ngay trong lúc process đang chạy.

Các metric chính:

```
Epoch
Step
Train Loss
Validation Loss
Train Accuracy
Validation Accuracy
Learning Rate
Training Time
```

Có thể hiện thị:

```
Epoch 12/100
Train Loss: 0.214
Val Loss:   0.238
Train Acc:  91.4%
Val Acc:    89.7%
LR:         0.0001
```

### Kiến trúc Monitoring

```
                 TRAINING JOB
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
     Metrics         Logs       System Stats
        │             │             │
        └─────────────┼─────────────┘
                      ↓
                 Monitoring
                      │
              ┌───────┴───────┐
              ↓               ↓
          Dashboard          Alert
              │               │
              ↓               ↓
          Human        Auto Recovery
                              │
                              ↓
                         Checkpoint
                              │
                              ↓
                            Resume
```

#### Alterting

Production không thể yêu cầu con người ngồi nhìn dashboard 24/7.

phải có __alert__:

```
Validation loss ↑↑
       ↓
     Alert

GPU memory > threshold
       ↓
     Alert

Training process stopped
       ↓
     Alert
       ↓
  Auto recovery
```

> Real-time monitoring không phải là một biểu đồ đẹp để nhìn loss. Nó là observability layer giúp biết training đang chạy thế nào, model có đang học đúng không, infrastructure có khỏe không và hệ thống có cần can thiệp hay tự recovery hay không.


## 4. Ghi log

Log là lịch sử của quá trình training, dùng để phân tích sau này.

```
logs/
├── training.log
├── metrics.csv
└── config.yaml
```

Ví dụ:

```
epoch,train_loss,val_loss,train_acc,val_acc,lr
1,0.82,0.79,71.2,73.1,0.001
2,0.61,0.58,78.4,80.2,0.001
3,0.45,0.47,84.1,83.7,0.0005
```

Phân biệt:

- __Log__ → ghi lại những gì đã xảy ra.
- __Monitoring__ → quan sát những gì đang xảy ra.
- __Checkpoint__ → lưu trạng thái để có thể tiếp tục.

Trong production, log là cơ chế ghi lại trạng thái, sự kiện và hành vi của training/inference system để có thể quan sát, debug, reproduce và audit.

| Nhóm               | Ghi gì?                            | Mục đích     |
| ------------------ | ---------------------------------- | ------------ |
| **Training log**   | loss, accuracy, epoch, LR          | Theo dõi học |
| **Experiment log** | config, dataset, model version     | Reproduce    |
| **System log**     | GPU, memory, runtime, error        | Debug        |
| **Production log** | latency, prediction, errors, drift | Monitoring   |

### Experiment Log

Không chỉ ghi: `loss = 0.2` mà phải biết loss 0.2 đến từ experiment nào. Ví dụ:

```
experiment/
├── config.yaml
├── metrics.csv
├── model.pt
└── metadata.json
```

`config.yaml`:

```YAML
model: resnet18
optimizer: adam
learning_rate: 0.001
batch_size: 64
epochs: 100
dataset_version: v3
```

Tư duy: `Result=f(Code,Data,Config,Environment)`

Note chút:

```
LOG
↓
"What happened?"

METRIC
↓
"How well is the model doing?"

CHECKPOINT
↓
"What state can I resume from?"

---

Epoch 50
│
├── Log
│   └── epoch=50, time=...
│
├── Metrics
│   ├── loss=0.21
│   └── accuracy=0.92
│
└── Checkpoint
    └── model + optimizer + scheduler
```

## 5. Control training loop automation

Training loop nên tự động xử lý toàn bộ lifecycle:

```
Start
  ↓
Load Config
  ↓
Create Model
  ↓
Create Optimizer
  ↓
Check Checkpoint
  ├── Có → Resume
  └── Không → Train từ đầu
  ↓
Training
  ├── Log metrics
  ├── Monitor
  ├── Save latest checkpoint
  └── Save best checkpoint
  ↓
Validation
  ↓
Early Stopping / Scheduler
  ↓
Next Epoch
```

Mục tiêu cuối cùng:

```
python scripts/train.py
```

và hệ thống tự: `train → monitor → log → checkpoint → resume → finish`

Đây là bước chuyển từ Notebook-based training sang reproducible automated training pipeline.

### Các lựa chọn để train model nếu không dùng từ Jupyter local sang cloud compute.

| Nền tảng                                                                      | Chạy khi tắt máy                  | GPU | Phù hợp                         |
| ----------------------------------------------------------------------------- | --------------------------------- | --- | ------------------------------- |
| **[Lightning AI](https://lightning.ai/?utm_source=chatgpt.com)**              | ✅                                 | ✅   | Học + project dài ngày          |
| **[RunPod](https://www.runpod.io/?utm_source=chatgpt.com)**                   | ✅                                 | ✅   | Train dài ngày, cần control cao |
| **[Kaggle](https://www.kaggle.com/?utm_source=chatgpt.com)**                  | ⚠️ Có giới hạn session            | ✅   | Experiment, dataset nhỏ/vừa     |
| **[Google Colab](https://colab.research.google.com/?utm_source=chatgpt.com)** | ⚠️ Không nên dùng cho job lâu ngày | ✅   | Notebook/experiment nhanh       |

- Lightning Studio giống một laptop trên cloud: có terminal, VS Code/JupyterLab, GPU, persistent storage và environment.
- RunPod phù hợp hơn khi bạn muốn kiểm soát GPU/container/server nhiều hơn. hỗ trợ persistent storage, nhiều loại GPU và quản lý instance bằng CLI/API; rất hợp với training dài ngày và automation.
- Kaggle rất tiện để học và experiment vì có GPU miễn phí, nhưng không nên coi nó là server để train nhiều ngày liên tục. Kaggle có quota GPU theo tuần và session/resource constraints
- Google Colab rất tốt cho notebook-based experimentation, nhưng không nên thiết kế pipeline 10 ngày phụ thuộc vào một Colab session.