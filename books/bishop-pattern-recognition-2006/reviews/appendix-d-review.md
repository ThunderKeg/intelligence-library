# 附录 D 独立审查

状态：**独立审查通过，可由 root 登记整附录验收。** 本 reviewer 未参与初译，负责 PDF 725–726 及 724 接口、整附录 JSON；root 独立负责 723–724、图 D.1 和网页，见 `appendix-d-a-review.md`、`appendix-d-ui-review.md`。原文唯一依据为仓库原 PDF，不以提取文本代替逐页查看，不使用本机模型。

- [x] 实际查看 725、726 与接口 724，逐段逐式核对 D.8–D.10。
- [x] 核对原边栏附录 E、Sagan 引用、向量粗体、微分记号和边界条件。
- [x] 核对 a 独审版本与整附录数学、非数学、图像和跨页结构守恒。
- [x] 实际查看 D.3 的两模式引用修复截图，核对所有 10 个公式索引。
- [x] 复核 root 的整附录网页证据，排除新增间距代码对 D 的影响，完成最终指纹与结论。

## 原页内容复核

已分别实际打开 `tmp/prml-root-review/appendix-d/page-724.png`、`page-725.png`、`page-726.png`。726 确为空白，725 从 D.7 与 D.3 的比较继续说明，不错误拼接成前一段。D.8 括号内的偏导、括号外对 x 的导数，D.9 两个平方，D.10 普通二阶导数及负号均与原页一致；没有凭推导添加或删除因子。

Euler–Lagrange 方程的命名、二阶微分方程及 y(x) 的边界条件、无导数被积函数 G(y,x)、对所有 x 的驻定条件、概率归一化、单个拉格朗日乘子与无约束优化、多维变量粗体 x、Sagan（1969）均完整。原条件 ∂G/∂y(x)=0 保留普通偏导，未误改为泛函导数。附录 E 原边栏在 JSON 中以独立括号保留。本分片没有图表、脚注、习题或人物框。未发现需要作者修正的内容问题。

root 已独立核对前半 723–724；本 reviewer 读取其正式报告并将当前 a 与其审过快照逐字比对。另实际打开最终 `assets/appendix-d/a-fig-D-1.png`，与接口原页核对红蓝曲线、两个函数标签、坐标轴和箭头，边缘完整；图注和三项数学标注译注均进入 JSON。

## 整附录 JSON 独立核验

`tmp/prml-review/appendix-d/verify_content.py` 通过：30 根块（标题 1、导读 1、正文 17、编号式 10、图 1），76 数学串与两分片及合并稿逐项多重集合相同，MathML 无 merror，1,035 个非数学 token 守恒。D.1–D.10 连续，无额外无编号显示式。全附录唯一跨页接段 `p01-b009` 保存 `continuedPdfPages:[724]`，跨图续句完整；D.7 后的 b 首段独立保留。未将原 E[f]/δF/f(x) 与 D.4 的 δE 擅自统一。

## 导航修复复核

AC-UI01 的附录引用修复也覆盖 D。已独立核对 D.1–D.10 的索引到对应 JSON 块，实际打开 D.3 的桌面浅色与 390px 深色点击落点图；目标公式在工具栏下，式号正确，窄屏长式使用局部横滑。`reader-qa-appendix-b-appendix-c-appendix-d-navigation-fix.json` 的 D 两模式真实引用点击均为 true。查看记录见 `tmp/prml-review/appendix-c/navigation-fix-viewed.json` 中的 D 两项；此项不替代 root 的完整网页独审。

## 已核内容指纹

| 项目 | SHA-256 |
|---|---|
| a 原始字节/LF | `a43db87cbca995362f55f82fbd15fb1055ea87c40d6cd346551c134f2cea2cf7` |
| b 原始字节/LF | `07a70f5dd4378a043604916a3878f88365a3ccb593b35e5e955b0ce7b47d6c3a` |
| 合并稿原始字节 | `e511951476c61d0e71d6222cb8fa75786043ce5f78f10b5adac39aed8b178011` |
| 合并稿 LF | `ead60185a8b8207e98669e45fe5d49901dde883cfc2911cd012ffadb46e60086` |
| JSON 正文 | `19084c5b7aaf740e43ec87d41541453710cd73e66d085557df11ea683366f4f4` |
| 图片集合 | `2275cdccd5c21fc60d634ef7ca8d63299b642f25703cd83d1d4b028e68d38186` |

## 网页独审证据及结论

root 未参与本附录初译，已实际查看最终 40 张网页图：14 常规页和 26 公式/图片定点与横滑图。覆盖全部 D.1–D.10、图 D.1 的完整图注/译注、两模式首尾和独立导读、阅读位置保存/重载恢复以及真实引用跳转。本 reviewer 已阅读其正式报告，并逐一重算 40 张证据 SHA，全部匹配；记录在 `tmp/prml-review/appendix-d/root-ui-proof-verified.json`，没有声称重复目视 root 的整套截图。

一张快速定位采集帧中邻接 D.2 没有完成绘制，root 已用 D.1/D.2 的桌面/手机完整定点和 D.2 实际横滑证据核验，未将异常采集帧作为公式通过证据。没有持久显示缺失或待修项。另由本 reviewer 实际查看 D.3 两个导航落点。

本 reviewer 独立 XML 遍历确认 D 不含任何 mspace 节点，因此新增的仅保留 mspace.width 的阅读器分支不改变 D 公式；全书回归结论另见 `math-spacing-review.md`。源页、实际查看图片、源稿快照和守恒结果保存在 `tmp/prml-review/appendix-d/`。正文、图像、JSON 与网页独审均通过，无遗留问题；接受状态由 root 统一写入。
