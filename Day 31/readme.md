# Application Layer

> **Nguồn chính:** [System Design Primer — Application Layer](https://github.com/donnemartin/system-design-primer#application-layer)
>
> **Nguồn bổ sung:** [Intro to Architecting Systems for Scale — Platform Layer](https://lethain.com/introduction-to-architecting-systems-for-scale/#platform_layer)

---

## 1. Tổng quan

Trong một hệ thống web đơn giản, web server có thể đồng thời đảm nhiệm việc tiếp nhận HTTP request và thực thi business logic:

```text
Client
   |
   v
Web Server
   |
   v
Database
```

![](img/yB5SYwm.png)

Khi hệ thống phát triển, việc đặt toàn bộ business logic trên web server tạo ra sự phụ thuộc giữa khả năng xử lý HTTP và khả năng xử lý ứng dụng. Một giải pháp là tách **Web Layer** khỏi **Application Layer**, còn được gọi là **Platform Layer**.

Kiến trúc tổng quát:

```text
Client
   |
   v
+-------------------+
|    Web Layer      |
|                   |
| HTTP / Routing    |
| Reverse Proxy     |
| Load Balancing    |
+---------+---------+
          |
          v
+-------------------+
| Application Layer |
|                   |
| Business Logic    |
| APIs              |
| Services          |
| Workers           |
+---------+---------+
          |
          v
+-------------------+
|    Data Layer     |
|                   |
| Database          |
| Cache             |
| Storage           |
+-------------------+
```

Mục tiêu chính của Application Layer là **tách business logic khỏi tầng web**, cho phép các thành phần được phát triển, cấu hình và mở rộng tương đối độc lập.

---

## 2. Web Layer và Application Layer

### 2.1. Separation of Responsibilities

Web Layer chủ yếu chịu trách nhiệm về giao tiếp với client:

$$
\text{Web Layer}
=
\{
\text{HTTP},
\text{Routing},
\text{TLS},
\text{Proxy},
\text{Load Balancing}
\}
$$

Application Layer chịu trách nhiệm thực thi logic của hệ thống:

$$
\text{Application Layer}
=
\{
\text{Business Logic},
\text{API Logic},
\text{Domain Logic},
\text{Background Processing}
\}
$$

Việc phân tách này giúp tránh việc một server phải đồng thời xử lý quá nhiều loại workload.

---

### 2.2. Independent Scaling

Một lợi ích quan trọng của Application Layer là cho phép Web Layer và Application Layer được **scale độc lập**.

Giả sử:

$$
N_W = \text{số lượng Web Servers}
$$

và:

$$
N_A = \text{số lượng Application Servers}
$$

Trong kiến trúc tách biệt:

$$
N_W \neq N_A
$$

Ví dụ:

```text
                Load Balancer
                      |
        +-------------+-------------+
        |             |             |
      Web 1         Web 2         Web 3
        |             |             |
        +-------------+-------------+
                      |
                      v
              Application Layer
                      |
        +-------------+-------------+
        |             |             |
      App 1         App 2         App 3
```

Nếu số lượng HTTP requests tăng, có thể tăng:

$$
N_W \rightarrow N_W + \Delta W
$$

mà không nhất thiết phải tăng Application Servers.

Ngược lại, nếu business logic trở thành bottleneck:

$$
N_A \rightarrow N_A + \Delta A
$$

mà không cần mở rộng Web Layer theo cùng tỷ lệ.

Do đó:

$$
\boxed{
\text{Web Scaling}
\perp
\text{Application Scaling}
}
$$

ở mức độ kiến trúc.

---

## 3. Application Servers

Application servers thực thi các logic nghiệp vụ phía sau Web Layer.

Ví dụ một hệ thống mạng xã hội có thể có:

```text
Application Layer
│
├── User
├── Follower
├── Feed
├── Search
├── Photo Upload
└── Notification
```

Mỗi thành phần có thể chịu trách nhiệm cho một business capability cụ thể.

Ví dụ:

$$
\text{User Service}
\rightarrow
\text{user profile}
$$

$$
\text{Feed Service}
\rightarrow
\text{news feed}
$$

$$
\text{Search Service}
\rightarrow
\text{search}
$$

$$
\text{Photo Service}
\rightarrow
\text{photo upload}
$$

Cách phân tách này tạo nền tảng cho kiến trúc **microservices**.

---

## 4. Single Responsibility Principle

Application Layer thường được thiết kế theo tư tưởng **Single Responsibility Principle (SRP)**.

Thay vì một application server khổng lồ:

```text
+--------------------------------+
|       Monolithic App           |
|                                |
| User                           |
| Feed                           |
| Search                         |
| Photo                          |
| Notification                   |
| Recommendation                 |
+--------------------------------+
```

có thể chia thành các service:

```text
+-------------+
| User        |
+-------------+

+-------------+
| Feed        |
+-------------+

+-------------+
| Search      |
+-------------+

+-------------+
| Photo       |
+-------------+

+-------------+
| Notification|
+-------------+
```

Mỗi service có một responsibility tương đối rõ ràng.

Tuy nhiên, SRP không có nghĩa là phải chia hệ thống thành càng nhiều service càng tốt.

Mục tiêu là xác định **ranh giới nghiệp vụ hợp lý**:

$$
\boxed{
\text{Service Boundary}
\approx
\text{Business Capability}
}
$$

---

## 5. Asynchronism

Application Layer cũng là nơi thường triển khai các **workers** để xử lý các tác vụ bất đồng bộ.

Không phải mọi công việc đều cần được hoàn thành trong request-response cycle.

Ví dụ user upload một ảnh:

```text
Client
   |
   v
Photo API
   |
   +------> Store Metadata
   |
   +------> Message Queue
                 |
                 v
            Image Worker
                 |
          +------+------+
          |             |
       Resize        Compress
          |             |
          +------+------+
                 |
                 v
              Storage
```

Thay vì:

```text
Request
   |
   +-- Upload
   +-- Resize
   +-- Compress
   +-- Generate Thumbnail
   |
   v
Response
```

hệ thống có thể trả response sau khi task được đưa vào queue:

$$
\text{Request}
\rightarrow
\text{Queue}
\rightarrow
\text{Worker}
\rightarrow
\text{Result}
$$

Khi đó thời gian response có thể gần với:

$$
T_{\text{response}}
\approx
T_{\text{enqueue}}
$$

thay vì:

$$
T_{\text{response}}
=
T_{\text{upload}}
+
T_{\text{resize}}
+
T_{\text{compress}}
+
T_{\text{thumbnail}}
$$

Điều này giúp giảm latency của request và cho phép workload nặng được xử lý độc lập.

---

## 6. Microservices

### 6.1. Định nghĩa

**Microservices** là kiến trúc trong đó một application được tổ chức thành tập hợp các service nhỏ, modular và có thể deploy độc lập.

Mỗi service thường:

* chạy như một process riêng;
* chịu trách nhiệm cho một business capability;
* có interface được định nghĩa rõ ràng;
* giao tiếp với các service khác thông qua network.

Có thể mô hình hóa:

$$
\text{Application}
=
\{S_1,S_2,\ldots,S_n\}
$$

trong đó:

$$
S_i
=
\text{một service phục vụ một business capability}
$$

---

## 7. Monolith và Microservices

### 7.1. Monolithic Architecture

```text
+----------------------------------+
|          Application             |
|                                  |
| User                             |
| Feed                             |
| Search                           |
| Photo                            |
| Notification                     |
+----------------------------------+
```

Toàn bộ application thường được build và deploy như một đơn vị:

$$
Deploy(Application)
$$

Nếu chỉ thay đổi Search:

```text
Search changed
      |
      v
Deploy entire application
```

---

### 7.2. Microservices Architecture

```text
+-------------+
| User        |
+-------------+

+-------------+
| Feed        |
+-------------+

+-------------+
| Search      |
+-------------+

+-------------+
| Photo       |
+-------------+

+-------------+
| Notification|
+-------------+
```

Mỗi service có thể được deploy độc lập:

$$
Deploy(S_{\text{search}})
$$

mà không nhất thiết:

$$
Deploy(S_{\text{user}})
$$

Đây là một trong những đặc điểm quan trọng của microservices:

$$
\boxed{\text{Independent Deployment}}
$$

---

## 8. Independent Scaling

Microservices cũng cho phép scale từng service dựa trên workload.

Ví dụ:

```text
User Service
   └── 2 instances

Feed Service
   └── 10 instances

Search Service
   └── 20 instances

Photo Service
   └── 5 instances
```

Nếu Search Service là bottleneck:

$$
N_{\text{search}}
\uparrow
$$

mà không nhất thiết:

$$
N_{\text{user}}
\uparrow
$$

Do đó:

$$
\boxed{
\text{Scaling follows workload}
}
$$

thay vì scale toàn bộ application.

---

## 9. Service Discovery

Khi hệ thống chỉ có một application server, địa chỉ của server có thể được biết trước.

Microservices lại có nhiều service và nhiều instance:

```text
User Service

10.0.0.10:8000
10.0.0.11:8000
10.0.0.12:8000
```

Khi đó một service khác cần biết:

> User Service hiện đang chạy ở đâu?

Đây là bài toán **Service Discovery**.

---

## 10. Service Registry

Service Discovery thường sử dụng một **Service Registry** để lưu thông tin của các service.

```text
+---------------------------+
|      Service Registry     |
+---------------------------+
| user-service              |
| 10.0.0.10:8000            |
| 10.0.0.11:8000            |
|                           |
| feed-service              |
| 10.0.0.20:8000            |
| 10.0.0.21:8000            |
+---------------------------+
```

Có thể biểu diễn:

$$
ServiceName
\rightarrow
\{IP, Port, Metadata\}
$$

Ví dụ:

$$
\texttt{user-service}
\rightarrow
\{
(10.0.0.10,8000),
(10.0.0.11,8000)
\}
$$

Các hệ thống như **Consul, Etcd và Zookeeper** có thể được sử dụng để hỗ trợ service discovery và coordination.

---

## 11. Service Registration

Khi một service instance khởi động, nó có thể đăng ký với registry:

```text
User Service
     |
     | register
     v
+----------------+
| Service        |
| Registry       |
+----------------+
```

Registry duy trì mapping:

$$
\text{Service Name}
\rightarrow
\text{Available Instances}
$$

Khi instance bị shutdown hoặc không còn hoạt động, thông tin của instance cần được cập nhật hoặc loại bỏ.

Điều này giúp hệ thống tránh gửi request đến các instance không còn tồn tại.

---

## 12. Health Check

Service Discovery thường kết hợp với **Health Check** để xác định instance nào đang hoạt động bình thường.

```text
              Service Registry
                     |
       +-------------+-------------+
       |             |             |
       v             v             v
    User #1       User #2       User #3
      OK            FAIL           OK
```

Nếu:

$$
Health(S_2)=false
$$

thì request không nên được gửi tới $S_2$.

Thay vào đó:

$$
Request
\rightarrow
\{S_1,S_3\}
$$

Health check có thể được thực hiện thông qua HTTP endpoint:

```http
GET /health
```

Ví dụ:

```json
{
  "status": "healthy"
}
```

Như vậy Service Discovery không chỉ giải quyết:

$$
\text{"Where is the service?"}
$$

mà còn hỗ trợ xác định:

$$
\text{"Which instance is available?"}
$$

---

## 13. Service Discovery và Load Balancing

Service Discovery và Load Balancing có vai trò khác nhau nhưng thường phối hợp với nhau.

```text
                  Service Registry
                         |
                 Healthy Instances
                         |
                         v
                  Load Balancer
                         |
             +-----------+-----------+
             |           |           |
             v           v           v
          App #1      App #2      App #3
```

Có thể phân biệt:

### Service Discovery

$$
\boxed{\text{Where are the services?}}
$$

### Health Check

$$
\boxed{\text{Which instances are healthy?}}
$$

### Load Balancer

$$
\boxed{\text{Which instance receives the request?}}
$$

---

## 14. Configuration và Key-Value Store

Một số hệ thống service discovery như Consul và Etcd còn cung cấp **key-value store**.

Dữ liệu có dạng:

$$
K \rightarrow V
$$

Ví dụ:

```text
database.host        -> db.internal
database.port        -> 5432
feature.new_feed     -> true
recommendation.model -> v3
```

Điều này cho phép configuration được quản lý tập trung thay vì hard-code trong application.

Ví dụ:

```text
Application
     |
     v
Configuration Store
     |
     +---- Database Config
     +---- Feature Flags
     +---- Service Config
```

Configuration có thể thay đổi theo environment:

$$
C_{\text{dev}}
\neq
C_{\text{staging}}
\neq
C_{\text{production}}
$$

---

## 15. Disadvantages của Application Layer

Việc bổ sung Application Layer và microservices không chỉ mang lại lợi ích. Nó đồng thời tạo ra nhiều complexity mới.

### 15.1. Architectural Complexity

Monolith:

```text
A -> B
```

Microservices:

```text
A -> B
A -> C
B -> D
C -> D
C -> E
```

Số lượng communication paths tăng khi số lượng services tăng.

Do đó:

$$
N_{\text{services}} \uparrow
\Rightarrow
N_{\text{dependencies}} \uparrow
$$

Hệ thống phải giải quyết thêm:

* service discovery;
* network communication;
* retries;
* timeouts;
* health checks;
* configuration;
* observability;
* distributed tracing.

---

## 16. Operational Complexity

Một monolith có thể được triển khai tương đối đơn giản:

```text
Build
  |
  v
Deploy
  |
  v
Application
```

Microservices yêu cầu quản lý nhiều deployment units:

```text
             CI/CD
               |
       +-------+-------+
       |       |       |
       v       v       v
     User    Feed    Search
       |       |       |
       +-------+-------+
               |
       Service Registry
               |
        Monitoring System
```

Mỗi service có thể có:

* version riêng;
* deployment riêng;
* logs riêng;
* metrics riêng;
* health status riêng;
* scaling policy riêng.

Do đó:

$$
\boxed{
\text{Microservices}
\rightarrow
\text{Operational Complexity}
\uparrow
}
$$

---

## 17. Network Communication và Partial Failure

Trong monolith, một lời gọi giữa các module thường chỉ là function call:

```python
result = service.process(data)
```

Trong microservices:

```text
Service A
    |
    | HTTP / RPC
    v
 Network
    |
    v
Service B
```

Network có thể:

* timeout;
* mất kết nối;
* trả response chậm;
* service đích bị down.

Do đó:

$$
P(\text{network failure}) > 0
$$

Application phải xử lý:

$$
\{
\text{Timeout},
\text{Retry},
\text{Fallback},
\text{Circuit Breaker}
\}
$$

Đây là một trong những khác biệt quan trọng giữa application architecture đơn giản và distributed architecture.

---

## 18. Microservices không phải luôn tốt hơn Monolith

Không nên xem microservices là kiến trúc luôn tốt hơn monolith.

Có thể biểu diễn trade-off:

$$
\text{Microservices}
=
\text{Independent Scaling}
+
\text{Independent Deployment}
+
\text{Service Isolation}
$$

nhưng đồng thời:

$$
+
\text{Network Complexity}
+
\text{Operational Complexity}
+
\text{Distributed System Complexity}
$$

Vì vậy lựa chọn kiến trúc phụ thuộc vào:

$$
Architecture
=
f(
Scale,
Domain,
Team,
Deployment,
Operational\ Capability
)
$$

Một hệ thống nhỏ có thể phù hợp với monolith, trong khi một hệ thống lớn với nhiều domain độc lập có thể hưởng lợi từ microservices.

---

## 19. Kiến trúc tổng hợp

Application Layer có thể được đặt trong toàn bộ kiến trúc system design như sau:

```text
                         Client
                           |
                           v
                          DNS
                           |
                           v
                          CDN
                           |
                           v
                    Load Balancer
                           |
                           v
                    Reverse Proxy
                           |
                           v
                    +-------------+
                    |  Web Layer  |
                    +------+------+
                           |
                           v
              +-------------------------+
              |    Application Layer    |
              |                         |
              |  User Service           |
              |  Feed Service           |
              |  Search Service         |
              |  Photo Service          |
              |  Notification Service   |
              |                         |
              |  Background Workers     |
              +-----------+-------------+
                          |
             +------------+------------+
             |                         |
             v                         v
      Service Discovery          Message Queue
             |                         |
             v                         v
      Service Registry              Workers
             |
             v
      +----------------+
      |   Data Layer   |
      |                |
      | DB / Cache     |
      | Object Storage |
      +----------------+
```

Có thể xem vai trò của từng tầng:

$$
\boxed{
DNS
\rightarrow
\text{Locate the system}
}
$$

$$
\boxed{
CDN
\rightarrow
\text{Deliver content closer to users}
}
$$

$$
\boxed{
Load\ Balancer
\rightarrow
\text{Distribute requests}
}
$$

$$
\boxed{
Reverse\ Proxy
\rightarrow
\text{Gateway into web infrastructure}
}
$$

$$
\boxed{
Application\ Layer
\rightarrow
\text{Execute business logic}
}
$$

$$
\boxed{
Service\ Discovery
\rightarrow
\text{Locate internal services}
}
$$

$$
\boxed{
Workers
\rightarrow
\text{Process asynchronous tasks}
}
$$

$$
\boxed{
Data\ Layer
\rightarrow
\text{Persist and retrieve data}
}
$$

---

## 20. Tổng kết

Application Layer giải quyết vấn đề **tách business logic khỏi Web Layer**, từ đó cho phép hệ thống mở rộng và tổ chức các thành phần độc lập hơn.

Ba ý tưởng quan trọng nhất là:

### 1. Independent Scaling

Web Layer và Application Layer có thể được scale độc lập:

$$
N_W \neq N_A
$$

### 2. Microservices

Application có thể được chia thành các service nhỏ, modular và independently deployable:

$$
\text{Application}
=
\{S_1,S_2,\ldots,S_n\}
$$

### 3. Service Discovery

Khi số lượng service tăng, hệ thống cần cơ chế để xác định service nào tồn tại và instance nào đang hoạt động:

$$
\text{Service Name}
\rightarrow
\text{Healthy Instances}
$$

Từ đó hình thành chuỗi kiến trúc:

```text
Application Layer
       |
       +---- Independent Scaling
       |
       +---- Single Responsibility
       |
       +---- Microservices
       |          |
       |          +---- Independent Deployment
       |          +---- Independent Scaling
       |
       +---- Asynchronism
       |          |
       |          +---- Queues
       |          +---- Workers
       |
       +---- Service Discovery
                  |
                  +---- Service Registry
                  +---- Health Checks
                  +---- Configuration
```

Tuy nhiên, khi chuyển từ monolith sang microservices:

$$
\text{Architectural Flexibility}
\uparrow
$$

đồng thời:

$$
\text{Operational Complexity}
\uparrow
$$

Do đó, mục tiêu của Application Layer không phải là **tối đa hóa số lượng service**, mà là tạo ra **ranh giới trách nhiệm hợp lý**, cho phép từng thành phần được scale, deploy và vận hành phù hợp với workload và business domain của nó.

---

## 21. Sources and Further Reading

1. **System Design Primer — Application Layer**
   https://github.com/donnemartin/system-design-primer#application-layer

2. **System Design Primer — Microservices**
   https://github.com/donnemartin/system-design-primer#microservices

3. **System Design Primer — Asynchronism**
   https://github.com/donnemartin/system-design-primer#asynchronism

4. **System Design Primer — Service Discovery**
   https://github.com/donnemartin/system-design-primer#service-discovery

5. **Intro to Architecting Systems for Scale — Platform Layer**
   https://lethain.com/introduction-to-architecting-systems-for-scale/#platform_layer

6. **Consul Documentation**
   https://developer.hashicorp.com/consul/docs

7. **Etcd Documentation**
   https://etcd.io/docs/

8. **Apache ZooKeeper Documentation**
   https://zookeeper.apache.org/

---

## Key Takeaways

> **Application Layer** tách business logic khỏi Web Layer và cho phép hai tầng scale độc lập.

> **Microservices** chia application thành các service nhỏ, modular và independently deployable.

> **Service Discovery** giúp các service tìm thấy nhau trong môi trường distributed.

> **Health Checks** giúp loại bỏ các service instance không khỏe khỏi quá trình routing.

> **Workers + Queues** cho phép xử lý workload bất đồng bộ và giảm thời gian response.

> **Trade-off:** Microservices mang lại khả năng scale và deploy độc lập nhưng đồng thời làm tăng architectural và operational complexity.

> **Nguyên tắc cốt lõi:** Không phải hệ thống càng nhiều microservices càng tốt; service boundary phải phản ánh business responsibility và workload thực tế.
