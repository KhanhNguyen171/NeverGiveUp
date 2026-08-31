# Learning Agent-Compatible Context Management for Long-Horizon Tasks

Bài báo này đặc biệt đáng chú ý vì nó không cố cải thiện trực tiếp LLM agent, mà đặt một **context manager bên ngoài agent**, huấn luyện manager bằng RL trong khi **đóng băng agent**. ([arXiv][1])

# 1. Nhìn toàn cảnh bài báo

Tên bài:

> **Learning Agent-Compatible Context Management for Long-Horizon Tasks**

Tác giả đề xuất **AdaCoM — Adaptive Context Management**.

Ý tưởng cốt lõi có thể cô đọng thành:

```text
                Long-horizon Task
                       │
                       ▼
              ┌─────────────────┐
              │  Frozen Agent A │
              └────────┬────────┘
                       │
                Action / Observation
                       │
                       ▼
              ┌─────────────────┐
              │ Context Manager │
              │     AdaCoM      │
              └────────┬────────┘
                       │
          modify / delete / merge /
             rewrite / preserve
                       │
                       ▼
             Managed Context
                       │
                       ▼
              Frozen Agent A
```

Điểm quan trọng nhất:

> **AdaCoM không train lại agent. Nó train một model khác để học cách quản lý context sao cho phù hợp với agent đang có.**

Đây chính là điểm khác biệt kiến trúc quan trọng nhất của paper. ([arXiv][1])

---

# Chương 1. Giới thiệu và vấn đề nghiên cứu

## 1.1. Bối cảnh

LLM agents ngày càng được sử dụng cho các nhiệm vụ **long-horizon**, chẳng hạn:

* web search;
* deep research;
* multi-step tool use;
* các nhiệm vụ có nhiều vòng reasoning → action → observation.

Trong những nhiệm vụ này, context tăng dần:

```text
Question
   ↓
Action₁ → Observation₁
   ↓
Action₂ → Observation₂
   ↓
Action₃ → Observation₃
   ↓
...
   ↓
Actionₜ → Observationₜ
```

Nếu agent luôn giữ toàn bộ trajectory, context có thể trở nên rất dài.

Vấn đề không đơn giản là **context vượt giới hạn token**.

Vấn đề sâu hơn là:

> **Context càng dài không đồng nghĩa reasoning càng tốt.**

Paper chỉ ra rằng context dài có thể gây:

* long-context degradation;
* quên constraint;
* positional bias;
* giảm khả năng reasoning;
* tìm kiếm lặp lại;
* premature abandonment.

([arXiv][1])

---

## 1.2. Vấn đề nghiên cứu

Một ReAct agent thông thường có context:

$$
c_t^{\mathrm{vanilla}}
=
(q,a_1,o_1,\ldots,a_t,o_t)
$$

trong đó:

* $q$: task/query;
* $a_t$: action của agent;
* $o_t$: observation từ environment.

Agent sinh action tiếp theo:

$$
a_{t+1}
\sim
A(c_t^{\mathrm{vanilla}})
$$

Tức là agent nhìn vào **toàn bộ context tích lũy** để quyết định bước tiếp theo. ([arXiv][1])

Nhưng context này có một vấn đề:

```text
Useful information
       +
Stale information
       +
Redundant information
       +
Intermediate reasoning
       +
Old tool results
       ↓
Very long context
       ↓
Reasoning degradation
```

---

# 2. Research Gap

Các nghiên cứu trước chủ yếu giải quyết context management bằng hai hướng.

### Hướng 1 — Agent tự quản lý context

Ví dụ:

```text
Agent
  │
  ├── reason
  ├── act
  ├── observe
  └── summarize/prune memory
```

Vấn đề:

> Agent phải được huấn luyện để biết cách sử dụng cơ chế context mới.

Điều này không thuận lợi khi sử dụng **closed-source agents**. ([arXiv][1])

---

### Hướng 2 — Fixed context management

Ví dụ:

```text
Context
   ↓
Summarization
   ↓
Compressed Context
```

Nhưng summarization là một chiến lược cố định.

Trong khi:

```text
Agent A ≠ Agent B ≠ Agent C
```

Các agent có:

* capability khác nhau;
* reasoning style khác nhau;
* training khác nhau;
* khả năng xử lý context khác nhau.

Do đó một chiến lược compression có thể tốt với agent A nhưng không tốt với agent B.

([arXiv][1])

---

# 3. Research Gap thực sự

Paper đặt ra câu hỏi:

> **Can we discover the preferred context management strategy for each agent without training the agent itself?** ([arXiv][1])

Đây chính là research gap.

Có thể biểu diễn:

```text
Existing approach

Agent
  ↓
Self-management
  ↓
Requires agent training


Alternative

Context
  ↓
Fixed summarization
  ↓
Same strategy for different agents


Paper

Frozen Agent
     ▲
     │
Adaptive Manager
     │
     └── learns agent-compatible strategy
```

---

# Chương 2. Cơ sở lý thuyết và tổng quan

## 2.1. ReAct Agent

AdaCoM được xây dựng trên workflow kiểu ReAct.

Agent liên tục thực hiện:

$$
\text{Reason}
\rightarrow
\text{Act}
\rightarrow
\text{Observe}
\rightarrow
\text{Reason}
\rightarrow \cdots
$$

Context vì thế phát triển theo thời gian.

AdaCoM không thay đổi logic reasoning của agent.

Nó thay đổi **context mà agent được nhìn thấy**.

---

# 4. Context Management khác Memory

Đây là một distinction rất quan trọng.

Paper phân biệt:

### Long-term memory

Mục tiêu:

> Lưu thông tin qua nhiều session/task/user.

Ví dụ:

```text
Conversation 1
       ↓
Persistent Memory
       ↓
Conversation 2
```

### AdaCoM

Mục tiêu:

> Quản lý **working context trong cùng một task dài**.

Ví dụ:

```text
Task
 ↓
Step 1
 ↓
Step 2
 ↓
Step 3
 ↓
...
 ↓
Step 30

AdaCoM quản lý context đang hoạt động
```

Paper gọi đây là **working-memory management** thay vì persistent memory. ([arXiv][1])

---

# Chương 3. Phương pháp nghiên cứu

# 3.1. Kiến trúc AdaCoM

Đây là phần quan trọng nhất của paper.

Agent được giữ nguyên:

$$
A = \text{Frozen}
$$

Manager có policy:

$$
\pi_\theta(m_t\mid p_t)
$$

Trong đó:

* $\theta$: parameters của context manager;
* $p_t$: management prompt;
* $m_t$: modification action.

([arXiv][1])

---

## 3.2. Workflow

Giả sử managed context sau bước $t-1$ là:

$$
\tilde{c}_{t-1}
$$

Agent thực hiện:

$$
a_t \sim A(\tilde{c}_{t-1})
$$

Environment trả về:

$$
o_t
$$

Sau đó tạo context trước khi management:

$$
c_t
=
\operatorname{Append}
(\tilde{c}_{t-1},a_t,o_t)
$$

Manager nhận:

$$
p_t=P(c_t)
$$

và sinh:

$$
m_t
\sim
\pi_\theta(\cdot\mid p_t)
$$

Cuối cùng:

$$
\tilde{c}_t
=
\operatorname{Apply}(c_t,m_t)
$$

Agent tiếp tục reasoning trên:

$$
\tilde{c}_t
$$

([arXiv][1])

Toàn bộ vòng lặp:

```text
                 ┌─────────────────────┐
                 │   Managed Context   │
                 │       c̃(t-1)        │
                 └──────────┬──────────┘
                            │
                            ▼
                     Frozen Agent A
                            │
                            ▼
                         Action
                            │
                            ▼
                       Environment
                            │
                            ▼
                       Observation
                            │
                            ▼
                    Pre-management
                       context ct
                            │
                            ▼
                    ┌──────────────┐
                    │ AdaCoM πθ    │
                    └──────┬───────┘
                           │
              Modification action mt
                           │
                           ▼
                  Managed Context c̃t
                           │
                           └──────────────► Agent
```

---

# 3.3. Điểm mới: Flexible Modification Action Space

Đây là innovation quan trọng.

Các phương pháp cũ thường nói:

```text
context → summarize
```

AdaCoM nói:

```text
context → arbitrary modification
```

Manager có thể:

* giữ nguyên;
* delete;
* rewrite;
* merge;
* condense;
* extract;
* thay đổi role của message.

Mỗi modification có cấu trúc:

$$
\delta_t^{(j)}
=
(
ids^{(j)},
role^{(j)},
justification^{(j)},
new\_content^{(j)}
)
$$

([arXiv][1])

Đặc biệt:

```text
new_content = empty
        ↓
delete

new_content ≠ empty
        ↓
rewrite / merge
```

Messages không được chọn sẽ được giữ nguyên. ([arXiv][1])

Đây là khác biệt rất quan trọng:

> **AdaCoM không học "cách summarize context". Nó học "nên làm gì với từng phần context".**

---

# 4. RL formulation

Paper formulation AdaCoM thành một **Markov Decision Process**.

State có thể hiểu là context hiện tại:

$$
s_t \approx c_t
$$

Action:

$$
m_t
\sim
\pi_\theta(m_t\mid p_t)
$$

Transition:

$$
c_t
\xrightarrow{m_t}
\tilde{c}_t
$$

sau đó frozen agent tiếp tục tương tác với environment.

Trajectory:

$$
\tau
=
((p_1,m_1),\ldots,(p_T,m_T))
$$

Reward cuối cùng phụ thuộc vào kết quả task của agent. ([arXiv][1])

---

# 5. Tại sao cần Process Reward?

Nếu chỉ dùng final reward:

```text
Manager
 ↓
30 modifications
 ↓
Agent answer
 ↓
Correct / Wrong
```

thì rất khó biết modification nào có ích.

Đây là **credit assignment problem**.

Paper bổ sung process rewards.

Có các penalty/reward cho:

### Context quá dài

Nếu:

$$
|\tilde{c}_t| \gt L_{\max}
$$

manager bị token penalty.

### Redundant action

Nếu agent liên tục thực hiện cùng tool call:

$$
(a_t,a_{t+1})
=
(\text{same tool, same parameters})
$$

manager action ở giữa bị penalty.

### Invalid output

Penalty nếu:

* JSON lỗi;
* message ID không tồn tại;
* thiếu field.

([arXiv][1])

---

# 6. Hai cấp độ reward

Paper phân biệt:

### Outcome reward

$$
R_i
$$

Đánh giá kết quả cuối task.

### Process reward

$$
Q_{i,t}
$$

Đánh giá hành vi quản lý context ở từng bước.

Sau normalization, paper kết hợp:

$$
A_{i,t}
=
A_i^R
+
\alpha A_{i,t}^Q
$$

sau đó normalize lại:

$$
\hat{A}_{i,t}
=
\frac{A_{i,t}-\mu_A}
{\sigma_A+\epsilon}
$$

([arXiv][1])

Ý tưởng rất quan trọng:

```text
Final answer
     ↓
Outcome signal

Intermediate management
     ↓
Process signal

       ↓

Combined advantage
       ↓
RL update
```

---

# 7. Policy Optimization

Paper sử dụng PPO-style clipped objective trên token được manager sinh ra:

$$
J(\theta)
=
\mathbb{E}
\left[
\frac{1}{Z}
\sum_{i,t,u}
\min
\left(
r_{i,t,u}(\theta)\hat{A}_{i,t},
\bar r_{i,t,u}(\theta)\hat{A}_{i,t}
\right)
\right]
$$

với:

$$
\bar r_{i,t,u}(\theta)
=
\operatorname{clip}
\left(
r_{i,t,u}(\theta),
1-\epsilon,
1+\epsilon
\right)
$$

([arXiv][1])

Paper sử dụng **SFT trước**, sau đó RL bằng **GRPO** để huấn luyện manager. ([arXiv][1])

Pipeline:

```text
Qwen3-4B-Instruct
        │
        ▼
       SFT
        │
        ▼
Learn valid modification format
        │
        ▼
       GRPO
        │
        ├── Outcome reward
        ├── Process reward
        └── Format / redundancy / token penalties
        │
        ▼
   AdaCoM Manager
```

---

# Chương 4. Thực nghiệm

## 8. Dataset / Benchmark

Paper sử dụng hai nhóm task.

### BrowseComp-Plus

Bài toán web search.

Agent có:

```text
search(query, top_k)
get_document(doc_id)
finish(...)
```

Training/test:

$$
680/150
$$

và sử dụng Qwen3-Embed-8B làm retriever. Maximum 35 iterations. ([arXiv][1])

### MCP-Bench-Wiki

Deep research dựa trên Wikipedia MCP.

Agent có 9 tools liên quan tới:

* search;
* retrieve;
* summarize;
* sections;
* related topics;
* links;
* facts.

([arXiv][1])

---

# 9. Baselines

Paper so sánh:

| Method              | Ý tưởng                                  |
| ------------------- | ---------------------------------------- |
| ReAct               | Không context management                 |
| SumAgent            | Agent tự summarization                   |
| MemAct              | Agent dùng pruning tool                  |
| SumCoM              | External manager nhưng chỉ summarization |
| AdaCoM w/o training | Flexible manager nhưng chưa SFT/RL       |
| **AdaCoM**          | Flexible + trained external manager      |

([arXiv][1])

Đây là một thiết kế ablation khá tốt vì nó tách được hai yếu tố:

```text
Flexible action space
        +
Training
```

---

# 10. Kết quả chính

Trên BrowseComp-Plus:

| Agent       | ReAct |    AdaCoM |
| ----------- | ----: | --------: |
| Qwen3-Max   | 27.78 | **36.67** |
| Kimi-K2     | 18.56 | **36.20** |
| GLM-4.5-Air | 32.56 | **35.33** |
| DeepSeek-V3 | 17.78 | **26.19** |
| Average     | 24.17 | **33.60** |

Relative gain trung bình:

$$
\boxed{+39.0\%}
$$

Kimi đạt:

$$
\boxed{+95.0\%}
$$

([arXiv][1])

Đây là bằng chứng quan trọng cho claim:

> Có thể cải thiện agent mà không cần retrain chính agent.

---

# 11. Kết quả trên Deep Research

MCP-Bench-Wiki:

| Agent    | ReAct |    AdaCoM |
| -------- | ----: | --------: |
| Kimi     | 55.05 | **60.01** |
| DeepSeek | 47.51 | **58.09** |
| Average  | 51.28 | **59.05** |

Average relative improvement:

$$
\boxed{+15.2\%}
$$

Kimi:

$$
+9.0\%
$$

DeepSeek:

$$
+22.3\%
$$

([arXiv][1])

---

# 12. AdaCoM thực sự giúp agent như thế nào?

Đây là phần tôi cho rằng **quan trọng hơn cả bảng benchmark**.

Paper phát hiện ba failure mode chính.

### 1. Constraint forgetting

Agent quên một số yêu cầu của task.

AdaCoM thường duy trì một compact state message chứa:

```text
Task requirements
        +
Unresolved constraints
        +
Useful evidence
        +
Current leads
        +
Rejected candidates
        +
Ineffective queries
```

Điều này giúp agent kiểm tra candidate dựa trên **toàn bộ constraints**, thay vì chỉ một phần. ([arXiv][1])

---

### 2. Premature abandonment

Agent từ bỏ task quá sớm.

AdaCoM giữ lại:

```text
What has been tried
        ↓
What failed
        ↓
What remains unresolved
        ↓
What should be searched next
```

Do đó agent ít "give up" hơn. ([arXiv][1])

---

### 3. Redundant exploration

Đặc biệt rõ ở Kimi.

Paper báo cáo khoảng:

$$
42.6\%
$$

tool-use steps của Kimi trong BrowseComp-Plus là repetitive.

AdaCoM ghi lại những gì đã thử và loại bỏ kết quả không hữu ích, từ đó giảm vòng lặp tìm kiếm. ([arXiv][1])

---

# 13. Phát hiện quan trọng nhất: Fidelity–Reliability Trade-off

Đây có lẽ là **scientific insight quan trọng nhất của paper**, không chỉ là AdaCoM.

Paper quan sát:

```text
Agent capability ↑
        ↓
Can tolerate more raw context
        ↓
Preserve more information
```

Ngược lại:

```text
Agent capability ↓
        ↓
Long context becomes harmful earlier
        ↓
Need aggressive compression
```

Các manager học được context length trung bình khoảng:

| Agent    | Context sau management |
| -------- | ---------------------: |
| DeepSeek |                  ~1.9K |
| Kimi     |                  ~3.4K |
| Qwen     |                  ~5.2K |
| GLM      |                  ~7.0K |

([arXiv][1])

---

# 14. Hai chiến lược manager học được

## Stronger agents

Ví dụ:

* GLM;
* Qwen.

Manager thường sử dụng:

```text
Raw context
     ↓
Grow
     ↓
Grow
     ↓
Occasional compression
```

Đây là:

> **Tiered management**

([arXiv][1])

---

## Weaker agents

Ví dụ:

* DeepSeek;
* Kimi.

Manager thường:

```text
New observation
      ↓
Immediate compression
      ↓
Short working memory
      ↓
Next step
```

Đây là:

> **Eager distillation**

([arXiv][1])

---

# 15. Insight sâu hơn

Paper không đơn giản kết luận:

> "Context càng ngắn càng tốt."

Mà ngược lại:

$$
\boxed{
\text{Optimal Context}
=
\text{Maximum Useful Information}
\quad
\text{subject to}
\quad
\text{Reliable Reasoning}
}
$$

Tức tồn tại một trade-off:

```text
             Fidelity
                ↑
                │       ●
                │      /
                │     /
                │    /
                │   /
                │  /
                └────────────→ Context length
                       ↑
                Reliability starts dropping
```

Có thể hiểu:

> **Context management không phải bài toán compression đơn thuần; nó là bài toán tìm context mà một agent cụ thể có thể sử dụng đáng tin cậy.**

Đây là điểm tôi đánh giá là đóng góp khái niệm đáng chú ý nhất.

---

# 16. Transfer giữa các agent

Một câu hỏi tiếp theo:

> Nếu đã train manager cho agent A, có dùng manager đó cho agent B không?

Paper thử nghiệm:

```text
Source agents
├── DeepSeek
├── Kimi
├── Qwen
└── GLM

Target agents
├── DeepSeek
├── Kimi
├── Qwen
├── GLM
├── GPT-OSS-20B
├── Gemini
├── Seed
└── GPT-4o-mini
```

Kết quả:

* 23/28 cross-agent pairs có improvement;
* trung bình cross-agent improvement: **22.1%**;
* toàn bộ 32 pairs gồm self-trained: **25.0%**;
* mức cross-agent cao nhất: **79.6%** trên Kimi với manager train từ DeepSeek. ([arXiv][1])

---

# 17. Nhưng transfer không chỉ phụ thuộc capability

Một phát hiện tinh tế hơn:

$$
\text{Transfer quality}
\approx
f(
\text{Capability proximity},
\text{Reasoning-style compatibility}
)
$$

Agent có performance ReAct tương tự thường transfer tốt hơn.

Nhưng không phải lúc nào cũng vậy.

Ví dụ paper ghi nhận:

* DeepSeek thích working memory ngắn với key findings/document IDs;
* manager học từ Kimi có xu hướng giữ search history chi tiết;
* Gemini không sử dụng tốt report-style memory của manager học từ Qwen.

([arXiv][1])

Do đó:

> **Capability similarity là first-order predictor, nhưng reasoning-style compatibility mới là yếu tố bổ sung quan trọng.**

---

# Chương 5. Kết luận

## 18. Paper thực sự đóng góp gì?

Có thể tái cấu trúc contribution thành 3 tầng.

### Contribution 1 — Architectural

Tách:

$$
\text{Agent}
\neq
\text{Context Manager}
$$

Agent được freeze.

Manager đứng bên ngoài.

---

### Contribution 2 — Algorithmic

Thay vì fixed summarization:

$$
\text{Summarize}(c)
$$

AdaCoM học:

$$
m_t
\sim
\pi_\theta(m_t|c_t)
$$

với action space có thể:

$$
\{
\text{rewrite},
\text{delete},
\text{merge},
\text{preserve},
\text{extract}
\}
$$

---

### Contribution 3 — Empirical / Scientific

Paper phát hiện:

$$
\boxed{
\text{Fidelity}
\leftrightarrow
\text{Reliability}
}
$$

và đưa ra bằng chứng rằng context management cần **agent-specific adaptation**. ([arXiv][1])

---

# 19. Limitations

Paper khá rõ về limitation.

### 19.1. Evaluation scope

Chỉ thử trên:

* web search;
* deep research.

Chưa thử:

* coding agents;
* embodied agents;
* long-form writing.

([arXiv][1])

### 19.2. Manager chỉ 4B

Manager dựa trên:

> Qwen3-4B-Instruct.

Với agent rất mạnh, 4B manager có thể không đủ khả năng preserve/compress evidence losslessly. ([arXiv][1])

### 19.3. Inference overhead

AdaCoM thêm một lần inference của manager ở mỗi agent step:

```text
Agent inference
      +
Manager inference
```

→ tăng token cost và latency. ([arXiv][1])

### 19.4. KV cache

Vì manager sửa context cũ:

```text
old context
   ↓
modify
   ↓
new context
```

KV cache của agent có thể khó reuse.

Điều này làm giảm hiệu quả inference. ([arXiv][1])

---

# 20. Cách hiểu bài báo trong một câu

Nếu phải nén toàn bộ paper thành một ý:

> **Thay vì bắt LLM agent tự học cách quản lý context, hãy đặt một LLM manager bên ngoài và dùng reinforcement learning để nó học context nào cần giữ, context nào cần nén/xóa, sao cho phù hợp với khả năng reasoning của agent đang được đóng băng.**

Và phát hiện quan trọng hơn:

> **Không tồn tại một chiến lược context management tối ưu cho mọi agent; agent mạnh có thể cần giữ nhiều thông tin hơn, trong khi agent yếu hơn thường cần compression mạnh hơn để duy trì reasoning reliability.**

---

## 21. Knowledge Map của bài báo

Có thể dùng cấu trúc này để tiếp tục đào sâu paper:

```text
Long-Horizon LLM Agents
│
├── ReAct
│   └── Growing Context
│
├── Long-Context Degradation
│   ├── Constraint Forgetting
│   ├── Premature Abandonment
│   └── Redundant Exploration
│
├── Existing Context Management
│   ├── Self Summarization
│   ├── Pruning Tool
│   └── Fixed Summarization
│
└── AdaCoM
    │
    ├── Frozen Agent
    │
    ├── External Context Manager
    │
    ├── Flexible Modification
    │   ├── Rewrite
    │   ├── Delete
    │   ├── Merge
    │   ├── Extract
    │   └── No Change
    │
    ├── SFT
    │
    ├── GRPO / RL
    │   ├── Outcome Reward
    │   ├── Process Reward
    │   ├── Token Penalty
    │   ├── Redundancy Penalty
    │   └── Format Penalty
    │
    └── Findings
        ├── Performance Improvement
        ├── Fidelity–Reliability Trade-off
        └── Capability-based Transfer
```

**Nhận xét tổng thể:** đây không chỉ là một paper về "summarize context". Trọng tâm sâu hơn là **agent-compatible context management**: context được xem như một **đối tượng có thể điều khiển bằng policy**, và policy đó phải học theo **đặc tính của agent downstream**. Chính vì vậy, phần đáng đào sâu nhất tiếp theo là **Section 3 — MDP + modification action space + GRPO/process-reward**, vì đó là nơi ý tưởng của paper được biến thành một hệ thống có thể train được. ([arXiv][1])

[1]: https://arxiv.org/pdf/2605.30785 "Learning Agent-Compatible Context Management for Long-Horizon Tasks"
