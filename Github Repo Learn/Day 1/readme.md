# Play2Perfect

📄 **Paper:** https://arxiv.org/abs/2606.26428

https://github.com/user-attachments/assets/6bfafdbc-41f4-472a-aeaa-444f7e50076b

## What Matters in Dexterous Play Pretraining for Precise Assembly?

**Play2Perfect** là một pipeline Reinforcement Learning (RL) hai giai đoạn cho bài toán **dexterous robotic manipulation** và **contact-rich assembly**:

1. **Play pretraining**: học các manipulation priors có tính tổng quát thông qua tương tác với nhiều object và goal.
2. **Precise assembly finetuning**: chuyển policy đã pretrained sang các bài toán assembly yêu cầu tiếp xúc và độ chính xác cao.

Repository cung cấp môi trường huấn luyện trên Isaac Sim/Isaac Lab, evaluation cho bốn bài toán assembly và một reference tối giản cho sim-to-real deployment.

Paper đặt câu hỏi trung tâm:

> Những yếu tố nào trong quá trình **dexterous play pretraining** thực sự quyết định khả năng giải quyết **precise assembly**?

Paper báo cáo rằng pretraining bằng play tạo ra prior có thể tái sử dụng cho grasping, in-hand reorientation và pose reaching; khi finetune, policy tập trung vào tương tác contact-rich cuối cùng.

---

# 1. Problem Formulation

## 1.1 Dexterous Manipulation

Robot có nhiều bậc tự do phải điều khiển đồng thời vị trí và chuyển động của nhiều khớp để thao tác với object.

Trạng thái hệ thống tại thời điểm $t$ có thể biểu diễn:

$$
s_t =
\left[
q_t,
\dot q_t,
x_t^o,
R_t^o,
v_t^o,
\omega_t^o,
g_t
\right]
$$

trong đó:

* $q_t$: joint positions.
* $\dot q_t$: joint velocities.
* $x_t^o$: object position.
* $R_t^o$: object orientation.
* $v_t^o$: object linear velocity.
* $\omega_t^o$: object angular velocity.
* $g_t$: goal state.

Policy học ánh xạ:

$$
a_t = \pi_\theta(s_t)
$$

với $a_t$ là action điều khiển robot.

---

## 1.2 Contact-Rich Assembly

Precise assembly khác với manipulation thông thường ở chỗ trạng thái thành công phụ thuộc mạnh vào **hình học tiếp xúc**.

Có thể mô hình hóa khoảng cách giữa object và goal thông qua một tập keypoint:

$$
K_o = \{k_1^o,\ldots,k_m^o\}
$$

$$
K_g = \{k_1^g,\ldots,k_m^g\}
$$

Một đại lượng lỗi hình học:

$$
d_K =
\max_i
\left\|
k_i^o-k_i^g
\right\|_2
$$

Assembly thành công khi:

$$
d_K \leq \epsilon
$$

với $\epsilon$ là success tolerance.

Điểm quan trọng là $\epsilon$ có thể rất nhỏ đối với precise assembly. Paper tập trung vào các task có độ chính xác cao, trong đó tight insertion có clearance $0.5,\mathrm{mm}$.

---

# 2. Core Idea: Play2Perfect

## 2.1 Hai giai đoạn học

Pipeline được tổ chức:

$$
\boxed{
\text{Play Pretraining}
\rightarrow
\text{Assembly Finetuning}
}
$$

Giai đoạn thứ nhất không cố giải quyết trực tiếp assembly.

Thay vào đó policy học các primitive manipulation có khả năng chuyển giao:

$$
\mathcal{P}_{play}
=
\{
\text{grasping},
\text{reorientation},
\text{reaching},
\text{object manipulation}
\}
$$

Sau đó:

$$
\pi_{assembly}
\leftarrow
\operatorname{Finetune}
(\pi_{play})
$$

Mục tiêu là giảm lượng exploration cần thiết trong bài toán assembly vốn có reward sparse và contact dynamics phức tạp.

---

## 2.2 Vì sao không RL trực tiếp trên Assembly?

Nếu train trực tiếp:

$$
\pi_\theta:
s_t
\rightarrow
a_t
$$

policy phải đồng thời học:

* grasp;
* lift;
* transport;
* orientation;
* reaching;
* contact;
* insertion;
* precise alignment.

Không gian exploration lớn trong khi vùng trạng thái thành công rất nhỏ.

Play2Perfect tách bài toán:

$$
\text{general manipulation learning}
\rightarrow
\text{task-specific precision learning}
$$

Đây là ý tưởng trung tâm của repository.

---

# 3. Reinforcement Learning Formulation

## 3.1 Markov Decision Process

Bài toán được mô hình hóa dưới dạng MDP:

$$
\mathcal{M}
=
(\mathcal{S},\mathcal{A},P,r,\gamma)
$$

Trong đó:

* $\mathcal{S}$: state space.
* $\mathcal{A}$: action space.
* $P(s_{t+1}|s_t,a_t)$: transition dynamics.
* $r(s_t,a_t)$: reward.
* $\gamma$: discount factor.

Policy:

$$
\pi_\theta(a_t|s_t)
$$

Mục tiêu:

$$
J(\theta)
=
\mathbb{E}_{\tau\sim\pi_\theta}
\left[
\sum_{t=0}^{T}
\gamma^t r_t
\right]
$$

---

## 3.2 Continuous Control

Robot có $29$ joints trong observation/action pipeline của repository. Observation utilities định nghĩa:

$$
N_{joint}=29
$$

và năm fingertips:

$$
N_{fingertip}=5
$$

Repository xây dựng observation từ joint state, palm state, object state, fingertip geometry và keypoints.

Action có dạng continuous:

$$
a_t\in[-1,1]^{29}
$$

Policy sinh phân phối:

$$
\pi_\theta(a_t|s_t)
=
\mathcal{N}
(\mu_\theta(s_t),\sigma_\theta)
$$

---

# 4. Stage 1 — Play Pretraining

## 4.1 Mục tiêu

Play environment không hướng trực tiếp tới một assembly task cụ thể.

Policy phải học cách tương tác với object và goal trong free space.

Các prior quan trọng:

$$
\text{Play Prior}
=
\{
\text{grasp},
\text{lift},
\text{reorientation},
\text{reaching}
\}
$$

Các prior này trở thành initialization cho Stage 2.

---

## 4.2 Observation Representation

Repository không sử dụng một state vector duy nhất.

Observation được xây dựng từ các thành phần:

$$
o_t =
[
q_t,
\dot q_t,
a_{t-1},
p_t^{palm},
R_t^{palm},
v_t^{palm},
R_t^o,
v_t^o,
p_t^{finger},
K_t^o,
K_t^g,
s^o,
d_t,
l_t,
\ldots
]
$$

Các field được khai báo tập trung trong `obs_utils.py`. Một số kích thước quan trọng:

$$
\begin{aligned}
q &\in \mathbb{R}^{29}\\
\dot q &\in \mathbb{R}^{29}\\
p^{palm} &\in \mathbb{R}^{3}\\
R^{palm} &\in \mathbb{R}^{4}\\
v^{palm} &\in \mathbb{R}^{6}\\
p^{finger} &\in \mathbb{R}^{15}\\
K^o &\in \mathbb{R}^{12}\\
K^g &\in \mathbb{R}^{12}
\end{aligned}
$$

Repository tính tổng observation dimension bằng tổng kích thước các field theo thứ tự cấu hình.

---

## 4.3 Coordinate Representation

Internal quaternion sử dụng thứ tự:

$$
q=(w,x,y,z)
$$

Trong policy observation, quaternion được chuyển sang convention:

$$
q=(x,y,z,w)
$$

Repository thực hiện conversion trước khi đưa quaternion vào observation.

Điều này quan trọng vì orientation representation phải nhất quán giữa:

$$
\text{simulation}
\rightarrow
\text{observation}
\rightarrow
\text{policy}
\rightarrow
\text{deployment}
$$

---

## 4.4 Object Keypoints

Keypoints được xác định trong object frame:

$$
k_i^{local}\in\mathbb{R}^3
$$

Chuyển sang world frame:

$$
k_i^{world}
=
p_o
+
R_o k_i^{local}
$$

Repository hiện thực phép biến đổi bằng quaternion rotation:

$$
k_i^{world}
=
p_o
+
q_o
\otimes
k_i^{local}
\otimes
q_o^{-1}
$$

Keypoints sau đó được sử dụng để đo khoảng cách object-goal.

---

# 5. Observation Noise and Delay

## 5.1 Domain Randomization trên Observation

Repository không chỉ randomize physical environment mà còn mô phỏng uncertainty của observation.

Object state có thể được tạo thành:

$$
\tilde p_o
=
p_o+\epsilon_p
$$

với:

$$
\epsilon_p
\sim
\mathcal{N}(0,\sigma_p^2I)
$$

Orientation được perturb bởi một rotation ngẫu nhiên:

$$
\tilde q_o
=
\Delta q\otimes q_o
$$

Velocity có thể được lấy từ state bị delay.

---

## 5.2 Observation Delay

Repository duy trì rolling queue:

$$
Q_t=
[
o_t,o_{t-1},\ldots,o_{t-k+1}
]
$$

và chọn một delay:

$$
d\sim U\{0,\ldots,k-1\}
$$

để tạo:

$$
\tilde o_t=o_{t-d}
$$

Mục tiêu là làm policy ít phụ thuộc vào observation lý tưởng của simulator.

---

# 6. Reward Design

Reward của Play được xây dựng từ nhiều thành phần thay vì chỉ dùng một distance reward.

Repository tổng hợp:

$$
R_t
=
R_{lift}
+
R_{finger}
+
R_{keypoint}
+
R_{bonus}
+
R_{penalty}
$$

Cụ thể gồm:

$$
R_t =
R_{lift}
+
R_{lift\_bonus}
+
R_{finger\_delta}
+
R_{keypoint}
+
R_{arm\_penalty}
+
R_{hand\_penalty}
+
R_{goal}
$$

Cấu trúc này được thực hiện trực tiếp trong `reward_utils.py`.

---

## 6.1 Lifting Reward

Độ cao tương đối:

$$
z_{lift}
=
0.05+z_o-z_{init}
$$

Reward:

$$
R_{lift}
=
\operatorname{clip}
(z_{lift},0,0.5)
\cdot
\lambda_{lift}
$$

Khi object vượt threshold:

$$
z_{lift}>z_{threshold}
$$

trạng thái `lifted` được latch.

Repository cũng sử dụng one-shot lifting bonus khi trạng thái chuyển:

$$
\neg lifted_t
\rightarrow
lifted_{t+1}
$$

---

## 6.2 Fingertip Distance Progress

Khoảng cách hiện tại của fingertip tới object:

$$
d_i^t
=
\|f_i^t-p_o^t\|_2
$$

Repository lưu khoảng cách tốt nhất trước đó:

$$
d_i^{best}
=
\min(d_i^{best},d_i^t)
$$

Reward tiến bộ:

$$
\Delta d_i
=
d_i^{best}-d_i^t
$$

và:

$$
R_{finger}
=
\lambda_f
\sum_i
\operatorname{clip}
(\Delta d_i,0,d_{max})
$$

Reward này chỉ hoạt động trước khi object được lifted.

---

## 6.3 Keypoint Progress

Sau khi object được lifted, reward chuyển trọng tâm sang alignment.

Sai số:

$$
d_K^t
=
\max_i
\|k_i^o-k_i^g\|_2
$$

Best distance:

$$
d_K^{best}
=
\min(d_K^{best},d_K^t)
$$

Progress:

$$
\Delta d_K
=
d_K^{best}-d_K^t
$$

Reward:

$$
R_K
=
\lambda_K
\operatorname{clip}
(\Delta d_K,0,d_{max})
\cdot
\mathbf{1}_{lifted}
$$

---

## 6.4 Action / Motion Penalty

Repository đặt penalty trên joint velocity:

$$
R_{arm}
=
-\lambda_{arm}
\sum_{j\in J_{arm}}
|\dot q_j|
$$

$$
R_{hand}
=
-\lambda_{hand}
\sum_{j\in J_{hand}}
|\dot q_j|
$$

Do đó policy không chỉ tối đa hóa task reward mà còn bị regularize về chuyển động.

---

## 6.5 Goal Bonus

Khi đạt goal:

$$
R_{goal}
=
\lambda_g
\mathbf{1}_{success}
$$

Repository hỗ trợ hai cơ chế:

* amortized goal bonus;
* lump-sum bonus khi yêu cầu consecutive success.

---

# 7. Success and Termination

## 7.1 Success Criterion

Success được xác định từ keypoint error:

$$
d_K\leq\epsilon
$$

Repository có cơ chế yêu cầu trạng thái gần goal duy trì trong nhiều bước liên tiếp.

Nếu:

$$
I_t=
\mathbf{1}[d_K^t\leq\epsilon]
$$

thì counter:

$$
C_t=C_{t-1}+I_t
$$

với yêu cầu consecutive:

$$
C_t=
(C_{t-1}+I_t)I_t
$$

Do đó chỉ khi trạng thái gần goal liên tục mới đạt:

$$
C_t\geq N_{success}
$$

---

## 7.2 Termination

Episode kết thúc khi xảy ra một trong các điều kiện:

$$
terminated
=
fall
\lor
max\_successes
\lor
hand\_far
$$

hoặc timeout:

$$
truncated
=
episode\_length
\geq
T_{max}
$$

Repository đặt ngưỡng `hand_far` dựa trên khoảng cách lớn nhất của fingertip và kiểm tra object fall theo độ cao local.

---

# 8. Success-Tolerance Curriculum

## 8.1 Motivation

Precise assembly yêu cầu tolerance nhỏ.

Nếu bắt policy đạt tolerance cực nhỏ ngay từ đầu, exploration trở nên khó.

Do đó tolerance có thể được giảm dần:

$$
\epsilon_{t+1}
=
\alpha\epsilon_t
$$

với:

$$
0<\alpha<1
$$

subject to:

$$
\epsilon_{target}
\leq
\epsilon_t
\leq
\epsilon_{initial}
$$

Repository cập nhật tolerance khi success rate của các episode trước đạt threshold.

---

# 9. Stage 2 — Precise Assembly

## 9.1 Reuse Play Environment

Điểm đáng chú ý trong implementation là:

```text
PreciseAssemblyEnv
        ↓
     extends
        ↓
     PlayEnv
```

`PreciseAssemblyEnv` kế thừa trực tiếp `PlayEnv`.

Điều này phản ánh thiết kế:

$$
\text{Assembly Environment}
=
\text{Play Environment}
+
\text{Assembly-specific dynamics}
$$

Thay vì xây dựng hoàn toàn một environment mới.

---

## 9.2 Problem Registry

Precise Assembly không hard-code một task duy nhất.

Problem được lấy từ registry:

$$
problem
\rightarrow
PROBLEM\_REGISTRY
\rightarrow
task\ specification
$$

Task specification quyết định:

* insertion object;
* receptive object;
* URDF;
* object scale;
* hole offset;
* insertion pose sequence;
* final insertion pose.

Repository validate `problem` trước khi khởi tạo environment.

---

# 10. Assembly Goal Sequence

## 10.1 Multi-Stage Goal

Một assembly task có thể chứa chuỗi subgoal:

$$
G=
(g_1,g_2,\ldots,g_n)
$$

Policy không nhất thiết đi trực tiếp:

$$
g_0\rightarrow g_n
$$

mà thực hiện:

$$
g_0
\rightarrow
g_1
\rightarrow
\cdots
\rightarrow
g_n
$$

Repository hỗ trợ `finalGoalOnly`, trong đó chỉ sử dụng final insertion pose.

---

## 10.2 Transport Prelude

Với chế độ `transportPreInsertFinal`, repository bổ sung hai waypoint trước insertion:

$$
g_{pre}=
\{
g_{lift},
g_{over-hole}
\}
$$

Sau đó mới thực hiện insertion sequence:

$$
G=
[
g_{lift},
g_{over-hole},
g_1,\ldots,g_n
]
$$

Điều này biến một long-horizon task thành chuỗi các geometric subgoal có cấu trúc.

---

# 11. Four Assembly Tasks

Repository định nghĩa bốn bài toán:

| Task                   | Problem key           |
| ---------------------- | --------------------- |
| Tight insertion        | `tight_insertion`     |
| Beam assembly — step 1 | `beam_assembly_step1` |
| Beam assembly — step 2 | `beam_assembly_step2` |
| Screwing               | `screwing`            |

Tight insertion sử dụng L-peg với tolerance/clearance $0.5,\mathrm{mm}$.

---

# 12. PPO and SAPG

## 12.1 PPO

Repository sử dụng `rl_games` làm RL backend.

PPO tối ưu objective dạng clipped surrogate:

$$
L^{CLIP}(\theta)
=
\mathbb{E}_t
\left[
\min
\left(
r_t(\theta)\hat A_t,
\operatorname{clip}
(r_t(\theta),1-\epsilon,1+\epsilon)
\hat A_t
\right)
\right]
$$

với:

$$
r_t(\theta)
=
\frac{
\pi_\theta(a_t|s_t)
}{
\pi_{\theta_{old}}(a_t|s_t)
}
$$

và $\hat A_t$ là advantage estimate.

---

## 12.2 GAE

Advantage được ước lượng bằng Generalized Advantage Estimation:

$$
\delta_t
=
r_t
+
\gamma V(s_{t+1})
-
V(s_t)
$$

$$
\hat A_t
=
\sum_{l=0}^{T-t-1}
(\gamma\lambda)^l
\delta_{t+l}
$$

Repository cấu hình:

$$
\gamma=0.99
$$

$$
\lambda=0.95
$$

trong training configuration.

---

# 13. SAPG

## 13.1 Role of SAPG

Repository không triển khai SAPG như một RL algorithm hoàn toàn tách biệt khỏi PPO.

Configuration ghi rõ SAPG được kích hoạt trên PPO thông qua các flag trong `a2c_common.py`.

Do đó kiến trúc:

$$
\boxed{
SAPG
=
PPO
+
\text{experience/exploration modifications}
}
$$

thay vì:

$$
SAPG
\neq
PPO
$$

theo nghĩa một implementation algorithm độc lập.

---

## 13.2 SAPG Configuration

Các thành phần SAPG quan trọng trong repository gồm:

$$
use\_others\_experience
$$

$$
off\_policy\_ratio
$$

$$
expl\_type
$$

$$
expl\_reward\_type
$$

$$
expl\_reward\_coef\_embd\_size
$$

$$
expl\_reward\_coef\_scale
$$

$$
expl\_coef\_block\_size
$$

Một constraint implementation quan trọng:

$$
N_{env}\bmod B_{expl}=0
$$

với:

$$
B_{expl}=4096
$$

trong configuration hiện tại.

---

# 14. Policy Architecture

## 14.1 Actor-Critic

Policy sử dụng actor-critic:

$$
\pi_\theta(a|s)
$$

và:

$$
V_\phi(s)
$$

Actor sinh action distribution, critic ước lượng expected return.

---

## 14.2 MLP + LSTM

Backbone trong Play SAPG configuration:

$$
MLP:
[
1024,
1024,
512,
512
]
$$

sau đó có LSTM:

$$
hidden\_size=1024
$$

với một recurrent layer.

Activation:

$$
ELU
$$

Configuration cũng bật layer normalization cho recurrent module.

Kiến trúc khái quát:

```text
Observation
     │
     ▼
  MLP 1024
     │
     ▼
  MLP 1024
     │
     ▼
  MLP 512
     │
     ▼
  MLP 512
     │
     ▼
   LSTM
     │
     ├──────────────► Actor
     │
     └──────────────► Critic
```

---

# 15. Asymmetric Actor-Critic

## 15.1 Motivation

Policy actor chỉ nên sử dụng observation có thể cung cấp trong deployment.

Critic trong simulation có thể sử dụng privileged state.

Do đó:

$$
o_t^{actor}
\subseteq
s_t^{privileged}
$$

Actor:

$$
a_t=\pi_\theta(o_t)
$$

Critic:

$$
V_\phi(s_t^{privileged})
$$

Đây là asymmetric actor-critic.

---

## 15.2 Central Value Network

Configuration chứa:

```text
central_value_config
```

với network riêng:

$$
[1024,1024,512,512]
$$

Repository mô tả rõ `stateList > obsList`, nghĩa là critic nhận state information phong phú hơn actor.

---

# 16. Student Observation and Distillation Path

Repository còn chứa cơ chế student observation.

Có ba observation groups:

$$
\{
policy,
critic,
teacher\_obs
\}
$$

Trong đó:

* `policy`: student observation.
* `critic`: privileged state.
* `teacher_obs`: observation mà frozen state-based teacher sử dụng.

Repository mô tả student có thể kết hợp:

$$
\text{image}
+
\text{proprioception}
$$

trong khi teacher sử dụng state-based observation.

Đây là cơ sở để mở rộng từ state-based simulation policy sang vision-based policy.

---

# 17. Environment Architecture

## 17.1 Isaac Lab DirectRLEnv

`PlayEnv` kế thừa:

```python
DirectRLEnv
```

và phân tách các operation chính:

$$
\begin{aligned}
setup &\rightarrow setup\_scene\\
reset &\rightarrow reset\_env\_state\\
action &\rightarrow apply\_action\_pipeline\\
termination &\rightarrow compute\_terminations\\
reward &\rightarrow compute\_rewards\\
observation &\rightarrow build\_observations
\end{aligned}
$$

---

## 17.2 Simulation Step

Một policy step có cấu trúc:

$$
s_t
\rightarrow
o_t
\rightarrow
\pi_\theta
\rightarrow
a_t
\rightarrow
physics
\rightarrow
s_{t+1}
$$

Trong implementation:

```text
_pre_physics_step
        ↓
apply_action_pipeline
        ↓
physics decimation
        ↓
_apply_action
        ↓
_get_dones
        ↓
_get_rewards
        ↓
_get_observations
```

`_apply_action()` đặt joint position target cho robot.

---

# 18. Training Pipeline

## 18.1 High-Level Architecture

Repository xây dựng training stack:

```text
Hydra Configuration
        │
        ▼
Isaac Lab Environment
        │
        ▼
Gymnasium
        │
        ▼
RlGamesVecEnvWrapper
        │
        ▼
rl_games Runner
        │
        ▼
PPO / SAPG
```

`train.py` trực tiếp mô tả pipeline này và sử dụng `Runner` từ `rl_games`.

---

## 18.2 Configuration Flow

Configuration được hợp nhất theo:

$$
Config
=
ConfigClass
+
TaskYAML
+
HydraCLI
$$

Sau đó environment được tạo:

$$
env
=
gym.make(task\_id,cfg)
$$

và được wrap trước khi truyền cho RL backend.

---

# 19. Vectorized Environment

RL training không chạy một environment duy nhất.

Thay vào đó:

$$
\mathcal{E}
=
\{E_1,E_2,\ldots,E_N\}
$$

với $N$ environment chạy song song.

Observation:

$$
O_t
\in
\mathbb{R}^{N\times D}
$$

Action:

$$
A_t
\in
\mathbb{R}^{N\times29}
$$

Điều này cho phép thu thập lượng lớn experience trên GPU.

Configuration sử dụng:

$$
num\_actors
=
num\_envs
$$

trong RL configuration.

---

# 20. Domain Randomization

Domain randomization là thành phần quan trọng để policy không overfit vào simulator.

Có thể xem training distribution là:

$$
p_{train}(s)
=
\int
p(s|\xi)
p(\xi)
d\xi
$$

trong đó $\xi$ là physical/environment parameters.

Các biến có thể được randomize gồm:

* object state;
* pose;
* observation;
* dynamics;
* goal;
* contact conditions.

Mục tiêu:

$$
\pi_\theta
\text{ robust across }
\xi\sim p(\xi)
$$

thay vì chỉ tối ưu:

$$
\pi_\theta
\text{ for }
\xi=\xi_{sim}
$$

---

# 21. Sim-to-Real

## 21.1 Simulation-to-Real Gap

Policy được train trong simulator:

$$
\pi_{sim}
$$

nhưng deployment trên robot thật yêu cầu:

$$
\pi_{real}
$$

Sai khác:

$$
P_{sim}(s'|s,a)
\neq
P_{real}(s'|s,a)
$$

và:

$$
O_{sim}
\neq
O_{real}
$$

Domain randomization và observation noise được dùng để giảm khoảng cách này.

---

## 21.2 Deployment Interface

Deployment sử dụng một RL player để:

1. load configuration;
2. load checkpoint;
3. khởi tạo recurrent state;
4. nhận observation;
5. thực hiện inference;
6. trả về normalized action.

Repository định nghĩa action space:

$$
a\in[-1,1]^{N_{actions}}
$$

và kiểm tra observation shape:

$$
O\in\mathbb{R}^{B\times N_{obs}}
$$

---

## 21.3 Recurrent State

Do policy sử dụng LSTM, inference phải duy trì hidden state:

$$
h_t,c_t
$$

và:

$$
(h_{t+1},a_t)
=
\pi_\theta(o_t,h_t,c_t)
$$

Do đó deployment không đơn giản là một hàm stateless:

$$
a=f(o)
$$

mà là:

$$
a_t=f(o_t,h_t,c_t)
$$

`rl_player.py` khởi tạo RNN state và hỗ trợ xử lý batch/chunk để duy trì recurrent states.

---

# 22. Evaluation

## 22.1 Interactive Evaluation

Repository cung cấp interactive evaluation bằng Viser.

Mục tiêu:

$$
\pi_\theta
\rightarrow
environment
\rightarrow
visualization
$$

cho phép quan sát trajectory của policy.

---

## 22.2 Offline Success Rate

Offline evaluation chạy nhiều environment song song và tính:

$$
SuccessRate
=
\frac{N_{success}}{N_{episodes}}
$$

Repository đánh giá riêng bốn problem:

$$
\{
tight\_insertion,
beam\_assembly\_step1,
beam\_assembly\_step2,
screwing
\}
$$

---

# 23. Repository Architecture

Cấu trúc logic chính:

```text
play2perfect/
│
├── isaacsimenvs/
│   ├── train.py
│   ├── cfg/
│   └── tasks/
│       ├── play/
│       └── precise_assembly/
│
├── evaluation/
│   ├── problems/
│   ├── eval_isaacsim.py
│   └── eval_offline.py
│
├── rl_games/
│
├── deployment/
│
├── assets/
│   └── urdf/
│
└── docs/
```

README xác định `isaacsimenvs` là training environment, `evaluation` là evaluation layer, `rl_games` là RL backend được vendored, `deployment` là sim-to-real reference và `assets/urdf` chứa robot/task assets.

---

# 24. Code-Level Dependency Graph

## 24.1 Training

```text
train.py
   │
   ├── Hydra
   │
   ├── Isaac Lab
   │      │
   │      └── DirectRLEnv
   │
   ├── Gymnasium
   │
   ├── RlGamesVecEnvWrapper
   │
   └── rl_games.Runner
             │
             └── PPO / SAPG
```

---

## 24.2 Play Environment

```text
PlayEnv
 │
 ├── scene_utils
 ├── reset_utils
 ├── action_utils
 ├── obs_utils
 ├── reward_utils
 ├── termination_utils
 └── logging_utils
```

Thiết kế này tách:

$$
Environment\ orchestration
\neq
Task\ mathematics
$$

`PlayEnv` chủ yếu điều phối lifecycle của Isaac Lab, còn reward, observation, reset và termination được tách thành utility modules.

---

# 25. Mathematical View of the Complete Pipeline

Có thể cô đọng toàn bộ Play2Perfect thành:

$$
\boxed{
\mathcal{D}_{play}
\overset{RL}{\longrightarrow}
\pi_{play}
\overset{finetune}{\longrightarrow}
\pi_{assembly}
}
$$

Trong Stage 1:

$$
\pi_{play}
=
\arg\max_\theta
\mathbb{E}
\left[
\sum_t
\gamma^t
R_{play}(s_t,a_t)
\right]
$$

Trong Stage 2:

$$
\pi_{assembly}
=
\operatorname{Finetune}
(
\pi_{play},
\mathcal{M}_{assembly}
)
$$

với:

$$
R_{assembly}
\approx
R_{precision}
+
R_{contact}
+
R_{progress}
+
R_{success}
$$

Về bản chất, Stage 1 học **manipulation prior**, còn Stage 2 học **task-specific precision**.

---

# 26. Research Perspective

## 26.1 Central Research Hypothesis

Giả thuyết của Play2Perfect có thể biểu diễn:

$$
\text{Dexterous Play Prior}
\Rightarrow
\text{Better Assembly Exploration}
$$

hay:

$$
\mathcal{H}_{play}
\rightarrow
\text{reduced search space}
$$

trong bài toán assembly.

---

## 26.2 Transfer Learning View

Nếu train từ scratch:

$$
\theta_0
\xrightarrow{Assembly\ RL}
\theta_{assembly}
$$

Nếu dùng Play2Perfect:

$$
\theta_0
\xrightarrow{Play\ RL}
\theta_{play}
\xrightarrow{Assembly\ RL}
\theta_{assembly}
$$

Vì $\theta_{play}$ đã encode manipulation priors, Stage 2 không cần khám phá lại toàn bộ skill space.

Paper báo cáo play-pretrained prior đạt sample efficiency cao hơn đáng kể so với RL từ scratch và đạt sim-to-real success trên tight insertion cùng các task assembly dài hơn.

---

# 27. Những thành phần cần tập trung khi nghiên cứu

## 27.1 Trọng tâm 1 — Play Pretraining

Cần hiểu:

$$
\text{Object Diversity}
+
\text{Goal Diversity}
+
\text{Trajectory Diversity}
$$

và cách chúng ảnh hưởng đến manipulation prior.

---

## 27.2 Trọng tâm 2 — Reward Decomposition

Đây là phần quan trọng để hiểu policy học như thế nào:

$$
R
=
R_{lift}
+
R_{fingertip}
+
R_{keypoint}
+
R_{penalty}
+
R_{success}
$$

Không nên xem reward là một scalar đơn giản; nó được thiết kế theo từng phase của manipulation.

---

## 27.3 Trọng tâm 3 — Geometric Representation

Đặc biệt cần hiểu:

$$
p,\quad q,\quad K,\quad d_K
$$

và transformation:

$$
k^{world}
=
p+Rk^{local}
$$

vì precise assembly phụ thuộc trực tiếp vào geometric alignment.

---

## 27.4 Trọng tâm 4 — PPO/SAPG

Cần nắm:

$$
\pi_\theta(a|s)
$$

$$
\hat A_t
$$

$$
L^{CLIP}
$$

và cách SAPG được overlay lên PPO trong implementation hiện tại.

---

## 27.5 Trọng tâm 5 — Asymmetric Actor-Critic

Phân biệt:

$$
o_t^{actor}
$$

và:

$$
s_t^{critic}
$$

để hiểu vì sao simulator có thể cung cấp privileged information cho critic mà không đưa trực tiếp cho deployed actor.

---

## 27.6 Trọng tâm 6 — Sim-to-Real

Cuối cùng cần nối:

$$
Domain\ Randomization
+
Observation\ Noise
+
Observation\ Delay
+
Robust\ Policy
\rightarrow
Sim2Real
$$

đây là cầu nối giữa RL trong simulator và robot thực.

---

# 28. Summary

Play2Perfect không đơn thuần là một implementation của PPO cho robotic assembly.

Cấu trúc nghiên cứu cốt lõi là:

$$
\boxed{
\text{Learn to Play}
\rightarrow
\text{Acquire Manipulation Prior}
\rightarrow
\text{Finetune for Precision}
}
$$

Toàn bộ hệ thống có thể nhìn dưới năm tầng:

```text
                 Play2Perfect
                      │
          ┌───────────┴───────────┐
          │                       │
    Play Pretraining       Precise Assembly
          │                       │
          └───────────┬───────────┘
                      │
               PPO / SAPG
                      │
             Isaac Lab / PhysX
                      │
                Sim-to-Real
```

Điểm cần ghi nhớ nhất:

1. **Play không phải assembly thu nhỏ**; nó là quá trình học manipulation priors tổng quát.
2. **Finetuning** chuyển prior đó sang contact-rich precision task.
3. **Keypoint geometry** là biểu diễn quan trọng cho precise alignment.
4. **Reward decomposition** tạo curriculum tự nhiên từ grasp/lift → alignment → success.
5. **PPO + SAPG** là RL optimization backbone của repository.
6. **Asymmetric critic** cho phép critic dùng privileged state trong simulation.
7. **Domain randomization + observation perturbation** hướng policy tới robustness.
8. **LSTM** khiến policy mang tính temporal và deployment phải duy trì recurrent state.
9. Kiến trúc code tách rõ **environment orchestration**, **task mathematics**, **RL backend**, **evaluation** và **deployment**.
10. Về mặt nghiên cứu, đóng góp trung tâm là chứng minh rằng **pretraining bằng dexterous play có thể tạo ra manipulation prior giúp RL giải quyết precise assembly hiệu quả hơn**.

## References

* [Play2Perfect — GitHub Repository](https://github.com/kushal2000/play2perfect?utm_source=chatgpt.com)
* [Play2Perfect — arXiv Paper](https://arxiv.org/abs/2606.26428?utm_source=chatgpt.com)
* [rl_games](https://github.com/Denys88/rl_games?utm_source=chatgpt.com)
* [SAPG](https://sapg-rl.github.io/?utm_source=chatgpt.com)
* [SimToolReal](https://github.com/tylerlum/simtoolreal?utm_source=chatgpt.com)
