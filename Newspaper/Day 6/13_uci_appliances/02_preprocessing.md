# 02. Preprocessing

## 1. Mục tiêu tiền xử lý

Dựa trên đặc điểm của **Appliances Energy Prediction Dataset** được trình bày ở `13_uci_appliances/01_dataset.md`, dữ liệu có cấu trúc chuỗi thời gian đa biến với chu kỳ quan sát 10 phút. Vì vậy, preprocessing không chỉ nhằm xử lý dữ liệu thiếu hoặc sai lệch mà còn phải **bảo toàn thứ tự thời gian, tránh rò rỉ thông tin tương lai và tạo biểu diễn phù hợp cho bài toán dự báo**.

Trong nghiên cứu này, preprocessing được xây dựng dựa trên các nguyên tắc đã trình bày ở các chương trước:

* **Data Cleaning:** kiểm tra timestamp, dữ liệu thiếu, dữ liệu trùng lặp và tính liên tục của chuỗi.
* **Data Transformation:** chuẩn hóa các biến liên tục nhưng không làm biến dạng các đặc trưng chu kỳ hoặc nhị phân.
* **Feature Engineering:** tạo các đặc trưng thời gian và đặc trưng lịch sử từ dữ liệu đã được kiểm soát.
* **Feature Selection:** giữ lại các nhóm đặc trưng có ý nghĩa đối với bài toán và kiểm soát các biến không mang thông tin dự báo.
* **Temporal Integrity:** mọi phép biến đổi có tham số học từ dữ liệu phải được fitting trên tập Train trước khi áp dụng cho Validation và Test.

Pipeline tổng quát được biểu diễn:

```text
Raw Data
   ↓
Timestamp Validation
   ↓
Data Quality Checks
   ↓
Chronological Split
   ↓
Train-only Transformation
   ↓
Feature Engineering
   ↓
Feature Selection / Representation
   ↓
Sliding Window Construction
   ↓
AI-ready Data
```

Điểm quan trọng là **chronological split phải được xác định trước các bước transformation có học tham số từ dữ liệu**, nhằm tránh data leakage.

---

## 2. Kiểm tra và chuẩn hóa thời gian

Trường `date` là thành phần quan trọng nhất của dataset vì nó xác định thứ tự của các quan sát. Timestamp được chuyển sang kiểu dữ liệu thời gian và sắp xếp theo thứ tự tăng dần:

```python
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)
```

Với hai timestamp liên tiếp $t_i$ và $t_{i+1}$, khoảng thời gian được kiểm tra theo:

$$
\Delta t_i=t_{i+1}-t_i
$$

Dữ liệu được xem là liên tục khi:

$$
\Delta t_i=10\text{ minutes}
$$

Các trường hợp không thỏa mãn điều kiện trên không được tự động nội suy trong bước preprocessing. Thay vào đó, chúng được đánh dấu để xác định các **continuity segments**. Điều này đặc biệt quan trọng khi xây dựng sliding window, vì một cửa sổ không được phép chứa khoảng thời gian bị gián đoạn.

Ngoài ra, timestamp trùng lặp cũng phải được phát hiện:

$$
t_i=t_j,\quad i\neq j
$$

Các bản ghi trùng timestamp cần được kiểm tra trước khi tạo cửa sổ thời gian để tránh tạo ra các mẫu huấn luyện không xác định.

---

## 3. Kiểm tra dữ liệu thiếu

Dataset UCI được công bố không chứa giá trị thiếu trong các trường dữ liệu chính. Tuy nhiên, kiểm tra missing values vẫn được giữ trong pipeline nhằm đảm bảo tính tổng quát của preprocessing.

Với mỗi đặc trưng $X_j$, tỷ lệ missing được xác định bởi:

$$
r_j=\frac{N_{\mathrm{missing},j}}{N}\times100%
$$

Trong đó $N$ là tổng số quan sát.

Nếu missing values xuất hiện do quá trình tái xử lý hoặc chuyển đổi dữ liệu, phương pháp xử lý phải phụ thuộc vào bản chất của biến. Đối với chuỗi thời gian, không nên mặc định sử dụng mean imputation cho mọi biến vì cách này có thể phá vỡ cấu trúc temporal dependency.

Đặc biệt, đối với target:

$$
y_t=\mathrm{Appliances}_t
$$

một quan sát bị thiếu target không được phép được sử dụng trực tiếp làm nhãn huấn luyện.

Do đó, missing-value handling trong nghiên cứu được xem là bước **kiểm soát chất lượng dữ liệu**, thay vì áp dụng một phép imputation cố định cho toàn bộ dataset.

---

## 4. Kiểm tra outlier và noise

Các biến cảm biến như nhiệt độ, độ ẩm, áp suất và tốc độ gió có thể xuất hiện những giá trị bất thường do lỗi cảm biến hoặc quá trình thu thập dữ liệu.

Việc phát hiện outlier được thực hiện dựa trên các phương pháp đã trình bày ở `03_data_cleaning/02_outlier_detection.md`. Một phương pháp phổ biến là IQR:

$$
IQR=Q_3-Q_1
$$

và một quan sát được xem là outlier theo quy tắc:

$$
x<Q_1-1.5IQR\quad\text{hoặc}\quad x>Q_3+1.5IQR
$$

Tuy nhiên, trong dữ liệu năng lượng, một giá trị lớn không nhất thiết là lỗi. Mức tiêu thụ cao có thể phản ánh một sự kiện thực tế. Vì vậy, **outlier detection không đồng nghĩa với outlier removal**.

Trong nghiên cứu này, việc loại bỏ hoặc clipping các giá trị bất thường không được thực hiện một cách tùy tiện. Nếu một quan sát vẫn hợp lệ về mặt vật lý và thời gian, nó được giữ lại để tránh làm thay đổi phân phối thực của dữ liệu.

Điều này cũng phù hợp với nguyên tắc đã xác định trong pipeline: **không clipping prediction trước khi tính metrics**.

---

## 5. Chia dữ liệu theo thời gian

Do đây là bài toán forecasting, dữ liệu được chia theo thứ tự thời gian thay vì random split.

Tập dữ liệu được chia thành ba phần:

$$
D=D_{\mathrm{train}}\cup D_{\mathrm{val}}\cup D_{\mathrm{test}}
$$

với tỷ lệ:

$$
D_{\mathrm{train}}=70%,\quad D_{\mathrm{val}}=15%,\quad D_{\mathrm{test}}=15%
$$

Thứ tự thời gian được bảo toàn:

$$
t_{\mathrm{train}} \lt t_{\mathrm{val}} \lt t_{\mathrm{test}}
$$

Không sử dụng shuffle trong quá trình phân chia dữ liệu.

Điều này đảm bảo rằng mô hình chỉ sử dụng thông tin trong quá khứ để dự báo tương lai. Đặc biệt, **Test set được khóa trong quá trình phát triển preprocessing và model**, chỉ được sử dụng cho đánh giá cuối cùng.

Cách chia này liên kết trực tiếp với nguyên tắc experimental design trong `09_empirical_analysis/01_experimental_setup.md` và tránh leakage giữa các giai đoạn của pipeline.

---

## 6. Scaling và normalization

Sau khi chronological split được xác định, các biến liên tục được scaling dựa **chỉ trên Train set**.

Với Standardization:

$$
x'=\frac{x-\mu_{\mathrm{train}}}{\sigma_{\mathrm{train}}}
$$

trong đó:

$$
\mu_{\mathrm{train}}=\frac{1}{N_{\mathrm{train}}}\sum_{i=1}^{N_{\mathrm{train}}}x_i
$$

và:

$$
\sigma_{\mathrm{train}}=\sqrt{\frac{1}{N_{\mathrm{train}}}\sum_{i=1}^{N_{\mathrm{train}}}(x_i-\mu_{\mathrm{train}})^2}
$$

Các tham số $\mu_{\mathrm{train}}$ và $\sigma_{\mathrm{train}}$ chỉ được ước lượng từ Train:

$$
\theta_{\mathrm{scale}}=f(D_{\mathrm{train}})
$$

Sau đó:

$$
D_{\mathrm{val}}'=f(D_{\mathrm{val}};\theta_{\mathrm{scale}})
$$

và:

$$
D_{\mathrm{test}}'=f(D_{\mathrm{test}};\theta_{\mathrm{scale}})
$$

Validation và Test không được phép tham gia vào quá trình fitting scaler.

Đối với các đặc trưng chu kỳ như:

$$
\mathrm{hour}_{\sin}=\sin\left(2\pi\frac{\mathrm{hour}}{24}\right)
$$

và:

$$
\mathrm{hour}_{\cos}=\cos\left(2\pi\frac{\mathrm{hour}}{24}\right)
$$

các biến này được giữ nguyên thay vì áp dụng StandardScaler lần thứ hai. Tương tự, các biến binary được giữ ở miền giá trị tự nhiên.

---

## 7. Target transformation

Target được định nghĩa:

$$
y_t=\mathrm{Appliances}_t
$$

và được đo bằng Wh.

Nghiên cứu xem xét hai cấu hình target:

* **YS0:** giữ nguyên target ở đơn vị Wh;
* **YS1:** StandardScaler target bằng tham số học từ Train.

Nếu sử dụng YS1:

$$
y_t'=\frac{y_t-\mu_y^{\mathrm{train}}}{\sigma_y^{\mathrm{train}}}
$$

Sau khi mô hình dự báo, kết quả phải được inverse transform về đơn vị Wh trước khi tính các metrics cuối cùng:

$$
\hat{y}_t=\hat{y}_t'\sigma_y^{\mathrm{train}}+\mu_y^{\mathrm{train}}
$$

Điều này đảm bảo rằng MAE và RMSE có thể được diễn giải trực tiếp theo đơn vị năng lượng.

---

## 8. Feature engineering sau preprocessing

Sau khi dữ liệu đã được kiểm soát về chất lượng và transformation, các đặc trưng mới được xây dựng theo nội dung của `05_feature_engineering/`.

Các đặc trưng thời gian được tạo từ timestamp, chẳng hạn:

$$
\mathrm{hour}*{\sin}=\sin\left(2\pi\frac{h}{24}\right),\quad\mathrm{hour}*{\cos}=\cos\left(2\pi\frac{h}{24}\right)
$$

và:

$$
\mathrm{dow}*{\sin}=\sin\left(2\pi\frac{d}{7}\right),\quad\mathrm{dow}*{\cos}=\cos\left(2\pi\frac{d}{7}\right)
$$

Trong đó $h$ là giờ trong ngày và $d$ là ngày trong tuần.

Đối với các đặc trưng lịch sử, lag và rolling chỉ sử dụng thông tin quá khứ. Ví dụ:

$$
\mathrm{lag}*k(t)=y*{t-k}
$$

và rolling mean:

$$
\mathrm{rollmean}*w(t)=\frac{1}{w}\sum*{i=1}^{w}y_{t-i}
$$

Không sử dụng $y_t$ hoặc bất kỳ thông tin nào thuộc tương lai để tạo feature cho thời điểm dự báo.

---

## 9. Feature groups trong nghiên cứu

Để đảm bảo khả năng kiểm soát thực nghiệm, các đặc trưng được tổ chức thành các nhóm:

| Group | Nội dung                               |
| ----- | -------------------------------------- |
| G0    | Metadata và thông tin thời gian cơ bản |
| G1    | Target `Appliances`                    |
| G2    | Raw exogenous features                 |
| G3    | Random control features `rv1`, `rv2`   |
| G4    | Engineered temporal features           |

Cách tổ chức này liên kết trực tiếp với chương `06_feature_selection/`, trong đó feature selection không chỉ được xem là loại bỏ các cột dư thừa mà còn là quá trình xác định **nhóm thông tin nào thực sự được phép đưa vào mô hình**.

Hai biến `rv1` và `rv2` đặc biệt hữu ích như các **control features**. Chúng được giữ trong một số cấu hình nhằm kiểm tra liệu pipeline hoặc mô hình có vô tình khai thác các thuộc tính không mang thông tin dự báo hay không.

---

## 10. Xây dựng sliding windows

Sau khi preprocessing và feature engineering hoàn tất, dữ liệu được chuyển sang dạng sequence-to-one.

Với lookback $L$, input window được định nghĩa:

$$
\mathbf{X}*{t-L+1:t}=\left[\mathbf{x}*{t-L+1},\mathbf{x}*{t-L+2},\ldots,\mathbf{x}*{t}\right]
$$

Target tương ứng là:

$$
y_{t+1}=\mathrm{Appliances}_{t+1}
$$

Do dữ liệu có chu kỳ 10 phút và $H=1$, mỗi mẫu thực hiện dự báo mức tiêu thụ tại thời điểm tiếp theo.

Ba lookback được sử dụng:

$$
L\in{36,72,144}
$$

tương ứng với 6 giờ, 12 giờ và 24 giờ dữ liệu lịch sử.

Một window chỉ hợp lệ khi:

1. Có đủ $L$ quan sát lịch sử.
2. Timestamp liên tục với khoảng cách 10 phút.
3. Input và target thuộc cùng một continuity segment.
4. Không tồn tại timestamp trùng lặp.
5. Target tồn tại và hợp lệ.

Do đó, một window không hợp lệ sẽ bị loại khỏi tập mẫu thay vì tự động điền dữ liệu thiếu thời gian.

---

## 11. Data leakage control

Data leakage là một trong những rủi ro quan trọng nhất của preprocessing cho forecasting.

Pipeline áp dụng nguyên tắc:

$$
\boxed{\mathrm{Fit\ preprocessing\ parameters\ on\ Train\ only}}
$$

Điều này áp dụng cho:

* scaling;
* normalization có tham số;
* target transformation;
* các thống kê được sử dụng để tạo feature;
* các bước feature selection có học từ dữ liệu.

Đặc biệt, không được tính mean, standard deviation, correlation hoặc feature importance trên toàn bộ dataset trước khi chia Train/Validation/Test.

Quy trình đúng là:

```text
Raw Data
   ↓
Temporal Validation
   ↓
Chronological Split
   ↓
Fit preprocessing on Train
   ↓
Transform Validation/Test
   ↓
Feature Engineering
   ↓
Window Construction
   ↓
Model
```

Cách tiếp cận này đảm bảo rằng thông tin từ Validation và Test không ảnh hưởng đến quá trình học preprocessing.

---

## 12. Kết nối với pipeline nghiên cứu

Preprocessing của UCI Appliances được xây dựng như một trường hợp cụ thể của pipeline tổng quát được trình bày trong `11_pipeline/`.

Có thể ánh xạ như sau:

| Pipeline tổng quát  | UCI Appliances                            |
| ------------------- | ----------------------------------------- |
| Data Cleaning       | Timestamp, duplicate, missing, continuity |
| Transformation      | StandardScaler cho continuous features    |
| Feature Engineering | Temporal, lag, rolling features           |
| Feature Selection   | Feature groups và control variables       |
| Representation      | Sliding windows                           |
| AI-ready Data       | Tensor dạng `[N, L, F]`                   |

Sau bước preprocessing, mỗi mẫu dữ liệu có dạng:

$$
\mathbf{X}\in\mathbb{R}^{L\times F}
$$

trong đó $L$ là lookback và $F$ là số lượng đặc trưng.

Tập dữ liệu cuối cùng được sử dụng cho mô hình có dạng:

$$
\mathcal{D}=\left\{\left(\mathbf{X}_{t-L+1:t},y_{t+1}\right)\right\}_{t=1}^{N}
$$

Đây là biểu diễn cuối cùng được chuyển sang bước modeling và evaluation trong `09_empirical_analysis/`.

---

## 13. Tóm tắt

Preprocessing đối với UCI Appliances không được thực hiện như một chuỗi các phép biến đổi độc lập mà được xây dựng thành một pipeline có thứ tự và kiểm soát leakage. Trọng tâm của pipeline là **bảo toàn temporal structure**, **fit transformation trên Train בלבד**, **phân biệt các loại feature**, và **chuyển dữ liệu bảng thành sequence phù hợp với forecasting**.

Kết quả của bước này là dữ liệu đã được kiểm soát chất lượng, transformation nhất quán và biểu diễn dưới dạng:

$$
\mathbf{X}*{t-L+1:t}\rightarrow y*{t+1}
$$

với $L\in{36,72,144}$. Đây là đầu vào trực tiếp cho bước **feature engineering và modeling thực nghiệm**, đồng thời tạo cầu nối giữa survey lý thuyết ở các chương trước và case study UCI Appliances ở chương này.
