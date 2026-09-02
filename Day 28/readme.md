Phần **Load Balancer** trong [System Design Primer – GitHub](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com) là một thành phần trung tâm của kiến trúc hệ thống có khả năng **scale-out**. GitHub tổ chức phần này theo chuỗi:

> **Load Balancer → Active-Passive / Active-Active → Layer 4 → Layer 7 → Horizontal Scaling → Trade-offs**

Cấu trúc này rất hợp lý để học System Design vì nó đi từ **vai trò → cơ chế phân phối → mức mạng → mức ứng dụng → khả năng mở rộng → nhược điểm**. ([GitHub][1])

Dưới đây là phần phân tích theo đúng tinh thần và cấu trúc của GitHub, nhưng bổ sung phần **cơ chế, mô hình toán học và trade-off** để dùng cho báo cáo học thuật.

---

# Load Balancer

## 1. Tổng quan

[Load balancer trong System Design Primer](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com#load-balancer)

**Load Balancer (LB)** là thành phần trung gian nhận các request từ client và phân phối chúng đến một hoặc nhiều backend server.

Kiến trúc cơ bản:

```text
                    ┌──────────────┐
                    │   Clients    │
                    └──────┬───────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Load Balancer   │
                  └───────┬─────────┘
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
        ┌─────────┐  ┌─────────┐  ┌─────────┐
        │ Server 1│  │ Server 2│  │ Server 3│
        └─────────┘  └─────────┘  └─────────┘
```

Thay vì:

```text
Client ───────────────► Server
```

ta có:

```text
Client ──► Load Balancer ──► Server
```

Điều này cho phép hệ thống có nhiều server xử lý cùng một loại workload.

Giả sử có $N$ server:

$$
S=\{S_1,S_2,\ldots,S_N\}
$$

và một tập request:

$$
R=\{R_1,R_2,\ldots,R_M\}.
$$

Load balancer thực hiện một hàm phân phối:

$$
f:R\rightarrow S
$$

sao cho mỗi request $R_i$ được ánh xạ tới một server:

$$
f(R_i)=S_j.
$$

Mục tiêu không đơn giản chỉ là "chia đều request", mà là **phân phối tải sao cho hệ thống đạt throughput cao, latency thấp và availability cao**.

---

## 2. Tại sao cần Load Balancer?

Tác giả nêu ba lợi ích chính:

* tránh gửi request đến server không khỏe;
* tránh overload;
* giúp loại bỏ single point of failure. ([GitHub][1])

Có thể hiểu thành ba vấn đề lớn.

### 2.1. Health-aware routing

Giả sử có:

```text
              Load Balancer
              /     |      \
             ▼      ▼       ▼
           S1      S2       S3
          healthy  DOWN    healthy
```

Nếu không có LB:

$$
P(R\rightarrow S_2) \gt 0
$$

thì request có thể được gửi đến server đang lỗi.

LB duy trì **health check** để xác định trạng thái backend:

$$
Health(S_i)\in\{healthy, unhealthy\}.
$$

Chỉ những server thỏa:

$$
Health(S_i)=healthy
$$

mới được đưa vào tập backend khả dụng.

Do đó:

$$
S_{available}
=
\{S_i\mid Health(S_i)=healthy\}.
$$

Request chỉ được phân phối trong:

$$
R_i\rightarrow S_j,\qquad S_j\in S_{available}.
$$

Đây là một trong những cơ chế quan trọng để tăng **availability**.

---

## 3. Load Balancing và Overload Prevention

Giả sử tổng request rate là: $\lambda$ và có $N$ backend server. Nếu phân phối tương đối đều, request rate trung bình mỗi server là:

$$
\lambda_i\approx\frac{\lambda}{N}.
$$

Ví dụ:

$$
\lambda=10,000\ requests/s
$$

với:

$$
N=10
$$

thì:

$$
\lambda_i\approx1,000\ requests/s.
$$

Nếu một server chỉ xử lý được:

$$
\mu=1,500\ requests/s
$$

thì hệ thống vẫn còn capacity.

Nhưng nếu toàn bộ traffic dồn vào một server:

$$
\lambda_1=10,000
$$

thì:

$$
\lambda_1 \gt \mu
$$

và server có thể bị overload.

Load balancer vì vậy trở thành một **control point** để phân phối workload.

---

## 4. Load Balancer không đồng nghĩa với "chia đều"

Đây là điểm rất quan trọng khi học System Design.

Một LB tốt không nhất thiết phải làm:

$$
Load(S_1)=Load(S_2)=\cdots=Load(S_N).
$$

Bởi vì các server có thể có capacity khác nhau.

Ví dụ:

```text
Server A: 4 CPU
Server B: 8 CPU
Server C: 16 CPU
```

Nếu dùng round robin:

```text
A → B → C → A → B → C
```

thì workload không phản ánh capacity thực tế.

Trong trường hợp đó có thể sử dụng **weighted round robin**:

$$
w_A:w_B:w_C=1:2:4.
$$

Khi đó traffic có thể được phân phối gần:

$$
\frac{1}{7},\frac{2}{7},\frac{4}{7}.
$$

Do đó, "load balancing" nên được hiểu là:

> **phân phối workload phù hợp với trạng thái và capacity của backend**, không đơn thuần là chia đều request.

GitHub liệt kê nhiều chiến lược như random, least loaded, session/cookies, round robin, weighted round robin, Layer 4 và Layer 7. ([GitHub][2])

---

## 5. Các chiến lược phân phối traffic

### 5.1. Random

Chọn server ngẫu nhiên:

$$
P(S_i)=\frac{1}{N}.
$$

Ưu điểm:

* đơn giản;
* dễ triển khai.

Nhược điểm:

* không phản ánh current load;
* có thể xảy ra imbalance trong khoảng thời gian ngắn.

---

### 5.2. Round Robin

Các request lần lượt được gửi đến:

```text
S1 → S2 → S3 → S1 → S2 → S3 → ...
```

Nếu có $N$ server thì request thứ $k$ có thể được ánh xạ:

$$
f(k)=S_{(k\bmod N)+1}.
$$

Ưu điểm:

* đơn giản;
* deterministic;
* overhead thấp.

Nhược điểm:

* giả định các server có capacity tương đương;
* không quan tâm server nào đang bận.

---

### 5.3. Weighted Round Robin

Mỗi server có trọng số:

$$
w_i>0.
$$

Traffic được phân phối theo:

$$
P(S_i)\approx
\frac{w_i}{\sum_{j=1}^{N}w_j}.
$$

Ví dụ:

$$
w_1=1,\qquad w_2=2,\qquad w_3=3.
$$

thì tỷ lệ traffic xấp xỉ:

$$
S_1:S_2:S_3=1:2:3.
$$

Phù hợp khi backend có capacity khác nhau.

---

### 5.4. Least Loaded

LB gửi request đến server đang ít tải nhất.

Có thể định nghĩa:

$$
S^*=
\arg\min_{S_i\in S_{available}} Load(S_i).
$$

Trong đó `Load` có thể dựa trên:

* active connections;
* CPU;
* memory;
* request queue;
* latency;
* hoặc một combination của các metric.

Đây thường là chiến lược thông minh hơn round robin nhưng yêu cầu LB có thông tin về trạng thái backend.

---

## 6. SSL Termination

GitHub cũng đề cập đến **SSL termination** như một lợi ích của load balancer. ([GitHub][1])

Không có LB:

```text
Client
   │ HTTPS
   ▼
Server 1
   │ TLS decryption
   ▼
Application
```

Nếu có nhiều server:

```text
Client
   │ HTTPS
   ▼
Load Balancer
   │ TLS termination
   ├──────────► Server 1
   ├──────────► Server 2
   └──────────► Server 3
```

LB xử lý TLS handshake và giải mã request.

Ta có:

$$
C_{TLS}=C_{handshake}+C_{encryption/decryption}.
$$

Nếu backend tự xử lý TLS, tổng chi phí trên $N$ server là:

$$
C_{total}
=
\sum_{i=1}^{N}C_{TLS,i}.
$$

Khi termination tại LB, phần TLS có thể được tập trung tại:

$$
C_{total}\approx C_{TLS,LB}.
$$

Điều này giúp backend tập trung vào application workload.

Ngoài ra, certificate có thể được quản lý tập trung thay vì phải cài đặt X.509 certificate trên từng backend server.

### Tuy nhiên

SSL termination **không có nghĩa backend bắt buộc phải dùng HTTP plaintext**.

Một kiến trúc production có thể là:

```text
Client
  │ HTTPS
  ▼
Load Balancer
  │ HTTPS
  ▼
Backend
```

tức là TLS được terminate tại LB rồi **re-encrypt** khi kết nối tới backend.

Điều này đặc biệt quan trọng khi traffic đi qua các network boundary không hoàn toàn trusted.

---

## 7. Session Persistence

Một vấn đề khác là **session persistence**, còn gọi là **sticky session**.

Ví dụ:

```text
Client A
   │
   ▼
Load Balancer
   │
   └──────► Server 1
```

Nếu request tiếp theo của Client A lại đi tới Server 2:

```text
Client A
   │
   ▼
Load Balancer
   │
   └──────► Server 2
```

thì session có thể bị mất nếu session chỉ nằm trong memory của Server 1.

Một giải pháp là sticky session:

$$
Client_A\rightarrow S_1
$$

và các request sau vẫn được route đến:

$$
R_A^{(1)},R_A^{(2)},\ldots,R_A^{(k)}
\rightarrow S_1.
$$

Có thể sử dụng cookie để LB xác định backend tương ứng.

---

## 8. Sticky Session vs Stateless Architecture

Tuy nhiên, trong kiến trúc scale lớn, **stateless application** thường được ưu tiên hơn.

Thay vì:

```text
Server 1
 └── Session A

Server 2
 └── Session B
```

ta đưa session ra ngoài:

```text
             ┌──────────────┐
             │    Redis     │
             │   Sessions   │
             └──────┬───────┘
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
        Server 1  Server 2  Server 3
```

Khi đó:

$$
Session(User)
\notin Memory(Server_i)
$$

mà:

$$
Session(User)\in CentralStore.
$$

Điều này cho phép:

$$
Request(User)\rightarrow S_i
$$

với bất kỳ backend healthy nào.

Đây chính là mối liên hệ giữa **load balancing → horizontal scaling → stateless architecture** mà GitHub nhấn mạnh. ([GitHub][2])

---

## 9. High Availability của Load Balancer

Một sai lầm phổ biến là:

```text
Client
   │
   ▼
Load Balancer
   │
 ┌─┼─┐
 ▼ ▼ ▼
S1 S2 S3
```

Nếu LB chết:

$$
Failure(LB)\Rightarrow Failure(System)
$$

Mặc dù backend vẫn hoạt động.

Khi đó LB trở thành:

> **Single Point of Failure (SPOF)**.

GitHub giải quyết vấn đề này bằng cách triển khai nhiều load balancer theo hai mô hình chính:

* **Active-Passive**
* **Active-Active** ([GitHub][1])

---

## 10. Active-Passive

```text
                 Client
                    │
                    ▼
             ┌────────────┐
             │ LB Primary │
             └──────┬─────┘
                    │
              ┌─────┴─────┐
              ▼           ▼
             S1           S2

             LB Secondary
                 standby
```

LB Primary xử lý traffic.

LB Secondary ở trạng thái standby.

Nếu:

$$
Failure(LB_{primary})=true
$$

thì hệ thống chuyển sang:

$$
LB_{secondary}.
$$

### Ưu điểm

* đơn giản hơn active-active;
* dễ reasoning;
* failover rõ ràng.

### Nhược điểm

Một phần capacity bị idle trong trạng thái bình thường.

---

## 11. Active-Active

```text
                  Client
                 /      \
                ▼        ▼
             LB 1       LB 2
              │           │
              └─────┬─────┘
                    │
             ┌──────┼──────┐
             ▼      ▼      ▼
            S1     S2     S3
```

Cả hai LB đều xử lý traffic.

Nếu một LB chết:

$$
Traffic(LB_1)\rightarrow LB_2.
$$

### Ưu điểm

* sử dụng tài nguyên tốt hơn;
* capacity lớn hơn;
* failover nhanh nếu thiết kế đúng.

### Nhược điểm

* routing phức tạp hơn;
* cần cơ chế health checking/failover;
* cần tránh split-brain hoặc traffic imbalance.

---

## 12. Layer 4 Load Balancing

[Layer 4 Load Balancing – GitHub](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com#layer-4-load-balancing)

Layer 4 tương ứng với **Transport Layer** trong mô hình TCP/IP/OSI.

LB chủ yếu quan tâm đến thông tin như:

```text
Source IP
Destination IP
Source Port
Destination Port
Protocol
```

GitHub mô tả L4 LB là loại dựa trên thông tin transport layer, thay vì nội dung application message. ([GitHub][2])

Ví dụ:

```text
Client
10.0.0.10:50000
        │
        │ TCP
        ▼
10.0.0.100:443
        │
        ▼
Load Balancer
        │
        ├──────► 10.0.1.10:443
        │
        ├──────► 10.0.1.11:443
        │
        └──────► 10.0.1.12:443
```

L4 không cần hiểu:

```text
GET /video
POST /payment
Cookie: session=...
```

Nó chủ yếu xử lý connection/packet-level information.

---

## 13. Tại sao L4 nhanh?

L4 không cần parse application payload.

Do đó processing có thể được mô hình hóa đơn giản:

$$
Cost_{L4}
\approx
Cost_{network}
+
Cost_{connection}
$$

trong khi L7 cần thêm:

$$
Cost_{L7}
\approx
Cost_{network}
+
Cost_{connection}
+
Cost_{TLS}
+
Cost_{HTTP\ parsing}
+
Cost_{routing}.
$$

Vì vậy:

$$
Cost_{L4} \lt Cost_{L7}
$$

trong nhiều trường hợp.

GitHub cũng nhấn mạnh L4 thường cần ít thời gian và computing resources hơn L7, mặc dù trên commodity hardware hiện đại, chênh lệch hiệu năng có thể không lớn. ([GitHub][1])

---

## 14. Layer 7 Load Balancing

[Layer 7 Load Balancing – GitHub](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com#layer-7-load-balancing)

Layer 7 tương ứng với **Application Layer**.

Điểm khác biệt quan trọng:

> **L7 LB hiểu application protocol và nội dung request ở mức cao hơn.**

Ví dụ HTTP request:

```http
GET /videos/123
Host: example.com
Cookie: session=abc
```

L7 LB có thể nhìn thấy:

```text
Path      = /videos/123
Host      = example.com
Cookie    = session=abc
Method    = GET
```

và đưa ra routing decision.

---

## 15. Ví dụ routing ở Layer 7

Giả sử hệ thống có:

```text
/videos/*    → Video Servers
/payment/*   → Payment Servers
/api/*       → API Servers
```

Ta có:

$$
f(request)=
\begin{cases}
VideoCluster, & path\in /videos/*\\
PaymentCluster, & path\in /payment/*\\
APICluster, & path\in /api/*
\end{cases}
$$

Kiến trúc:

```text
                         ┌───────────────┐
                         │ L7 Load       │
                         │ Balancer      │
                         └───────┬───────┘
                                 │
             ┌───────────────────┼───────────────────┐
             ▼                   ▼                   ▼
       /videos/*            /payment/*            /api/*
             │                   │                   │
             ▼                   ▼                   ▼
      Video Cluster       Payment Cluster        API Cluster
```

Đây là lý do L7 có **flexibility** cao hơn L4.

---

## 16. L4 vs L7

| Đặc điểm            | Layer 4            | Layer 7                              |
| ------------------- | ------------------ | ------------------------------------ |
| Layer               | Transport          | Application                          |
| Quan sát            | IP, port, protocol | HTTP headers, path, cookies, message |
| Hiểu HTTP           | Không cần          | Có                                   |
| Routing theo URL    | Không              | Có                                   |
| Routing theo cookie | Không ở mức HTTP   | Có                                   |
| Processing          | Thấp hơn           | Cao hơn                              |
| Flexibility         | Thấp hơn           | Cao hơn                              |
| Use case            | TCP/UDP traffic    | HTTP/API/microservices               |

Có thể tóm tắt:

$$
L4
\Rightarrow
Fast,\ Low\ overhead
$$

trong khi:

$$
L7
\Rightarrow
Flexible,\ Application-aware.
$$

Không nên hiểu rằng **L4 luôn tốt hơn L7**. Đây là trade-off:

$$
Flexibility
\longleftrightarrow
Processing\ Cost.
$$

---

## 17. Horizontal Scaling

[Horizontal Scaling – GitHub](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com#horizontal-scaling)

Đây là phần quan trọng nhất về mặt System Design.

Có hai cách scale:

### Vertical Scaling

Tăng capacity của một server:

$$
S_1
\rightarrow
S_1'
$$

Ví dụ:

```text
8 CPU → 32 CPU
32 GB RAM → 128 GB RAM
```

### Horizontal Scaling

Thêm nhiều server:

$$
S_1
\rightarrow
\{S_1,S_2,\ldots,S_N\}.
$$

GitHub nhấn mạnh load balancer giúp hệ thống scale-out bằng cách phân phối traffic giữa các commodity machines. ([GitHub][1])

---

## 18. Vì sao Load Balancer là nền tảng của Horizontal Scaling?

Không có LB:

```text
Client
   │
   ▼
Server
```

Thêm server:

```text
             ┌──► Server 1
Client ──────┼──► Server 2
             └──► Server 3
```

Client phải biết server nào cần gọi.

Có LB:

```text
                   ┌──► Server 1
                   │
Client ──► LB ─────┼──► Server 2
                   │
                   └──► Server 3
```

Client chỉ cần biết:

$$
Client\rightarrow LB
$$

LB chịu trách nhiệm:

$$
LB\rightarrow S_i.
$$

Do đó backend có thể tăng từ:

$$
N=3
$$

lên:

$$
N=100
$$

mà client không cần biết topology bên trong.

---

## 19. Capacity của hệ thống khi Scale Out

Giả sử mỗi server có capacity:

$$
C
$$

và có $N$ server.

Nếu workload có thể scale gần tuyến tính:

$$
C_{total}\approx N\times C.
$$

Ví dụ:

$$
C=1,000\ requests/s
$$

và:

$$
N=10
$$

thì theoretical capacity:

$$
C_{total}\approx10,000\ requests/s.
$$

Nhưng production thường không đạt scaling tuyến tính hoàn hảo vì còn:

* load balancer;
* database;
* cache;
* network;
* synchronization;
* connection limits;
* lock contention.

Do đó:

$$
C_{real} \lt N\times C.
$$

Đây chính là lý do GitHub nhấn mạnh rằng khi scale upstream servers, downstream components như cache và database cũng phải xử lý nhiều simultaneous connections hơn. ([GitHub][2])

---

## 20. Stateless Server

Horizontal scaling dẫn đến một nguyên tắc rất quan trọng:

> **Backend application server nên càng stateless càng tốt.**

Không nên:

```text
Server 1
 ├── Session A
 ├── Session B
 └── User data
```

vì khi server chết:

$$
Failure(S_1)
\Rightarrow
Loss(Session_A,Session_B).
$$

Thay vào đó:

```text
                 Redis / Database
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
     Server 1       Server 2       Server 3
```

Các server trở thành những worker tương đối interchangeable:

$$
S_1\approx S_2\approx S_3.
$$

Đây là một trong những điều kiện giúp horizontal scaling hoạt động hiệu quả.

---

## 21. Nhược điểm của Horizontal Scaling

GitHub chỉ ra hai vấn đề lớn: complexity và downstream load. ([GitHub][2])

Khi:

$$
N_{server}\uparrow
$$

thì không chỉ application capacity tăng mà số connection tới downstream services cũng có thể tăng:

$$
Connections_{DB}\uparrow
$$

và:

$$
Connections_{Cache}\uparrow.
$$

Ví dụ:

```text
        Load Balancer
              │
     ┌────────┼────────┐
     ▼        ▼        ▼
    App1     App2     App3
     │        │        │
     └────────┼────────┘
              ▼
          Database
```

Nếu từ 3 application servers tăng lên 100:

```text
App1
App2
App3
...
App100
   │
   ▼
Database
```

database có thể trở thành bottleneck mới.

Do đó:

$$
Scale(App)
\not\Rightarrow
Scale(System).
$$

Đây là một insight cực kỳ quan trọng trong System Design.

---

## 22. Nhược điểm của Load Balancer

GitHub chỉ ra ba trade-off chính:

1. LB có thể trở thành performance bottleneck.
2. LB làm kiến trúc phức tạp hơn.
3. Một LB duy nhất lại chính là SPOF. ([GitHub][1])

Có thể biểu diễn:

$$
Traffic_{system}
\rightarrow LB
\rightarrow Backend.
$$

Nếu capacity của LB là:

$$
C_{LB}
$$

và traffic:

$$
\lambda \gt C_{LB}
$$

thì dù backend có capacity rất lớn:

$$
C_{backend}\gg C_{LB},
$$

toàn hệ thống vẫn bị giới hạn bởi:

$$
C_{system}\approx C_{LB}.
$$

LB trở thành **bottleneck**.

---

## 23. Load Balancer không loại bỏ bottleneck — nó di chuyển bottleneck

Đây là cách tư duy tốt hơn khi học System Design.

Ban đầu:

```text
Client → App Server
```

App Server là bottleneck:

$$
Bottleneck=App.
$$

Thêm LB:

```text
Client → LB → App1
             App2
             App3
```

App capacity tăng, nhưng có thể xuất hiện:

$$
Bottleneck=LB.
$$

Sau đó scale LB:

```text
Client
  │
  ├──► LB1 ──► App Cluster
  │
  └──► LB2 ──► App Cluster
```

lúc này database có thể trở thành:

$$
Bottleneck=Database.
$$

Vì vậy System Design là quá trình liên tục:

$$
Identify\ Bottleneck
\rightarrow
Scale
\rightarrow
New\ Bottleneck
\rightarrow
Scale.
$$

Đây cũng phù hợp với triết lý của System Design Primer rằng khi scale hệ thống cần xác định bottleneck và giải quyết nó bằng các pattern phù hợp. ([GitHub][1])

---

## 24. Tổng hợp kiến trúc

Một hệ thống web production có thể tiến hóa:

### Bước 1 — Single Server

```text
Client
  │
  ▼
Server
```

### Bước 2 — Load Balancer

```text
Client
  │
  ▼
LB
  │
  ▼
Server
```

### Bước 3 — Horizontal Scaling

```text
             ┌──► App 1
Client ──► LB├──► App 2
             └──► App 3
```

### Bước 4 — Stateless + Shared State

```text
                    ┌──► App 1 ──┐
                    ├──► App 2 ──┼──► Redis
Client ──► LB ──────┤             └──► DB
                    └──► App 3
```

### Bước 5 — High Availability

```text
                       ┌──► LB 1 ──┐
Client ────────────────┤           ├──► App Cluster
                       └──► LB 2 ──┘
```

Từ đó ta có:

$$
High\ Availability
+
Horizontal\ Scaling
+
Stateless\ Application
+
Shared\ State
$$

là nền tảng của một kiến trúc web có khả năng scale tốt.

---

## 25. Những trade-off cần nhớ

| Quyết định         | Lợi ích                       | Chi phí                      |
| ------------------ | ----------------------------- | ---------------------------- |
| Load Balancer      | Scale + availability          | Complexity                   |
| L4                 | Fast, low overhead            | Ít application awareness     |
| L7                 | Flexible routing              | Processing overhead          |
| Round Robin        | Đơn giản                      | Không biết current load      |
| Weighted RR        | Phù hợp heterogeneous servers | Cần quản lý weight           |
| Least Loaded       | Load distribution tốt         | Cần monitoring/state         |
| Sticky Session     | Giữ session đơn giản          | Giảm flexibility khi scale   |
| Stateless          | Scale dễ                      | Cần external state store     |
| Active-Passive     | Đơn giản                      | Standby capacity bị lãng phí |
| Active-Active      | Tận dụng resource tốt         | Complexity cao               |
| SSL Termination    | Centralized TLS               | LB cần xử lý TLS             |
| Horizontal Scaling | Capacity + availability       | Downstream complexity        |

---

## 26. Mental model cần nhớ

Nếu học phần này để **System Design interview**, có thể ghi nhớ theo chuỗi:

```text
                 LOAD BALANCER
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Routing       Health       Scaling
          │            │            │
          ▼            ▼            ▼
   Round Robin      Health Check   Horizontal
   Least Loaded                    Scaling
   Weighted RR                         │
                                       ▼
                                  Stateless App
                                       │
                                  ┌────┴────┐
                                  ▼         ▼
                                Cache       DB
```

Và câu hỏi quan trọng nhất không phải:

> "Load Balancer là gì?"

mà là:

> **"Tại sao hệ thống cần Load Balancer, nó giải quyết bottleneck nào, và bottleneck tiếp theo sẽ xuất hiện ở đâu?"**

Có thể quy về:

$$
\boxed{
Client
\rightarrow
Load\ Balancer
\rightarrow
Stateless\ Application
\rightarrow
Cache
\rightarrow
Database
}
$$

với HA:

$$
\boxed{
Multiple\ Load\ Balancers
+
Multiple\ Application\ Servers
+
Replicated\ Dependencies
}
$$

---

## Liên kết học theo đúng cấu trúc GitHub

GitHub hiện vẫn tổ chức `Load balancer` cùng các nhánh **Active-passive, Active-active, Layer 4, Layer 7 và Horizontal scaling** trong phần index của repository. ([GitHub][1])

* [System Design Primer – README chính](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com)
* [Load Balancer](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com#load-balancer)
* [Active-Passive](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com#active-passive)
* [Active-Active](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com#active-active)
* [Layer 4 Load Balancing](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com#layer-4-load-balancing)
* [Layer 7 Load Balancing](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com#layer-7-load-balancing)
* [Horizontal Scaling](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com#horizontal-scaling)
* [Load Balancer vs Reverse Proxy](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com#load-balancer-vs-reverse-proxy)

[1]: https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com "GitHub - donnemartin/system-design-primer: Learn how to design large-scale systems. Prep for the system design interview. Includes Anki flashcards. · GitHub"
[2]: https://github.com/donnemartin/system-design-primer/blob/master/README.md?plain=1&utm_source=chatgpt.com "system-design-primer/README.md at master · donnemartin/system-design-primer · GitHub"
