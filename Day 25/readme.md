# Consistency & Availability Patterns

## 1. Tổng quan

Trong hệ thống phân tán, dữ liệu và dịch vụ thường được triển khai trên nhiều máy chủ hoặc nhiều bản sao (**replicas**) nhằm đáp ứng yêu cầu về khả năng mở rộng, độ tin cậy và khả năng chịu lỗi. Tuy nhiên, việc phân tán tài nguyên tạo ra hai bài toán nền tảng:

1. **Consistency** — các bản sao dữ liệu nhìn thấy và phản ánh các cập nhật như thế nào?
2. **Availability** — hệ thống có thể tiếp tục cung cấp dịch vụ khi một hoặc nhiều thành phần gặp lỗi hay không?

Hai khái niệm này có quan hệ chặt chẽ nhưng không đồng nhất. Consistency tập trung vào **tính nhất quán của trạng thái dữ liệu**, trong khi availability tập trung vào **khả năng hệ thống tiếp tục phục vụ request**.

Có thể khái quát:

$$\boxed{
\text{Distributed System}
\rightarrow
\begin{cases}
\text{Consistency}\\
\text{Availability}\\
\text{Fault Tolerance}\\
\text{Scalability}
\end{cases}
}$$

Một hệ thống thực tế phải lựa chọn các consistency guarantee và availability mechanisms phù hợp với yêu cầu nghiệp vụ thay vì cố gắng tối đa hóa mọi thuộc tính cùng lúc.

---

# 2. Consistency Patterns

## 2.1. Khái niệm Consistency

Khi một hệ thống có nhiều bản sao của cùng một dữ liệu, các replica có thể không được cập nhật đồng thời.

Ví dụ:

```text
                 ┌──────────────┐
                 │   Primary    │
                 └──────┬───────┘
                        │
                Replication
             ┌──────────┼──────────┐
             ↓          ↓          ↓
          Replica A  Replica B  Replica C
```

Giả sử giá trị ban đầu là:

$$x=100$$

Sau một thao tác ghi:

$$x\leftarrow 50$$

có thể tồn tại trạng thái tạm thời:

```text
Replica A = 50
Replica B = 100
Replica C = 100
```

Do đó, hệ thống cần xác định:

> Khi nào một read bắt buộc phải nhìn thấy giá trị mới?

Đây chính là vấn đề của **consistency model**.

---

## 2.2. Weak Consistency

**Weak consistency** cho phép một read sau write không nhất thiết nhìn thấy dữ liệu mới.

Có thể xảy ra:

```text
Write x = 50
      ↓
Replica A = 50
Replica B = 100
      ↓
Read A → 50
Read B → 100
```

Hệ thống không đảm bảo rằng mọi replica đều phản ánh write mới ngay lập tức, thậm chí trong một số hệ thống realtime, một số cập nhật có thể không được phục hồi.

Weak consistency phù hợp với các ứng dụng mà dữ liệu mới nhất không phải yêu cầu tuyệt đối, đặc biệt khi latency và responsiveness quan trọng hơn consistency.

Ví dụ:

* voice communication;
* video chat;
* realtime multiplayer games;
* một số hệ thống telemetry hoặc streaming.

Ví dụ, nếu một packet thoại bị mất trong quá trình mất kết nối, hệ thống không nhất thiết phải retransmit toàn bộ nội dung đã bỏ lỡ. Việc cố gắng khôi phục tuyệt đối mọi dữ liệu có thể làm tăng latency và ảnh hưởng trải nghiệm realtime.

---

## 2.3. Eventual Consistency

**Eventual consistency** cung cấp guarantee mạnh hơn weak consistency.

Nếu không xuất hiện các write mới và hệ thống tiếp tục hoạt động bình thường, các replica cuối cùng sẽ hội tụ về cùng một trạng thái:

$$\lim_{t\rightarrow\infty}R_i(t)=v$$

với mọi replica (R_i).

Ví dụ:

```text
t0:
A = 100
B = 100
C = 100

t1:
A = 50
B = 100
C = 100

t2:
A = 50
B = 50
C = 100

t3:
A = 50
B = 50
C = 50
```

Trong giai đoạn chuyển tiếp, client có thể đọc dữ liệu cũ, nhưng hệ thống đảm bảo rằng các replica sẽ dần hội tụ.

Eventual consistency thường sử dụng **asynchronous replication**:

```text
Client
   │
   ↓
Primary
   │
   ├────→ Replica A
   ├────→ Replica B
   └────→ Replica C
```

Primary có thể xác nhận write trước khi mọi replica hoàn thành replication.

Điều này làm giảm write latency và tăng khả năng hệ thống tiếp tục hoạt động khi một replica tạm thời không khả dụng.

Các ví dụ điển hình gồm:

* DNS;
* email;
* distributed caching;
* một số hệ thống distributed storage;
* social media feeds.

---

## 2.4. Strong Consistency

**Strong consistency** yêu cầu rằng sau khi một write được hệ thống xác nhận, các read hợp lệ tiếp theo phải nhìn thấy trạng thái mới nhất theo consistency guarantee của hệ thống.

Ví dụ:

```text
Initial:
A = 100
B = 100
C = 100

Write x = 50

       ↓

A = 50
B = 50
C = 50

       ↓

Write success
```

Sau đó:

```text
Read A → 50
Read B → 50
Read C → 50
```

Strong consistency thường yêu cầu coordination giữa các node. Một phương pháp phổ biến là synchronous replication hoặc các cơ chế consensus/quorum.

Ưu điểm:

* dữ liệu có guarantee chặt chẽ hơn;
* phù hợp với transaction;
* giảm khả năng đọc stale data.

Nhược điểm:

* latency cao hơn;
* communication overhead;
* coordination complexity;
* availability có thể giảm trong một số failure scenarios.

Strong consistency thường phù hợp với:

* financial transactions;
* inventory;
* account balance;
* transactional databases;
* các hệ thống yêu cầu tính toàn vẹn cao.

---

## 2.5. So sánh Consistency Models

| Đặc điểm       | Weak                     | Eventual               | Strong                              |
| -------------- | ------------------------ | ---------------------- | ----------------------------------- |
| Read sau write | Có thể cũ                | Có thể cũ tạm thời     | Phải phản ánh update theo guarantee |
| Replication    | Không nhất thiết đồng bộ | Thường asynchronous    | Thường cần coordination             |
| Latency        | Thấp                     | Thấp                   | Cao hơn                             |
| Availability   | Cao                      | Cao                    | Thường thấp hơn khi failure         |
| Stale data     | Có thể                   | Có thể tạm thời        | Không theo guarantee                |
| Use case       | Realtime                 | Distributed/high-scale | Transactional                       |

Cần lưu ý rằng đây không phải là thứ hạng từ "xấu" đến "tốt". Mỗi consistency model là một **trade-off**.

---

# 3. Availability Patterns

## 3.1. Khái niệm Availability

**Availability** biểu thị khả năng hệ thống tiếp tục cung cấp dịch vụ khi client gửi request.

Một hệ thống có availability cao cần hạn chế ảnh hưởng của:

* server failure;
* hardware failure;
* network failure;
* software failure;
* datacenter failure;
* maintenance.

Hai pattern quan trọng để xây dựng high availability là:

$$\boxed{
\text{Fail-over}
\quad+\quad
\text{Replication}
}$$

---

# 4. Fail-over

Fail-over là cơ chế chuyển traffic từ một thành phần đang gặp lỗi sang một thành phần dự phòng.

```text
Primary Server
      │
      │ failure
      ↓
Backup Server
      │
      ↓
Continue service
```

Fail-over có hai mô hình chính:

1. Active-passive
2. Active-active

---

## 4.1. Active-passive

Trong mô hình active-passive:

```text
              Heartbeat
        ┌──────────────────┐
        │                  │
        ↓                  ↓
┌──────────────┐    ┌──────────────┐
│ Active       │    │ Passive      │
│ Server       │    │ Server       │
│              │    │ Standby      │
└──────────────┘    └──────────────┘
       │
       ↓
    Traffic
```

Chỉ **active server** xử lý traffic.

Passive server ở trạng thái standby và theo dõi active server thông qua heartbeat.

Nếu heartbeat bị gián đoạn:

```text
Active failure
      ↓
Heartbeat timeout
      ↓
Passive promoted
      ↓
Traffic redirected
```

Passive server có thể ở:

* **hot standby** — server đã chạy và sẵn sàng nhận traffic;
* **cold standby** — server phải khởi động hoặc khôi phục trước khi phục vụ.

Do đó, thời gian downtime phụ thuộc đáng kể vào thời gian phát hiện failure và thời gian chuyển đổi:

$$T_{downtime}
\approx
T_{detection}
+
T_{promotion}
+
T_{rerouting}$$

### Ưu điểm

* kiến trúc tương đối đơn giản;
* dễ kiểm soát state;
* phù hợp với các hệ thống có một primary rõ ràng.

### Nhược điểm

* tài nguyên passive có thể bị sử dụng không hiệu quả;
* fail-over tạo ra downtime;
* có thể mất dữ liệu nếu replication chưa hoàn thành.

---

# 5. Active-active

Trong active-active, nhiều server đồng thời xử lý traffic:

```text
                 Load Balancer
                 /           \
                ↓             ↓
        ┌──────────────┐ ┌──────────────┐
        │ Server A     │ │ Server B     │
        │ Active       │ │ Active       │
        └──────────────┘ └──────────────┘
```

Traffic được phân phối giữa các server.

Nếu một server failure:

```text
Server A → failure

Remaining traffic
       ↓
Server B
```

Mô hình này vừa cung cấp redundancy vừa tận dụng tài nguyên của nhiều server.

### Ưu điểm

* sử dụng tài nguyên hiệu quả hơn;
* không cần chờ một passive server khởi động;
* có khả năng tăng throughput;
* failure của một node ít ảnh hưởng hơn.

### Nhược điểm

* routing phức tạp hơn;
* state synchronization khó hơn;
* concurrent writes có thể tạo conflict;
* yêu cầu thiết kế tốt về consistency.

Active-active thường liên quan trực tiếp đến consistency:

```text
Client A ──→ Server A ──→ Data
Client B ──→ Server B ──→ Data
                         ↑
                    Synchronization
```

Nếu hai server cùng ghi vào cùng một dữ liệu, hệ thống cần cơ chế xử lý conflict và ordering.

---

# 6. Fail-over và Replication không giống nhau

Hai khái niệm này thường bị nhầm lẫn.

### Replication

Mục tiêu chính:

> Tạo và duy trì nhiều bản sao dữ liệu hoặc trạng thái.

```text
Primary
  ├──→ Replica A
  ├──→ Replica B
  └──→ Replica C
```

### Fail-over

Mục tiêu chính:

> Duy trì khả năng phục vụ khi một thành phần thất bại.

```text
Active
   ↓ failure
Passive
   ↓
Service continues
```

Trong hệ thống thực tế, chúng thường được kết hợp:

```text
        Primary
           │
      Replication
       /       \
      ↓         ↓
 Replica A   Replica B
       \       /
        Fail-over
           ↓
     Service continuity
```

Replication cung cấp **redundancy**, trong khi fail-over cung cấp **mechanism để sử dụng redundancy khi failure xảy ra**.

---

# 7. Hạn chế của Fail-over

Fail-over không miễn phí.

### 7.1. Hardware cost

Hệ thống phải duy trì thêm server hoặc infrastructure:

$$\text{Cost}_{HA}

\gt

\text{Cost}_{single\ server}$$

### 7.2. System complexity

Phải xử lý:

* heartbeat;
* failure detection;
* leader election;
* traffic rerouting;
* state recovery;
* split-brain;
* data synchronization.

### 7.3. Potential data loss

Nếu replication là asynchronous:

```text
Primary
   │
   ├── Write A
   ├── Write B
   └── Write C
          │
          X failure
          ↓
      Replica
   only has A, B
```

Write C có thể chưa được replicate.

Do đó:

$$\text{Data Loss Risk}
\propto
\text{Replication Lag}$$

Trong thực tế, replication lag càng lớn thì lượng dữ liệu có nguy cơ mất khi primary failure càng lớn.

---

# 8. Availability trong các con số

Availability thường được biểu diễn dưới dạng phần trăm uptime:

$$Availability=

\frac{Uptime}
{Uptime+Downtime}$$

Hoặc:

$$Availability=

1-
\frac{Downtime}
{Total\ Time}$$

Một cách biểu diễn phổ biến là **number of nines**.

---

## 8.1. Three nines — 99.9%

$$A=99.9%=0.999$$

Downtime xấp xỉ:

| Chu kỳ  |              Downtime |
| ------- | --------------------: |
| 1 năm   | 8 giờ 45 phút 57 giây |
| 1 tháng |     43 phút 49.7 giây |
| 1 tuần  |      10 phút 4.8 giây |
| 1 ngày  |      1 phút 26.4 giây |

---

## 8.2. Four nines — 99.99%

$$A=99.99%=0.9999$$

Downtime xấp xỉ:

| Chu kỳ  |          Downtime |
| ------- | ----------------: |
| 1 năm   | 52 phút 35.7 giây |
| 1 tháng |    4 phút 23 giây |
| 1 tuần  |     1 phút 5 giây |
| 1 ngày  |          8.6 giây |

Điểm quan trọng là chỉ tăng availability từ:

$$99.9%
\rightarrow
99.99%$$

nhưng downtime hàng năm giảm từ khoảng:

$$8.77\text{ giờ}
\rightarrow
0.88\text{ giờ}$$

Do đó, thêm một "9" có ý nghĩa rất lớn đối với hệ thống production.

---

# 9. Availability của các component trong hệ thống

Một service thường không chỉ có một component:

```text
Client
   ↓
Load Balancer
   ↓
Application Server
   ↓
Database
   ↓
Storage
```

Availability tổng thể phụ thuộc vào quan hệ giữa các component.

Hai trường hợp cơ bản là:

1. **Series / sequential components**
2. **Parallel / redundant components**

---

# 10. Components trong sequence

Nếu hai component đều bắt buộc phải hoạt động:

```text
Client
  ↓
Foo
  ↓
Bar
  ↓
Response
```

thì cả Foo và Bar đều phải available.

Do đó:

$$A_{total}=

A_{Foo}\times A_{Bar}$$

Ví dụ:

$$A_{Foo}=0.999$$

$$A_{Bar}=0.999$$

thì:

$$A_{total}=0.999\times0.999$$

$$A_{total}=0.998001$$

Xấp xỉ 99.8%.

Điều này cho thấy:

> **Khi các component nằm trong chuỗi phụ thuộc, reliability của hệ thống giảm theo tích availability của các component.**

---

# 11. Components trong parallel

Nếu hai component có thể thay thế lẫn nhau:

```text
                 ┌──→ Foo ──┐
Client ──────────┤           ├──→ Response
                 └──→ Bar ──┘
```

service chỉ failure khi **cả Foo và Bar cùng failure**.

Xác suất failure của Foo:

$$F_{Foo}=1-A_{Foo}$$

Tương tự:

$$F_{Bar}=1-A_{Bar}$$

Do đó:

$$F_{total}=

(1-A_{Foo})(1-A_{Bar})$$

và:

$$\boxed{
A_{total}=

1-(1-A_{Foo})(1-A_{Bar})
}$$

Nếu:

$$A_{Foo}=A_{Bar}=0.999$$

thì:

$$A_{total}=

1-(0.001)(0.001)=0.999999$$

Đây là lý do redundancy có thể làm availability tăng rất mạnh.

---

# 12. Series vs Parallel

Có thể tổng quát hóa:

### Series

Tất cả component phải hoạt động:

$$\boxed{
A_{system}=

\prod_{i=1}^{n}A_i
}$$

### Parallel

Chỉ cần ít nhất một component hoạt động:

$$\boxed{
A_{system}=

1-\prod_{i=1}^{n}(1-A_i)
}$$

Giả định quan trọng ở đây là các failure event đủ độc lập để phép tính này có ý nghĩa. Trong hệ thống thực tế, các failure thường có **common-cause failures** như mất điện, lỗi network, lỗi deployment hoặc lỗi một dependency chung. Khi đó, availability thực tế có thể thấp hơn mô hình lý thuyết.

---

# 13. Mối quan hệ giữa Consistency và Availability

Consistency và availability không phải hai khái niệm độc lập.

Giả sử có:

```text
        Primary
        /      \
       ↓        ↓
 Replica A   Replica B
```

Nếu replication asynchronous:

```text
Write
  ↓
Primary = new
Replica A = new
Replica B = old
```

Hệ thống có thể tiếp tục trả response từ Replica B.

Điều này tăng availability nhưng có thể làm giảm consistency.

Ngược lại, nếu hệ thống yêu cầu mọi replica phải đồng bộ trước khi trả response:

```text
Write
 ↓
Primary
 ↓
wait for replicas
 ↓
success
```

consistency guarantee cao hơn nhưng latency và availability trong failure scenarios có thể bị ảnh hưởng.

Do đó:

$$\boxed{
Consistency
\leftrightarrow
Availability
\leftrightarrow
Latency
}$$

là một trong những trade-off trung tâm của distributed system design.

---

# 14. Liên hệ với CAP Theorem

Trong điều kiện network partition, CAP theorem cho rằng hệ thống không thể đồng thời đảm bảo đầy đủ:

$$C+A+P$$

Trong đó:

* $C$: Consistency;
* $A$: Availability;
* $P$: Partition tolerance.

Trong một distributed system thực tế, partition tolerance thường được xem là yêu cầu bắt buộc vì network failure là điều không thể loại bỏ hoàn toàn.

Do đó, khi partition xảy ra, hệ thống thường phải lựa chọn giữa hai hướng:

### Ưu tiên Consistency

```text
Partition
   ↓
Cannot guarantee latest state
   ↓
Reject / delay request
```

Hệ thống hy sinh một phần availability để giữ consistency.

### Ưu tiên Availability

```text
Partition
   ↓
Continue serving requests
   ↓
Potentially stale data
```

Hệ thống tiếp tục phục vụ nhưng chấp nhận dữ liệu có thể chưa nhất quán.

Vì vậy, CAP không đơn giản nói rằng "một hệ thống chỉ được chọn hai trong ba chữ". Chính xác hơn, **khi partition xảy ra**, hệ thống phải đánh đổi giữa consistency và availability theo consistency guarantee mà nó muốn duy trì.

---

# 15. Tổng hợp kiến trúc

Có thể nhìn toàn bộ hai nhóm pattern như sau:

```text
                  Distributed System
                         │
            ┌────────────┴────────────┐
            ↓                         ↓
      Consistency                 Availability
            │                         │
     ┌──────┼──────┐            ┌─────┴─────┐
     ↓      ↓      ↓            ↓           ↓
   Weak  Eventual Strong     Fail-over  Replication
                                  │
                            ┌─────┴─────┐
                            ↓           ↓
                     Active-passive Active-active
```

Trong đó:

* **Consistency patterns** quyết định cách hệ thống xử lý sự khác biệt giữa các bản sao.
* **Replication** tạo ra các bản sao để tăng redundancy và scalability.
* **Fail-over** cho phép hệ thống chuyển sang tài nguyên dự phòng khi failure xảy ra.
* **Availability metrics** định lượng khả năng hệ thống tiếp tục phục vụ.
* **Series/parallel architecture** quyết định cách availability của các component được kết hợp.

---

# 16. Kết luận

Consistency và availability là hai thuộc tính nền tảng trong thiết kế hệ thống phân tán. **Consistency patterns** xác định mức độ đảm bảo mà hệ thống cung cấp đối với việc quan sát và đồng bộ các cập nhật giữa các replica. Weak consistency ưu tiên latency và khả năng đáp ứng trong các ứng dụng realtime; eventual consistency cho phép các replica tạm thời không đồng nhất nhưng cuối cùng hội tụ; trong khi strong consistency cung cấp guarantee chặt chẽ hơn, phù hợp với các hệ thống transactional.

Ở phía availability, **fail-over** và **replication** là hai cơ chế bổ trợ quan trọng. Replication tạo ra redundancy, trong khi fail-over khai thác redundancy đó để duy trì dịch vụ khi component gặp lỗi. Active-passive đơn giản hơn nhưng có thể tạo downtime trong quá trình chuyển đổi, còn active-active tận dụng đồng thời nhiều node nhưng yêu cầu xử lý routing, state synchronization và consistency phức tạp hơn.

Availability cũng cần được phân tích ở cấp độ kiến trúc. Với các component mắc nối tiếp, availability tổng thể là tích availability của từng component:

$$A_{series}=\prod_i A_i$$

Trong khi với các component hoạt động song song và có khả năng thay thế:

$$A_{parallel}=

1-\prod_i(1-A_i)$$

Do đó, **redundancy có thể cải thiện availability đáng kể**, nhưng đồng thời làm tăng chi phí và độ phức tạp của hệ thống.

Cuối cùng, không tồn tại một kiến trúc tối ưu cho mọi ứng dụng. Một hệ thống tốt phải xác định **consistency guarantee tối thiểu**, **availability target**, **latency requirement** và **failure model** trước khi lựa chọn replication và fail-over strategy. Đây chính là tư duy cốt lõi của System Design:

$$\boxed{
\text{Requirements}
\rightarrow
\text{Trade-offs}
\rightarrow
\text{Architecture}
}$$
