# 离线图片、交叉引用与发布

本清单记录翻译验收后的 Git 与网站交付；此前 `reviews/acceptance.json` 是全书翻译完成时的工作区快照，保持原样。

- [x] 核对线上与本地差异：线上 main 尚未收录本书，本地已有完整图片清单和生成的引用链接。
- [x] 从当前已发布版本构造独立发布目录，只加入本书及必要的共享登记。
- [x] 首次联网仅打开卷首，等待图片准备完成后断网；验证未访问章节和全部图片。
- [x] 验证章内、跨章、公式、图、习题与参考文献跳转，以及窄屏显示。
- [x] 独立 Agent 审查发布目录与实际浏览器结果，修复发现的问题。
- [x] 核对暂存范围，commit & push。
- [x] GitHub Pages 部署成功，线上版本与发布内容一致；线上离线图片与跳转复验。

发布提交：`6ec1b8c57a6f3a4541818fae6f6413017e4ad0f8`，已推送至远端 `main`；[Pages 运行 37192172967](https://github.com/ThunderKeg/intelligence-library/actions/runs/37192172967) 部署成功。线上全新浏览器只联网访问卷首，断网后全部 181 个图像字节及哈希、23 个阅读单元、八类引用点击／刷新／返回均通过。详见 [发布记录](reviews/release-integration.md) 与 [线上实测证据](reviews/evidence/release-published.json)。
