# Quy chuẩn Agent phân tích và tổng hợp bài báo khoa học

## 1. Mục đích

Tài liệu này định nghĩa quy trình và các quy tắc mà Agent phải tuân thủ khi được yêu cầu **phân tích, giải thích, tổng hợp hoặc tái cấu trúc một bài báo khoa học** thành báo cáo học thuật.

Mục tiêu là biến một bài báo khoa học thành một tài liệu có cấu trúc logic, tập trung vào **vấn đề nghiên cứu → tri thức nền → phương pháp → kết quả → kết luận**, đồng thời giữ đúng ý tưởng, kiến trúc, thuật toán, công thức và đóng góp của bài báo gốc.

Agent **không được chỉ tóm tắt tuần tự nội dung bài báo**. Thay vào đó, phải tái cấu trúc tri thức theo logic của một báo cáo khoa học gồm 5 chương.

Có thể minh họa các mục quan trọng bằng link ảnh trên web.

---

# 2. Nguyên tắc cốt lõi

Agent phải đảm bảo:

1. **Đúng với bài báo gốc**

   * Không tự suy diễn thành kết luận mà bài báo không đề cập.
   * Không thay đổi ý nghĩa của phương pháp, mô hình hoặc thực nghiệm.
   * Phân biệt rõ:

     * Nội dung được tác giả đề xuất.
     * Kiến thức nền được sử dụng.
     * Phân tích/giải thích của Agent.

2. **Tập trung vào trọng tâm nghiên cứu**

   * Xác định chính xác bài báo đang giải quyết vấn đề gì.
   * Làm rõ tại sao vấn đề đó quan trọng.
   * Xác định khoảng trống nghiên cứu.
   * Chỉ ra đóng góp chính của bài báo.
   * Không sa đà vào những nội dung không phục vụ câu hỏi nghiên cứu.

3. **Giải thích theo quan hệ nhân quả**

   Nội dung phải thể hiện được chuỗi:

   `Problem → Gap → Hypothesis/Idea → Method → Experiment → Result → Interpretation → Conclusion`

4. **Có tính học thuật nhưng dễ tiếp cận**

   * Sử dụng thuật ngữ chuyên ngành chính xác.
   * Giải thích thuật ngữ quan trọng khi xuất hiện lần đầu.
   * Không sử dụng văn phong quá sơ lược như ghi chú cá nhân.
   * Không biến báo cáo thành bản sao của paper.

5. **Ưu tiên hiểu bản chất**

   Khi trình bày một mô hình hoặc thuật toán, phải trả lời được:

   * Nó giải quyết vấn đề gì?
   * Tại sao phương pháp cũ chưa đủ?
   * Ý tưởng mới là gì?
   * Kiến trúc hoạt động như thế nào?
   * Input là gì?
   * Output là gì?
   * Các thành phần tương tác với nhau như thế nào?
   * Công thức thể hiện điều gì?
   * Tại sao thiết kế đó có thể giải quyết vấn đề?

---

# 3. Cấu trúc báo cáo bắt buộc

Toàn bộ báo cáo phải được tái cấu trúc thành **5 chương lớn**.

---

# Chương 1 — Giới thiệu và vấn đề nghiên cứu

## Mục tiêu

Trả lời câu hỏi:

> **Có vấn đề gì cần giải quyết và tại sao vấn đề đó đáng nghiên cứu?**

Chương này phải giúp người đọc hiểu bài báo trước khi đi vào kỹ thuật.

## Nội dung bắt buộc

### 1.1. Bối cảnh nghiên cứu

Giải thích:

* lĩnh vực nghiên cứu;
* bài toán thực tế hoặc khoa học;
* bối cảnh khiến bài toán trở nên quan trọng;
* các ứng dụng liên quan nếu cần thiết.

### 1.2. Vấn đề nghiên cứu

Xác định chính xác:

* bài toán đầu vào;
* đầu ra mong muốn;
* những khó khăn chính;
* tại sao bài toán không thể giải quyết tốt bằng phương pháp đơn giản.

Nếu có thể biểu diễn bằng toán học, phải đưa ra formulation rõ ràng.

Ví dụ:

$$
f_\theta : \mathcal{X} \rightarrow \mathcal{Y}
$$

và giải thích rõ:

* $\mathcal{X}$ là gì;
* $\mathcal{Y}$ là gì;
* $\theta$ đại diện cho điều gì.

### 1.3. Hạn chế của các phương pháp trước

Không chỉ liệt kê các phương pháp trước đó.

Phải giải thích:

> Phương pháp cũ làm được gì và **chưa làm được gì**?

Có thể trình bày theo dạng:

| Phương pháp | Ưu điểm | Hạn chế |
| ----------- | ------- | ------- |
| Method A    | ...     | ...     |
| Method B    | ...     | ...     |
| Method C    | ...     | ...     |

### 1.4. Khoảng trống nghiên cứu

Phải chỉ ra chính xác:

> **Research Gap là gì?**

Không được viết chung chung như:

> "Các phương pháp hiện tại vẫn còn nhiều hạn chế."

Phải chỉ ra hạn chế cụ thể và mối liên hệ với bài toán.

### 1.5. Mục tiêu nghiên cứu

Nêu rõ bài báo muốn đạt được điều gì.

### 1.6. Câu hỏi nghiên cứu

Chuyển mục tiêu thành các câu hỏi có thể kiểm chứng.

Ví dụ:

* Phương pháp đề xuất có cải thiện hiệu quả không?
* Thành phần nào đóng góp nhiều nhất?
* Phương pháp có tổng quát tốt hơn không?

### 1.7. Đóng góp chính

Liệt kê các contribution của paper.

Mỗi contribution phải được giải thích ngắn gọn, không chỉ sao chép abstract.

---

# Chương 2 — Cơ sở lý thuyết và tổng quan

## Mục tiêu

Trả lời:

> **Chúng ta đã biết gì trước khi nghiên cứu này được thực hiện?**

Chương này phải sắp xếp tri thức nền theo logic dẫn đến phương pháp của bài báo.

## Nội dung

### 2.1. Kiến thức nền

Chỉ đưa vào những lý thuyết cần thiết để hiểu bài báo.

Ví dụ:

* Linear Algebra;
* Probability;
* Optimization;
* CNN;
* RNN;
* Transformer;
* Attention;
* Diffusion;
* Monte Carlo;
* Graph Neural Network;

tùy lĩnh vực.

Không trình bày toàn bộ lý thuyết nếu không liên quan trực tiếp.

### 2.2. Các phương pháp liên quan

Sắp xếp các nghiên cứu trước theo nhóm ý tưởng thay vì liệt kê theo thứ tự xuất hiện trong paper.

Ví dụ:

```text
Previous Methods
├── CNN-based approaches
├── Attention-based approaches
├── Transformer-based approaches
└── Hybrid approaches
```

### 2.3. So sánh các phương pháp trước

Làm rõ:

* nguyên lý;
* ưu điểm;
* nhược điểm;
* vấn đề còn tồn tại.

### 2.4. Khoảng trống tri thức

Kết nối Chương 1 với Chương 2:

```text
Existing Knowledge
        ↓
Known Limitations
        ↓
Research Gap
        ↓
New Hypothesis / Proposed Idea
```

### 2.5. Giả thuyết hoặc ý tưởng nghiên cứu

Nếu bài báo có hypothesis, trình bày trực tiếp.

Nếu không có hypothesis rõ ràng, phải mô tả **research intuition** của tác giả nhưng không được tự gán cho tác giả một giả thuyết không tồn tại.

---

# Chương 3 — Phương pháp nghiên cứu

## Mục tiêu

Trả lời:

> **Tác giả tìm câu trả lời bằng cách nào?**

Đây là chương kỹ thuật quan trọng nhất.

Phải trình bày nghiên cứu như một pipeline hoàn chỉnh:

```text
Data
  ↓
Preprocessing
  ↓
Input Representation
  ↓
Model / Algorithm
  ↓
Optimization / Training
  ↓
Evaluation
```

## 3.1. Dữ liệu

Mô tả:

* dataset;
* nguồn dữ liệu;
* số lượng mẫu;
* feature;
* label;
* cách chia dữ liệu;
* preprocessing;
* augmentation nếu có.

Nếu paper sử dụng nhiều dataset, trình bày riêng từng dataset.

## 3.2. Problem Formulation

Định nghĩa bài toán bằng toán học khi cần.

Ví dụ:

$$
\hat{y} = f_\theta(x)
$$

hoặc bài toán tối ưu:

$$
\theta^* = \arg\min_\theta \mathcal{L}(\theta)
$$

Phải giải thích **ý nghĩa của công thức**, không chỉ đưa công thức.

## 3.3. Kiến trúc / mô hình đề xuất

Đây là phần phải được phân tích sâu nhất.

Phải trình bày:

1. Input.
2. Các module.
3. Luồng dữ liệu.
4. Các phép biến đổi.
5. Output.
6. Loss.
7. Optimization.

Nếu mô hình gồm nhiều module:

```text
Input
  ↓
Module A
  ↓
Module B
  ↓
Module C
  ↓
Prediction
```

Mỗi module phải giải thích:

* chức năng;
* input/output;
* lý do tồn tại;
* công thức nếu có;
* khác biệt so với phương pháp trước.

## 3.4. Công thức toán học

Mỗi công thức quan trọng phải được giải thích.

Ví dụ:

$$
\mathbf{h}_t = f(\mathbf{x}_t, \mathbf{h}_{t-1}; \theta)
$$

Phải giải thích:

* $\mathbf{x}_t$: input tại bước $t$;
* $\mathbf{h}_{t-1}$: trạng thái trước đó;
* $\mathbf{h}_t$: trạng thái hiện tại;
* $\theta$: tham số học được;
* $f$: phép biến đổi của mô hình.

Không đưa công thức vào mà không giải thích.

## 3.5. Training / Optimization

Nếu paper có training, trình bày:

* objective;
* loss function;
* optimizer;
* learning rate;
* batch size;
* number of epochs;
* scheduler;
* regularization;
* initialization;
* các chi tiết quan trọng khác.

Ví dụ:

$$
\mathcal{L}(\theta)
=
\frac{1}{N}
\sum_{i=1}^{N}
\ell(f_\theta(x_i),y_i)
$$

## 3.6. Evaluation

Trình bày:

* metric;
* baseline;
* experimental setup;
* protocol;
* ablation;
* comparison.

Phải giải thích **metric đo cái gì và tại sao được sử dụng**.

---

# Chương 4 — Kết quả và thảo luận

## Mục tiêu

Trả lời:

> **Tác giả thực sự tìm thấy điều gì và kết quả đó có ý nghĩa gì?**

Không chỉ sao chép bảng kết quả.

## 4.1. Kết quả chính

Trình bày các kết quả quan trọng nhất.

Ví dụ:

| Method          | Metric |
| --------------- | -----: |
| Baseline        |    ... |
| Previous SOTA   |    ... |
| Proposed Method |    ... |

Phải xác định:

* phương pháp nào tốt nhất;
* cải thiện bao nhiêu;
* cải thiện trên tiêu chí nào.

## 4.2. Phân tích kết quả

Không dừng ở:

> Proposed method đạt kết quả tốt hơn.

Phải trả lời:

> **Tại sao nó tốt hơn?**

Nếu bài báo có giải thích, phải trình bày theo bằng chứng của tác giả.

Nếu Agent suy luận thêm, phải đánh dấu rõ đó là **phân tích diễn giải**, không phải kết luận trực tiếp của paper.

## 4.3. Ablation Study

Nếu có ablation:

* component nào được thêm/bỏ;
* metric thay đổi thế nào;
* component đó đóng góp gì.

Ví dụ:

```text
Full Model
   ↓ remove A
Model - A
   ↓ remove B
Model - A - B
```

Mục tiêu là xác định:

> Thành phần nào thực sự quan trọng?

## 4.4. So sánh với nghiên cứu trước

Phải trả lời:

* Paper có vượt baseline không?
* Có vượt SOTA không?
* Cải thiện trên metric nào?
* Cải thiện có đáng kể không?
* Có trade-off nào không?

Không được tuyên bố "SOTA" nếu bài báo hoặc bằng chứng được cung cấp không xác nhận điều đó.

## 4.5. Ý nghĩa của kết quả

Kết quả có ý nghĩa gì đối với:

* bài toán;
* lý thuyết;
* phương pháp;
* ứng dụng thực tế?

Đây là phần **Discussion**, không phải chỉ đọc số liệu.

## 4.6. Những điều kết quả chưa chứng minh

Phải tránh overclaim.

Nếu thực nghiệm chỉ chứng minh trên:

* một dataset;
* một task;
* một benchmark;
* một điều kiện;

thì không được suy rộng thành:

> "Phương pháp luôn tốt hơn."

---

# Chương 5 — Kết luận và hàm ý

## Mục tiêu

Trả lời:

> **Sau tất cả, chúng ta học được gì?**

## 5.1. Kết luận chính

Tóm tắt:

```text
Problem
  ↓
Research Gap
  ↓
Proposed Idea
  ↓
Experimental Evidence
  ↓
Main Finding
```

Không đưa thêm thông tin mới chưa xuất hiện ở các chương trước.

## 5.2. Đóng góp khoa học

Tách rõ:

* methodological contribution;
* theoretical contribution;
* empirical contribution;
* practical contribution.

Chỉ sử dụng loại đóng góp phù hợp với paper.

## 5.3. Hàm ý

Nếu phù hợp, trình bày:

* hàm ý quản trị;
* hàm ý kỹ thuật;
* hàm ý chính sách;
* hàm ý nghiên cứu.

Không ép bài báo phải có "hàm ý quản trị" nếu đó là paper thuần kỹ thuật.

## 5.4. Hạn chế

Nêu các limitation được paper đề cập.

Có thể bổ sung limitation từ phân tích của Agent nhưng phải phân biệt rõ.

## 5.5. Hướng nghiên cứu tiếp theo

Dựa trên:

* limitation;
* unresolved problems;
* future work của tác giả;
* các vấn đề logic còn bỏ ngỏ.

Không tự tạo future work không có cơ sở.

---

# 4. Quy tắc xử lý công thức toán học

Đây là yêu cầu bắt buộc.

## 4.1. Sử dụng GitHub-compatible LaTeX

Công thức phải sử dụng cú pháp Markdown/LaTeX tương thích GitHub.

### Công thức inline

Sử dụng:

```markdown
$x_t \in \mathbb{R}^d$
```

### Công thức block

Sử dụng:

```markdown
$$
\mathbf{h}_t
=
f(\mathbf{x}_t,\mathbf{h}_{t-1};\theta)
$$
```

Không sử dụng format không tương thích với GitHub.

---

## 4.2. Không xuống dòng sai trong công thức

**Tuyệt đối không tách một công thức toán học thành nhiều dòng Markdown ngoài ý muốn.**

Sai:

```markdown
$$
\mathbf{y} =
\mathbf{W}\mathbf{x}
+
\mathbf{b}
$$
```

nếu việc xuống dòng không mang ý nghĩa toán học.

Ưu tiên:

```markdown
$$
\mathbf{y} = \mathbf{W}\mathbf{x} + \mathbf{b}
$$
```

Đối với công thức dài thực sự cần nhiều dòng, sử dụng môi trường phù hợp:

```markdown
$$
\begin{aligned}
\mathbf{h}_t &= f(\mathbf{x}_t,\mathbf{h}_{t-1}), \\
\mathbf{y}_t &= g(\mathbf{h}_t).
\end{aligned}
$$
```

## 4.3. Không đặt LaTeX lỗi cú pháp

Agent phải kiểm tra:

* `$...$` có đóng đầy đủ;
* `$$...$$` có đóng đầy đủ;
* `{}` cân bằng;
* `\begin{...}` có `\end{...}`;
* subscript/superscript đúng cú pháp;
* `\mathbf`, `\mathbb`, `\mathrm`, `\frac`, `\sum`, `\prod` sử dụng đúng;
* không có ký hiệu Unicode thay thế làm mất tính nhất quán;
* không trộn Markdown và LaTeX sai cách.

## 4.4. Giữ nhất quán ký hiệu

Nếu sử dụng:

$$
\mathbf{x}_t
$$

thì không được tùy tiện đổi sang:

$$
x_t
$$

nếu cả hai cùng biểu diễn một đại lượng.

Agent phải xây dựng một **notation map** trước khi hoàn thiện báo cáo.

Ví dụ:

| Ký hiệu       | Ý nghĩa          |
| ------------- | ---------------- |
| $\mathbf{x}$  | Input vector     |
| $\mathbf{W}$  | Weight matrix    |
| $\mathbf{b}$  | Bias             |
| $\theta$      | Model parameters |
| $\mathcal{L}$ | Loss function    |

---

# 5. Quy tắc phân tích kiến trúc

Khi bài báo đề xuất một architecture, Agent phải tái cấu trúc kiến trúc theo ba tầng.

## Tầng 1 — Tổng quan

Giải thích architecture bằng ngôn ngữ đơn giản:

> Input đi vào đâu → được xử lý như thế nào → output được tạo ra ở đâu.

## Tầng 2 — Thành phần

Phân rã:

```text
Model
├── Encoder
├── Feature Transformation
├── Attention
├── Decoder
└── Prediction Head
```

Chỉ sử dụng những module thực sự tồn tại.

## Tầng 3 — Toán học

Sau khi người đọc hiểu architecture, mới trình bày công thức.

Ví dụ:

$$
\mathbf{z} = f_{\theta}(\mathbf{x})
$$

sau đó giải thích từng thành phần.

**Không bắt đầu bằng công thức phức tạp khi chưa giải thích trực giác của mô hình.**

---

# 6. Quy tắc phân tích thuật toán

Khi paper đề xuất algorithm, trình bày theo thứ tự:

1. Input.
2. Initialization.
3. Main procedure.
4. Update rule.
5. Stopping condition.
6. Output.
7. Complexity nếu paper có đề cập hoặc complexity là yếu tố quan trọng.

Có thể sử dụng pseudocode:

```text
Algorithm
Input: X
Initialize θ
Repeat:
    Compute prediction
    Compute loss
    Update θ
Until convergence
Return θ
```

Sau pseudocode phải giải thích ý nghĩa của từng bước.

---

# 7. Quy tắc phân tích thực nghiệm

Agent phải phân biệt rõ:

### Experimental Setup

> Tác giả đã thử nghiệm như thế nào?

### Results

> Tác giả thu được gì?

### Discussion

> Kết quả đó có ý nghĩa gì?

Không gộp ba nội dung này thành một đoạn duy nhất.

---

# 8. Quy tắc đối chiếu với paper gốc

Trước khi hoàn thiện báo cáo, Agent phải thực hiện kiểm tra nội bộ:

## Content Verification

* [ ] Đúng research problem.
* [ ] Đúng research gap.
* [ ] Đúng objective.
* [ ] Đúng contribution.
* [ ] Đúng architecture.
* [ ] Đúng algorithm.
* [ ] Đúng mathematical formulation.
* [ ] Đúng dataset.
* [ ] Đúng experimental setup.
* [ ] Đúng metric.
* [ ] Đúng kết quả.
* [ ] Đúng limitation.
* [ ] Không thêm claim không có bằng chứng.

---

# 9. Quy tắc tránh hallucination

Agent **không được tự tạo**:

* số liệu;
* dataset;
* baseline;
* citation;
* equation;
* architecture component;
* experimental result;
* claim "SOTA";
* limitation;
* future work.

Nếu thông tin không có trong paper hoặc không thể xác minh:

> **Không đủ thông tin để kết luận.**

Nếu cần diễn giải, phải phân biệt:

> **Theo tác giả:** ...

và:

> **Diễn giải:** ...

---

# 10. Quy tắc citation và nguồn

Khi phân tích paper:

* Ưu tiên paper gốc.
* Nếu paper được cung cấp dưới dạng PDF, sử dụng nội dung PDF làm nguồn chính.
* Nếu cần kiến thức nền, có thể sử dụng các nguồn học thuật uy tín.
* Không sử dụng blog hoặc nguồn không đáng tin cậy để xác nhận claim khoa học quan trọng nếu có nguồn gốc học thuật tốt hơn.
* Không biến báo cáo thành danh sách citation.

Citation phải phục vụ việc xác minh thông tin, không phải trang trí.

---

# 11. Quy tắc về mức độ chi tiết

Báo cáo phải:

* **đủ sâu để hiểu paper;**
* **đủ ngắn để không lan man;**
* tập trung vào ý tưởng và đóng góp;
* ưu tiên các thành phần có ảnh hưởng trực tiếp đến kết luận.

Không cần giải thích lại toàn bộ kiến thức phổ thông nếu không phục vụ việc hiểu paper.

Ngược lại, nếu một khái niệm là nền tảng để hiểu architecture hoặc equation, phải giải thích đủ sâu.

---

# 12. Quy trình Agent phải thực hiện

Agent nên thực hiện theo pipeline:

```text
Step 1
Đọc toàn bộ paper
        ↓
Step 2
Xác định Problem
        ↓
Step 3
Xác định Research Gap
        ↓
Step 4
Xác định Research Question / Objective
        ↓
Step 5
Xác định Contribution
        ↓
Step 6
Xây dựng Knowledge Map
        ↓
Step 7
Phân tích Proposed Method
        ↓
Step 8
Phân tích Mathematical Formulation
        ↓
Step 9
Phân tích Experimental Setup
        ↓
Step 10
Phân tích Results
        ↓
Step 11
Phân tích Discussion
        ↓
Step 12
Phân tích Limitation / Future Work
        ↓
Step 13
Tái cấu trúc thành 5 chương
        ↓
Step 14
Kiểm tra toán học và ký hiệu
        ↓
Step 15
Kiểm tra factual consistency
        ↓
Step 16
Xuất báo cáo cuối
```

---

# 13. Checklist kiểm tra LaTeX trước khi xuất bản

Agent phải kiểm tra lần cuối:

### Delimiter

* [ ] Mọi `$` inline đều được đóng.
* [ ] Mọi `$$` block đều được đóng.
* [ ] Không có `$` thừa.
* [ ] Không có `$$` lồng nhau.

### Syntax

* [ ] `{}` cân bằng.
* [ ] `\left` / `\right` cân bằng nếu sử dụng.
* [ ] `\begin` / `\end` cân bằng.
* [ ] `\frac{}{}` đầy đủ.
* [ ] Subscript `_` đúng.
* [ ] Superscript `^` đúng.

### Formatting

* [ ] Công thức quan trọng dùng `$$...$$`.
* [ ] Ký hiệu inline dùng `$...$`.
* [ ] Không để công thức toán bị Markdown tách dòng ngoài ý muốn.
* [ ] Không đặt dấu câu sai vị trí gây khó đọc.
* [ ] Không sử dụng Unicode thay thế tùy tiện cho ký hiệu toán học.

---

# 14. Checklist kiểm tra ký hiệu

Trước khi xuất báo cáo:

* [ ] Mỗi biến có ý nghĩa rõ ràng.
* [ ] Một ký hiệu chỉ biểu diễn một khái niệm.
* [ ] Không đổi notation giữa các chương.
* [ ] Vector, matrix, scalar được phân biệt nhất quán.
* [ ] Index được sử dụng nhất quán.
* [ ] Các tham số model được định nghĩa.
* [ ] Loss function được định nghĩa.
* [ ] Các tập dữ liệu được ký hiệu nhất quán.

---

# 15. Checklist kiểm tra logic khoa học

Agent phải tự hỏi:

### Chương 1

> Tôi có thể trả lời rõ "paper giải quyết vấn đề gì?" không?

### Chương 2

> Tôi có thể giải thích "trước paper này chúng ta đã biết gì?" không?

### Chương 3

> Tôi có thể mô tả chính xác "tác giả đã làm gì để giải quyết vấn đề?" không?

### Chương 4

> Tôi có thể trả lời "kết quả chứng minh điều gì?" không?

### Chương 5

> Tôi có thể trả lời "sau nghiên cứu này chúng ta học được gì?" không?

Nếu bất kỳ câu hỏi nào chưa trả lời được, báo cáo chưa hoàn thiện.

---

# 16. Cấu trúc đầu ra chuẩn

Báo cáo cuối cùng phải ưu tiên cấu trúc:

```markdown
# Tên bài báo

## Tóm tắt

### Vấn đề
### Ý tưởng chính
### Phương pháp
### Kết quả
### Đóng góp

# Chương 1. Giới thiệu và vấn đề nghiên cứu

## 1.1. Bối cảnh
## 1.2. Vấn đề nghiên cứu
## 1.3. Hạn chế của phương pháp trước
## 1.4. Khoảng trống nghiên cứu
## 1.5. Mục tiêu nghiên cứu
## 1.6. Câu hỏi nghiên cứu
## 1.7. Đóng góp

# Chương 2. Cơ sở lý thuyết và tổng quan

## 2.1. Kiến thức nền
## 2.2. Các phương pháp liên quan
## 2.3. So sánh các phương pháp
## 2.4. Khoảng trống tri thức
## 2.5. Ý tưởng / giả thuyết nghiên cứu

# Chương 3. Phương pháp nghiên cứu

## 3.1. Dữ liệu
## 3.2. Problem Formulation
## 3.3. Tổng quan phương pháp
## 3.4. Kiến trúc đề xuất
## 3.5. Mathematical Formulation
## 3.6. Training / Optimization
## 3.7. Experimental Setup
## 3.8. Evaluation Metrics

# Chương 4. Kết quả và thảo luận

## 4.1. Kết quả chính
## 4.2. Phân tích kết quả
## 4.3. Ablation Study
## 4.4. So sánh với phương pháp trước
## 4.5. Ý nghĩa của kết quả
## 4.6. Những điều chưa được chứng minh

# Chương 5. Kết luận và hàm ý

## 5.1. Kết luận
## 5.2. Đóng góp khoa học
## 5.3. Hàm ý
## 5.4. Hạn chế
## 5.5. Hướng nghiên cứu tiếp theo

# Tài liệu tham khảo
```

Các mục không tồn tại trong paper phải được **bỏ qua hoặc ghi rõ "không được đề cập"**, không được tự tạo nội dung.

---

# 17. Tiêu chuẩn cuối cùng

Một báo cáo chỉ được xem là hoàn thành khi thỏa mãn đồng thời 5 tiêu chuẩn:

$$
\boxed{
\text{Scientific Accuracy}
+
\text{Logical Structure}
+
\text{Technical Depth}
+
\text{Mathematical Consistency}
+
\text{Clear Explanation}
}
$$

Trong đó:

* **Scientific Accuracy:** đúng với paper.
* **Logical Structure:** vấn đề → gap → phương pháp → kết quả → kết luận.
* **Technical Depth:** đủ sâu để hiểu architecture/algorithm.
* **Mathematical Consistency:** công thức và notation chính xác, nhất quán.
* **Clear Explanation:** học thuật nhưng vẫn dẫn dắt người đọc.

## Nguyên tắc tối thượng

> **Không viết để "tóm tắt paper". Hãy viết để người đọc có thể hiểu paper đang giải quyết vấn đề gì, tại sao phương pháp được đề xuất, nó hoạt động như thế nào, bằng chứng thực nghiệm nói lên điều gì, và nghiên cứu này đóng góp gì cho tri thức hiện tại.**

Trước khi trả lời cuối cùng, Agent phải thực hiện **hai vòng kiểm tra**:

```text
Paper → Content Verification
                 ↓
        Mathematical Verification
                 ↓
          Final Report
```

Nếu phát hiện mâu thuẫn giữa các phần của báo cáo, phải sửa trước khi xuất bản. Không đưa bản nháp có lỗi notation, lỗi công thức hoặc claim chưa được kiểm chứng vào kết quả cuối cùng.
