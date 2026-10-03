$$
\begin{aligned}
\mathbf w_T
&=\mathbf w_{T-1}+\alpha(G-\mathbf w_{T-1}^{\top}\mathbf x_{T-1})\mathbf x_{T-1}\\
&=\mathbf w_{T-1}+\alpha\mathbf x_{T-1}(-\mathbf x_{T-1}^{\top}\mathbf w_{T-1})+\alpha G\mathbf x_{T-1}\\
&=(\mathbf I-\alpha\mathbf x_{T-1}\mathbf x_{T-1}^{\top})\mathbf w_{T-1}+\alpha G\mathbf x_{T-1}\\
&=\mathbf F_{T-1}\mathbf w_{T-1}+\alpha G\mathbf x_{T-1},
\end{aligned}
$$

其中 \(\mathbf F_t\doteq\mathbf I-\alpha\mathbf x_t\mathbf x_t^\top\) 是一个“遗忘”或“衰减”矩阵。继续递归展开：

$$
\begin{aligned}
\mathbf w_T
&=\mathbf F_{T-1}(\mathbf F_{T-2}\mathbf w_{T-2}+\alpha G\mathbf x_{T-2})+\alpha G\mathbf x_{T-1}\\
&=\mathbf F_{T-1}\mathbf F_{T-2}\mathbf w_{T-2}
+\alpha G(\mathbf F_{T-1}\mathbf x_{T-2}+\mathbf x_{T-1})\\
&=\mathbf F_{T-1}\mathbf F_{T-2}(\mathbf F_{T-3}\mathbf w_{T-3}+\alpha G\mathbf x_{T-3})
+\alpha G(\mathbf F_{T-1}\mathbf x_{T-2}+\mathbf x_{T-1})\\
&=\mathbf F_{T-1}\mathbf F_{T-2}\mathbf F_{T-3}\mathbf w_{T-3}
+\alpha G(\mathbf F_{T-1}\mathbf F_{T-2}\mathbf x_{T-3}
+\mathbf F_{T-1}\mathbf x_{T-2}+\mathbf x_{T-1})\\
&\vdots\\
&=\underbrace{\mathbf F_{T-1}\mathbf F_{T-2}\cdots\mathbf F_0\mathbf w_0}_{\mathbf a_{T-1}}
+\alpha G\underbrace{\sum_{k=0}^{T-1}\mathbf F_{T-1}\mathbf F_{T-2}\cdots\mathbf F_{k+1}\mathbf x_k}_{\mathbf z_{T-1}}\\
&=\mathbf a_{T-1}+\alpha G\mathbf z_{T-1}.
\end{aligned}\tag{12.14}
$$

其中 \(\mathbf a_{T-1}\) 和 \(\mathbf z_{T-1}\) 是两个辅助存储向量在时刻 \(T-1\) 的值；即使尚不知道 \(G\)，也可以用每步 \(O(d)\) 的计算量增量更新它们。\(\mathbf z_t\) 实际上是 Dutch 式的资格迹。先初始化为 \(\mathbf z_0=\mathbf x_0\)，然后按下式更新：

$$
\begin{aligned}
\mathbf z_t
&=\sum_{k=0}^{t}\mathbf F_t\mathbf F_{t-1}\cdots\mathbf F_{k+1}\mathbf x_k,\qquad 1\le t<T\\
&=\sum_{k=0}^{t-1}\mathbf F_t\mathbf F_{t-1}\cdots\mathbf F_{k+1}\mathbf x_k+\mathbf x_t\\
&=\mathbf F_t\sum_{k=0}^{t-1}\mathbf F_{t-1}\mathbf F_{t-2}\cdots\mathbf F_{k+1}\mathbf x_k+\mathbf x_t\\
&=\mathbf F_t\mathbf z_{t-1}+\mathbf x_t\\
&=(\mathbf I-\alpha\mathbf x_t\mathbf x_t^\top)\mathbf z_{t-1}+\mathbf x_t\\
&=\mathbf z_{t-1}-\alpha\mathbf x_t\mathbf x_t^\top\mathbf z_{t-1}+\mathbf x_t\\
&=\mathbf z_{t-1}-\alpha(\mathbf z_{t-1}^\top\mathbf x_t)\mathbf x_t+\mathbf x_t\\
&=\mathbf z_{t-1}+\bigl(1-\alpha\mathbf z_{t-1}^\top\mathbf x_t\bigr)\mathbf x_t.
\end{aligned}
$$

这就是 \(\gamma\lambda=1\) 情形下的 Dutch 迹（对照式（12.11））。辅助向量 \(\mathbf a_t\) 先初始化为 \(\mathbf a_0=\mathbf w_0\)，再按下式更新：

$$
\mathbf a_t\doteq\mathbf F_t\mathbf F_{t-1}\cdots\mathbf F_0\mathbf w_0
=\mathbf F_t\mathbf a_{t-1}
=\mathbf a_{t-1}-\alpha\mathbf x_t\mathbf x_t^\top\mathbf a_{t-1},
\qquad 1\le t<T.
$$
