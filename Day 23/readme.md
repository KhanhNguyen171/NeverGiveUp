# How to approach a system design interview question

Phần này của **System Design Primer** là một trong những framework quan trọng nhất để trả lời System Design Interview. Điểm cốt lõi không phải là “vẽ thật nhiều server”, mà là **biết dẫn dắt cuộc phỏng vấn từ yêu cầu → kiến trúc → chi tiết → khả năng scale → trade-off**.

[System Design Primer – How to approach a system design interview question](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com#how-to-approach-a-system-design-interview-question)


## How to approach a system design interview question

### Cách tiếp cận một câu hỏi System Design Interview

System Design Interview là một **cuộc hội thoại có tính mở** (*open-ended conversation*). Bạn được kỳ vọng là người **chủ động dẫn dắt cuộc thảo luận**.

Có thể sử dụng các bước sau để định hướng cuộc thảo luận. Để củng cố quy trình này, hãy thực hành với phần **System design interview questions with solutions** theo các bước dưới đây.

---

## Step 1 — Xác định use cases, constraints và assumptions

### Xác định các trường hợp sử dụng, ràng buộc và giả định

Trước tiên, hãy thu thập yêu cầu và xác định phạm vi của bài toán.

Đặt câu hỏi để làm rõ:

* Use case nào cần hỗ trợ?
* Hệ thống phục vụ ai?
* Người dùng sẽ sử dụng hệ thống như thế nào?
* Có bao nhiêu người dùng?
* Hệ thống cần thực hiện những chức năng gì?
* Input và output là gì?
* Hệ thống phải xử lý bao nhiêu dữ liệu?
* Có bao nhiêu request mỗi giây?
* Tỷ lệ đọc/ghi là bao nhiêu?

### Những câu hỏi quan trọng

> **Who is going to use it?**

- Ai sử dụng hệ thống?

> **How are they going to use it?**

- Họ sử dụng hệ thống như thế nào?

> **How many users are there?**

- Có bao nhiêu user?

> **What does the system do?**

- Hệ thống thực hiện chức năng gì?

> **What are the inputs and outputs?**

- Input và output là gì?

> **How much data do we expect to handle?**

- Hệ thống phải xử lý bao nhiêu dữ liệu?

> **How many requests per second do we expect?**

- Hệ thống cần xử lý bao nhiêu request/giây?

> **What is the expected read to write ratio?**

- Tỷ lệ đọc/ghi dự kiến là bao nhiêu?

---

## Step 2 — Tạo high-level design

### Thiết kế kiến trúc cấp cao

Sau khi hiểu bài toán, xây dựng một thiết kế cấp cao bao gồm những component quan trọng.

Hai việc chính:

1. Vẽ các component chính và kết nối giữa chúng.
2. Giải thích lý do lựa chọn kiến trúc.

Ví dụ:

```text
                 ┌──────────────┐
                 │    Client    │
                 └──────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Load Balancer │
                └───────┬───────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
       ┌─────────────┐     ┌─────────────┐
       │ App Server  │     │ App Server  │
       └──────┬──────┘     └──────┬──────┘
              │                   │
              └─────────┬─────────┘
                        ▼
                  ┌───────────┐
                  │   Cache   │
                  └─────┬─────┘
                        │
                        ▼
                  ┌───────────┐
                  │ Database  │
                  └───────────┘
```

Nhưng **không được vẽ kiến trúc này ngay từ đầu**.

Đây là một lỗi rất phổ biến.

Trước tiên phải xác định requirements và scale.

---

## Step 3 — Design core components

### Thiết kế các thành phần cốt lõi

Sau high-level design, bắt đầu đi sâu vào từng component quan trọng.

Ví dụ đề bài:

> Design a URL Shortener.

Bạn có thể phải thiết kế:

### 1. Sinh short URL

```text
Long URL
   │
   ▼
Hash / ID Generator
   │
   ▼
Base62 encoding
   │
   ▼
Short URL
```

Sau đó phải thảo luận:

* MD5 hay thuật toán khác?
* Base62?
* Hash collision?
* SQL hay NoSQL?
* Database schema?
* Index?

### 2. Chuyển short URL thành URL gốc

```text
Short URL
    │
    ▼
Database lookup
    │
    ▼
Original URL
    │
    ▼
HTTP Redirect
```

### 3. API

Ví dụ:

```http
POST /urls
GET /{short_code}
```

Và cần suy nghĩ về:

* API contract
* Request/response
* Error handling
* Object-oriented design
* Data model

---

## Step 4 — Scale the design

### Mở rộng hệ thống

Sau khi có thiết kế cơ bản, đặt câu hỏi:

> **Điểm nghẽn nằm ở đâu?**

Ví dụ:

```text
             Traffic
                │
                ▼
        ┌───────────────┐
        │ Load Balancer │
        └───────┬───────┘
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
     App 1    App 2    App 3
       │        │        │
       └────────┼────────┘
                ▼
              Cache
                │
                ▼
             Database
```

Có thể cần:

* Load Balancer
* Horizontal Scaling
* Caching
* Database Sharding

Nhưng điều quan trọng là:

> **Không phải hệ thống nào cũng cần tất cả những thứ trên.**

Bạn phải giải thích:

**Tại sao cần?**

và:

**Tại sao chọn giải pháp này thay vì giải pháp khác?**

---

## 2. Ý tưởng quan trọng nhất: System Design là một quá trình

Nếu chỉ nhớ một framework, hãy nhớ:

```text
Requirements
     │
     ▼
Estimation
     │
     ▼
High-Level Design
     │
     ▼
Core Components
     │
     ▼
Bottlenecks
     │
     ▼
Scaling
     │
     ▼
Trade-offs
```

Đây chính là **flow tư duy** của một System Design Interview.

Không phải:

```text
Question
   ↓
Kafka + Redis + Kubernetes + MongoDB
```

Đây là kiểu trả lời mà interviewer thường không đánh giá cao.

---

## 3. Step 1 thực chất quan trọng như thế nào?

Đây có lẽ là phần **quan trọng nhất đối với người mới học System Design**.

Ví dụ interviewer hỏi:

> **Design YouTube.**

Nếu lập tức vẽ:

```text
Client
 ↓
API Gateway
 ↓
Microservices
 ↓
Kafka
 ↓
Redis
 ↓
S3
 ↓
CDN
```

thì bạn đang **thiết kế trước khi hiểu bài toán**.

Thay vào đó phải hỏi:

### Functional requirements

Ví dụ:

* User upload video?
* User xem video?
* User search video?
* Like/comment?
* Subscribe?
* Recommendation?

Sau đó giới hạn scope:

> Trong interview này, tôi sẽ tập trung vào **video upload + video playback**.

Đây gọi là **scoping**.

---

## 4. Functional vs Non-functional requirements

Đây là một khái niệm bạn nên bổ sung vào framework trên.

### Functional requirements

Hệ thống **làm được gì?**

Ví dụ với YouTube:

```text
Upload video
Watch video
Search video
Like video
Comment
```

### Non-functional requirements

Hệ thống **phải hoạt động như thế nào?**

Ví dụ:

```text
Availability
Latency
Scalability
Consistency
Durability
Reliability
Security
```

Ví dụ:

> Video playback phải có latency thấp.

hoặc:

> Hệ thống phải chịu được 1 million concurrent users.

Đây mới là những yêu cầu quyết định kiến trúc.

---

## 5. Back-of-the-envelope calculation

Đây là phần rất quan trọng nhưng người mới thường bỏ qua.

Mục đích là biến:

> "Hệ thống rất lớn"

thành:

> "Hệ thống cần khoảng X requests/second và Y TB storage."

Ví dụ:

Giả sử:

```text
Users = 10 million
DAU = 2 million

Mỗi user:
10 requests/day
```

Thì:

```text
Total requests/day
= 2M × 10
= 20M requests/day
```

QPS trung bình:

```text
20,000,000 / 86,400
≈ 231 QPS
```

Nếu peak traffic gấp 5:

```text
Peak QPS
≈ 231 × 5
≈ 1,155 QPS
```

Từ đây mới bắt đầu suy nghĩ:

> Một server có chịu được ~1,200 QPS không?

Nếu không:

```text
1 server
    ↓
Horizontal Scaling
    ↓
10 servers
```

---

## 6. Read/Write Ratio rất quan trọng

Ví dụ:

```text
Read : Write = 100 : 1
```

thì architecture sẽ khác rất nhiều so với:

```text
Read : Write = 1 : 1
```

Ví dụ URL Shortener:

```text
POST /shorten
```

tạo URL mới → write.

Trong khi:

```text
GET /abc123
```

→ read.

Nếu:

```text
Read = 99%
Write = 1%
```

thì caching trở nên cực kỳ hấp dẫn.

```text
Client
  │
  ▼
Cache
  │
  ├── HIT ──→ Response
  │
  └── MISS
        │
        ▼
     Database
```

Đây là ví dụ điển hình cho việc:

> **Requirement → workload → architecture**

---

## 7. Step 2 — High-Level Design

Ở bước này, mục tiêu chưa phải là biết từng field trong database.

Mục tiêu là trả lời:

> **Các thành phần lớn của hệ thống là gì và chúng nói chuyện với nhau như thế nào?**

Ví dụ một hệ thống web:

```text
                  ┌─────────┐
                  │ Client  │
                  └────┬────┘
                       │
                       ▼
                ┌─────────────┐
                │ CDN / LB    │
                └──────┬──────┘
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
      ┌─────────────┐     ┌─────────────┐
      │ App Server  │     │ App Server  │
      └──────┬──────┘     └──────┬──────┘
             │                   │
             └─────────┬─────────┘
                       ▼
                  ┌─────────┐
                  │ Cache   │
                  └────┬────┘
                       │
                       ▼
                  ┌─────────┐
                  │   DB    │
                  └─────────┘
```

Sau đó **justify từng component**.

Ví dụ:

> Tôi sử dụng Load Balancer vì application server có thể scale horizontally.

> Tôi sử dụng cache vì workload có read/write ratio rất cao.

> Tôi dùng database vì dữ liệu cần persistence.

---

## 8. Step 3 — Core Components

Đây là lúc interviewer bắt đầu đào sâu.

Ví dụ:

> Design Twitter/X timeline.

High-level:

```text
Client
  │
  ▼
API
  │
  ├──── Tweet Service
  │
  ├──── User Service
  │
  └──── Timeline Service
              │
              ▼
             Cache
              │
              ▼
              DB
```

Sau đó interviewer có thể hỏi:

> Timeline được tạo như thế nào?

Lúc này bạn phải đi sâu vào algorithm.

Có hai hướng kinh điển:

### Fan-out on write

Khi user tweet:

```text
Tweet
  │
  ▼
Find followers
  │
  ▼
Push tweet into followers' timelines
```

Ưu điểm:

```text
Read timeline → rất nhanh
```

Nhược điểm:

```text
Celebrity có 100M followers
→ write amplification cực lớn
```

### Fan-out on read

Không push tweet ngay.

Khi user mở timeline:

```text
Get followed users
       │
       ▼
Get their tweets
       │
       ▼
Merge
       │
       ▼
Timeline
```

Ưu điểm:

```text
Write nhẹ
```

Nhược điểm:

```text
Read phức tạp + latency cao hơn
```

Và cuối cùng:

> Có thể sử dụng **hybrid approach**.

Đây chính là **trade-off discussion**.

---

## 9. Step 4 — Scaling

Một cách học rất tốt là luôn hỏi 4 câu:

### ① Compute bottleneck?

Server có quá tải không?

→ Horizontal scaling.

### ② Network bottleneck?

Traffic quá lớn?

→ CDN / compression / batching.

### ③ Database bottleneck?

Database quá tải?

→

```text
Caching
Read replicas
Partitioning
Sharding
Indexes
```

### ④ Latency bottleneck?

Request quá chậm?

→

```text
Cache
CDN
Async processing
Denormalization
Precomputation
```

---

## 10. "Everything is a trade-off"

Đây là câu cực kỳ quan trọng trong System Design.

Không có:

> **Best architecture**

Mà chỉ có:

> **Architecture phù hợp với requirements và constraints.**

Ví dụ:

| Choice          | Đổi lại                                                           |
| --------------- | ----------------------------------------------------------------- |
| Cache           | nhanh hơn nhưng stale data                                        |
| NoSQL           | scale dễ nhưng query flexibility giảm                             |
| SQL             | consistency/relational mạnh nhưng horizontal scaling phức tạp hơn |
| Sharding        | scale DB nhưng query/operation phức tạp                           |
| Async queue     | giảm latency request nhưng eventual consistency                   |
| Replication     | availability/read throughput tốt hơn nhưng consistency khó hơn    |
| Denormalization | read nhanh hơn nhưng write phức tạp                               |

Vì vậy interviewer thường thích câu:

> "Tôi chọn A vì requirement X. Trade-off là Y. Nếu constraint Z thay đổi, tôi sẽ cân nhắc B."

hơn là:

> "Redis là tốt nhất."

---

## 11. Framework hoàn chỉnh nên ghi nhớ

Từ nội dung của Primer, bạn có thể nâng thành framework học System Design như sau:

```text
┌─────────────────────────────┐
│ 1. REQUIREMENTS             │
│ Functional                  │
│ Non-functional              │
│ Scope                       │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ 2. ESTIMATION               │
│ Users                       │
│ DAU/MAU                     │
│ QPS                         │
│ Read/Write                  │
│ Storage                     │
│ Bandwidth                   │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ 3. HIGH-LEVEL DESIGN       │
│ Client                      │
│ API                         │
│ Services                    │
│ Cache                       │
│ DB                          │
│ Queue                       │
│ CDN                         │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ 4. CORE COMPONENTS          │
│ API                         │
│ Data model                  │
│ Algorithms                  │
│ Storage                     │
│ Communication               │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ 5. BOTTLENECKS              │
│ CPU                         │
│ Memory                      │
│ Network                     │
│ Database                    │
│ Latency                     │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ 6. SCALE                    │
│ LB                          │
│ Horizontal scaling          │
│ Cache                       │
│ Replication                 │
│ Partitioning / Sharding     │
│ CDN                         │
│ Async processing            │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ 7. TRADE-OFFS               │
│ Consistency                 │
│ Availability                │
│ Latency                     │
│ Cost                        │
│ Complexity                  │
└─────────────────────────────┘
```

---

## 12. Cách áp dụng khi đi phỏng vấn

Giả sử interviewer nói:

> **Design Instagram.**

Đừng bắt đầu vẽ.

Hãy bắt đầu bằng:

### 1. Clarify

> "Before designing the system, I'd like to clarify the scope."

Sau đó hỏi:

```text
Users?
DAU?
Upload photo?
View feed?
Like/comment?
Follow?
Search?
```

### 2. Chốt scope

> "For this interview, I'll focus on photo upload and home feed generation."

### 3. Estimate

```text
100M DAU
10M uploads/day
500M feed reads/day
```

### 4. High-level architecture

```text
Client
  │
  ▼
API Gateway
  │
  ├── User Service
  ├── Post Service
  ├── Feed Service
  │
  ├── Object Storage
  ├── Cache
  ├── Database
  └── Message Queue
```

### 5. Deep dive

Ví dụ:

> Feed được generate như thế nào?

→ Fan-out on write/read/hybrid.

### 6. Scale

> Database bottleneck?

→ replication / partitioning / sharding.

> Image delivery bottleneck?

→ object storage + CDN.

> Feed generation quá chậm?

→ cache + precomputation + async processing.

### 7. Trade-off

Cuối cùng:

> "The main trade-off here is between write amplification and read latency."

Đây mới thực sự là **System Design thinking**.

---

## 13. Điều cần học tiếp từ System Design Primer

Phần bạn gửi mới là **framework để giải bài**, chưa phải toàn bộ kiến thức System Design.

Sau phần này, nên học theo dependency:

```text
                    SYSTEM DESIGN
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   Fundamentals      Databases        Networking
        │                │                │
        ▼                ▼                ▼
   Availability      SQL/NoSQL        HTTP/TCP
   Scalability       Replication      DNS
   Consistency       Sharding         CDN
   Reliability       Indexing         Load Balancer
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                  Distributed Systems
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
        Cache          Queue         Messaging
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                  Design Patterns
                         │
                         ▼
                 Real-world Systems
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       URL Shortener   Twitter        YouTube
       Instagram      Dropbox        Uber
       WhatsApp       Netflix        etc.
```

[System Design Primer – System Design Topics](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com#system-design-topics-start-here)

**Điểm quan trọng:** đừng học các bài *URL Shortener, Twitter, Instagram, YouTube...* như những bài thuộc lòng. Hãy dùng chúng để luyện một chu trình cố định:

> **Requirements → Estimation → Architecture → Deep Dive → Bottleneck → Scaling → Trade-off.**

Đó mới là kỹ năng mà System Design Interview thực sự kiểm tra.
