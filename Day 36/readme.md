# Security

Security là một chủ đề rộng trong system design. Trong phạm vi của `System Design Primer`, mục tiêu không phải xây dựng một hệ thống bảo mật hoàn chỉnh mà tập trung vào các nguyên tắc cơ bản cần được xem xét khi thiết kế hệ thống.

Nguồn gốc của phần này cũng lưu ý rằng nội dung security hiện cần được cập nhật và khuyến khích cộng đồng đóng góp.

Mục tiêu cốt lõi có thể quy về bốn nguyên tắc:

1. Bảo vệ dữ liệu khi truyền và khi lưu trữ.
2. Kiểm soát và làm sạch dữ liệu đầu vào.
3. Ngăn chặn SQL injection bằng parameterized queries.
4. Áp dụng nguyên tắc least privilege.

## 1. Encrypt in transit and at rest

### 1.1. Encryption in transit

Dữ liệu `in transit` là dữ liệu đang được truyền giữa các thành phần của hệ thống, ví dụ:

$$
Client \rightarrow Load\ Balancer \rightarrow Application\ Server
$$

hoặc:

$$
Application\ Server \rightarrow Database
$$

Nếu dữ liệu truyền qua mạng không được bảo vệ, attacker có thể cố gắng đọc hoặc thay đổi dữ liệu trong quá trình truyền.

Vì vậy, hệ thống cần sử dụng cơ chế mã hóa khi truyền dữ liệu.

Mục tiêu:

* Bảo mật nội dung dữ liệu.
* Giảm nguy cơ nghe lén.
* Bảo vệ thông tin xác thực.
* Bảo vệ dữ liệu giữa các service.

### 1.2. Encryption at rest

Dữ liệu `at rest` là dữ liệu đang được lưu trữ trên:

* Database.
* File system.
* Object storage.
* Backup.
* Persistent storage.

Ví dụ:

$$
Application \rightarrow Database
$$

Database có thể chứa:

* Password hoặc credential-related data.
* Personal information.
* Business data.
* Access tokens.
* Transaction information.

Do đó, việc chỉ bảo vệ network layer là chưa đủ. Dữ liệu lưu trữ cũng cần được bảo vệ.

### 1.3. Nguyên tắc tổng quát

Có thể mô hình hóa security của dữ liệu theo hai trạng thái:

$$
Data\ Security =
Security_{in\ transit}
+
Security_{at\ rest}
$$

Trong thiết kế hệ thống, cả hai trạng thái đều phải được xem xét.

---

## 2. Input Sanitization


Một hệ thống lớn thường nhận dữ liệu từ nhiều nguồn:

$$
User \rightarrow API \rightarrow Application \rightarrow Database
$$

Input từ người dùng không nên được giả định là an toàn.

Nếu application sử dụng trực tiếp input của người dùng trong:

* HTML.
* JavaScript.
* SQL query.
* Command.
* Template.
* API parameters.

thì attacker có thể lợi dụng input để thực hiện hành vi ngoài dự kiến.

### 2.1. Cross-Site Scripting

Cross-Site Scripting (`XSS`) xảy ra khi dữ liệu không đáng tin cậy được đưa vào nội dung web theo cách cho phép attacker thực thi script trong browser của người dùng.

Mô hình đơn giản:

$$
Untrusted\ Input
\rightarrow
Web\ Application
\rightarrow
Browser
\rightarrow
Malicious\ Script
$$

Do đó, application cần xử lý và kiểm tra input trước khi sử dụng.

#### 2.1.1. Input validation

Input validation kiểm tra xem dữ liệu có phù hợp với yêu cầu hay không.

Ví dụ một trường `age` có thể yêu cầu:

$$
age \in \mathbb{Z}
$$

và:

$$
0 \leq age \leq 150
$$

Thay vì chấp nhận mọi chuỗi dữ liệu.

#### 2.1.2. Sanitization

Sanitization loại bỏ hoặc biến đổi những phần dữ liệu có khả năng gây nguy hiểm trước khi đưa vào hệ thống.

Mục tiêu là giảm khả năng untrusted input được diễn giải như code hoặc command.

---

## 3. SQL Injection

SQL injection là một trong những rủi ro quan trọng khi application xây dựng SQL query từ input người dùng theo cách không an toàn.

Kiến trúc nguy hiểm:

$$
User\ Input
\rightarrow
String\ Concatenation
\rightarrow
SQL\ Query
\rightarrow
Database
$$

Nếu input được ghép trực tiếp vào query, dữ liệu đầu vào có thể thay đổi cấu trúc của câu lệnh SQL.

### 3.1. Parameterized queries

`System Design Primer` khuyến nghị sử dụng parameterized queries để ngăn SQL injection.

Thay vì:

$$
SQL = "SELECT\ ... " + UserInput
$$

application sử dụng query với parameter:

$$
SQL = "SELECT\ ...\ WHERE\ id = ?"
$$

và truyền giá trị:

$$
Parameter = UserInput
$$

Database engine sẽ phân biệt:

$$
SQL\ Structure
\neq
User\ Data
$$

Đây là điểm quan trọng: **input của người dùng phải được xem là dữ liệu, không phải một phần của câu lệnh SQL.**

### 3.2. Ý nghĩa trong system design

Security không chỉ là một component độc lập.

Nó phải xuất hiện xuyên suốt data flow:

$$
Client
\rightarrow
API
\rightarrow
Application
\rightarrow
Database
$$

Tại mỗi boundary cần xem xét:

* Input validation.
* Authentication.
* Authorization.
* Data protection.
* Query safety.

---

## 4. Principle of Least Privilege

`Least privilege` là nguyên tắc cấp cho một user, process hoặc service **chỉ những quyền cần thiết để thực hiện nhiệm vụ của nó**.

Giả sử application chỉ cần đọc một bảng:

$$
Permission(Application)
=
READ
$$

thì không nên cấp:

$$
Permission(Application)
=
READ + WRITE + DELETE + ADMIN
$$

### 4.1. Giảm blast radius

Nếu một service bị compromise, quyền hạn nhỏ hơn sẽ giới hạn phạm vi ảnh hưởng.

Giả sử:

$$
Service_A
\rightarrow
Database
$$

Nếu `Service_A` có toàn bộ quyền database và bị compromise:

$$
Compromise(Service_A)
\Rightarrow
Potentially\ Compromise(Database)
$$

Ngược lại, nếu service chỉ có quyền cần thiết:

$$
Compromise(Service_A)
\Rightarrow
Limited\ Impact
$$

Do đó:

$$
Least\ Privilege
\rightarrow
Reduced\ Attack\ Surface
$$

### 4.2. Least privilege trong distributed system

Trong hệ thống nhiều service:

$$
Service_A
\rightarrow
Service_B
\rightarrow
Database
$$

mỗi service nên có identity và permission riêng.

Không nên sử dụng một credential có quyền quản trị cho toàn bộ hệ thống.

---

## 5. Security Design Summary

Bốn nguyên tắc trong phần Security có thể tổng hợp thành:

$$
Security =
Encryption
+
Input\ Validation
+
Parameterized\ Queries
+
Least\ Privilege
$$

| Nguyên tắc            | Vấn đề giải quyết               | Vị trí          |
| --------------------- | ------------------------------- | --------------- |
| Encrypt in transit    | Bảo vệ dữ liệu khi truyền       | Network         |
| Encrypt at rest       | Bảo vệ dữ liệu lưu trữ          | Storage         |
| Input sanitization    | Kiểm soát dữ liệu không tin cậy | Application     |
| Parameterized queries | Ngăn SQL injection              | Database access |
| Least privilege       | Hạn chế quyền truy cập          | Toàn hệ thống   |

Điểm quan trọng nhất là security phải được xem như **một thuộc tính xuyên suốt kiến trúc**, thay vì chỉ là một lớp được bổ sung sau khi hệ thống đã hoàn thành.

### Source(s) and further reading

* API Security Checklist
* Security Guide for Developers
* OWASP Top Ten

---

# Appendix

Phần Appendix cung cấp các công cụ tham khảo phục vụ việc **ước lượng nhanh trong system design**.

Trong một buổi system design interview, không phải mọi con số đều cần chính xác tuyệt đối. Điều quan trọng là có thể nhanh chóng ước lượng:

* Thời gian xử lý.
* Dung lượng bộ nhớ.
* Throughput.
* Network latency.
* Storage capacity.

Hai tài nguyên chính được `System Design Primer` đưa ra là:

1. Powers of two table.
2. Latency numbers every programmer should know.

---

## 1. Powers of Two Table

Powers of two là một công cụ quan trọng để thực hiện các phép ước lượng nhanh.

Ta có:

$$
2^n
$$

Một số giá trị quan trọng:

|    Power |       Exact Value | Approximate Value | Bytes |
| -------: | ----------------: | ----------------: | ----: |
|    $2^7$ |               128 |               128 |       |
|    $2^8$ |               256 |               256 |       |
| $2^{10}$ |             1,024 |        1 thousand |  1 KB |
| $2^{16}$ |            65,536 |                   | 64 KB |
| $2^{20}$ |         1,048,576 |         1 million |  1 MB |
| $2^{30}$ |     1,073,741,824 |         1 billion |  1 GB |
| $2^{32}$ |     4,294,967,296 |                   |  4 GB |
| $2^{40}$ | 1,099,511,627,776 |        1 trillion |  1 TB |

### 1.1. Tại sao powers of two quan trọng?

Trong system design, chúng ta thường phải trả lời các câu hỏi dạng:

> Hệ thống cần bao nhiêu memory?

Giả sử có:

$$
N = 10^6
$$

object và mỗi object chiếm:

$$
S = 1\ KB
$$

thì storage xấp xỉ:

$$
Memory = N \times S
$$

$$
= 10^6 \times 1KB
\approx 1GB
$$

Mục tiêu không phải đạt độ chính xác tuyệt đối mà nhanh chóng xác định **order of magnitude**.

### 1.2. Order of magnitude

Ví dụ:

$$
10^6 \approx 1\ million
$$

$$
10^9 \approx 1\ billion
$$

$$
10^{12} \approx 1\ trillion
$$

Những xấp xỉ này giúp đánh giá nhanh liệu một thiết kế có khả thi hay không.

---

## 2. Latency Numbers Every Programmer Should Know

Latency là thời gian cần để một operation hoàn thành.

Các hệ thống khác nhau có latency rất khác nhau:

```text
Latency Comparison Numbers
--------------------------
L1 cache reference                           0.5 ns
Branch mispredict                            5   ns
L2 cache reference                           7   ns
Mutex lock/unlock                           25   ns
Main memory reference                      100   ns
Compress 1K bytes with Zippy            10,000   ns
Send 1 KB bytes over 1 Gbps network     10,000   ns
Read 4 KB randomly from SSD             150,000   ns
Read 1 MB sequentially from memory     250,000   ns
Round trip within same datacenter      500,000   ns
Read 1 MB sequentially from SSD     1,000,000   ns
HDD seek                            10,000,000   ns
Read 1 MB sequentially from 1 Gbps  10,000,000   ns
Read 1 MB sequentially from HDD     30,000,000   ns
Send packet CA->Netherlands->CA    150,000,000   ns
```

### 2.1. Đơn vị latency

Các đơn vị cơ bản:

$$
1ns = 10^{-9}s
$$

$$
1\mu s = 10^{-6}s = 1000ns
$$

$$
1ms = 10^{-3}s = 1000\mu s
$$

Do đó:

$$
1ms = 1,000,000ns
$$

### 2.2. So sánh memory và storage

Ví dụ:

$$
L1 \approx 0.5ns
$$

trong khi:

$$
Main\ Memory \approx 100ns
$$

Do đó:

$$
\frac{100}{0.5}=200
$$

Main memory có latency xấp xỉ 200 lần L1 cache theo bảng tham khảo.

SSD và HDD còn chậm hơn đáng kể.

Điều này giải thích tại sao system designer thường cố gắng:

$$
Avoid\ Unnecessary\ I/O
$$

và sử dụng:

* Cache.
* Batching.
* Asynchronous processing.
* Data locality.
* In-memory data structures.

### 2.3. Network latency

Network không chỉ có bandwidth mà còn có latency.

Ví dụ một request có flow:

$$
Client
\rightarrow
Server
\rightarrow
Database
\rightarrow
Server
\rightarrow
Client
$$

Nếu mỗi network round trip có latency đáng kể thì tổng thời gian phản hồi có thể tăng nhanh.

Do đó, một hệ thống có thể có:

$$
High\ Bandwidth
\neq
Low\ Latency
$$

Hai khái niệm phải được phân tích riêng.

### 2.4. Các metric suy ra

Từ các con số trên, tài liệu đưa ra một số xấp xỉ hữu ích:

* Đọc tuần tự từ HDD: khoảng 30 MB/s.
* Đọc tuần tự qua 1 Gbps Ethernet: khoảng 100 MB/s.
* Đọc tuần tự từ SSD: khoảng 1 GB/s.
* Đọc tuần tự từ main memory: khoảng 4 GB/s.
* Khoảng 6–7 world-wide round trips mỗi giây.
* Khoảng 2,000 round trips mỗi giây trong cùng một data center.

Những con số này không nên được hiểu là benchmark cố định cho mọi phần cứng. Chúng là **mental reference points** dùng cho estimation.

---

## 3. Latency Numbers Visualized

Việc trực quan hóa latency giúp thể hiện rõ khoảng cách giữa:

$$
CPU\ Cache
\rightarrow
Memory
\rightarrow
SSD
\rightarrow
HDD
\rightarrow
Network
$$

Điểm quan trọng cần ghi nhớ không phải từng giá trị tuyệt đối mà là **magnitude difference**.

Một operation có latency lớn khi được thực hiện hàng triệu hoặc hàng tỷ lần sẽ trở thành bottleneck.

Nếu một operation có latency: $L$ và được thực hiện: $N$ lần, chi phí tổng quát có thể hình dung ở mức:

$$
T \approx N \times L
$$

Trong hệ thống phân tán, cần đặc biệt chú ý những operation liên quan đến:

* Network round trips.
* Disk I/O.
* Database access.
* Cross-service communication.

### Source(s) and further reading

* Latency numbers every programmer should know.
* Designs, lessons, and advice from building large distributed systems.
* Software Engineering Advice from Building Large-Scale Distributed Systems.

---

## 4. Additional System Design Interview Questions

Phần này tập hợp các câu hỏi system design phổ biến và các tài nguyên để tiếp tục nghiên cứu.

Mục tiêu không phải ghi nhớ từng architecture mà là luyện khả năng chuyển từ:

$$
Requirements
\rightarrow
Architecture
\rightarrow
Trade\!-\!offs
$$

### 4.1. File synchronization

**Problem:** Design a file synchronization service like Dropbox.

Các vấn đề cần nghiên cứu:

* File metadata.
* File storage.
* Synchronization.
* Conflict resolution.
* Large file transfer.
* Incremental updates.
* Scalability.

### 4.2. Search engine

**Problem:** Design a search engine like Google.

Các thành phần cần suy nghĩ:

$$
Crawler
\rightarrow
Indexer
\rightarrow
Search\ Index
\rightarrow
Query\ Service
$$

Các vấn đề chính:

* Web crawling.
* Indexing.
* Ranking.
* Distributed storage.
* Query latency.

### 4.3. Web crawler

**Problem:** Design a scalable web crawler.

Một crawler cần xử lý:

$$
URL\ Frontier
\rightarrow
Crawler
\rightarrow
Fetched\ Pages
\rightarrow
Parser
\rightarrow
Index
$$

Các vấn đề quan trọng:

* Distributed crawling.
* URL deduplication.
* Rate limiting.
* Scheduling.
* Storage.

### 4.4. Google Docs

**Problem:** Design Google Docs.

Trọng tâm là collaboration và synchronization.

Nhiều client cùng thay đổi một document:

$$
Client_A
\rightarrow
Document
\leftarrow
Client_B
$$

Do đó cần nghiên cứu:

* Concurrent editing.
* Synchronization.
* Conflict resolution.
* Data consistency.

### 4.5. Key-value store

**Problem:** Design a key-value store like Redis.

Mô hình cơ bản:

$$
Key \rightarrow Value
$$

Các vấn đề:

* Partitioning.
* Replication.
* Persistence.
* Consistency.
* Availability.
* Memory management.

### 4.6. Cache system

**Problem:** Design a cache system like Memcached.

Mục tiêu chính:

$$
Reduce\ Database\ Load
$$

và:

$$
Reduce\ Read\ Latency
$$

Các vấn đề cần nghiên cứu:

* Cache eviction.
* Cache consistency.
* Distribution.
* Replication.
* Memory constraints.

### 4.7. Recommendation system

**Problem:** Design a recommendation system.

Một kiến trúc khái quát:

$$
User\ Activity
\rightarrow
Feature\ Generation
\rightarrow
Recommendation
\rightarrow
Ranking
$$

Các vấn đề:

* User modeling.
* Item modeling.
* Candidate generation.
* Ranking.
* Scalability.

### 4.8. URL shortening service

**Problem:** Design a URL shortening service like Bitly.

Flow:

$$
Long\ URL
\rightarrow
Short\ ID
\rightarrow
Storage
$$

Khi truy cập:

$$
Short\ ID
\rightarrow
Lookup
\rightarrow
Long\ URL
\rightarrow
Redirect
$$

Các vấn đề:

* ID generation.
* Hash collision.
* Base62.
* Database schema.
* Read/write ratio.
* Cache.

### 4.9. Chat application

**Problem:** Design a chat application like WhatsApp.

Hệ thống phải xử lý:

$$
User_A
\leftrightarrow
Chat\ Service
\leftrightarrow
User_B
$$

Các vấn đề:

* Real-time communication.
* Message ordering.
* Delivery.
* Persistence.
* Presence.
* Scaling connections.

### 4.10. Image sharing system

**Problem:** Design a picture-sharing system like Instagram.

Kiến trúc có thể phân tách:

$$
Upload
\rightarrow
Object\ Storage
\rightarrow
Processing
\rightarrow
CDN
\rightarrow
Client
$$

Các vấn đề:

* Image storage.
* Image processing.
* Metadata.
* CDN.
* Feed generation.
* Scaling.

### 4.11. News feed

**Problem:** Design a social network news feed.

Điểm khó là số lượng user và quan hệ giữa user.

Một feed có thể được xây dựng dựa trên:

$$
User
+
Social\ Graph
+
Activity
\rightarrow
Feed
$$

Các vấn đề:

* Fan-out.
* Feed generation.
* Caching.
* Ranking.
* Hot users.
* Read/write trade-off.

### 4.12. CDN

**Problem:** Design a content delivery network.

Mục tiêu:

$$
Client
\rightarrow
Nearest\ Edge
\rightarrow
Content
$$

thay vì:

$$
Client
\rightarrow
Origin\ Server
$$

cho mọi request.

Các vấn đề:

* Edge locations.
* Cache.
* Origin.
* Cache invalidation.
* Geographic distribution.

### 4.13. API rate limiter

**Problem:** Design an API rate limiter.

Mục tiêu:

$$
Requests_{user} \leq Limit
$$

trong một khoảng thời gian xác định.

Ví dụ:

$$
100\ requests/minute
$$

Các vấn đề:

* Distributed counters.
* Burst traffic.
* Expiration.
* Consistency.
* Low latency.

### 4.14. Stock exchange

**Problem:** Design a stock exchange such as NASDAQ or Binance.

Đây là bài toán yêu cầu latency thấp và throughput cao.

Flow khái quát:

$$
Order
\rightarrow
Validation
\rightarrow
Order\ Book
\rightarrow
Matching
\rightarrow
Execution
$$

Các vấn đề:

* Matching engine.
* Order book.
* Ordering.
* Consistency.
* Fault tolerance.
* Low latency.

---

## 5. Real World Architectures

Phần `Real world architectures` cung cấp các bài viết và tài liệu về kiến trúc của những hệ thống thực tế.

Tài liệu nhấn mạnh rằng không nên tập trung vào từng chi tiết implementation nhỏ.

Thay vào đó cần:

1. Xác định shared principles.
2. Xác định common technologies.
3. Xác định architecture patterns.
4. Hiểu vấn đề mà từng component giải quyết.
5. Hiểu giới hạn của từng component.
6. Học từ các lesson learned.

### 5.1. Data processing

#### 5.1.1. MapReduce

MapReduce là mô hình distributed data processing.

Mô hình:

$$
Input
\rightarrow
Map
\rightarrow
Shuffle
\rightarrow
Reduce
\rightarrow
Output
$$

Ý tưởng chính là phân chia computation thành nhiều worker.

#### 5.1.2. Spark

Spark là nền tảng distributed data processing.

Điểm cần nghiên cứu:

* Distributed computation.
* Data partitioning.
* Parallel processing.
* Fault tolerance.

#### 5.1.3. Storm

Storm tập trung vào distributed stream processing.

Có thể mô hình hóa:

$$
Event\ Stream
\rightarrow
Processing\ Topology
\rightarrow
Result
$$

---

## 6. Data Stores

Phần real-world architectures giới thiệu nhiều loại distributed data store.

### 6.1. Bigtable

Bigtable là distributed column-oriented database.

Điểm nghiên cứu:

* Distributed storage.
* Column-oriented organization.
* Horizontal scalability.

### 6.2. HBase

HBase là open-source implementation dựa trên ý tưởng Bigtable.

### 6.3. Cassandra

Cassandra là distributed column-oriented database.

Các vấn đề quan trọng:

* Partitioning.
* Replication.
* Availability.
* Distributed writes.

### 6.4. DynamoDB

DynamoDB được đưa vào như một document-oriented database.

Điểm cần nghiên cứu:

* Distributed storage.
* Partitioning.
* Availability.
* Scalability.

### 6.5. MongoDB

MongoDB là document-oriented database.

Dữ liệu có thể được biểu diễn theo document thay vì bảng quan hệ truyền thống.

### 6.6. Spanner

Spanner là globally distributed database.

Điểm đặc biệt cần nghiên cứu:

$$
Global\ Distribution
+
Consistency
+
Scalability
$$

---

## 7. Distributed Memory Systems

### 7.1. Memcached

Memcached là distributed memory caching system.

Mục tiêu:

$$
Fast\ Access
\rightarrow
Reduce\ Backend\ Load
$$

### 7.2. Redis

Redis là distributed memory caching system có persistence và hỗ trợ nhiều loại value.

Điểm cần nghiên cứu:

* In-memory access.
* Data structures.
* Persistence.
* Distributed deployment.

---

## 8. File Systems

### 8.1. Google File System

GFS là distributed file system.

Mục tiêu chính:

$$
Large\ Scale
+
Distributed\ Storage
+
Fault\ Tolerance
$$

### 8.2. Hadoop File System

HDFS là open-source implementation của ý tưởng distributed file system tương tự GFS.

---

## 9. Miscellaneous Distributed Systems

### 9.1. Chubby

Chubby là lock service cho loosely-coupled distributed systems.

Nó giải quyết bài toán coordination giữa các thành phần.

### 9.2. Dapper

Dapper là distributed systems tracing infrastructure.

Mục tiêu:

$$
Request
\rightarrow
Multiple\ Services
\rightarrow
Trace
$$

giúp theo dõi một request xuyên qua distributed system.

### 9.3. Kafka

Kafka là hệ thống pub/sub message queue.

Mô hình:

$$
Producer
\rightarrow
Kafka
\rightarrow
Consumer
$$

Kafka phù hợp với các hệ thống cần xử lý event stream hoặc message ở quy mô lớn.

### 9.4. ZooKeeper

ZooKeeper cung cấp centralized infrastructure và services hỗ trợ synchronization.

Trong distributed system, coordination là một vấn đề quan trọng vì nhiều node cần cùng nhìn thấy trạng thái hoặc configuration nhất quán.

---

## 10. Company Architectures

Phần này tập hợp architecture case studies từ nhiều công ty.

Các ví dụ gồm:

* Amazon.
* Dropbox.
* Google.
* Instagram.
* Facebook.
* Netflix.
* Pinterest.
* Twitter.
* Uber.
* WhatsApp.
* YouTube.
* Stack Overflow.
* Salesforce.
* Tumblr.
* TripAdvisor.

### 10.1. Cách học company architecture

Không nên học theo cách:

$$
Company_A = Architecture_A
$$

mà nên trích xuất các pattern:

$$
Architecture
\rightarrow
Problem
\rightarrow
Solution
\rightarrow
Trade\!-\!off
$$

Ví dụ cần đặt câu hỏi:

* Component này giải quyết bottleneck nào?
* Tại sao cần cache?
* Tại sao cần sharding?
* Tại sao cần asynchronous processing?
* Tại sao cần replication?
* Bottleneck nằm ở đâu?
* Nếu traffic tăng $10\times$ thì điều gì xảy ra?

---

## 11. Company Engineering Blogs

Engineering blogs là nguồn tài liệu để nghiên cứu architecture thực tế từ các công ty.

Các nguồn trong tài liệu bao gồm:

* Airbnb Engineering.
* Atlassian Developers.
* AWS Blog.
* Dropbox Tech Blog.
* Facebook Engineering.
* GitHub Engineering.
* Google Research.
* Instagram Engineering.
* LinkedIn Engineering.
* Microsoft Engineering.
* Netflix Tech Blog.
* Pinterest Engineering.
* Salesforce Engineering.
* Slack Engineering.
* Stripe Engineering.
* Twitter Engineering.
* Uber Engineering.
* Yahoo Engineering.

### 11.1. Mục tiêu học engineering blogs

Engineering blog không nên được đọc đơn thuần như tài liệu công nghệ.

Nên chuyển mỗi bài viết thành chuỗi câu hỏi:

$$
Problem
\rightarrow
Constraint
\rightarrow
Design
\rightarrow
Bottleneck
\rightarrow
Trade\!-\!off
\rightarrow
Lesson
$$

Đây chính là cách chuyển kiến thức architecture thực tế thành kiến thức system design có thể tái sử dụng.

### Source(s) and further reading

Nguồn của phần engineering blogs trong repository cũng đề cập đến một repository chuyên tổng hợp các engineering blogs để tránh trùng lặp công sức khi đóng góp tài liệu.

---

# Under Development

Tại thời điểm tài liệu nguồn được cung cấp, repository đánh dấu một số chủ đề là `Under development`.

Các chủ đề gồm:

* Distributed computing with MapReduce.
* Consistent hashing.
* Scatter gather.

## 1. Distributed computing with MapReduce

MapReduce cần được nghiên cứu sâu hơn ở mức:

$$
Distributed\ Data
\rightarrow
Parallel\ Computation
\rightarrow
Aggregation
$$

## 2. Consistent hashing

Consistent hashing giải quyết các vấn đề liên quan đến phân phối key trên nhiều node.

Mục tiêu:

$$
Key
\rightarrow
Node
$$

và hạn chế lượng key phải di chuyển khi node được thêm hoặc loại bỏ.

## 3. Scatter gather

Scatter-gather mô hình hóa việc một request được gửi đến nhiều backend:

$$
Request
\rightarrow
\begin{cases}
Service_1\\
Service_2\\
\vdots\\
Service_n
\end{cases}
\rightarrow
Aggregation
$$

Pattern này cần được cân nhắc về:

* Latency.
* Failure.
* Partial results.
* Fan-out.
* Aggregation.