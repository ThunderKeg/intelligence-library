# 第 45 章原书核对笔记

- PDF 547→548（印刷 535→536）：原书从 PDF547 末的 “Kalman filters, widely used” 接到 PDF548 页首 “to model speech waveforms, also correspond ...”。为避免网站出现残句，译稿在 `pdf-547.md` 中完成整个句子，含“克里金”方法；`pdf-548.md` 从下一个完整的小标题开始。
- PDF 549（印刷 537）式 (45.7)：印本积分测度为 $\mathrm d^H\mathbf w$，而本页例 45.3 中 $H$ 表示隐单元数，$\mathbf w$ 又包含输入、隐层及输出的多组权重和偏置。译稿照印本保留积分测度，不凭维数推导改写。
- PDF 550（印刷 538）样条段落：印本说三次样条的“结点”是二阶导数不连续处，并说在式 (45.10) 加入 $(p-1)$ 个项即可约束任意 $(p-1)$ 次多项式。译稿都照印本保留，未按通常样条平滑结论或自由度计数改写；请独立源审核可视原页。
- PDF 551（印刷 539）式 (45.13) 后的 $A\equiv[D^p]^{\mathsf T}D^p$ 未含式左侧的 $\alpha$；式 (45.15) 的频率权重在印本为 $h^{p/2}$。译稿照高清原页逐字符保留，不按常见推导补入系数或更改指数。
- PDF 554→555（印刷 542→543）：PDF 554 页末“$\mathbf C_{N+1}$ is the $(N+1)\times(N+1)$ covariance”续 PDF 555 页首“matrix for the vector $\mathbf t_{N+1}\equiv(t_1,\ldots,t_{N+1})^{\mathsf T}$”。为避免网页出现残句，整句放在 `pdf-554.md`；`pdf-555.md` 从其后“定义子矩阵”起。
- PDF 557→558（印刷 545→546）：PDF 557 末句“We would like to ‘learn’ these”接 PDF 558 页首“hyperparameters from the data.”，译稿在 `pdf-557.md` 写成完整句，`pdf-558.md` 从下一句继续。
- PDF 559→560（印刷 547→548）：PDF 559 末句“Gaussian processes in”接 PDF 560 页首“contrast are simply smoothing devices.”，译稿把整句放在 `pdf-559.md`，`pdf-560.md` 从下一完整问句开始。
