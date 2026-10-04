# MacKay 完整离线阅读独立 QA

结论：**本地正式路径离线验收 PASS**（2026-10-04）。测试只读使用原始 `books.js`、正式章节 JSON、`sw.js` 和图片 manifest；未拦截路由或修改站点文件。

## 预缓存

- `offline-images.json` 列出 442 个不同图像路径，文件均存在；实际总大小 29,466,950 字节，与 manifest 声明一致，版本 `33b222d463ffbbc10aea`。
- 以全新 Edge／Playwright context、允许 Service Worker，从正式 `?book=mackay-information-theory-2003&chapter=00` 冷启动。本地 HTTP 下约 3.2 秒，离线图片面板从 `checking` 进入 `complete` 并隐藏，浏览器页面获得 Service Worker controller。
- 浏览器 Cache API 独立检查：图片缓存含本书 manifest 的 **442／442** 个路径，缺失 0；核心缓存共 222 项，其中本书正式章节 JSON **81／81** 项，且包含图片 manifest。

## 断网阅读

调用 Playwright context 的 `set_offline(True)` 后，按顺序重新打开下列真实正式路径。六次文档响应均为 HTTP 200 且 `from_service_worker=True`；`navigator.onLine=false`、Service Worker 仍控制页面，阅读块加载完成，图片准备面板随后隐藏。

| 单元 | 阅读块 | 首块 | 末块 | 断网代表图解码 |
| --- | ---: | --- | --- | --- |
| 00 | 132 | `read-p001-b001` | `read-p014-b024` | 出版社徽标 PNG，640×210 |
| 01 | 252 | `read-p015-b001` | `read-p033-b014` | 通信示例 SVG，760×320 |
| 50 | 89 | `read-p601-b001` | `read-p608-b007` | 图 50.1 PNG，570×2730 |
| C | 125 | `read-p617-b001` | `read-p624-b003` | 原书表图 PNG，2500×3020 |
| REF | 319 | `read-p625-b001` | `read-p631-b045` | 原页无图 |
| IDX | 1150 | `read-p632-b001` | `read-p640-b169` | 原页无图 |

四张代表图均在断网后执行 `img.decode()` 成功，`complete=true` 且自然宽高非零。六页无 JS／控制台错误、失败请求或 HTTP ≥400 响应。此测试覆盖本地正式站点的冷缓存和真实断网读页；线上 Pages 部署仍以其实际构建版本与域名为准。
