# 索引原页预读基线

root已实际查看PDF749–758全部10页（5张双页图）；758右栏为空，但该页左栏有大量索引项，不能算空白页。原图在tmp/prml-root-review/appendix-index/。尚未翻译或独立验收。

- 源索引按英文词顺序、每页先左栏后右栏。保留全部主条、缩进子条、see交叉参照、页码与粗体页码。749开头说明：粗体页码表示该主题的主要信息来源；此含义必须保留，不能把页码都转成同一种字重。
- 使用中文词条并保留英文术语用于对照；维持原书顺序，不按中文重新排序或合并相近词条。原书同时收录“independent identically distributed”和“independent, identically distributed”，也分别收录latent/hidden等别名，均保留。
- 原页码是书上印刷页码，正文物理页=印刷页+20；罗马页码vii对应前言PDF7。应保留原页码文本，并在集成时链接到本书相应原页的正文块；不要把显示页码改成PDF物理页。see项链接到对应索引主题。
- 多层项例：covariance/covariance matrix；Gaussian的conditional/marginal/ML/mixture等；graphical model多子项；hidden Markov model多子项；mixture model；neural network；principal component analysis；probability；prior；support vector machine。子项不能提升成无上下文独立主条，也不能丢掉。
- 跨栏层次：752左栏graphical model的最后子项在同页右栏开头“undirected”；756左栏probability的子项续到同页右栏开头“sum rule/theory”。长条的换行也需回接，例如753右栏首iterative reweighted least squares的多页码续行、757右栏首statistical learning theory的see续行。不要把相邻的不同主条误合并。
- 首项1-of-K coding scheme，末项Yellowstone National Park。所有数字、希腊字母、K/ν/ε及书目人名仍须按原页核对。没有图表、显示公式、习题、脚注或章首装饰图。

站点已支持<p class="index-entry">和<p class="index-subentry">的富文本条目与缩进，可按原主条/子条使用；页码用strong精确保留粗体，英语中变量可用em及Unicode希腊字母。不要使用当前会丢字重的普通列表。最终页码/see链接由root集成。拆分可取749–752 / 753–758；首段的索引使用说明由a翻译。独审须检查每项文字、层级、see目标与所有页码，不以机器计数代替原页核对。

后续逐条核对更正：PDF753右栏首原印为 iterative reweighted least squares，已由作者b及root实际查看4倍原页确认；与IRLS的see名称一致，无需别名映射。预读时漏记re仅在本基线中纠正，不据提取文字改变原条。
