# 本书译稿格式

只在分配给自己的文件中编写。正文唯一依据是仓库原 PDF；`source-inventory.json` 和 `tmp/convex/text/` 只是待核对候选与提取辅助，不代表原页、语义或完整性已经审查。原页 PNG 放在 `tmp/convex/pages/`，不得用于阅读页配图。`tools/qa_reader.py` 由集成 Agent 单独维护。

## 文件与页码

- 正文章节：`translation/chapter-01.md` 至 `chapter-11.md`；附录：`chapter-A.md`、`chapter-B.md`、`chapter-C.md`。
- 其他单元：`frontmatter.md`、`contents.md`、`preface.md`、`part-I.md`、`part-II.md`、`part-III.md`、`appendices.md`、`references.md`、`notation.md`。
- 上述 23 份源稿是 `tools/common.py` 中 `CHAPTERS` 明确列出的唯一构建输入。`figure-fragments-*.md` 是保留用于核对交接与审查历史的初稿片段，首注亦标明不是阅读章节；其中尚未吸收的后续措辞或字形修正以正式章稿为准，不得重新覆盖已验收章稿。
- 输出一律为本书目录下的 `chapter-<ID>.json`，例如 `chapter-frontmatter.json`、`chapter-A.json`。保留原书顺序，不按目录书签机械切章：附录分隔页是 PDF 645，References 从 PDF 699 开始。
- 每单元一个 `#`；原节、小节、次级标题依次用 `##`、`###`、`####`。保留原编号。无编号标题也保留对应层级。
- 报告一节完成前，须看到下一节标题的实际原页位置；若标题从页中开始，其上方的前节续文仍归前节，不能按页尾或书签提前结束。
- 在每个物理 PDF 页的译文起点写 `<!-- pdf-page: 15 -->`。编号从 PDF 第一页起算，印刷页 1 对应 PDF 15。包括空白页标记，不添加虚构阅读内容。同一原段跨页时，可把标记放在段中；编译器保留整个段落，并将下一块归到新页。
- 各章和附录正文前加入短导读：`<aside class="chapter-guide">导读（编者）：……</aside>`。导读用纯文本，并明确与原文分开。

## 公式、表格、代码与脚注

行内公式用 `$x_1^2$`。行间公式独占一块，原编号用 `\tag`：

```tex
$$
\begin{aligned}
\text{minimize}\quad & f_0(x) \\
\text{subject to}\quad & f_i(x)\leq b_i,\quad i=1,\ldots,m.
\end{aligned}
\tag{1.1}
$$
```

每个显示公式至多一个原编号；无编号公式不要添加编号。编译器通过仓库固定版本的 KaTeX 生成 MathML，保留 `data-tex` 与标准 TeX annotation，编号位于可滚动公式外侧。不要把公式渲染成图片，也不要改写原符号。需要原行间对齐时用 `aligned`、`array`、`cases` 等合法 TeX。

表格使用 Markdown 表格或语义 HTML `table`，逐格核对。宽表格自动横向滚动；原目录的两列表格单独适配窄屏。数值简单的少列表格使用 `style="min-width:0;width:100%"`，确保窄屏同时显示各列；第 4 章四资产表采用这一方式。代码用有语言标识的围栏块，代码中的 `$` 不会被当作公式。列表用标准 Markdown。脚注可用 `[^note-id]` 与 `[^note-id]: 脚注正文`；保留原脚注标记与相应引用，复杂原脚注也可用显式 HTML。

原书算法用 `div.algorithm` 与 `markdown="1"` 保留标题、给定条件、循环、步骤及终止条件；用文本、列表和数学表达，不转为图片。算法与例、注使用本书局部样式保留上下边线。字母小问之间留空行，续段与行间式保持四空格缩进，并检查实际生成的 `li` 归属；仅检查公式能否编译不能发现列表吞并。

## 图片与图内文字

必须保留完整图形并翻译图注、全部图内英文。图片保存在本书 `assets/` 下；支持 PNG、JPEG、WebP，以及不含外部图片或主动内容的 SVG。使用如下 HTML（`data-figure` 为原图编号，非编号徽记等可省略）：

```html
<figure id="fig-2-1" data-figure="2.1">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/figure-2-1.png"
     alt="说明完整图形含义的中文替代文本"
     data-source-page="36" data-source-rect="106,120,464,350">
<figcaption>图 2.1 原图注的完整译文，公式可用 $x$。</figcaption>
<p class="figure-translation">图内文字：原词一——译文一；原词二——译文二。</p>
</figure>
```

`data-source-rect` 为 PDF point 坐标，原点在页面左上角，顺序为 `x0,y0,x1,y1`；务必先查看原页再定范围。裁剪工具可自动写同名 `.source.json`，此时 `img` 可省略这两个来源属性：

```powershell
python -X utf8 books/boyd-vandenberghe-convex-optimization-2004/tools/crop.py --page 36 --rect 106 120 464 350 --output books/boyd-vandenberghe-convex-optimization-2004/assets/figure-2-1.png
```

裁剪工具拒绝覆盖现有图片，并拒绝整页或接近整页的矩形。数值检查不能证明裁剪内容完整，仍须对照原图审查。若图形确实没有需译的英文，可在 `figure` 写 `data-no-english-text="true"`，并由独立审查确认；数学符号、刻度与图形内容仍须保留。HTML 块内若要使用 Markdown 的段落、列表等，添加 `markdown="1"` 并留空行。

原书确无独立图注的插图（例如习题 3.2 的两幅等值线图），使用 `data-uncaptioned="true"` 并保留上下文题干，不虚构图注或图号。仍须完整图片、中文 alt 与来源坐标，并在独立审查中核实原书确无图注。

原书浮动图插在跨页句子中间时，源稿和页标记仍按 PDF 顺序保留。可为 `figure` 加 `data-reader-after="目标段落id"`，并给后面的完整说明末块添加对应 `id`。构建器仅把明确标记的图片移到该块后，保留图片之间的原顺序，以及移动前各块的原页归属。图与目标必须是同一容器内的直接兄弟元素：允许章级或同一个 `example`／`remark`／`exercise`／`algorithm` 框内，目标必须唯一且位于后方，不能跨容器移动。

同一个原段或无序列表被浮图分断时，前段用 `<p id="前段id">` 或 `<ul id="前段id">`，后段用相同元素并加 `data-reader-continue="前段id"`；需要 Markdown 时同时加 `markdown="1"`。先将图显式移到后段之后，构建器才把后段接到前段。两段之间仅允许空白和原页标记，不能跳过其他正文、标题或图。后段若有 `id`，仍以段内或首个列表项内的空锚点保留；数学、文字、列表项和页标记不得删除。该机制只用于原书同一段／列表的续接，不合并独立段落。示例与防护回归见 `tools/test_build.py`。

若原书浮图落在后一则例题的续页，但图注明确属于前一则例题，可为图添加 `data-reader-owner="所属例id"`。此规则仅允许把后一例中的图归到紧邻的前一个同级 `div.example` 末尾，且前例正文必须确实引用该图；不允许跳过例题或标题，也不能同时使用 `data-reader-after`。例如图 7.3 的图注引用 (7.8)，内容属于例 7.2，尽管原图印在例 7.3 的续页。必须先对照原页确认，并由独立审查者检查生成后的归属；原稿、图片来源页、裁剪坐标和各例的文字都保持不变。

若章级图片因原书浮动排版插入后续例／注的续页，可用 `data-reader-after-container="该框id"`，让完整例／注先读完，再在框外显示该图。图必须是这个框的直接子元素，目标必须就是自身所属框，框前紧邻段落还须明确引用该图；不能与另外两种移动属性混用。图 8.12 展示注 8.1 前的 logistic 分类例子，但原图插在注 8.1 最后一句之前，属于此情形。此规则不移动其他文字、数学或来源页。

原书后置浮图落入下一节、但实际属于前一节时，可用 `data-reader-after-previous="目标段落id"` 把图放回前文的完整说明段后。该规则仅接受章级图和同层的唯一 `p`，目标必须位于原图之前并明确引用该图的精确编号；不能以标题、公式、例框或将被合并的续段为目标。目标位置与全部图的原有相对顺序必须一致，不允许跨容器或混用多种移动属性。源码仍按原 PDF 页序保留图片和页标；构建器在移动前记录来源，移动不改变图注、图内文字、图片路径、坐标或物理页。第 10 章图 10.1–10.7 使用此规则，图 10.8 仍用向后移动的 `data-reader-after`。

章级浮图实际属于前文算例、但中间隔有证明文字时，可用独立的 `data-reader-return-to-example="例框id"` 返回该例末尾。目标必须是原图之前唯一的章级 `div.example`，且其直属段落必须明确引用精确图号；不能越过一级至三级标题或其他例、注、习题、算法框。图号必须合法且唯一，五种移动属性互斥，移动后仍保持全章原图顺序及原页信息。第 11 章图 11.2 使用此规则；既有 `data-reader-owner` 仍只处理紧邻例框，不扩大其适用范围。

若直接引图的段落还引出后续模型或参数式，返回浮图时可另用 `data-reader-citation="直接引图段落id"`，把图放在这组模型说明的完整结尾。此附加属性只与 `data-reader-after-previous` 合用；引用段和目标段都须是唯一的章级段落，前者在后者之前，且明确引用精确图号。从引用段至目标段仅允许连续的普通段落与行间公式，不得越过任何标题、框、列表、表格或其他图片。无此属性时，目标段仍须自己引用图号；不得改写原文或增补引用来绕过守卫。第 11 章图 11.10／11.11／11.14 使用此规则。

本书使用随书提供的 STIX Two Math 字体，确保多行矩阵括号可伸展；源文件、版本及许可证在 `assets/fonts/`，样式仅作用于本书。显示公式保留外层横滚，中文公式标签保持不换行。无需改动共享站点样式。

`assets/reader.css` 是本书样式源。编译器同步将其嵌入章节首块，并调整字体相对路径，使阅读器恢复进度前已应用本书样式。修改该 CSS 后须重建已生成章节并检查进度恢复；作者译稿中仍禁止任意 `style` 或 `link` 元素。

构建器把 MathML `columnalign` 显式映射到单元格 CSS，保留标准值并提供浏览器兼容值，使 aligned 的左列右对齐、右列左对齐，矩阵单元格居中。`qa_reader.py` 检查实际几何位置，不能仅以 TeX 编译成功判断公式排版正确。

浏览器未必实现 MathML 的 `script`／`bold` 字形变体。构建器把这些叶节点转换为对应的 Unicode 数学字形，并用 `data-source-glyph`／`data-source-mathvariant` 保留转换前信息；普通斜体与运算符保持原样。对叠置算符，仅移除妨碍浏览器布局的单子元素 `mo` 包装，并保留原结构供逆向核对。两种兼容处理均不改写 `data-tex` 或 TeX annotation，须检查实际字形、上下位置及整章逆变换后的内容相等性。

按原页使用粗体的具名算子可写成 `\operatorname{\mathbf{dom}}`，以保留算子间距。KaTeX 会为此生成嵌套的 `mi > mrow > mi`，构建器仅将完整的粗体 ASCII 字母序列合成一个标识符，并用 `data-source-operator-mathml` 保存原结构，再应用上述字形兼容；后继函数应用符 U+2061 保持原样。此规则不改变普通体算子、变量、上下标或原 TeX。不得根据名称批量猜测粗体：例如 `sign` 在原书不同位置有不同字形，信赖域下标 `\mathrm{tr}` 也不是迹算子。

原生 MathML 把 U+2061 显示为零宽。在上述受控算子后继为普通或内部数学项时，显式给应用符设置 `rspace="0.1667em"`，保留 TeX 的窄间距，避免 `dom f` 黏连；后继为括号、分隔符、显式空格或没有参数时不添加。`data-source-operator-spacing` 保留原应用符，源 TeX 不变。原页字形、KaTeX HTML 的间距分类、最终浏览器几何与逆变换相等性须分别核验。

带上下标的算子若整个基底恰为上述名称及应用符，例如 `epi_K f`，间距加在完整的 `msub`／`msup`／`msubsup` 后，用 `data-source-operator-script-spacing` 标记新增 `mspace`；不得在基底内部加间距而把下标推开。

## 构建与客观核对

书末参考文献逐条保留引用键、全部作者、作品原题名、刊物／出版社、年份、卷期、页码、版次和原附注；作品标题提供中文译名并附原题名，方便核对与查找，作者和刊物／出版社名称可保留原文。不可将排版换行造成的断词连字符误作作品名称的一部分，也不把原书旧网址改成未经核准的新网址。引用键中的附加符号须回看原页，例如 `Bjö96`、`Löf04`、`Löw34`、`Pré71`，不能沿用 PDF 提取后的分离字形。书后预检在 `tmp/convex/backmatter-preflight.md`，仍需独立逐条审查。

从仓库根目录运行，只指定自己拥有的章节，避免覆盖他人的 JSON：

```powershell
python -X utf8 books/boyd-vandenberghe-convex-optimization-2004/tools/build.py 01 --check --report tmp/convex/chapter-01-structure.json
python -X utf8 books/boyd-vandenberghe-convex-optimization-2004/tools/build.py 01
python -X utf8 books/boyd-vandenberghe-convex-optimization-2004/tools/validate.py 01 --report tmp/convex/chapter-01-consistency.json
python -X utf8 books/boyd-vandenberghe-convex-optimization-2004/tools/test_build.py
```

`--check` 不写 JSON；`--partial` 只供未完稿，允许缺页标记并明确报告缺口。默认构建只处理已有源文件。`validate.py` 不指定 ID 时核对所有单元，缺少源稿或输出即报告未完成的结构缺口。公式与图编号差异是“需要回看原 PDF 的候选差异”，不得据此宣称语义错误，也不得因无差异就宣称译稿完整。构建和验证都不会把任何章节标成完成，最终状态由独立审查、修复和网站实测共同决定。

章节编译后运行 `tools/link_references.py`，为已经存在的目标加入静态引用链接；可显式传入各章 ID 以限定当前稳定文件。该步骤保留每个可见字符和 MathML 节点，且幂等；`--check` 只核对是否需要重建。引文方括号内的章、节等细节属于被引著作（如 `[BTN01, §4.3]`），只链接书目键，不把该节误连到本书；相关回归见 `tools/test_link_references.py`。重建章节后须重新运行链接步骤。`validate.py` 会在剥离这些自动链接后对比源稿，结构相符不等于译文审查通过。

参考文献题名中的部分、章、式等编号属于被引作品，不触发本书编号链接；上标加号仍属于书目键本身。无编号标题开头的数学变量（例如 `$A$ 最优设计`）不作为附录编号，只有 `A.1`、`7.5` 等带点编号进入小节编号字段。

`tools/offline_manifest.py` 从全部阅读单元的图片引用生成 `offline-images.json`，逐文件哈希构成缓存版本；使用 `--check` 核对现有清单，用 `--report <路径>` 导出图片哈希台账。数学字体作为站点核心离线资源登记，不混入图片清单。

重建源清单：`tools/inventory.py`；已经目视确认的提取漏项另存 `source-inventory-corrections.json`，重建时按原 PDF 哈希校验并补入，不能因提取器遗漏而删除原书内容。原页渲染：`tools/inventory.py --render-only --render 7-15,644-647,698-699`，可用 `--render all`。这些工具只提取、编排或检查文件，不调用本机模型或翻译服务。
