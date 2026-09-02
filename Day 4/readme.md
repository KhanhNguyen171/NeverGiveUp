# Fine-Tune Models

__Fine-tuning__ là quá trình lấy một __pre-trained model__ đã học trên tập dữ liệu lớn và tiếp tục cập nhật một phần hoặc toàn bộ trọng số trên __target dataset__ để thích nghi với nhiệm vụ mới. Đây là một kỹ thuật quan trọng của [Transfer Learning]((https://arxiv.org/pdf/1801.06146)).

Mục tiêu là để điều chỉnh các đặc trưng đã học được của mô hình được huấn luyện trước cho một nhiệm vụ mới, có liên quan, dẫn đến hiệu suất tốt hơn với ít dữ liệu hơn và thời gian huấn luyện nhanh hơn so với việc huấn luyện một mô hình từ đầu.

```mermaid
flowchart LR
    A["Pre-trained Model<br/>Source Dataset"] --> B["Modify Model<br/>Task-specific Head"]
    B --> C["Freeze Layers<br/>Optional"]
    C --> D["Fine-tune<br/>Low Learning Rate"]
    D --> E["Unfreeze More Layers<br/>Optional"]
    E --> F["Evaluate<br/>Validation/Test"]
    F --> G["Hyperparameter Tuning"]
```

| Câu hỏi    | Giải thích                                                                                                                                                         |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **WHAT?**  | Fine-tuning = **tiếp tục huấn luyện pre-trained model** trên dữ liệu của task mới để điều chỉnh representation đã học.                                                     |
| **WHY?**   | **Tận dụng knowledge/features đã học**, giảm dữ liệu cần thiết, thời gian huấn luyện vì mô hình đã được huấn luyện một phần từ trước nên quá trình hội tụ khi tinh chỉnh xảy ra nhanh hơn và thường cải thiện khả năng tổng quát và độ chính xác cao hơn so với train from scratch. ([arXiv][1])        |
| **WHERE?** | Dùng trong **Transfer Learning**, phổ biến ở Computer Vision, NLP và các mô hình foundation/pre-trained model. ([Journal of Machine Learning Research][2])                 |
| **WHEN?**  | Khi **target dataset nhỏ**, tài nguyên hạn chế hoặc đã có pre-trained model trên domain/task liên quan.                                                                    |
| **WHICH?** | Chọn model có **pre-training data/task càng gần target task càng tốt**. Mức độ tương đồng giữa source và target ảnh hưởng trực tiếp đến hiệu quả fine-tuning. ([arXiv][3]) |
| **HOW?**   | **① Chọn pretrained model → ② thay task-specific head → ③ freeze một số layer → ④ train với learning rate thấp → ⑤ unfreeze dần nếu cần → ⑥ evaluate/tune.**               |

[1]: https://arxiv.org/abs/1801.06146?utm_source=chatgpt.com "Universal Language Model Fine-tuning for Text Classification"
[2]: https://jmlr.org/beta/papers/v21/20-074.html?utm_source=chatgpt.com "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer"
[3]: https://arxiv.org/abs/1903.05987?utm_source=chatgpt.com "To Tune or Not to Tune? Adapting Pretrained Representations to Diverse Tasks"

> Pre-training học representation tổng quát → Fine-tuning điều chỉnh representation đó cho target task.

Không nhất thiết phải freeze layer. Có hai cách phổ biến:
- __Feature Extraction__: freeze toàn bộ backbone, chỉ train classifier/head.
- __Fine-tuning__: mở một phần hoặc toàn bộ backbone và cập nhật weights với __learning rate nhỏ.__ Nghiên cứu cho thấy lựa chọn giữa hai cách phụ thuộc đáng kể vào độ tương đồng giữa __pre-training task__ và __target task.__

## Freeze Layer

Freeze layer = đóng băng layer, nghĩa là không cập nhật trọng số (weights) và bias của layer đó trong quá trình training. Tức là model vẫn forward qua layer đó và tạo feature, nhưng optimizer không thay đổi parameters của layer.

Trong Fine-Tune

```mermaid
flowchart LR
    A["Input"] --> B["Early Layers<br/>🔒 Frozen"]
    B --> C["Middle Layers<br/>🔒 Frozen"]
    C --> D["Later Layers<br/>🔓 Trainable"]
    D --> E["New Classification Head<br/>🔓 Trainable"]
```

Ví dụ trong CNN:

| Layer      | Trạng thái    | Vai trò                                 |
| ---------- | ------------- | --------------------------------------- |
| Conv 1–3   | 🔒 **Freeze** | Giữ feature tổng quát như edge, texture |
| Conv 4–5   | 🔓 **Train**  | Học feature phù hợp dataset mới         |
| Classifier | 🔓 **Train**  | Học mapping sang class mới              |

Ta dùng Freeze vì khi dataset nhỏ thì mô hình dễ bị overfitting nếu cập nhật toàn bộ model. Việc đóng băng các layer đầu giúp:
- giữ lại feature đã học tốt từ pretrained model;
- giảm số trainable parameters;
- giảm computation;
- hạn chế catastrophic forgetting.

## Hugging Face API

__Hugging Face API__ chủ yếu cung cấp model và inference; fine-tuning model lớn thường được thực hiện bằng `Transformers + PEFT/LoRA + TRL` trên GPU, sau đó upload model/adapter đã fine-tune trở lại Hub.

## Lựa chọn Model phù hợp

### Theo quy mô

| Quy mô                           | Đặc điểm                          | Cách fine-tune nên cân nhắc                           |
| -------------------------------- | --------------------------------- | ----------------------------------------------------- |
| **< 1B**                         | Nhẹ hơn, dễ thử nghiệm            | Full FT hoặc LoRA                                     |
| **1B–7B**                        | Bắt đầu tốn nhiều VRAM            | LoRA là lựa chọn thực tế                              |
| **7B–13B**                       | Full FT thường rất tốn tài nguyên | LoRA / QLoRA                                          |
| **13B+**                         | Chi phí full FT rất lớn           | PEFT + LoRA/QLoRA + quantization/distributed training |
| **Vision / Diffusion model lớn** | Cấu trúc khác LLM                 | LoRA/PEFT hoặc fine-tune component cần thiết          |

> **Lưu ý:** Không nên chọn phương pháp chỉ dựa trên số B parameters. Dataset size, task, GPU memory và architecture cũng quyết định phương pháp phù hợp.

PEFT hỗ trợ nhiều phương pháp như **LoRA, AdaLoRA, IA3, prompt tuning, prefix tuning,...**; LoRA là điểm bắt đầu phổ biến cho large models.

---

### Phương pháp Fine-tuning

| Method                   | Base model             | Parameters train | Khi dùng                                          |
| ------------------------ | ---------------------- | ---------------- | ------------------------------------------------- |
| **Full Fine-tuning**     | Toàn bộ model          | 100%             | Model nhỏ / đủ GPU                                |
| **LoRA**                 | Freeze base + adapter  | Rất ít           | Lựa chọn mặc định cho LLM lớn                     |
| **QLoRA**                | Quantized base + LoRA  | Rất ít           | Khi VRAM hạn chế                                  |
| **AdaLoRA**              | Base + adaptive LoRA   | Ít               | Muốn phân bổ parameter budget linh hoạt           |
| **IA3**                  | Base + learned vectors | Rất ít           | PEFT nhẹ, task phù hợp                            |
| **Prompt/Prefix Tuning** | Base frozen            | Rất ít           | Điều chỉnh behavior bằng learned prompts/prefixes |

LoRA giữ nguyên pretrained weights và thêm các ma trận low-rank trainable; QLoRA-style training có thể áp dụng LoRA trên các linear layers của model.

---

### Theo model

| Model / Family             | Task phổ biến                 | Fine-tuning                  |
| -------------------------- | ----------------------------- | ---------------------------- |
| **BERT / RoBERTa**         | Classification, NER           | Full FT hoặc LoRA            |
| **T5 / FLAN-T5**           | Seq2Seq, generation           | Full FT hoặc LoRA            |
| **Llama / Qwen / Mistral** | Chat, instruction, generation | **LoRA / QLoRA + SFT**       |
| **Vision Transformer**     | Image classification          | Full FT hoặc LoRA            |
| **CLIP**                   | Vision-Language               | LoRA / component-specific FT |
| **Stable Diffusion**       | Image generation              | **LoRA**                     |

Không nên hiểu rằng mỗi model **bắt buộc** dùng một method duy nhất; Hugging Face PEFT hỗ trợ nhiều task/model architecture và method khác nhau.

## Pipeline Finetune theo Hugging face

```mermaid
flowchart LR
    A["Hugging Face Hub"] --> B["Load Pre-trained Model"]
    C["Dataset"] --> D["Prepare / Tokenize"]
    B --> E["PEFT / LoRA"]
    D --> F["Trainer / SFTTrainer"]
    E --> F
    F --> G["Train"]
    G --> H["Evaluate"]
    H --> I["Save Adapter / Model"]
    I --> J["Push to Hub"]
```

## Quy trình mẫu

### Step 1 — Load model từ Hub

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "Qwen/Qwen3-0.6B"

tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto"
)
```

Hugging Face `Transformers` cung cấp API `from_pretrained()` để load pretrained model từ Hub.

---

### Step 2 — Load và chuẩn bị Dataset

```python
from datasets import load_dataset

dataset = load_dataset(
    "your_dataset",
    split="train"
)
```

Với instruction/chat model, dataset thường được chuẩn hóa thành dạng **prompt-completion** hoặc **conversational messages** trước khi SFT.

---

### Step 3 — Chọn PEFT method

Ví dụ **LoRA**:

```python
from peft import LoraConfig

peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules="all-linear",
    task_type="CAUSAL_LM"
)
```

Base model được freeze; chỉ LoRA parameters được cập nhật.

---

### Step 4 — SFT với TRL

```python
from trl import SFTConfig, SFTTrainer

training_args = SFTConfig(
    output_dir="./output",
    num_train_epochs=3,
    learning_rate=1e-4
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    peft_config=peft_config
)

trainer.train()
```

`SFTTrainer` của TRL được thiết kế cho **Supervised Fine-Tuning** các language models và tích hợp với PEFT.

---

### Step 5 — Save / Push lên Hugging Face Hub

```python
trainer.save_model("./adapter")

trainer.push_to_hub()
```

Với PEFT, có thể lưu và chia sẻ **adapter** thay vì phải lưu toàn bộ base model. Khi sử dụng adapter từ Hub, cần base model tương ứng.