# Efficient On-Device Agents via Adaptive Context Management

**Authors:** Sanidhya Vijayvargiya, Rahul Lokesh

**arXiv:** 2511.03728

**Primary area:** Computer Science — Artificial Intelligence

**Version:** v1, 24 September 2025 ([arXiv][1])

---

# Tóm tắt

## Vấn đề

AI agent chạy trực tiếp trên thiết bị có lợi thế về **privacy, latency và personalization**, nhưng bị giới hạn bởi bộ nhớ và khả năng tính toán của thiết bị. Khi agent tương tác nhiều vòng với người dùng, tool và cloud agent, context tăng nhanh.

Có ba nguồn gây **context bloat** chính:

1. Lịch sử hội thoại ngày càng dài.
2. Tool schema quá verbose.
3. Số lượng tool tăng làm system prompt phình to.

Điều này không chỉ làm tăng memory/KV-cache mà còn có thể làm giảm reliability của agent. Tác giả nhấn mạnh rằng ngay cả context khoảng **5–10K tokens** cũng có thể trở thành vấn đề đối với on-device agent. ([arXiv][1])

## Ý tưởng chính

Paper không cố gắng đơn giản là tạo một context window lớn hơn.

Thay vào đó, tác giả đặt câu hỏi:

> **Có thể giữ lại thông tin quan trọng của agent nhưng loại bỏ phần context không cần thiết hay không?**

Câu trả lời là có, bằng cách quản lý context ở **semantic level**:

```text
Raw Conversation
       │
       ▼
State-Tracker
       │
       ▼
Context State Object (CSO)
       │
       ▼
Executor
```

Đồng thời, tool được xử lý theo:

```text
Lightweight Tool Bank
        │
        ▼
   Tool Selection
        │
        ▼
Full Tool Schema
        │
        ▼
   Tool Execution
```

## Phương pháp

Framework gồm ba thành phần:

* **Dynamic Memory:** dùng hai LoRA adapter để biến lịch sử hội thoại thành CSO.
* **Token-efficient Schema:** rút gọn tool schema.
* **JIT Schema Passing:** chỉ truyền full schema sau khi tool được chọn. ([arXiv][1])

## Kết quả

Trên 406 task với 19 tool chưa xuất hiện trong training:

* Initial context giảm từ khoảng **3,200 → 400 tokens**.
* Memory-efficient model giảm tốc độ context growth khoảng **10×** trong multi-tool.
* Trong cloud delegation, context growth giảm **hơn 20×**.
* Combined model đạt **F1 cao nhất tổng thể** trong tool calling. ([arXiv][1])

## Đóng góp

Điểm quan trọng nhất của paper không phải chỉ là "compress context", mà là:

> **Thiết kế context như một trạng thái có cấu trúc, được học để giữ lại thông tin có giá trị cho agent, thay vì lưu toàn bộ lịch sử hội thoại.**

---

# Chương 1. Giới thiệu và vấn đề nghiên cứu

## 1.1. Bối cảnh

AI agent hiện đại thường được xây dựng trên LLM và có khả năng:

* hội thoại;
* gọi tool;
* tương tác với môi trường;
* thực hiện multi-step task;
* định tuyến task sang model/cloud agent.

On-device agent đưa các khả năng này xuống smartphone hoặc edge device để đạt:

* latency thấp;
* privacy cao;
* personalization tốt;
* khả năng truy cập trực tiếp dữ liệu và ứng dụng trên thiết bị.

Tuy nhiên, agentic workflow có đặc điểm khác chatbot thông thường:

```text
User
 ↓
Agent
 ↓
Tool
 ↓
Environment
 ↓
Agent
 ↓
Tool
 ↓
...
```

Mỗi vòng lặp tạo thêm tokens vào context.

Tác giả xác định hai vấn đề trực tiếp của context dài:

1. KV cache tăng theo context length.
2. Reliability giảm khi context trở nên dài và nhiễu. ([arXiv][1])

Có thể mô hình hóa context tại timestep $t$ đơn giản là:

$$
C_t = C_{t-1} \oplus m_t
$$

trong đó:

* $C_t$: context tại thời điểm $t$;
* $m_t$: message/observation mới;
* $\oplus$: phép nối context.

Nếu mỗi lượt tạo trung bình $\Delta$ tokens:

$$
|C_t| \approx |C_0| + t\Delta
$$

Do đó context tăng gần tuyến tính theo số lượt tương tác.

Vấn đề là **on-device memory budget rất nhỏ**, nên tăng context trở thành bottleneck thực tế.

---

## 1.2. Vấn đề nghiên cứu

Paper tập trung vào một agent có thể thực hiện ba loại hành động:

```text
                    ┌── Direct Response
User → On-device ───┼── Local Tool Execution
                    └── Cloud Delegation
```

3B SLM đóng vai trò **orchestrator**.

Input của agent có thể biểu diễn:

$$
x_t = (u_t, C_t, T_t)
$$

trong đó:

* $u_t$: user query;
* $C_t$: conversational state;
* $T_t$: thông tin về tools.

Agent tạo action:

$$
a_t = f_\theta(x_t)
$$

với:

$$
a_t \in
\{
\text{response},
\text{local tool call},
\text{cloud delegation}
\}
$$

Nhưng $C_t$ và $T_t$ ngày càng lớn.

Do đó bài toán nghiên cứu có thể diễn đạt là:

> Làm thế nào duy trì khả năng agentic của SLM trong khi giảm lượng context cần thiết cho inference trên thiết bị?

---

## 1.3. Hạn chế của phương pháp trước

Paper phân loại các hướng trước thành nhiều nhóm.

| Nhóm                           | Ưu điểm                       | Hạn chế đối với on-device                      |
| ------------------------------ | ----------------------------- | ---------------------------------------------- |
| Inter-session memory           | Duy trì memory lâu dài        | Có thể mất fine-grained information            |
| Recursive summarization        | Giảm context                  | Có nguy cơ mất thông tin                       |
| KV compression                 | Giảm memory thấp tầng         | Opaque, heuristic                              |
| Long-context modeling          | Hỗ trợ context rất dài        | Không phù hợp với budget nhỏ                   |
| Retrieval-based tool selection | Giảm số tool schema           | Retriever có thể chọn sai hoặc không chọn tool |
| Full tool schemas              | Agent biết toàn bộ capability | Context rất lớn                                |

Đặc biệt, các phương pháp KV compression thường dựa vào các heuristic như attention magnitude hoặc reconstruction error. Điều này có thể loại bỏ thông tin hiện tại chưa quan trọng nhưng sẽ cần ở một timestep xa hơn. ([arXiv][1])

---

## 1.4. Khoảng trống nghiên cứu

Research gap của paper khá cụ thể:

> **Các phương pháp hiện tại chưa giải quyết đồng thời context growth từ conversational history và tool-schema overhead trong điều kiện memory budget rất hạn chế của on-device agent.**

Có thể biểu diễn:

```text
             Context Bloat
                  │
        ┌─────────┴─────────┐
        │                   │
 Conversation History   Tool Schemas
        │                   │
        ▼                   ▼
   Memory Growth       Prompt Growth
        │                   │
        └─────────┬─────────┘
                  ▼
        On-device Bottleneck
```

Paper vì vậy không giải quyết một nguồn context bloat duy nhất mà thiết kế **một framework tổng thể**.

---

## 1.5. Mục tiêu nghiên cứu

Mục tiêu là xây dựng một on-device agent:

* giữ được khả năng multi-turn;
* sử dụng nhiều tool;
* có thể delegate sang cloud;
* giảm context growth;
* vẫn duy trì task performance;
* phù hợp với inference trên thiết bị.

---

## 1.6. Câu hỏi nghiên cứu

Từ thiết kế và thực nghiệm của paper, có thể đặt các câu hỏi kiểm chứng:

1. Có thể thay thế raw conversation history bằng một representation nhỏ hơn mà vẫn giữ task performance không?
2. Token-efficient schema có giảm initial context không?
3. JIT schema passing có mở rộng số lượng tool mà agent có thể biết không?
4. Dual-adapter memory có làm giảm context growth không?
5. Kết hợp memory và tool optimization có giữ hoặc cải thiện tool-calling performance không?

---

## 1.7. Đóng góp chính

Paper nêu ba đóng góp chính:

### Contribution 1 — On-device agent architecture

3B SLM đóng vai trò orchestrator giữa:

```text
User
 │
 ▼
3B SLM
 ├── Direct response
 ├── Local tools
 └── Cloud agent
```

### Contribution 2 — Dual-adapter memory

Hai LoRA adapter:

$$
\text{LoRA}_{Exec}
$$

và

$$
\text{LoRA}_{Mem}
$$

được sử dụng cho hai nhiệm vụ khác nhau.

Executor thực hiện task; State-Tracker cập nhật memory.

### Contribution 3 — Efficient tool management

Kết hợp:

$$
\text{Compact Schema}
+
\text{JIT Schema Passing}
$$

để giảm tool-related context overhead. ([arXiv][1])

---

# Chương 2. Cơ sở lý thuyết và tổng quan

## 2.1. Context trong LLM agent

Trong LLM agent, context không chỉ là hội thoại.

Nó có thể gồm:

```text
System Instructions
+
Conversation History
+
Tool Schemas
+
Tool Calls
+
Tool Outputs
+
Cloud Responses
```

Vì vậy:

$$
C_t =
S \oplus H_t \oplus T_t \oplus O_t
$$

với:

* $S$: system instructions;
* $H_t$: history;
* $T_t$: tool information;
* $O_t$: observations/tool outputs.

Khi $|C_t|$ tăng, chi phí inference và memory tăng.

---

## 2.2. KV Cache

Transformer sử dụng Key-Value cache để tránh tính lại các token cũ.

Một cách khái quát:

$$
\mathrm{KVCache}_t
=
\mathrm{KVCache}_{t-1}
\oplus
(K_t,V_t)
$$

Do đó memory requirement tăng theo số token.

Paper nhấn mạnh rằng context window dài tạo ra **linear KV-cache growth**, đặc biệt nghiêm trọng trên thiết bị hạn chế tài nguyên. ([arXiv][1])

---

## 2.3. LoRA

Paper sử dụng LoRA để fine-tune model 3B hiệu quả hơn.

Ý tưởng cơ bản của LoRA là thay vì cập nhật toàn bộ matrix $W$, biểu diễn update dưới dạng low-rank:

$$
W' = W + \Delta W
$$

với:

$$
\Delta W = BA
$$

trong đó $A$ và $B$ có rank nhỏ.

Điều này cho phép tạo adapter chuyên biệt mà không phải thay đổi toàn bộ base model.

Paper tận dụng đặc điểm modular này để xây dựng hai adapter chuyên biệt. ([arXiv][1])

---

## 2.4. Context State Object

Thay vì:

```text
User message 1
Assistant message 1
Tool output 1
User message 2
...
```

paper sử dụng một state log có cấu trúc:

```text
user goal: ...
completed steps: ...
tool errors: ...
agent limitation: ...
important constraint: ...
```

Điểm quan trọng:

> CSO không đơn thuần là một summary.

Nó là **task-oriented structured memory**.

State-Tracker được huấn luyện để biết thông tin nào cần giữ lại.

---

## 2.5. Tool Schema

Một tool thường được mô tả bằng schema chứa:

```text
name
description
parameters
...
```

Nếu toàn bộ schema của hàng chục tool được đưa vào system prompt:

$$
|T| = \sum_{i=1}^{N}|T_i|
$$

thì context tăng theo số lượng tool.

Paper rút gọn representation xuống những field cần thiết cho invocation và loại bỏ formatting dư thừa. Kết quả trung bình giảm khoảng **40% tokens/tool**. ([arXiv][1])

---

## 2.6. Just-in-Time Schema Passing

Thay vì:

```text
All tools
 ↓
All full schemas
 ↓
LLM
```

paper sử dụng:

```text
All tool names + descriptions
              ↓
       Tool Selection
              ↓
       Selected Tool
              ↓
       Full Schema
              ↓
       Tool Arguments
              ↓
        Execution
```

Điểm quan trọng là agent **vẫn biết capability của toàn bộ toolset**, nhưng không phải đọc full schema của tất cả tools ngay từ đầu. ([arXiv][1])

---

## 2.7. Các phương pháp liên quan

Có thể tổ chức landscape thành:

```text
Context Management
│
├── Inter-session memory
│   ├── Recursive summarization
│   └── MemGPT
│
├── Intra-session memory
│   └── MEM1
│
├── Long-context modeling
│   ├── RAG
│   └── Sparse Attention
│
├── KV compression
│
└── Semantic context management
    └── CSO
```

Paper đặt CSO vào hướng **semantic-level context management**, thay vì compression ở low-level KV representation. ([arXiv][1])

---

## 2.8. Khoảng trống → ý tưởng

Logic của paper:

```text
Long Context
     ↓
Memory + Reliability Problem
     ↓
Raw history is wasteful
     ↓
Need semantic compression
     ↓
Structured Context State Object
```

Đồng thời:

```text
Many Tool Schemas
       ↓
Prompt Bloat
       ↓
Need capability awareness
without full schema exposure
       ↓
JIT Schema Passing
```

Hai ý tưởng này sau đó được kết hợp thành một framework.

---

# Chương 3. Phương pháp nghiên cứu

# 3.1. Tổng quan framework

Kiến trúc tổng thể:

```text
                         ┌──────────────────┐
                         │      User        │
                         └────────┬─────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │   On-device 3B SLM     │
                     │      Executor          │
                     └───────┬───────┬────────┘
                             │       │
                ┌────────────┘       └────────────┐
                ▼                                 ▼
         Local Tool Execution              Cloud Delegation
                │                                 │
                └──────────────┬──────────────────┘
                               ▼
                       Interaction Result
                               │
                               ▼
                     ┌──────────────────┐
                     │ State-Tracker    │
                     │    LoRA_Mem      │
                     └────────┬─────────┘
                              │
                              ▼
                         CSO Update
                              │
                              ▼
                    CSO_t = CSO_{t-1} ⊕ Δ_t
```

Framework gồm hai subsystem chính:

1. **Dynamic Memory**
2. **Tool Schema Management**

---

# 3.2. Problem Formulation

Gọi:

* $u_t$: user input ở timestep $t$;
* $C_{t-1}$: Context State Object trước đó;
* $\theta_E$: tham số Executor;
* $\theta_M$: tham số State-Tracker.

Executor tạo action:

$$
a_t =
f_{\theta_E}(u_t,C_{t-1})
$$

Sau khi có assistant response/tool observation $o_t$, State-Tracker tạo delta:

$$
\Delta_t =
g_{\theta_M}(u_t,a_t,o_t,C_{t-1})
$$

CSO mới:

$$
C_t = C_{t-1} \oplus \Delta_t
$$

Đây là phương trình trung tâm của memory architecture.

Ý nghĩa:

> Không lưu lại toàn bộ $u_t,a_t,o_t$ vào context. Chỉ lưu phần thông tin mà State-Tracker cho rằng cần thiết cho các timestep tương lai.

---

# 3.3. Dynamic Memory — Dual Adapter

Paper sử dụng hai adapter.

## Executor — $\mathrm{LoRA}_{Exec}$

Executor là adapter chính.

Input:

$$
(C_{t-1},u_t)
$$

Output:

$$
a_t = f_{\theta_E}(C_{t-1},u_t)
$$

Nó thực hiện:

* direct response;
* tool call;
* cloud delegation.

---

## State-Tracker — $\mathrm{LoRA}_{Mem}$

State-Tracker có nhiệm vụ hoàn toàn khác.

Input:

$$
(C_{t-1},u_t,a_t,o_t)
$$

Output:

$$
\Delta_t
$$

Sau đó:

$$
C_t=C_{t-1}\oplus\Delta_t
$$

State-Tracker có **119M parameters** và được thiết kế chuyên biệt cho memory update. ([arXiv][1])

---

# 3.4. Memory Update Cycle

Một interaction cycle:

### Step 1 — Execute

Executor đọc:

```text
CSO_{t-1}
+
User Query
```

và thực hiện task.

### Step 2 — Track

State-Tracker đọc:

```text
CSO_{t-1}
+
Latest Interaction
```

và sinh:

```text
Δ_t
```

### Step 3 — Append

$$
CSO_t = CSO_{t-1}\oplus\Delta_t
$$

Do chỉ append delta nhỏ, context growth được giảm đáng kể. ([arXiv][1])

---

# 3.5. Tại sao dùng Append-only Log?

Một thiết kế quan trọng của paper là **append-only**.

Không rewrite toàn bộ CSO sau mỗi turn.

Thay vào đó:

```text
CSO_0
 ↓ append Δ_1
CSO_1
 ↓ append Δ_2
CSO_2
 ↓ append Δ_3
CSO_3
```

Điều này có lợi cho KV cache.

Phần context cũ không thay đổi nên KV cache có thể được giữ lại.

Paper cho biết implementation của họ duy trì KV cache riêng cho hai adapter; vì CSO chỉ append nên phần static context được cache lại, chỉ delta và query mới cần xử lý. ([arXiv][1])

Đây là một điểm kiến trúc rất quan trọng:

> **Semantic compression được thiết kế đồng thời với inference optimization.**

---

# 3.6. CSO không phải Summary thông thường

Paper cố tình không sử dụng summary tự nhiên dạng paragraph.

Ví dụ representation có thể mang tính:

```text
user goal: enable power saving
completed steps: wifi disabled
agent refusals: cannot predict stock prices
tool errors: ...
```

Mục tiêu là giữ:

* user goal;
* constraints;
* completed steps;
* unresolved problems;
* tool errors;
* agent limitations;
* environment feedback.

State-Tracker được huấn luyện để tạo những update này. ([arXiv][1])

---

# 3.7. Token-efficient Tool Schema

Schema truyền thống có thể chứa nhiều formatting không cần thiết.

Paper chỉ giữ các thành phần thiết yếu:

```text
name
description
parameters
```

và loại bỏ whitespace/fields không cần thiết.

Kết quả:

$$
\text{Token Cost}_{compact}
\approx
0.6
\times
\text{Token Cost}_{standard}
$$

theo mức giảm trung bình khoảng 40% mà paper báo cáo. ([arXiv][1])

---

# 3.8. JIT Schema Passing

Đây là cơ chế thứ hai.

## Stage 1 — Selection

Agent nhận:

```text
Tool A — description
Tool B — description
Tool C — description
...
Tool N — description
```

Không nhận full schema.

Agent chọn:

$$
t^* =
\arg\max_{t\in T}
P(t\mid u,C)
$$

Đây là cách diễn giải toán học cho quá trình lựa chọn tool; paper mô tả quy trình nhưng không đưa phương trình argmax này như một công thức chính thức.

## Stage 2 — Execution

Sau khi chọn $t^*$:

```text
Selected Tool
      ↓
Full Compact Schema
      ↓
Generate Arguments
      ↓
Execute
```

Do đó:

$$
\text{Initial Context}
\ll
\text{Full Tool Context}
$$

nhưng agent vẫn có capability awareness ở mức tên + description. ([arXiv][1])

---

# 3.9. Data Generation

Paper xây dựng dataset bằng cách:

```text
100 base tools
       ↓
50 variants / tool
       ↓
5,000 unique tools
```

Bốn loại task:

1. Multi-tool.
2. Cloud delegation.
3. Mixed on-device/cloud.
4. Conversational queries. ([arXiv][1])

Trajectory được tạo bằng Gemini 2.0 Flash.

Quá trình curation:

```text
Generated Trajectory
        ↓
Ground-truth validation
        ↓
LLM-as-Judge
        ↓
Curated trajectory
```

([arXiv][1])

---

# 3.10. Training

Base model:

> **xLAM 2 3B**

Fine-tuning sử dụng LoRA. Mỗi training example chứa khoảng 10–14 tools, gồm correct tool, cloud tool và distractor tools. ([arXiv][1])

### State-Tracker

Teacher:

> Gemini 2.0 Flash

Teacher tạo ground-truth CSO update.

Sau đó:

$$
(\text{turn},\Delta_t)
\rightarrow
\mathrm{LoRA}_{Mem}
$$

Đây là **hard distillation**. ([arXiv][1])

### Executor

Executor được train để sử dụng ground-truth CSO:

$$
(C_t,u_t)
\rightarrow
\text{response/tool call}
$$

Hai adapter do đó được **co-adapt** với cùng representation. ([arXiv][1])

---

# 3.11. Experimental Setup

Evaluation gồm:

* **406 tasks**
* **19 unseen tools**
* simulated user;
* long trajectories;
* ambiguity;
* multi-step intents.

19 tools chưa xuất hiện trong training được dùng để kiểm tra generalization thay vì memorization tool signature. ([arXiv][1])

Năm variant:

| Model            | Ý nghĩa                    |
| ---------------- | -------------------------- |
| xLAM-2 3B        | Reference                  |
| Baseline FT      | Fine-tuned + full history  |
| Tool-Efficient   | Tool optimization          |
| Memory-Efficient | CSO memory                 |
| Combined         | Memory + Tool optimization |

([arXiv][1])

---

# 3.12. Evaluation Metrics

### Precision

$$
P=
\frac{\text{Correct Tool Calls}}
{\text{All Tool Calls}}
$$

Đo mức độ agent tránh gọi tool sai.

### Recall

$$
R=
\frac{\text{Correct Tool Calls}}
{\text{Required Tool Calls}}
$$

Đo agent có thực hiện đủ tool cần thiết hay không.

### F1

$$
F_1 =
\frac{2PR}{P+R}
$$

Đây là metric cân bằng precision và recall.

Ngoài ra paper sử dụng **LLM-as-Judge**, chấm chất lượng trajectory từ 1 đến 5, và theo dõi input context length ở mỗi assistant turn. Kết quả được trung bình trên 3 runs. ([arXiv][1])

---

# Chương 4. Kết quả và thảo luận

# 4.1. Kết quả chính

Bảng kết quả chính:

| Model            | Cloud F1 | Multi-tool F1 | On-device + Cloud F1 | Conversation Q |
| ---------------- | -------: | ------------: | -------------------: | -------------: |
| xLAM-2 3B        |     0.41 |          0.87 |                 0.57 |           2.18 |
| Baseline FT      |     1.00 |          0.83 |                 0.88 |           2.87 |
| Tool-Efficient   |     0.93 |          0.86 |                 0.73 |           3.21 |
| Memory-Efficient |     1.00 |          0.87 |                 0.89 |           3.32 |
| **Combined**     | **0.99** |      **0.93** |             **0.94** |       **3.80** |

([arXiv][1])

Kết quả nổi bật:

> **Combined đạt F1 cao nhất trong các nhóm task tool-calling quan trọng.**

---

# 4.2. Initial Context

Đây là một trong những kết quả quan trọng nhất.

| Model            |           Initial context |
| ---------------- | ------------------------: |
| xLAM-2           |              3,200 tokens |
| Baseline         |              2,100 tokens |
| Memory-Efficient |              2,100 tokens |
| Tool-Efficient   |                400 tokens |
| Combined         | khoảng mức Tool-Efficient |

([arXiv][1])

Từ:

$$
3200 \rightarrow 400
$$

tức giảm khoảng:

$$
\frac{3200}{400}=8
$$

lần về initial tool-related context footprint.

Paper liên hệ điều này với khả năng hỗ trợ toolset lớn hơn trong cùng token budget và TTFT tốt hơn. ([arXiv][1])

---

# 4.3. Context Growth

Trong multi-tool:

```text
Baseline
    ↗
   ↗
  ↗
 ↗
→ ~5000 tokens

Memory-Efficient
────────────
      ──────
→ +100–200 tokens
```

Sau 25 turns:

* Baseline tăng lên khoảng 5,000 tokens.
* Memory-Efficient chỉ tăng khoảng 100–200 tokens.

Paper báo cáo khoảng **10× reduction** trong context accumulation. ([arXiv][1])

---

## Cloud Delegation

Đây là trường hợp quan trọng hơn.

Baseline:

$$
\sim10,000-12,000
\text{ tokens}
$$

Memory-Efficient:

$$
\sim500
\text{ tokens}
$$

Do đó context growth giảm **hơn 20×**. ([arXiv][1])

Lý do là cloud response thường verbose.

Nếu lưu raw response:

$$
C_t=C_{t-1}\oplus O_t^{cloud}
$$

thì $O_t^{cloud}$ có thể rất lớn.

CSO thay thế nó bằng:

$$
C_t=C_{t-1}\oplus\Delta_t
$$

với:

$$
|\Delta_t|\ll|O_t^{cloud}|
$$

Đây chính là cơ chế tạo ra lợi ích lớn nhất.

---

# 4.4. Ablation — Tool vs Memory

Có thể hiểu experimental design như:

```text
                 Full Framework
                      │
             ┌────────┴────────┐
             │                 │
          Memory              Tool
             │                 │
             ▼                 ▼
 Memory-Efficient       Tool-Efficient
             │                 │
             └────────┬────────┘
                      ▼
                   Combined
```

### Tool-Efficient

Ưu điểm:

* precision cao;
* context initial rất nhỏ.

Nhược điểm:

* recall thấp hơn;
* có thể khó pivot sang tool khác nếu lựa chọn đầu tiên sai.

### Memory-Efficient

Ưu điểm:

* recall cao;
* xử lý ambiguity tốt;
* error recovery tốt;
* context growth rất thấp.

### Combined

Kết hợp hai ưu điểm:

$$
\text{Combined}
=
\text{Memory Efficiency}
+
\text{Tool Efficiency}
$$

và đạt F1 cao nhất tổng thể. ([arXiv][1])

---

# 4.5. Tại sao CSO giúp agent tốt hơn?

Đây là phần Discussion quan trọng.

Paper quan sát failure mode:

```text
Tool call
   ↓
Error
   ↓
Long context
   ↓
Error bị "chìm"
   ↓
Agent gọi lại tool cũ
   ↓
Error loop
```

CSO biến:

```text
Tool error: invalid parameter
```

thành một entry nổi bật trong structured state.

Do đó:

```text
Tool Error
   ↓
State Tracker
   ↓
CSO: persistent error
   ↓
Executor sees error
   ↓
Change strategy
```

Tác giả liên hệ hiện tượng này với **attention dilution** trong long context và cho rằng structured CSO giúp Executor tập trung vào thông tin quan trọng hơn. Đây là cách diễn giải/hypothesis của tác giả, không phải một định luật được chứng minh trực tiếp bởi experiment. ([arXiv][1])

---

# 4.6. CSO học được gì?

Phân tích qualitative của paper cho thấy State-Tracker không chỉ học summarization.

Ba đặc tính được quan sát:

### 1. Task-oriented decomposition

Một user request phức tạp được phân tách thành:

```text
user goal
blocker
agent limitation
completed step
```

### 2. Adaptive logging

Turn đơn giản:

```text
small Δ_t
```

Cloud response verbose:

```text
larger Δ_t
```

Tức State-Tracker học cách thay đổi độ dài update theo information density.

### 3. Structured representation

Key-value format được cho là phù hợp với khả năng structured-data của xLAM-2. Tác giả đưa ra đây như một hypothesis/interpretation. ([arXiv][1])

---

# 4.7. Precision–Recall Trade-off

Paper phát hiện trade-off rõ:

```text
Tool-Efficient
    ↓
High Precision
    ↓
Lower Recall

Memory-Efficient
    ↓
Higher Flexibility
    ↓
Higher Recall
```

Tool-Efficient buộc agent thực hiện selection trước nên giảm tool call sai, nhưng nếu lựa chọn đầu tiên sai thì khó chuyển hướng.

Memory-Efficient giữ structured history nên có khả năng thử strategy khác tốt hơn. ([arXiv][1])

Combined tận dụng cả hai.

---

# 4.8. Những điều kết quả chưa chứng minh

Không nên diễn giải paper thành:

> "CSO luôn tốt hơn raw context."

Paper **chưa chứng minh điều này trong mọi domain**.

Các limitation được chính tác giả nêu:

1. Training chỉ một epoch và fixed data distribution.
2. Generalization sang open-domain task chưa được chứng minh.
3. State-Tracker phụ thuộc vào teacher distillation.
4. CSO policy có thể không phải global optimum.
5. Evaluation protocol là custom nên direct comparison với benchmark khác bị hạn chế. ([arXiv][1])

Đặc biệt:

> **19 unseen tools** chứng minh một mức generalization đối với novel APIs trong evaluation setup, nhưng không đồng nghĩa với generalization toàn diện sang open-domain agent tasks.

---

# Chương 5. Kết luận và hàm ý

# 5.1. Kết luận

Logic toàn bộ paper:

```text
On-device Agent
      ↓
Limited Memory
      ↓
Context Bloat
 ┌────┴─────┐
 │          │
History   Tool Schema
 │          │
 ▼          ▼
CSO        JIT
 │          │
 └────┬─────┘
      ▼
Context-efficient Agent
      ↓
Strong Task Performance
      +
Much Smaller Context
```

Paper cho thấy rằng không nhất thiết phải tăng context window để xây dựng agent có khả năng stateful.

Một hướng khác là:

> **làm cho context trở nên có cấu trúc và chỉ giữ thông tin cần thiết cho quyết định tương lai.**

---

# 5.2. Đóng góp khoa học

## Methodological contribution

Dual-adapter memory:

$$
\mathrm{LoRA}_{Exec}
+
\mathrm{LoRA}_{Mem}
$$

với CSO làm interface giữa memory và execution.

## System contribution

Kết hợp:

$$
\text{CSO}
+
\text{Compact Schema}
+
\text{JIT}
$$

thành một framework thống nhất cho on-device agent.

## Empirical contribution

Thực nghiệm cho thấy context có thể giảm rất mạnh mà vẫn giữ performance:

$$
\text{Context Reduction}
\not\Rightarrow
\text{Task Performance Collapse}
$$

Trong một số trường hợp performance còn tăng.

---

# 5.3. Hàm ý kỹ thuật

Hàm ý quan trọng nhất của paper là:

> **Context engineering có thể quan trọng không kém model scaling đối với on-device agents.**

Thay vì:

```text
Larger Model
+
Longer Context
```

có thể sử dụng:

```text
Smaller Model
+
Structured Memory
+
Selective Tool Context
```

Điều này đặc biệt phù hợp với edge/on-device deployment.

---

# 5.4. Hạn chế

Các limitation chính theo tác giả:

* training scope còn hạn chế;
* chỉ một epoch;
* fixed data distribution;
* phụ thuộc supervised distillation;
* teacher model ảnh hưởng chất lượng State-Tracker;
* custom evaluation;
* chưa chứng minh open-domain generalization. ([arXiv][1])

Ngoài ra, hệ thống CSO có overhead:

$$
\approx80\text{ MB}
$$

và khoảng:

$$
500\text{ ms/turn}
$$

cho memory update cycle trên Galaxy S25 CPU trong implementation được báo cáo. ([arXiv][1])

Vì vậy context compression **không miễn phí**.

---

# 5.5. Hướng nghiên cứu tiếp theo

Tác giả đề xuất đặc biệt:

### Reinforcement Learning

SFT hiện tại không hoàn toàn tối ưu cho adaptive decision making.

Do đó có thể nghiên cứu:

$$
\pi_\theta(a_t|C_t,u_t)
$$

với reward phản ánh:

* task success;
* context cost;
* tool efficiency;
* error recovery;
* latency.

Paper trực tiếp đề xuất RL như một hướng tiếp theo để huấn luyện agent có khả năng quyết định adaptive tốt hơn. ([arXiv][1])

---

# Tái cấu trúc ý tưởng cốt lõi của paper

Nếu bỏ toàn bộ chi tiết phụ, paper thực chất đang giải quyết **hai bài toán context khác nhau**:

```text
                 ON-DEVICE AGENT
                       │
          ┌────────────┴────────────┐
          │                         │
    History Bloat              Tool Bloat
          │                         │
          ▼                         ▼
   Semantic Memory             JIT Schema
          │                         │
          ▼                         ▼
        CSO                 Tool Selection
          │                         │
          └────────────┬────────────┘
                       ▼
              Context-efficient
                    Agent
```

Có thể cô đọng thành:

$$
\boxed{
\text{Efficient Agent}
=
\text{Semantic Memory}
+
\text{Selective Tool Context}
}
$$

Trong đó:

$$
\text{Semantic Memory}
:
H_{1:t}
\rightarrow
CSO_t
$$

và:

$$
\text{Tool Management}
:
\{T_1,\ldots,T_N\}
\rightarrow
T_{selected}
$$

Đây là **ý tưởng trung tâm** của toàn bộ nghiên cứu.

---

# Notation Map

| Ký hiệu    | Ý nghĩa                               |
| ---------- | ------------------------------------- |
| $u_t$      | User input tại timestep $t$           |
| $C_t$      | Context State Object tại timestep $t$ |
| $\Delta_t$ | CSO update mới                        |
| $a_t$      | Action của agent                      |
| $o_t$      | Observation/tool output               |
| $\theta_E$ | Tham số Executor                      |
| $\theta_M$ | Tham số State-Tracker                 |
| $\oplus$   | Phép append/concatenation             |
| $T$        | Tập các tools                         |
| $T_i$      | Tool thứ $i$                          |
| $t^*$      | Tool được lựa chọn                    |

Notation trên được dùng thống nhất trong phần phân tích; riêng một số phương trình như $a_t=f_{\theta_E}(\cdot)$ là **formalization của Agent để giải thích architecture**, không phải công thức được paper viết nguyên dạng.

---

# Content Verification

| Thành phần                    | Trạng thái |
| ----------------------------- | ---------- |
| Research problem              | ✓          |
| Research gap                  | ✓          |
| Objective                     | ✓          |
| Contributions                 | ✓          |
| Architecture                  | ✓          |
| Dual-adapter memory           | ✓          |
| CSO                           | ✓          |
| JIT schema                    | ✓          |
| Training                      | ✓          |
| Dataset/evaluation            | ✓          |
| Metrics                       | ✓          |
| Main results                  | ✓          |
| Ablation/component comparison | ✓          |
| Discussion                    | ✓          |
| Limitations                   | ✓          |
| Future work                   | ✓          |

# Mathematical Verification

Các công thức cốt lõi được chuẩn hóa theo một notation thống nhất:

$$
a_t=f_{\theta_E}(u_t,C_{t-1})
$$

$$
\Delta_t=g_{\theta_M}(u_t,a_t,o_t,C_{t-1})
$$

$$
C_t=C_{t-1}\oplus\Delta_t
$$

và không sử dụng các ký hiệu khác nhau cho cùng một khái niệm.

**Lưu ý:** ba phương trình trên là **formalization để giải thích kiến trúc**, trong khi phương trình $C_t=C_{t-1}\oplus\Delta_t$ được paper nêu trực tiếp. ([arXiv][1])

---

## Kết luận

> **Bài báo không đề xuất một LLM lớn hơn hay một context window lớn hơn; nó đề xuất thay đổi cách agent “nhớ” và “nhìn thấy tool”: lưu lịch sử dưới dạng CSO có cấu trúc bằng dual-LoRA memory, đồng thời chỉ đưa full tool schema vào context đúng lúc cần thiết.**

Đó là lý do paper đạt được **giảm mạnh context cost nhưng vẫn duy trì, thậm chí cải thiện, khả năng tool-use trong các task multi-turn**. ([arXiv][1])

[1]: https://arxiv.org/pdf/2511.03728 "Efficient On-Device Agents via Adaptive Context Management"
