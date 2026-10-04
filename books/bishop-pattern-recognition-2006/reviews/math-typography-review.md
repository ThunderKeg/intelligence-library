# PRML 数学字体与围栏排版复核

第6章审查发现，浏览器默认数学字体使两行矩阵和分段表达式的围栏维持单行高度。仅补充 MathML stretchy 属性无效。现于本书作用域加载未经修改的 STIX Two Math v2.13b171 WOFF2；字体、OFL 1.1 许可与固定提交来源分别保存在 assets/fonts/ 下，原 TeX、MathML 和章节 JSON 未改变。

## 验证

- root运行第1–6章桌面1440浅色、手机390深色的12组阅读器回归，全部通过；见 reader-qa-chapter-01-chapter-02-chapter-03-chapter-04-chapter-05-chapter-06.json。
- math-font-geometry-qa.json记录12组均实际加载字体，138个多行矩阵/分段围栏均通过高度检测；reviewer独立复算最小围栏/内容高度比为1.0。
- reviewer实际查看1.52、2.67、3.40、4.137、5.132、6.65、6.95的桌面与手机共14张最终图，并复看第6章更新后的常规截图。围栏完整，原下括弧修复未回退。记录及截图指纹见 chapter-06-review.md 和 tmp/prml-review/chapter-06/font-regression-viewed-ui.json。
- QA工具已加入字体加载等待；有数学内容时验证字体成功加载，并对多行表格相邻的可伸展围栏检查几何高度。没有数学内容的页面不强求加载字体。

字体SHA-256：094191335def3f0452c81ec0713cfc2f29bb6af8cecbf79b60881fbf2db97562。

结论：本书字体修复通过现有六章回归；后续章节仍逐章做内容及显示验收。最终站点集成须将 WOFF2 纳入离线核心资源，不混入图像索引。

## 第 11 章 C11-01：竖线围栏的补充回归

独立 reviewer 在第 11 章正式截图发现，式 11.9/11.12 的行列式竖线只有普通字高。它与前述字体问题不同：U+2223 在 MathML Core 中默认不伸展，即使已有 fence=true，也需要显式 stretchy=true。本书构建器现只为精确的 `<mo fence="true">∣</mo>` 补该属性，未改 TeX、字符或条件概率的 mid。

实际查看与独立验证完成，补充回归通过：

- 受影响 18 式：第 1 章 1.27；第 2 章 2.133/2.231；第 4 章 4.103/4.126/4.128/4.132；第 5 章 5.29/5.30/5.40/5.125/5.126/5.128、PDF 286 无编号 Taylor 式、5.170；第 11 章 11.5/11.9/11.12。
- reviewer 实际逐张打开 `tmp/prml-determinant-qa/` 的全部 42 张截图：18 式的 1440 浅色/390 深色共 36 张，另有 6 张实际横滑。竖线包住全部分式，求值下标完整，相邻括号和条件竖线没有显示回退。
- `determinant-fence-regression.json` 的 54 个竖线均显式伸展；44 个有相邻分式可比较的竖线，独立复算最小高度比为 1.0138473053892216。截图清单、逐文件 SHA 和实际查看记录见 `tmp/prml-review/chapter-11/determinant-viewed-ui.json`。
- 独立重算 15 单元的源稿/生成内容/图片指纹，全部与预期一致；全部源稿和图片不变。只有这 5 章的生成内容变化；在当前 JSON 中只撤销新增的 stretchy 属性，即可逐章还原全部旧生成内容指纹。其他 10 单元完全不变。完整证据为 `tmp/prml-review/chapter-11/determinant-attribute-verification.json`，变更前记录为 `tmp/prml-determinant-fingerprints.json`。
- 修复后 5 章 × 两模式的 `reader-qa-chapter-01-chapter-02-chapter-04-chapter-05-chapter-11.json` 已复核：字体和围栏高度、无页横溢出/控制台错误、稳定目录落点、末尾阅读进度保存与重载恢复全部通过。该轮未执行章内引用点击，原逐章真实点击证据继续保留。

补充接受的生成内容 SHA（排除 editorialStatus/sourcePdfSha256/reviewRecord）：

| 章节 | 修复后 SHA-256 |
| --- | --- |
| 1 | `68c20aaa5489146a97c0e3343b821b971b689ae2b6983815ca85eac4acede6e1` |
| 2 | `7a320b41919438cb295fde8e42f928568c5b34f0a025fede6102980b042a9eff` |
| 4 | `36315cd0bec0c03ca922c4e4df572ac11e1cfc0f7688659688cbbce79d2bdedf` |
| 5 | `77c7a7a9175a5c644f5b4f08aed97d93d4a5b61ece2fefd424a441bcb15ed94b` |
| 11 | `274c9eb439bf439b194588cf8986edb95c60cb278e6618339fc9c2bd537c0901` |

本记录补充接受前 1/2/4/5 章的精确显示属性变更，原内容审查记录仍保留；第 11 章完整验收见 `chapter-11-review.md`。后续由 root 更新验收元数据，本 reviewer 不改章节 JSON。
