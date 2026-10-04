# 离线图片与引用发布验收

本次交付将已完整验收的《凸优化》接入正式站点：注册 23 个阅读单元，预缓存章节、图片清单和数学字体，首次联网打开图书时预取全部 181 个图像。图片准备完成后，尚未访问的章节和插图也能离线打开。

正文已生成 2,409 条经目标校验的链接，覆盖章、节、篇、公式、图、例、习题、算法及文献。独立浏览器审查发现并修复了跨章引用后的返回位置问题，以及返回后继续阅读再刷新时的过期位置问题。共享阅读器现在按浏览器历史条目保存来源段，并随后续阅读更新该条目的位置。

## 发布范围

最终隔离交付基线为 `d4f34229c32387ef923a85cf01ca4118baac4b52`，保留另一 Agent 已提交的 MacKay 内容。相对该基线，本次只新增本书目录，并修改 `books.js`、`sw.js`、`app.js`、`README.md` 与 Pages 工作流；未纳入其他书尚未提交的文件或样式。

此前 `acceptance.json` 保持翻译终验时的历史快照。本次再次校验 23 份正文源稿和 23 份章节 JSON，全部与已验收 SHA-256 一致，没有修改译文或数学内容。

## 验证

- 31 项构建回归、9 项引用回归通过；离线清单共 181 项、4,774,071 字节。
- 最新基线上的实际 Service Worker 检查通过：四种屏幕／主题组合，共 92 个离线阅读视图；181 图离线响应的字节数与 SHA-256 均一致。
- 按 Pages 规则生成的公开目录包含 1,496 个文件；195 个核心缓存路径均存在，不包含源 PDF 或译稿 Markdown。
- 公开目录使用全新浏览器，仅联网访问卷首；断网后先读取并核对全部 181 图，再访问 23 个阅读单元，验证八类引用的点击、刷新与返回。测试不拦截或替换书架、正文或 Service Worker。
- 独立 Agent 的引用目标、真实导航、历史记录及旧书入口复验见 [release-review.md](release-review.md)。
- 提交检查保留已验收文件的原始字节。Windows CRLF 按行尾处理；上游 `assets/fonts/OFL.txt` 第 20 行原有尾空格作为原许可证保留，其余暂存文件的空白检查通过。

本文件记录发布前的验收。部署后的检查使用 `tools/qa_published.py`，按实际提交 SHA 核对线上 Service Worker，并再次验证冷缓存离线图像、章节 JSON 和交叉引用。

## 线上验收

`6ec1b8c57a6f3a4541818fae6f6413017e4ad0f8` 已推送至远端 main，[GitHub Pages 运行 37192172967](https://github.com/ThunderKeg/intelligence-library/actions/runs/37192172967) 成功完成。

对[正式网站](https://thunderkeg.github.io/intelligence-library/?book=boyd-vandenberghe-convex-optimization-2004&chapter=frontmatter)重新创建浏览器上下文，确认线上 Service Worker 的版本等于上述提交。只在联网状态打开卷首，图片准备完成后断网，先于任何其他章节访问逐一读取 181 个图像，其字节数和 SHA-256 均与已验收资产一致。随后全部 23 份线上章节 JSON 与本地验收内容一致，23 个手机深色阅读视图、八类引用点击／刷新／Back 均通过，没有 JavaScript 错误。195 个核心资源的线上 HTTP 检查全部返回 200。

完整结果见 [release-published.json](evidence/release-published.json)；本节随后的提交仅补充验收记录，不改动正文、图像、阅读器或工作流。
