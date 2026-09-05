# Chương 1. CNN — Fundamentals

## 1.1. Basic

1. CNN là gì?
2. Tại sao CNN phù hợp với dữ liệu ảnh?
3. Ảnh có thể được biểu diễn dưới dạng tensor như thế nào?
4. Ba chiều cơ bản của một ảnh RGB là gì?
5. Convolution layer là gì?
6. Kernel/filter là gì?
7. Feature map là gì?
8. Một convolution operation hoạt động như thế nào?
9. Vì sao CNN không kết nối toàn bộ pixel với một neuron như Fully Connected Network?
10. Local connectivity là gì?
11. Weight sharing là gì?
12. Vì sao weight sharing giúp giảm số lượng tham số?
13. Receptive field là gì?
14. Vì sao receptive field quan trọng trong CNN?
15. Stride là gì?
16. Padding là gì?
17. Valid convolution là gì?
18. Same convolution là gì?
19. Zero padding có tác dụng gì?
20. Pooling layer là gì?
21. Max pooling và average pooling khác nhau thế nào?
22. Tại sao pooling được sử dụng trong CNN?
23. Activation function đóng vai trò gì trong CNN?
24. Tại sao CNN thường sử dụng ReLU?
25. Một CNN cơ bản gồm những thành phần nào?
26. Convolution → activation → pooling có ý nghĩa gì?
27. CNN học feature như thế nào?
28. Tại sao các layer đầu CNN thường học edge?
29. Các layer sâu hơn học object representation như thế nào?
30. CNN có thực sự hiểu object hay chỉ học statistical patterns?

## 1.2. Intermediate

31. Convolution trong deep learning có thực sự giống convolution toán học không?
32. Cross-correlation khác convolution như thế nào?
33. Output size của convolution được tính như thế nào?
34. Padding ảnh hưởng đến spatial resolution như thế nào?
35. Stride ảnh hưởng đến spatial resolution như thế nào?
36. Kernel size ảnh hưởng đến receptive field như thế nào?
37. Tại sao kernel 3×3 phổ biến?
38. Hai convolution 3×3 có thể thay thế một convolution 5×5 như thế nào?
39. Vì sao stacking nhiều convolution nhỏ có lợi?
40. Parameter count của convolution layer được tính như thế nào?
41. FLOPs của convolution layer phụ thuộc vào những yếu tố nào?
42. Vì sao convolution có inductive bias mạnh?
43. Translation equivariance là gì?
44. CNN có translation invariance hay equivariance?
45. Pooling tạo ra tính bất biến với translation như thế nào?
46. Tại sao CNN có khả năng khai thác spatial locality?
47. Tại sao CNN có hierarchical representation?
48. Vì sao CNN cần nhiều layer để nhận diện object phức tạp?
49. Receptive field lý thuyết và receptive field thực tế khác nhau thế nào?
50. Effective receptive field là gì?

## 1.3. Advanced

51. Phân tích inductive bias của CNN dưới góc nhìn toán học.
52. Tại sao locality là một giả định phù hợp với ảnh tự nhiên?
53. Weight sharing tạo ra prior gì cho quá trình học?
54. Translation equivariance được biểu diễn như thế nào bằng toán học?
55. Khi nào translation equivariance trở thành hạn chế?
56. Pooling có làm mất thông tin không?
57. Downsampling ảnh hưởng đến high-frequency information như thế nào?
58. Vì sao CNN khó mô hình hóa global dependency?
59. Có thể mở rộng receptive field mà không tăng quá nhiều computational cost bằng cách nào?
60. Dilated convolution giải quyết vấn đề gì?
61. Depthwise convolution khác standard convolution như thế nào?
62. Pointwise convolution có vai trò gì?
63. Depthwise separable convolution giảm computation như thế nào?
64. Group convolution là gì?
65. Bottleneck convolution có mục đích gì?
66. Residual connection giải quyết vấn đề nào trong CNN?
67. Skip connection ảnh hưởng đến gradient flow như thế nào?
68. Tại sao mạng CNN rất sâu có thể khó tối ưu nếu không có residual connection?
69. CNN có thể được xem là một hierarchical feature extractor như thế nào?
70. Những giả định nào của CNN không còn tối ưu khi dataset trở nên rất lớn?

---

# Chương 2. CNN — Mathematics & Computation

## 2.1. Convolution

71. Viết công thức convolution 2D.
72. Viết công thức output của convolution layer.
73. Tính kích thước output với kernel, stride và padding cho trước.
74. Tính số lượng parameter của một convolution layer.
75. Tính FLOPs của convolution layer.
76. Tại sao bias có số lượng parameter bằng số output channels?
77. Với input có `C_in` channels và output có `C_out` channels, kernel thực sự có shape gì?
78. Tại sao convolution kernel không chỉ có kích thước `K×K` mà còn có chiều channel?
79. Một filter tạo ra bao nhiêu feature map?
80. Một convolution layer tạo ra bao nhiêu output channels?

## 2.2. Backpropagation

81. Gradient đi qua convolution như thế nào?
82. CNN cập nhật kernel bằng backpropagation như thế nào?
83. Gradient của kernel phụ thuộc vào input như thế nào?
84. Gradient của input phụ thuộc vào kernel như thế nào?
85. Pooling layer truyền gradient như thế nào?
86. Max pooling backward hoạt động thế nào?
87. Tại sao ReLU có thể gây dead neurons?
88. Vanishing gradient xuất hiện trong CNN như thế nào?
89. Residual connection giúp gradient propagation như thế nào?

## 2.3. Architecture reasoning

90. Nếu tăng kernel size thì điều gì xảy ra?
91. Nếu tăng số channels thì điều gì xảy ra?
92. Nếu tăng depth nhưng giữ width thì điều gì xảy ra?
93. Nếu tăng width nhưng giữ depth thì điều gì xảy ra?
94. Depth và width ảnh hưởng thế nào đến representation capacity?
95. Spatial resolution và channel dimension có trade-off gì?
96. Tại sao CNN thường giảm spatial resolution nhưng tăng channel dimension?
97. Feature hierarchy có thể được giải thích bằng sự thay đổi spatial/channel dimensions như thế nào?
98. Tại sao layer đầu cần spatial resolution cao?
99. Tại sao layer sâu có thể sử dụng spatial resolution thấp hơn?
100. Làm thế nào để thiết kế CNN cân bằng giữa accuracy và computational cost?

---

# Chương 3. CNN — Classic Architectures

![Image](https://images.openai.com/static-rsc-4/qNJN5QxIiVN-FgiUI3hTicWdekiKp8P4lNoGyewO5MC30PEJaGFkuV_gDI1ohSol7RfaRxCR5hc3S9p8jQCWoowJh9x1NEjjZopcrRoucl0MS_aD6LoL-fJ1R3Jk4rByR9Z1awZOaZDxMlpsbNBNbCQt8J4AxZPn9ABE3Hnm_MROQIC4LrR_Jg8Q93bPKrKr?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/vZCafpA_H99GLrQEnPwRq1QOFAeIfEWDKOUMmU12l0foJzeZ0d_krkKD0TqCvuY0xd5Cf4dbN6bl_xvRKVhQpyOE5vGAms5A8o5Y9uPE1aoRXOGdosA0oVECAjDA1yR6RTsmCt7yKZKxI0S7kLy707M_--MSMlhHLwt6A52KcaOhgvWdU_kUPyYDd2m8sJs1?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/n4xoJano9bHeVYqVN-nBOTsQpo_s5uNMW70pFK9JkK0BdHC_cR2ZA0XDx0DsOF23SVfX4usNJ_F5EyOhhZ-8W7N-V3NJ06FCvQS-LgxHz-TwNGV5vlc_qByJHcm7njacPYFotwW0-GBUX2Byi82g_25eQbZ5k1Uwvur8iKtgYQeuerGfHSN1P7Aytgbwzgpl?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/qCCAVoNg6rFJbHzcVm9vjJI1rMqTcxVwiHzviEwb8vvjMIqKFBJviBb7d17bmE8zC0y3L5dpG8LrR8t1uSM2cIUIIgfN7Tbdr15CY5jZY10Sw4HiBiIS_WrPYH4CJyAsrpDHjAC_0rX4r1dh7G_8HgrNlIvjfwRNhJzEPme6kroczzr40mr8UMaGkplxq8Jt?purpose=fullsize)

## 3.1. LeNet

101. LeNet là gì?
102. LeNet giải quyết bài toán nào?
103. Cấu trúc cơ bản của LeNet gồm những thành phần nào?
104. LeNet sử dụng convolution và pooling như thế nào?
105. Ý nghĩa lịch sử của LeNet đối với CNN là gì?

## 3.2. AlexNet

106. AlexNet khác LeNet ở những điểm nào?
107. Vì sao AlexNet có ảnh hưởng lớn đến deep learning hiện đại?
108. AlexNet sử dụng ReLU vì lý do gì?
109. Vai trò của dropout trong AlexNet là gì?
110. AlexNet sử dụng GPU như thế nào?
111. AlexNet giải quyết vấn đề training CNN quy mô lớn như thế nào?

## 3.3. VGG

112. Ý tưởng chính của VGG là gì?
113. Vì sao VGG sử dụng nhiều convolution 3×3?
114. Hai convolution 3×3 tương đương receptive field với kernel nào?
115. VGG đánh đổi điều gì khi sử dụng kiến trúc rất sâu?
116. Tại sao VGG có nhiều parameter?
117. Vì sao VGG thường được dùng làm backbone dù computational cost cao?

## 3.4. GoogLeNet / Inception

118. Ý tưởng chính của Inception là gì?
119. Vì sao Inception sử dụng nhiều kernel size trong cùng một block?
120. Inception block xử lý multi-scale feature như thế nào?
121. Vai trò của 1×1 convolution trong Inception là gì?
122. Vì sao 1×1 convolution giúp giảm computation?
123. Inception giải quyết vấn đề computational cost như thế nào?
124. So sánh VGG và Inception về depth, width và computation.

## 3.5. ResNet

125. ResNet giải quyết vấn đề nào?
126. Residual block là gì?
127. Vì sao học residual function dễ hơn học direct mapping?
128. Viết công thức residual block.
129. Skip connection ảnh hưởng đến gradient như thế nào?
130. Identity mapping có ý nghĩa gì?
131. Tại sao ResNet có thể rất sâu?
132. ResNet-18, ResNet-34, ResNet-50 khác nhau như thế nào?
133. Bottleneck block là gì?
134. Tại sao ResNet-50 sử dụng bottleneck?
135. ResNet có phải chỉ đơn giản là CNN sâu hơn không?

## 3.6. DenseNet

136. DenseNet khác ResNet như thế nào?
137. Dense connection là gì?
138. DenseNet tái sử dụng feature như thế nào?
139. Vì sao DenseNet có parameter efficiency tốt?
140. DenseNet và ResNet khác nhau về flow của feature như thế nào?

---

# Chương 4. CNN — Modern Extensions

## 4.1. Efficient CNN

141. MobileNet giải quyết vấn đề gì?
142. Depthwise separable convolution hoạt động như thế nào?
143. MobileNet khác ResNet về computational design như thế nào?
144. EfficientNet sử dụng nguyên lý nào để scale CNN?
145. Compound scaling là gì?
146. EfficientNet scale depth, width và resolution như thế nào?
147. Vì sao tăng cả depth, width và resolution có thể hiệu quả hơn chỉ tăng một chiều?

## 4.2. Dense / Residual / Multi-scale

148. DenseNet và ResNet khác nhau về connectivity như thế nào?
149. Feature reuse có lợi ích gì?
150. Multi-scale feature representation là gì?
151. Feature Pyramid Network (FPN) giải quyết vấn đề gì?
152. Vì sao object detection cần multi-scale representation?
153. Top-down pathway của FPN hoạt động như thế nào?
154. Skip connection trong FPN khác residual connection như thế nào?

## 4.3. Attention-based CNN

155. Attention trong CNN là gì?
156. Channel attention là gì?
157. Spatial attention là gì?
158. SE block hoạt động như thế nào?
159. CBAM mở rộng SE như thế nào?
160. Attention có thay thế convolution hoàn toàn không?
161. CNN + attention tạo ra inductive bias như thế nào?
162. Tại sao attention có thể giúp CNN tập trung vào feature quan trọng?

## 4.4. Modern convolution

163. Dilated convolution là gì?
164. Deformable convolution là gì?
165. Deformable convolution thay đổi inductive bias của CNN như thế nào?
166. Group convolution là gì?
167. Depthwise convolution có hạn chế gì?
168. Pointwise convolution có vai trò gì?
169. ConvNeXt là gì?
170. ConvNeXt học được gì từ Transformer?
171. ConvNeXt thay đổi CNN truyền thống ở những điểm nào?
172. Tại sao ConvNeXt được xem là modernized CNN?

---

# Chương 5. Vision Transformer — Fundamentals

![Image](https://images.openai.com/static-rsc-4/GXvNiqlF1B0i16uLmepGGdUCqMKd2lQBDTsgAaxQ068N47R07a6hvHJ9Hua3cgNISm2hpwQjbDT01nQb3bXYM6XtAJ7fEOkbtCbym_6e3xufpbMQIKMYpNLOKyvOC1L_axhbYZMfd0WQeiJ3wawIVpJQLZyILC9X2fwLckpPX-aECv-p0NYCnHOFtBXqQxjA?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/swBvyRpR7J63cYMh2X_ZqKGO2sDlr61reHLBwpj_HB-fhvklapnpnXtHelizGlHy050Je9JPcDWIgUXh_jVaIZ5Fgt7VdJPh9FyrmOBhhPVAUZYXyMmJD-0ITmiDON2LSYo4QtMBRrQHirruJCU5TPfodETv3ZAS1Z4Dw1dfWEa42PRZdOkF890ryP1UWm6_?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/4EctOGAkibJHDa8K2z0sxptw49pxTebsUtLQPtd4yyighAlhwOrt7hqr1UcJkIVFqMXVgRBlFAbQ9m8LMWa60E6JnCppBxvaMPgQSdziRnewE4gvRPy5V9sRcLGMP7Xt8TC5IOpvYX1HyDqpPlC_h_xurYntKfFydBs3YQNTaHtM1NdQFJN7O2kgWx1xwJLu?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/AAW8A_ovP3krOaL0CdCkbn2K5cz8cTBELrVRAxxwdSyb0s4u0C7w4D9LFIHdZdpgNC1QcSe9zXtjj15CFqGTCxPcHezdy2z31u3pmvlA-xpIHpLC883YF89Yx8ElGJdCOFUMPAn1QGDmPx3M4r5nwkV4WJXpmy820ni2nIdEBZ-qpVXb-okME5Kx0ZBTdRm8?purpose=fullsize)

## 5.1. Basic

173. Vision Transformer (ViT) là gì?
174. Ý tưởng cốt lõi của ViT là gì?
175. Tại sao Transformer có thể được áp dụng cho ảnh?
176. ViT biến ảnh thành sequence như thế nào?
177. Patch là gì?
178. Patch embedding là gì?
179. Tại sao ảnh được chia thành các patch?
180. Patch size ảnh hưởng đến model như thế nào?
181. Image patch có thể được xem như token như thế nào?
182. ViT sử dụng positional information như thế nào?
183. CLS token là gì?
184. Tại sao ViT cần positional embedding?
185. Transformer Encoder trong ViT gồm những thành phần nào?
186. Multi-Head Self-Attention là gì?
187. LayerNorm trong ViT có vai trò gì?
188. MLP block trong ViT có vai trò gì?
189. Residual connection trong ViT có vai trò gì?
190. Một ViT block gồm những thành phần nào?

## 5.2. Intermediate

191. Viết pipeline từ ảnh đến classification output của ViT.
192. Nếu ảnh có kích thước `H×W`, patch size `P`, số token là bao nhiêu?
193. Patch embedding được thực hiện bằng phép toán nào?
194. Tại sao patch embedding có thể được implement bằng Conv2d?
195. Sequence length của ViT phụ thuộc vào yếu tố nào?
196. Sequence length ảnh hưởng computational cost như thế nào?
197. Vì sao giảm patch size làm ViT đắt hơn?
198. Positional embedding có thể là learned hay fixed?
199. Self-attention hoạt động trên các image patches như thế nào?
200. Attention giữa hai patch có ý nghĩa gì?
201. ViT có local inductive bias giống CNN không?
202. ViT học spatial relationship như thế nào?
203. Vì sao ViT có global receptive field ngay từ layer đầu?
204. CNN và ViT khác nhau như thế nào về receptive field?
205. MLP block trong Transformer có tác dụng gì ngoài attention?

## 5.3. Advanced

206. Viết công thức Self-Attention.
207. Q, K, V trong ViT đại diện cho điều gì?
208. Vì sao attention được scale bởi `sqrt(d_k)`?
209. Multi-head attention có lợi ích gì?
210. Tại sao nhiều head có thể học các loại relationship khác nhau?
211. Complexity của self-attention theo sequence length là gì?
212. Nếu giảm patch size từ 16 xuống 8 thì sequence length thay đổi thế nào?
213. Vì sao ViT có computational bottleneck ở self-attention?
214. Vì sao ViT ít inductive bias hơn CNN?
215. "Data-driven learning" của ViT có nghĩa gì?
216. Tại sao ViT thường cần nhiều dữ liệu hơn CNN trong một số thiết lập?
217. Global dependency được hình thành trong ViT như thế nào?
218. ViT có translation equivariance tự nhiên như CNN không?
219. Điều gì xảy ra nếu bỏ positional embedding khỏi ViT?
220. Patchification làm mất thông tin gì?
221. Patch size có thể được xem là một hyperparameter kiến trúc như thế nào?

---

# Chương 6. ViT — Mathematics & Computation

## 6.1. Patch Embedding

222. Cho ảnh `224×224×3`, patch `16×16`, có bao nhiêu patch?
223. Nếu patch size giảm một nửa thì số token thay đổi bao nhiêu lần?
224. Patch embedding biến tensor ảnh thành tensor sequence như thế nào?
225. Tính số parameter của patch projection.
226. Vì sao patch embedding có thể xem như linear projection?
227. Patch embedding bằng Conv2d có ý nghĩa toán học gì?

## 6.2. Self-Attention

228. Viết đầy đủ công thức:

$$
Attention(Q,K,V)
=
softmax\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

229. Tại sao `QKᵀ` tạo ra attention score?
230. Vì sao softmax được áp dụng trên attention score?
231. Tại sao attention matrix có kích thước `N×N`?
232. `N` đại diện cho gì trong ViT?
233. Vì sao self-attention có complexity `O(N²)`?
234. `N` phụ thuộc vào patch size như thế nào?
235. Tại sao độ phân giải ảnh cao gây khó khăn cho ViT?
236. Multi-head attention thay đổi representation như thế nào?
237. Tại sao concatenate các head lại với nhau?
238. Projection cuối cùng của MHA có vai trò gì?

## 6.3. Transformer Block

239. Pre-Norm và Post-Norm khác nhau như thế nào?
240. Vì sao LayerNorm thường được sử dụng trong Transformer?
241. MLP block có cấu trúc như thế nào?
242. Vì sao MLP thường expand hidden dimension?
243. Residual connection trong Transformer có tác dụng gì?
244. Tại sao ViT không cần convolution để xây dựng representation?
245. ViT có thể học local feature không?
246. Self-attention có thể học global và local relationship đồng thời không?

---

# Chương 7. ViT — Famous Architectures & Extensions

## 7.1. Original ViT

247. Kiến trúc ViT nguyên bản gồm những thành phần nào?
248. ViT khác Transformer dùng cho NLP ở đâu?
249. Tại sao ViT có thể sử dụng kiến trúc Transformer Encoder?
250. Tại sao không cần Transformer Decoder cho image classification?

## 7.2. DeiT

251. DeiT giải quyết hạn chế nào của ViT?
252. Vì sao DeiT quan tâm đến data efficiency?
253. Knowledge distillation được sử dụng trong DeiT như thế nào?
254. Distillation token là gì?
255. DeiT khác ViT nguyên bản ở đâu?

## 7.3. Swin Transformer

256. Swin Transformer giải quyết vấn đề gì của ViT?
257. Window-based self-attention là gì?
258. Vì sao Swin sử dụng local windows?
259. Shifted window là gì?
260. Tại sao cần shift window?
261. Swin xây dựng hierarchical representation như CNN như thế nào?
262. Swin có complexity tốt hơn ViT ở độ phân giải cao như thế nào?
263. So sánh receptive field của ViT và Swin.

## 7.4. Hybrid Architectures

264. CNN + Transformer hybrid architecture là gì?
265. Tại sao kết hợp CNN và Transformer?
266. CNN có thể được sử dụng ở front-end của ViT như thế nào?
267. Transformer có thể được sử dụng sau CNN backbone như thế nào?
268. Hybrid architecture có thể tận dụng inductive bias của CNN và global modeling của Transformer như thế nào?

## 7.5. Hierarchical Vision Transformers

269. Tại sao hierarchical representation quan trọng trong computer vision?
270. Vì sao ViT nguyên bản không có hierarchy rõ ràng như CNN?
271. Hierarchical ViT giải quyết vấn đề này như thế nào?
272. Vì sao object detection thường thích backbone có multi-scale features?
273. So sánh hierarchical CNN và hierarchical Transformer.

## 7.6. Modern ViT Design

274. Vì sao một số ViT hiện đại thay đổi positional encoding?
275. Relative positional encoding là gì?
276. Vì sao relative position có thể phù hợp hơn absolute position?
277. Rotary positional encoding có thể được áp dụng cho vision như thế nào?
278. Vì sao một số kiến trúc giảm hoặc loại bỏ CLS token?
279. Global average pooling có thể thay thế CLS token như thế nào?
280. ViT hiện đại đã học gì từ thiết kế CNN?

---

# Chương 8. CNN vs ViT — Basic Comparison

## 8.1. Khái niệm

281. CNN và ViT khác nhau ở ý tưởng cốt lõi nào?
282. CNN xử lý ảnh theo local như thế nào?
283. ViT xử lý ảnh theo global như thế nào?
284. CNN sử dụng convolution, ViT sử dụng self-attention — sự khác biệt bản chất là gì?
285. CNN có inductive bias gì?
286. ViT có inductive bias gì?
287. CNN và ViT khác nhau thế nào về spatial locality?
288. CNN và ViT khác nhau thế nào về global dependency?
289. CNN và ViT khác nhau thế nào về parameter sharing?
290. CNN và ViT khác nhau thế nào về receptive field?

## 8.2. Representation

291. CNN học feature hierarchy như thế nào?
292. ViT học feature representation như thế nào?
293. CNN có tập trung vào object hơn ViT không?
294. ViT có thực sự tập trung background nhiều hơn CNN không?
295. Attention map của ViT có thể được xem là explanation của model không?
296. Feature map CNN và token representation của ViT khác nhau thế nào?
297. Channel dimension trong CNN tương ứng với khái niệm nào trong ViT?
298. Spatial dimension trong CNN tương ứng với sequence dimension trong ViT như thế nào?

---

# Chương 9. CNN vs ViT — Architecture & Representation

## 9.1. Local vs Global

299. Vì sao CNN có local receptive field?
300. Vì sao ViT có global interaction ngay từ đầu?
301. Tại sao local inductive bias có lợi với ảnh?
302. Khi nào global interaction có lợi hơn local processing?
303. CNN cần bao nhiêu layer để một neuron có thể nhìn toàn ảnh?
304. ViT cần bao nhiêu attention layer để patch tương tác với toàn bộ patch khác?
305. Global attention có luôn tốt hơn local convolution không?
306. Locality có phải là hạn chế của CNN không?
307. Global attention có phải luôn là ưu điểm của ViT không?

## 9.2. Inductive Bias

308. CNN có những inductive bias nào?
309. ViT có những inductive bias nào?
310. Vì sao CNN thường data-efficient hơn trong regime dữ liệu nhỏ?
311. Vì sao ViT có thể hưởng lợi mạnh từ large-scale pretraining?
312. Khi dữ liệu tăng rất lớn, sự khác biệt inductive bias thay đổi thế nào?
313. Có thể giảm inductive bias của CNN bằng cách nào?
314. Có thể đưa inductive bias kiểu CNN vào ViT bằng cách nào?

---

# Chương 10. CNN vs ViT — Training & Optimization

315. CNN và ViT khác nhau thế nào về độ khó training?
316. Vì sao ViT thường nhạy với initialization và optimization hơn CNN trong một số thiết lập?
317. CNN và ViT có yêu cầu learning rate giống nhau không?
318. Batch size ảnh hưởng đến CNN và ViT như thế nào?
319. Weight decay ảnh hưởng thế nào đến CNN và ViT?
320. Data augmentation quan trọng với CNN và ViT khác nhau thế nào?
321. Vì sao ViT thường hưởng lợi từ augmentation mạnh?
322. Mixup và CutMix có thể giúp ViT như thế nào?
323. CNN và ViT khác nhau thế nào về overfitting?
324. Vì sao pretraining quan trọng với ViT?
325. Transfer learning CNN và ViT khác nhau thế nào?
326. Fine-tuning CNN và ViT có chiến lược khác nhau không?
327. Layer freezing có ý nghĩa gì với CNN?
328. Layer freezing có ý nghĩa gì với ViT?
329. Vì sao learning rate có thể cần khác nhau giữa pretrained backbone và classification head?

---

# Chương 11. CNN vs ViT — Data, Compute & Generalization

## 11.1. Data

330. CNN và ViT cần lượng dữ liệu khác nhau như thế nào?
331. Vì sao CNN thường hoạt động tốt trong low-data regime?
332. Vì sao ViT có thể vượt CNN khi dữ liệu đủ lớn?
333. Pretraining thay đổi sự khác biệt CNN vs ViT như thế nào?
334. Self-supervised pretraining ảnh hưởng thế nào đến ViT?
335. ImageNet-scale pretraining có vai trò gì?

## 11.2. Computational Cost

336. Complexity của convolution phụ thuộc vào những yếu tố nào?
337. Complexity của self-attention phụ thuộc vào những yếu tố nào?
338. Vì sao ViT gặp vấn đề khi image resolution tăng?
339. Vì sao CNN có thể hiệu quả hơn ở high-resolution image?
340. Tại sao Swin dùng window attention?
341. So sánh memory complexity của CNN và ViT.
342. So sánh inference latency của CNN và ViT.
343. FLOPs thấp có luôn đồng nghĩa latency thấp không?
344. Hardware GPU ảnh hưởng thế nào đến CNN và ViT?
345. Memory bandwidth ảnh hưởng thế nào đến hai kiến trúc?

---

# Chương 12. CNN vs ViT — Vision Tasks

## 12.1. Image Classification

346. CNN và ViT khác nhau thế nào trong image classification?
347. Vì sao classification là task phù hợp với ViT nguyên bản?
348. CNN có ưu điểm gì trong classification?
349. ViT có ưu điểm gì trong classification?
350. Khi nào nên chọn CNN cho classification?
351. Khi nào nên chọn ViT cho classification?

## 12.2. Object Detection

352. Vì sao image classification và object detection yêu cầu representation khác nhau?
353. Tại sao object detection cần multi-scale features?
354. CNN backbone hỗ trợ object detection như thế nào?
355. ViT backbone hỗ trợ object detection như thế nào?
356. Tại sao hierarchical Transformer phù hợp với detection?
357. FPN trong CNN và hierarchical feature trong Transformer khác nhau thế nào?

## 12.3. Segmentation

358. Vì sao semantic segmentation cần spatial detail?
359. CNN encoder-decoder xử lý segmentation như thế nào?
360. ViT có thể sử dụng cho segmentation như thế nào?
361. Vì sao patchification có thể gây mất spatial detail?
362. CNN và ViT khác nhau thế nào khi khôi phục spatial resolution?

## 12.4. Video

363. CNN xử lý video như thế nào?
364. ViT có thể mở rộng sang video như thế nào?
365. Spatial attention và temporal attention khác nhau thế nào?
366. Vì sao video Transformer có computational cost rất lớn?
367. CNN và Transformer khác nhau thế nào trong modeling temporal dependency?

---

# Chương 13. CNN vs ViT — Failure Analysis & Debugging

## 13.1. CNN Failure

368. CNN bị overfitting thì kiểm tra những gì?
369. CNN underfitting thì kiểm tra những gì?
370. Nếu loss không giảm, cần kiểm tra những thành phần nào?
371. Nếu gradient exploding trong CNN, nguyên nhân có thể là gì?
372. Nếu feature map trở nên quá nhỏ, vấn đề có thể nằm ở đâu?
373. Nếu model mất spatial information quá nhanh, cần kiểm tra gì?
374. Nếu CNN nhận diện object tốt nhưng thất bại với thay đổi vị trí, nguyên nhân là gì?

## 13.2. ViT Failure

375. Nếu ViT overfit trên dataset nhỏ, cần kiểm tra gì?
376. Nếu ViT training không ổn định, cần kiểm tra những hyperparameter nào?
377. Nếu ViT không hội tụ, cần kiểm tra patch embedding không?
378. Nếu positional embedding sai shape thì chuyện gì xảy ra?
379. Nếu thay đổi image resolution khi inference thì positional embedding xử lý thế nào?
380. Sequence length quá lớn gây vấn đề gì?
381. Nếu GPU hết memory khi training ViT, nguyên nhân chính có thể là gì?
382. Nếu ViT không học được spatial relationship, cần kiểm tra gì?
383. Nếu attention map trở nên quá uniform, điều đó có thể chỉ ra vấn đề gì?

---

# Chương 14. CNN vs ViT — Architecture Design

## 14.1. Design Reasoning

384. Nếu xây dựng model cho dataset nhỏ, bạn chọn CNN hay ViT? Vì sao?
385. Nếu dataset cực lớn, lựa chọn có thay đổi không?
386. Nếu image resolution rất cao, lựa chọn có thay đổi không?
387. Nếu latency là constraint chính, nên cân nhắc kiến trúc nào?
388. Nếu memory là constraint chính, nên cân nhắc kiến trúc nào?
389. Nếu cần global context mạnh, kiến trúc nào phù hợp?
390. Nếu cần local texture mạnh, kiến trúc nào phù hợp?
391. Nếu cần model mobile/edge, lựa chọn nào hợp lý?
392. Nếu cần transfer learning, CNN và ViT khác nhau thế nào?
393. Nếu có pretrained CNN nhưng không có pretrained ViT phù hợp, bạn chọn gì?
394. Nếu có dữ liệu rất ít nhưng domain khác ImageNet, bạn sẽ thiết kế thế nào?

## 14.2. Hybrid Design

395. Tại sao cần CNN + Transformer?
396. CNN có thể đóng vai trò feature extractor trước Transformer như thế nào?
397. Transformer có thể đóng vai trò global context module sau CNN như thế nào?
398. Có thể thay convolution bằng self-attention hoàn toàn không?
399. Khi thay convolution bằng self-attention, inductive bias nào bị mất?
400. Khi thêm convolution vào ViT, inductive bias nào được đưa trở lại?
401. Hybrid architecture có nhất thiết tốt hơn CNN hoặc ViT thuần túy không?
402. Làm thế nào thiết kế ablation study cho CNN vs ViT vs Hybrid?

---

# Chương 15. CNN vs ViT — Research-Level Questions

## 15.1. Inductive Bias

403. Tại sao inductive bias quyết định data efficiency?
404. CNN và ViT đại diện cho hai cách đưa prior vào learning như thế nào?
405. Nếu bỏ locality bias khỏi CNN, architecture sẽ thay đổi thế nào?
406. Nếu thêm locality bias vào ViT, model sẽ thay đổi thế nào?
407. Có thể xem ViT là một mô hình ít prior hơn CNN không?
408. Ít inductive bias có phải luôn tốt hơn không?
409. Khi dataset đủ lớn, inductive bias còn quan trọng không?

## 15.2. Scaling

410. CNN scale theo depth như thế nào?
411. CNN scale theo width như thế nào?
412. CNN scale theo resolution như thế nào?
413. ViT scale theo model dimension như thế nào?
414. ViT scale theo số layer như thế nào?
415. ViT scale theo số token như thế nào?
416. Scaling laws ảnh hưởng thế nào đến CNN và ViT?
417. Tại sao large-scale training có thể thay đổi kết luận CNN vs ViT?

## 15.3. Representation Learning

418. CNN học hierarchical representation như thế nào?
419. ViT học hierarchical representation như thế nào?
420. CNN có thể học global representation không?
421. ViT có thể học local representation không?
422. Attention head có thể biểu diễn những loại relationship nào?
423. Feature hierarchy của CNN và token hierarchy của ViT khác nhau thế nào?
424. Layer depth ảnh hưởng thế nào đến semantic abstraction trong hai kiến trúc?

## 15.4. Interpretability

425. Feature visualization của CNN cho biết điều gì?
426. Attention visualization của ViT cho biết điều gì?
427. Attention map có phải explanation đáng tin cậy không?
428. Saliency map có thể được dùng để so sánh CNN và ViT không?
429. Làm thế nào thiết kế experiment để kiểm tra model thực sự sử dụng object thay vì background?
430. Làm thế nào kiểm tra CNN/ViT có học shortcut không?

---

# Chương 16. Interview Challenge

Đây là nhóm câu hỏi nên dùng ở mức **phỏng vấn ML/DL nâng cao**, yêu cầu giải thích bằng reasoning thay vì học thuộc.

## 16.1. Explain the Architecture

431. Hãy giải thích CNN từ pixel đến classification output.
432. Hãy giải thích ViT từ pixel đến classification output.
433. Hãy giải thích tại sao CNN có local receptive field.
434. Hãy giải thích tại sao ViT có global receptive field.
435. Hãy giải thích inductive bias của CNN.
436. Hãy giải thích inductive bias của ViT.
437. Hãy giải thích tại sao CNN thường tốt với dataset nhỏ.
438. Hãy giải thích tại sao ViT có thể scale tốt với dataset lớn.
439. Hãy giải thích tại sao patch size ảnh hưởng mạnh đến ViT.
440. Hãy giải thích tại sao self-attention có complexity `O(N²)`.

## 16.2. Compare

441. CNN vs ViT: local vs global?
442. CNN vs ViT: parameter sharing?
443. CNN vs ViT: receptive field?
444. CNN vs ViT: inductive bias?
445. CNN vs ViT: data efficiency?
446. CNN vs ViT: computational complexity?
447. CNN vs ViT: memory usage?
448. CNN vs ViT: training stability?
449. CNN vs ViT: scalability?
450. CNN vs ViT: transfer learning?
451. CNN vs ViT: high-resolution images?
452. CNN vs ViT: small dataset?
453. CNN vs ViT: large dataset?
454. CNN vs ViT: edge deployment?
455. CNN vs ViT: object detection?
456. CNN vs ViT: segmentation?

## 16.3. Architecture Reasoning

457. Nếu CNN không có pooling thì điều gì xảy ra?
458. Nếu CNN chỉ dùng kernel 1×1 thì còn học spatial relationship không?
459. Nếu tăng kernel size liên tục thì tại sao không phải lúc nào cũng tốt?
460. Nếu bỏ residual connection khỏi ResNet thì điều gì xảy ra?
461. Nếu ViT bỏ positional embedding thì điều gì xảy ra?
462. Nếu ViT giảm patch size xuống rất nhỏ thì điều gì xảy ra?
463. Nếu ViT tăng patch size quá lớn thì điều gì xảy ra?
464. Nếu bỏ CLS token thì ViT có thể classification bằng cách nào?
465. Nếu thay self-attention bằng convolution thì architecture sẽ thay đổi bản chất thế nào?
466. Nếu thay convolution bằng self-attention thì architecture sẽ thay đổi bản chất thế nào?

## 16.4. Design Challenge

467. Thiết kế model cho dataset 10K ảnh.
468. Thiết kế model cho dataset hàng triệu ảnh.
469. Thiết kế model cho ảnh `224×224`.
470. Thiết kế model cho ảnh `4K`.
471. Thiết kế model chạy real-time trên edge device.
472. Thiết kế model cần global context mạnh.
473. Thiết kế model cần nhận diện texture nhỏ.
474. Thiết kế hybrid CNN-ViT.
475. Chọn patch size cho một ViT và giải thích trade-off.
476. Chọn depth/width của CNN và giải thích trade-off.
477. Chọn số attention heads cho ViT và giải thích trade-off.
478. Thiết kế ablation study giữa CNN và ViT.

---

# Chương 17. Research & Critical Thinking

479. Tại sao CNN xuất hiện trước Transformer trong computer vision?
480. Transformer có thực sự "thay thế" CNN không?
481. ViT có thực sự không cần inductive bias không?
482. CNN có thể đạt global modeling bằng cách nào?
483. ViT có thể đạt locality bằng cách nào?
484. Local attention có phải là sự kết hợp giữa CNN và ViT không?
485. Hierarchical Transformer có đang tái tạo lại ý tưởng của CNN không?
486. ConvNeXt cho thấy điều gì về sự khác biệt giữa CNN và Transformer?
487. Nếu hai model có cùng FLOPs, model nào chắc chắn nhanh hơn không?
488. Nếu hai model có cùng số parameter, model nào chắc chắn tốt hơn không?
489. Accuracy cao hơn có chứng minh architecture tốt hơn không?
490. Làm thế nào tách ảnh hưởng của architecture khỏi ảnh hưởng của pretraining?
491. Làm thế nào thiết kế fair comparison giữa CNN và ViT?
492. Vì sao cần giữ dataset, augmentation và training budget giống nhau khi so sánh?
493. Làm thế nào thực hiện ablation để xác định lợi ích thực sự của self-attention?
494. Làm thế nào xác định lợi ích đến từ architecture hay scale?
495. Nếu ViT tốt hơn CNN, làm thế nào kiểm tra nguyên nhân là global attention?
496. Nếu CNN tốt hơn ViT, làm thế nào kiểm tra nguyên nhân là inductive bias?
497. Có thể xây dựng một experiment để đo mức độ local/global dependency của model không?
498. Có thể định lượng inductive bias của CNN và ViT không?
499. Khi nào CNN vẫn là lựa chọn khoa học hợp lý thay vì chạy theo Transformer?
500. Trong tương lai, CNN và ViT có thể hội tụ về một kiến trúc chung không?
