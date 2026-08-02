# Feature Selection

## Learning Objectives

- Triển khai các phương pháp Filter (Variance Threshold, Mutual Information, Chi-Squared) và các phương pháp Wrapper (Recursive Feature Elimination - RFE, Forward Selection) from scratch.

- Giải thích vì sao Mutual Information có thể phát hiện mối quan hệ phi tuyến giữa đặc trưng và biến mục tiêu mà Correlation không thể phát hiện.

- So sánh L1 Regularization (Embedded Feature Selection) với Recursive Feature Elimination (RFE) (Wrapper Feature Selection), đồng thời đánh giá sự đánh đổi về chi phí tính toán giữa hai phương pháp.

- Xây dựng pipeline lựa chọn đặc trưng (Feature Selection Pipeline) bằng cách kết hợp nhiều phương pháp và chứng minh khả năng cải thiện khả năng tổng quát hóa (Generalization) trên tập dữ liệu kiểm thử (held-out data).

## The Problem

Bạn có 500 đặc trưng (features). Mô hình huấn luyện chậm, liên tục __overfitting__, và không ai có thể giải thích được mô hình đã học những gì. Bạn tiếp tục thêm nhiều đặc trưng với hy vọng cải thiện hiệu suất. Kết quả lại càng tệ hơn.

Đây chính là __lời nguyền của tính chiều cao (Curse of Dimensionality)__. Khi số lượng đặc trưng tăng lên, __thể tích của không gian đặc trưng (feature space)__ tăng theo cấp số nhân. Các điểm dữ liệu trở nên thưa thớt hơn. Khoảng cách giữa các điểm dần hội tụ và mất đi khả năng phân biệt. Mô hình cần lượng dữ liệu lớn hơn theo cấp số nhân để tìm ra các mẫu thực sự. Những đặc trưng chứa nhiễu lấn át các đặc trưng mang tín hiệu. Overfitting trở thành trạng thái mặc định.

Feature Selection là giải pháp cho vấn đề này. Loại bỏ nhiễu. Loại bỏ sự dư thừa. Chỉ giữ lại những đặc trưng thực sự mang thông tin về biến mục tiêu. Kết quả là:

- Thời gian huấn luyện nhanh hơn.
- Khả năng tổng quát hóa tốt hơn.
- Mô hình dễ giải thích hơn.

Mục tiêu không phải là sử dụng toàn bộ thông tin hiện có, mà là sử dụng đúng thông tin cần thiết.

## Phân loại các phương pháp lựa chọn đặc trưng

> Giới thiệu các phương pháp phổ biến dựa trên quan hệ giữa quá trình lựa chọn đặc trưng và quá trình huấn luyện mô hình.

### Phương pháp filter

> Filter Methods là nhóm phương pháp lựa chọn đặc trưng (Feature Selection) bằng cách đánh giá từng feature độc lập thông qua một thước đo thống kê (statistical measure). Không sử dụng mô hình Machine Learning, mỗi feature dược chấm điểm riêng biệt.

Các phương pháp Filter phổ biến gồm:

| Phương pháp        | Ý tưởng                                    | Dữ liệu phù hợp             |
| ------------------ | ------------------------------------------ | --------------------------- |
| Variance Threshold | Loại feature có phương sai rất nhỏ         | Mọi bài toán                |
| Pearson Correlation        | Chọn feature có tương quan mạnh với target | Regression                  |
| Mutual Information | Đo lượng thông tin giữa feature và target  | Regression & Classification |
| Chi-Squared (χ²)   | Đo mức phụ thuộc giữa feature và target    | Classification              |

> Filter Methods sử dụng các thước đo thống kê để đánh giá và xếp hạng từng đặc trưng một cách độc lập, sau đó giữ lại các đặc trưng mang nhiều thông tin nhất trước khi đưa dữ liệu vào mô hình học máy. ưu điểm của phương pháp này là nhanh và chi phí thấp, nhưng nhược điểm là không phát hiện được sự tương tác giữa các đặc trưng và không loại bỏ hoàn toàn thông tin dư thừa.

### Phương pháp wrapper

> Wrapper Methods là nhóm phương pháp Feature Selection sử dụng một mô hình Machine Learning để đánh giá chất lượng của tập hợp các đặc trưng (feature subset).

Đối với mỗi tập đặc trưng ứng viên $S$, mô hình học máy $M$ sẽ được huấn luyện trên tập dữ liệu chỉ chứa các đặc trưng trong $S$, sau đó được đánh giá bằng một tiêu chí như __Accuracy__, __F1-score__, __Precision__, __Recall__, __RMSE__ hoặc __Cross Validation Score__. Mục tiêu của bài toán là tìm tập đặc trưng giúp mô hình đạt hiệu năng dự đoán cao nhất.

Bài toán lựa chọn đặc trưng có thể được biểu diễn tổng quát như sau:

$$S^{*}=\arg\max_{S\subseteq{1,\ldots,p}} J(S;M)$$

Trong đó:
- $S$ là tập đặc trưng được lựa chọn.
- $p$ là tổng số đặc trưng ban đầu.
- $M$ là số mô hình học máy được sử dụng để đánh giá
- $J(S; M)$ là hàm đánh giá hiệu năng của mô hình trên tập đặc trưng S

Do số lượng đặc trưng có thể lên đến $2^p$, , việc đánh giá toàn bộ không gian tìm kiếm là không khả thi khi số lượng đặc trưng lớn. Vì vậy, __Wrapper Methods__ thường kết hợp mô hình học máy với các chiến lược tìm kiếm heuristic nhằm giảm số lần đánh giá.

Các phương pháp phổ biến gồm:
- __Forward Selection__: bắt đầu từ tập đặc trưng rỗng, sau đó lần lượt thêm đặc trưng mang lại mức cải thiện hiệu năng lớn nhất.
- __Backward Elimination__: bắt đầu với toàn bộ đặc trưng, sau đó loại bỏ dần đặc trưng ít quan trọng nhất.
- __Recursive Feature Elimination (RFE)__: lặp lại quá trình huấn luyện và loại bỏ các đặc trưng có mức độ quan trọng thấp cho đến khi còn số lượng đặc trưng mong muốn.
- __Sequential Backward Selection (SBS)__: loại bỏ từng đặc trưng theo từng bước dựa trên sự thay đổi hiệu năng của mô hình.

Ưu điểm của Wrapper Methods là mỗi tập đặc trưng được đánh giá trực tiếp thông qua hiệu năng thực tế của mô hình. Nhờ đó, phương pháp có thể xem xét sự tương tác giữa nhiều đặc trưng, lựa chọn được tập đặc trưng tối ưu hơn so với các phương pháp Filter trong nhiều bài toán.

Hạn chế chính của phương pháp là chi phí tính toán cao, do mô hình phải được huấn luyện và đánh giá nhiều lần trên các tập đặc trưng khác nhau. Ngoài ra, kết quả lựa chọn phụ thuộc vào loại mô hình, siêu tham số (hyperparameters) và tiêu chí đánh giá được sử dụng. Nếu không áp dụng quy trình đánh giá phù hợp (ví dụ Cross Validation), Wrapper Methods có thể dẫn đến overfitting ngay trong quá trình lựa chọn đặc trưng.

> Wrapper Methods sử dụng hiệu năng của mô hình để lựa chọn tập đặc trưng tối ưu. Phương pháp này thường đạt hiệu quả cao nhưng phải đánh đổi bằng thời gian huấn luyện và chi phí tính toán lớn.

### Phương pháp Embedded

> Embedded Methods là phương pháp lựa chọn đặc trưng ngay trong quá trình huấn luyện mô hình. Thay vì đánh giá đặc trưng trước (Filter) hoặc huấn luyện nhiều mô hình để tìm tập đặc trưng tốt nhất (Wrapper), Embedded Methods tích hợp việc lựa chọn đặc trưng vào quá trình tối ưu mô hình.

Một mô hình Embedded có thể được biểu diễn tổng quát như sau:

$$\hat{\theta}= \arg \min_\theta \{\mathcal L (\theta) + \lambda \Omega (\theta) \}$$

Trong đó:
- $\mathcal L (\theta)$ là hàm mất mát (Loss Function)
- $\Omega (\theta)$ là hàm regularization.
- $\lambda$ là hệ số điều chỉnh mức độ regularization.

Đối với __L1 Regularization (Lasso)__, hàm regularization có dạng:

$$\Omega (\theta) = \sum^p_{j=1} |\theta_j|$$

L1 Regularization có xu hướng đưa nhiều hệ số về 0, do đó các đặc trưng tương ứng sẽ bị loại bỏ khỏi mô hình.

Ưu điểm của Embedded Methods là __chỉ cần huấn luyện mô hình một lần__, nên chi phí tính toán thấp hơn Wrapper Methods nhưng vẫn xem xét được mối quan hệ giữa đặc trưng và mô hình. Ngoài ra, phương pháp này thường cho kết quả lựa chọn đặc trưng ổn định và hiệu quả trên các tập dữ liệu có số chiều lớn.

Hạn chế của Embedded Methods là __phụ thuộc vào mô hình được sử dụng__. Không phải mọi thuật toán đều hỗ trợ lựa chọn đặc trưng theo cách này, và tập đặc trưng được chọn có thể thay đổi khi thay đổi mô hình hoặc tham số regularization.

> Embedded Methods thực hiện lựa chọn đặc trưng trong quá trình huấn luyện mô hình, giúp cân bằng giữa tốc độ của Filter Methods và độ chính xác của Wrapper Methods. Phương pháp tiêu biểu là L1 Regularization (Lasso) và các mô hình Decision Tree hoặc Random Forest dựa trên độ quan trọng của đặc trưng (Feature Importance).


| Tiêu chí                             | **Filter Methods**                                   | **Wrapper Methods**                                              | **Embedded Methods**                                       |
| ------------------------------------ | ---------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------- |
| **Nguyên lý**                        | Đánh giá từng đặc trưng bằng thước đo thống kê       | Đánh giá các tập đặc trưng bằng hiệu năng của mô hình            | Lựa chọn đặc trưng ngay trong quá trình huấn luyện mô hình |
| **Có sử dụng mô hình?**              | ❌ Không                                              | ✅ Có                                                             | ✅ Có                                                       |
| **Tiêu chí đánh giá**                | Statistical Measure (Variance, MI, χ²,...)           | Accuracy, F1, RMSE, Cross Validation,...                         | Trọng số hoặc Feature Importance của mô hình               |
| **Xét tương tác giữa các đặc trưng** | ❌ Không                                              | ✅ Có                                                             | ✅ Có (phụ thuộc mô hình)                                   |
| **Số lần huấn luyện mô hình**        | Không cần huấn luyện                                 | Huấn luyện nhiều lần                                             | Huấn luyện một lần                                         |
| **Chi phí tính toán**                | Thấp                                                 | Cao                                                              | Trung bình                                                 |
| **Tốc độ**                           | Nhanh                                                | Chậm                                                             | Nhanh hơn Wrapper                                          |
| **Nguy cơ Overfitting**              | Thấp                                                 | Cao nếu đánh giá không đúng                                      | Thấp hơn Wrapper                                           |
| **Ưu điểm**                          | Đơn giản, nhanh, phù hợp dữ liệu nhiều đặc trưng     | Độ chính xác lựa chọn cao, tìm được tương tác giữa các đặc trưng | Cân bằng giữa tốc độ và hiệu quả lựa chọn                  |
| **Hạn chế**                          | Không phát hiện được sự tương tác giữa các đặc trưng | Tốn thời gian và tài nguyên tính toán                            | Phụ thuộc vào mô hình và phương pháp regularization        |
| **Phương pháp tiêu biểu**            | Variance Threshold, Mutual Information, Chi-Squared  | Forward Selection, Backward Elimination, RFE                     | Lasso (L1), Decision Tree, Random Forest                   |
| **Đầu ra phổ biến**            | Điểm hoặc bảng xếp hạng đặc trưng  | Tập con hoặc bảng xếp hạng đặc trưng                     | Hệ số hoặc độ quan trọng đặc trưng                   |

## Các cách phân loại Feature Selection khác

> Ba nhóm Filter, Wrapper và Embedded là cách phân loại phổ biến nhất dựa trên cơ chế lựa chọn đặc trưng. Tuy nhiên, trong thực tế, các phương pháp Feature Selection còn có thể được phân loại theo thông tin sử dụng, cách đánh giá đặc trưng và chiến lược tìm kiếm. Những cách phân loại này giúp hiểu rõ hơn bản chất của từng thuật toán và lựa chọn phương pháp phù hợp với từng bài toán.

### Phân loại theo thông tin sử dụng

Dựa trên việc sử dụng biến mục tiêu (Target), Feature Selection được chia thành ba nhóm:

| Nhóm                                  | Đặc điểm                                                                                                                   |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **Supervised Feature Selection**      | Sử dụng dữ liệu có nhãn để đánh giá mức độ liên quan giữa đặc trưng và biến mục tiêu.                                      |
| **Unsupervised Feature Selection**    | Không sử dụng nhãn, lựa chọn đặc trưng dựa trên cấu trúc nội tại của dữ liệu như phương sai, phân cụm hoặc mức độ dư thừa. |
| **Semi-supervised Feature Selection** | Kết hợp dữ liệu có nhãn và không có nhãn, phù hợp khi số lượng mẫu được gán nhãn hạn chế.                                  |

### Phân loại theo cách đánh giá đặc trưng

Dựa trên cách đánh giá đặc trưng, Feature Selection gồm hai nhóm:

| Nhóm                     | Đặc điểm                                                                                                                           |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Univariate Methods**   | Đánh giá từng đặc trưng độc lập với các đặc trưng khác. Ví dụ: Pearson Correlation, Chi-Squared, ANOVA F-test, Mutual Information. |
| **Multivariate Methods** | Đánh giá đồng thời nhiều đặc trưng, xem xét sự tương tác và mức độ bổ sung thông tin giữa các đặc trưng.                           |

### Phân loại theo chiến lược tìm kiếm

Dựa trên cách khám phá không gian tập đặc trưng, Feature Selection có thể được chia thành:

| Chiến lược            | Đặc điểm                                                                                                                                        |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Exhaustive Search** | Đánh giá toàn bộ các tập con đặc trưng để tìm nghiệm tối ưu, nhưng chi phí tính toán rất lớn.                                                   |
| **Heuristic Search**  | Chỉ khám phá một phần không gian tìm kiếm bằng các chiến lược như Forward Selection, Backward Elimination hoặc RFE nhằm giảm chi phí tính toán. |

Các cách phân loại trên không thay thế ba nhóm Filter, Wrapper và Embedded, mà chỉ mô tả Feature Selection dưới những góc nhìn khác nhau:

- __Filter – Wrapper – Embedded__: phân loại theo cơ chế lựa chọn đặc trưng.
- __Supervised – Unsupervised – Semi-supervised__: phân loại theo thông tin sử dụng.
- __Univariate – Multivariate__: phân loại theo cách đánh giá đặc trưng.
- __Exhaustive – Heuristic__: phân loại theo chiến lược tìm kiếm.

## Variance Threshold

Variance Threshold là phương pháp Filter Feature Selection loại bỏ các đặc trưng có phương sai thấp, vì chúng gần như không thay đổi giữa các mẫu dữ liệu và chứa rất ít thông tin.

Phương sai của một đặc trưng được tính theo:

$$Var(x) = \frac {1} {n} \sum^n_{i=1} (x_i - \bar{x})^2$$

Nếu: $Var(x) \lt τ$ thì đặc trưng sẽ bị loại bỏ, trong đó $τ$ là ngưỡng phương sai được xác định trước.

Ưu điểm: đơn giản, chi phí tính toán thấp và thường được sử dụng như bước tiền xử lý để loại bỏ các đặc trưng hằng hoặc gần hằng.

Hạn chế: phương pháp không sử dụng biến mục tiêu, vì vậy một đặc trưng có phương sai cao vẫn có thể chỉ là nhiễu và không hữu ích cho mô hình.

> Variance Threshold chỉ đánh giá mức độ biến thiên của đặc trưng, không đánh giá mối liên hệ với biến mục tiêu, nên thường được kết hợp với các phương pháp Feature Selection khác.

## Mutual Information

__Mutual Information (MI)__ là phương pháp __Filter Feature Selection đo lượng thông tin mà một đặc trưng X cung cấp về biến mục tiêu Y__. Giá trị MI càng lớn, đặc trưng càng hữu ích cho việc dự đoán.

Công thức: 

$$I(X; Y) = \sum_x \sum_y p(x, y) log(\frac {p(x, y)} {p(x) p(y)})$$

Nếu $X$ và $Y$ độc lập thì: $I(X; Y) = 0$

__Ưu điểm:__ Mutual Information có thể phát hiện __mối quan hệ phi tuyến (nonlinear)__ giữa đặc trưng và biến mục tiêu, trong khi Correlation chỉ phản ánh mối quan hệ tuyến tính.

Đối với dữ liệu liên tục, các giá trị thường được __chia thành các khoảng (bins)__ trước khi tính MI. Số lượng bins ảnh hưởng trực tiếp đến độ chính xác của phép ước lượng.

> Mutual Information đánh giá mức độ phụ thuộc giữa đặc trưng và biến mục tiêu, có khả năng phát hiện cả quan hệ tuyến tính và phi tuyến, nên thường hiệu quả hơn Correlation trong nhiều bài toán lựa chọn đặc trưng.

## Recursive Feature Elimination (RFE)

__Recursive Feature Elimination (RFE)__ là phương pháp __Wrapper Feature Selection__ thực hiện lựa chọn đặc trưng bằng cách lặp lại quá trình huấn luyện mô hình và loại bỏ dần các đặc trưng ít quan trọng nhất.

Quy trình thực hiện:

1. Huấn luyện mô hình với toàn bộ đặc trưng.
2. Xếp hạng mức độ quan trọng của các đặc trưng.
3. Loại bỏ đặc trưng có độ quan trọng thấp nhất.
4. Lặp lại cho đến khi còn số lượng đặc trưng mong muốn.

__Ưu điểm:__ RFE đánh giá đặc trưng dựa trên hiệu năng của mô hình và có thể xem xét sự tương tác giữa các đặc trưng, do đó thường cho kết quả tốt hơn các phương pháp Filter.

__Hạn chế:__ RFE phải huấn luyện mô hình nhiều lần nên có chi phí tính toán cao, đặc biệt khi số lượng đặc trưng lớn. Có thể giảm thời gian bằng cách loại bỏ nhiều đặc trưng sau mỗi vòng lặp.

> RFE là phương pháp Wrapper lựa chọn đặc trưng bằng cách huấn luyện mô hình nhiều lần và loại bỏ dần các đặc trưng ít quan trọng, giúp cải thiện chất lượng lựa chọn nhưng đánh đổi bằng chi phí tính toán lớn.

## L1 (Lasso) Regularization

__L1 (Lasso) Regularization__ là phương pháp __Embedded Feature Selection__ thực hiện lựa chọn đặc trưng ngay trong quá trình huấn luyện bằng cách thêm chuẩn L1 vào hàm mất mát:

$$\text{Loss} = \text{Prediction Error} + \alpha \sum^p_{i=1} |w_i|$$

trong đó $\alpha$ điều khiển mức độ regularization. Giá trị $\alpha$ càng lớn thì càng nhiều trọng số $w_i$ bị đưa về 0, đồng nghĩa với việc các đặc trưng tương ứng bị loại bỏ.

__Ưu điểm:__ chỉ cần huấn luyện mô hình một lần, tự động loại bỏ các đặc trưng không quan trọng và giảm ảnh hưởng của các đặc trưng tương quan cao.

__Hạn chế:__ chỉ phù hợp với mô hình tuyến tính và không phản ánh được mức độ quan trọng của các đặc trưng trong các mối quan hệ phi tuyến.

> L1 (Lasso) là phương pháp __Embedded__ lựa chọn đặc trưng bằng cách đưa __trọng số của các đặc trưng không quan trọng về 0__ ngay trong quá trình tối ưu mô hình, giúp giảm số lượng đặc trưng với chi phí tính toán thấp.

## Tree-Based Feature Importance

__Tree-Based Feature Importance__ là phương pháp __Embedded Feature Selection__ sử dụng các mô hình cây quyết định (Decision Tree, Random Forest, Gradient Boosting) để đánh giá mức độ quan trọng của từng đặc trưng. Đặc trưng nào giúp __giảm impurity__ (Gini, Entropy hoặc Variance) nhiều hơn sẽ có độ quan trọng cao hơn.

Đối với Random Forest, độ quan trọng của một đặc trưng được tính bằng __trung bình mức giảm impurity trên tất cả các cây__:

$$Importance(feature_j) = \frac {1} {T} \sum^T_{t=1} \sum (n_{samples} \times \text{Impurity decrease})$$

__Ưu điểm:__ tự động phát hiện __mối quan hệ phi tuyến__ và __sự tương tác giữa các đặc trưng__, đồng thời không cần thực hiện Feature Selection riêng biệt.

__Hạn chế:__ phương pháp có xu hướng __ưu tiên các đặc trưng có nhiều giá trị khác nhau (high cardinality)__, vì vậy nên kết hợp với __Permutation Importance__ để kiểm tra lại kết quả.

> Tree-Based Feature Importance lựa chọn đặc trưng dựa trên mức giảm impurity trong các mô hình cây, phù hợp với dữ liệu có quan hệ phi tuyến nhưng cần lưu ý sai lệch đối với các đặc trưng có nhiều giá trị duy nhất.

## Permutation Importance

__Permutation Importance__ là phương pháp __Model-Agnostic Feature Importance__, đánh giá mức độ quan trọng của đặc trưng bằng cách __xáo trộn (shuffle)__ giá trị của từng đặc trưng trên tập validation và đo mức suy giảm hiệu năng của mô hình.

Quy trình thực hiện:

1. Huấn luyện mô hình và ghi nhận hiệu năng ban đầu.
2. Xáo trộn giá trị của từng đặc trưng.
3. Đánh giá lại mô hình và tính mức giảm hiệu năng.

Nếu việc xáo trộn một đặc trưng làm hiệu năng giảm nhiều, đặc trưng đó được xem là quan trọng. Ngược lại, nếu hiệu năng gần như không thay đổi thì đặc trưng đóng góp rất ít cho mô hình.

__Ưu điểm:__ không phụ thuộc vào loại mô hình và tránh được hiện tượng __cardinality bias__ của Tree-Based Feature Importance.

__Hạn chế:__ chi phí tính toán cao vì phải đánh giá lại mô hình cho từng đặc trưng và thường cần lặp lại nhiều lần để kết quả ổn định.

> Permutation Importance đánh giá đặc trưng thông qua __mức suy giảm hiệu năng của mô hình sau khi xáo trộn dữ liệu__, giúp phản ánh trực tiếp mức độ phụ thuộc của mô hình vào từng đặc trưng.

### Comparision table

| **Method**                              | **Type**       | **Uses Model**              | **Speed**        | **Captures Nonlinear Relationships** | **Captures Feature Interactions** |
| --------------------------------------- | -------------- | --------------------------- | ---------------- | ------------------------------------ | --------------------------------- |
| **Variance Threshold**                  | Filter         | ❌                           | ⭐⭐⭐⭐⭐ Very Fast  | ❌                                    | ❌                                 |
| **Mutual Information**                  | Filter         | ❌                           | ⭐⭐⭐⭐ Fast        | ✅                                    | ❌                                 |
| **Recursive Feature Elimination (RFE)** | Wrapper        | ✅                           | ⭐ Slow           | Phụ thuộc mô hình                    | ✅                                 |
| **L1 (Lasso) Regularization**           | Embedded       | ✅                           | ⭐⭐⭐⭐ Fast        | ❌                                    | ❌                                 |
| **Tree-Based Feature Importance**       | Embedded       | ✅                           | ⭐⭐⭐ Fast         | ✅                                    | ✅                                 |
| **Permutation Importance**              | Model-Agnostic | ✅ *(mô hình đã huấn luyện)* | ⭐⭐ Moderate–Slow | ✅                                    | ✅                                 |


## Built It

### Step 1: Tạo dữ liệu tổng hợp (Synthetic Dataset)

Đầu tiên, xây dựng một bộ dữ liệu tổng hợp để đánh giá các phương pháp **Feature Selection**. Bộ dữ liệu gồm ba nhóm đặc trưng:

- **Informative:** chứa thông tin trực tiếp để dự đoán biến mục tiêu.
- **Correlated:** tương quan với các đặc trưng quan trọng.
- **Noise:** dữ liệu nhiễu, không có giá trị dự đoán.

```python
import numpy as np

def make_feature_selection_data(n_samples=500, seed=42):
    rng = np.random.RandomState(seed)

    # Informative features
    x1 = rng.randn(n_samples)
    x2 = rng.randn(n_samples)
    x3 = rng.randn(n_samples)
    x4 = x1 + 0.1 * rng.randn(n_samples)
    x5 = x2 + 0.1 * rng.randn(n_samples)

    informative = np.column_stack([x1, x2, x3, x4, x5])

    # Correlated features
    correlated = np.column_stack([
        x1 * 0.9 + 0.1 * rng.randn(n_samples),
        x2 * 0.8 + 0.2 * rng.randn(n_samples),
        x3 * 0.7 + 0.3 * rng.randn(n_samples),
        x1 * 0.5 + x2 * 0.5 + 0.1 * rng.randn(n_samples),
        x2 * 0.6 + x3 * 0.4 + 0.1 * rng.randn(n_samples),
    ])

    # Noise features
    noise = rng.randn(n_samples, 10) * 0.5

    # Feature matrix
    X = np.hstack([informative, correlated, noise])

    # Binary target
    y = (2 * x1- 1.5 * x2 + x3 + 0.5 * rng.randn(n_samples) > 0).astype(int)

    feature_names = (
        [f"info_{i}" for i in range(5)]
        + [f"corr_{i}" for i in range(5)]
        + [f"noise_{i}" for i in range(10)]
    )

    return X, y, feature_names
```

#### Cấu trúc dữ liệu

| Nhóm đặc trưng | Chỉ số | Ý nghĩa |
|---------------|--------|----------|
| Informative | 0–4 | Đặc trưng quan trọng, chứa thông tin dự đoán |
| Correlated | 5–9 | Đặc trưng tương quan với nhóm Informative |
| Noise | 10–19 | Đặc trưng nhiễu, không mang thông tin |

#### Mục tiêu

Một phương pháp **Feature Selection** tốt cần:

- Xếp hạng **Informative Features (0–4)** cao nhất.
- Giữ lại các **Correlated Features (5–9)** nếu chúng vẫn hữu ích.
- Xếp hạng thấp hoặc loại bỏ **Noise Features (10–19)**.

### Step 2: Variance Threshold

Tiếp theo, áp dụng **Variance Threshold** để loại bỏ các đặc trưng có **phương sai thấp**. Phương pháp tính phương sai của từng đặc trưng, sau đó so sánh với một ngưỡng đã xác định trước.

```python
def variance_threshold(X, threshold=0.01):
    variances = np.var(X, axis=0)
    mask = variances > threshold
    return mask, variances
```

#### Giải thích

- `np.var(X, axis=0)`: tính phương sai của từng đặc trưng.
- `threshold`: ngưỡng phương sai tối thiểu.
- `mask`: mảng Boolean, `True` nếu đặc trưng được giữ lại và `False` nếu bị loại bỏ.
- `variances`: giá trị phương sai của tất cả các đặc trưng.

#### Kết quả

- Giữ lại các đặc trưng có:

$$\mathrm{Var}(X) > \tau$$

- Loại bỏ các đặc trưng có phương sai thấp hoặc gần như không thay đổi giữa các mẫu dữ liệu.

> **Mục tiêu:** Loại bỏ các đặc trưng hằng hoặc gần hằng trước khi áp dụng các phương pháp Feature Selection khác.

### Step 3: Mutual Information

Tiếp theo, sử dụng **Mutual Information (MI)** để đo mức độ phụ thuộc giữa từng đặc trưng và biến mục tiêu. Đối với dữ liệu liên tục, các giá trị được **rời rạc hóa (discretize)** thành nhiều khoảng trước khi tính MI.

```python
import numpy as np

def discretize(x, n_bins=10):
    min_val, max_val = x.min(), x.max()

    if max_val == min_val:
        return np.zeros_like(x, dtype=int)

    bin_edges = np.linspace(min_val, max_val, n_bins + 1)
    binned = np.digitize(x, bin_edges[1:-1])

    return binned


def mutual_information(X, y, n_bins=10):
    n_samples, n_features = X.shape
    mi_scores = np.zeros(n_features)

    y_vals, y_counts = np.unique(y, return_counts=True)
    p_y = y_counts / n_samples

    for f in range(n_features):
        x_binned = discretize(X[:, f], n_bins)

        x_vals, x_counts = np.unique(x_binned, return_counts=True)
        p_x = dict(zip(x_vals, x_counts / n_samples))

        mi = 0.0

        for xv in x_vals:
            for yi, yv in enumerate(y_vals):
                joint_mask = (x_binned == xv) & (y == yv)
                p_xy = np.sum(joint_mask) / n_samples

                if p_xy > 0:
                    mi += p_xy * np.log(
                        p_xy / (p_x[xv] * p_y[yi])
                    )

        mi_scores[f] = mi

    return mi_scores
```

### Giải thích

- `discretize()`: chia dữ liệu liên tục thành các khoảng (bins).
- `mutual_information()`: tính điểm Mutual Information cho từng đặc trưng.
- `mi_scores`: điểm MI của mỗi đặc trưng, giá trị càng lớn thì đặc trưng càng quan trọng.

### Kết quả

- **MI = 0:** đặc trưng độc lập với biến mục tiêu.
- **MI càng lớn:** đặc trưng chứa càng nhiều thông tin hữu ích để dự đoán biến mục tiêu.

> **Mục tiêu:** Xếp hạng các đặc trưng dựa trên **lượng thông tin** mà chúng cung cấp cho biến mục tiêu, đồng thời phát hiện được cả **mối quan hệ tuyến tính và phi tuyến**.

### Step 4: Recursive Feature Elimination (RFE)

Tiếp theo, áp dụng **Recursive Feature Elimination (RFE)** để lựa chọn đặc trưng. Phương pháp sử dụng mô hình **Logistic Regression** để tính độ quan trọng của các đặc trưng, sau đó loại bỏ dần đặc trưng có trọng số nhỏ nhất cho đến khi còn số lượng đặc trưng mong muốn.

```python
import numpy as np

def simple_logistic_importance(X, y, lr=0.1, epochs=100):
    n_samples, n_features = X.shape

    w = np.zeros(n_features)
    b = 0.0

    for _ in range(epochs):
        z = X @ w + b
        pred = 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))

        error = pred - y
        w -= lr * (X.T @ error) / n_samples
        b -= lr * np.mean(error)

    return w, b


def rfe(X, y, n_features_to_select=5, lr=0.1, epochs=100):
    n_total = X.shape[1]

    remaining = list(range(n_total))
    rankings = np.ones(n_total, dtype=int)
    rank = n_total

    while len(remaining) > n_features_to_select:
        X_subset = X[:, remaining]

        w, _ = simple_logistic_importance(X_subset, y, lr, epochs)

        importances = np.abs(w)

        least_idx = np.argmin(importances)
        original_idx = remaining[least_idx]

        rankings[original_idx] = rank
        rank -= 1

        remaining.pop(least_idx)

    for idx in remaining:
        rankings[idx] = 1

    selected_mask = rankings == 1
    return selected_mask, rankings
```

### Giải thích

- `simple_logistic_importance()`: huấn luyện Logistic Regression và sử dụng giá trị tuyệt đối của trọng số (`|w|`) để đánh giá độ quan trọng của từng đặc trưng.
- `rfe()`: lặp lại quá trình huấn luyện, xếp hạng và loại bỏ đặc trưng có độ quan trọng thấp nhất cho đến khi còn số lượng đặc trưng mong muốn.
- `selected_mask`: đánh dấu các đặc trưng được giữ lại.
- `rankings`: xếp hạng mức độ quan trọng của từng đặc trưng.

> **Mục tiêu:** Lựa chọn tập đặc trưng tối ưu bằng cách **loại bỏ dần các đặc trưng ít quan trọng**, đồng thời xem xét sự tương tác giữa các đặc trưng trong quá trình huấn luyện mô hình.

### Step 5: L1 Feature Selection

Tiếp theo, sử dụng **L1 Regularization (Lasso)** để lựa chọn đặc trưng. Trong quá trình huấn luyện Logistic Regression, chuẩn **L1** sẽ đưa các trọng số nhỏ về **0**, từ đó tự động loại bỏ các đặc trưng không quan trọng.

```python
def soft_threshold(w, alpha):
    return np.sign(w) * np.maximum(np.abs(w) - alpha, 0)


def l1_feature_selection(X, y, alpha=0.1, lr=0.01, epochs=500):
    n_samples, n_features = X.shape
    w = np.zeros(n_features)
    b = 0.0

    for _ in range(epochs):
        z = X @ w + b
        pred = 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))

        error = pred - y

        gradient_w = (X.T @ error) / n_samples
        gradient_b = np.mean(error)

        w -= lr * gradient_w
        w = soft_threshold(w, lr * alpha)
        b -= lr * gradient_b

    selected_mask = np.abs(w) > 1e-6

    return selected_mask, w
```

### Giải thích

- `soft_threshold()`: áp dụng **Soft Thresholding** để đưa các trọng số nhỏ về **0**.
- `l1_feature_selection()`: huấn luyện Logistic Regression với **L1 Regularization**.
- `selected_mask`: đánh dấu các đặc trưng có trọng số khác 0.
- `w`: trọng số cuối cùng của từng đặc trưng.

> **Mục tiêu:** Tự động loại bỏ các đặc trưng không quan trọng bằng cách **đưa trọng số của chúng về 0** ngay trong quá trình huấn luyện mô hình.

### Step 6: Tree-Based Feature Importance

Tiếp theo, sử dụng **Tree-Based Feature Importance** để đánh giá mức độ quan trọng của từng đặc trưng. Phương pháp xây dựng nhiều cây quyết định, tính **mức giảm Gini Impurity** tại mỗi nút phân chia và cộng dồn để xác định độ quan trọng của từng đặc trưng.

```python
def gini_impurity(y):
    if len(y) == 0:
        return 0.0

    classes, counts = np.unique(y, return_counts=True)
    probs = counts / len(y)

    return 1.0 - np.sum(probs ** 2)


def best_split(X, y, feature_idx):
    values = np.unique(X[:, feature_idx])

    if len(values) <= 1:
        return None, -1.0

    best_threshold = None
    best_gain = -1.0
    parent_gini = gini_impurity(y)
    n = len(y)

    for i in range(len(values) - 1):
        threshold = (values[i] + values[i + 1]) / 2.0

        left_mask = X[:, feature_idx] <= threshold
        right_mask = ~left_mask

        n_left = np.sum(left_mask)
        n_right = np.sum(right_mask)

        if n_left == 0 or n_right == 0:
            continue

        gain = (parent_gini - (n_left / n) * gini_impurity(y[left_mask]) - (n_right / n) * gini_impurity(y[right_mask]))

        if gain > best_gain:
            best_gain = gain
            best_threshold = threshold

    return best_threshold, best_gain


def tree_importance(X, y, n_trees=50, max_depth=5, seed=42):
    rng = np.random.RandomState(seed)

    n_samples, n_features = X.shape
    importances = np.zeros(n_features)

    for _ in range(n_trees):
        sample_idx = rng.choice(n_samples, size=n_samples, replace=True)

        feature_subset = rng.choice(n_features, size=max(1, int(np.sqrt(n_features))), replace=False)

        X_boot = X[sample_idx]
        y_boot = y[sample_idx]

        tree_imp = _build_tree_importance(X_boot, y_boot, feature_subset, max_depth)

        importances += tree_imp

    total = importances.sum()

    if total > 0:
        importances /= total

    return importances


def _build_tree_importance(X, y, feature_subset, max_depth, depth=0):
    n_features = X.shape[1]
    importances = np.zeros(n_features)

    if depth >= max_depth or len(np.unique(y)) <= 1 or len(y) < 4:
        return importances

    best_feature = None
    best_threshold = None
    best_gain = -1.0

    for f in feature_subset:
        threshold, gain = best_split(X, y, f)

        if gain > best_gain:
            best_gain = gain
            best_feature = f
            best_threshold = threshold

    if best_feature is None or best_gain <= 0:
        return importances

    importances[best_feature] += best_gain * len(y)

    left_mask = X[:, best_feature] <= best_threshold
    right_mask = ~left_mask

    importances += _build_tree_importance(
        X[left_mask],
        y[left_mask],
        feature_subset,
        max_depth,
        depth + 1
    )

    importances += _build_tree_importance(
        X[right_mask],
        y[right_mask],
        feature_subset,
        max_depth,
        depth + 1
    )

    return importances
```

### Giải thích

- `gini_impurity()`: tính chỉ số **Gini Impurity**.
- `best_split()`: tìm ngưỡng chia có **Gini Gain** lớn nhất.
- `tree_importance()`: xây dựng nhiều cây và tổng hợp độ quan trọng của các đặc trưng.
- `_build_tree_importance()`: xây dựng cây đệ quy và cộng dồn mức giảm impurity của từng đặc trưng.

> **Mục tiêu:** Đánh giá mức độ quan trọng của đặc trưng dựa trên **tổng mức giảm Gini Impurity** trong nhiều cây quyết định. Đặc trưng tạo ra mức giảm impurity càng lớn sẽ có **Feature Importance** càng cao.

### Step 7: Run all methods and compare
The code file runs all five methods on the same synthetic dataset and prints a comparison table showing which features each method selects.

## Use it

Scikit-learn cung cấp sẵn các phương pháp **Feature Selection**, giúp xây dựng pipeline nhanh hơn, tối ưu hơn và dễ tích hợp vào quy trình huấn luyện mô hình.

```python
import numpy as np

from sklearn.feature_selection import (
    VarianceThreshold,
    mutual_info_classif,
    RFE,
    SelectFromModel,
)

from sklearn.linear_model import (
    Lasso,
    LogisticRegression,
)

from sklearn.ensemble import RandomForestClassifier


# Variance Threshold
vt = VarianceThreshold(threshold=0.01)
X_filtered = vt.fit_transform(X)

# Mutual Information
mi_scores = mutual_info_classif(X, y)
top_k = np.argsort(mi_scores)[-10:]

# Recursive Feature Elimination (RFE)
rfe_selector = RFE(
    LogisticRegression(),
    n_features_to_select=10
)
rfe_selector.fit(X, y)
X_rfe = rfe_selector.transform(X)

# L1 (Lasso)
lasso_selector = SelectFromModel(
    Lasso(alpha=0.01)
)
lasso_selector.fit(X, y)
X_lasso = lasso_selector.transform(X)

# Tree-Based Feature Importance
rf = RandomForestClassifier(
    n_estimators=100
)
rf.fit(X, y)

importances = rf.feature_importances_
```

### Giải thích

- **VarianceThreshold:** loại bỏ các đặc trưng có phương sai thấp.
- **mutual_info_classif:** tính điểm Mutual Information cho từng đặc trưng.
- **RFE:** loại bỏ dần các đặc trưng ít quan trọng.
- **SelectFromModel (Lasso):** lựa chọn các đặc trưng có trọng số khác 0.
- **RandomForestClassifier:** đánh giá Feature Importance dựa trên mức giảm impurity.

### So sánh với cài đặt từ đầu

| From Scratch | Scikit-learn |
|--------------|--------------|
| Giúp hiểu rõ nguyên lý hoạt động của từng thuật toán. | Được tối ưu về tốc độ và độ ổn định. |
| Tự cài đặt từng bước tính toán. | Chỉ cần gọi API có sẵn. |
| Phù hợp cho học tập và nghiên cứu. | Phù hợp cho xây dựng hệ thống thực tế (Production). |

> **Điểm cần nhớ:** Các phiên bản **From Scratch** giúp hiểu bản chất của thuật toán, trong khi **Scikit-learn** cung cấp các cài đặt đã được tối ưu về hiệu năng, độ chính xác và khả năng tích hợp vào pipeline Machine Learning.
