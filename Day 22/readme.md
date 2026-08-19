# invalidating cache & đặt tên biến

## 1. Invalidating Cache

### Cache là gì?

Cache là việc lưu lại kết quả đã tính để lần sau không phải tính lại.

Ví dụ một pipeline đơn giản:

```
Raw Data
   ↓
Preprocessing
   ↓
Feature Engineering
   ↓
Model
   ↓
Prediction
```

Nếu feature engineering mất 20 phút, ta có thể cache kết quả: `features.parquet` và lần chạy sau chỉ cần: `Raw Data → [cached features] → Model` thay vì phải run lại pipeline

Một vấn đề về version nên được chú ý: khi ta từ .csv qua một feature_engineering_v1() lưu ra features.parquet sau đó ta nâng cấp feature_engineering_v2() nhưng input là features.parquet của version cũ thì đây chính là cache invalidation -> `Khi nào một cached result không còn hợp lệ và phải được tính lại?`. Nó không gây Crash mà tạo ra một kết quả hợp lệ nhưng về mặt kỹ thuật lại sai về mặt khoa học.

Ta nên xác định cache dựa trên dependence của nó ví dụ: `features.parquet` phụ thuộc vào: `raw_data, preprocessing_code, feature_config, dataset_version` nếu bất kỳ mục nào thay đổi thì `→ cache invalid, recompute`. Ta có thể xác định một hàm biểu diễn:

$$C = f(D, P, F, V)$$

Trong đó:
- $D$: input data
- $P$: preprocessing logic
- $F$: Configuration/features
- $V$: Version

Ta có thể lưu vào .json và Quy định một Cache hợp lệ nếu các dependency khớp version với nhau

Ví dụ một manifest:
``` Json
{
    "dataset_version": "DATA-v3",
    "feature_version": "FEATURE-v2",
    "preprocessing_version": "PREP-v4"
}
```

## 2. Đặt tên biến

Ở mức basic khi làm việc với Machine Learning ta thường đặt tên biến:

```py
X_train
X_val
X_test
```

Nhưng chưa chắc đã là đủ khi ta làm việc với các project lớn hơn, nếu pipeline có scaling thì ta cần thêm:

```py
X_train_raw
X_train_scaled

y_train_wh
y_train_scaled
```

Để ta xác định được:

```
raw       → dữ liệu gốc
scaled    → dữ liệu đã chuẩn hóa
train     → thuộc Train
val       → thuộc Validation
wh        → đơn vị vật lý
```

Những quy chuẩn này giúp quá trình code được minh bạch và debug trở nên dễ dàng khi xác định rõ là biến nào đang gặp vấn đề.

có thể tuân theo một số quy tắc như sau: 

- Quy tắc 1: Tên phải nói lên vai trò của
- Quy tắc 2: hàm = ĐỘNG TỪ, Biến = DANH TỪ
    - phân rõ ra: hàm làm biệc, hàm kiểm tra, biến lưu trữ
- Quy tắc 3: Tên có độ dài vừa phải và minh bạch
- Quy tắc 4: Tính nhất quán giữa phong cách đặt tên
- Quy tắc 5: Trách các tên gây hiểu nhầm