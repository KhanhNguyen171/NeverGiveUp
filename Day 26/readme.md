# Domain Name System

Phần này trong **System Design Primer** đang giới thiệu DNS dưới góc nhìn **system design**, tức không chỉ hỏi “DNS là gì?” mà quan trọng hơn là: **DNS hoạt động thế nào, nó ảnh hưởng đến scalability/availability ra sao, và tại sao DNS có thể được dùng để routing traffic**.

[System Design Primer – GitHub](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com)

---

# 1. DNS là gì?

DNS (**Domain Name System**) là hệ thống ánh xạ:

$$\text{Domain Name} \rightarrow \text{IP Address}$$

Ví dụ:

```text
www.example.com
       ↓
93.184.216.34
```

Con người thích sử dụng:

```text
www.example.com
```

trong khi máy tính cần địa chỉ IP để thiết lập kết nối:

```text
93.184.216.34
```

Do đó có thể xem DNS như một **distributed naming system**.

Điểm quan trọng trong System Design là:

> DNS không trực tiếp phục vụ business request. Nó giúp client **tìm ra nơi cần gửi request**.

Ví dụ:

```text
User
  │
  │ www.example.com
  ▼
DNS
  │
  │ 203.0.113.10
  ▼
Load Balancer
  │
  ▼
Application Servers
```

Vì vậy DNS nằm ở **rất gần entry point của hệ thống**.

---

# 2. DNS có tính hierarchical

DNS không phải một database duy nhất chứa toàn bộ domain trên Internet.

Nó có kiến trúc phân cấp:

```text
                         Root
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
             .com        .org        .vn
              │
              ▼
          example.com
              │
       ┌──────┴──────┐
       ▼             ▼
   www.example.com  api.example.com
```

Có thể hiểu:

```text
.
└── com
    └── example
        ├── www
        └── api
```

Các tầng có trách nhiệm khác nhau.

Ví dụ khi resolve:

```text
www.example.com
```

DNS resolver có thể lần lượt tìm:

```text
Root
  ↓
.com
  ↓
example.com
  ↓
www.example.com
```

Điều này giúp DNS có thể scale trên phạm vi Internet.

---

# 3. Recursive resolver và authoritative DNS

Đây là phần rất quan trọng nhưng đoạn Primer trên viết khá ngắn.

Có thể phân biệt hai loại server:

### Recursive DNS resolver

Đây thường là DNS server mà client sử dụng thông qua:

* ISP
* router
* public DNS provider
* corporate network

Ví dụ:

```text
Client
   │
   │ DNS query
   ▼
Recursive Resolver
```

Resolver chịu trách nhiệm tìm câu trả lời thay client.

---

### Authoritative DNS server

Đây là server **có thẩm quyền đối với một domain**.

Ví dụ:

```text
example.com
     │
     ▼
Authoritative DNS
     │
     ├── www → 1.2.3.4
     ├── api → 1.2.3.5
     └── mail → mail.example.com
```

Authoritative server là nguồn dữ liệu DNS chính thức cho zone/domain đó.

---

# 4. DNS caching

Nếu mỗi request đều phải đi từ client lên Root → TLD → Authoritative DNS thì Internet sẽ cực kỳ chậm và DNS infrastructure sẽ chịu tải khổng lồ.

Vì vậy DNS sử dụng **caching**.

Ví dụ lần đầu:

```text
Browser
   │
   ▼
OS cache
   │ miss
   ▼
Recursive DNS
   │ miss
   ▼
Authoritative DNS
   │
   ▼
93.184.216.34
```

Sau đó kết quả được cache:

```text
Browser / OS
      │
      │ cache hit
      ▼
93.184.216.34
```

Không cần query DNS từ đầu nữa.

---

# 5. TTL — Time To Live

DNS record có một thuộc tính rất quan trọng:

**TTL (Time To Live)**.

Ví dụ:

```text
www.example.com
A
93.184.216.34
TTL = 300 seconds
```

Điều này có nghĩa resolver/cache có thể coi record này còn hợp lệ trong khoảng:

$$TTL = 300s$$

Sau khi TTL hết hạn:

```text
Cache
  │
  │ expired
  ▼
DNS query lại
```

---

# 6. Tại sao DNS propagation xảy ra?

Giả sử ban đầu:

```text
www.example.com
        ↓
10.0.0.1
```

Sau đó bạn đổi thành:

```text
www.example.com
        ↓
10.0.0.2
```

Nhưng các resolver trên Internet có thể đang cache:

```text
www.example.com → 10.0.0.1
```

Do đó trong một khoảng thời gian:

```text
User A → old IP
User B → old IP
User C → new IP
```

Đây chính là một trong những nguyên nhân của **DNS propagation delay**.

Điểm cần nhớ:

> Thay đổi DNS record không có nghĩa là toàn bộ Internet lập tức nhìn thấy giá trị mới.

TTL càng lớn → cache càng lâu → propagation có thể lâu hơn.

TTL càng nhỏ → thay đổi được nhận biết nhanh hơn nhưng DNS query frequency tăng.

Đây là một trade-off:

$$\boxed{
\text{TTL thấp}
\leftrightarrow
\text{freshness cao + DNS load cao}
}$$

$$\boxed{
\text{TTL cao}
\leftrightarrow
\text{cache hiệu quả + freshness thấp}
}$$

---

# 7. Các DNS record quan trọng

Primer liệt kê 4 loại record chính.

## 7.1 NS record

**NS = Name Server**

Cho biết authoritative DNS server nào chịu trách nhiệm cho domain/zone.

Ví dụ:

```text
example.com
    NS
    ns1.example-dns.com
```

Có thể hiểu:

> “Muốn biết DNS information của `example.com` thì hỏi server này.”

---

# 8. MX record

**MX = Mail Exchange**

Xác định mail server chịu trách nhiệm nhận email cho domain.

Ví dụ:

```text
example.com
     MX
mail.example.com
```

Khi gửi:

```text
user@example.com
```

mail system sẽ tra MX record để biết gửi email đến đâu.

---

# 9. A record

**A = Address**

Ánh xạ hostname → IPv4 address.

Ví dụ:

```text
www.example.com
        A
192.0.2.10
```

Tức:

$$[www.example.com](http://www.example.com) \rightarrow 192.0.2.10$$

Đây là loại record trực tiếp nhất đối với web system.

Ngoài A record còn có:

```text
AAAA → IPv6
```

Ví dụ:

```text
www.example.com
        AAAA
2001:db8::1
```

---

# 10. CNAME

**CNAME = Canonical Name**

CNAME ánh xạ một hostname tới một hostname khác.

Ví dụ:

```text
example.com
     │
     ▼
www.example.com
```

Hoặc:

```text
api.example.com
       │
       ▼
api.example.cdnprovider.com
```

Điểm quan trọng:

> CNAME trỏ tới **tên**, không phải trực tiếp tới IP.

Trong thực tế CNAME rất hữu ích khi sử dụng:

* CDN
* cloud service
* managed infrastructure
* load balancing services

---

# 11. DNS không chỉ dùng để "đổi domain thành IP"

Đây là phần quan trọng nhất khi học **System Design**.

DNS có thể trở thành một **traffic routing layer**.

Thay vì:

```text
www.example.com
        ↓
Server A
```

ta có:

```text
              DNS
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
    Server A Server B Server C
```

DNS có thể quyết định IP nào được trả về cho client.

Do đó DNS có thể hỗ trợ:

* load distribution
* failover
* geographic routing
* latency-based routing
* A/B testing
* disaster recovery

---

# 12. Weighted Round Robin

Giả sử có:

```text
Server A
Server B
Server C
```

DNS có thể phân phối traffic theo weight:

```text
A: 50%
B: 30%
C: 20%
```

Ví dụ:

```text
1000 requests

A ≈ 500
B ≈ 300
C ≈ 200
```

Điều này hữu ích khi server có capacity khác nhau.

Ví dụ:

```text
Cluster A: 100 servers
Cluster B: 20 servers
```

Không nên chia traffic:

```text
50% / 50%
```

mà có thể:

```text
80% / 20%
```

---

# 13. A/B testing bằng DNS

DNS cũng có thể hỗ trợ A/B testing.

Ví dụ:

```text
                www.example.com
                       │
                      DNS
                 ┌─────┴─────┐
                 ▼           ▼
              Version A   Version B
                 90%          10%
```

Trong đó:

```text
A = production version
B = experimental version
```

DNS trả IP tương ứng với một tỷ lệ nhất định.

Tuy nhiên cần nhớ:

> DNS-based A/B testing không phải lúc nào cũng chính xác tuyệt đối theo từng request.

Lý do là DNS response được cache.

Ví dụ DNS trả:

```text
Version B
```

và resolver cache kết quả trong 300 giây.

Trong khoảng thời gian đó nhiều client có thể tiếp tục nhận cùng routing decision.

---

# 14. Latency-based routing

Đây là một kỹ thuật rất quan trọng trong distributed systems.

Giả sử hệ thống có:

```text
US
 │
 └── US servers

Europe
 │
 └── EU servers

Asia
 │
 └── Asia servers
```

DNS có thể trả endpoint phù hợp với latency thấp hơn.

Ví dụ:

```text
User Vietnam
      │
      ▼
     DNS
      │
      ▼
Singapore Region
```

Trong khi:

```text
User US
   │
   ▼
  DNS
   │
   ▼
US Region
```

Mục tiêu:

$$\min \text{Latency}$$

[AWS Route 53 – Latency-based routing](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-latency.html?utm_source=chatgpt.com)

---

# 15. Geolocation-based routing

Khác với latency-based routing, geolocation routing dựa vào **vị trí của client**.

Ví dụ:

```text
Vietnam
   ↓
Vietnam/Singapore region

Japan
   ↓
Tokyo region

US
   ↓
US region
```

Có thể biểu diễn:

$$f(\text{client location}) \rightarrow \text{endpoint}$$

[AWS Route 53 – Geolocation routing](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-geo.html?utm_source=chatgpt.com)

Điều này hữu ích khi hệ thống cần:

* data residency
* localization
* regulatory compliance
* giảm latency
* regional traffic control

---

# 16. DNS trong kiến trúc lớn

Một kiến trúc thực tế có thể trông như:

```text
                    User
                      │
                      ▼
                  DNS Resolver
                      │
                      ▼
               Authoritative DNS
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
         Region US         Region Asia
             │                 │
             ▼                 ▼
        Load Balancer     Load Balancer
             │                 │
       ┌─────┴─────┐     ┌─────┴─────┐
       ▼           ▼     ▼           ▼
     App A       App B App C       App D
```

DNS có thể quyết định **region nào** được sử dụng.

Sau đó Load Balancer tiếp tục quyết định **server nào** trong region đó.

Đây là một distinction rất quan trọng:

```text
DNS
 ↓
Global traffic routing

Load Balancer
 ↓
Regional traffic distribution
```

---

# 17. DNS Failover

DNS cũng có thể hỗ trợ failover.

Ví dụ:

```text
              DNS
               │
        ┌──────┴──────┐
        ▼             ▼
   Primary DC      Backup DC
      ACTIVE         STANDBY
```

Nếu primary gặp sự cố:

```text
Primary
   X
   │
   ▼
DNS
   │
   ▼
Backup
```

Client được trả về IP của backup.

Tuy nhiên đây **không phải instant failover** vì DNS caching tồn tại.

Ví dụ:

```text
TTL = 300s
```

thì một số resolver/client có thể tiếp tục sử dụng endpoint cũ trong một khoảng thời gian.

---

# 18. Vì sao DNS có thể trở thành bottleneck?

DNS nằm rất gần entry point của Internet.

Nếu DNS infrastructure gặp sự cố:

```text
User
  │
  X
 DNS
```

thì user có thể không resolve được:

```text
www.example.com
```

dù application server vẫn hoàn toàn khỏe.

Đây là một failure mode rất quan trọng:

```text
Application healthy
       │
       │
       ▼
     DNS ❌
       │
       ▼
Users cannot reach application
```

---

# 19. Nhược điểm 1 — DNS lookup latency

DNS lookup tạo thêm latency.

Nếu cache miss:

```text
Client
  ↓
DNS Resolver
  ↓
Root
  ↓
TLD
  ↓
Authoritative DNS
  ↓
IP
  ↓
Application
```

Tuy nhiên caching giúp giảm vấn đề này đáng kể.

Trong trường hợp cache hit:

```text
Client
  ↓
DNS cache
  ↓
IP
```

Do đó DNS được thiết kế dựa rất mạnh vào caching.

---

# 20. Nhược điểm 2 — DNS propagation

Đây là vấn đề đặc biệt quan trọng khi thiết kế deployment.

Giả sử muốn chuyển:

```text
Old Server
10.0.0.1
```

sang:

```text
New Server
10.0.0.2
```

Ta đổi:

```text
www.example.com
        ↓
10.0.0.2
```

nhưng một số cache vẫn có:

```text
www.example.com → 10.0.0.1
```

Do đó trong một khoảng thời gian:

```text
              DNS
               │
       ┌───────┴────────┐
       ▼                ▼
Old Server          New Server
```

Traffic có thể đi tới cả hai.

Đây là lý do DNS cần được xem xét khi triển khai:

* migration
* blue/green deployment
* disaster recovery
* region migration

---

# 21. Nhược điểm 3 — DNS DDoS

DNS infrastructure cũng có thể bị DDoS.

Nếu DNS provider bị tấn công:

```text
Users
  │
  ▼
DNS ❌
  │
  X
Application
```

thì application có thể vẫn chạy nhưng user không thể tìm được IP.

Đây là lý do production systems thường sử dụng:

* multiple authoritative DNS servers
* geographically distributed DNS infrastructure
* Anycast
* DNS caching
* managed DNS providers

Một ví dụ managed DNS phổ biến là [Cloudflare DNS](https://www.cloudflare.com/dns/?utm_source=chatgpt.com) và [Amazon Route 53](https://aws.amazon.com/route53/?utm_source=chatgpt.com).

---

# 22. DNS và Availability

Nếu nhìn từ góc độ System Design, ta có:

$$Availability_{system}
\approx
Availability_{DNS}
\times
Availability_{Network}
\times
Availability_{Application}$$

Đây không phải công thức đánh giá availability hoàn chỉnh trong mọi kiến trúc, nhưng nó giúp hình dung một ý quan trọng:

> Một component ở entry point bị lỗi có thể làm toàn bộ hệ thống trở nên inaccessible.

Do đó DNS cần được thiết kế để **highly available**.

---

# 23. DNS và Scalability

DNS giúp scale hệ thống theo một cách rất đặc biệt.

Thay vì:

```text
www.example.com
      ↓
1 server
```

có thể:

```text
www.example.com
      ↓
DNS
 ┌────┼────┬────┐
 ↓    ↓    ↓    ↓
 A    B    C    D
```

DNS giúp client tìm được một trong nhiều endpoint.

Khi kết hợp với:

```text
DNS
 ↓
CDN
 ↓
Load Balancer
 ↓
Application Servers
 ↓
Database
```

ta có thể xây dựng hệ thống scale rất lớn.

---

# 24. DNS không phải Load Balancer

Đây là một misconception phổ biến.

DNS có thể **phân phối traffic**, nhưng không hoàn toàn giống Load Balancer.

### DNS

Quyết định:

```text
Client → endpoint nào?
```

### Load Balancer

Quyết định:

```text
Request → backend server nào?
```

Ví dụ:

```text
                 DNS
                  │
           ┌──────┴──────┐
           ▼             ▼
        Region A       Region B
           │             │
           ▼             ▼
           LB            LB
        ┌──┴──┐        ┌──┴──┐
        ▼     ▼        ▼     ▼
       S1    S2       S3    S4
```

DNS routing có **coarse-grained control** hơn.

Load Balancer có **fine-grained control** hơn.

---

# 25. Cách tư duy DNS trong System Design Interview

Khi gặp một bài System Design có domain:

```text
example.com
```

hãy tự hỏi:

### Câu hỏi 1

```text
Domain được resolve ở đâu?
```

→ DNS.

### Câu hỏi 2

```text
Có nhiều region không?
```

→ latency/geolocation routing.

### Câu hỏi 3

```text
Có nhiều cluster không?
```

→ weighted routing / load balancing.

### Câu hỏi 4

```text
Có failover không?
```

→ DNS failover.

### Câu hỏi 5

```text
Nếu DNS provider chết thì sao?
```

→ redundancy / multiple DNS servers / managed DNS.

### Câu hỏi 6

```text
DNS cache ảnh hưởng thế nào?
```

→ TTL + propagation delay.

---

# 26. Một ví dụ System Design hoàn chỉnh

Giả sử thiết kế một hệ thống global:

```text
                         Users
                           │
                           ▼
                          DNS
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
          US Region    EU Region     Asia Region
             │             │             │
             ▼             ▼             ▼
             LB            LB            LB
             │             │             │
          ┌──┴──┐        ┌─┴──┐        ┌─┴──┐
          ▼     ▼        ▼    ▼        ▼    ▼
         App   App      App  App      App  App
```

DNS chịu trách nhiệm **global routing**:

$$DNS:
\text{User}
\rightarrow
\text{Region}$$

Load Balancer chịu trách nhiệm **local routing**:

$$LB:
\text{Request}
\rightarrow
\text{Application Server}$$

Đây là cách DNS thường xuất hiện trong kiến trúc distributed system.

---

# 27. Tóm tắt kiến thức cần nhớ

Có thể cô đọng toàn bộ phần DNS thành:

```text
DNS
│
├── Naming
│   └── domain → IP
│
├── Hierarchical
│   ├── Root
│   ├── TLD
│   └── Authoritative DNS
│
├── Caching
│   └── TTL
│
├── Records
│   ├── NS
│   ├── MX
│   ├── A
│   ├── AAAA
│   └── CNAME
│
├── Traffic Routing
│   ├── Weighted
│   ├── Latency-based
│   └── Geolocation-based
│
├── Availability
│   ├── Failover
│   └── Distributed DNS
│
└── Limitations
    ├── Lookup latency
    ├── Propagation delay
    ├── Cache staleness
    └── DDoS
```

### Quan trọng nhất khi học System Design

Bạn nên nhớ chuỗi:

$$\boxed{
DNS
\rightarrow
Global Traffic Routing
\rightarrow
Load\ Balancer
\rightarrow
Application Servers
}$$

và trade-off cốt lõi:

$$\boxed{
TTL \uparrow
\Rightarrow
DNS\ Load \downarrow,\ Freshness \downarrow
}$$

$$\boxed{
TTL \downarrow
\Rightarrow
DNS\ Load \uparrow,\ Failover/Freshness \uparrow
}$$

Nếu học theo **System Design Primer**, DNS nên được đặt trong nhóm **scalability + availability + traffic routing**, chứ không nên chỉ học như một khái niệm networking đơn thuần.
