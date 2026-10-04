# 参考文献 b 分片作者自检记录

范围为 PDF 物理页 739–748（印刷页 719–728），从 Jaakkola/Jordan（2000）至 Zarchan/Musoff（2005）。仅修改 references-b.md 与本记录；源页渲染和辅助比对材料位于 tmp/prml-source，不改 a 分片、共享工具或整章 JSON。

## 完成项

- [x] 编辑前查 git status，读取参考文献源页基线；实际逐页查看 739–748 全部 10 页。每页按左栏从上到下，再右栏从上到下的顺序翻译，未用候选条目数代替目视核对。
- [x] 共 225 条书目，分为 229 个页内段；4 个多出的段是跨页续文。每条原题旁有中文译名；Nilsson 的重印题名另有中文译名，因此共有 226 组题名译文。
- [x] 所有作者及其顺序、首字母、年份与 a/b/c 后缀、December、原题大小写、书刊/会议名、编辑者、卷期、页码、出版社/地点、版次、技术报告号、学位与机构、重印和历史出版状态逐条核对。下面的逐条清单明确登记字段检查结果。
- [x] 原书论文题名通常正体，书名、期刊名、会议录名按各处原页斜体；卷号按源逐项粗体。已按 root 的格式反馈修复最早五页统一 em 的写法，并核对全 10 页。最终有 215 个 em 片段和 90 个 strong 片段。
- [x] 采用原 PDF 字体跨度定位强调，并对每个页内段的原文字母和数字做辅助一致性检查，229/229 相符。该检查按 NFKD 处理连字/组合变音，只作定位和防漏辅证；标点、变音字形、断词、译义仍以实际原页为准。
- [x] 姓名及字形如 Föglein、Sjölander、Kůrková、Lütkepohl、Rätsch、Schölkopf、Møller、Müller、Nadaraya 的 É、Quiñonero-Candela、Svensén、Sankhyā 均按原页。Le Cun 与 LeCun、Nystrom 等源书不同写法不按记忆统一。
- [x] 4 处跨页续接均用 join-previous-paragraph-with-space；同页跨栏的 Kuss（740）及 MacKay（1997，741）等已合为完整条目，不误拆新条。
- [x] 10 个页标齐全；本分片不写 H1 或导读。无图表、显示公式、脚注或习题。HTML 的 p/em/strong 标签均平衡，无异常标签。

## 逐页数量

| PDF 页 | 左栏起始 | 右栏起始 | 本页新条目 | 含跨页续文的段数 |
| --- | --- | --- | --- | --- |
| 739 | 13 | 12 | 25 | 25 |
| 740 | 12 | 10 | 22 | 22 |
| 741 | 13 | 12 | 25 | 26 |
| 742 | 12 | 12 | 24 | 24 |
| 743 | 12 | 12 | 24 | 24 |
| 744 | 11 | 13 | 24 | 24 |
| 745 | 10 | 12 | 22 | 23 |
| 746 | 10 | 11 | 21 | 22 |
| 747 | 10 | 13 | 23 | 24 |
| 748 | 11 | 4 | 15 | 15 |

总计 225 条新条目。与 a 负责的 183 条相加为原书 408 条候选；本表数字已经本作者逐页实看和逐条检查，不只依赖候选登记。

## 跨页字段

- 740→741：Le Cun、Denker、Solla（1990），740 停在编辑者 D. S. Touretzky（Ed.）之后，741 接会议录、Volume 2、pp. 598–605 和 Morgan Kaufmann。
- 744→745：Roth/Steinhage（2000），744 停在编辑者 S. A.，745 接 Solla、Leen、Müller 及会议录 Volume 12、MIT Press。
- 745→746：Simard/Le Cun/Denker（1993），745 停在 Hanson、Cowan 和 and，746 接 C. L. Giles、会议录 Volume 5、pp. 50–58、Morgan Kaufmann。
- 746→747：Tino/Nabney/Sun（2001），746 停在 In，747 接 Dorffner、Bischof、Hornik、ICANN 2001、pp. 421–428 和 Springer。

## 原印细节和修复记录

- 739 的 Kanazawa 条目作者为 S. Russel（单个末尾 l）；740 为 Kschischnang，Lauritzen/Spiegelhalter 原题印 probabailities；742 的 McEliece 原题印 ‘Belief Ppropagation’。以上均已额外实际查看 4 倍原页细节后恢复源印，不静默更正。
- 744 Platt 条目编辑者为 D. Shuurmans，745 Schölkopf（2001）作者为 J. Platt 而非 J. C. Platt；746 原作者写 Stinchecombe，Tarassenko 原题写 mamograms。以上已实际查看 4 倍细节并修复初读偏差。
- 739 原名 Jeffries，期刊缩写 Pro. Roy. Soc. AA；742 Moore 原题用 hierarch；743 Neal（1997）机构写 Department of Computer Statistics；745 Seeger 机构写 University of Edinburg；746 Teh 期刊名写 Americal；747 Tipping/Bishop（1999b）原卷号为 21。按原页保留，不引入外部新版校正。
- 743 Opper（2000b）原名是 Winther，4 倍复看后修复初读为 Winthor 的误差；1999、2000a、2000b 均各自按原页保留。
- 历史状态保留：Jordan（2007）In preparation；Kuss（2006）in press；MacKay（1997）Unpublished manuscript；Teh 等（2006）to appear。未以现时出版情况替换。
- McCulloch、Rumelhart、Widrow 等的重印字段，Nilsson 重印题名/出版商/1990，Minsky 的 Expanded edition 1990，以及 Shannon 的两个页码区间，均完整保留。
- 生成式/判别式、鲁棒、新颖性检测、狄利克雷、期望传播、标准技术术语沿全书约定。源书拼写疑点不放进阅读正文。

## 逐条字段清单

下表每个“✓”均指本作者已对照该条原页检查对应字段；“出版字段”包含该条原有的全部期刊/会议/书籍、编辑、卷期页码、出版社/机构、版次、历史状态或重印信息，不表示原书每条都有这些字段。“强调”指原文正体/斜体/粗体。

| PDF/条目 | 原条目识别 | 中文题名 | 作者/年 | 原题/译义 | 出版字段 | 强调 |
| --- | --- | --- | --- | --- | --- | --- |
| 739.01 | Jaakkola, T. and M. I. Jordan (2000) | 通过变分方法进行贝叶斯参数估计 | ✓ | ✓ | ✓ | ✓ |
| 739.02 | Jaakkola, T. S. (2001) | 变分近似方法教程 | ✓ | ✓ | ✓ | ✓ |
| 739.03 | Jaakkola, T. S. and D. Haussler (1999) | 在判别式分类器中利用生成式模型 | ✓ | ✓ | ✓ | ✓ |
| 739.04 | Jacobs, R. A., M. I. Jordan, S. J. Nowlan, and G. E. Hinton (1991) | 局部专家的自适应混合 | ✓ | ✓ | ✓ | ✓ |
| 739.05 | Jaynes, E. T. (2003) | 概率论：科学的逻辑 | ✓ | ✓ | ✓ | ✓ |
| 739.06 | Jebara, T. (2004) | 机器学习：判别式与生成式方法 | ✓ | ✓ | ✓ | ✓ |
| 739.07 | Jeffries, H. (1946) | 估计问题中先验概率的一种不变形式 | ✓ | ✓ | ✓ | ✓ |
| 739.08 | Jelinek, F. (1997) | 语音识别的统计方法 | ✓ | ✓ | ✓ | ✓ |
| 739.09 | Jensen, C., A. Kong, and U. Kjaerulff (1995) | 超大型概率专家系统中的分块 Gibbs 采样 | ✓ | ✓ | ✓ | ✓ |
| 739.10 | Jensen, F. V. (1996) | 贝叶斯网络导论 | ✓ | ✓ | ✓ | ✓ |
| 739.11 | Jerrum, M. and A. Sinclair (1996) | 马尔可夫链蒙特卡洛方法：近似计数与积分的一种方法 | ✓ | ✓ | ✓ | ✓ |
| 739.12 | Jolliffe, I. T. (2002) | 主成分分析 | ✓ | ✓ | ✓ | ✓ |
| 739.13 | Jordan, M. I. (1999) | 图模型中的学习 | ✓ | ✓ | ✓ | ✓ |
| 739.14 | Jordan, M. I. (2007) | 概率图模型导论 | ✓ | ✓ | ✓ | ✓ |
| 739.15 | Jordan, M. I., Z. Ghahramani, T. S. Jaakkola, and L. K. Saul (1999) | 图模型变分方法导论 | ✓ | ✓ | ✓ | ✓ |
| 739.16 | Jordan, M. I. and R. A. Jacobs (1994) | 层次专家混合与 EM 算法 | ✓ | ✓ | ✓ | ✓ |
| 739.17 | Jutten, C. and J. Herault (1991) | 源信号盲分离，1：基于神经仿生结构的自适应算法 | ✓ | ✓ | ✓ | ✓ |
| 739.18 | Kalman, R. E. (1960) | 线性滤波与预测问题的新方法 | ✓ | ✓ | ✓ | ✓ |
| 739.19 | Kambhatla, N. and T. K. Leen (1997) | 通过局部主成分分析进行降维 | ✓ | ✓ | ✓ | ✓ |
| 739.20 | Kanazawa, K., D. Koller, and S. Russel (1995) | 动态概率网络的随机模拟算法 | ✓ | ✓ | ✓ | ✓ |
| 739.21 | Kapadia, S. (1998) | 隐马尔可夫模型的判别式训练 | ✓ | ✓ | ✓ | ✓ |
| 739.22 | Kapur, J. (1989) | 科学与工程中的最大熵方法 | ✓ | ✓ | ✓ | ✓ |
| 739.23 | Karush, W. (1939) | 以不等式为附加约束的多变量函数极小值 | ✓ | ✓ | ✓ | ✓ |
| 739.24 | Kass, R. E. and A. E. Raftery (1995) | 贝叶斯因子 | ✓ | ✓ | ✓ | ✓ |
| 739.25 | Kearns, M. J. and U. V. Vazirani (1994) | 计算学习理论导论 | ✓ | ✓ | ✓ | ✓ |
| 740.01 | Kindermann, R. and J. L. Snell (1980) | 马尔可夫随机场及其应用 | ✓ | ✓ | ✓ | ✓ |
| 740.02 | Kittler, J. and J. Föglein (1984) | 多光谱像素数据的上下文分类 | ✓ | ✓ | ✓ | ✓ |
| 740.03 | Kohonen, T. (1982) | 拓扑正确的特征映射的自组织形成 | ✓ | ✓ | ✓ | ✓ |
| 740.04 | Kohonen, T. (1995) | 自组织映射 | ✓ | ✓ | ✓ | ✓ |
| 740.05 | Kolmogorov, V. and R. Zabih (2004) | 哪些能量函数可以通过图割来最小化？ | ✓ | ✓ | ✓ | ✓ |
| 740.06 | Kreinovich, V. Y. (1991) | 任意非线性足以使神经网络表示所有函数：一个定理 | ✓ | ✓ | ✓ | ✓ |
| 740.07 | Krogh, A., M. Brown, I. S. Mian, K. Sjölander, and D. Haussler (1994) | 计算生物学中的隐马尔可夫模型：在蛋白质建模中的应用 | ✓ | ✓ | ✓ | ✓ |
| 740.08 | Kschischnang, F. R., B. J. Frey, and H. A. Loeliger (2001) | 因子图与和积算法 | ✓ | ✓ | ✓ | ✓ |
| 740.09 | Kuhn, H. W. and A. W. Tucker (1951) | 非线性规划 | ✓ | ✓ | ✓ | ✓ |
| 740.10 | Kullback, S. and R. A. Leibler (1951) | 论信息与充分性 | ✓ | ✓ | ✓ | ✓ |
| 740.11 | Kůrková, V. and P. C. Kainen (1994) | 功能等价的前馈神经网络 | ✓ | ✓ | ✓ | ✓ |
| 740.12 | Kuss, M. and C. Rasmussen (2006) | 评估高斯过程分类的近似方法 | ✓ | ✓ | ✓ | ✓ |
| 740.13 | Lasserre, J., C. M. Bishop, and T. Minka (2006) | 生成式模型与判别式模型的有理论依据的混合 | ✓ | ✓ | ✓ | ✓ |
| 740.14 | Lauritzen, S. and N. Wermuth (1989) | 部分定性、部分定量变量之间关联的图模型 | ✓ | ✓ | ✓ | ✓ |
| 740.15 | Lauritzen, S. L. (1992) | 混合图关联模型中概率、均值与方差的传播 | ✓ | ✓ | ✓ | ✓ |
| 740.16 | Lauritzen, S. L. (1996) | 图模型 | ✓ | ✓ | ✓ | ✓ |
| 740.17 | Lauritzen, S. L. and D. J. Spiegelhalter (1988) | 图结构上的局部概率计算及其在专家系统中的应用 | ✓ | ✓ | ✓ | ✓ |
| 740.18 | Lawley, D. N. (1953) | 因子分析的一种修正估计方法及若干大样本结果 | ✓ | ✓ | ✓ | ✓ |
| 740.19 | Lawrence, N. D., A. I. T. Rowstron, C. M. Bishop, and M. J. Taylor (2002) | 优化移动设备的同步时间 | ✓ | ✓ | ✓ | ✓ |
| 740.20 | Lazarsfeld, P. F. and N. W. Henry (1968) | 潜在结构分析 | ✓ | ✓ | ✓ | ✓ |
| 740.21 | Le Cun, Y., B. Boser, J. S. Denker, D. Henderson, R. E. Howard, W. Hubbard, and L. D. Jackel (1989) | 将反向传播应用于手写邮政编码识别 | ✓ | ✓ | ✓ | ✓ |
| 740.22→741 | Le Cun, Y., J. S. Denker, and S. A. Solla (1990) | 最优脑损伤 | ✓ | ✓ | ✓ | ✓ |
| 741.01 | LeCun, Y., L. Bottou, Y. Bengio, and P. Haffner (1998) | 将基于梯度的学习应用于文档识别 | ✓ | ✓ | ✓ | ✓ |
| 741.02 | Lee, Y., Y. Lin, and G. Wahba (2001) | 多类别支持向量机 | ✓ | ✓ | ✓ | ✓ |
| 741.03 | Leen, T. K. (1995) | 从数据分布到不变性学习中的正则化 | ✓ | ✓ | ✓ | ✓ |
| 741.04 | Lindley, D. V. (1982) | 评分规则与概率的必然性 | ✓ | ✓ | ✓ | ✓ |
| 741.05 | Liu, J. S. (Ed.) (2001) | 科学计算中的蒙特卡洛策略 | ✓ | ✓ | ✓ | ✓ |
| 741.06 | Lloyd, S. P. (1982) | PCM 中的最小二乘量化 | ✓ | ✓ | ✓ | ✓ |
| 741.07 | Lütkepohl, H. (1996) | 矩阵手册 | ✓ | ✓ | ✓ | ✓ |
| 741.08 | MacKay, D. J. C. (1992a) | 贝叶斯插值 | ✓ | ✓ | ✓ | ✓ |
| 741.09 | MacKay, D. J. C. (1992b) | 证据框架在分类网络中的应用 | ✓ | ✓ | ✓ | ✓ |
| 741.10 | MacKay, D. J. C. (1992c) | 反向传播网络的实用贝叶斯框架 | ✓ | ✓ | ✓ | ✓ |
| 741.11 | MacKay, D. J. C. (1994) | 反向传播网络的贝叶斯方法 | ✓ | ✓ | ✓ | ✓ |
| 741.12 | MacKay, D. J. C. (1995) | 贝叶斯神经网络与密度网络 | ✓ | ✓ | ✓ | ✓ |
| 741.13 | MacKay, D. J. C. (1997) | 隐马尔可夫模型的集成学习 | ✓ | ✓ | ✓ | ✓ |
| 741.14 | MacKay, D. J. C. (1998) | 高斯过程导论 | ✓ | ✓ | ✓ | ✓ |
| 741.15 | MacKay, D. J. C. (1999) | 超参数处理的近似方法比较 | ✓ | ✓ | ✓ | ✓ |
| 741.16 | MacKay, D. J. C. (2003) | 信息论、推断与学习算法 | ✓ | ✓ | ✓ | ✓ |
| 741.17 | MacKay, D. J. C. and M. N. Gibbs (1999) | 密度网络 | ✓ | ✓ | ✓ | ✓ |
| 741.18 | MacKay, D. J. C. and R. M. Neal (1999) | 基于极稀疏矩阵的优良纠错码 | ✓ | ✓ | ✓ | ✓ |
| 741.19 | MacQueen, J. (1967) | 多元观测分类与分析的若干方法 | ✓ | ✓ | ✓ | ✓ |
| 741.20 | Magnus, J. R. and H. Neudecker (1999) | 矩阵微分及其在统计学和计量经济学中的应用 | ✓ | ✓ | ✓ | ✓ |
| 741.21 | Mallat, S. (1999) | 信号处理的小波之旅 | ✓ | ✓ | ✓ | ✓ |
| 741.22 | Manning, C. D. and H. Schütze (1999) | 统计自然语言处理基础 | ✓ | ✓ | ✓ | ✓ |
| 741.23 | Mardia, K. V. and P. E. Jupp (2000) | 方向统计学 | ✓ | ✓ | ✓ | ✓ |
| 741.24 | Maybeck, P. S. (1982) | 随机模型、估计与控制 | ✓ | ✓ | ✓ | ✓ |
| 741.25 | McAllester, D. A. (2003) | PAC 贝叶斯随机模型选择 | ✓ | ✓ | ✓ | ✓ |
| 742.01 | McCullagh, P. and J. A. Nelder (1989) | 广义线性模型 | ✓ | ✓ | ✓ | ✓ |
| 742.02 | McCulloch, W. S. and W. Pitts (1943) | 神经活动内在观念的逻辑演算 | ✓ | ✓ | ✓ | ✓ |
| 742.03 | McEliece, R. J., D. J. C. MacKay, and J. F. Cheng (1998) | 将 Turbo 译码视为 Pearl“信念传播”算法的一个实例 | ✓ | ✓ | ✓ | ✓ |
| 742.04 | McLachlan, G. J. and K. E. Basford (1988) | 混合模型：推断及其在聚类中的应用 | ✓ | ✓ | ✓ | ✓ |
| 742.05 | McLachlan, G. J. and T. Krishnan (1997) | EM 算法及其扩展 | ✓ | ✓ | ✓ | ✓ |
| 742.06 | McLachlan, G. J. and D. Peel (2000) | 有限混合模型 | ✓ | ✓ | ✓ | ✓ |
| 742.07 | Meng, X. L. and D. B. Rubin (1993) | 通过 ECM 算法进行最大似然估计：一个通用框架 | ✓ | ✓ | ✓ | ✓ |
| 742.08 | Metropolis, N., A. W. Rosenbluth, M. N. Rosenbluth, A. H. Teller, and E. Teller (1953) | 使用快速计算机计算状态方程 | ✓ | ✓ | ✓ | ✓ |
| 742.09 | Metropolis, N. and S. Ulam (1949) | 蒙特卡洛方法 | ✓ | ✓ | ✓ | ✓ |
| 742.10 | Mika, S., G. Rätsch, J. Weston, and B. Schölkopf (1999) | 使用核函数的 Fisher 判别分析 | ✓ | ✓ | ✓ | ✓ |
| 742.11 | Minka, T. (2001a) | 用于近似贝叶斯推断的期望传播 | ✓ | ✓ | ✓ | ✓ |
| 742.12 | Minka, T. (2001b) | 一族贝叶斯推断近似算法 | ✓ | ✓ | ✓ | ✓ |
| 742.13 | Minka, T. (2004) | 幂期望传播 | ✓ | ✓ | ✓ | ✓ |
| 742.14 | Minka, T. (2005) | 散度度量与消息传递 | ✓ | ✓ | ✓ | ✓ |
| 742.15 | Minka, T. P. (2001c) | 自动选择 PCA 的维数 | ✓ | ✓ | ✓ | ✓ |
| 742.16 | Minsky, M. L. and S. A. Papert (1969) | 感知机 | ✓ | ✓ | ✓ | ✓ |
| 742.17 | Miskin, J. W. and D. J. C. MacKay (2001) | 用于盲源分离的集成学习 | ✓ | ✓ | ✓ | ✓ |
| 742.18 | Møller, M. (1993) | 前馈神经网络的高效训练 | ✓ | ✓ | ✓ | ✓ |
| 742.19 | Moody, J. and C. J. Darken (1989) | 由局部调谐处理单元构成的网络中的快速学习 | ✓ | ✓ | ✓ | ✓ |
| 742.20 | Moore, A. W. (2000) | 锚点层次结构：利用三角不等式应对高维数据 | ✓ | ✓ | ✓ | ✓ |
| 742.21 | Müller, K. R., S. Mika, G. Rätsch, K. Tsuda, and B. Schölkopf (2001) | 基于核的学习算法导论 | ✓ | ✓ | ✓ | ✓ |
| 742.22 | Müller, P. and F. A. Quintana (2004) | 非参数贝叶斯数据分析 | ✓ | ✓ | ✓ | ✓ |
| 742.23 | Nabney, I. T. (2002) | Netlab：模式识别算法 | ✓ | ✓ | ✓ | ✓ |
| 742.24 | Nadaraya, É. A. (1964) | 论回归估计 | ✓ | ✓ | ✓ | ✓ |
| 743.01 | Nag, R., K. Wong, and F. Fallside (1986) | 使用隐马尔可夫模型进行文字识别 | ✓ | ✓ | ✓ | ✓ |
| 743.02 | Neal, R. M. (1993) | 使用马尔可夫链蒙特卡洛方法进行概率推断 | ✓ | ✓ | ✓ | ✓ |
| 743.03 | Neal, R. M. (1996) | 神经网络的贝叶斯学习 | ✓ | ✓ | ✓ | ✓ |
| 743.04 | Neal, R. M. (1997) | 用于贝叶斯回归与分类的高斯过程模型的蒙特卡洛实现 | ✓ | ✓ | ✓ | ✓ |
| 743.05 | Neal, R. M. (1999) | 利用有序过松弛抑制马尔可夫链蒙特卡洛中的随机游走 | ✓ | ✓ | ✓ | ✓ |
| 743.06 | Neal, R. M. (2000) | 狄利克雷过程混合模型的马尔可夫链采样 | ✓ | ✓ | ✓ | ✓ |
| 743.07 | Neal, R. M. (2003) | 切片采样 | ✓ | ✓ | ✓ | ✓ |
| 743.08 | Neal, R. M. and G. E. Hinton (1999) | 为增量及其他变体提供依据的 EM 算法新视角 | ✓ | ✓ | ✓ | ✓ |
| 743.09 | Nelder, J. A. and R. W. M. Wedderburn (1972) | 广义线性模型 | ✓ | ✓ | ✓ | ✓ |
| 743.10 | Nilsson, N. J. (1965) | 学习机器 | ✓ | ✓ | ✓ | ✓ |
| 743.11 | Nocedal, J. and S. J. Wright (1999) | 数值优化 | ✓ | ✓ | ✓ | ✓ |
| 743.12 | Nowlan, S. J. and G. E. Hinton (1992) | 通过软权重共享简化神经网络 | ✓ | ✓ | ✓ | ✓ |
| 743.13 | Ogden, R. T. (1997) | 统计应用与数据分析中的小波基础 | ✓ | ✓ | ✓ | ✓ |
| 743.14 | Opper, M. and O. Winther (1999) | 在线学习的贝叶斯方法 | ✓ | ✓ | ✓ | ✓ |
| 743.15 | Opper, M. and O. Winther (2000a) | 高斯过程与 SVM：平均场理论和留一法 | ✓ | ✓ | ✓ | ✓ |
| 743.16 | Opper, M. and O. Winther (2000b) | 用于分类的高斯过程 | ✓ | ✓ | ✓ | ✓ |
| 743.17 | Osuna, E., R. Freund, and F. Girosi (1996) | 支持向量机：训练与应用 | ✓ | ✓ | ✓ | ✓ |
| 743.18 | Papoulis, A. (1984) | 概率、随机变量与随机过程 | ✓ | ✓ | ✓ | ✓ |
| 743.19 | Parisi, G. (1988) | 统计场论 | ✓ | ✓ | ✓ | ✓ |
| 743.20 | Pearl, J. (1988) | 智能系统中的概率推理 | ✓ | ✓ | ✓ | ✓ |
| 743.21 | Pearlmutter, B. A. (1994) | Hessian 矩阵的快速精确乘法 | ✓ | ✓ | ✓ | ✓ |
| 743.22 | Pearlmutter, B. A. and L. C. Parra (1997) | 最大似然源分离：对上下文敏感的 ICA 推广 | ✓ | ✓ | ✓ | ✓ |
| 743.23 | Pearson, K. (1901) | 论空间点系的最佳拟合直线与平面 | ✓ | ✓ | ✓ | ✓ |
| 743.24 | Platt, J. C. (1999) | 使用序贯最小优化快速训练支持向量机 | ✓ | ✓ | ✓ | ✓ |
| 744.01 | Platt, J. C. (2000) | 支持向量机的概率 | ✓ | ✓ | ✓ | ✓ |
| 744.02 | Platt, J. C., N. Cristianini, and J. Shawe-Taylor (2000) | 用于多类分类的大间隔有向无环图 | ✓ | ✓ | ✓ | ✓ |
| 744.03 | Poggio, T. and F. Girosi (1990) | 用于逼近与学习的网络 | ✓ | ✓ | ✓ | ✓ |
| 744.04 | Powell, M. J. D. (1987) | 用于多变量插值的径向基函数：综述 | ✓ | ✓ | ✓ | ✓ |
| 744.05 | Press, W. H., S. A. Teukolsky, W. T. Vetterling, and B. P. Flannery (1992) | C 语言数值算法：科学计算的艺术 | ✓ | ✓ | ✓ | ✓ |
| 744.06 | Qazaz, C. S., C. K. I. Williams, and C. M. Bishop (1997) | 广义线性回归中贝叶斯误差条的一个上界 | ✓ | ✓ | ✓ | ✓ |
| 744.07 | Quinlan, J. R. (1986) | 决策树的归纳 | ✓ | ✓ | ✓ | ✓ |
| 744.08 | Quinlan, J. R. (1993) | C4.5：机器学习程序 | ✓ | ✓ | ✓ | ✓ |
| 744.09 | Rabiner, L. and B. H. Juang (1993) | 语音识别基础 | ✓ | ✓ | ✓ | ✓ |
| 744.10 | Rabiner, L. R. (1989) | 隐马尔可夫模型教程及其在语音识别中的部分应用 | ✓ | ✓ | ✓ | ✓ |
| 744.11 | Ramasubramanian, V. and K. K. Paliwal (1990) | 面向快速最近邻搜索的 k-d 树的广义优化 | ✓ | ✓ | ✓ | ✓ |
| 744.12 | Ramsey, F. (1931) | 真理与概率 | ✓ | ✓ | ✓ | ✓ |
| 744.13 | Rao, C. R. and S. K. Mitra (1971) | 矩阵的广义逆及其应用 | ✓ | ✓ | ✓ | ✓ |
| 744.14 | Rasmussen, C. E. (1996) | 高斯过程及其他非线性回归方法的评估 | ✓ | ✓ | ✓ | ✓ |
| 744.15 | Rasmussen, C. E. and J. Quiñonero-Candela (2005) | 通过增广修复相关向量机 | ✓ | ✓ | ✓ | ✓ |
| 744.16 | Rasmussen, C. E. and C. K. I. Williams (2006) | 用于机器学习的高斯过程 | ✓ | ✓ | ✓ | ✓ |
| 744.17 | Rauch, H. E., F. Tung, and C. T. Striebel (1965) | 线性动态系统的最大似然估计 | ✓ | ✓ | ✓ | ✓ |
| 744.18 | Ricotti, L. P., S. Ragazzini, and G. Martinelli (1988) | 在次优二阶反向传播神经网络中学习单词重音 | ✓ | ✓ | ✓ | ✓ |
| 744.19 | Ripley, B. D. (1996) | 模式识别与神经网络 | ✓ | ✓ | ✓ | ✓ |
| 744.20 | Robbins, H. and S. Monro (1951) | 一种随机逼近方法 | ✓ | ✓ | ✓ | ✓ |
| 744.21 | Robert, C. P. and G. Casella (1999) | 蒙特卡洛统计方法 | ✓ | ✓ | ✓ | ✓ |
| 744.22 | Rockafellar, R. (1972) | 凸分析 | ✓ | ✓ | ✓ | ✓ |
| 744.23 | Rosenblatt, F. (1962) | 神经动力学原理：感知机与脑机制理论 | ✓ | ✓ | ✓ | ✓ |
| 744.24→745 | Roth, V. and V. Steinhage (2000) | 使用核函数的非线性判别分析 | ✓ | ✓ | ✓ | ✓ |
| 745.01 | Roweis, S. (1998) | PCA 与 SPCA 的 EM 算法 | ✓ | ✓ | ✓ | ✓ |
| 745.02 | Roweis, S. and Z. Ghahramani (1999) | 线性高斯模型的统一综述 | ✓ | ✓ | ✓ | ✓ |
| 745.03 | Roweis, S. and L. Saul (2000, December) | 通过局部线性嵌入进行非线性降维 | ✓ | ✓ | ✓ | ✓ |
| 745.04 | Rubin, D. B. (1983) | 迭代重加权最小二乘 | ✓ | ✓ | ✓ | ✓ |
| 745.05 | Rubin, D. B. and D. T. Thayer (1982) | 最大似然因子分析的 EM 算法 | ✓ | ✓ | ✓ | ✓ |
| 745.06 | Rumelhart, D. E., G. E. Hinton, and R. J. Williams (1986) | 通过误差传播学习内部表示 | ✓ | ✓ | ✓ | ✓ |
| 745.07 | Rumelhart, D. E., J. L. McClelland, and the PDP Research Group (Eds.) (1986) | 并行分布式处理：认知微观结构探索 | ✓ | ✓ | ✓ | ✓ |
| 745.08 | Sagan, H. (1969) | 变分法导论 | ✓ | ✓ | ✓ | ✓ |
| 745.09 | Savage, L. J. (1961) | 统计实践的主观基础 | ✓ | ✓ | ✓ | ✓ |
| 745.10 | Schölkopf, B., J. Platt, J. Shawe-Taylor, A. Smola, and R. C. Williamson (2001) | 估计高维分布的支撑集 | ✓ | ✓ | ✓ | ✓ |
| 745.11 | Schölkopf, B., A. Smola, and K.-R. Müller (1998) | 作为核特征值问题的非线性成分分析 | ✓ | ✓ | ✓ | ✓ |
| 745.12 | Schölkopf, B., A. Smola, R. C. Williamson, and P. L. Bartlett (2000) | 新的支持向量算法 | ✓ | ✓ | ✓ | ✓ |
| 745.13 | Schölkopf, B. and A. J. Smola (2002) | 核学习 | ✓ | ✓ | ✓ | ✓ |
| 745.14 | Schwarz, G. (1978) | 估计模型的维数 | ✓ | ✓ | ✓ | ✓ |
| 745.15 | Schwarz, H. R. (1988) | 有限元方法 | ✓ | ✓ | ✓ | ✓ |
| 745.16 | Seeger, M. (2003) | 贝叶斯高斯过程模型：PAC 贝叶斯泛化误差界与稀疏近似 | ✓ | ✓ | ✓ | ✓ |
| 745.17 | Seeger, M., C. K. I. Williams, and N. Lawrence (2003) | 加速稀疏高斯过程的快速前向选择 | ✓ | ✓ | ✓ | ✓ |
| 745.18 | Shachter, R. D. and M. Peot (1990) | 信念网络中一般概率推断的模拟方法 | ✓ | ✓ | ✓ | ✓ |
| 745.19 | Shannon, C. E. (1948) | 通信的数学理论 | ✓ | ✓ | ✓ | ✓ |
| 745.20 | Shawe-Taylor, J. and N. Cristianini (2004) | 模式分析的核方法 | ✓ | ✓ | ✓ | ✓ |
| 745.21 | Sietsma, J. and R. J. F. Dow (1991) | 构建具有泛化能力的人工神经网络 | ✓ | ✓ | ✓ | ✓ |
| 745.22→746 | Simard, P., Y. Le Cun, and J. Denker (1993) | 使用一种新的变换距离实现高效模式识别 | ✓ | ✓ | ✓ | ✓ |
| 746.01 | Simard, P., B. Victorri, Y. Le Cun, and J. Denker (1992) | 切向传播：在自适应网络中指定选定不变性的一种形式体系 | ✓ | ✓ | ✓ | ✓ |
| 746.02 | Simard, P. Y., D. Steinkraus, and J. Platt (2003) | 卷积神经网络应用于视觉文档分析的最佳实践 | ✓ | ✓ | ✓ | ✓ |
| 746.03 | Sirovich, L. (1987) | 湍流与相干结构的动力学 | ✓ | ✓ | ✓ | ✓ |
| 746.04 | Smola, A. J. and P. Bartlett (2001) | 稀疏贪心高斯过程回归 | ✓ | ✓ | ✓ | ✓ |
| 746.05 | Spiegelhalter, D. and S. Lauritzen (1990) | 有向图结构上条件概率的序贯更新 | ✓ | ✓ | ✓ | ✓ |
| 746.06 | Stinchecombe, M. and H. White (1989) | 使用隐藏层激活函数非 sigmoid 的前馈网络进行通用逼近 | ✓ | ✓ | ✓ | ✓ |
| 746.07 | Stone, J. V. (2004) | 独立成分分析：入门教程 | ✓ | ✓ | ✓ | ✓ |
| 746.08 | Sung, K. K. and T. Poggio (1994) | 用于基于视图的人脸检测的实例学习 | ✓ | ✓ | ✓ | ✓ |
| 746.09 | Sutton, R. S. and A. G. Barto (1998) | 强化学习导论 | ✓ | ✓ | ✓ | ✓ |
| 746.10 | Svensén, M. and C. M. Bishop (2004) | 鲁棒贝叶斯混合建模 | ✓ | ✓ | ✓ | ✓ |
| 746.11 | Tarassenko, L. (1995) | 用于乳腺 X 线影像中肿块识别的新颖性检测 | ✓ | ✓ | ✓ | ✓ |
| 746.12 | Tax, D. and R. Duin (1999) | 使用支持向量描述数据域 | ✓ | ✓ | ✓ | ✓ |
| 746.13 | Teh, Y. W., M. I. Jordan, M. J. Beal, and D. M. Blei (2006) | 层次狄利克雷过程 | ✓ | ✓ | ✓ | ✓ |
| 746.14 | Tenenbaum, J. B., V. de Silva, and J. C. Langford (2000, December) | 非线性降维的全局框架 | ✓ | ✓ | ✓ | ✓ |
| 746.15 | Tesauro, G. (1994) | TD-Gammon：达到大师水平的自学双陆棋程序 | ✓ | ✓ | ✓ | ✓ |
| 746.16 | Thiesson, B., D. M. Chickering, D. Heckerman, and C. Meek (2004) | 使用图模型进行 ARMA 时间序列建模 | ✓ | ✓ | ✓ | ✓ |
| 746.17 | Tibshirani, R. (1996) | 通过 lasso 进行回归收缩与选择 | ✓ | ✓ | ✓ | ✓ |
| 746.18 | Tierney, L. (1994) | 用于探索后验分布的马尔可夫链 | ✓ | ✓ | ✓ | ✓ |
| 746.19 | Tikhonov, A. N. and V. Y. Arsenin (1977) | 不适定问题的求解 | ✓ | ✓ | ✓ | ✓ |
| 746.20 | Tino, P. and I. T. Nabney (2002) | 层次 GTM：有理论依据地构建局部非线性投影流形 | ✓ | ✓ | ✓ | ✓ |
| 746.21→747 | Tino, P., I. T. Nabney, and Y. Sun (2001) | 使用方向曲率可视化 GTM 投影流形的折叠模式 | ✓ | ✓ | ✓ | ✓ |
| 747.01 | Tipping, M. E. (1999) | 高维二元数据的概率可视化 | ✓ | ✓ | ✓ | ✓ |
| 747.02 | Tipping, M. E. (2001) | 稀疏贝叶斯学习与相关向量机 | ✓ | ✓ | ✓ | ✓ |
| 747.03 | Tipping, M. E. and C. M. Bishop (1997) | 概率主成分分析 | ✓ | ✓ | ✓ | ✓ |
| 747.04 | Tipping, M. E. and C. M. Bishop (1999a) | 概率主成分分析器的混合 | ✓ | ✓ | ✓ | ✓ |
| 747.05 | Tipping, M. E. and C. M. Bishop (1999b) | 概率主成分分析 | ✓ | ✓ | ✓ | ✓ |
| 747.06 | Tipping, M. E. and A. Faul (2003) | 稀疏贝叶斯模型的快速边缘似然最大化 | ✓ | ✓ | ✓ | ✓ |
| 747.07 | Tong, S. and D. Koller (2000) | 受限制的贝叶斯最优分类器 | ✓ | ✓ | ✓ | ✓ |
| 747.08 | Tresp, V. (2001) | 将基于核的系统扩展到大型数据集 | ✓ | ✓ | ✓ | ✓ |
| 747.09 | Uhlenbeck, G. E. and L. S. Ornstein (1930) | 论布朗运动理论 | ✓ | ✓ | ✓ | ✓ |
| 747.10 | Valiant, L. G. (1984) | 可学习性的理论 | ✓ | ✓ | ✓ | ✓ |
| 747.11 | Vapnik, V. N. (1982) | 基于经验数据的依赖关系估计 | ✓ | ✓ | ✓ | ✓ |
| 747.12 | Vapnik, V. N. (1995) | 统计学习理论的本质 | ✓ | ✓ | ✓ | ✓ |
| 747.13 | Vapnik, V. N. (1998) | 统计学习理论 | ✓ | ✓ | ✓ | ✓ |
| 747.14 | Veropoulos, K., C. Campbell, and N. Cristianini (1999) | 控制支持向量机的敏感性 | ✓ | ✓ | ✓ | ✓ |
| 747.15 | Vidakovic, B. (1999) | 使用小波进行统计建模 | ✓ | ✓ | ✓ | ✓ |
| 747.16 | Viola, P. and M. Jones (2004) | 鲁棒实时人脸检测 | ✓ | ✓ | ✓ | ✓ |
| 747.17 | Viterbi, A. J. (1967) | 卷积码的误差界与渐近最优译码算法 | ✓ | ✓ | ✓ | ✓ |
| 747.18 | Viterbi, A. J. and J. K. Omura (1979) | 数字通信与编码原理 | ✓ | ✓ | ✓ | ✓ |
| 747.19 | Wahba, G. (1975) | 广义样条平滑问题中选择平滑参数的 GCV 与 GML 方法比较 | ✓ | ✓ | ✓ | ✓ |
| 747.20 | Wainwright, M. J., T. S. Jaakkola, and A. S. Willsky (2005) | 对数配分函数的一类新上界 | ✓ | ✓ | ✓ | ✓ |
| 747.21 | Walker, A. M. (1969) | 论后验分布的渐近行为 | ✓ | ✓ | ✓ | ✓ |
| 747.22 | Walker, S. G., P. Damien, P. W. Laud, and A. F. M. Smith (1999) | 随机分布及相关函数的贝叶斯非参数推断（附讨论） | ✓ | ✓ | ✓ | ✓ |
| 747.23 | Watson, G. S. (1964) | 平滑回归分析 | ✓ | ✓ | ✓ | ✓ |
| 748.01 | Webb, A. R. (1994) | 前馈网络的函数逼近：用于泛化的最小二乘方法 | ✓ | ✓ | ✓ | ✓ |
| 748.02 | Weisstein, E. W. (1999) | CRC 简明数学百科全书 | ✓ | ✓ | ✓ | ✓ |
| 748.03 | Weston, J. and C. Watkins (1999) | 多类支持向量机 | ✓ | ✓ | ✓ | ✓ |
| 748.04 | Whittaker, J. (1990) | 应用多元统计中的图模型 | ✓ | ✓ | ✓ | ✓ |
| 748.05 | Widrow, B. and M. E. Hoff (1960) | 自适应开关电路 | ✓ | ✓ | ✓ | ✓ |
| 748.06 | Widrow, B. and M. A. Lehr (1990) | 自适应神经网络三十年：感知机、madeline 与反向传播 | ✓ | ✓ | ✓ | ✓ |
| 748.07 | Wiegerinck, W. and T. Heskes (2003) | 分数信念传播 | ✓ | ✓ | ✓ | ✓ |
| 748.08 | Williams, C. K. I. (1998) | 无限神经网络的计算 | ✓ | ✓ | ✓ | ✓ |
| 748.09 | Williams, C. K. I. (1999) | 高斯过程预测：从线性回归到线性预测及其推广 | ✓ | ✓ | ✓ | ✓ |
| 748.10 | Williams, C. K. I. and D. Barber (1998) | 使用高斯过程进行贝叶斯分类 | ✓ | ✓ | ✓ | ✓ |
| 748.11 | Williams, C. K. I. and M. Seeger (2001) | 使用 Nystrom 方法加速核机器 | ✓ | ✓ | ✓ | ✓ |
| 748.12 | Williams, O., A. Blake, and R. Cipolla (2005) | 用于高效视觉跟踪的稀疏贝叶斯学习 | ✓ | ✓ | ✓ | ✓ |
| 748.13 | Williams, P. M. (1996) | 使用神经网络为条件多元密度建模 | ✓ | ✓ | ✓ | ✓ |
| 748.14 | Winn, J. and C. M. Bishop (2005) | 变分消息传递 | ✓ | ✓ | ✓ | ✓ |
| 748.15 | Zarchan, P. and H. Musoff (2005) | 卡尔曼滤波基础：实用方法 | ✓ | ✓ | ✓ | ✓ |

## 最终交接

- 正文原始字节 SHA-256：`7b0777811a5b4df96bf9d59c1f84def4c2a2d96fdb5d7aeb0cc7bfd628468808`。
- 没有未辨认的原文字段。此记录为作者自检，独立逐条审查与网站验收仍由 reviewer/root 负责；不自行宣布参考文献整体验收。

## 独立审查修订

- RB-01：PDF 743 Platt（1999）题名译文的 SMO 名称改为第 7 章已定义的“序贯最小优化”。仅改中文译名，英文、全部出版字段和字体不变。
- RB-02：PDF 746 Simard 等（1992）题名译文改为第 5 章已定义的“切向传播”。仅改中文术语，原题和书目字段、样式不变。
- 保留原始换行并反向恢复上述两个中文术语后的 SHA 与审查快照 5bcd50d2… 完全一致；最终正文指纹已更新，待 reviewer 差异复核。
