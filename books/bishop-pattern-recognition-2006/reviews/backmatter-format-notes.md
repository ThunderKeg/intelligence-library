# 书后材料格式与集成准备

root负责构建器、共享站点及验收元数据；各作者只写自己分片与图。以下是待实现内容的技术约定，不构成翻译或验收。

- 附录A步骤含独立显示式：分段有序列表保留start编号，公式独立块位于第2与第3步之间。无需把显示数学塞进li。
- 参考文献用`<p class="reference-entry">`，保留原书斜体，中文题名附原题，作者/出版信息完整。跨页同条目使用`join-previous-paragraph`（不加空格）或`join-previous-paragraph-with-space`（加一个空格）；后续p仍使用reference-entry。构建器已支持并保留em/a节点及continuedPdfPages。小型跨页夹具验证通过，第13章完整输出重新在内存生成逐字段相等。
- 索引用`<p class="index-entry">`和`<p class="index-subentry">`保留英文序、主次层级、strong页码与em斜体；不使用会丢内联强调的普通列表。希腊字母可用Unicode；原印页码由root最终转为可点击目标。
- 原书目录构建器已可读取条目上的本书内部href；目前源稿仍未添加跳转，不影响已验收文字。所有章节/附录/书后材料完成后，用当前块ID为285目录条目写入链接，保留标题/强弱/层级/页码，然后独立重新验收目录。
- app.js当前referenceMatches仅识别A–C，最终集成需扩展A–E；originalContents分支当前忽略href，最终补链接节点。共享文件最终修改前重新检查现状。
- 附录内容QA已扩展编号式连续覆盖和A–E图号唯一/完整覆盖；未编号图另由源页与图片清单独审。实际附录生成后运行。
- 最终登记本书公共书架、离线JSON/引用索引/图片清单，STIX字体加入CORE缓存；保留其他书的现有变更。全书独审后才能标完成。

- 部署清单额外检查：`.github/workflows/pages.yml`目前只自动复制chapter-*.json和assets，其他JSON仅列出Deep Learning/Sutton。因此最终必须为PRML增加frontmatter/preface/notation/contents、appendix-a–e、references/index/reference-index/offline-images的精确复制循环，避免本地可读而部署缺失。现阶段仅记录，未改共享工作流。
- 全书术语初查候选在`terminology-scan-before-final.json`：第8章Dirichlet分布/先验与第2/10章中文名不一致；生成/判别模型是否统一“式”需全书审查定稿；Jacobian与雅可比需按全书首次定义统一。所有14章均只有一个独立导读。原目录与已验收节标题的32处差异记录于`contents-title-consistency-pending.json`，最终对齐已审标题再独立复核。
