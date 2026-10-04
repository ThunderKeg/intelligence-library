# 新增引用索引断网回归

结论：**PASS**。使用全新 Edge 持久化配置，先在书架页安装并激活真实 `sw.js`，确认预缓存后才断网；随后通过真实 `books.js`、章节 JSON 和 `reference-index.json` 打开阅读页。未拦截请求或注入数据。

## 缓存与测试条件

- `navigator.serviceWorker.controller` 指向本地站点的 `sw.js`；`intelligence-library-__BUILD_VERSION__` 核心缓存有 **223** 项，其中 MacKay `chapter-*.json` **81/81** 项，且包含 `books/mackay-information-theory-2003/reference-index.json`。测试前图片缓存为 0 项，说明章节与引用索引的断网结果依赖核心预缓存。
- 切换 Edge 浏览器配置为断网后，三个阅读页面均报告 `navigator.onLine === false`；完成测试时核心缓存仍为 223 项、MacKay 章节仍为 81 项、引用索引仍在缓存。

## 断网实测

| 位置 | 预期 | 结果 |
| --- | --- | --- |
| 第 26 章 `read-p352-b005` 的“第六部分” | 链接到第六部分扉页 | 生成 `chapter=VI#read-p567-b001`；点击后断网打开 `read-p567-b001`，H1 为“第六部分 稀疏图码”。第 26 章共生成 44 个引用链接。 |
| 第 43 章 `read-p535-b017` 的“式 (16.5)” | 印本引用没有对应编号式，保留原文而不建错链 | 句子完整显示，所在块的 `<a>` 数量为 0；本章其他引用链接仍生成 11 个。 |
| 第 26 章 `read-p347-b002` 的“图 26.1” | 章内图引用可跳转 | 生成 `#read-p347-b003`，点击后定位到 `read-p347-b003.reading-figure`。 |

断网期间无页面脚本错误或 HTTP 4xx/5xx 响应。没有启动整本书图片离线下载；本次只验引用链接、章节和引用索引的预缓存，未把图像离线解码列入结论。

截图与原始运行记录临时存于 `%TEMP%\mackay-reference-offline-qa\`：`ch26-part-link-offline.png`、`part-VI-target-offline.png`、`ch43-equation-16-5-unlinked-offline.png`、`ch26-figure-26-1-link-offline.png`、`result.json`。
