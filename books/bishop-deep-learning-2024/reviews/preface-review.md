# 前言独立审查记录

## 覆盖与结论

- 以仓库根目录原书 PDF 的**物理第 5–10 页**（印刷页 v–x）为唯一正文依据，逐页查看 PDF 原页，并与 `chapters/preface.md` 对照。已核查全部标题、正文段落、跨页衔接、习题难度符号、书名与引文、两处网址、反馈邮箱、BibTeX 字段、数学记号、致谢名单和署名。六个 `pdf-page` 标记与原书页序一致。
- 原书前言无图片、表格、编号公式、正文脚注或项目列表。BibTeX 条目的键、作者、书名、年份、出版社均与 PDF 一致；致谢中的 62 位具名审阅者顺序齐全，重音符号在译稿中可辨。正文没有发现整句遗漏；85 处行内数学表达式均能由当前 KaTeX 转为 MathML。
- **结论：暂不通过验收。** 第 9 页 big-O 定义虽照原书抄录，却与标准数学含义相反，必须明示原书疑点；另有原书段落被拆开、绝对值解释易误导，以及数据向量的数学字体在当前转换链中未保持原样。当前站点尚未集成前言，正式阅读页的移动端和深色模式还不能验收。

## 需处理的问题

| PDF 物理页 | 译稿位置 | 问题与原页证据 | 建议 |
| --- | --- | --- | --- |
| 9 | `preface.md:82` | 原书写“$g(x)=\mathcal O(f(x))$ 表示 $\lvert f(x)/g(x)\rvert$ 当 $x\to\infty$ 有界”，译稿忠实照录。但标准 big-O 应检查 $\lvert g(x)/f(x)\rvert$ 是否有界。按原书说法取 $g(x)=x^3, f(x)=x^2$ 会错误地断言 $x^3=\mathcal O(x^2)$；原书紧随的 $3x^2+2$ 例子无法暴露分子分母颠倒。 | 把此处列入原书勘误，并在阅读页用清楚标明的简短说明给出标准定义；不要无说明地改写为仿佛原书原样如此。此项是原书疑点，并非初译误抄。 |
| 5 | `preface.md:9`、`:11` | PDF 的“Goals of the book”下从 *This expanding impact…* 到 *…known for decades* 是一个连续段落；原页 *future specialization. Due to the breadth…* 仍在同一段。译稿在“打下牢固基础”后分成两段。 | 合并为与原书相同的段落，同时保留全部现有文字。 |
| 6 | `preface.md:23`、`:25` | “Structure of the book”中原书第二段从 *A clear understanding…* 延续到 *…variety of backgrounds*；*The focus of the book, however…* 位于同段。译稿从“本书的重点”另起一段。 | 恢复原书段落边界。 |
| 6–7 | `preface.md:27`、`:31` | 原书从 *Conceptually, this book…* 跨页延续到 *…almost entirely non-Bayesian*，其中 *This means that…* 未另起段。译稿在“重新组织”后另起一段。 | 将跨页内容保持为同一阅读段落，`pdf-page: 7` 标记仍可保留作核对定位。 |
| 8–9 | `preface.md:78`、`:82` | 原书“Mathematical notation”最后一段从 *The symbol ∀…* 跨页到 *The notation g(x)…* 和下取整定义；PDF 第 9 页首的 *set. The notation…* 是上页段落的续文。译稿在页码注释后把 big-O 与下取整另起一段。 | 在处理 big-O 勘误时一并恢复段落连续性，保留物理页标记。 |
| 8 | `preface.md:74` | 原书将 $\lvert x\rvert$ 称为标量的 *modulus (the positive part)*，随后明确说也是 *absolute value*。译稿“即它的非负部分”容易被理解为正部 $\max(x,0)$；例如 $x=-2$ 时正部是 0，绝对值却是 2。 | 中文直接解释为“绝对值（总为非负的模）”，并将原书 *positive part* 的含混措辞记入勘误，不要让译文产生错误的数学定义。 |
| 9 | `preface.md:84` | PDF 用不同字形区分 $N$ 维数据向量与 $D$ 维变量向量；译稿写 `\boldsymbol{\mathsf{x}}` 与 `\mathbf{x}`。用当前 `scripts/tex_to_mathml.js` 实测，前者输出 `<mi mathvariant="sans-serif">x</mi>`，后者输出 `<mi mathvariant="bold">x</mi>`；前者的粗体属性丢失。 | 集成前确定可输出“粗体无衬线”数据向量的记法或渲染方式，实际查看网页并确认两种记号仍明确可区分且可复制。此项是渲染风险，不能仅以 TeX 源码看似正确判为通过。 |

## 已核对且无需修改的重点

- PDF 第 7 页的网站地址、反馈邮箱与六行 BibTeX 在译稿 `preface.md:33`–`:48` 中完整保留；`arXiv:YYMM.XXXXX` 与追加 `vN` 的格式在第 8 页对应 `:64` 准确。
- PDF 第 8–9 页关于向量、矩阵、转置、单位矩阵、拼接、期望、协方差、邻居集合、泛函、数据矩阵 $\mathbf X$ 与元素 $x_{ni}$ 的内容均在译稿 `:74`–`:84` 找到；除上述数学定义和字体问题，未发现变量或下标误抄。
- PDF 第 9–10 页致谢姓名、机构名、Jemima、Jenna、Mark、Antalya，以及两位作者署名、Cambridge 和 2023 年 10 月，均在译稿 `:88`–`:102` 对应位置保留。
