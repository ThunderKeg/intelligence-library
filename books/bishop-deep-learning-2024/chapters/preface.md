<!-- pdf-page: 5 -->

# 前言

深度学习利用大型数据集训练多层神经网络，以解决复杂的信息处理任务，如今已成为机器学习领域最成功的范式。过去十年，深度学习改变了计算机视觉、语音识别和自然语言处理等众多领域，并越来越广泛地应用于医疗、制造、商业、金融、科学发现等行业。最近，一类称为大语言模型的庞大神经网络出现了。这些模型的可学习参数量达到万亿量级，展现出通用人工智能的最初迹象，正在推动技术史上规模最大的变革之一。

## 本书的目标

随着深度学习的影响不断扩大，机器学习研究论文的数量与涉及领域也迅速增长，创新步伐仍在加快。对于初学者，理解关键思想已是一项挑战，更不用说追上研究前沿。在这样的背景下，《深度学习：基础与概念》希望帮助机器学习初学者，以及已有相关经验的读者，深入理解支撑深度学习的基础思想和现代深度学习架构与技术的核心概念。这些内容能为读者今后的专门研究打下牢固基础。鉴于这一领域范围广、变化快，我们没有试图全面综述最新研究。本书的主要价值之一在于提炼关键思想。尽管深度学习还会快速发展，这些基础与概念有望经得起时间检验。例如，在本书写作期间，大语言模型发展很快，但其底层的 Transformer 架构和注意力机制在此前五年基本保持不变；机器学习的许多核心原理则已为人所知数十年。

<!-- pdf-page: 6 -->

## 负责任地使用技术

深度学习是一项用途广泛、能力强大的技术，有潜力为世界创造巨大价值，并帮助应对社会面临的一些紧迫挑战。但也正因为如此，它既可能被蓄意滥用，也可能带来无意的伤害。本书选择不讨论深度学习应用中的伦理与社会问题，因为这些问题既重要又复杂，值得比这样一本技术教材所能提供的篇幅更深入的讨论。不过，要讨论这些问题，也需要扎实了解底层技术及其工作原理；我们希望本书能为相关讨论作出有价值的贡献。我们仍强烈建议读者在学习技术的同时，关注自己工作的更广泛影响，并了解如何负责任地使用深度学习和人工智能。

## 本书的结构

本书分为较多篇幅适中的章节，每章探讨一个具体主题。全书采用线性安排：每章只依赖前面章节介绍过的内容。它适合用于机器学习本科或研究生课程的两个学期教学，也适合研究人员和自学者阅读。

要清楚理解机器学习，必须具备一定的数学知识。其中最关键的是概率论、线性代数和多元微积分。本书对所需的概率论概念作了自成体系的介绍，并在附录中概述一些有用的线性代数结果。我们假定读者已熟悉多元微积分的基本概念，但仍提供变分法和拉格朗日乘子法的入门附录。本书的重点是清楚地解释思想，并着重介绍具有实际应用价值的方法，而不是抽象理论。对于较复杂的概念，我们尽可能从文字描述、图示和数学公式等互补角度加以说明。此外，正文讨论的许多关键算法还在单独的方框中作了总结。这些总结不处理计算效率问题，而是对正文中的数学解释加以补充。我们希望不同背景的读者都能读懂本书。

从概念上说，本书也许最适合作为《Neural Networks for Pattern Recognition》（Bishop，1995b）的后续著作。那本书首次从统计学视角对神经网络作了全面论述。本书也可视为《Pattern Recognition and Machine Learning》（Bishop，2006）的姊妹篇；后者覆盖更广的机器学习主题，但出版于深度学习革命之前。为了使本书能够独立阅读，我们从 Bishop（2006）中选取了合适的内容，并围绕深度学习所需的基础思想重新组织。

<!-- pdf-page: 7 -->

<!-- join-previous-paragraph -->

因此，Bishop（2006）中讨论的许多机器学习主题虽然今天仍很有价值，却没有收入本书。例如，那本书深入讨论了贝叶斯方法，而本书几乎完全不采用贝叶斯视角。

本书配有网站，提供辅助资料，包括可免费使用的电子版图书、习题解答，以及 PDF 和 JPEG 格式的可下载图片：

https://www.bishopbook.com

引用本书时，可使用下面的 BibTeX 条目：

```bibtex
@book{Bishop:DeepLearning24,
  author = {Christopher M. Bishop and Hugh Bishop},
  title = {Deep Learning: Foundations and Concepts},
  year = {2024},
  publisher = {Springer}
}
```

如对本书有反馈，或发现错误，请发送邮件至 feedback@bishopbook.com。

## 参考文献

我们着重讨论核心思想，因此没有试图全面回顾相关文献；考虑到这一领域的研究规模和发展速度，这样的回顾也不可能做到。尽管如此，我们仍列出了部分重要研究论文、综述文章和其他进一步阅读资料。许多文献还提供了重要的实现细节；为了不让读者分心，正文并未展开这些细节。

关于一般机器学习与深度学习已有许多著作。其中，在程度与风格上最接近本书的包括 Bishop（2006）、Goodfellow、Bengio 与 Courville（2016）、Murphy（2022）、Murphy（2023）以及 Prince（2023）。

过去十年，机器学习领域发表研究成果的方式发生了明显变化。许多论文在提交同行评审的会议或期刊之前，甚至不再提交正式出版，就先发布到在线论文存储网站。这类网站中最常用的是 arXiv（读作“archive”）：

https://arXiv.org

网站允许作者更新论文，因此同一篇论文可能有多个版本，并对应不同日历年份；这会使引用的版本与年份有时不够明确。arXiv 同时提供论文 PDF 的免费访问。因此，我们采用一个简单规则：按论文首次上传的年份引用，但建议读者阅读最新版本。

<!-- pdf-page: 8 -->

arXiv 论文采用 `arXiv:YYMM.XXXXX` 格式编号，其中 `YY` 和 `MM` 分别表示首次上传的年份与月份。后续版本在编号末尾加版本号 `N`，写作 `arXiv:YYMM.XXXXXvN`。

## 习题

每章末尾都有一组习题，用于巩固正文中的关键思想，或对这些思想作出有意义的拓展和推广。习题是本书的重要组成部分，并按难度分级：从只需片刻即可完成的（⋆），到明显更复杂的（⋆⋆⋆）。我们强烈建议读者动手完成习题，因为积极参与能大幅提高学习效果。所有习题的详细解答均可从本书网站下载 PDF 文件。

## 数学记号

本书沿用 Bishop（2006）的记号。关于机器学习中的数学概览，可参见 Deisenroth、Faisal 与 Ong（2020）。

向量用小写粗体正体字母表示，例如 $\mathbf{x}$；矩阵用大写粗体正体字母表示，例如 $\mathbf{M}$。除非另有说明，所有向量均为列向量。上标 $\mathsf{T}$ 表示矩阵或向量的转置，因此 $\mathbf{x}^{\mathsf{T}}$ 是行向量。记号 $(w_1,\ldots,w_M)$ 表示含 $M$ 个元素的行向量，相应的列向量写作 $\mathbf{w}=(w_1,\ldots,w_M)^{\mathsf{T}}$。$M\times M$ 单位矩阵（identity matrix，也称 unit matrix）记为 $\mathbf{I}_M$；如果维度不会引起歧义，就简写为 $\mathbf{I}$。它的元素 $I_{ij}$ 在 $i=j$ 时为 $1$，在 $i\ne j$ 时为 $0$。单位矩阵的元素有时也记作 $\delta_{ij}$。记号 $\mathbf{1}$ 表示所有元素均为 $1$ 的列向量。$\mathbf{a}\oplus\mathbf{b}$ 表示向量 $\mathbf{a}$ 与 $\mathbf{b}$ 的拼接：若 $\mathbf{a}=(a_1,\ldots,a_N)$，$\mathbf{b}=(b_1,\ldots,b_M)$，则 $\mathbf{a}\oplus\mathbf{b}=(a_1,\ldots,a_N,b_1,\ldots,b_M)$。$|x|$ 表示标量 $x$ 的模，也就是总为非负的绝对值。矩阵 $\mathbf{A}$ 的行列式记作 $\det\mathbf{A}$。

记号 $x\sim p(x)$ 表示 $x$ 从分布 $p(x)$ 中采样。如有歧义，我们用 $p_x(\cdot)$ 这样的下标说明所指的密度。关于随机变量 $x$，函数 $f(x,y)$ 的期望记为 $\mathbb{E}_x[f(x,y)]$。如果平均所针对的变量很明确，就省略下标，例如 $\mathbb{E}[x]$。如果 $x$ 的分布以另一个变量 $z$ 为条件，相应的条件期望写作 $\mathbb{E}_x[f(x)\mid z]$。类似地，$f(x)$ 的方差记作 $\operatorname{var}[f(x)]$；对于向量变量，协方差写作 $\operatorname{cov}[\mathbf{x},\mathbf{y}]$。我们也用 $\operatorname{cov}[\mathbf{x}]$ 简写 $\operatorname{cov}[\mathbf{x},\mathbf{x}]$。

符号 $\forall$ 表示“对所有”，因此 $\forall m\in\mathcal{M}$ 表示集合 $\mathcal{M}$ 中的所有 $m$ 值。$\mathbb{R}$ 表示实数集。在图上，结点 $i$ 的邻居集合记作 $\mathcal{N}(i)$；不要把它与高斯分布（也称正态分布）$\mathcal{N}(x\mid\mu,\sigma^2)$ 混淆。泛函记作 $f[y]$，其中 $y(x)$ 是函数。附录 B 讨论泛函的概念。花括号 $\{\}$ 表示集合。

<!-- pdf-page: 9 -->

<!-- join-previous-paragraph -->

记号 $g(x)=\mathcal{O}(f(x))$ 表示当 $x\to\infty$ 时，$|f(x)/g(x)|$ 有界。例如，若 $g(x)=3x^2+2$，则 $g(x)=\mathcal{O}(x^2)$。记号 $\lfloor x\rfloor$ 表示 $x$ 的下取整，即不大于 $x$ 的最大整数。

译注：原书在 $g(x)=\mathcal O(f(x))$ 的定义中颠倒了分子与分母。标准定义要求当 $x\to\infty$ 时 $|g(x)/f(x)|$ 有界。

假设我们有 $N$ 个独立同分布的 $D$ 维向量观测值 $\mathbf{x}_1,\ldots,\mathbf{x}_N$，其中 $\mathbf{x}=(x_1,\ldots,x_D)^{\mathsf{T}}$。我们可以将这些观测合成一个 $N\times D$ 的数据矩阵 $\mathbf{X}$；矩阵的第 $n$ 行对应行向量 $\mathbf{x}_n^{\mathsf{T}}$。因此，$\mathbf{X}$ 的第 $n$ 行第 $i$ 列元素是第 $n$ 个观测 $\mathbf{x}_n$ 的第 $i$ 个分量，记作 $x_{ni}$。对于一维变量，这样的矩阵记作 $\boldsymbol{\mathsf{x}}$，它是一个列向量，第 $n$ 个元素为 $x_n$。注意，我们用不同字体区分维度为 $N$ 的数据向量 $\boldsymbol{\mathsf{x}}$ 与维度为 $D$ 的变量向量 $\mathbf{x}$。

## 致谢

我们衷心感谢许多人审阅章节草稿并提出宝贵意见。尤其感谢 Samuel Albanie、Cristian Bodnar、John Bronskill、Wessel Bruinsma、Ignas Budvytis、Chi Chen、Yaoyi Chen、Long Chen、Fergal Cotter、Sam Devlin、Aleksander Durumeric、Sebastian Ehlert、Katarina Elez、Andrew Foong、Hong Ge、Paul Gladkov、Paula Gori Giorgi、John Gossman、Tengda Han、Juyeon Heo、Katja Hofmann、Chin-Wei Huang、Yongchaio Huang、Giulio Isacchini、Matthew Johnson、Pragya Kale、Atharva Kelkar、Leon Klein、Pushmeet Kohli、Bonnie Kruft、Adrian Li、Haiguang Liu、Ziheng Lu、Giulia Luise、Stratis Markou、Sergio Valcarcel Macua、Krzysztof Maziarz、Matěj Mezera、Laurence Midgley、Usman Munir、Félix Musil、Elise van der Pol、Tao Qin、Isaac Reid、David Rosenberger、Lloyd Russell、Maximilian Schebek、Megan Stanley、Karin Strauss、Clark Templeton、Marlon Tobaben、Aldo Sayeg Pasos-Trejo、Richard Turner、Max Welling、Furu Wei、Robert Weston、Chris Williams、Yingce Xia、Shufang Xie、Iryna Zaporozhets、Claudio Zeni、Xieyuan Zhang，以及在讨论中作出贡献的其他许多同事。我们还感谢编辑 Paul Drougas、Springer 的其他同事，以及文字编辑 Jonathan Webley 在本书制作过程中给予的支持。

我们特别感谢 Markus Svensén。他曾为 Bishop（2006）的图片和排版，包括本书继续使用的 LaTeX 样式文件，提供大量帮助。我们也感谢许多科学家允许我们转载其已发表研究中的图示。特定图片的致谢列在相应图注中。

Chris 衷心感谢 Microsoft 营造了富有启发性的研究环境，并给予他撰写本书的机会。不过，本书表达的观点和意见属于作者，不一定代表 Microsoft 或其关联机构。与儿子 Hugh 合作完成本书是巨大的荣幸与乐趣；这个共同项目始于第一次新冠疫情封锁期间。

<!-- pdf-page: 10 -->

Hugh 感谢 Wayve Technologies Ltd 慷慨地允许他以兼职方式工作，使他能够参与本书的写作；公司也为他的工作和学习提供了鼓舞人心、支持充分的环境。本书观点不一定代表 Wayve 或其关联机构。他感谢未婚妻 Jemima 始终如一的支持，以及她在语法和文风方面提供的建议。他也感谢 Chris；Chris 一直是一位出色的同事，并在 Hugh 的整个人生中给予他启发。

最后，我们共同感谢家人 Jenna 和 Mark，感谢的事多得无法在这里一一列出。我们似乎是在很久以前，一家人在安塔利亚的海滩上观看日全食，并为《Pattern Recognition and Machine Learning》的献辞页拍下合照。

Chris Bishop、Hugh Bishop  
英国剑桥  
2023 年 10 月
