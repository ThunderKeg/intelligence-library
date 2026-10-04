# PRML 发布候选：离线图片与正文引用独立审查

状态：**通过最终候选的发布前独立审查，无待修项。** 最终结论以末尾“v4 与 Git LF 发布字节最终附记”为准；保留 v3 阶段证据，不将不同字节版本混称为同一版本。本报告不声称已经提交、推送或线上部署。

审查者：`/root/prml_reviewer`；日期：2026-10-04。未修改译文、生成 JSON、共享文件或执行 Git 操作。

## v3 候选与范围

- 基线：`d4f34229c32387ef923a85cf01ca4118baac4b52`。六个基线文件由集成 Agent 导出到 `tmp/prml-release-base-v3/`；本审查直接比较这些字节，没有执行 Git 命令。
- 候选：`tmp/prml-release-candidate-v3/`；实际 Pages 暂存产物：其 `site/` 子目录；浏览器入口：`http://127.0.0.1:8807/`。
- 发布涉及 PRML 已验收的 25 个阅读单元、图像、清单及本书材料，以及 `app.js`、`styles.css`、`books.js`、`sw.js`、`README.md`、`.github/workflows/pages.yml` 六个共享文件。
- 早期 `9af2265` 候选的 24 次点击及 24 张目视截图通过后，共享主分支加入了 MacKay。集成 Agent 改从 `d4f34229` 构建 v3，本审查随后重跑全部 24 次点击并再次实际查看全部 24 张截图；该阶段结论绑定 v3。旧证据保存在 `tmp/prml-review/release/`，不冒充 v3 证据。

## 源码与发布资源核验

六文件的完整增量已逐份阅读，并自行生成差异及反向精确比较：

1. `app.js` 仅补充原 PDF 页码保存后备值、MathML 的 `columnlines`/`rowlines` 与限定数值单位的 `mspace.width`、11 处附录字母范围 A–C→A–E。逐项反向恢复后，按 LF 读取的全文与导出基线完全相同；保留基线已有的 MacKay 滚动恢复及七部分引用逻辑。
2. `styles.css` 的原基线是完整前缀，新增 7 条规则均限于 PRML 选择器或 PRML 专用字体。覆盖目录页码粗体、表题换行、STIX 数学字体、矩阵列对齐与下括弧。
3. `books.js` 仅新增 PRML 对象。独立求值后，其余四本书的完整对象与顺序和基线相等；包括已提交的 MacKay。未引入候选外尚未提交的其他新书。
4. `sw.js` 仅增加 28 个 PRML 核心资源（25 个阅读单元、引用索引、图片离线清单、数学字体）。删除这 28 行后全文与基线相同，既有核心资源顺序保持。产物只进一步替换部署版本占位符。
5. Pages 工作流只增加 PRML 的 13 个非 `chapter-*` JSON 拷贝，原章节/图片拷贝与其他书规则保留。README 只新增本书说明，明确须等待首次图片准备完成。
6. 独立检查所有候选 catalog 内容路径与全部 CORE 路径均存在于真正 `site/` 产物中。PRML 全部 **370 个资源**（25 单元＋3 项索引/清单/字体＋342 图）的源码与产物 SHA-256 逐项相等；这些资源与早期已测候选也逐字节相同。

离线图片清单版本为 `3bc8e3064263d19ea4b7`，共 342 张、47,896,614 字节。其图片预取不依赖滚动到图片或先访问相应章节；首次打开本书便触发整份清单准备。仅当全部资源缓存完成才显示完成，失败不会被记成成功。正文链接依赖本书 `reference-index.json` 成功加载及 catalog/target 校验；索引加载失败时现有行为会保留普通文字，因此线上发布须同时核实该文件与 Service Worker 的新版本。

独立证据：`tmp/prml-review/release/v3/candidate-scope-audit.json`、`exact-delta-audit.json`、`independent-diff/`。

## 真实正文引用点击

使用仓库现有 Playwright/Chromium 环境。内置 Browser 初始化因 `node:process` 导入限制失败，已告知集成 Agent；后者授权使用该既有测试环境。每个用例建立新浏览器上下文，直接点击真实正文段落中的链接，不注入链接，也不以目录点击替代。两种模式为 1440×1000 浅色及 390×844 深色。

以下 12 个用例均在两模式通过，共 **24 次真实点击**；24 张最终截图均由 reviewer 逐张实际查看。

| 类型／点击文字 | 源阅读单元与块（PDF 物理页） | 目标阅读单元与块（PDF 物理页） |
|---|---|---|
| 第 3 章 | `chapter-01:p05-b005`（25） | `chapter-03:p01-b001`（157） |
| 第 3.4 节 | `chapter-01:p09-b004`（29） | `chapter-03:p25-b005`（181） |
| 图 1.11 | `chapter-02:p54-b007`（140） | `chapter-01:p16-b001`（36） |
| 表 1.1 | `chapter-01:p08-b006`（28） | `chapter-01:p08-b005`（28） |
| 式（1.141） | `chapter-02:p05-b008`（91） | `chapter-01:p62-b002`（82） |
| 式（1.2） | `chapter-01:p06-b006`（26） | `chapter-01:p05-b007`（25） |
| 习题 1.10 | `chapter-02:p04-b011`（90） | `chapter-01:p59-b013`（79） |
| 附录 A | `chapter-01:p04-b005`（24） | `appendix-a:p01-b001`（697） |
| 附录 D | `chapter-01:p46-b011`（66） | `appendix-d:p01-b001`（723） |
| 附录 E | `chapter-01:p51-b012`（71） | `appendix-e:p01-b001`（727） |
| 式（C.19） | `chapter-02:p27-b015`（113） | `appendix-c:p03-b021`（717） |
| 图 1.1 | `chapter-01:p01-b005`（21） | `chapter-01:p02-b002`（22） |

逐次断言并实际核验了链接唯一性、href、点击后的书与单元、目标块 ID/类型、最终 URL/hash、目标 H1、滚动稳定后的目标位置、图片解码、无页面级横溢出及无 JavaScript 错误。所有目标顶端均位于固定工具栏下方；手机上的宽图保留局部横向滚动与提示。

这些点击覆盖跨章章节、小节、图、公式、习题，章内表/式/图，以及附录 A、D、E 和附录 C 的公式。它们是类型覆盖的代表用例，**不是逐一点击全书所有正文引用**。该组测试关闭 Service Worker，以隔离当前发布产物；本组不作为断网证据。

脚本：`tmp/prml-review/release/check_body_references.py`。可复现命令：

```powershell
python tmp/prml-review/release/check_body_references.py --candidate tmp/prml-release-candidate-v3 --out tmp/prml-review/release/v3 --base http://127.0.0.1:8807/
```

原始点击记录：`tmp/prml-review/release/v3/body-reference-results.json`；实际查看与截图 SHA 清单：`viewed-body-references.json`。

## 全书阅读与真正断网证据

此部分执行者是集成 Agent root，本 reviewer 阅读脚本/报告并独立交叉校验结果及当前发布字节，没有重复执行其完整 50 模式与断网测试，也没有声称自己目视其全部截图。

- `reader-release-v3-qa.json`：25 单元×两模式＝50 次，通过。独立读取确认每个单元的末尾进度重载恢复、无 JavaScript 错误、无页面级横溢出。SHA-256：`62f6e2425dfb07c8739e25ccec60af017ca9c26fcba221c9bd02ce06872a812f`。
- `offline-release-v3-qa.json`：新上下文只联网打开卷首，等待图片准备完成，然后仅用 `caches.match` 检查缓存，不以在线逐资源 fetch 人工预热。断网后请求全部 370 个资源并打开 25 个单元、解码 342 张图片，885 个响应全部来自 Service Worker 且状态 200。独立复核断网前及断网后 370 个 SHA 均与 v3 `site/` 当前文件相等，无脚本错误。SHA-256：`861c7a9f7b6f660204f017abee85c62b3c76940c1e156a38dba389cd164efdc7`。
- root 另报告既有站点 `scripts/smoke_test.py` 全套通过；这不是本 reviewer 亲自执行的项目。

交叉核验记录：`tmp/prml-review/release/v3/root-evidence-crosscheck.json`。根因层面，本地已有通用预取和引用渲染功能；本次使 PRML 的清单、索引、字体及所有阅读资源完整进入发布目录与 Service Worker，并补齐附录 D/E 的识别。未凭本地结果推断此前线上故障的唯一原因。

## v3 阶段输入指纹

| 文件 | v3 候选源码 SHA-256 |
|---|---|
| `app.js` | `93ba4cb53262d5d49bc4db54c946bd803d0bd807355d33f20d256ef42d79e434` |
| `styles.css` | `ccf087368971c0df519326a33e728a764539c86f55d5090a9145d7becb709903` |
| `books.js` | `f5c9d0f8efc014d73afefe86fc32dcc0abc2c03f2cd3fd31b1a014053fb695d5` |
| `sw.js` | `d0afea9d06185f67987baa0d5942f25e813e822ecc36849f1cde5a2d858665d4` |
| `README.md` | `88dcb898458dbabc4b073b1524fe05a7a4ae0019223824a6ef7d92d59c0f535b` |
| `.github/workflows/pages.yml` | `80d0d66e2612afeef3dcbbe16d5dd4257e8de45711af9a0df366fc9a2e93884f` |

浏览器实际服务的 `app.js`、`styles.css`、`books.js` 与上述源码逐字节相同；`sw.js` 仅替换版本标识，产物 SHA-256 为 `8cc3af248fd3ce4a1bce374f800200b36d0e782f37b0b054c11d58f0d22ddc20`。其缓存名为 `intelligence-library-prml-release-validation-v3`。本轮结束再次检查四个浏览器共享输入没有漂移。

## 部署后的最小核验

发布前功能和范围无待修项。提交、推送与部署由集成 Agent 执行；部署后至少验证：

1. 实际站点路径上的 catalog、引用索引、图片清单和 Service Worker 新版本正确，资源为对应提交的字节；工作流没有漏掉附录及卷首 JSON。
2. 新浏览器上下文仅首次联网打开本书，等待全部图片准备完成；随后真正断网，打开未访问的后续章节，确认图片与数学字体加载。
3. 在实际站点路径上点击一个跨章公式／图和附录 D/E 正文引用，确认目标 hash 与落点；已有 Service Worker 的用户能获得新版本。

上述线上核验属于发布后的检查，不在本报告中冒记为已完成。

## v4 与 Git LF 发布字节最终附记

最终增量基线为 `6ec1b8c57a6f3a4541818fae6f6413017e4ad0f8`，已包含 MacKay 与 Convex 的提交。root 之后继续保留仅涉及他书审查文档的远端更新。以下接受范围绑定实际文件指纹，不以共享工作区 HEAD 的持续变化替代内容核验。

`tmp/prml-release-base-v4/` 保存新的六文件基线。独立比较确认：六文件中 PRML 的全部增加/删除行与 v3 已审增量逐行相同；其余五本书的 catalog 对象与顺序、原 CORE 资源及全部已有发布路径均完整保留。PRML 的 370 个资源与 v3 逐字节相等；CSS 归一化换行后全文相等。`app.js` 与 v3 的新增语义仅为基线已有的 `historyReturn`：跨单元引用离开时保留源段落，浏览器后退或刷新时优先恢复该段。该增量已实际阅读并专项测试。

浏览器测试入口为 `http://127.0.0.1:8808/`，目录是 `tmp/prml-release-exact-v4/site/`。该目录虽然名称含 exact，实际是 **Windows 发布模拟字节**：不能称为 Git LF 原字节。此目录上的 24 个正文点击重跑全部通过；另对以下三项各在两模式执行 Back→reload，合计 6 次后退、6 次刷新，全部恢复到原段落且目标未被工具栏遮挡：

| 点击项 | 返回／刷新后必须恢复的源块 | 双模式结果 |
|---|---|---|
| 图 1.11 | `chapter-02:p54-b007` | 通过 |
| 式（1.141） | `chapter-02:p05-b008` | 通过 |
| 附录 E | `chapter-01:p51-b012` | 通过 |

24 张点击目标图与 12 张返回/刷新图，共 **36 张 v4 截图已全部逐张实际查看**，无待修。运行脚本为同一 `check_body_references.py`，增加 `--candidate tmp/prml-release-exact-v4 --out tmp/prml-review/release/v4 --base http://127.0.0.1:8808/ --roundtrip`。点击测试仍关闭 SW；记录与所有截图 SHA 分别见 `tmp/prml-review/release/v4/body-reference-results.json`、`viewed-body-references.json`。

root 随后通过关闭 archive 的 CRLF 转换导出真正的 Git LF 目录 `tmp/prml-release-git-exact/`，发布目录为其 `site/`（8809）。root 的 `tmp/prml-git-artifact-verification.json` 记录导出树 `8626dfb2f11561ad7abd4196dcd8b13cf6c7b98e`。reviewer 未运行 Git，但自行逐文件读取并比较该目录和刚才实际查看的 Windows 模拟产物：**1868 个公开文件路径完全相同，其中 1716 个字节完全相同，152 个仅 CRLF/LF 不同，无其他差异。** 因此不重复相同内容的 36 张 UI；保留两套 raw SHA，未将它们混同。独立逐文件表见 `tmp/prml-review/release/v4/git-lf-byte-equivalence.json`。

最终 LF 目录另由 root 完整执行真正断网测试，报告 `offline-release-git-exact-qa.json`：25 单元、370 资源、342 图通过，885 响应全部 SW/200、零 pageerror。reviewer 独立读取报告，并将断网前缓存及断网后响应的每个资源 SHA 与真正 LF 发布目录逐项再核，均相等。报告 raw SHA-256：`71300f881e68cb62b212eec41a395144a68eafedd7ee390d8b2570e6254d7ef5`。本次 QA 仅补充等待 25 个 TOC 节点再断言，避免正文插入后、异步引用索引加载完成前过早检查；不削减检查项目，也未修改产品代码。

真正 Git LF 源码的六文件 raw SHA-256 已由 reviewer 独立复算；最终提交内容应保持下列字节，后续新增审查记录不改变这些发布输入：

| 文件 | 最终 Git LF 源码 raw SHA-256 |
|---|---|
| `app.js` | `a956d9201a844a9c40c63383d7e83f50057b77af8519443b6d85e3c5de55d458` |
| `styles.css` | `ccf087368971c0df519326a33e728a764539c86f55d5090a9145d7becb709903` |
| `books.js` | `95d62234f4937459e5c5bb129d0bc8973d4f4998fe24e5c2ab5abbe52857731e` |
| `sw.js` | `f26133b4666157036a6df93f76b4e3341556ab7144521fd9ffd510e4745cd2ef` |
| `README.md` | `cac8c359af3299013a8d170f2d09a7e0ae8af1a22b80062eebafbc71bc118bdf` |
| `.github/workflows/pages.yml` | `76b17e1a166cce25c03feabdc514933894a1d7b70f742959b5f390714807a78f` |

最终实际 LF `site/sw.js` 因版本占位符替换，其 raw SHA-256 为 `2d1a75edaa0c824ee43c8b4700d99a492a35efe2c25778c00b46ee548b4056bd`；其他三个公开共享文件与源码逐字节相同。`tmp/prml-review/release/v4/git-lf-scope-audit.json` 还独立确认所有 catalog/CORE 路径实存、本书 370 个源码/产物文件逐一相等；`git-lf-evidence-crosscheck.json` 记录最终报告与源码 SHA 复算。

**最终通过：本书首次联网打开并等待图片准备完成后，未访问章节的图片已具备完整离线缓存；正文引用的各类实际跳转与跨章返回/刷新通过；与其他已提交图书的整合无本轮待修项。** 完整 50 模式阅读检查来自 v3；v4 新的返回逻辑由 24 次跳转及 12 次返回/刷新专项覆盖，所有 PRML 内容/样式及最终发布字节的等价关系已明确。线上部署后的最小核验仍按上一节由集成 Agent 执行，不在此预发独审中提前记为完成。
