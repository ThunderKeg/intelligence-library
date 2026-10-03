![图 7.5](assets/fig-7-5.png)

图 7.5：本章前面讨论的三种 n 步动作价值更新（图示为四步情形）的备份图，以及统一它们的第四种更新。标记 ρ 表示在异策略情形下需要重要性采样的半步转移。第四种更新逐状态决定采样（\(\sigma_t=1\)）还是不采样（\(\sigma_t=0\)），从而统一其他方法。

图内文字译注：4-step Sarsa＝四步 Sarsa；4-step Tree backup＝四步树备份；4-step Expected Sarsa＝四步期望 Sarsa；4-step Q(σ)＝四步 Q(σ)；ρ＝异策略学习时所需的重要性采样比率；σ＝1 表示采样，σ＝0 表示求期望。空心圆表示状态，实心圆表示行动。

当然，图中最后一个备份图还提示许多其他可能。为了进一步扩展选择范围，可以让采样与求期望之间连续变化。令 \(\sigma_t\in[0,1]\) 表示第 \(t\) 步采样的程度：\(\sigma=1\) 表示完全采样，\(\sigma=0\) 表示完全求期望而不采样。随机变量 \(\sigma_t\) 可以根据时刻 \(t\) 的状态、行动或状态—行动对来设定。我们把这个提出的新算法称为 n 步 Q(σ)。

现在推导 n 步 Q(σ) 的公式。先以界限 \(h=t+n\) 改写树备份的 n 步回报（7.16），再用期望近似价值 \(\bar V\)（7.8）表示：

公式：\(\begin{aligned}G_{t:h}&=R_{t+1}+\gamma\sum_{a\ne A_{t+1}}\pi(a\mid S_{t+1})Q_{h-1}(S_{t+1},a)+\gamma\pi(A_{t+1}\mid S_{t+1})G_{t+1:h}\\&=R_{t+1}+\gamma\bar V_{h-1}(S_{t+1})-\gamma\pi(A_{t+1}\mid S_{t+1})Q_{h-1}(S_{t+1},A_{t+1})+\gamma\pi(A_{t+1}\mid S_{t+1})G_{t+1:h}\\&=R_{t+1}+\gamma\pi(A_{t+1}\mid S_{t+1})\bigl(G_{t+1:h}-Q_{h-1}(S_{t+1},A_{t+1})\bigr)+\gamma\bar V_{h-1}(S_{t+1}).\end{aligned}\)

这与含控制变量的 Sarsa n 步回报（7.14）完全一样，只是把重要性采样比率 \(\rho_{t+1}\) 换成行动概率 \(\pi(A_{t+1}\mid S_{t+1})\)。对于 Q(σ)，我们在这两种情形之间作线性插值：

公式（7.17）：\(G_{t:h}\doteq R_{t+1}+\gamma\Bigl(\sigma_{t+1}\rho_{t+1}+(1-\sigma_{t+1})\pi(A_{t+1}\mid S_{t+1})\Bigr)\bigl(G_{t+1:h}-Q_{h-1}(S_{t+1},A_{t+1})\bigr)+\gamma\bar V_{h-1}(S_{t+1}),\qquad t<h<T\)。
