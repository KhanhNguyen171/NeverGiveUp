# Cache

> **Source:** [System Design Primer – Cache](https://github.com/donnemartin/system-design-primer#cache)

## 1. Tổng quan

**Caching** là kỹ thuật lưu trữ tạm thời những dữ liệu hoặc kết quả được truy cập thường xuyên tại một tầng lưu trữ có tốc độ truy cập nhanh hơn so với nguồn dữ liệu gốc.

Mục tiêu chính của caching là:

* giảm **latency** của request;
* giảm số lượng request tới database;
* giảm tải cho application server;
* hấp thụ các traffic spike;
* cải thiện khả năng mở rộng của hệ thống.

Trong một hệ thống không có cache, request thường phải đi qua toàn bộ pipeline:

```text
Client
   ↓
Web Server
   ↓
Application Server
   ↓
Database
   ↓
Application Server
   ↓
Web Server
   ↓
Client
```

Nếu dữ liệu đã được truy cập trước đó và có thể tái sử dụng, hệ thống có thể đưa cache vào trước database:

```text
Client
   ↓
Web Server
   ↓
Application Server
   ↓
Cache ────── Cache Hit ──────→ Response
   │
   │ Cache Miss
   ↓
Database
   ↓
Cache
   ↓
Response
```

Theo System Design Primer, cache đặc biệt hữu ích khi một số item phổ biến tạo ra **uneven load distribution** trên database. Cache có thể hấp thụ các request tới những dữ liệu "hot", từ đó giảm bottleneck tại database. ([GitHub][1])

---

# 2. Vì sao Cache cải thiện Performance?

Giả sử thời gian xử lý một request là:

$$
T_{request}
=
T_{network}
+
T_{application}
+
T_{database}
$$

Trong nhiều hệ thống, phần truy cập database có thể trở thành bottleneck.

Khi sử dụng cache:

$$
T_{cache}
\ll
T_{database}
$$

Do đó, với một **cache hit**:

$$
T_{request}
\approx
T_{network}
+
T_{application}
+
T_{cache}
$$

thay vì:

$$
T_{request}
\approx
T_{network}
+
T_{application}
+
T_{database}
$$

Điều này đặc biệt có lợi đối với các workload có tính **read-heavy**.

---

## 2.1 Cache Hit và Cache Miss

Hai trạng thái cơ bản:

### Cache Hit

Dữ liệu tồn tại trong cache:

```text
Request
   ↓
Cache
   ↓
 HIT
   ↓
Response
```

Không cần truy cập database.

### Cache Miss

Dữ liệu không tồn tại trong cache:

```text
Request
   ↓
Cache
   ↓
 MISS
   ↓
Database
   ↓
Cache
   ↓
Response
```

Do đó, hiệu quả của cache phụ thuộc lớn vào **cache hit rate**.

Ta định nghĩa:

$$
HitRate =
\frac{N_{hit}}
{N_{hit}+N_{miss}}
$$

và:

$$
MissRate =
\frac{N_{miss}}
{N_{hit}+N_{miss}}
$$

với:

$$
HitRate + MissRate = 1
$$

Một cache có hit rate cao sẽ giảm đáng kể số request phải đi tới database.

---

# 3. Cache trong kiến trúc hệ thống

System Design Primer phân chia cache theo **vị trí đặt cache** thành nhiều tầng. ([GitHub][1])

```text
                ┌─────────────────┐
                │      Client     │
                │ Browser / OS    │
                └────────┬────────┘
                         │
                    Client Cache
                         │
                         ▼
                ┌─────────────────┐
                │      CDN        │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Reverse Proxy   │
                │ / Web Server    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Application     │
                │ Server          │
                └────────┬────────┘
                         │
                    App Cache
                Redis / Memcached
                         │
                         ▼
                ┌─────────────────┐
                │    Database     │
                │ DB Cache        │
                └─────────────────┘
```

Các tầng chính:

1. **Client caching**
2. **CDN caching**
3. **Web server caching**
4. **Database caching**
5. **Application caching**

---

# 4. Client Caching

Client cache nằm ở phía client, ví dụ:

* browser cache;
* operating system cache;
* local application cache.

Luồng:

```text
Client
   │
   ├── Cache Hit → sử dụng dữ liệu local
   │
   └── Cache Miss → gửi request tới server
```

Ưu điểm lớn nhất là request có thể được xử lý **ngay tại client**, không cần đi qua network.

Điều này làm giảm:

$$
Latency_{network}
$$

và:

$$
ServerLoad
$$

---

# 5. CDN Caching

CDN (**Content Delivery Network**) có thể được xem là một dạng distributed cache.

Thay vì client luôn truy cập origin server:

```text
Client
   ↓
Origin Server
```

CDN cho phép:

```text
Client
   ↓
Nearest CDN Edge
   ↓
Cached Content
```

Nếu nội dung chưa có tại edge:

```text
Client
   ↓
CDN Edge
   ↓
Cache Miss
   ↓
Origin Server
   ↓
CDN
   ↓
Client
```

System Design Primer cũng phân loại CDN là một dạng cache. ([GitHub][1])

CDN đặc biệt phù hợp với:

* images;
* JavaScript;
* CSS;
* video;
* static HTML;
* các nội dung có thể cache theo URL.

---

# 6. Web Server Caching

Reverse proxy hoặc web server có thể cache response trước khi request đi tới application server.

Ví dụ:

```text
Client
   ↓
Reverse Proxy
   ↓
Cache
   │
   ├── HIT → Response
   │
   └── MISS
          ↓
      Application
```

Các công nghệ thường gặp gồm:

* Varnish;
* Nginx caching;
* reverse proxy caching.

System Design Primer chỉ ra rằng reverse proxy có thể trực tiếp phục vụ static và dynamic content mà không cần request tới application server. ([GitHub][1])

---

# 7. Database Caching

Database thường đã có một cơ chế cache nội bộ.

Ví dụ:

```text
Application
     ↓
Database
     ↓
┌───────────────┐
│ Database Cache│
└───────────────┘
     ↓
 Disk / Storage
```

Database cache thường lưu các dữ liệu được truy cập thường xuyên trong memory nhằm tránh đọc storage nhiều lần.

Tuy nhiên, database cache là một **implementation detail của database**, trong khi application cache cho phép developer chủ động quyết định:

* cache dữ liệu nào;
* key nào;
* TTL bao lâu;
* eviction policy nào;
* consistency model nào.

---

# 8. Application Caching

Đây là tầng cache quan trọng trong system design.

Các hệ thống phổ biến:

* Redis
* Memcached

Application cache nằm giữa application và persistent storage:

```text
Application
     │
     ▼
┌─────────────┐
│    Cache    │
│ Redis /     │
│ Memcached   │
└──────┬──────┘
       │
       ▼
   Database
```

Dữ liệu được giữ trong RAM nên có latency thấp hơn đáng kể so với việc phải truy cập persistent storage.

System Design Primer nhấn mạnh rằng RAM có dung lượng giới hạn, vì vậy cache cần các thuật toán eviction như **LRU** để giữ dữ liệu "hot" và loại bỏ dữ liệu ít được truy cập. ([GitHub][1])

---

# 9. Redis và Memcached

| Đặc điểm          | Redis                       | Memcached                 |
| ----------------- | --------------------------- | ------------------------- |
| Key-value         | ✓                           | ✓                         |
| In-memory         | ✓                           | ✓                         |
| Persistence       | ✓                           | Không phải mục tiêu chính |
| Data structures   | Nhiều                       | Đơn giản                  |
| Sorted Set        | ✓                           | ✗                         |
| List              | ✓                           | ✗                         |
| Distributed cache | ✓                           | ✓                         |
| Use case          | Cache + nhiều workload khác | Cache đơn giản            |

Theo repository, Redis có thêm **persistence** và các cấu trúc dữ liệu như **sorted sets** và **lists**. ([GitHub][1])

Điểm quan trọng:

> Redis/Memcached không nhất thiết thay thế database.

Thông thường:

```text
Database = Source of Truth

Cache = Fast temporary representation
```

---

# 10. Cache cái gì?

System Design Primer chia caching thành hai nhóm lớn:

1. **Database query**
2. **Object**

Các cấp độ cache có thể gồm: ([GitHub][1])

```text
Row
 ↓
Query Result
 ↓
Object
 ↓
Rendered HTML
```

---

# 11. Caching ở Database Query Level

Ý tưởng:

$$
key = Hash(Query)
$$

Ví dụ:

```text
SELECT * FROM users WHERE id = 123
```

có thể được biến thành:

```text
cache_key = hash(query)
```

và:

```text
cache[cache_key] = query_result
```

Luồng:

```text
Query
  ↓
Hash(Query)
  ↓
Cache
  │
  ├── HIT → Query Result
  │
  └── MISS
       ↓
    Database
       ↓
    Result
       ↓
     Cache
```

## Vấn đề

Query-level caching gặp khó khăn khi dữ liệu thay đổi.

Giả sử:

```text
users
orders
products
```

Một query có thể JOIN cả ba bảng.

Nếu một row trong `users` thay đổi, rất khó xác định chính xác những cached query nào bị ảnh hưởng.

Do đó:

$$
DataUpdate
\Rightarrow
Many\ CachedQueries\ MayBecomeInvalid
$$

Đây là lý do query-level cache có vấn đề về **cache invalidation**. ([GitHub][1])

---

# 12. Caching ở Object Level

Thay vì cache query, application xây dựng một object hoàn chỉnh.

Ví dụ:

```text
Database
   ↓
User Record
   ↓
Application Object
   ↓
Cache
```

Key:

```text
user:12345
```

Value:

```json
{
  "id": 12345,
  "name": "Alice",
  "email": "alice@example.com"
}
```

Khi user thay đổi:

```text
UPDATE user
     ↓
invalidate user:12345
```

Object-level caching thường dễ quản lý hơn query-level caching vì application biết rõ object nào tương ứng với dữ liệu nào.

System Design Primer đề xuất các đối tượng có thể cache như:

* user sessions;
* fully rendered web pages;
* activity streams;
* user graph data. ([GitHub][1])

---

# 13. File-based Cache

File-based caching thường không được ưu tiên trong hệ thống scale lớn.

Ví dụ:

```text
Application Server 1
      ↓
   local cache

Application Server 2
      ↓
   local cache
```

Nếu request chuyển từ Server 1 sang Server 2:

```text
Request
   ↓
Server 2
   ↓
Cache MISS
```

Trong khi dữ liệu có thể đã tồn tại trên Server 1.

Điều này làm horizontal scaling và cloning phức tạp hơn. System Design Primer vì vậy khuyến nghị tránh file-based caching khi có thể. ([GitHub][1])

---

# 14. Cache Eviction

Cache có memory hữu hạn:

$$
Capacity_{cache} \ll Capacity_{database}
$$

Do đó không thể giữ tất cả dữ liệu.

Khi cache đầy:

```text
New Entry
    ↓
Cache Full
    ↓
Eviction Policy
    ↓
Remove Old / Cold Entry
    ↓
Insert New Entry
```

Một policy phổ biến là **LRU — Least Recently Used**.

Ý tưởng:

> Xóa entry đã lâu không được sử dụng.

Nếu cache chứa:

```text
A → B → C → D
```

và `A` là entry được truy cập gần đây nhất:

```text
A → C → D → B
```

thì `B` trở thành ứng viên tốt để eviction.

Có thể biểu diễn:

$$
Evict(x)
=
\arg\min_{x \in Cache} LastAccess(x)
$$

LRU phù hợp với workload có **temporal locality**: dữ liệu vừa được truy cập có xu hướng tiếp tục được truy cập.

---

# 15. Khi nào cập nhật Cache?

Đây là phần quan trọng nhất của cache design.

System Design Primer đưa ra bốn chiến lược:

```text
When to update cache
│
├── Cache-aside
├── Write-through
├── Write-behind / Write-back
└── Refresh-ahead
```

([GitHub][1])

---

# 16. Cache-aside

Cache-aside còn được gọi là **lazy loading**.

Application chịu trách nhiệm điều khiển cả cache và database.

```text
              ┌──────────────┐
              │ Application  │
              └──────┬───────┘
                     │
                 Cache GET
                     │
              ┌──────▼───────┐
              │    Cache     │
              └──────┬───────┘
                     │
             ┌───────┴───────┐
             │               │
           HIT             MISS
             │               │
             ▼               ▼
          Return          Database
                             │
                             ▼
                           Cache
                             │
                             ▼
                           Return
```

Flow:

1. Application kiểm tra cache.
2. Nếu hit → trả dữ liệu.
3. Nếu miss → đọc database.
4. Ghi kết quả vào cache.
5. Trả kết quả.

Pseudo-code:

```python
def get_user(user_id):
    key = f"user.{user_id}"

    user = cache.get(key)

    if user is None:
        user = db.query(
            "SELECT * FROM users WHERE user_id = %s",
            user_id
        )

        if user is not None:
            cache.set(key, json.dumps(user))

    return user
```

Đây chính là flow mà repository sử dụng để minh họa cache-aside. ([GitHub][1])

---

## 16.1 Ưu điểm

### Chỉ cache dữ liệu được sử dụng

Nếu một object chưa bao giờ được request:

```text
Database
   │
   X
 Cache
```

nó không cần xuất hiện trong cache.

Do đó:

$$
Memory_{used}
\downarrow
$$

### Dễ triển khai

Application kiểm soát:

```text
cache.get()
cache.set()
db.query()
```

### Phù hợp read-heavy workload

```text
Read
 ↓
Cache
 ↓
Fast
```

---

## 16.2 Nhược điểm

Cache miss tạo thêm nhiều bước:

```text
Application
    ↓
Cache MISS
    ↓
Database
    ↓
Cache SET
    ↓
Application
```

Do đó latency của miss cao hơn hit.

Ngoài ra, nếu database được cập nhật mà cache chưa được invalidated:

```text
Database = Version 2
Cache    = Version 1
```

thì:

$$
Cache \neq SourceOfTruth
$$

Repository đề cập TTL hoặc write-through như những cách giảm vấn đề stale data. ([GitHub][1])

---

# 17. Write-through

Trong write-through:

```text
Application
     ↓
   Cache
     ↓
Database
```

Application ghi vào cache, sau đó cache **đồng bộ** ghi xuống database.

Flow:

```text
Application
     │
     │ SET
     ▼
   Cache
     │
     │ synchronous write
     ▼
 Database
     │
     ▼
  Return
```

Có thể biểu diễn:

$$
Write_{application}
\rightarrow
Write_{cache}
\rightarrow
Write_{database}
$$

Ví dụ:

```python
def set_user(user_id, values):
    user = db.query(
        "UPDATE Users SET ... WHERE id = %s",
        user_id
    )

    cache.set(user_id, user)
```

Repository nhấn mạnh rằng write-through làm write operation chậm hơn, nhưng những lần đọc ngay sau đó có thể nhanh vì dữ liệu đã tồn tại trong cache. ([GitHub][1])

---

## 17.1 Ưu điểm

Sau khi write hoàn thành:

```text
Cache ≈ Database
```

Do đó giảm khả năng cache chứa dữ liệu cũ.

Đặc biệt hữu ích khi:

```text
Write
 ↓
Read immediately
```

---

## 17.2 Nhược điểm

Nếu application ghi rất nhiều dữ liệu nhưng phần lớn không bao giờ được đọc:

```text
Write A → Cache
Write B → Cache
Write C → Cache
Write D → Cache

        ↓

Không ai đọc A/B/C/D
```

thì cache bị lãng phí.

TTL có thể giúp loại bỏ những entry không được sử dụng. ([GitHub][1])

---

# 18. Write-behind / Write-back

Write-behind chuyển database write thành **asynchronous operation**.

```text
Application
     ↓
   Cache
     │
     │ async
     ▼
  Database
```

Flow:

```text
Application
     ↓
Update Cache
     ↓
Return immediately
     │
     │ asynchronous
     ▼
Database
```

Có thể biểu diễn:

$$
T_{response}
\approx
T_{cache}
$$

thay vì:

$$
T_{response}
\approx
T_{cache}
+
T_{database}
$$

Do đó write performance có thể được cải thiện đáng kể.

---

## 18.1 Ưu điểm

Database write được tách khỏi request path:

```text
Request
   ↓
Cache
   ↓
Response
```

Database:

```text
          ┌───────────────┐
          │ Async Worker  │
          └───────┬───────┘
                  ↓
              Database
```

Điều này rất hữu ích khi database write chậm hoặc có workload write lớn.

---

## 18.2 Nhược điểm

Đây là trade-off quan trọng:

```text
Cache updated
      ↓
Database not yet updated
      ↓
Cache failure
      ↓
Potential data loss
```

Do đó:

$$
Data\ in\ Cache
\neq
Data\ persisted
$$

trong một khoảng thời gian.

System Design Primer xác định **data loss** và **implementation complexity** là hai nhược điểm chính của write-behind. ([GitHub][1])

---

# 19. Refresh-ahead

Refresh-ahead cố gắng cập nhật cache **trước khi entry hết hạn**.

Ví dụ:

```text
TTL = 60 seconds
```

thay vì chờ:

```text
60s → Expire → Cache Miss → Database
```

hệ thống có thể:

```text
50s
 ↓
Refresh
 ↓
New value
 ↓
TTL reset
```

Flow:

```text
             Cache
               │
        approaching expiry
               │
               ▼
        Refresh in background
               │
               ▼
           Database
               │
               ▼
          Updated Cache
```

Mục tiêu:

$$
CacheMissRate \downarrow
$$

và:

$$
Latency \downarrow
$$

Repository chỉ ra rằng refresh-ahead đặc biệt hiệu quả khi hệ thống dự đoán tốt những item sẽ được truy cập tiếp theo. ([GitHub][1])

---

## 19.1 Nhược điểm

Nếu dự đoán sai:

```text
Refresh item
      ↓
Không ai sử dụng
      ↓
Wasted computation
      ↓
Wasted database/cache resources
```

Do đó:

$$
PredictionAccuracy \downarrow
\Rightarrow
RefreshOverhead \uparrow
$$

---

# 20. So sánh các Cache Update Strategy

| Strategy      | Read          | Write              | Consistency          | Complexity | Rủi ro           |
| ------------- | ------------- | ------------------ | -------------------- | ---------- | ---------------- |
| Cache-aside   | Fast sau miss | DB trước/cache sau | Có thể stale         | Thấp       | Cache miss       |
| Write-through | Fast          | Chậm hơn           | Tốt                  | Trung bình | Cache warming    |
| Write-behind  | Fast          | Rất nhanh          | Eventual             | Cao        | Data loss        |
| Refresh-ahead | Rất nhanh     | Tùy implementation | Tốt nếu refresh đúng | Cao        | Refresh lãng phí |

Có thể nhìn theo trục:

```text
                    Consistency
                         ↑
                         │
                 Write-through
                         │
                Cache-aside
                         │
                  Write-behind
                         │
                         └──────────────→ Write Performance
```

Không có strategy nào luôn tốt nhất.

Đây chính là tư duy **trade-off** của system design.

---

# 21. Cache Invalidation

Một trong những vấn đề nổi tiếng nhất của distributed systems là:

> **Cache invalidation**

Giả sử:

```text
Database
user:123 = Alice
```

Cache:

```text
user:123 = Alice
```

User thay đổi:

```text
Database
user:123 = Bob
```

nhưng cache vẫn:

```text
Cache
user:123 = Alice
```

Ta có:

$$
V_{cache} \neq V_{database}
$$

Đây là **stale cache**.

---

## 21.1 TTL

Một giải pháp là **Time-To-Live**.

Mỗi cache entry có:

$$
TTL > 0
$$

Sau khi:

$$
t_{current} - t_{created} > TTL
$$

entry bị xem là expired.

Ví dụ:

```text
user:123
TTL = 300s
```

Sau 5 phút cache entry hết hạn.

### Ưu điểm

Đơn giản.

### Nhược điểm

TTL không đảm bảo consistency ngay lập tức.

Nếu:

```text
Database update
     ↓
Cache vẫn valid
     ↓
User đọc stale data
```

thì stale data vẫn tồn tại cho tới khi TTL hết hạn.

---

# 22. Cache Consistency

Có thể mô hình hóa freshness:

$$
Freshness(t)
=
V_{cache}(t) = V_{source}(t)
$$

Nếu:

$$
V_{cache}(t) \neq V_{source}(t)
$$

thì cache stale.

Các hệ thống phải lựa chọn giữa:

```text
Consistency
     ↕
Performance
```

Ví dụ:

### Stronger consistency

```text
Write DB
   ↓
Invalidate Cache
   ↓
Next Read → DB
```

### Higher performance

```text
Write DB
   ↓
Cache remains
   ↓
Eventually refresh
```

Đây là một trade-off trực tiếp với các consistency patterns trong System Design Primer.

---

# 23. Cache Stampede

Một vấn đề quan trọng cần bổ sung khi học cache là **cache stampede**.

Giả sử:

```text
Popular key = user:123
```

Cache entry đồng thời hết hạn.

Có 10,000 requests:

```text
Request 1 ─┐
Request 2 ─┤
Request 3 ─┤
...        ├──→ Cache MISS
Request N ─┘
               ↓
           Database
```

Tất cả request cùng truy vấn database.

Khi đó:

$$
DatabaseLoad \uparrow\uparrow
$$

Có thể dẫn đến:

```text
Cache Expiration
       ↓
Massive Cache Miss
       ↓
Database Overload
       ↓
Higher Latency
       ↓
Timeout
```

Một hệ thống production thường cần các cơ chế như:

* request coalescing;
* locking;
* single-flight;
* jittered TTL;
* refresh-ahead;
* stale-while-revalidate.

---

# 24. Distributed Cache

Khi hệ thống lớn, một cache node có thể không đủ.

Ta có:

```text
                Application
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
       Cache 1    Cache 2    Cache 3
```

Có ba hướng cơ bản:

### 1. Mỗi node có cache riêng

```text
Cache 1 → Data A
Cache 2 → Data B
Cache 3 → Data C
```

Đơn giản nhưng hit rate có thể thấp.

### 2. Mỗi node chứa toàn bộ cache

```text
Cache 1 → A B C
Cache 2 → A B C
Cache 3 → A B C
```

Dễ sử dụng nhưng tốn memory.

### 3. Sharded cache

```text
Key A → Cache 1
Key B → Cache 2
Key C → Cache 3
```

Thông thường đây là lựa chọn có khả năng scale tốt hơn.

System Design Primer sử dụng chính ý tưởng **sharding + consistent hashing** trong bài toán thiết kế query cache khi cache cần mở rộng lên nhiều máy. ([GitHub][2])

---

# 25. Consistent Hashing

Với distributed cache:

$$
node = hash(key) \bmod N
$$

cách này có vấn đề khi số node thay đổi.

Ví dụ:

```text
N = 3
```

sau đó:

```text
N = 4
```

nhiều key bị remap:

$$
hash(key) \bmod 3
\neq
hash(key) \bmod 4
$$

→ cache hit rate giảm mạnh.

**Consistent hashing** giảm lượng key phải di chuyển khi node được thêm hoặc loại bỏ.

Do đó:

```text
Distributed Cache
       ↓
 Sharding
       ↓
Consistent Hashing
       ↓
Better scalability
```

Trong solution thiết kế query cache của repository, tác giả cũng đề xuất sharding và consistent hashing khi cache cluster cần mở rộng. ([GitHub][2])

---

# 26. Tổng hợp kiến trúc Cache

Một kiến trúc hoàn chỉnh có thể hình dung:

```text
                         Client
                           │
                     Client Cache
                           │
                           ▼
                         CDN
                           │
                           ▼
                    Reverse Proxy
                           │
                           ▼
                    Application
                           │
                    ┌──────┴──────┐
                    │             │
                    ▼             ▼
              Application      Other
                 Cache         Services
              Redis/Memcached
                    │
                    ▼
                Database
                    │
             Database Cache
                    │
                    ▼
               Persistent
                Storage
```

Mỗi tầng giải quyết một loại latency/load khác nhau.

---

# 27. Cache Design theo 3 câu hỏi

Có thể cô đọng toàn bộ phần Cache của System Design Primer thành framework:

```text
                     CACHE
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
      WHERE?         WHAT?        WHEN?
          │            │            │
          ▼            ▼            ▼
       Client        Query       Cache-aside
       CDN           Object      Write-through
       Web Server    HTML        Write-behind
       Database      Session     Refresh-ahead
       Application
```

### WHERE?

> Cache được đặt ở đâu?

### WHAT?

> Cache dữ liệu gì?

### WHEN?

> Cache được đọc/ghi/cập nhật như thế nào?

Đây là cách tốt nhất để tiếp cận bài toán cache trong system design.

---

# 28. Trade-off tổng quát

Caching không phải là "thêm Redis là hệ thống nhanh hơn".

Nó tạo ra một trade-off:

$$
Performance
\uparrow
\quad\Longleftrightarrow\quad
Consistency\ Complexity
\uparrow
$$

và:

$$
DatabaseLoad
\downarrow
\quad\Longleftrightarrow\quad
CacheManagement
\uparrow
$$

Cụ thể:

| Lợi ích                    | Chi phí                      |
| -------------------------- | ---------------------------- |
| Latency giảm               | Cache invalidation           |
| Database load giảm         | Stale data                   |
| Throughput tăng            | Memory giới hạn              |
| Hấp thụ traffic spike      | Eviction                     |
| Scale read workload        | Distributed cache complexity |
| Giảm expensive computation | Cache stampede               |

---

# 29. Nhược điểm của Cache

System Design Primer tổng kết ba vấn đề chính: ([GitHub][1])

### 29.1 Consistency

Phải duy trì:

$$
Cache \leftrightarrow Source\ of\ Truth
$$

### 29.2 Cache invalidation

Phải xác định:

> Khi nào dữ liệu trong cache không còn hợp lệ?

Đây thường là phần khó nhất của cache design.

### 29.3 Application complexity

Thêm Redis/Memcached đồng nghĩa với thêm:

```text
Deployment
Monitoring
Failure handling
Eviction
Expiration
Consistency
Scaling
Serialization
```

Do đó cache phải được thêm khi nó thực sự giải quyết bottleneck.

---

# 30. Góc nhìn System Design

Khi gặp một bài toán system design, không nên bắt đầu bằng:

> "Có nên dùng Redis không?"

Mà nên bắt đầu bằng:

### Bước 1 — Xác định bottleneck

```text
Database quá tải?
Application quá tải?
Network latency?
Expensive computation?
Hot data?
```

### Bước 2 — Xác định workload

$$
Read/Write\ Ratio
$$

Ví dụ:

$$
Reads : Writes = 1000 : 1
$$

→ caching thường rất hấp dẫn.

### Bước 3 — Xác định dữ liệu hot

```text
Hot data
   ↓
Cache

Cold data
   ↓
Database
```

### Bước 4 — Chọn cache location

```text
Client?
CDN?
Web Server?
Application?
Database?
```

### Bước 5 — Chọn cache granularity

```text
Query?
Row?
Object?
HTML?
```

### Bước 6 — Chọn update strategy

```text
Cache-aside?
Write-through?
Write-behind?
Refresh-ahead?
```

### Bước 7 — Xử lý failure

```text
Cache down?
Node down?
Network partition?
Cache miss spike?
Database overload?
```

### Bước 8 — Scale

```text
Single Cache
     ↓
Cluster
     ↓
Sharding
     ↓
Consistent Hashing
```

---

# 31. Cheat Sheet

```text
CACHE
│
├── Why?
│   ├── Reduce latency
│   ├── Reduce database load
│   ├── Increase throughput
│   └── Absorb traffic spikes
│
├── Where?
│   ├── Client
│   ├── CDN
│   ├── Web server
│   ├── Database
│   └── Application
│
├── What?
│   ├── Row
│   ├── Query
│   ├── Object
│   └── Rendered HTML
│
├── Eviction
│   └── LRU
│
├── Update
│   ├── Cache-aside
│   ├── Write-through
│   ├── Write-behind
│   └── Refresh-ahead
│
├── Distributed Cache
│   ├── Replication
│   ├── Sharding
│   └── Consistent hashing
│
└── Problems
    ├── Stale data
    ├── Cache invalidation
    ├── Cache miss
    ├── Cache stampede
    ├── Limited memory
    └── Operational complexity
```

---

## 32. Kết luận

Có thể hiểu **Cache** không đơn giản là một database nhanh hơn, mà là một **performance layer** nằm giữa consumer và source of truth.

Mô hình cốt lõi:

$$
Request
\rightarrow
Cache
\rightarrow
Database
$$

Trong đó:

$$
CacheHit
\Rightarrow
FastResponse
$$

và:

$$
CacheMiss
\Rightarrow
DatabaseAccess
\rightarrow
CacheFill
$$

Toàn bộ phần Cache trong System Design Primer thực chất xoay quanh ba vấn đề nền tảng:

$$
\boxed{\text{Where to cache}}
$$

$$
\boxed{\text{What to cache}}
$$

$$
\boxed{\text{When to update cache}}
$$

Sau đó mới đi tới các vấn đề nâng cao:

$$
\boxed{
Eviction
\rightarrow
Invalidation
\rightarrow
Consistency
\rightarrow
Distribution
\rightarrow
Failure
\rightarrow
Scaling
}
$$

Đặc biệt, **không tồn tại cache strategy tối ưu tuyệt đối**. Cache-aside đơn giản và linh hoạt; write-through ưu tiên consistency; write-behind ưu tiên write performance nhưng chấp nhận rủi ro; refresh-ahead ưu tiên latency nhưng phụ thuộc khả năng dự đoán workload. Đây chính là tư duy **trade-off** mà System Design Primer nhấn mạnh xuyên suốt tài liệu. ([GitHub][1])

### Tài liệu gốc

* [System Design Primer – Cache](https://github.com/donnemartin/system-design-primer?utm_source=chatgpt.com#cache)
* [System Design Primer – Query Cache Design](https://github.com/donnemartin/system-design-primer/tree/master/solutions/system_design/query_cache?utm_source=chatgpt.com)
* [Scalable System Design Patterns](http://horicky.blogspot.com/2010/10/scalable-system-design-patterns.html?utm_source=chatgpt.com)
* [AWS ElastiCache Strategies](https://docs.aws.amazon.com/AmazonElastiCache/latest/UserGuide/Strategies.html?utm_source=chatgpt.com)

[1]: https://github.com/donnemartin/system-design-primer "GitHub - donnemartin/system-design-primer: Learn how to design large-scale systems. Prep for the system design interview. Includes Anki flashcards. · GitHub"
[2]: https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/query_cache/README.md?utm_source=chatgpt.com "system-design-primer/solutions/system_design/query_cache/README.md at master · donnemartin/system-design-primer · GitHub"
