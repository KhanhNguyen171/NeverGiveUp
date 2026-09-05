# Bộ câu hỏi QA — Decision Tree & Tree-Based Models

# Chương 1. Decision Tree — Fundamentals

### 1.1. Basic

1. Decision Tree là gì?
2. Decision Tree giải quyết được những loại bài toán nào?
3. Decision Tree cho classification hoạt động như thế nào?
4. Decision Tree cho regression hoạt động như thế nào?
5. Node là gì?
6. Root node là gì?
7. Internal node là gì?
8. Leaf node là gì?
9. Branch là gì?
10. Một Decision Tree đưa ra prediction như thế nào?
11. Decision Tree học từ dữ liệu như thế nào?
12. Feature được sử dụng trong Decision Tree như thế nào?
13. Split là gì?
14. Vì sao Decision Tree cần chia dữ liệu thành các subset?
15. Một split tốt được định nghĩa như thế nào?
16. Decision Tree lựa chọn feature để split bằng cách nào?
17. Decision Tree lựa chọn threshold như thế nào?
18. Vì sao Decision Tree có thể biểu diễn decision boundary phi tuyến?
19. Decision Tree có cần feature scaling không?
20. Decision Tree có cần chuẩn hóa dữ liệu không?
21. Decision Tree có xử lý categorical feature được không?
22. Decision Tree có xử lý missing value được không?
23. Decision Tree có thể biểu diễn interaction giữa các feature như thế nào?
24. Vì sao Decision Tree dễ interpret?
25. Prediction tại leaf node được xác định như thế nào?

---

# Chương 2. Decision Tree — Splitting Criteria

## 2.1. Entropy

26. Entropy là gì?
27. Entropy đo lường điều gì?
28. Viết công thức entropy.

$$
H(S)=-\sum_{k=1}^{K}p_k\log_2p_k
$$

29. Entropy bằng 0 có ý nghĩa gì?
30. Khi nào entropy đạt giá trị cực đại?
31. Entropy thay đổi như thế nào khi class distribution thay đổi?
32. Vì sao entropy được sử dụng để xây dựng Decision Tree?
33. Entropy của một node có 2 class được tính như thế nào?
34. Entropy của node thuần nhất bằng bao nhiêu?
35. Entropy có liên hệ gì với uncertainty?

## 2.2. Information Gain

36. Information Gain là gì?
37. Viết công thức Information Gain.

$$
IG(S,A)
=
H(S)
-
\sum_{v}
\frac{|S_v|}{|S|}
H(S_v)
$$

38. Tại sao Information Gain sử dụng weighted entropy?
39. Feature nào được chọn nếu có Information Gain lớn nhất?
40. Information Gain có bias đối với feature nhiều giá trị như thế nào?
41. Vì sao Decision Tree ID3 sử dụng Information Gain?
42. Information Gain và entropy liên hệ với nhau như thế nào?

## 2.3. Gini Impurity

43. Gini impurity là gì?
44. Viết công thức Gini.

$$
Gini(S)
=
1-\sum_{k=1}^{K}p_k^2
$$

45. Gini bằng 0 có ý nghĩa gì?
46. Gini khác entropy như thế nào?
47. Tại sao CART thường sử dụng Gini?
48. Gini và entropy có thường tạo ra tree giống nhau không?
49. Khi nào nên sử dụng Gini thay vì entropy?

## 2.4. Regression Criteria

50. Decision Tree Regression sử dụng tiêu chí split nào?
51. MSE trong Decision Tree Regression được sử dụng như thế nào?
52. Vì sao variance reduction có thể được sử dụng để chọn split?
53. Leaf prediction trong regression được tính như thế nào?
54. Tại sao prediction tại leaf thường là mean?
55. Nếu sử dụng MAE thay cho MSE thì prediction tại leaf thay đổi như thế nào?

---

# Chương 3. Decision Tree — Tree Construction Algorithm

### 3.1. Thuật toán

56. Mô tả thuật toán xây dựng Decision Tree.
57. Root node được lựa chọn như thế nào?
58. Tại mỗi node cần thực hiện những bước nào?
59. Làm thế nào tìm được best split?
60. Best feature được xác định như thế nào?
61. Best threshold được xác định như thế nào?
62. Khi nào tree tiếp tục split?
63. Khi nào tree dừng lại?
64. Vì sao Decision Tree sử dụng greedy algorithm?
65. Greedy split có đảm bảo tìm được global optimal tree không?
66. Tại sao tìm global optimal Decision Tree khó?
67. Complexity của việc xây dựng Decision Tree phụ thuộc vào những yếu tố nào?
68. Feature có nhiều giá trị liên tục được xử lý như thế nào?
69. Candidate thresholds được tạo ra như thế nào?
70. Nếu tất cả samples tại node thuộc cùng một class thì chuyện gì xảy ra?

### 3.2. Stopping Conditions

71. `max_depth` có tác dụng gì?
72. `min_samples_split` có tác dụng gì?
73. `min_samples_leaf` có tác dụng gì?
74. `max_leaf_nodes` có tác dụng gì?
75. Nếu không giới hạn depth thì điều gì có thể xảy ra?
76. Vì sao Decision Tree dễ overfit?
77. Underfitting xảy ra khi tree quá nông như thế nào?
78. Overfitting xảy ra khi tree quá sâu như thế nào?
79. Pre-pruning là gì?
80. Post-pruning là gì?
81. So sánh pre-pruning và post-pruning.
82. Cost-complexity pruning là gì?

---

# Chương 4. Decision Tree — Mathematics & Theory

83. Tại sao Decision Tree có thể mô hình hóa nonlinear function?
84. Decision Tree tạo decision boundary có dạng gì?
85. Tại sao boundary của Decision Tree thường axis-aligned?
86. Làm thế nào Decision Tree biểu diễn XOR?
87. Decision Tree có thể biểu diễn mọi decision boundary không?
88. Decision Tree có approximation capability như thế nào?
89. Vì sao Decision Tree có variance cao?
90. Bias và variance của Decision Tree thay đổi theo depth như thế nào?
91. Vì sao một tree sâu có low bias nhưng high variance?
92. Vì sao một tree nông có high bias nhưng low variance?
93. Decision Tree có differentiable không?
94. Tại sao Decision Tree khó tối ưu bằng gradient descent?
95. Split selection khác gradient-based optimization như thế nào?
96. Vì sao Decision Tree không cần backpropagation?
97. Decision Tree có thể được xem là một piecewise constant model như thế nào?
98. Decision Tree Regression biểu diễn hàm liên tục như thế nào?
99. Tại sao Decision Tree prediction không smooth?
100. Điều gì xảy ra với prediction khi threshold thay đổi rất nhỏ?

---

# Chương 5. Decision Tree — Classic Algorithms

### 5.1. ID3

101. ID3 là gì?
102. ID3 sử dụng splitting criterion nào?
103. ID3 xử lý categorical features như thế nào?
104. Hạn chế chính của ID3 là gì?
105. Vì sao Information Gain có bias đối với feature nhiều giá trị?

### 5.2. C4.5

106. C4.5 mở rộng ID3 như thế nào?
107. Gain Ratio là gì?
108. Vì sao C4.5 sử dụng Gain Ratio?
109. C4.5 xử lý continuous feature như thế nào?
110. C4.5 xử lý missing values như thế nào?

### 5.3. CART

111. CART là gì?
112. CART khác ID3 như thế nào?
113. CART sử dụng criterion nào cho classification?
114. CART sử dụng criterion nào cho regression?
115. Vì sao CART tạo binary tree?
116. Binary split có ưu điểm gì?
117. CART thực hiện pruning như thế nào?
118. So sánh ID3, C4.5 và CART.

---

# Chương 6. Decision Tree — Practical Issues

119. Decision Tree có nhạy với outlier không?
120. Vì sao Decision Tree thường ít nhạy với feature scaling?
121. Decision Tree có nhạy với dữ liệu nhiễu không?
122. Missing values ảnh hưởng thế nào?
123. Class imbalance ảnh hưởng thế nào đến tree?
124. Decision Tree có thể sử dụng class weights như thế nào?
125. Feature importance của Decision Tree được tính như thế nào?
126. Vì sao impurity-based feature importance có thể gây bias?
127. Permutation importance là gì?
128. Feature importance và causal importance có giống nhau không?
129. Decision Tree có thể tạo ra spurious split như thế nào?
130. Data leakage ảnh hưởng thế nào đến Decision Tree?

---

# Chương 7. Bagging — Mở rộng từ Decision Tree

## 7.1. Fundamentals

131. Bagging là gì?
132. Bagging viết đầy đủ là gì?
133. Tại sao Bagging được xây dựng từ nhiều model?
134. Bootstrap sampling là gì?
135. Vì sao bootstrap sample có thể chứa duplicate samples?
136. Out-of-Bag sample là gì?
137. Bagging giảm variance như thế nào?
138. Tại sao averaging nhiều model giúp giảm variance?
139. Bagging có làm giảm bias không?
140. Khi nào Bagging hiệu quả?

## 7.2. Random Forest

141. Random Forest là gì?
142. Random Forest khác Bagging Decision Trees như thế nào?
143. Tại sao Random Forest chọn random subset of features?
144. Feature subsampling giúp giảm correlation giữa các trees như thế nào?
145. Vì sao giảm correlation giữa trees giúp ensemble tốt hơn?
146. Random Forest prediction cho classification được thực hiện như thế nào?
147. Random Forest prediction cho regression được thực hiện như thế nào?
148. Random Forest sử dụng bootstrap như thế nào?
149. Random Forest có cần pruning từng tree không?
150. Vì sao Random Forest thường sử dụng nhiều deep trees?
151. Random Forest giải quyết variance của single tree như thế nào?
152. Random Forest có bias cao hơn single deep tree không?
153. Số lượng trees ảnh hưởng thế nào đến performance?
154. Khi nào thêm trees không còn cải thiện đáng kể?
155. `max_features` ảnh hưởng thế nào đến Random Forest?

---

# Chương 8. Random Forest — Advanced

156. Phân tích Random Forest dưới bias-variance decomposition.
157. Vì sao correlation giữa trees quan trọng?
158. Nếu các trees hoàn toàn giống nhau thì ensemble có lợi không?
159. Nếu các trees hoàn toàn độc lập thì variance thay đổi thế nào?
160. Bootstrap sampling tạo diversity như thế nào?
161. Feature randomness tạo diversity như thế nào?
162. Out-of-Bag evaluation hoạt động như thế nào?
163. OOB error có thể thay thế validation set không?
164. Random Forest có thể overfit khi số trees tăng không?
165. Random Forest có bias đối với categorical variables nhiều levels không?
166. Random Forest có phù hợp với high-dimensional data không?
167. Random Forest có phù hợp với sparse data không?
168. Random Forest có extrapolate tốt trong regression không?
169. Vì sao tree ensemble regression thường không extrapolate tốt?
170. Random Forest và Gradient Boosting khác nhau về cách xây dựng trees như thế nào?

---

# Chương 9. Boosting — Fundamental

171. Boosting là gì?
172. Boosting khác Bagging như thế nào?
173. Bagging train models độc lập hay tuần tự?
174. Boosting train models độc lập hay tuần tự?
175. Boosting tập trung vào samples khó như thế nào?
176. Weak learner là gì?
177. Tại sao decision stump thường được dùng làm weak learner?
178. Boosting biến weak learners thành strong learner như thế nào?
179. Boosting chủ yếu giảm bias hay variance?
180. Boosting có thể overfit không?
181. Learning rate trong boosting có vai trò gì?
182. Number of estimators ảnh hưởng thế nào?
183. Learning rate và number of trees có trade-off gì?

---

# Chương 10. AdaBoost

184. AdaBoost là gì?
185. AdaBoost hoạt động theo nguyên lý nào?
186. Sample weight trong AdaBoost là gì?
187. Vì sao samples bị phân loại sai được tăng weight?
188. Weak learner được chọn như thế nào?
189. Model weight được tính như thế nào?
190. AdaBoost kết hợp weak learners như thế nào?
191. Tại sao AdaBoost có thể giảm bias?
192. AdaBoost nhạy với noise như thế nào?
193. Vì sao outlier có thể gây vấn đề cho AdaBoost?
194. AdaBoost classification và regression khác nhau như thế nào?
195. AdaBoost khác Random Forest ở đâu?

---

# Chương 11. Gradient Boosting

196. Gradient Boosting là gì?
197. Ý tưởng cốt lõi của Gradient Boosting là gì?
198. Tại sao Gradient Boosting có chữ "Gradient"?
199. Gradient Boosting tối ưu objective function như thế nào?
200. Residual trong Gradient Boosting có ý nghĩa gì?
201. Vì sao tree tiếp theo học residual của ensemble hiện tại?
202. Viết công thức cập nhật của Gradient Boosting.

$$
F_m(x)
=
F_{m-1}(x)
+
\eta h_m(x)
$$

203. `η` có ý nghĩa gì?
204. Weak learner trong Gradient Boosting thường là gì?
205. Vì sao Gradient Boosting thường sử dụng shallow trees?
206. Gradient Boosting khác AdaBoost như thế nào?
207. Gradient Boosting có thể giải quyết regression không?
208. Gradient Boosting có thể sử dụng arbitrary differentiable loss không?
209. Negative gradient có vai trò gì?
210. Gradient Boosting có thể được hiểu như functional gradient descent như thế nào?

---

# Chương 12. XGBoost

![Image](https://images.openai.com/static-rsc-4/cGumbAHadJH1zbqIwJDLXPxbLoVAMohDbm6Ms8mXi8BeiV6WX6AgiDtjROe-aweXG5TntIt57ruzIc1RFafjgEZ0ZMkFCMy33khoyb0BRkJI6lTq3Mql-JMyCkZm_bYFAHskB-_lx3ZNphSbSIkEfTz4qE1URq3KpT_noKF9-VkIrKmhrpFjh3KwvE7VvcVn?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Tg3pobwS0SV8yonKRyOYMqVYiJeIQ27JLYN7qKYMsISOC0xn4oRBCQ-RcrBBXFUgVrSXjGFmrRaY-g7SH_J8Bxxf6uQYTyfC8b66X3Dum_YRL85uFEo8TuoVyX8GfgPxTGah8NeMcsDFGDuPSWHBBLgObqa1uWfHlcBE6ss_nuuHvzDJvo4bwb3CilA63fD9?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/u9uxpjF7HP1Hhm5pPe-3-yNFVD_ZHqsG4GRiuChOGgtVo9N96apYQA0q6yUsHZiQA8_GfQkU5G-yGtqjDZeiHe8a-UfvbXr-C7j5CbTGXN4Iueid0HtbBqYTPCwTd6ezGjsU8os_K0dB9XInSjt58eU0MbGZsV_saiLBF1HddKD5Bj72eIUg146TRjclZMP2?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/hEVbyYkeQkbTbg6m4FJUH6c6Pa1OWipncADpnbtdc6M1V2NKJgkAgRPa4cuAwzyr19RBRWnzsjhyvIDkUm_j2YPwR_CvpFdsvAI6yiTLZFtDUJLtn2Oa91-SCJogNlO9OyOdNFcdrqw1Vn4Jr1IblZPmAkA34s4w5GUNPF384jziWtZPfye361E8eoQ1Euov?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/2fPhjUNJf1-G2hN12lJv3lKeLvLfPd7d7TjYlLMp3FRAKqvRUcQaidEWyOa104e7Ng1Le5lKA66JpWDCArXZOsJ1bFxMmzzHohixctNXMqFVOpi72F6Gyurv1izho71Rl_WH6T3U8CQQeJKdJekUSvLBbOFwDGcQZSuXoLSVHJ-4nf9WqvNUNeirWVgi4RGM?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/SYRWjXvgPcHezB_1FtdG0IylplsbjE1pUTu6LfOyPwf79lSG-R3uU9R5zPrYwV9uvcTQ-8DsJbL6JvuDEsGtPOIAuPAegBaysXZ10xIYLM9FHGb_INAwgj403UlFTtp7jYwxjdPx2ERS7StG_f4KGfuiYIl1FE6RXeCcAqNKsTa4ndRYIQoVo2_vHAL9I0Yt?purpose=fullsize)

211. XGBoost là gì?
212. XGBoost mở rộng Gradient Boosting như thế nào?
213. Objective function của XGBoost gồm những thành phần nào?
214. Regularization term trong XGBoost có vai trò gì?
215. XGBoost sử dụng first-order gradient như thế nào?
216. XGBoost sử dụng second-order gradient như thế nào?
217. Hessian có vai trò gì trong XGBoost?
218. Vì sao XGBoost được gọi là second-order boosting?
219. XGBoost tìm split bằng cách nào?
220. Gain của một split được tính như thế nào?
221. Vì sao regularization ảnh hưởng đến split?
222. `max_depth` ảnh hưởng thế nào?
223. `min_child_weight` là gì?
224. `subsample` có tác dụng gì?
225. `colsample_bytree` có tác dụng gì?
226. `learning_rate` có vai trò gì?
227. `n_estimators` có vai trò gì?
228. `gamma` ảnh hưởng đến split như thế nào?
229. `reg_alpha` và `reg_lambda` khác nhau thế nào?
230. XGBoost xử lý missing values như thế nào?
231. XGBoost có thể overfit không?
232. Early stopping trong XGBoost hoạt động như thế nào?
233. Vì sao XGBoost thường rất mạnh trên tabular data?

---

# Chương 13. LightGBM

234. LightGBM là gì?
235. LightGBM khác XGBoost ở đâu?
236. Histogram-based learning là gì?
237. Vì sao histogram giúp tăng tốc Gradient Boosting?
238. Leaf-wise tree growth là gì?
239. Leaf-wise khác level-wise như thế nào?
240. Vì sao leaf-wise có thể đạt loss thấp nhanh hơn?
241. Vì sao leaf-wise dễ overfit?
242. `num_leaves` có ý nghĩa gì?
243. `max_depth` có vai trò gì trong LightGBM?
244. GOSS là gì?
245. EFB là gì?
246. LightGBM có lợi thế gì trên large-scale tabular data?
247. Khi nào LightGBM có thể không phù hợp?

---

# Chương 14. CatBoost

248. CatBoost là gì?
249. CatBoost được thiết kế để giải quyết vấn đề gì?
250. Vì sao categorical features khó xử lý trong boosting?
251. CatBoost xử lý categorical features như thế nào?
252. Target encoding là gì?
253. Vì sao target encoding có nguy cơ leakage?
254. CatBoost giải quyết target leakage trong categorical encoding như thế nào?
255. Ordered boosting là gì?
256. CatBoost khác XGBoost và LightGBM như thế nào?
257. Khi nào CatBoost đặc biệt hữu ích?

---

# Chương 15. So sánh toàn bộ họ Tree Models

258. Decision Tree vs Random Forest?
259. Decision Tree vs Gradient Boosting?
260. Random Forest vs Gradient Boosting?
261. Bagging vs Boosting?
262. AdaBoost vs Gradient Boosting?
263. Gradient Boosting vs XGBoost?
264. XGBoost vs LightGBM?
265. XGBoost vs CatBoost?
266. Random Forest vs XGBoost trên tabular data?
267. Single Tree vs Ensemble?
268. Deep Tree vs Shallow Tree?
269. Bagging giảm variance như thế nào?
270. Boosting giảm bias như thế nào?
271. Random Forest và XGBoost khác nhau về training dependency như thế nào?
272. Random Forest có thể parallelize dễ hơn Boosting không?
273. Vì sao Boosting khó parallelize theo thứ tự trees?
274. Vì sao Random Forest thường robust hơn với noise?
275. Vì sao Boosting có thể đạt accuracy cao hơn nhưng nhạy tuning hơn?

---

# Chương 16. Tree Models — Hyperparameter Reasoning

276. Khi nào tăng `max_depth`?
277. Khi nào giảm `max_depth`?
278. `n_estimators` ảnh hưởng thế nào đến Random Forest?
279. `max_features` ảnh hưởng thế nào?
280. `min_samples_leaf` ảnh hưởng thế nào?
281. `learning_rate` ảnh hưởng thế nào đến Gradient Boosting?
282. `n_estimators` và `learning_rate` có quan hệ gì?
283. `subsample` có tác dụng gì?
284. Tại sao tăng model complexity có thể làm validation error tăng?
285. Làm thế nào phát hiện tree ensemble đang overfit?
286. Làm thế nào phát hiện ensemble đang underfit?
287. Có nên tune tất cả hyperparameters cùng lúc không?
288. Làm thế nào thiết kế hyperparameter search cho XGBoost?
289. Vì sao early stopping quan trọng trong boosting?
290. Cross-validation được sử dụng thế nào để chọn hyperparameters?

---

# Chương 17. Tree Models — Complexity & Engineering

291. Complexity của Decision Tree training là gì?
292. Complexity của prediction bằng Decision Tree là gì?
293. Random Forest training có thể parallelize ở đâu?
294. Random Forest inference complexity phụ thuộc vào gì?
295. Gradient Boosting training complexity phụ thuộc vào gì?
296. Vì sao số lượng trees ảnh hưởng inference latency?
297. Depth của tree ảnh hưởng latency như thế nào?
298. Number of leaves ảnh hưởng model complexity như thế nào?
299. Memory footprint của Random Forest phụ thuộc vào gì?
300. Vì sao XGBoost/LightGBM có thể nhanh hơn một implementation Decision Tree naïve?
301. Histogram algorithm giảm computation như thế nào?
302. Parallelism trong tree-based models hoạt động ở những mức nào?
303. CPU có lợi thế gì khi training tree-based models?
304. GPU có lợi thế gì với Gradient Boosting?
305. Model size ảnh hưởng deployment như thế nào?

---

# Chương 18. Interpretability & Explainability

306. Vì sao Decision Tree được xem là interpretable?
307. Tree depth ảnh hưởng interpretability như thế nào?
308. Feature importance là gì?
309. Impurity-based importance được tính như thế nào?
310. Permutation importance hoạt động như thế nào?
311. SHAP là gì?
312. SHAP giải thích tree-based model như thế nào?
313. TreeSHAP có ưu điểm gì?
314. Feature importance có thể gây hiểu nhầm như thế nào?
315. Correlated features ảnh hưởng feature importance thế nào?
316. Feature importance có chứng minh causal relationship không?
317. Decision Tree có thực sự dễ giải thích khi tree rất sâu không?

---

# Chương 19. Tree Models — Failure Analysis

318. Vì sao single Decision Tree dễ overfit?
319. Vì sao Random Forest có thể fail?
320. Vì sao Gradient Boosting có thể overfit?
321. Noise ảnh hưởng AdaBoost thế nào?
322. Outlier ảnh hưởng Boosting thế nào?
323. Class imbalance ảnh hưởng tree ensemble thế nào?
324. High-cardinality categorical feature gây vấn đề gì?
325. Target leakage ảnh hưởng CatBoost/XGBoost như thế nào?
326. Data drift ảnh hưởng tree models thế nào?
327. Concept drift ảnh hưởng tree models thế nào?
328. Tree models có extrapolate tốt không?
329. Vì sao tree-based regression thường không tốt với extrapolation?
330. Khi nào linear model tốt hơn tree model?
331. Khi nào neural network tốt hơn tree model?
332. Khi nào Random Forest tốt hơn XGBoost?
333. Khi nào XGBoost tốt hơn Random Forest?

---

# Chương 20. Research-Level Questions

334. Tại sao Decision Tree sử dụng greedy optimization?
335. Bài toán tìm optimal Decision Tree có khó về mặt computational complexity không?
336. Tại sao tree pruning là một bài toán model selection?
337. Bias-variance decomposition giải thích single tree như thế nào?
338. Bias-variance decomposition giải thích Random Forest như thế nào?
339. Boosting có thể được giải thích dưới góc nhìn functional optimization như thế nào?
340. Gradient Boosting liên hệ với gradient descent như thế nào?
341. XGBoost liên hệ với Newton's method như thế nào?
342. Vì sao Hessian có thể cải thiện tree boosting?
343. Regularization trong XGBoost khác regularization trong neural network như thế nào?
344. Tại sao tree ensemble rất mạnh trên tabular data?
345. Vì sao neural network không phải lúc nào cũng vượt tree ensemble trên tabular data?
346. Tree models biểu diễn feature interaction như thế nào?
347. Vì sao tree models tự động học interaction giữa features?
348. Có thể xem tree ensemble như một adaptive basis function không?
349. Random Forest và Gradient Boosting khác nhau thế nào về error decomposition?
350. Tại sao boosting có thể biến weak learners thành strong learner?
351. Tại sao boosting có thể tiếp tục cải thiện sau khi training error đã rất thấp?
352. Vì sao regularization quan trọng hơn khi tree complexity tăng?
353. Có thể kết hợp tree models với neural networks như thế nào?
354. Tree-based representation có thể được sử dụng làm input cho neural network không?
355. Neural network có thể học cấu trúc decision tree không?

---

# Chương 21. Interview — Algorithm Reasoning

Đây là nhóm nên dùng để **tự trả lời bằng miệng trong phỏng vấn**.

### Decision Tree

356. Hãy giải thích Decision Tree trong 2 phút.
357. Tại sao Decision Tree không cần normalization?
358. Entropy và Gini khác nhau thế nào?
359. Information Gain hoạt động thế nào?
360. Tại sao Decision Tree dễ overfit?
361. Làm thế nào chống overfitting?
362. Pre-pruning và post-pruning khác nhau thế nào?
363. Decision Tree classification và regression khác nhau thế nào?

### Random Forest

364. Random Forest hoạt động như thế nào?
365. Tại sao phải randomize cả samples và features?
366. Tại sao nhiều trees tốt hơn một tree?
367. Tại sao Random Forest ít overfit hơn single tree?
368. OOB error là gì?
369. Random Forest có thể parallelize không?

### Boosting

370. Bagging và Boosting khác nhau thế nào?
371. Gradient Boosting hoạt động thế nào?
372. Residual có vai trò gì?
373. Learning rate và number of trees trade-off thế nào?
374. Vì sao boosting dễ overfit?
375. Vì sao weak learner thường là shallow tree?

### XGBoost

376. XGBoost khác Gradient Boosting như thế nào?
377. Tại sao XGBoost sử dụng gradient và Hessian?
378. Regularization của XGBoost hoạt động thế nào?
379. Early stopping hoạt động thế nào?
380. Tại sao XGBoost mạnh trên tabular data?

---

# Chương 22. Case Study — Chọn thuật toán

381. Dataset nhỏ với feature tabular → chọn model nào?
382. Dataset lớn với nhiều categorical features → chọn model nào?
383. Dataset có nhiều missing values → chọn model nào?
384. Dataset có nonlinear interaction mạnh → chọn model nào?
385. Dataset có nhiều noise → chọn model nào?
386. Dataset có class imbalance → chọn model nào?
387. Dataset cần interpretability cao → chọn model nào?
388. Dataset cần inference nhanh → chọn model nào?
389. Dataset cần accuracy cao nhất → nên bắt đầu từ model nào?
390. Dataset có vài nghìn samples và hàng trăm features → lựa chọn thế nào?
391. Dataset có hàng triệu samples → lựa chọn thế nào?
392. Khi nào dùng Logistic Regression thay vì Decision Tree?
393. Khi nào dùng Random Forest thay vì XGBoost?
394. Khi nào dùng LightGBM thay vì XGBoost?
395. Khi nào dùng CatBoost thay vì hai model trên?
