:::source-box

### 投影矩阵

对于线性函数近似器，投影操作是线性的，因此可以用一个 \(|\mathcal S|\times|\mathcal S|\) 矩阵表示：

$$
\Pi\doteq\mathbf X(\mathbf X^\top\mathbf D\mathbf X)^{-1}
\mathbf X^\top\mathbf D.
\tag{11.13}
$$

与 9.4 节一样，\(\mathbf D\) 是一个 \(|\mathcal S|\times|\mathcal S|\) 对角矩阵，对角线元素为 \(\mu(s)\)；\(\mathbf X\) 是一个 \(|\mathcal S|\times d\) 矩阵，每一行是一个状态的特征向量 \(\mathbf x(s)^\top\)。如果式（11.13）中的逆不存在，就改用伪逆。借助这些矩阵，向量的范数平方可写为

$$
\lVert v\rVert_\mu^2=v^\top\mathbf Dv,
\tag{11.14}
$$

而近似的线性价值函数可写为

$$
v_{\mathbf w}=\mathbf X\mathbf w.
\tag{11.15}
$$

:::end-source-box

真实价值函数 \(v_\pi\) 是唯一精确满足式（11.16）的价值函数。如果用近似价值函数 \(v_{\mathbf w}\) 取代 \(v_\pi\)，修改后的方程左右两边之差，就可以衡量 \(v_{\mathbf w}\) 偏离 \(v_\pi\) 的程度。我们称之为状态 \(s\) 处的*贝尔曼误差*：

$$
\bar\delta_{\mathbf w}(s)\doteq
\left(\sum_a\pi(a\mid s)\sum_{s',r}
p(s',r\mid s,a)\bigl[r+\gamma v_{\mathbf w}(s')\bigr]\right)
-v_{\mathbf w}(s)
\tag{11.17}
$$

$$
=\mathbb E_\pi\!\left[
R_{t+1}+\gamma v_{\mathbf w}(S_{t+1})-v_{\mathbf w}(S_t)
\mid S_t=s,\ A_t\sim\pi
\right].
\tag{11.18}
$$

这清楚地显示了贝尔曼误差与 TD 误差（式（11.3））之间的关系：贝尔曼误差是 TD 误差的期望。

所有状态上的贝尔曼误差组成的向量 \(\bar{\boldsymbol\delta}_{\mathbf w}\in\mathbb R^{|\mathcal S|}\)，称为*贝尔曼误差向量*（图 11.3 中的 BE）。这个向量在所用范数下的整体大小，是衡量价值函数误差的总体指标，称为*均方贝尔曼误差*：

$$
\overline{\mathrm{BE}}(\mathbf w)=
\lVert\bar{\boldsymbol\delta}_{\mathbf w}\rVert_\mu^2.
\tag{11.19}
$$

一般无法把 \(\overline{\mathrm{BE}}\) 降为零（此时 \(v_{\mathbf w}=v_\pi\)）；但对于线性函数近似，存在唯一一个使 \(\overline{\mathrm{BE}}\) 最小的 \(\mathbf w\)。可表示函数子空间中的这个点（图 11.3 标为 min BE），通常不同于使 \(\overline{\mathrm{VE}}\) 最小的点 \(\Pi v_\pi\)。接下来两节讨论力求最小化 \(\overline{\mathrm{BE}}\) 的方法。

图 11.3 把贝尔曼误差向量画成对近似价值函数应用贝尔曼算子 \(B_\pi:\mathbb R^{|\mathcal S|}\to\mathbb R^{|\mathcal S|}\) 的结果。贝尔曼算子定义为
