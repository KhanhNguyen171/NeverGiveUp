# Perception Before Supervision: Self-Contained Visual Distillation from Counterfactual Blind Spots

> code: https://github.com/mbzuai-oryx/CVPD
>
> Project Page: https://mbzuai-oryx.github.io/CVPD/
>
> Model: https://huggingface.co/shravvvv/CVPD
>
> Link bài báo: https://arxiv.org/pdf/2608.09931

### Abstract

Việc tự cải thiện các **Multimodal Large Language Models (MLLMs)** hiện thường dựa trên các phương pháp dựa vào reward, cung cấp phản hồi dưới dạng một giá trị vô hướng khá thô. **Distillation** là một hướng giàu thông tin hơn nhờ cung cấp supervision dày đặc ở mức token, nhưng trong miền thị giác, phương pháp này thường phụ thuộc vào context đặc quyền được xây dựng từ annotation, công cụ bên ngoài hoặc các mô hình mạnh hơn.

Bài báo giới thiệu **CVPD (Contrastive Counterfactual Visual Process Distillation)**, một framework được đề xuất nhằm thực hiện **dense, on-policy, token-level visual self-distillation** cho MLLMs mà không cần nguồn giám sát bên ngoài.

Ý tưởng chính của CVPD là xác định **visual blind spots** — những vùng trong ảnh mà khi phóng to (**crop**) sẽ làm thay đổi và làm sắc nét phân phối câu trả lời của model, trong khi khi loại bỏ vùng đó (**ghost**) thì hành vi trên toàn ảnh gần như không thay đổi. Điều này cho thấy model **đã có khả năng mã hóa thông tin thị giác cần thiết nhưng chưa sử dụng nó một cách ổn định khi xử lý toàn bộ ảnh**.

CVPD sử dụng **Counterfactual Criterion gồm ba điều kiện** để phát hiện trực tiếp các vùng này từ chính phản hồi của model, sau đó chuyển chúng thành **dense contrastive supervision** cho quá trình self-distillation.

Cụ thể:

* **Crop view** đóng vai trò **positive teacher**, cung cấp tín hiệu về khả năng nhận biết chi tiết mà model có thể khai thác khi tập trung đúng vùng.
* **Ghost view** đóng vai trò **negative teacher**, biểu diễn hành vi mặc định khi model không sử dụng vùng thông tin đó.
* **Full-image view** là policy mà model cần cải thiện.

Trên **Qwen3-VL-8B-Instruct**, CVPD vượt qua sáu phương pháp self-evolving trên mười hai benchmark và không gây regression trên benchmark nào. Các mức cải thiện lớn nhất đạt được trên những nhiệm vụ yêu cầu khả năng chú ý thị giác cục bộ chính xác, với **+3.60 trên OCRBench**, **+3.38 trên MMStar Fine-Grained Perception** và **+3.08 trên MMStar Logical Reasoning**.

## 1. Introduction

Bài báo đặt vấn đề **self-improvement cho Multimodal Large Language Models (MLLMs)**. Hai hướng chính hiện nay là **reward/correctness-based methods** và **distillation**.

Các phương pháp dựa trên reward có ưu điểm là không cần annotation, nhưng tín hiệu học thường chỉ là **scalar reward hoặc advantage** cho toàn bộ response/trajectory. Vì vậy, chúng không chỉ ra cụ thể **token nào cần thay đổi và nên thay đổi theo hướng nào**.

Distillation cung cấp supervision giàu thông tin hơn ở mức token bằng cách cho student học theo **next-token distribution của teacher**. Tuy nhiên, visual distillation gặp vấn đề về **privileged visual context**: cần một phiên bản của ảnh giúp model nhận ra thông tin mà nó bỏ sót trong ảnh gốc. Các phương pháp trước thường phải dùng **annotation, segmentation model, recognition system hoặc model mạnh hơn** để tạo context này. 

Công trình gần nhất là **Vision-OPD**, khai thác hiện tượng **regional-to-global perception gap**: cùng một MLLM có thể trả lời đúng khi nhìn một crop tập trung vào vùng bằng chứng nhưng lại trả lời sai khi nhìn toàn bộ ảnh. Tuy nhiên, Vision-OPD vẫn phụ thuộc vào các pipeline bên ngoài để xác định vùng, tạo câu hỏi và tạo answer labels. 

CVPD giải quyết khoảng trống này bằng cách **tự phát hiện visual blind spots từ chính hành vi counterfactual của model**. Một vùng được xem là blind spot khi:

* **Crop vùng đó** làm thay đổi và làm sắc nét phân phối câu trả lời.
* **Xóa/che vùng đó** gần như không làm thay đổi hành vi trên ảnh đầy đủ.
* Điều này cho thấy model **đã có khả năng nhận biết thông tin trong vùng nhưng không khai thác nó khi nhìn toàn ảnh**.

Từ đó, CVPD dùng **crop view làm positive teacher** và **ghost view làm negative teacher**, tạo ra supervision dày đặc ở mức token mà không cần annotation, reward, segmentation system hay model mạnh hơn. 

**Đóng góp chính:**

1. Đề xuất **three-gate Counterfactual Blind-Spot Criterion** để tự phát hiện vùng thị giác bị bỏ sót.
2. Đề xuất **Contrastive Self-Distillation** với positive/negative teacher từ cùng backbone.
3. Cho thấy CVPD cải thiện ổn định trên **12 visual perception và reasoning benchmarks**, đặc biệt ở các nhiệm vụ cần attention chính xác vào vùng nhỏ. 

## 2. Related Work

### Self-Improvement for Multimodal LLMs

Các phương pháp self-improvement hiện chủ yếu dựa trên **reinforcement learning, reward hoặc self-generated data**. Các phương pháp như GRPO, DAPO và các biến thể R1-style cho MLLM sử dụng reward hoặc advantage để cải thiện khả năng reasoning.

Các phương pháp self-evolving như **STaR, ReST, Self-Rewarding Language Models** và các biến thể cho MLLM giảm phụ thuộc vào annotation bằng cách tự tạo dữ liệu, tự đánh giá hoặc self-play.

Tuy nhiên, điểm chung của các phương pháp này là supervision vẫn mang tính **aggregate**: response, trajectory hoặc reasoning step nhận reward/score/advantage thay vì **token-level corrective supervision**. 

### On-Policy Self-Distillation

**Knowledge Distillation** cho phép student học theo **next-token distribution của teacher**, cung cấp supervision chi tiết hơn reward.

**On-policy distillation** khắc phục vấn đề exposure bias bằng cách đánh giá teacher trên chính trajectory do student sinh ra. Các phương pháp như **GKD, OPSD và SDPO** cho thấy teacher có thể được tạo từ cùng model bằng cách cung cấp cho nó một **privileged context**, sau đó distill prediction về policy không có context đó.

Nguyên tắc chung là:

$$\text{Privileged Context} \rightarrow \text{Behavior Gap} \rightarrow \text{Dense Token-Level Supervision}$$

Vấn đề còn lại trong vision là **làm thế nào tạo privileged visual context mà không cần nguồn bên ngoài**. 

### Visual On-Policy Distillation

**Vision-OPD** khai thác **regional-to-global perception gap**: crop đúng vùng bằng chứng có thể giúp cùng một MLLM trả lời chính xác hơn so với full image.

Tuy nhiên, Vision-OPD vẫn cần:

* object recognition / segmentation để tìm evidence regions;
* MLLM để tạo crop-answerable questions;
* model mạnh hơn để tạo consensus answer labels.

Do đó, **teacher có thể đến từ cùng backbone nhưng privileged context vẫn được tạo externally**. 

### Khoảng trống mà CVPD giải quyết

Các hướng trước tạo thành hai nhóm:

$$\text{Reward-based} \rightarrow \text{Self-contained nhưng coarse supervision}$$

$$\text{Distillation-based} \rightarrow \text{Dense supervision nhưng cần privileged context}$$

CVPD kết hợp hai mục tiêu này:

$$\boxed{\text{Self-contained}+\text{On-policy}+\text{Dense Token-Level Visual Supervision}}$$

Điểm mới cốt lõi là **privileged visual context không được tạo bởi annotation, segmentation, reward model hay stronger model**, mà được phát hiện trực tiếp từ **counterfactual behavior của chính model đang được train**. 

## 3. Preliminaries

Phần này giới thiệu **on-policy distillation**, là nền tảng để CVPD xây dựng self-distillation cho MLLM. 

### 3.1. On-Policy Distillation

On-policy distillation cho phép **student** học theo phân phối token của **teacher** trên chính trajectory do student sinh ra.

Với input multimodal $(I,q)$, student sinh response:

$$y\sim p_S(\cdot|I,q)$$

Teacher được cung cấp một **privileged visual context** $\tilde I$, trong khi student chỉ nhìn ảnh gốc $I$.

Mục tiêu distillation là:

$$L_{OPD}(\theta)=\mathbb{E}*{(I,q)\sim D,y\sim p_S}\left[\frac{1}{|y|}\sum*{t=1}^{|y|}D\left(p_T(\cdot|\tilde I,q,y_{<t})\parallel p_S(\cdot|I,q,y_{<t})\right)\right]$$

Trong đó:

* $p_S$: student policy.
* $p_T$: teacher policy.
* $I$: ảnh đầu vào của student.
* $\tilde I$: privileged visual context của teacher.
* $q$: câu hỏi.
* $y_{<t}$: các token trước vị trí $t$.
* $D$: divergence giữa hai phân phối token.

Khác với reinforcement learning chỉ cung cấp **scalar reward**, OPD cung cấp **dense supervision tại từng token** trên trajectory do student tự sinh. 

### 3.2. Vấn đề của Self-Distillation trong Vision

Trong self-distillation, teacher và student dùng cùng backbone nên không có sự khác biệt về model capacity. Sự khác biệt phải đến từ **conditioning context**.

Với visual MLLM, cần tìm một vùng $R$ sao cho:

$$p_{\text{crop}}\neq p_{\text{full}}$$

tức là khi tập trung vào vùng đó, model thay đổi hành vi đáng kể.

CVPD dựa trên hiện tượng **regional-to-global perception gap**: model có thể trả lời đúng khi chỉ nhìn vùng bằng chứng nhưng không khai thác được thông tin đó khi nhìn toàn ảnh. 

### 3.3. Divergence được sử dụng

CVPD sử dụng **Jensen-Shannon divergence (JSD)** để đo sự khác biệt giữa các phân phối:

$$D=D_{JS}$$

Divergence được tính **theo từng token**, sử dụng union của top-$K$ logits từ teacher và student với $K=100$.

Đây là cơ sở để CVPD xác định xem một vùng ảnh có thực sự tạo ra **behavior gap** cần thiết cho self-distillation hay không. 

**Ý chính của Preliminaries:** OPD cung cấp dense token-level supervision, nhưng CVPD cần tự tìm được **privileged visual context**. Phần Method tiếp theo giải quyết chính vấn đề này bằng **Counterfactual Blind-Spot Criterion**.

## 4. Method: CVPD

CVPD gồm **hai phase**:

1. **Counterfactual Blind-Spot Discovery**: tìm các vùng ảnh mà model có khả năng nhận biết nhưng không khai thác khi nhìn toàn ảnh.
2. **Contrastive Self-Distillation**: dùng các vùng này để tạo supervision ở mức token cho student. 

### 4.1. Self-discovered Visual Blind Spots

Với ảnh $I$, câu hỏi $q$ và một vùng ứng viên $R$, CVPD tạo ba visual views từ cùng một model $p_\theta$:

* **Full view**: ảnh gốc.
* **Crop view**: crop vùng $R$, thêm margin 20% và upscale về kích thước ban đầu.
* **Ghost view**: giữ toàn ảnh nhưng Gaussian blur vùng $R$.

Tương ứng:

$$p_{full}=p_\theta(\cdot|I,q)$$

$$p_{crop}=p_\theta(\cdot|crop(I,R),q)$$

$$p_{ghost}=p_\theta(\cdot|ghost(I,R),q)$$

CVPD gọi $R$ là **visual blind spot** khi thỏa mãn ba gates:

#### Gate 1 — Latent Capability Divergence

Crop phải tạo ra sự thay đổi đủ lớn so với full image:

$$D_{JS}(p_{crop}\parallel p_{full})\geq\tau_{crop}$$

Điều này cho thấy khi được tập trung vào $R$, model có thể khai thác thêm thông tin mà full-image policy chưa thể hiện. 

#### Gate 2 — Default Perceptual Invariance

Ghost không được làm thay đổi đáng kể hành vi của full image:

$$D_{JS}(p_{ghost}\parallel p_{full})\leq\tau_{ghost}$$

Nếu xóa thông tin trong $R$ mà prediction gần như không đổi, model ban đầu gần như **không sử dụng vùng $R$**. Vì vậy ghost view có thể đại diện cho hành vi mặc định/inattentive của model. 

#### Gate 3 — Epistemic Sharpening

Crop phải làm prediction **sắc nét hơn**, thay vì chỉ tạo ra một thay đổi bất kỳ:

$$H[p_{crop}(y_0)]<H[p_{full}(y_0)]$$

Trong đó $H[\cdot]$ là entropy của phân phối tại token đầu tiên $y_0$.

Ba điều kiện kết hợp để xác định vùng mà:

$$\text{Crop}=\text{Useful Perception},\qquad\text{Ghost}=\text{Inattentive Default}$$

Sau khi lọc, các vùng được xếp hạng theo:

$$score(R)=D_{JS}(p_{crop}\parallel p_{full})-D_{JS}(p_{ghost}\parallel p_{full})+H[p_{full}(y_0)]-H[p_{crop}(y_0)]$$

CVPD giữ vùng có score cao nhất cho mỗi ảnh. 

#### Cách tạo candidate regions

Model tự tạo:

* fine-grained question $q$;
* probe answer $a$;
* candidate regions từ **self-grounding**, **3×3 grid** và **2×2 grid**.

Toàn bộ quá trình discovery đều dùng chính model đang được train, không sử dụng annotation, segmentation model hay stronger model. 

---

### 4.2. Contrastive Visual Process Distillation

Sau khi có **Curated Blind-Spot Pool**:

$$D_{CVPD}={(I_i,q_i,R_i,a_i)}_{i=1}^{N}$$

CVPD tạo **bốn policies** từ cùng backbone:

* $\pi_s$: **online student**, full image, có gradient.
* $\pi_+$: **crop-conditioned positive teacher**.
* $\pi_-$: **ghost-conditioned negative teacher**.
* $\pi_{ref}$: **reference policy**, full image với LoRA adapter tắt.

Teacher $\pi_+$ và $\pi_-$ dùng **EMA/Momentum Teacher**, không có gradient. 

Loss tại mỗi token gồm ba thành phần:

$$L_t=D_{JS}(\pi_+\parallel\pi_s)+\lambda_{rank}\max(0,m+D_{JS}(\pi_+\parallel\pi_s)-D_{JS}(\pi_-\parallel\pi_s))+\beta_tD_{KL}(\pi_s\parallel\pi_{ref})$$

#### 1. Latent Transfer

$$D_{JS}(\pi_+\parallel\pi_s)$$

Student được kéo về phía **crop teacher**, nhằm chuyển khả năng perceptual mà model đã thể hiện khi tập trung vào vùng $R$ sang policy xử lý full image.

#### 2. Contrastive Ranking

$$\lambda_{rank}\max(0,m+D_{JS}(\pi_+\parallel\pi_s)-D_{JS}(\pi_-\parallel\pi_s))$$

Không chỉ học từ crop teacher, student còn phải **phân biệt crop với ghost**.

Mục tiêu là:

$$D_{JS}(\pi_+\parallel\pi_s)+m\leq D_{JS}(\pi_-\parallel\pi_s)$$

Tức là student phải gần **positive teacher** hơn **negative teacher**. Ghost vì vậy trở thành một **negative learning signal**, thay vì chỉ được sử dụng để lọc blind spots ở Phase 1. 

#### 3. KL Anchor

$$\beta_tD_{KL}(\pi_s\parallel\pi_{ref})$$

Giữ student gần policy ban đầu trên full image, nhằm tránh việc cải thiện perception cục bộ làm suy giảm các năng lực multimodal tổng quát.

$\beta_t$ được điều chỉnh online để duy trì target KL:

$$\kappa=0.03$$

Cuối cùng, CVPD lấy trung bình loss trên toàn bộ rollout:

$$L_{CVPD}=\mathbb{E}*{(I,q,R,a)\sim D*{CVPD}}\left[\frac{1}{|a|}\sum_{t=1}^{|a|}L_t\right]$$

Điểm cốt lõi của Phase 2 là **crop và ghost tạo thành một cặp teacher đối lập**: crop chỉ ra model *có thể thấy gì*, còn ghost chỉ ra model *đang mặc định bỏ qua gì*. Student học để tiến gần crop teacher và tránh ghost teacher ở **từng token**. 


## 5. Experiments

CVPD được đánh giá trên **Qwen3-VL-4B và Qwen3-VL-8B-Instruct**, sử dụng **15,000 ảnh không gán nhãn**. Sau quá trình blind-spot discovery, thu được khoảng **2,590 curated tuples**, tương đương tỷ lệ giữ lại **17.2%**. Đánh giá trên **12 benchmark** về visual perception và multimodal reasoning. 

### 5.1. Main Results

Kết quả chính cho thấy **CVPD đạt kết quả tốt nhất trên cả 12 benchmark ở cả 4B và 8B** và là phương pháp duy nhất **không gây regression so với base model**. 

Trên **Qwen3-VL-8B-Instruct**, các cải thiện lớn nhất là:

| Benchmark                      |  Base |      CVPD |      Gain |
| ------------------------------ | ----: | --------: | --------: |
| OCRBench                       | 82.80 | **86.40** | **+3.60** |
| MMStar Fine-Grained Perception | 60.25 | **63.63** | **+3.38** |
| MMStar Logical Reasoning       | 61.69 | **64.77** | **+3.08** |

Các benchmark yêu cầu **localized visual attention** có mức cải thiện lớn nhất. Điều này phù hợp trực tiếp với mục tiêu của CVPD: giúp model khai thác các chi tiết thị giác mà trước đó bỏ sót khi nhìn toàn ảnh. 

Đồng thời, CVPD vẫn cải thiện các benchmark multimodal tổng quát, cho thấy việc tập trung vào visual blind spots **không đánh đổi năng lực tổng quát**. 

---

### 5.2. Ablation Study

Ablation tập trung kiểm tra vai trò của từng thành phần CVPD trên Qwen3-VL-8B.

**Hai thành phần quan trọng nhất là:**

#### 1. Counterfactual Criterion

Thay các blind spots được chọn bằng **random regions** làm hiệu năng giảm mạnh nhất:

* OCRBench: $86.40\rightarrow83.80$ (**−2.60**)
* MMStar FG: $63.63\rightarrow61.10$ (**−2.53**)

Điều này cho thấy **chất lượng vùng được chọn là yếu tố cốt lõi**. Random crop chủ yếu tạo noise, trong khi three-gate criterion tìm được những vùng thực sự chứa perceptual information mà model đang bỏ qua. 

#### 2. Contrastive Ranking Objective

Loại bỏ ranking loss cũng gây giảm đáng kể:

* OCRBench: $86.40\rightarrow84.10$ (**−2.30**)
* MMStar FG: $63.63\rightarrow61.47$ (**−2.16**)

Điều này chứng minh rằng **chỉ học từ crop teacher là chưa đủ**. Ghost teacher cung cấp negative signal để student chủ động tránh hành vi inattentive mặc định. 

Các thành phần còn lại có tác động nhỏ hơn:

* **EMA teacher** giúp target ổn định hơn.
* **Toàn bộ curated pool** tốt hơn chỉ dùng subset chất lượng cao.
* **Unfreeze vision encoder** làm giảm nhẹ hiệu năng → giữ vision encoder frozen là lựa chọn tốt hơn trong thiết lập này. 

**Kết luận ablation:**
$\boxed{\text{Blind-spot curation}+\text{Contrastive ranking}}$ là hai thành phần đóng góp lớn nhất vào hiệu quả của CVPD.

---

### 5.3. Sensitivity Analysis

Phân tích ba hyperparameter chính:

* Ranking weight $\lambda_{rank}$
* Margin $m$
* KL target $\kappa$

Giá trị mặc định:

$$\lambda_{rank}=0.5,\quad m=0.10,\quad\kappa=0.03$$

Đây là cấu hình cho **trade-off tốt nhất**. 

Đối với $\lambda_{rank}$:

| $\lambda_{rank}$ | MMStar FG |  OCRBench |
| ---------------: | --------: | --------: |
|              0.0 |     61.47 |     84.10 |
|             0.25 |     62.85 |     85.55 |
|          **0.5** | **63.63** | **86.40** |
|              1.0 |     63.00 |     85.65 |

$\lambda_{rank}=0.5$ đạt kết quả tốt nhất. Ranking quá yếu không đủ tách crop và ghost; ranking quá mạnh lại làm ảnh hưởng đến tín hiệu distillation chính. 

$ m$ và $\kappa$ ít nhạy hơn: các thay đổi trong khoảng được thử nghiệm chỉ gây biến động nhỏ, cho thấy CVPD **không yêu cầu tuning quá chính xác** đối với hai tham số này. 

---

### 5.4. Blind-Spot Source Analysis

CVPD sử dụng ba nguồn candidate regions:

1. **Track A:** Self-grounding.
2. **Track B:** $3\times3$ grid.
3. **Track C:** $2\times2$ grid.

Từng nguồn riêng lẻ đều cải thiện so với base model. **3×3 grid là nguồn mạnh nhất khi sử dụng riêng**, vì tạo ra nhiều vùng nhỏ hơn và tăng khả năng tìm được visual evidence cục bộ. 

| Source           |    Samples | MMStar FG |  OCRBench |
| ---------------- | ---------: | --------: | --------: |
| Grounding        |       ~699 |     62.50 |     84.90 |
| 2×2 grid         |       ~777 |     62.80 |     85.30 |
| 3×3 grid         |     ~1,373 | **63.20** | **85.95** |
| **All combined** | **~2,590** | **63.63** | **86.40** |

Quan trọng nhất, **kết hợp cả ba nguồn cho kết quả tốt nhất**. Điều này cho thấy self-grounding, coarse grid và fine grid tìm được **các blind spots bổ sung cho nhau** ở những spatial granularity khác nhau. 

**Ý chính của toàn bộ Experiments:** CVPD không chỉ cải thiện benchmark; các ablation xác nhận rằng **việc tìm đúng blind spot và sử dụng ghost như negative teacher chính là hai yếu tố quyết định hiệu quả của phương pháp**.


## 6. Conclusion

CVPD cho thấy một hướng tiếp cận quan trọng cho **self-improvement của Multimodal Large Language Models (MLLMs)**: model không nhất thiết phải cần annotation, reward model hay một model mạnh hơn để tự cải thiện khả năng perception. Thay vào đó, **chính hành vi của model có thể được dùng để phát hiện những thông tin thị giác mà model đã có khả năng nhận biết nhưng chưa khai thác tốt**. 

Toàn bộ bài báo có thể hiểu theo chuỗi sau:

$$\text{Full Image}\rightarrow\text{Counterfactual Probing}\rightarrow\text{Blind Spots}\rightarrow\text{Contrastive Distillation}\rightarrow\text{Improved Perception}$$

### Người đọc cần nắm được gì?

**1. Vấn đề**

MLLM có thể **nhìn thấy thông tin nhưng không sử dụng nó đúng cách** khi xử lý toàn bộ ảnh. Đây là nguồn gốc của nhiều lỗi trong fine-grained visual perception.

**2. Ý tưởng cốt lõi**

Thay vì hỏi *“model cần học thêm kiến thức gì?”*, CVPD hỏi:

> **“Model đang bỏ sót vùng nào mà nó thực sự đã có khả năng hiểu?”**

Đó chính là **visual blind spot**.

**3. Cách phát hiện**

CVPD so sánh ba cách nhìn cùng một ảnh:

$$\text{Full}\quad\text{vs.}\quad\text{Crop}\quad\text{vs.}\quad\text{Ghost}$$

* **Crop:** tập trung vào vùng → cho thấy model *có thể khai thác gì*.
* **Ghost:** làm mờ vùng → cho thấy model *đang mặc định bỏ qua gì*.
* **Full:** hành vi hiện tại cần được cải thiện.

Ba điều kiện counterfactual được dùng để lọc ra những vùng thực sự có giá trị.

**4. Cách học**

Sau khi tìm được blind spots, CVPD không dùng chúng làm label cứng. Nó biến chúng thành **dense token-level supervision**:

$$\text{Crop Teacher}=\text{Positive Signal}$$

$$\text{Ghost Teacher}=\text{Negative Signal}$$

Student được kéo gần crop teacher và đồng thời bị đẩy xa ghost teacher.

**5. Những gì thí nghiệm chứng minh**

Kết quả cho thấy:

* CVPD cải thiện trên **12 benchmark**.
* Cải thiện mạnh nhất ở các nhiệm vụ cần **localized visual attention**.
* **Counterfactual Criterion** là thành phần quan trọng nhất.
* **Contrastive Ranking** là thành phần quan trọng thứ hai.
* Kết hợp **self-grounding + 2×2 grid + 3×3 grid** tìm được các blind spots bổ sung cho nhau.
* Không cần external annotation, segmentation, reward model hoặc stronger model trong quá trình tạo training signal. 

### Bài học quan trọng nhất

CVPD đưa ra một góc nhìn đáng chú ý về **self-distillation**:

$$\boxed{\text{Self-improvement}\neq\text{Always learn new knowledge}}$$

Mà có thể là:

$$\boxed{\text{Self-improvement}=\text{Learn to better use knowledge the model already has}}$$

Đây là điểm quan trọng nhất cần nhớ khi học bài báo: **CVPD không chủ yếu bổ sung kiến thức thị giác mới cho MLLM; nó tìm ra các “blind spots” trong quá trình perception và dùng counterfactual contrastive distillation để giúp model khai thác tốt hơn những biểu diễn thị giác vốn đã tồn tại trong chính nó.** 
