强调 TD(\(\lambda\)) 定义如下：

\[
\begin{aligned}
\mathbf w_{t+1}&\doteq\mathbf w_t+\alpha\delta_t^s\mathbf z_t,\\
\delta_t^s&\doteq R_{t+1}+\gamma_{t+1}\mathbf w_t^\top\mathbf x_{t+1}-\mathbf w_t^\top\mathbf x_t,\\
\mathbf z_t&\doteq\rho_t(\gamma_t\lambda_t\mathbf z_{t-1}+M_t\mathbf x_t),\qquad\mathbf z_{-1}\doteq\mathbf0,\\
M_t&\doteq\lambda_t I_t+(1-\lambda_t)F_t,\\
F_t&\doteq\rho_{t-1}\gamma_tF_{t-1}+I_t,\qquad F_0\doteq i(S_0).
\end{aligned}
\]

其中 \(M_t\geq0\) 是**强调量**的一般形式，\(F_t\geq0\) 称为**跟踪迹**（followon trace），\(I_t\geq0\) 是§11.8 所述的**兴趣度**。注意，与 \(\delta_t^s\) 一样，\(M_t\) 实际上并不需要作为额外的内存变量；把它的定义代入资格迹方程即可从算法中消去。真正在线版强调 TD(\(\lambda\)) 的伪代码和软件可在网上获取（Sutton，2015b）。

在同策略情形（所有 \(t\) 的 \(\rho_t=1\)），强调 TD(\(\lambda\)) 与传统 TD(\(\lambda\)) 相似，但仍有显著差别。实际上，强调 TD(\(\lambda\)) 对所有依赖状态的 \(\lambda\) 函数都保证收敛；TD(\(\lambda\)) 则不能做到，它只对所有常数 \(\lambda\) 保证收敛。参见 Yu 的反例（Ghiassian、Rafiee 和 Sutton，2016）。

## 12.12 实现问题

乍看起来，使用资格迹的表格型方法似乎比单步方法复杂得多。朴素实现要求每个状态（或状态—行动对）在每个时间步更新其价值估计和资格迹。对单指令多数据并行计算机或合理的人工神经网络（ANN）实现，这未必是问题；但对传统串行计算机，这是个问题。幸运的是，当 \(\lambda\) 和 \(\gamma\) 取典型值时，几乎所有状态的资格迹都接近零；只有最近访问过的状态，其资格迹才显著大于零。只更新这少数几个状态，就能比较准确地近似这些算法。

因此，在传统计算机上实际实现时，可以只跟踪并更新那少数显著大于零的资格迹。使用这一技巧，表格型方法中资格迹带来的计算开销通常只是单步方法的几倍。确切的倍数当然取决于 \(\lambda\)、\(\gamma\) 以及其他计算的开销。注意，从某种意义上说，表格型情形是资格迹计算复杂度最糟的情形。使用函数近似时，不使用资格迹的计算优势通常会缩小。例如，如果使用人工神经网络和反向传播，资格迹一般仅使每步所需的内存和计算量加倍。截断 \(\lambda\)-回报方法（§12.3）虽然总须一些额外内存，但可在传统计算机上高效计算。
