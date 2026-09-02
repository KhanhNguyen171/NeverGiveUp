# Reverse Proxy

Phần **Reverse Proxy** trong *System Design Primer* rất quan trọng vì nó nằm ở lớp **entry point** của hệ thống: client không nhất thiết truy cập trực tiếp vào application server, mà đi qua một thành phần trung gian đứng trước backend.

Điểm cần phân biệt rõ là:

> **Reverse proxy là một vai trò/chức năng kiến trúc; load balancer là một chức năng phân phối traffic. Hai chức năng này có thể được triển khai bởi cùng một phần mềm như NGINX hoặc HAProxy.**

Dưới đây là cách phân tích lại theo đúng cấu trúc của phần trong GitHub, nhưng giải thích sâu hơn để có thể đưa vào báo cáo.

---

## 1. Reverse Proxy là gì?

![Image](https://images.openai.com/static-rsc-4/95HJd9vbghyJ2tve3KedtI24E9VlxhgUbXfiE4xbGWpIftkAFdzFUPbdsHhKauqEn9FcbiGQnDXWDZV1Gn2p6xEXoJj58BXwA77HajQL15MECnshQ5NhFTooqCm7UNcalP66G83wNmmSB3ALTivMn2qi-T6nRPmMk-vJvGCGNJuk0vrXRVI7TCYHBFsf8Qnr?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/zO_rY60-iOa2KA1HEzzT25nxJ2OE-j6nL4sLrq85Mjr2u-zOxQDbiL1SAGCmslDVbUxAfwqhFVYF-JjKJMBovMFw08HNCslHO14xpU94cQP5DRGjkJnbJtrIH9djqmi9mtYSa_4BSho1cw6qDdi6Dn86vhuama23tPdWdLi56gLZP7fawow0qQ8Cr2kZGpZa?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/caCKW7s6Btf316reP5886YRGoUfQgUgQqAdAA7l4zAR8Hdpxoikpilfz0S-B6qFnjcTTg2Dh6I22oe1BoOlmFpIKjoSVqBe6IkcZB9WZKyLrn9BilZJh86q6Ln2q5AV7UxSDe0V8QYuKBYTWe55EQDlhz8TJhPhsHiZdi8S0FpUCLKUpDpHTOhIgjzzt47mH?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/JCJi_PH0A7mRlikUSbR0oO4sfgOZNBv6-2sZi49dqmn8jaAnZAev3GVXKXx9TMWayQ4FK5U_HcDnWQxwLRPUPhL9ONDb79GfzgE7dCNkq4MSFUbROTTbCrUh1VQJDrGKaFoPeSyKR7mQulEZYU_65W_h9wnkS8Ec1AAtOO62MIMso-TRt1zfCmbUVYchhl20?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/CTkk6pK8rAUx0UU0hb8R3Dm6S6F_YIUAmE5uhiI2BgNiTDQ9z6TIETd7e3R3kO6oZWoZosHcaElZ30YhKQwO2WDD573QlNaP5lhvuh9PimK0SX7Fu42bJm3hm5fYxYgsNro_v94LlGuG7moC6_84Rr1yHzADn7hs4kXndQtO3jEfkyc4Cg-jtG1Y4KD5qgNZ?purpose=fullsize)

**Reverse proxy** là một server nằm ở phía trước các server nội bộ (**backend servers**), đóng vai trò là **điểm tiếp nhận request từ client**.

Thay vì:

```text
Client
   |
   v
Application Server
```

kiến trúc có reverse proxy sẽ trở thành:

```text
Client
   |
   v
Reverse Proxy
   |
   v
Application Server
```

Client chỉ biết đến địa chỉ của reverse proxy. Reverse proxy tiếp nhận request, quyết định request nên được xử lý như thế nào, sau đó chuyển tiếp request đến backend phù hợp.

Luồng cơ bản:

```text
Client
   |
   | HTTP/HTTPS Request
   v
+-------------------+
|   Reverse Proxy   |
+-------------------+
          |
          | Forward request
          v
+-------------------+
| Backend Server    |
| Application       |
+-------------------+
          |
          | Response
          v
+-------------------+
|   Reverse Proxy   |
+-------------------+
          |
          | Response
          v
       Client
```

Điểm quan trọng là **reverse proxy đại diện cho backend trước client**.

Ví dụ:

```text
https://example.com
       |
       v
  Reverse Proxy
       |
       +------> API Server
       |
       +------> Web Server
       |
       +------> Image Server
```

Client không cần biết các backend server này tồn tại ở đâu hoặc có bao nhiêu server.

---

## 2. Vì sao cần Reverse Proxy?

Nếu client truy cập trực tiếp vào backend, kiến trúc đơn giản:

```text
Client ---> Application Server
```

nhưng backend phải tự xử lý rất nhiều trách nhiệm:

* TLS/SSL
* authentication
* connection management
* compression
* caching
* static files
* request routing
* security filtering
* traffic distribution

Khi hệ thống lớn lên, việc để application server xử lý tất cả các nhiệm vụ này không tối ưu.

Reverse proxy cho phép tách các trách nhiệm đó:

```text
                  +-------------------+
                  |   Reverse Proxy   |
                  |-------------------|
                  | TLS termination   |
                  | Caching           |
                  | Compression       |
                  | Routing           |
                  | Security          |
                  | Static content    |
                  +-------------------+
                           |
              +------------+------------+
              |            |            |
              v            v            v
          Server A     Server B     Server C
```

Do đó, reverse proxy không đơn thuần là "server chuyển tiếp request", mà là một **abstraction layer giữa public network và internal infrastructure**.

---

## 3. Các lợi ích chính

### 3.1. Increased Security

Một reverse proxy giúp **ẩn infrastructure phía sau nó**.

Ví dụ backend có:

```text
10.0.1.10
10.0.1.11
10.0.1.12
```

Client không cần biết những địa chỉ này.

Thay vào đó:

```text
Client
   |
   v
example.com
   |
   v
Reverse Proxy
   |
   +----> 10.0.1.10
   +----> 10.0.1.11
   +----> 10.0.1.12
```

Điều này tạo ra một abstraction boundary:

$$
\text{Client} \rightarrow \boxed{\text{Reverse Proxy}} \rightarrow \text{Internal Infrastructure}
$$

Reverse proxy có thể thực hiện các chính sách như:

* blacklist IP;
* rate limiting;
* giới hạn số connection;
* filtering request;
* kiểm tra header;
* chặn traffic bất thường;
* ẩn topology của backend.

Tuy nhiên, cần hiểu chính xác:

> **Reverse proxy không tự động biến hệ thống thành secure.**

Nó chỉ tạo ra một lớp có thể tập trung các cơ chế bảo vệ.

---

## 4. Increased Scalability and Flexibility

Một trong những lợi ích lớn nhất là **client không phụ thuộc trực tiếp vào backend**.

Giả sử ban đầu:

```text
Client
   |
   v
Reverse Proxy
   |
   v
Server A
```

Khi traffic tăng, ta có thể thêm:

```text
Client
   |
   v
Reverse Proxy
   |
   +------> Server A
   |
   +------> Server B
   |
   +------> Server C
```

Client vẫn gửi request tới cùng một endpoint:

```text
https://example.com
```

Không cần biết backend đã thay đổi từ:

```text
Server A
```

thành:

```text
Server A
Server B
Server C
```

Đây chính là **decoupling** giữa client và backend.

Có thể biểu diễn:

$$
\text{Client} \not\rightarrow \text{Backend directly}
$$

mà:

$$
\text{Client}
\rightarrow
\text{Reverse Proxy}
\rightarrow
\text{Backend Pool}
$$

Do đó backend có thể:

* scale out;
* thay đổi IP;
* thay đổi server;
* deploy phiên bản mới;
* thay đổi topology;

mà client không cần biết.

---

## 5. SSL Termination

Đây là một chức năng rất phổ biến của reverse proxy.

Nếu không có reverse proxy:

```text
Client
   |
 HTTPS
   |
   v
Application Server
```

application server phải thực hiện:

1. nhận encrypted traffic;
2. TLS handshake;
3. decrypt request;
4. xử lý application logic;
5. encrypt response;
6. gửi response.

Nếu có reverse proxy:

```text
Client
   |
 HTTPS
   v
+------------------+
| Reverse Proxy    |
| TLS termination  |
+------------------+
   |
 HTTP / HTTPS
   |
   v
Application Server
```

Reverse proxy thực hiện TLS termination.

Nói cách khác:

$$
\text{HTTPS}_{client}
\rightarrow
\text{TLS Termination}
\rightarrow
\text{HTTP/HTTPS}_{backend}
$$

Ví dụ:

```text
Client
   |
   | HTTPS
   v
NGINX
   |
   | HTTP
   v
Application
```

Trong trường hợp này, certificate không cần được cài trên từng application server.

Điều này đặc biệt hữu ích khi có nhiều backend:

```text
             HTTPS
Client ----------------> NGINX
                           |
                  +--------+--------+
                  |        |        |
                  v        v        v
                App A    App B    App C
```

Certificate được quản lý tập trung tại NGINX.

### Nhưng có một điểm cần lưu ý

SSL termination **không có nghĩa traffic giữa reverse proxy và backend bắt buộc phải là HTTP**.

Trong môi trường production, có thể sử dụng:

```text
Client
   |
 HTTPS
   v
Reverse Proxy
   |
 HTTPS
   v
Backend
```

Đây là mô hình **TLS passthrough/end-to-end encryption ở mức ứng dụng**, hoặc TLS được terminate rồi re-encrypt tới backend.

---

## 6. Compression

Reverse proxy cũng có thể thực hiện compression trước khi gửi response tới client.

Không compression:

```text
Backend
   |
   | 10 MB
   v
Reverse Proxy
   |
   | 10 MB
   v
Client
```

Có compression:

```text
Backend
   |
   | 10 MB
   v
Reverse Proxy
   |
   | 2 MB
   v
Client
```

Mục tiêu là giảm:

$$
\text{Network Bandwidth}
$$

và thường cải thiện:

$$
\text{Transfer Time}
$$

Đặc biệt hữu ích đối với:

* HTML;
* CSS;
* JavaScript;
* JSON;
* text-based responses.

Ví dụ:

```text
Client
   |
   | Accept-Encoding: gzip
   v
Reverse Proxy
   |
   | gzip response
   v
Client
```

Thay vì để từng application server tự xử lý compression, reverse proxy có thể tập trung chức năng này.

---

## 7. Caching

Reverse proxy có thể lưu response vào cache.

Không có cache:

```text
Client
   |
   v
Reverse Proxy
   |
   v
Backend
   |
   v
Database
```

Mỗi request đều phải đi tới backend.

Có cache:

```text
Client
   |
   v
Reverse Proxy
   |
   +---- Cache HIT ----> Response
   |
   +---- Cache MISS ---> Backend
```

Nếu response tồn tại trong cache:

$$
\text{Request}
\rightarrow
\text{Cache HIT}
\rightarrow
\text{Response}
$$

thì backend không cần xử lý request đó.

Ngược lại:

$$
\text{Request}
\rightarrow
\text{Cache MISS}
\rightarrow
\text{Backend}
\rightarrow
\text{Cache}
\rightarrow
\text{Client}
$$

Caching giúp:

* giảm load backend;
* giảm database queries;
* giảm latency;
* tăng throughput.

Nhưng cache cũng tạo ra một trade-off quan trọng:

$$
\text{Performance}
\leftrightarrow
\text{Freshness}
$$

Dữ liệu cache có thể cũ hơn dữ liệu trong database.

---

## 8. Static Content

Reverse proxy cũng có thể trực tiếp phục vụ static files.

Ví dụ:

```text
/static/app.js
/static/style.css
/images/logo.png
/videos/demo.mp4
```

thay vì:

```text
Client
   |
   v
Reverse Proxy
   |
   v
Application
   |
   v
File System
```

có thể:

```text
Client
   |
   v
Reverse Proxy
   |
   +----> Static files
   |
   +----> Application
```

Ví dụ:

```text
Client
   |
   v
NGINX
   |
   +---- /style.css ------> Static File
   |
   +---- /app.js ---------> Static File
   |
   +---- /api/users ------> Backend
```

Đây là một dạng **request routing**.

Quy tắc có thể được mô hình hóa:

$$
f(\text{request}) =
\begin{cases}
\text{Static Server}, & \text{if request is static}\\
\text{Application Server}, & \text{if request is dynamic}
\end{cases}
$$

Như vậy application server chỉ tập trung vào dynamic requests.

---

## 9. Reverse Proxy vs Load Balancer

Đây là phần dễ gây nhầm lẫn nhất.

### 9.1. Load Balancer

Load balancer tập trung vào việc:

> **phân phối traffic giữa nhiều backend server.**

Ví dụ:

```text
              +--> Server A
              |
Client --> LB +--> Server B
              |
              +--> Server C
```

Mục tiêu chính:

$$
\text{Distribute Load}
$$

Ví dụ request được phân phối:

```text
Request 1 --> Server A
Request 2 --> Server B
Request 3 --> Server C
Request 4 --> Server A
```

---

### 9.2. Reverse Proxy

Reverse proxy có phạm vi rộng hơn.

Nó có thể:

```text
Client
   |
   v
Reverse Proxy
   |
   +--> Authentication
   +--> TLS termination
   +--> Compression
   +--> Caching
   +--> Static content
   +--> Routing
   +--> Backend
```

Reverse proxy **không bắt buộc phải có nhiều backend**.

Ngay cả:

```text
Client
   |
   v
Reverse Proxy
   |
   v
One Application Server
```

vẫn có ý nghĩa.

---

## 10. Quan hệ giữa Reverse Proxy và Load Balancer

Điểm quan trọng cần ghi nhớ:

> **Load balancing có thể là một chức năng của reverse proxy.**

Do đó hai khái niệm không hoàn toàn loại trừ nhau.

Có thể có:

```text
                    Reverse Proxy
                         |
             +-----------+-----------+
             |           |           |
             v           v           v
           App A       App B       App C
```

Reverse proxy đồng thời thực hiện load balancing.

Khi đó:

$$
\text{Reverse Proxy}
=
\text{Proxy}
+
\text{Routing}
+
\text{Load Balancing}
+
\text{Caching}
+
\text{TLS}
+\cdots
$$

Trong khi load balancer có thể chỉ tập trung vào:

$$
\text{Load Balancer}
\rightarrow
\text{Traffic Distribution}
$$

---

## 11. Một ví dụ thực tế

Giả sử một website có kiến trúc:

```text
                         Internet
                            |
                            v
                    +---------------+
                    | Reverse Proxy |
                    |    NGINX      |
                    +---------------+
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
           App 1          App 2         App 3
              |             |             |
              +-------------+-------------+
                            |
                            v
                         Database
```

NGINX có thể thực hiện đồng thời:

### TLS

```text
HTTPS --> NGINX
```

### Routing

```text
/api/*       --> Application
/static/*    --> Static files
```

### Load balancing

```text
/api/users

        +--> App 1
        +--> App 2
        +--> App 3
```

### Caching

```text
GET /api/products
        |
        v
     Cache?
      /   \
    HIT   MISS
    |       |
 Response  Backend
```

### Compression

```text
Backend Response
       |
       v
   Compression
       |
       v
     Client
```

Do đó reverse proxy trở thành **control point** của traffic vào hệ thống.

---

## 12. Disadvantages

### 12.1. Increased Complexity

Thêm reverse proxy nghĩa là thêm một infrastructure component:

```text
Client
   |
   v
Reverse Proxy
   |
   v
Application
```

thay vì:

```text
Client
   |
   v
Application
```

Vì vậy phải quản lý thêm:

* configuration;
* monitoring;
* deployment;
* logs;
* certificates;
* health checks;
* failure handling.

---

## 13. Single Point of Failure

Nếu chỉ có một reverse proxy:

```text
             +-------------+
Client ----> |   Proxy     |
             +-------------+
                    |
                    v
                Backend
```

Proxy chết:

```text
Client -X-> Reverse Proxy -X-> Backend
```

thì toàn bộ hệ thống có thể không truy cập được.

Do đó reverse proxy trở thành:

$$
\boxed{\text{Single Point of Failure}}
$$

### Giải pháp

Có thể triển khai nhiều reverse proxy:

```text
                  Client
                    |
                    v
             +-------------+
             | Load Balancer|
             +-------------+
                /       \
               v         v
          Proxy A      Proxy B
             |            |
             +------+-----+
                    |
                    v
                 Backend
```

Nhưng điều này lại làm kiến trúc phức tạp hơn.

Đây chính là trade-off:

$$
\text{High Availability}
\leftrightarrow
\text{Architectural Complexity}
$$

---

## 14. Kiến trúc tổng quát cần ghi nhớ

Có thể tóm tắt reverse proxy bằng mô hình:

```text
                         CLIENTS
                            |
                            v
                 +----------------------+
                 |    REVERSE PROXY     |
                 +----------------------+
                 |                      |
                 | TLS termination      |
                 | Routing              |
                 | Load balancing       |
                 | Caching              |
                 | Compression          |
                 | Security filtering   |
                 | Static content       |
                 +----------------------+
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
         Backend A      Backend B      Backend C
             |              |              |
             +--------------+--------------+
                            |
                            v
                         Database
```

Tư tưởng kiến trúc quan trọng nhất là:

$$
\boxed{
\text{Client}
\rightarrow
\text{Reverse Proxy}
\rightarrow
\text{Internal Services}
}
$$

Reverse proxy tạo ra **một lớp trung gian**, giúp client được tách khỏi implementation và topology thực tế của backend.

---

## 15. Reverse Proxy trong toàn bộ System Design

Nếu đặt nó vào một hệ thống lớn hơn, ta có thể thấy vị trí của reverse proxy như sau:

```text
                         Users
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
              +------------+------------+
              |            |            |
              v            v            v
           API Server   API Server   API Server
              |            |            |
              +------------+------------+
                           |
                           v
                    Cache / Database
```

Tuy nhiên **không phải hệ thống nào cũng cần tất cả các lớp này**.

Một hệ thống nhỏ có thể chỉ cần:

```text
Client
  |
  v
Reverse Proxy
  |
  v
Application
```

Hệ thống lớn hơn:

```text
Client
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
  +----> App 1
  +----> App 2
  +----> App 3
```

Và trong nhiều kiến trúc, **Load Balancer và Reverse Proxy có thể được gộp thành một thành phần**, đặc biệt khi sử dụng các giải pháp như NGINX hoặc HAProxy.

---

## 16. Các liên kết học tập trong GitHub

Phần này nằm trong **System Design Primer** của Donne Martin:

[System Design Primer – GitHub](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com)

Các tài liệu mà phần Reverse Proxy tham chiếu gồm:

* [Reverse proxy vs. load balancer – NGINX](https://www.nginx.com/resources/glossary/reverse-proxy-vs-load-balancer/?utm_source=chatgpt.com)
* [Inside NGINX: How We Designed for Performance & Scale](https://www.nginx.com/blog/inside-nginx-how-we-designed-for-performance-scale/?utm_source=chatgpt.com)
* [HAProxy Architecture Guide](http://www.haproxy.org/download/1.2/doc/architecture.txt?utm_source=chatgpt.com)
* [Reverse Proxy – Wikipedia](https://en.wikipedia.org/wiki/Reverse_proxy?utm_source=chatgpt.com)

### Ý chính nên ghi nhớ

| Thành phần          | Mục tiêu chính                                  |
| ------------------- | ----------------------------------------------- |
| **Reverse Proxy**   | Trung gian giữa client và backend               |
| **Load Balancer**   | Phân phối request tới nhiều backend             |
| **CDN**             | Đưa content gần user hơn                        |
| **Cache**           | Giảm số request phải xử lý bởi backend          |
| **SSL Termination** | Xử lý TLS tập trung                             |
| **Static Server**   | Phục vụ static content mà không cần application |

Và điểm quan trọng nhất:

$$
\boxed{
\text{Reverse Proxy} \neq \text{Load Balancer}
}
$$

nhưng:

$$
\boxed{
\text{Reverse Proxy có thể thực hiện Load Balancing}
}
$$

Do đó khi thiết kế hệ thống, không nên hỏi đơn giản **"reverse proxy hay load balancer?"**, mà nên xác định **thành phần đó cần đảm nhận những responsibilities nào**. NGINX và HAProxy là những ví dụ điển hình có thể đảm nhận nhiều vai trò cùng lúc.
