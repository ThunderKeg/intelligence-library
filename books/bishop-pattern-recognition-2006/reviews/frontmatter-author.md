# 卷首初译记录

作者：主 Agent。状态：初译完成，独立审查与浏览器验收待完成；不代表全书完成。

- 范围：PDF 物理页 1–20；卷首 1–6、前言 7–10、数学记号 11–12、目录 13–20。
- 逐页渲染：`tmp/prml-front/page-001.png` 至 `page-020.png`；每两页合图供原页对照。页面 10 经视觉检查为空白，仅保留页标。
- 原图：封面、Springer 标志、日食合影均从 PDF 内嵌图像直接提取；没有用整页正文截图替代译文。源 xref 分别为 5762、19、34。
- 前言：全部致谢姓名、习题难度与 www 标识说明、原书网站和配套书计划保留。内容以这份 PDF 的出版时间叙述为准。
- 数学记号：核对 PDF 字体；观测向量与数据向量不同，后者用粗体无衬线 MathML。原文的大 O 定义保留，即 `|f/g|` 有界，不静默改成常规定义。
- 原书疑点：PDF 3 的 Wallace 书名实际印为 `Minimum Massage Length`。英文保留，中文按技术语义译为“最小消息长度”。请独立审查判断是否需要译注。
- 原目录：逐页核对标题、层级及印刷页码。PDF 16 目录列有第 7 章习题，印刷页 357，原 PDF 书签漏列；任务清单须补入。
- 编译：`python -X utf8 books/bishop-pattern-recognition-2006/tools/build.py frontmatter preface notation contents --preview` 成功；四部分 JSON 均保留 `draft-unreviewed`。
- 未完成：独立审查、目录跨章实际目标验证、移动端/深色模式、全书一致性检查。
