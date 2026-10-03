# 目录（续）

- 9.9 基于记忆的函数近似（Memory-based Function Approximation）—— 230
- 9.10 基于核的函数近似（Kernel-based Function Approximation）—— 232
- 9.11 深入理解同策略学习：兴趣与强调（Looking Deeper at On-policy Learning: Interest and Emphasis）—— 234
- 9.12 小结（Summary）—— 236

## 10 使用函数近似的同策略控制（On-policy Control with Approximation）—— 243

- 10.1 回合式半梯度控制（Episodic Semi-gradient Control）—— 243
- 10.2 半梯度 n 步 Sarsa（Semi-gradient n-step Sarsa）—— 247
- 10.3 平均奖励：持续式任务的一种新问题设定（Average Reward: A New Problem Setting for Continuing Tasks）—— 249
- 10.4 不再推荐折扣式设定（Deprecating the Discounted Setting）—— 253
- 10.5 差分式半梯度 n 步 Sarsa（Differential Semi-gradient n-step Sarsa）—— 255
- 10.6 小结（Summary）—— 256

## 11 *使用函数近似的异策略方法（Off-policy Methods with Approximation）—— 257

- 11.1 半梯度方法（Semi-gradient Methods）—— 258
- 11.2 异策略发散的例子（Examples of Off-policy Divergence）—— 260
- 11.3 致命三要素（The Deadly Triad）—— 264
- 11.4 线性价值函数的几何结构（Linear Value-function Geometry）—— 266
- 11.5 对贝尔曼误差做梯度下降（Gradient Descent in the Bellman Error）—— 269
- 11.6 贝尔曼误差不可学习（The Bellman Error is Not Learnable）—— 274
- 11.7 梯度 TD 方法（Gradient-TD Methods）—— 278
- 11.8 强调型 TD 方法（Emphatic-TD Methods）—— 281
- 11.9 降低方差（Reducing Variance）—— 283
- 11.10 小结（Summary）—— 284

## 12 资格迹（Eligibility Traces）—— 287

- 12.1 λ 回报（The λ-return）—— 288
- 12.2 TD(λ) 方法（TD(λ)）—— 292
- 12.3 n 步截断 λ 回报方法（n-step Truncated λ-return Methods）—— 295
- 12.4 重做更新：在线 λ 回报算法（Redoing Updates: Online λ-return Algorithm）—— 297
- 12.5 真正的在线 TD(λ)（True Online TD(λ)）—— 299
- 12.6 *蒙特卡洛学习中的 Dutch 迹（Dutch Traces in Monte Carlo Learning）—— 301
- 12.7 Sarsa(λ) 算法（Sarsa(λ)）—— 303
- 12.8 可变的 λ 与 γ（Variable λ and γ）—— 307
- 12.9 使用控制变量的异策略迹（Off-policy Traces with Control Variates）—— 309
- 12.10 从 Watkins 的 Q(λ) 到树备份(λ)（Watkins’s Q(λ) to Tree-Backup(λ)）—— 312
- 12.11 带迹的稳定异策略方法（Stable Off-policy Methods with Traces）—— 314
- 12.12 实现问题（Implementation Issues）—— 316
- 12.13 结论（Conclusions）—— 317
