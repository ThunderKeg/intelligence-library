# 公共集成与离线验证的独立代码审查

审查者：Agent a。本记录先覆盖 `tools/qa_offline.py` 和 `qa_reader.py`、`qa_content.py` 新增的 `--report-name` 范围。仅作只读代码审查，未修改译稿、图片、共享文件或检查工具；未把静态推导的反例称为已在正式网页复现，也未宣称执行了最终离线浏览器验收。

公共 `books.js`、`sw.js`、Pages workflow 与 README 的本书增量，以及多书实际烟雾检查，将在 root 通知补丁完成后另行审查。其他书包括并发更新至 41 章的 MacKay 均不在本轮修改范围。

## 离线检查初审发现

以下行号对应初次读取的 `qa_offline.py`。各项已向 root 发送精确位置及反例；root 已修复，后续只读复核见下文。

| 编号 | 优先级 | 位置 | 可误报成功的反例 | 所需检查 |
| --- | --- | --- | --- | --- |
| PI-01 | P2 | 40–57 | 缓存中的章节 JSON 与本地文件字节数相同，但一个数学运算符 `+` 被改成 `-`；标题、块数、MathML 数量保持相同。现有长度/数量断言不能区分两份内容，资源仍可被当成完整已核版本。 | 缓存内容和断网后 fetch 内容分别与本地对应文件的 SHA-256 比较，保留 HTTP 状态和 Service Worker 来源检查。 |
| PI-02 | P2 | 74–76、84–85 | 渲染器保留每个 figure 的 `.reading-block`，却漏掉其中所有 `img`。现有块数和数学断言不受影响，图片循环为空，没有 `.figure-error`，因此缺图仍能通过；报告只记录少了的图片数而不失败。 | 从 compiled 块得到预期图片实例，核对数量和有序 src，再逐张 decode。 |
| PI-03 | P3 | 28、67–83 | 浏览器偏好设为 dark，但应用仍把 `html[data-theme]` 设为 light。脚本未断言实际主题，其他内容和几何条件可以全部通过。 | 核对实际 `html[data-theme]` 与所测试模式一致；报告准确注明只有这一种离线视口/模式。 |
| PI-04 | P2 | 71–73 | 25 个目录链接数量不变，但前后章导航都错误指向 chapter-01；当前章 href 只需以 `#read-` 开头，甚至可指不存在的块。脚本逐章通过直接 `page.goto` 加载，仍能得到正确内容，因此不会发现这些导航目标错误。 | 用 inventory 顺序核对目录/前后章预期 href，验证当前章目标真实存在。若没有实际点击，应明确这些是目标断言、逐章直接导航，而不是前后章链接点击验收。 |

初版已经提供的有效检查包括：新 context 中注册并等待 Service Worker 控制、等待离线面板 complete、列出的本书资源缓存存在、断网 fetch 成功、25 个单元逐一直接加载、响应来源于 Service Worker、书标识及 H1、块与数学数量、现有图片可解码、字体加载与横向溢出。上述四项不否定这些已有断言，只指出其不能排除的具体假阳性。

### 修复后的只读复核

PI-01–04 的所述反例均已被新增断言覆盖，现关闭：

- PI-01：本地逐资源计算 SHA-256；缓存正文及断网 fetch 正文都由 Web Crypto 计算 SHA-256，再逐资源与本地值相等比较。原 HTTP 状态、字节数及 Service Worker 来源检查保留。
- PI-02：预期图片取自 compiled 中全部嵌套 figure，先把页面有序图片绝对 src 列表与预期列表作精确相等比较，再逐张解码；缺图、重排或错误 src 均不再能靠空循环通过。
- PI-03：逐章断言 `html[data-theme] == dark`。这仍是 390×844 深色这一种离线模式，不表示离线浅色/桌面也执行过。
- PI-04：当前章条目必须唯一，href 精确匹配 compiled 的首个目录块，文字匹配公共目录集成计划；前后章 href 有序列表精确匹配 inventory 相邻单元。只读核对该计划与 inventory 的 25 个单元 ID 顺序一致。原反例中前后章均指 chapter-01 会失败。覆盖范围仍是逐章直接导航、当前项/相邻链接目标检查；没有把未点击的链接宣称为点击通过，也没有逐项断言每个非当前目录项的 href。

上述是依据当前代码和真实本地产物的审查结论。最终实际离线浏览器任务由 root 执行，本审查者未另行启动。

## 报告命名增量

`qa_reader.py` 的 `--report-name` 在执行前限定为 `[a-z0-9-]+\.json`，将路径固定在本书 `reviews/` 下；未提供时继续原有 units/suffix 命名。`qa_content.py` 在写出前使用同一完整匹配白名单，未提供时继续原有命名。新参数只选择报告文件名，不绕过原检查、缩减单元列表或提前写成功报告。此次范围内未发现报告命名导致误报成功或路径越界的问题。文件名白名单是代码检查结论，本轮未额外执行这些完整浏览器或结构任务。

## 阶段状态

- [x] 只读检查三项指定范围，给出问题位置和反例。
- [x] 向集成 Agent 回传 PI-01–04。
- [x] 复核离线脚本修复并固化当前代码指纹。
- [x] 只读审查 root 尚未应用的四文件公共集成提案，确认本书增量及他书文本守恒；实际应用后的复核仍待通知。
- [x] 多书实际烟雾检查及其结果记录；PI-07/08 由 root 修复后独立复验，见下文最终结论。

本记录不作为全书内容验收、最终离线验收或其他书验收的替代材料。

## 当前已审工具指纹（raw SHA-256）

| 文件 | SHA-256 |
| --- | --- |
| tools/qa_offline.py | `78cff7debd0e2e922549cf4867ea9d4c59c9b83e23f92777af5962cef8de1234` |
| tools/qa_reader.py（仅 report-name 增量） | `12230b761c7bdf936c5d7d7f46b90002facc76e694abfc32c723dbf3b905db2d` |
| tools/qa_content.py（仅 report-name 增量） | `968e2913e3c13602e23c9f14794764c94e86b7ae2b999ae2aa663edeeb75c8e6` |

## 尚未应用的公共集成提案

已只读审查 `tmp/prml-global-review/public-proposed/` 中四文件提案、manifest 及 `../prepare_public.py`，公共原文件尚未由本轮提案改写。

1. **PI-05（P2，已修复并复核）——提案指纹与实际字节不符。** 初版生成器对 LF 字符串计算 `proposedSha256`，却用 Windows 默认 `write_text` 写成 CRLF，四份提案实际 raw SHA 均不相符。root 改为显式 LF 写出，对实际 `read_bytes()` 计算指纹，并另记 `proposedLfSha256`。当前逐文件确认源文件 raw/LF、提案 raw/LF 四项均与 manifest 完全一致。
2. **PI-06（P3，已修复并复核）——README 的后两条工具路径省略书目录。** 初版段落先给仓库根下完整 build 命令，却随后只写根目录不存在的 `tools/indexes.py`、`tools/verify_book.py`。现三条命令均明确 `python books/bishop-pattern-recognition-2006/tools/...`，路径实际存在。

当前提案仅含约定增量，未发现未关闭问题：

- `books.js`：用 Node 解析旧、新目录并比较数据对象。仅增加 PRML，四本原书的数据与顺序完全相同；目录由 4 本变为 5 本。本书 25 单元与计划和 inventory 同序、路径存在。MacKay 仍为 62 个阅读单元，含第 41 章及 `41-postscript`，没有回退到旧版本。
- `sw.js`：仅向 CORE_ASSETS 插入 28 项，即 25 单元 JSON、引用索引、离线图片清单及本书数学字体。逐项与计划相等、路径全存在；剔除 PRML 后旧缓存条目和顺序完全相同。Service Worker 处理器未改。两份 JavaScript 均通过 Node 语法解析。
- `pages.yml`：仅新增本书 13 个非 chapter JSON 的复制循环，恰为卷首四单元、附录五单元、参考文献、索引、引用索引和离线清单。14 个 chapter JSON 及全部图片/字体由原有 find 规则覆盖；当前本书 370 项离线所需资源都存在且被上述规则涵盖。未执行正式发布工作流，也未新增发布其他私有源文件的规则。
- `README.md`：仅新增一段本书说明和一个空行，原有 MacKay 第 1–41 章等描述完整保留。段落中的完成/全书离线说明为拟应用后的状态，仍须依据最终实际验收再应用。
- 将每份文件按 LF 归一化后逐行 diff，仅有插入：books.js 162 行、sw.js 28 行、README 2 行、workflow 5 行；没有删改其他书内容。当前公共原文件 raw SHA 仍与提案生成时一致。若应用前他人有新增，必须重新以当时公共文件构造并核对增量，不能用这份快照覆盖新内容。

### 当前提案指纹

以下均为已核实际文件 raw SHA-256，提案使用 LF，因此与其 LF 指纹相同。公共实际应用和浏览器烟雾检查尚未进行。

| 提案文件 | SHA-256 |
| --- | --- |
| books.js | `49f9673162c5b632cd69f3675794d4aa203e3143257189fe2378f1fb2d3a72f5` |
| sw.js | `c1526ee68dc9103e85b629ef486e7680bf01801fb9dc6ccdd075c88f2fcfe164` |
| README.md | `a4686fe8c9702d8a51e9cf46b20e9e3dedc82ed3681f295b2e0c3133ac1ee62d` |
| pages.yml | `79aec0c73f819f14a64d42ae4df8c82e85e48a330914ca18689634c50c42a43c` |

## 原目录顶层页码粗体样式的追加复核

已只读复核 `styles.css` 第 194 行：`#reader-article[data-book-id="bishop-pattern-recognition-2006"] .original-contents strong.contents-title + .contents-page`。选择器必须同时满足本书 article 标识、原目录容器和相邻的 strong 标题，因此不会影响 MacKay、Bishop 2024、Shannon、Sutton 或其他书。`app.js` 对 originalContents 的实际构造顺序为 strong/span 标题后紧接 `.contents-page`；即使标题内部包有链接，两者仍是相邻兄弟元素，选择器匹配不变。

当前 contents JSON 中 285 项恰有 24 项 `strong: true`，且全部为 depth 0；其余 261 项采用 span 标题，不匹配新增规则。字体粗细改为 700、文字色改为主题变量 `--ink`，作用仅为这 24 个顶层页码。此次仅做选择器与结构/数据匹配复核，未代替 b 的原页粗体依据和最终目录截图验收。当前 styles.css raw SHA-256 为 `c1bb596e2f365c4bbda6e7f07430be9a98ff4944417b9b9e9471a5d12ae78f09`，范围仅这一条新增规则。

## 审查链校验与公共提案基线的追加复核

已只读复核 `verify_book.py` 新增的审查链检查。当前 review 的 `renderingAddenda` 和 `structuralAddenda` 均逐个验证文件存在；每个 `previousReviews` 项必须仍是 `accepted`，原记录及原 `renderingAddenda` 也必须存在。原有当前译稿、渲染内容、图片指纹校验和 chapter 的审查记录一致性检查没有被替换或跳过。

独立执行从当前工具 AST 提取的这两段检查，确认 25 单元现有记录通过；其中第 4、5、6、8、12、13 章和参考文献这 7 个重绑单元都各保留一份原 accepted 记录，相关原附加审查文件也全部存在。再仅在内存副本中分别加入缺失 structuralAddenda、把原审查状态改成 draft、换成不存在的原记录、加入缺失的原 renderingAddenda，四个反例均被拒绝。没有调用工具 main，没有覆写正式全书验证结果。临时证据为 `tmp/prml-public-a-review/review-chain-proposal-refresh.json`。

这项检查验证已经记录的状态和文件存在性，不自动判断记录的语义、重新验收旧稿，或根据文件存在就认可内容。它只遍历已有的 previousReviews，不证明未登记的历史审查是否齐全；本轮另外直接确认了上述 7 份历史链实际仍在。当前历史项没有嵌套 previousReviews 或 structuralAddenda，因此本轮没有把未实现的递归历史检查宣称为通过。此增量在约定范围内无待修问题。

`prepare_public.py` 现先对四个公共原件各调用一次 `read_bytes()`，后续 LF 归一化、source raw 指纹和 `before-*` 快照都来自同一个内存值。新 manifest 的 `sourceFile` 可以追溯到该精确原始字节快照，消除了准备过程中再次读取原件造成基线混配的风险。实际应用时仍需对比当时公共原件；提案生成后发生的并发新增不由此步骤锁定。

本轮重新逐文件核对 manifest：before 快照 raw/LF、提案实际 raw/LF 四项指纹全部相符，检查当时四份公共原件也仍与 before 快照逐字节相同。LF 差异依旧只有 PRML 插入：books.js 162 行、sw.js 28 行、README 2 行、workflow 5 行。用 Node 重新解析前后 books 数据并剔除 PRML 比较，四本原书的数据及顺序完全一致；MacKay 已由上次审查时的 62 个单元增加为 64 个，末尾为 `40`、`41`、`41-postscript`、`42`、`43`，刷新提案完整保留了并发新增。临时结果为 `tmp/prml-public-a-review/catalog-refresh.json`。

本次复核后的 raw SHA-256 如下；尚未应用公共提案，也尚未进行多书实际浏览器烟雾检查。

| 文件 | SHA-256 |
| --- | --- |
| tools/verify_book.py（仅上述增量） | `cccb349c22e6c24534e97c509286dd4f5fffa0a3634557bcb8c82159e10f0181` |
| tmp/prml-global-review/prepare_public.py | `01c0cd96cd89d6eb972dd4f48ca7a30af6ad69d2c48aec1587425ce7d44059e3` |
| 刷新提案 books.js | `3d5be645f1aeb538929ecf4e9dba5f9e7f3d5a264dc7d0c37e630f77446dcb8a` |
| 刷新提案 sw.js | `c1526ee68dc9103e85b629ef486e7680bf01801fb9dc6ccdd075c88f2fcfe164` |
| 刷新提案 README.md | `d0b9612c3ffc9943ecd8263fe75608295eb6d76fb166b55aeb7badc2f0b870f1` |
| 刷新提案 pages.yml | `79aec0c73f819f14a64d42ae4df8c82e85e48a330914ca18689634c50c42a43c` |

## 实际应用后的公共文件复核

已读取 `reviews/public-integration-application.json`，将四份 `before-*` 原始快照、当时提案的实际字节及 appliedRawSha256 逐项核对，全部相符。应用时的差异仍只有前述 PRML 插入；原有四本书的对象和顺序完全保留。本书实际对象与 `catalog-integration-plan.json` 精确相等，含全部 25 单元。

应用后 MacKay Agent 继续追加了第 44 章、`45-prelude`，并更新对应说明。最终烟雾绑定的 books.js 为 `db687b8a…2685`，其中 MacKay 有 66 单元；原 64 单元前缀逐对象、逐字段和顺序保持相同。其他三个原有图书对象及 PRML 对象不变。README 后续仅更新了两处 MacKay 进度说明，PRML 新增段落完整保留。这些并发追加与 PRML 接入增量分开记录，没有用提案覆盖后续工作，也没有扩大为新章内容审查。

公共发布清单复核通过：SW 中本书恰有 28 个预缓存路径；workflow 的 13 个非 chapter JSON 复制项精确匹配本书所需项；其余 14 章 JSON、342 幅图片和数学字体由既有规则覆盖。370 项必要资源都存在并被规则涵盖。此项是本地路径和规则核对，没有执行 GitHub Pages 发布，也没有把本地服务器能访问所有文件等同于正式发布成功。

证据：`tmp/prml-public-a-smoke/applied-public-verification.json`、`catalog-final-verification.json`、`compat-and-readme-final-verification.json`，以及测试时的 `books-current-snapshot.js`、`README-current-snapshot.md`。首个 applied-public-verification 记录的是加入第 44 章时的中间快照，后续以 catalog-final-verification 和下表绑定测试版本。

## 实际烟雾发现的旧式公式兼容问题

| 编号 | 现象与定位 | 最终修复及独立复验 |
| --- | --- | --- |
| PI-07，P2，已关闭 | 书架进入 Shannon 的 chapter-00 或从目录进入 chapter-01，均实际触发 `Cannot read properties of null (reading 'scrollWidth')`。栈为 `app.js:674 updateFormulaHints → startTracking`。该书 rich HTML 使用直接含 math 的 `.book-formula`，没有内部 `.formula-scroll`，导致进度初始化中断。 | root 将 scroller 改为内部 `.formula-scroll` 或 formula 本身。最终两页、两模式均无 JavaScript 错误，4 次进度存储与刷新恢复实测通过。 |
| PI-08，P2，已关闭 | PI-07 临时 guard 消除异常后，390 深色模式仍在 Shannon chapter-01 的 `read-p02-b004` 发现宽公式撑出正文：viewport 390，document.scrollWidth 540。 | root 仅为 `.reading-rich .book-formula:has(> math)` 增加 `overflow-x:auto`，并让提示逻辑使用该旧容器。实测容器 clientWidth 342、scrollWidth 530、scrollLeft 可到 188；提示可见、tabIndex 为 0、可取得焦点，页面宽度保持 390。已实际查看左右两端截图。 |

两项是本次兼容烟雾发现的既有问题，不归因为 PRML 新增正文或接入记录。已直接读取 Git HEAD，确认原提示循环及未判空的 scroller 访问原已存在。对 root 保存的修前快照反向比较，最终 app.js 只有 scroller 回退这一行变动，styles.css 只有上述限定选择器这一行新增；没有修改任何书的正文、公式内容或图片。原诊断保存在 `tmp/prml-public-a-smoke/all-formula-diagnostic.json` 和 `shannon-mobile-overflow-diagnostic.json`，失败阶段截图分别保存在 `before-pi07/`、`before-pi08/`。

Sutton 第 2 章另有 30 个源 JSON 明确以 text 保存、没有 MathML 的公式。最初套用 PRML 的“零 formula-fallback”规则会误判这份既有格式；独立验证该 JSON 与 Git HEAD 逐字节相同（SHA-256 `89b9b13ed8d6caaa702800620564a59104425119f230ccf13cba990d9f50092a`），然后按源块 ID 和完整文本逐个核对这些显示。所有提供 MathML 的公式仍不允许意外回退；没有以忽略回退数量的方式放宽检查，也没有擅改他书格式。

## 双模式真实浏览器结果

在 `http://127.0.0.1:8795/` 用独立 Chromium context 运行：1440×1000 浅色、390×844 深色。实际从书架点击每本书入口，再点击桌面或手机目录进入代表页；同时检查搜索命中、无结果、清空恢复、返回书架、正确书标识/URL/H1、全部预期 reading-block ID 顺序、目录数量和当前项、实际主题、首屏图片解码以及页面无整体横向溢出。

| 图书 | 实测阅读页 |
| --- | --- |
| PRML 2006 | 公共入口打开卷首，再从目录进入第 1 章 |
| Bishop 2024 | 从公共入口进入第 1 章 |
| Shannon 1948 | 默认引言及第一篇；另实测两页的进度存储和刷新恢复 |
| Sutton 与 Barto | 从公共入口进入第 2 章 |
| MacKay | 从公共入口进入第 44 章；目录包括并发追加的 45-prelude |

最终共 14 个阅读页检查、4 次 Shannon 进度恢复、22 张截图通过；JavaScript 错误为 0。22 张最终截图均已逐张用 view_image 实际查看：书架五张卡片和入口正常；标题、导读、侧栏/手机目录、正文和可见图片无新增重叠或截断。两张旧式公式横滑截图初次探针定位到内部 div，被固定工具栏遮挡，End 键又滚离目标；视觉检查发现后，仅重拍这两张，改为定位 reading-block 并用 preventScroll 聚焦，最终目标 top 85.22、toolbarBottom 62，公式完整位于视口。旧捕获和原报告保留在 `capture-correction-before/`，修正属于截图脚本，不是网站变更。

本轮为直接验证当前公共文件而禁用 Service Worker；因此 PRML、Bishop、Sutton 截图中的离线准备失败提示来自该测试设置。本记录不将该提示当作正常环境离线失败，也不将本轮当作离线验收。真正断网、25 单元全书资源与进度回归由 root 另行执行，分别见其 offline-compat-qa 和 reader-compat-qa 记录；本审查者没有重复执行或冒称独立完成这些全书测试。

可复核产物为 `tmp/prml-public-a-smoke/run_smoke.py`、`smoke-results.json` 及其列出的 22 个 PNG；每张 PNG 的实际 SHA 已再次与报告核对相等。最终 smoke-results.json raw SHA-256 为 `8ce15df24522c16053392ee87aed790e051dbe54be3acdbf01fcff9c8ac948f6`。

### 最终绑定指纹与结论

| 文件 | raw SHA-256 |
| --- | --- |
| books.js（实际烟雾版本） | `db687b8ac788c9c770e6aa75cce221054e6bf3ed0236b4de29692b19e28e2685` |
| sw.js | `c1526ee68dc9103e85b629ef486e7680bf01801fb9dc6ccdd075c88f2fcfe164` |
| README.md（其后 MacKay 45 导页说明追加已复核） | `ee43e70b226d57c3fa066c235b6bbbb916a68a329858416db952d1d80ac37c1e` |
| .github/workflows/pages.yml | `79aec0c73f819f14a64d42ae4df8c82e85e48a330914ca18689634c50c42a43c` |
| app.js（PI-07/08 最终兼容版） | `7cfed5604cadb18d4cbb45091f4d8f12c1c5cab12420aa884909507a02d7fca7` |
| styles.css（PI-08 最终兼容版） | `89908aebbf294ddf87242df4a3ae8ec21a96bdd4a2827d2353e03335cc3fdb62` |

**结论：约定范围的公共增量、发布清单和五书双模式兼容烟雾独立复核通过，PI-01–08 均已关闭，无待修项。** 该结论限于本报告给出的代码增量、测试版本及代表页，不替代任何图书的逐页翻译验收、其他书全章审查或正式部署验证。本轮审查者仅写本报告与自己的临时证据，没有修改共享文件、译稿或其他书内容。
