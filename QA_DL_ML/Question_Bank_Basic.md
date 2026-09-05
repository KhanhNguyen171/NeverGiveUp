# MACHINE LEARNING & DEEP LEARNING — QA QUESTION BANK

# Chương 1. Mathematical Foundations for ML

## 1.1 Linear Algebra

1. __Vector, matrix và tensor khác nhau như thế nào?__
    - __Vector:__ mảng một chiều, biểu diễn một điểm hoặc một hướng trong không gian. 
        - $\mathbf{x}\in\mathbb{R}^n$
        - Vector → một sample hoặc feature vector.
    - __Matrix:__ mảng hai chiều gồm các hàng và cột. 
        - $A\in\mathbb{R}^{m\times n}$
        - Matrix → dataset, weight matrix.
    - __Tensor:__ mở rộng của vector và matrix lên nhiều chiều. 
        - $X\in\mathbb{R}^{d_1\times d_2\times\cdots\times d_k}$
        - Tensor → dữ liệu ảnh, video, batch dữ liệu neural network.

---

2. __Dot product có ý nghĩa hình học và ML như thế nào?__
    - Với hai vector: $ \mathbf{x},\mathbf{y}\in\mathbb{R}^n $
    - dot product: $ \mathbf{x}^\top\mathbf{y} = \sum_{i=1}^{n}x_i y_i$
    - Về hình học: $ \mathbf{x}^\top\mathbf{y} = \|\mathbf{x}\|\|\mathbf{y}\|\cos\theta$ 
    - Do đó dot product đo mức độ cùng hướng của hai vector.
    - Trong ML, nó xuất hiện trong: Linear regression, Neural network: $Wx$, Similarity, Attention: $QK^\top$.

---

3. __Matrix multiplication hoạt động như thế nào?__
    - Cho: $ A\in\mathbb{R}^{m\times n}, \qquad B\in\mathbb{R}^{n\times p} $ 
    - thì: $C=AB\in\mathbb{R}^{m\times p}$
    - Mỗi phần tử: $ C_{ij} = \sum_{k=1}^{n}A_{ik}B_{kj} $
    - Điều kiện quan trọng:
    $$\boxed{\text{số cột của }A=\text{số hàng của }B}$$
    - Matrix multiplication có thể xem là tổ hợp tuyến tính các vector.

---

4. __Vì sao phép nhân ma trận xuất hiện xuyên suốt trong neural network?__
    - Một layer tuyến tính có dạng:
    $$ \mathbf{y}=W\mathbf{x}+\mathbf{b} $$
    - Trong đó:
        - $x$: input.
        - $W$: learnable parameters.
        - $b$: bias.
        - $y$: output.
    - Phép nhân $W x$ thực hiện __linear transformation__ từ không gian input sang không gian output.

    - Một neural network về cơ bản liên tục thực hiện:
    $$ x \rightarrow W_1x \rightarrow f \rightarrow W_2x \rightarrow f \rightarrow\cdots $$

    - Trong đó $f$ là nonlinear activation.
    - __Ý chính: matrix multiplication__ là phép toán cốt lõi để biến đổi representation trong neural network.

---

5. __Eigenvalue và eigenvector là gì?__
    - Với ma trận vuông $A$, eigenvector $\mathbf{v}$ thỏa:

    $$ A\mathbf{v}=\lambda\mathbf{v} $$

    - Trong đó:
        - $\mathbf{v}$: eigenvector.
        - $\lambda$: eigenvalue.

    - Ý nghĩa:

    > Khi biến đổi vector $\mathbf{v}$ bằng $A$, hướng của $\mathbf{v}$ không thay đổi; chỉ độ lớn thay đổi bởi $\lambda$.

    - Eigenvalue được tìm từ:

    $$ \det(A-\lambda I)=0 $$

---

6. __Eigen decomposition có ý nghĩa gì trong Machine Learning?__
    - Với một số ma trận phù hợp:
    $$ A=V\Lambda V^{-1} $$

    - Trong đó:
        - $V$: các eigenvector.
        - $\Lambda$: ma trận đường chéo chứa eigenvalue.

    - Eigen decomposition cho phép biểu diễn một transformation theo các __hướng đặc biệt của không gian__.

    - Trong ML, nó quan trọng trong: 
        - PCA.
        - Phân tích covariance matrix.
        - Dimensionality reduction.
        - Phân tích stability và optimization.

    - Đặc biệt trong PCA, eigenvectors của covariance matrix xác định các __principal directions__, còn eigenvalues biểu diễn lượng variance theo các hướng đó.

---

7. __SVD là gì và tại sao nó quan trọng?__
    - SVD phân rã một ma trận:
    $$ A=U\Sigma V^\top $$
    - với:
        - $U$: left singular vectors.
        - $\Sigma$: singular values.
        - $V$: right singular vectors.

    - SVD tồn tại cho __mọi ma trận thực.__

    - Các singular values: $\sigma_1\geq\sigma_2\geq\cdots\geq0$ cho biết mức độ quan trọng của các directions.

    - SVD quan trọng vì được dùng cho:
        - PCA.
        - Dimensionality reduction.
        - Low-rank approximation.
        - Matrix compression.
        - Pseudoinverse.
        - Recommendation systems.

---

8. __Rank của ma trận có ý nghĩa gì?__
    - __Rank__ là số lượng chiều độc lập tuyến tính mà ma trận có thể biểu diễn.

    $$ \operatorname{rank}(A) = \text{số lượng independent rows} $$

    - và cũng bằng:

    $$ \operatorname{rank}(A) = \text{số lượng independent columns} $$

    - Với: $ A\in\mathbb{R}^{m\times n} $

    - ta có: $ \operatorname{rank}(A)\leq\min(m,n) $

    - Rank thấp nghĩa là dữ liệu/biến đổi có __redundancy__ và thực sự nằm trong không gian có số chiều nhỏ hơn.

---

9. __Norm là gì? Phân biệt $L_1$, $L_2$ và Frobenius norm.__
    - Norm đo __độ lớn__ của vector hoặc matrix.

    - $L_1$ norm Với vector: Thường liên quan đến sparsity.

    $$\|\mathbf{x}\|_1 = \sum_i |x_i|$$

    - $L_2$ norm: Đây là Euclidean length.

    $$\|\mathbf{x}\|_2 = \sqrt{\sum_i x_i^2}$$

    - __Frobenius norm__ Dùng cho matrix:

    $$ \|A\|_F = \sqrt{\sum_i\sum_j A_{ij}^2} $$

    - Có thể xem là $L_2$ norm của toàn bộ phần tử trong matrix.

    - Trong ML, norms thường xuất hiện trong __regularization__:

    $$ L=L_{\text{data}}+\lambda\|W\| $$

---

10. __Orthogonality là gì?__
    - Hai vector $\mathbf{x}$ và $\mathbf{y}$ trực giao nếu:

    $$ \mathbf{x}^\top\mathbf{y}=0 $$

    - tương đương: $ \cos\theta=0 $ nên: $ \theta=90^\circ $

    - Một matrix $Q$ là orthogonal nếu:

    $$ Q^\top Q=I $$

    - Do đó:

    $$ Q^{-1}=Q^\top $$

    - Orthogonal transformation bảo toàn norm:

    $$ \|Qx\|_2=\|x\|_2 $$

---

11. __Positive definite và positive semidefinite matrix là gì?__
    - Xét matrix đối xứng $A$.

    - __Positive definite (PD):__
    $$ \boxed{x^\top Ax>0,\quad\forall x\neq0} $$

    - Tương đương tất cả eigenvalues của $A$ đều dương: $ \lambda_i>0 $

    - __Positive semidefinite (PSD):__

    $$ \boxed{x^\top Ax\geq0,\quad\forall x} $$

    - Tương đương: $ \lambda_i\geq0 $ Do đó: $ PD\Rightarrow PSD $ nhưng: $ PSD\not\Rightarrow PD $. PSD có thể có eigenvalue bằng $0$.

---

12. __Covariance matrix có những tính chất gì?__
    - Với random vector: $ X\in\mathbb{R}^d $

    - __covariance matrix:__

    $$ \Sigma = \mathbb{E} [(X-\mu)(X-\mu)^\top] $$

    - Trong đó:

    $$ \mu=\mathbb{E}[X] $$

    - Các tính chất quan trọng:

        1. __Square matrix__
        $$\Sigma\in\mathbb{R}^{d\times d}$$
        2. __Symmetric__
        $$\Sigma^\top=\Sigma$$
        3. __Positive semidefinite__
        $$\mathbf{x}^\top\Sigma\mathbf{x}\geq0$$
        4. __Diagonal chứa variance của từng feature:__
        $$\Sigma_{ii}=\operatorname{Var}(X_i)$$
        5. __Off-diagonal chứa covariance:__
        $$\Sigma_{ij}=\operatorname{Cov}(X_i,X_j)$$

---

13. __Vì sao covariance matrix luôn positive semidefinite?__
    - Bắt đầu từ:
    $$ \Sigma = \mathbb{E} [(X-\mu)(X-\mu)^\top] $$

    - Với một vector bất kỳ $a$:

    $$ a^\top\Sigma a $$

    - ta có:

    $$ a^\top\Sigma a = a^\top \mathbb{E}[(X-\mu)(X-\mu)^\top] a $$

    - Đưa $a$ vào trong:

    $$ = \mathbb{E} \left[ a^\top(X-\mu)(X-\mu)^\top a \right] $$ $$ = \mathbb{E} \left[ \left(a^\top(X-\mu)\right)^2 \right] $$

    - Mà bình phương luôn không âm:

    $$ \left(a^\top(X-\mu)\right)^2\geq0 $$

    - nên:

    $$ \boxed{a^\top\Sigma a\geq0} $$

    - Do đó:

    $$ \boxed{\Sigma\text{ là positive semidefinite}} $$

    - __Đây là điểm rất quan trọng:__ $a^\top\Sigma a$ chính là __variance__ của projection $a^\top X$:

    $$ a^\top\Sigma a = \operatorname{Var}(a^\top X)\geq0 $$

    - Vì variance không thể âm, covariance matrix bắt buộc phải là PSD.

---

## 1.2 Calculus

14. Derivative là gì?
15. Partial derivative là gì?
16. Gradient là gì?
17. Jacobian là gì?
18. Hessian là gì?
19. Gradient biểu diễn điều gì về hàm loss?
20. Hessian cung cấp thông tin gì mà gradient không có?
21. Chain rule là gì?
22. Vì sao chain rule là nền tảng của backpropagation?
23. Directional derivative là gì?
24. Local minimum, global minimum và saddle point khác nhau như thế nào?

## 1.3 Probability & Statistics

25. Random variable là gì?
26. Probability distribution là gì?
27. Expected value và variance là gì?
28. Covariance và correlation khác nhau như thế nào?
29. Conditional probability là gì?
30. Bayes' theorem là gì?
31. Independence và conditional independence khác nhau như thế nào?
32. Maximum Likelihood Estimation là gì?
33. Maximum A Posteriori là gì?
34. Bias và variance trong statistical learning là gì?
35. Law of Large Numbers và Central Limit Theorem có vai trò gì trong ML?

---

# Chương 2. Machine Learning Fundamentals

## 2.1 Learning Problem

36. Machine Learning là gì?
37. Supervised, unsupervised và reinforcement learning khác nhau như thế nào?
38. Feature, target và label là gì?
39. Training set, validation set và test set có vai trò gì?
40. Vì sao không được sử dụng test set để tuning model?
41. Data leakage là gì?
42. Model parameter và hyperparameter khác nhau như thế nào?
43. Empirical risk và expected risk là gì?
44. Generalization là gì?
45. Overfitting và underfitting là gì?
46. Bias-variance tradeoff là gì?

## 2.2 ML Pipeline

47. Một ML pipeline thực tế gồm những bước nào?
48. Data preprocessing nên được thực hiện ở đâu trong pipeline?
49. Khi nào cần normalization?
50. Khi nào cần standardization?
51. Vì sao scaler phải được fit trên training data?
52. Missing values nên được xử lý như thế nào?
53. Outlier ảnh hưởng đến ML model như thế nào?
54. Feature engineering là gì?
55. Feature selection và feature extraction khác nhau như thế nào?
56. Cross-validation hoạt động như thế nào?
57. Stratified cross-validation dùng khi nào?
58. Time-series data cần split như thế nào để tránh leakage?

---

# Chương 3. Linear Regression

59. Linear Regression giải quyết bài toán gì?
60. Mô hình Linear Regression được biểu diễn như thế nào?
61. Ordinary Least Squares là gì?
62. Vì sao OLS sử dụng squared error?
63. Hàm loss MSE được xây dựng như thế nào?
64. Làm thế nào để suy ra nghiệm đóng của Linear Regression?
65. Normal Equation là gì?
66. Khi nào Normal Equation không phù hợp?
67. Gradient Descent giải Linear Regression như thế nào?
68. Batch GD, SGD và Mini-batch GD khác nhau như thế nào?
69. Learning rate ảnh hưởng thế nào đến quá trình tối ưu?
70. Multicollinearity là gì?
71. Ridge Regression là gì?
72. Lasso Regression là gì?
73. Elastic Net là gì?
74. Vì sao L1 có khả năng tạo sparse model?
75. Ridge và Lasso khác nhau về mặt optimization như thế nào?

---

# Chương 4. Classification

## 4.1 Logistic Regression

76. Logistic Regression khác Linear Regression như thế nào?
77. Vì sao Logistic Regression sử dụng sigmoid?
78. Sigmoid function có những tính chất gì?
79. Log-odds là gì?
80. Binary Cross-Entropy được suy ra như thế nào?
81. Vì sao Logistic Regression có thể được xem là probabilistic model?
82. Decision boundary của Logistic Regression được xác định như thế nào?
83. Logistic Regression có thể giải quyết multiclass classification không?
84. One-vs-Rest và Softmax classification khác nhau như thế nào?

## 4.2 Classification Metrics

85. Confusion matrix là gì?
86. Accuracy là gì?
87. Precision và Recall khác nhau như thế nào?
88. F1-score là gì?
89. ROC curve là gì?
90. AUC có ý nghĩa gì?
91. Khi nào accuracy là metric không phù hợp?
92. Precision-recall tradeoff là gì?
93. Threshold classification ảnh hưởng đến precision và recall như thế nào?

---

# Chương 5. Decision Trees

94. Decision Tree hoạt động dựa trên nguyên lý nào?
95. Entropy là gì?
96. Information Gain là gì?
97. Gini Impurity là gì?
98. Information Gain và Gini Impurity khác nhau như thế nào?
99. Decision Tree chọn feature để split như thế nào?
100. Vì sao Decision Tree dễ overfit?
101. Maximum depth có tác dụng gì?
102. Minimum samples split và minimum samples leaf là gì?
103. Pruning là gì?
104. Decision Tree Regression khác Classification như thế nào?
105. Decision Tree có cần feature scaling không?
106. Vì sao Decision Tree có thể biểu diễn nonlinear decision boundary?

---

# Chương 6. Ensemble Learning

107. Ensemble Learning là gì?
108. Bagging là gì?
109. Boosting là gì?
110. Random Forest hoạt động như thế nào?
111. Vì sao Random Forest sử dụng bootstrap sampling?
112. Random feature selection có tác dụng gì?
113. Random Forest giảm variance như thế nào?
114. AdaBoost hoạt động như thế nào?
115. Gradient Boosting hoạt động như thế nào?
116. XGBoost khác Gradient Boosting truyền thống như thế nào?
117. Bagging và Boosting khác nhau về cơ chế học như thế nào?
118. Vì sao Boosting có thể dễ overfit?
119. Feature importance trong tree-based models được tính như thế nào?

---

# Chương 7. K-Nearest Neighbors

120. KNN hoạt động như thế nào?
121. Khoảng cách Euclidean có ý nghĩa gì?
122. Manhattan distance khác Euclidean distance như thế nào?
123. $k$ ảnh hưởng thế nào đến KNN?
124. $k$ quá nhỏ gây vấn đề gì?
125. $k$ quá lớn gây vấn đề gì?
126. Vì sao KNN nhạy với feature scaling?
127. Curse of dimensionality là gì?
128. KNN có training phase thực sự hay không?
129. Độ phức tạp inference của KNN là gì?
130. Khi nào KNN phù hợp và khi nào không?

---

# Chương 8. Support Vector Machine

131. SVM giải quyết bài toán gì?
132. Hyperplane là gì?
133. Margin là gì?
134. Support vectors là gì?
135. Vì sao SVM muốn maximize margin?
136. Hard-margin và soft-margin SVM khác nhau như thế nào?
137. Parameter $C$ có ý nghĩa gì?
138. Hinge loss là gì?
139. Kernel trick là gì?
140. Linear kernel, polynomial kernel và RBF kernel khác nhau như thế nào?
141. Vì sao kernel giúp SVM xử lý nonlinear problem?
142. $C$ và $\gamma$ trong RBF SVM ảnh hưởng thế nào đến model?
143. SVM có cần feature scaling không?

---

# Chương 9. Unsupervised Learning

## 9.1 Clustering

144. Unsupervised Learning khác Supervised Learning như thế nào?
145. K-Means hoạt động như thế nào?
146. Objective function của K-Means là gì?
147. Vì sao K-Means hội tụ?
148. K-Means initialization ảnh hưởng như thế nào?
149. K-Means++ là gì?
150. Làm thế nào chọn $K$?
151. Elbow method là gì?
152. Silhouette score là gì?
153. Khi nào K-Means thất bại?
154. K-Means có nhạy với scaling không?
155. Hierarchical clustering là gì?
156. Agglomerative và divisive clustering khác nhau như thế nào?
157. DBSCAN hoạt động dựa trên nguyên lý nào?
158. DBSCAN xử lý noise như thế nào?
159. K-Means và DBSCAN khác nhau như thế nào?

---

# Chương 10. Dimensionality Reduction

160. Vì sao cần dimensionality reduction?
161. Curse of dimensionality ảnh hưởng thế nào đến ML?
162. PCA là gì?
163. PCA tối ưu objective function nào?
164. PCA liên quan thế nào đến covariance matrix?
165. Vì sao eigenvectors của covariance matrix xuất hiện trong PCA?
166. Principal components có ý nghĩa gì?
167. Explained variance là gì?
168. PCA có cần standardization không?
169. PCA và feature selection khác nhau như thế nào?
170. PCA có thể sử dụng cho supervised learning không?
171. PCA có thể gây information loss như thế nào?

---

# Chương 11. Neural Network Fundamentals

## 11.1 Perceptron

172. Perceptron là gì?
173. Một neuron thực hiện phép tính gì?
174. Activation function có vai trò gì?
175. Vì sao neural network cần nonlinear activation?
176. Perceptron có thể giải XOR không?
177. Vì sao một linear layer không thể giải quyết XOR?

## 11.2 MLP

178. Multi-Layer Perceptron là gì?
179. Forward propagation là gì?
180. Computational graph là gì?
181. Backpropagation là gì?
182. Chain rule được sử dụng trong backpropagation như thế nào?
183. Gradient của một layer được tính như thế nào?
184. Vanishing gradient là gì?
185. Exploding gradient là gì?
186. Saturation của activation function là gì?
187. Sigmoid, Tanh và ReLU khác nhau như thế nào?
188. Vì sao ReLU phổ biến hơn sigmoid trong hidden layers?
189. Dying ReLU là gì?
190. Leaky ReLU giải quyết vấn đề gì?

---

# Chương 12. Loss Functions

191. Loss function là gì?
192. Objective function và loss function khác nhau như thế nào?
193. MSE phù hợp với bài toán nào?
194. MAE khác MSE như thế nào?
195. Binary Cross-Entropy là gì?
196. Categorical Cross-Entropy là gì?
197. Vì sao Cross-Entropy phù hợp với classification?
198. Softmax kết hợp với Cross-Entropy như thế nào?
199. NLL Loss là gì?
200. Huber Loss là gì?
201. Loss function ảnh hưởng thế nào đến gradient?
202. Một loss function tốt cần những đặc tính gì?

---

# Chương 13. Optimization & Training Algorithms

Chapter 4 của tài liệu bạn gửi đặt trọng tâm vào loss, optimizer, learning rate, batch size, epochs và các thuật toán GD/SGD/Adam/RMSprop/Adagrad/Adadelta/AdamW/LBFGS. 

### 13.1 Gradient Descent

203. Gradient Descent là gì?
204. Tại sao update parameter theo negative gradient?
205. Learning rate có ý nghĩa gì?
206. Learning rate quá lớn gây ra điều gì?
207. Learning rate quá nhỏ gây ra điều gì?
208. Batch Gradient Descent là gì?
209. SGD là gì?
210. Mini-batch Gradient Descent là gì?
211. Vì sao mini-batch thường được sử dụng trong Deep Learning?
212. Noise trong stochastic gradient có lợi hay có hại?

### 13.2 Momentum

213. Momentum giải quyết vấn đề gì?
214. Momentum được xây dựng về mặt toán học như thế nào?
215. Momentum ảnh hưởng thế nào đến oscillation?
216. Nesterov Momentum là gì?
217. Momentum và learning rate có quan hệ như thế nào?

### 13.3 Adaptive Optimizers

218. AdaGrad hoạt động như thế nào?
219. Vì sao AdaGrad phù hợp với sparse features?
220. Nhược điểm chính của AdaGrad là gì?
221. RMSprop giải quyết vấn đề gì của AdaGrad?
222. Adam kết hợp những ý tưởng nào?
223. First moment và second moment trong Adam là gì?
224. Vì sao Adam cần bias correction?
225. Vai trò của $\beta_1$ và $\beta_2$ là gì?
226. Adam và SGD khác nhau như thế nào?
227. Khi nào SGD có thể được ưu tiên hơn Adam?
228. AdamW khác Adam như thế nào?
229. Weight decay trong AdamW được decouple như thế nào?
230. LBFGS là gì?
231. Vì sao LBFGS được xem là quasi-Newton method?
232. Hessian approximation được sử dụng như thế nào trong LBFGS?

Tài liệu cũng nhấn mạnh AdamW, Adam và SGD with momentum như các lựa chọn optimizer phổ biến, đồng thời mô tả LBFGS theo hướng quasi-Newton. 

---

# Chương 14. Learning Rate Scheduling

233. Learning-rate scheduling là gì?
234. Vì sao không luôn giữ learning rate cố định?
235. StepLR hoạt động như thế nào?
236. MultiStepLR khác StepLR như thế nào?
237. ExponentialLR là gì?
238. Cosine Annealing là gì?
239. ReduceLROnPlateau hoạt động dựa trên điều kiện nào?
240. CyclicLR là gì?
241. OneCycleLR là gì?
242. Epoch-based scheduler và iteration-based scheduler khác nhau như thế nào?
243. Khi nào gọi `scheduler.step()`?
244. Vì sao ReduceLROnPlateau cần validation metric?
245. Learning-rate schedule ảnh hưởng thế nào đến convergence?
246. Learning-rate schedule ảnh hưởng thế nào đến generalization?

Các scheduler trên đều được trình bày trong Chapter 4, cùng với cách sử dụng `scheduler.step()` theo từng loại. 

---

# Chương 15. Regularization

247. Regularization là gì?
248. Vì sao regularization giúp giảm overfitting?
249. L1 regularization hoạt động như thế nào?
250. L2 regularization hoạt động như thế nào?
251. L1 và L2 khác nhau về ảnh hưởng đến weights như thế nào?
252. Weight decay có liên hệ gì với L2 regularization?
253. Dropout là gì?
254. Dropout hoạt động như thế nào trong training?
255. Tại sao dropout phải được tắt trong evaluation?
256. Dropout rate ảnh hưởng thế nào đến model?
257. Early stopping là gì?
258. Vì sao validation set được sử dụng trong early stopping?
259. Patience là gì?
260. Data augmentation có phải regularization không?
261. Regularization và data augmentation khác nhau như thế nào?

Chapter 4 trình bày Dropout, weight decay và early stopping như các kỹ thuật regularization chính. 

---

# Chương 16. Batch Normalization & Initialization

262. Batch Normalization là gì?
263. Vì sao BatchNorm có thể giúp training ổn định hơn?
264. BatchNorm được thực hiện ở vị trí nào trong neural network?
265. Training mode và evaluation mode của BatchNorm khác nhau như thế nào?
266. Batch size ảnh hưởng đến BatchNorm như thế nào?
267. Xavier initialization là gì?
268. He initialization là gì?
269. Vì sao initialization quan trọng?
270. Poor initialization gây ra vấn đề gì?
271. Xavier phù hợp với activation nào?
272. He initialization phù hợp với activation nào?

---

# Chương 17. Gradient Problems

273. Vanishing gradient xảy ra như thế nào?
274. Exploding gradient xảy ra như thế nào?
275. Tại sao sigmoid dễ gây vanishing gradient?
276. Deep network ảnh hưởng thế nào đến gradient?
277. RNN đặc biệt dễ gặp gradient problem vì sao?
278. Gradient clipping là gì?
279. Clipping by value và clipping by norm khác nhau như thế nào?
280. Vì sao gradient clipping thường được dùng cho RNN?
281. Gradient clipping nên đặt ở đâu trong training loop?
282. Gradient clipping có giải quyết vanishing gradient không?
283. Gradient clipping ảnh hưởng thế nào đến optimization?

Chapter 4 xác định gradient clipping là kỹ thuật giới hạn độ lớn gradient, đặc biệt hữu ích với RNN và đặt sau `loss.backward()` nhưng trước optimizer update. 

---

# Chương 18. Convolutional Neural Networks

284. CNN giải quyết vấn đề gì?
285. Convolution operation là gì?
286. Kernel/filter là gì?
287. Receptive field là gì?
288. Stride là gì?
289. Padding là gì?
290. Output size của convolution được tính như thế nào?
291. Parameter sharing là gì?
292. Vì sao CNN có inductive bias về locality?
293. CNN học spatial hierarchy như thế nào?
294. Pooling có tác dụng gì?
295. Max pooling và average pooling khác nhau như thế nào?
296. $1\times1$ convolution có tác dụng gì?
297. Dilated convolution là gì?
298. Depthwise convolution là gì?
299. CNN khác Fully Connected Network như thế nào?
300. Vì sao CNN thường hiệu quả với image data?

---

# Chương 19. RNN

Chapter 6 xác định RNN là kiến trúc dành cho sequence data, sử dụng recurrent connection và hidden state để duy trì thông tin từ các time step trước. 

### 19.1 Fundamental RNN

301. Sequence data là gì?
302. Vì sao order của sequence quan trọng?
303. RNN khác feedforward neural network như thế nào?
304. Recurrent connection là gì?
305. Hidden state là gì?
306. RNN cập nhật hidden state như thế nào?
307. Tại sao RNN có khả năng biểu diễn temporal dependency?
308. RNN xử lý sequence theo cơ chế nào?
309. RNN có thể xử lý sequence có độ dài thay đổi không?
310. RNN có những dạng input-output architecture nào?
311. Many-to-one là gì?
312. One-to-many là gì?
313. Many-to-many là gì?
314. Encoder-decoder khác synchronized sequence-to-sequence như thế nào?

Tài liệu mô tả các dạng sequence architecture từ fixed input/output đến sequence-to-sequence và synchronized sequence input/output. 

### 19.2 RNN Training

315. RNN được train bằng backpropagation như thế nào?
316. Backpropagation Through Time (BPTT) là gì?
317. Vì sao BPTT có thể gây vanishing gradient?
318. Vì sao BPTT có thể gây exploding gradient?
319. Sequence length ảnh hưởng thế nào đến computational cost?
320. Hidden state có được giữ giữa các sequence không?
321. Truncated BPTT là gì?
322. Gradient clipping giải quyết vấn đề gì trong RNN?

---

# Chương 20. LSTM

323. Tại sao LSTM được phát triển?
324. LSTM giải quyết hạn chế nào của Vanilla RNN?
325. Cell state là gì?
326. Hidden state và cell state khác nhau như thế nào?
327. Forget gate là gì?
328. Input gate là gì?
329. Output gate là gì?
330. Candidate cell state là gì?
331. Sigmoid được sử dụng trong gates để làm gì?
332. Tanh được sử dụng ở đâu trong LSTM?
333. LSTM cập nhật cell state như thế nào?
334. LSTM giúp gradient truyền qua sequence như thế nào?
335. Tại sao LSTM có khả năng học long-term dependency tốt hơn Vanilla RNN?
336. LSTM có hoàn toàn loại bỏ vanishing gradient không?
337. Bidirectional LSTM là gì?
338. Stacked LSTM là gì?
339. ConvLSTM là gì?
340. LSTM kết hợp Attention như thế nào?

Chapter 6 giới thiệu LSTM như một RNN được thiết kế để học long-term dependencies và liệt kê BiLSTM, ConvLSTM và LSTM kết hợp attention. 

---

# Chương 21. GRU

341. GRU là gì?
342. Tại sao GRU được xem là simplified LSTM?
343. GRU có những gates nào?
344. Update gate có vai trò gì?
345. Reset gate có vai trò gì?
346. GRU khác LSTM ở hidden state như thế nào?
347. GRU có cell state không?
348. Vì sao GRU thường có ít parameters hơn LSTM?
349. Khi nào GRU có thể được ưu tiên hơn LSTM?
350. GRU có giải quyết vanishing gradient giống LSTM không?
351. GRU và Vanilla RNN khác nhau như thế nào?
352. GRU và LSTM khác nhau về computational cost như thế nào?

Chapter 6 nêu rõ GRU sử dụng một hidden state và hai gate, trong khi LSTM có hidden state + cell state và ba gate tiêu chuẩn. 

---

# Chương 22. Encoder–Decoder

353. Encoder-decoder architecture là gì?
354. Encoder có nhiệm vụ gì?
355. Decoder có nhiệm vụ gì?
356. Context vector là gì?
357. Tại sao encoder-decoder phù hợp với sequence-to-sequence?
358. Input sequence và output sequence có cần cùng độ dài không?
359. Decoder sử dụng thông tin nào để sinh token tiếp theo?
360. Start-of-sequence token có vai trò gì?
361. End-of-sequence token có vai trò gì?
362. Encoder-decoder vanilla gặp bottleneck nào?
363. Attention được đưa vào encoder-decoder để giải quyết vấn đề gì?

Chapter 6 mô tả encoder đọc sequence và tạo context representation, sau đó decoder sinh output từng phần tử cho tới end-of-sequence token. 

---

# Chương 23. Attention & Transformer

364. Attention mechanism là gì?
365. Query, Key và Value là gì?
366. Self-attention là gì?
367. Scaled dot-product attention được tính như thế nào?
368. Vì sao phải scale $QK^T$?
369. Multi-head attention là gì?
370. Vì sao cần nhiều attention heads?
371. Self-attention khác convolution như thế nào?
372. Self-attention khác RNN như thế nào?
373. Vì sao Transformer không cần recurrent connection?
374. Positional encoding giải quyết vấn đề gì?
375. Encoder và decoder của Transformer khác nhau như thế nào?
376. Causal attention là gì?
377. Transformer có ưu điểm gì so với RNN?
378. Transformer có nhược điểm gì?
379. Vì sao attention complexity thường là $O(n^2)$ theo sequence length?

---

# Chương 24. Representation Learning

380. Representation learning là gì?
381. Feature learning khác feature engineering như thế nào?
382. Embedding là gì?
383. Word embedding biểu diễn điều gì?
384. One-hot encoding khác embedding như thế nào?
385. Vì sao embedding có thể biểu diễn semantic relationship?
386. Latent representation là gì?
387. Autoencoder là gì?
388. Encoder và decoder của Autoencoder làm gì?
389. Reconstruction loss là gì?
390. Bottleneck có vai trò gì?

---

# Chương 25. Transfer Learning & Fine-Tuning

Chapter 4 định nghĩa fine-tuning là tiếp tục train pretrained model trên dataset/task cụ thể; quy trình gồm chọn pretrained model, chuẩn bị dataset, sửa architecture, freeze/unfreeze layers, train, evaluate và tuning hyperparameters. 

391. Transfer Learning là gì?
392. Pretrained model là gì?
393. Fine-tuning khác training from scratch như thế nào?
394. Khi nào nên sử dụng pretrained model?
395. Khi nào không nên fine-tune?
396. Vì sao pretrained features có thể hữu ích cho target task?
397. Vì sao dataset similarity ảnh hưởng đến fine-tuning?
398. Vì sao dataset nhỏ thường cần freeze nhiều layers hơn?
399. Layer freezing là gì?
400. Layer unfreezing là gì?
401. Vì sao fine-tuning thường sử dụng learning rate nhỏ?
402. Discriminative learning rate là gì?
403. Catastrophic forgetting là gì?
404. Fine-tuning toàn bộ model và partial fine-tuning khác nhau như thế nào?
405. Fine-tuning classification model cần thay đổi output layer như thế nào?
406. Fine-tuning language model khác image classification fine-tuning như thế nào?

---

# Chương 26. PyTorch Training Pipeline

407. `Dataset` có vai trò gì?
408. `DataLoader` có vai trò gì?
409. `batch_size` ảnh hưởng thế nào đến training?
410. `shuffle=True` có ý nghĩa gì?
411. Khi nào không nên shuffle data?
412. `drop_last=True` dùng khi nào?
413. `model.train()` khác `model.eval()` như thế nào?
414. `torch.no_grad()` có tác dụng gì?
415. `optimizer.zero_grad()` cần thiết vì sao?
416. `loss.backward()` làm gì?
417. `optimizer.step()` làm gì?
418. Một training iteration gồm những bước nào?
419. Một epoch là gì?
420. Validation loop khác training loop như thế nào?
421. Vì sao validation không cần backward?
422. Checkpoint nên lưu những thông tin nào?
423. Best model checkpoint khác last checkpoint như thế nào?

Chapter 4 mô tả Dataset/DataLoader, batching, shuffling và augmentation như các thành phần cốt lõi của PyTorch data pipeline. 

---

# Chương 27. Data Augmentation

424. Data augmentation là gì?
425. Vì sao augmentation giúp generalization?
426. Khi nào augmentation có thể làm hỏng dữ liệu?
427. Image augmentation gồm những phép biến đổi nào?
428. Random crop có tác dụng gì?
429. Random rotation có tác dụng gì?
430. Color jitter có tác dụng gì?
431. Gaussian blur có tác dụng gì?
432. Augmentation nên được áp dụng cho train, validation hay test?
433. Augmentation khác oversampling như thế nào?

---

# Chương 28. Evaluation & Generalization

434. Training loss giảm nhưng validation loss tăng nghĩa là gì?
435. Training accuracy cao nhưng test accuracy thấp nghĩa là gì?
436. Validation set được dùng để làm gì?
437. Test set được dùng để làm gì?
438. Cross-validation có thể thay thế test set không?
439. Model selection nên dựa trên metric nào?
440. Vì sao metric phải phù hợp với business/scientific objective?
441. Calibration là gì?
442. Generalization gap là gì?
443. Distribution shift là gì?
444. Covariate shift là gì?
445. Concept drift là gì?

---

# Chương 29. Debugging Machine Learning

446. Làm thế nào xác định model không học?
447. Nếu loss = NaN, cần kiểm tra những gì?
448. Nếu loss không giảm, cần kiểm tra những gì?
449. Nếu training loss giảm nhưng validation loss tăng, cần xử lý thế nào?
450. Nếu gradient bằng zero, nguyên nhân có thể là gì?
451. Nếu gradient quá lớn, nguyên nhân có thể là gì?
452. Làm thế nào kiểm tra gradient?
453. Làm thế nào kiểm tra model có thực sự update parameters?
454. Làm thế nào phát hiện data leakage?
455. Làm thế nào kiểm tra input shape?
456. Làm thế nào kiểm tra output shape?
457. Làm thế nào xác định learning rate không phù hợp?
458. Làm thế nào xác định batch size gây instability?
459. Làm thế nào kiểm tra preprocessing consistency giữa train và test?
460. Làm thế nào debug một training pipeline theo từng stage?

---

# Chương 30. ML/DL Interview — Fundamental Questions

461. Machine Learning là gì?
462. Deep Learning khác Machine Learning truyền thống như thế nào?
463. Model parameter và hyperparameter khác nhau thế nào?
464. Overfitting là gì và xử lý thế nào?
465. Underfitting là gì và xử lý thế nào?
466. Bias-variance tradeoff là gì?
467. Gradient Descent là gì?
468. SGD khác Batch GD thế nào?
469. Adam khác SGD thế nào?
470. Learning rate quan trọng như thế nào?
471. Batch size ảnh hưởng thế nào đến training?
472. Epoch là gì?
473. Regularization là gì?
474. Dropout hoạt động như thế nào?
475. BatchNorm hoạt động như thế nào?
476. Vanishing gradient là gì?
477. Exploding gradient là gì?
478. Backpropagation là gì?
479. CNN khác RNN như thế nào?
480. RNN khác Transformer như thế nào?
481. LSTM khác GRU như thế nào?
482. Transfer Learning là gì?
483. Fine-tuning là gì?
484. Data leakage là gì?
485. Tại sao test set phải được giữ độc lập?

---

# Chương 31. Algorithmic Interview — "Explain the Algorithm"

Với **mỗi thuật toán**, nên có một bộ câu hỏi cố định:

486. Thuật toán giải quyết bài toán gì?
487. Input của thuật toán là gì?
488. Output của thuật toán là gì?
489. Ý tưởng cốt lõi của thuật toán là gì?
490. Objective/Loss function là gì?
491. Thuật toán tối ưu objective như thế nào?
492. Công thức toán học của thuật toán là gì?
493. Thuật toán có những hyperparameter nào?
494. Hyperparameter nào quan trọng nhất?
495. Độ phức tạp thời gian là gì?
496. Độ phức tạp bộ nhớ là gì?
497. Thuật toán có assumption nào?
498. Khi nào thuật toán hoạt động tốt?
499. Khi nào thuật toán thất bại?
500. Điểm mạnh của thuật toán là gì?
501. Điểm yếu của thuật toán là gì?
502. Thuật toán khác phương pháp gần nhất ở điểm nào?
503. Có thể implement thuật toán từ scratch như thế nào?
504. Làm thế nào kiểm chứng implementation?
505. Làm thế nào debug implementation?

---

# Chương 32. Deep Learning Interview — Architecture Reasoning

506. Khi nào chọn MLP?
507. Khi nào chọn CNN?
508. Khi nào chọn RNN?
509. Khi nào chọn LSTM?
510. Khi nào chọn GRU?
511. Khi nào chọn Transformer?
512. Architecture nào phù hợp với spatial data?
513. Architecture nào phù hợp với sequential data?
514. Vì sao inductive bias quan trọng?
515. CNN có inductive bias gì?
516. RNN có inductive bias gì?
517. Transformer có inductive bias gì?
518. Tăng depth khác tăng width như thế nào?
519. Tăng model capacity ảnh hưởng thế nào đến bias và variance?
520. Làm thế nào chọn architecture dựa trên dataset?
521. Làm thế nào xác định bottleneck của model?

---

# Chương 33. Research-Level Questions

522. Model đang học representation hay memorization?
523. Làm thế nào chứng minh model generalize?
524. Objective function có thực sự phù hợp với task không?
525. Metric có phản ánh objective không?
526. Model improvement đến từ architecture hay data?
527. Làm thế nào thiết kế ablation study?
528. Làm thế nào xác định contribution của từng component?
529. Làm thế nào đảm bảo experiment reproducibility?
530. Random seed có ý nghĩa gì?
531. Làm thế nào phân biệt statistical improvement và random variation?
532. Làm thế nào thiết kế baseline?
533. Baseline tốt cần những đặc điểm gì?
534. Khi nào một model phức tạp không đáng sử dụng?
535. Làm thế nào đánh giá computational efficiency?
536. Accuracy tăng nhưng latency tăng mạnh có phải improvement không?
537. Làm thế nào đánh giá robustness?
538. Distribution shift ảnh hưởng thế nào đến model?
539. Làm thế nào phát hiện model đang exploit spurious correlation?
540. Làm thế nào thiết kế một experiment để kiểm chứng hypothesis?

---

## Cách sử dụng bộ QA này

Tôi khuyến nghị **không học 540 câu này như một danh sách thuộc lòng**. Với mỗi thuật toán, hãy buộc bản thân trả lời theo tầng:

> **Definition → Intuition → Mathematics → Algorithm → Assumptions → Complexity → Failure Cases → Comparison → Implementation → Debugging → Research**

Ví dụ với **LSTM**:

```text
Definition
    ↓
Tại sao cần LSTM?
    ↓
Vanilla RNN thất bại ở đâu?
    ↓
Cell state / Hidden state
    ↓
Forget / Input / Output gate
    ↓
Forward equations
    ↓
BPTT
    ↓
Vanishing / Exploding Gradient
    ↓
LSTM vs GRU
    ↓
LSTM vs Transformer
    ↓
PyTorch implementation
    ↓
Debugging
    ↓
Khi nào LSTM không còn là lựa chọn tốt?
```

Cấu trúc này phù hợp với cách học **nghiên cứu thuật toán**, thay vì chỉ học API/framework. Đặc biệt, Chapter 6 của bạn đi từ sequence data → RNN → các dạng architecture → LSTM → GRU → encoder-decoder, nên QA cũng nên giữ đúng progression đó.  

**Bộ trên có thể xem là Question Bank nền tảng.** Khi chuyển sang giai đoạn luyện phỏng vấn, có thể tách tiếp thành 3 cấp:

* **Level 1 — Fundamental:** định nghĩa, nguyên lý, công thức.
* **Level 2 — Algorithmic:** suy luận, so sánh, complexity, failure cases.
* **Level 3 — Research/Interview:** thiết kế model, debugging, ablation, trade-off và giải thích quyết định kiến trúc.
