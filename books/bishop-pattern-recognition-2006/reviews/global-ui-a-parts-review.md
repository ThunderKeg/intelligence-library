# PRML 全书术语增量：a 分片独立 UI 审查

审查日期：2026-10-04。审查者：prml_translate_b。状态：本次增量 UI 审查完成，未发现待修 UI 问题。

本审查覆盖未由审查者初译的 a 分片：第 4、5、6、8、13 章的全部 35 个修订块，以及参考文献 a 分片的 6 个代表条目。没有将本人初译的 b 分片纳入本次独立审查。此记录仅对修订后的实际网页显示负责，不代替逐页对照原 PDF 的语义、内容与公式审查，也不宣告全书最终验收。

## 执行与证据范围

- 按 reviews/global-ui-change-plan.json 的 originalAuthor=a 选取正文目标，逐项核对范围无遗漏；参考文献抽取首条、斜体书名、跨原页条目、长题名与强调、带附加符作者名及 a 分片末条。
- 使用现有 tools/qa_targets.py 的浏览器流程。临时包装器仅把自动报告输出从公共 reviews 目录重定向至本审查的独立临时目录；未修改共享脚本、译稿、图片或章节 JSON。
- 首轮包含 41 个目标、82 个“目标 × 显示模式”检查，产生 88 张截图；模式为 1440 × 1000 浅色、390 × 844 深色。全部首轮输出截图均已通过 view_image 实际逐张查看，包含图像水平滑动终点与长段落续屏。
- 第 5 章一处邻近公式的首轮截图有绘制时序问题，追加两张稳定绘制后的复查截图并实际查看。共实际查看 90 张，逐张 SHA-256 见后表；没有把仅生成而未查看的截图计入通过。
- 各次 QA 进程均成功结束，未报 JavaScript 错误、页面整体横向溢出、缺失目标或字体检查失败。宽图和宽公式使用各自横向滚动容器。
- 审查结束时重新计算本次 6 个单元的 JSON SHA-256，与截图前保存的逐单元快照完全一致。global-delta-qa.json 的 passed=true 作为结构守恒的另行证据；其中原文、译题和强调等逐字守恒结果不扩大本审查的人工 UI 覆盖范围。

执行入口：tmp/prml-global-ui-a/run_targets.py；唯一复查入口：tmp/prml-global-ui-a/run_targets_settled.py。每个单元的目标文件、JSON 快照、QA 报告与截图放在同名子目录，避免重复块 ID 覆盖。

## 范围与逐项结果

| 单元 | 目标数 | 首轮双模式检查数 | 首轮截图数 | 结果 |
| --- | ---: | ---: | ---: | --- |
| chapter-04 | 1 | 2 | 2 | 已逐张查看，通过 |
| chapter-05 | 12 | 24 | 26 | 已逐张查看，通过 |
| chapter-06 | 5 | 10 | 10 | 已逐张查看，通过 |
| chapter-08 | 6 | 12 | 14 | 已逐张查看，通过 |
| chapter-13 | 11 | 22 | 24 | 已逐张查看，通过 |
| references | 6 | 12 | 12 | 已逐张查看，通过 |
| chapter-05-recheck | 1 个既有目标 | 2 次追加复查 | 2 | 已逐张查看，绘制时序项关闭 |

具体视觉结论：第 4 章的“概率生成式模型”标题与目录一致；第 5 章导读、标题、正文和图 5.8 中“雅可比矩阵”的中文、英文括注及邻近数学无文字覆盖；第 6、8 章的“生成式／判别式”及“狄利克雷”完整显示；第 13 章“格图”的首次英文括注、重复引用及四幅受影响图注显示正常。窄屏目标文字均能换行，深色正文与图注可辨认，图内原始信息没有被新译文遮住。

| 单元 | 块 ID | PDF 物理页 | 类型 | 1440 浅色 / 390 深色 |
| --- | --- | ---: | --- | --- |
| chapter-04 | p18-b005 | 216 | heading | 已实际查看 / 已实际查看，通过 |
| chapter-05 | p01-b002 | 245 | intro | 已实际查看 / 已实际查看，通过 |
| chapter-05 | p02-b004 | 246 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-05 | p17-b006 | 261 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-05 | p23-b001 | 267 | figure | 已实际查看 / 已实际查看，通过 |
| chapter-05 | p23-b004 | 267 | heading | 已实际查看 / 已实际查看，通过 |
| chapter-05 | p23-b005 | 267 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-05 | p23-b007 | 267 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-05 | p23-b009 | 267 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-05 | p23-b010 | 267 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-05 | p24-b003 | 268 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-05 | p24-b004 | 268 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-05 | p24-b012 | 268 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-06 | p07-b011 | 317 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-06 | p07-b012 | 317 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-06 | p08-b004 | 318 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-06 | p08-b007 | 318 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-06 | p13-b008 | 323 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-08 | p07-b005 | 385 | heading | 已实际查看 / 已实际查看，通过 |
| chapter-08 | p08-b004 | 386 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-08 | p08-b005 | 386 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-08 | p10-b005 | 388 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-08 | p11-b001 | 389 | figure | 已实际查看 / 已实际查看，通过 |
| chapter-08 | p22-b008 | 400 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-13 | p07-b008 | 631 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-13 | p08-b001 | 632 | figure | 已实际查看 / 已实际查看，通过 |
| chapter-13 | p08-b007 | 632 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-13 | p09-b003 | 633 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-13 | p10-b004 | 634 | figure | 已实际查看 / 已实际查看，通过 |
| chapter-13 | p11-b006 | 635 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-13 | p17-b001 | 641 | figure | 已实际查看 / 已实际查看，通过 |
| chapter-13 | p17-b002 | 641 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-13 | p18-b001 | 642 | figure | 已实际查看 / 已实际查看，通过 |
| chapter-13 | p19-b003 | 643 | paragraph | 已实际查看 / 已实际查看，通过 |
| chapter-13 | p23-b009 | 647 | paragraph | 已实际查看 / 已实际查看，通过 |

参考文献 6 条在两种模式下均逐条查看。抽样没有发现括注分离、句点重复、文字截断或强调丢失；英文原题和中文题名的完整守恒由既有全 170 条结构检查另行覆盖，本表只记实际抽样显示结果。

| 块 ID | PDF 物理页 | 条目 | 实际查看重点与结果 |
| --- | --- | --- | --- |
| p01-b002 | 731 | Abramowitz and Stegun (1965) | 首条；斜体书名、中文题名括注与其后句点、出版社衔接。 |
| p01-b009 | 731 | Amari (1985) | 斜体长书名；窄屏英文与中文题名分别换行，括注闭合。 |
| p01-b017 | 731–732 | Attias (1999b) | 原 PDF 跨页条目；网页保持单条连续显示，原题、译题、会议录强调及页码连贯。 |
| p02-b005 | 732 | Baldi and Hornik (1989) | 长论文题名；中文括注后句点正常，期刊斜体与卷号粗体可辨。 |
| p08-b021 | 738 | Hyvärinen and Oja (1997) | 作者附加符 ä 可辨；中文括注、期刊斜体及卷号粗体正常。 |
| p08-b023 | 738 | Ito (1991) | a 分片末条；长中英题名换行后仍是完整书目，括注、期刊及卷期页码衔接正常。 |

## 发现与复查

GU-A01（截图证据时序，已关闭）：首轮 chapter-05/p02-b004-1440-light.png 的修订目标段落已完整显示，但紧随其后的公式 5.1 所在位置暂时留白。没有据此判断源公式缺失，也没有修改产品内容。使用同一 QA 流程，在滚动后等待两次 requestAnimationFrame 及 250 ms 再截图；chapter-05-recheck/p02-b004-1440-light.png 中公式 5.1 已完整绘制。同步复看窄屏深色截图，目标段落仍正常。两次复查截图均在下面清单中固定 SHA。该项不再有待修产品问题，首轮截图留存以说明复查原因。

没有其他待修 UI 项。未编辑源文、译稿、章节 JSON、图片、样式或共享工具；本轮仅写本报告与 tmp/prml-global-ui-a 下的审查材料。

## 已审版本 SHA-256

下列为实际截图使用并在审查结束时复算一致的 JSON 原始字节 SHA-256，不是翻译源码的归一化指纹。

| 单元 | JSON raw SHA-256 |
| --- | --- |
| chapter-04 | `2d5243740f6d4bba477119da4fa413986977ff6735043c7c2dea045235759030` |
| chapter-05 | `c34a53aea8a2df80785beee0964e75b42049b64babae6c4b5d8c855d69e63562` |
| chapter-06 | `cb5302d8241c4b74f1cc2136581be30d8f96753f641287250069e616af9b1349` |
| chapter-08 | `0b31ade4dbc8f77a3f2976cb0ba8dc2a65f0914b455af75b640c271d2255c5aa` |
| chapter-13 | `cc0bc88d24c870c61e34e8e5f99b73a58785b9dbd1cd0f68b8ac1d50c0bc3517` |
| references | `c87bd3af3fde4fa4558d15da20088476c26f62d96fdd426dafd9a226eef5077c` |

| 支持文件 | raw SHA-256 |
| --- | --- |
| tmp/prml-global-ui-a/scope.json | `1e7377dc9a9cce0d43fdcfb2273526e9ed777099384d351c90ae36af39b5b2e4` |
| books/bishop-pattern-recognition-2006/reviews/global-ui-change-plan.json | `5980c90cf1ad6978b4ca80b4ef07a7244fe74735e26f65d714f4b045d18e0f1a` |
| books/bishop-pattern-recognition-2006/reviews/global-delta-qa.json | `9b7ac651a9baa03b37c0260cd9422922163d4b05522c970758ce45d72743d935` |
| books/bishop-pattern-recognition-2006/tools/qa_targets.py | `46ee58368a35eea0de1a367b21288e0770bf430962c2aace321bee9463072468` |
| tmp/prml-global-ui-a/run_targets.py | `c9d2c8fb6ebe6019eb1518a1faa2e893cda1b2fd0eba8cf2ed6fbe18f14df089` |
| tmp/prml-global-ui-a/run_targets_settled.py | `a60526763571430c6442da25714a193a818ffbda365bb5b9b7e2d20405da53b5` |
| tmp/prml-global-ui-a/chapter-04/reader-qa-chapter-04-targets-global-a.json | `512002a0444752b86043d6c6fa39f548798158002fa27638b6c4a388ede6e4f5` |
| tmp/prml-global-ui-a/chapter-05/reader-qa-chapter-05-targets-global-a.json | `596151719d78af5157ab71341272fcf389c5fda0abe4cd0656fdba89b2cfece6` |
| tmp/prml-global-ui-a/chapter-06/reader-qa-chapter-06-targets-global-a.json | `c0f12af5bfaeeeb24b6c4da6daac7776dc909d5cc941281578bfb4b5ea205838` |
| tmp/prml-global-ui-a/chapter-08/reader-qa-chapter-08-targets-global-a.json | `1c7dd00ded34780f293930931cfba37eb2d61eb759a855d1fcccee052df81fb3` |
| tmp/prml-global-ui-a/chapter-13/reader-qa-chapter-13-targets-global-a.json | `16993c20d3c726ac94afe43300ea0cdea871739d3a680297bb55deb506f5af6a` |
| tmp/prml-global-ui-a/references/reader-qa-references-targets-global-a.json | `04e4d9110c17f94947b98854124f5ed5954b78f762075e44b3503bccc139f9bd` |
| tmp/prml-global-ui-a/chapter-05-recheck/reader-qa-chapter-05-targets-global-a-settled.json | `93b945df106a1b17213137d972bfc80a38265cf54bbaef8535297cf1adf72418` |

## 实际逐张查看的截图清单

以下路径均相对于 tmp/prml-global-ui-a。每行都已实际查看；“首轮，需结合复查”仅指 GU-A01 的邻近公式绘制状态，该图中的修订目标文字本身已通过。

| 截图 | 尺寸 | 实际查看结果 | raw SHA-256 |
| --- | --- | --- | --- |
| chapter-04/p18-b005-1440-light.png | 1440 × 1000 | 已查看，通过 | `c91f94536195aff6faf69d96dea9a4da362ce5994094d7aff1f2290c198beadc` |
| chapter-04/p18-b005-390-dark.png | 390 × 844 | 已查看，通过 | `86b2b4f04136ddcf8952ea7bf289116ad82ad24ebe58e2cc451a6c23b4396177` |
| chapter-05/p01-b002-1440-light.png | 1440 × 1000 | 已查看，通过 | `55b4479da14f85aadac4ec1958ecfbb69c6479656692d2e814d9b5f2675f1d73` |
| chapter-05/p01-b002-390-dark.png | 390 × 844 | 已查看，通过 | `87d7db7b2a26a5720dfce590cae4f4e5e95fed46f6cf358a638e29f498438b10` |
| chapter-05/p02-b004-1440-light.png | 1440 × 1000 | 已查看；首轮，需结合 GU-A01 复查 | `46097d1fc46c08c8ebf49d50c9141c9d0f57406956c60abeeb071d918defd2cf` |
| chapter-05/p02-b004-390-dark.png | 390 × 844 | 已查看，通过 | `0c727180b244650bde158702bd59d4de697983cfca7dea62cc701989a69face5` |
| chapter-05/p17-b006-1440-light.png | 1440 × 1000 | 已查看，通过 | `d73611f754cb420300a61ad301966db6e086b63771e1a6e230bdf7433238fe20` |
| chapter-05/p17-b006-390-dark-continuation-1.png | 390 × 844 | 已查看，通过 | `71d38b226ad80ab13e397bb7c28fdf98fdfdfafc5e9a260e6f7987d019a2e4d0` |
| chapter-05/p17-b006-390-dark.png | 390 × 844 | 已查看，通过 | `b25d80c541ccd4e590f9bde3c4b1653de8dcd8724c30f0514d1b24186a7d1868` |
| chapter-05/p23-b001-1440-light.png | 1440 × 1000 | 已查看，通过 | `208595cb7124d3a0b0ea622aa7b1ca0799246fd0e0b0a68105acac5d35c41bd5` |
| chapter-05/p23-b001-390-dark-pan-0.png | 390 × 844 | 已查看，通过 | `34488c21376a784e32541ad96f0f2ffb689ed8d5150d5b8e9dddfb96fae94db0` |
| chapter-05/p23-b001-390-dark.png | 390 × 844 | 已查看，通过 | `0cbd56f9bd010e49c73a61a4249a85f187677c76c5ed37adb57b0b5cc37a090c` |
| chapter-05/p23-b004-1440-light.png | 1440 × 1000 | 已查看，通过 | `96bad8b9fc57dfdadd6194d0ff693b7816e9bf0141433b1606a42d1cfa42831f` |
| chapter-05/p23-b004-390-dark.png | 390 × 844 | 已查看，通过 | `4ae063ed6e6928f4a55a362ff536ea2329b4e0a1c198675a7e515537139356cd` |
| chapter-05/p23-b005-1440-light.png | 1440 × 1000 | 已查看，通过 | `19b12d5cbc9e13b466d072e8c81c766c0c84c04d13c8348860db5bababe4c296` |
| chapter-05/p23-b005-390-dark.png | 390 × 844 | 已查看，通过 | `8f14dc6acb1c42780ce564fcc867bd008abafdbbb66abc15af5f3f163e28ebf3` |
| chapter-05/p23-b007-1440-light.png | 1440 × 1000 | 已查看，通过 | `d594e72df3bb99ddc0367f2049706f29a4895ee391cea2cd5e9cf5641e67a63b` |
| chapter-05/p23-b007-390-dark.png | 390 × 844 | 已查看，通过 | `d3d277fb82757a924a932b70e54421d4251cf0c8255767ddd3315ce7c58cf4f2` |
| chapter-05/p23-b009-1440-light.png | 1440 × 1000 | 已查看，通过 | `ad5b08d9d815a938c9783e533b6740be6f3bc682ecb03bffd53285b2eddb3bea` |
| chapter-05/p23-b009-390-dark.png | 390 × 844 | 已查看，通过 | `73e52efe5c3c34a9b0a2132168129900a24f05c525fffa47c0a94b50ef13e515` |
| chapter-05/p23-b010-1440-light.png | 1440 × 1000 | 已查看，通过 | `e405fc85312fffa6495fef009162d7aca9d16c5f2cafb70feac269c9ad5d7f5e` |
| chapter-05/p23-b010-390-dark.png | 390 × 844 | 已查看，通过 | `1aedac4dfd2f82b3bcb154e32ededf5b09f25ceb33d0d5b8fd64067ad7c7cb9e` |
| chapter-05/p24-b003-1440-light.png | 1440 × 1000 | 已查看，通过 | `c6434a8afc69a180e0f47b62f0fecc62d1925f8bda1633c204e128452e4b1139` |
| chapter-05/p24-b003-390-dark.png | 390 × 844 | 已查看，通过 | `b56529183f6cfddcbbc8b06cff9e89e90c74a70a409ce4ce81cd8fa6168eef91` |
| chapter-05/p24-b004-1440-light.png | 1440 × 1000 | 已查看，通过 | `c886eb69844371f5c670b722f1173a79681d963c6cb4d74e231a149314fab289` |
| chapter-05/p24-b004-390-dark.png | 390 × 844 | 已查看，通过 | `bfb1b7437849b6e157371a0c6e2704fd950fe25e4b80b09a9ed42d542d2303e2` |
| chapter-05/p24-b012-1440-light.png | 1440 × 1000 | 已查看，通过 | `12f0ee5a9cb8f7cb9d9eab4605b91643372bf203968332f4bd0047fc097c041a` |
| chapter-05/p24-b012-390-dark.png | 390 × 844 | 已查看，通过 | `e1c6bb41be1ff1d7343c60d4923d01585798c879b704021c0d90b0f7105f1ae1` |
| chapter-05-recheck/p02-b004-1440-light.png | 1440 × 1000 | 已查看，复查通过 | `08dab6207bf48e3facb187758280c8bc57ebf0098bbd919cb98183fc275c4f8e` |
| chapter-05-recheck/p02-b004-390-dark.png | 390 × 844 | 已查看，复查通过 | `0c727180b244650bde158702bd59d4de697983cfca7dea62cc701989a69face5` |
| chapter-06/p07-b011-1440-light.png | 1440 × 1000 | 已查看，通过 | `a45d4b82105877290152c9c47b182ccb86c77a03414e02c4cf6b8009a733c773` |
| chapter-06/p07-b011-390-dark.png | 390 × 844 | 已查看，通过 | `502d93059ff885b8ec1d7e51acc8c546db9d8f9c11360a77e5e5be970772d451` |
| chapter-06/p07-b012-1440-light.png | 1440 × 1000 | 已查看，通过 | `6554df043229ba2c4f9c174f050aa4c1c7941e96a20454f3a869113c223c5c86` |
| chapter-06/p07-b012-390-dark.png | 390 × 844 | 已查看，通过 | `eab18a82acd17ede52b6cd93b459ba890b870dc6bf10c81695f275e72f84a6d0` |
| chapter-06/p08-b004-1440-light.png | 1440 × 1000 | 已查看，通过 | `71ecec97731741cd37e908d28e24b52ba7d998fe3a9264e2f246d2b9d7a8eb3d` |
| chapter-06/p08-b004-390-dark.png | 390 × 844 | 已查看，通过 | `52cda4d254d54dafa8557827a9059425ac8ed012d303b18ec8fa914733e25526` |
| chapter-06/p08-b007-1440-light.png | 1440 × 1000 | 已查看，通过 | `3f6e4973acdacba84726ef502d51d7d970c43c789eb3ca6f6be81b80f9a63c3d` |
| chapter-06/p08-b007-390-dark.png | 390 × 844 | 已查看，通过 | `c0a6b48747cff483f9c277bbee92eef494936c2652898fd4ebbd98bbfd2986c4` |
| chapter-06/p13-b008-1440-light.png | 1440 × 1000 | 已查看，通过 | `5d3c8b0f0303e5433b78533614736eae15395386fb88374875bccf0dda379e2b` |
| chapter-06/p13-b008-390-dark.png | 390 × 844 | 已查看，通过 | `2784cbd41576f92a1fd47b0e402570d1dbccb0443a25d04270cdd870aa51b708` |
| chapter-08/p07-b005-1440-light.png | 1440 × 1000 | 已查看，通过 | `8f56eda4fe729fc4e2db8221fb13f47350bf923317e360ff88f8f5c5503ccac3` |
| chapter-08/p07-b005-390-dark.png | 390 × 844 | 已查看，通过 | `a94ec1c21f5c0b987ac9e90270d3d2a64214dc473fc91b62828882e7ba986512` |
| chapter-08/p08-b004-1440-light.png | 1440 × 1000 | 已查看，通过 | `9a030798ddac43c313ed35e273bae377f8f1810cf4846812e44d331c36827560` |
| chapter-08/p08-b004-390-dark.png | 390 × 844 | 已查看，通过 | `261f7b209833e2ed45bb41cccd32ebc8e120ad51204b84129303ac0ea3bc24e5` |
| chapter-08/p08-b005-1440-light.png | 1440 × 1000 | 已查看，通过 | `c4c218fdcdd2673bf33c8c99dad14516e17ab0899a69562c4aa038d0338c494d` |
| chapter-08/p08-b005-390-dark.png | 390 × 844 | 已查看，通过 | `6b175f08fda1dc9e41217cc3402e1d14aa927689f1083887dacce9a51fa9268a` |
| chapter-08/p10-b005-1440-light.png | 1440 × 1000 | 已查看，通过 | `a0ca19254ace69b6e1c8c6478903a77b3bc44555bc6b103f3701b6a00d318f8b` |
| chapter-08/p10-b005-390-dark.png | 390 × 844 | 已查看，通过 | `5bd93453669ee05aeb775da5b5fc5a3bc7539c81d823dbadd9bacb32aa8fa9be` |
| chapter-08/p11-b001-1440-light.png | 1440 × 1000 | 已查看，通过 | `a35ffd359cb0cfe3422f9da0524cea8fb361597984c0b88af61ad0438943e589` |
| chapter-08/p11-b001-390-dark-pan-0.png | 390 × 844 | 已查看，通过 | `cd8ce2469991658005aded4e96de7625787a87919bc536638105bdf111514376` |
| chapter-08/p11-b001-390-dark.png | 390 × 844 | 已查看，通过 | `e34a0d295e5b35ab707ee774a92af7c19a62a6e02f2cd4c48e59bd9d3c836657` |
| chapter-08/p22-b008-1440-light.png | 1440 × 1000 | 已查看，通过 | `a6e5a5ad050e6c386acb7a1cef99f777c6dd188c4466ba1da529630357d8af90` |
| chapter-08/p22-b008-390-dark-continuation-1.png | 390 × 844 | 已查看，通过 | `2ed4e25014ecbd7c965048dd2bc7d5f15ddc1bf69c393f16505e0a1aa75d9c88` |
| chapter-08/p22-b008-390-dark.png | 390 × 844 | 已查看，通过 | `0beb15075925826843402fc79f85d27717a24cb2a5be68c5dffe30d9f9e41321` |
| chapter-13/p07-b008-1440-light.png | 1440 × 1000 | 已查看，通过 | `d77033c055e34bf112d63b58c0b288571cc97c020d93b6cc8ceda3929e74fd3d` |
| chapter-13/p07-b008-390-dark.png | 390 × 844 | 已查看，通过 | `db9d7e246a351c12f84862161b2efb09cb871f3af7bf65c80fd2e959f2d88dec` |
| chapter-13/p08-b001-1440-light.png | 1440 × 1000 | 已查看，通过 | `8dfaf3100647afda3ea0e1fa8e8123c87294a27f97a62695c61f52af858e7df1` |
| chapter-13/p08-b001-390-dark-pan-0.png | 390 × 844 | 已查看，通过 | `277598011753add7391e88150ff8bae7ddd45dc098899d7ad1105d90935fff60` |
| chapter-13/p08-b001-390-dark.png | 390 × 844 | 已查看，通过 | `858238e5783352046f7f507650a04faa521eb41db4b2dbe0282fe61dfac293bc` |
| chapter-13/p08-b007-1440-light.png | 1440 × 1000 | 已查看，通过 | `66e83d78ffba558980498b9f8d01442cb909b62c1966608bfa229d861b1563f7` |
| chapter-13/p08-b007-390-dark.png | 390 × 844 | 已查看，通过 | `cefc2b7a396091f6af09ffe8ef217396d77347584db340cbbc04503ddf4ac424` |
| chapter-13/p09-b003-1440-light.png | 1440 × 1000 | 已查看，通过 | `2b325744e292184616dbe2042fa803c62d8de7df28140bd8ce7b70269486e361` |
| chapter-13/p09-b003-390-dark.png | 390 × 844 | 已查看，通过 | `487ea42074ff065f64d93ca202f39ad9ba5bd5705365ee88c4251126ad258ee6` |
| chapter-13/p10-b004-1440-light.png | 1440 × 1000 | 已查看，通过 | `a409443a071a382430f1359523e94efe4e45d0853eafd189c8c9aa93280cc67d` |
| chapter-13/p10-b004-390-dark-pan-0.png | 390 × 844 | 已查看，通过 | `7eb57266608c50ad603d244bbfb5fc3012d55155adc1fe617b8971556cd17288` |
| chapter-13/p10-b004-390-dark.png | 390 × 844 | 已查看，通过 | `61f84333368358ae921ec40aad12b0703cd826de8d6b9fb639077eafd7e33f69` |
| chapter-13/p11-b006-1440-light.png | 1440 × 1000 | 已查看，通过 | `e16a47f868aae086236cd6d8793e7c515fe8398fc8325c1f1d80caa19fc29717` |
| chapter-13/p11-b006-390-dark.png | 390 × 844 | 已查看，通过 | `fb35f7283fc02364d6f7a78aa5e107480d410a2dfb99eef9e8520835c90878d4` |
| chapter-13/p17-b001-1440-light.png | 1440 × 1000 | 已查看，通过 | `93a691faef75d5d6f0af51f764de2ceaeead79be598be048f90edd482326636a` |
| chapter-13/p17-b001-390-dark.png | 390 × 844 | 已查看，通过 | `6cf6d6ad9cef02068669b9cc402c25f654ef8b949129911bac23a72c71a843ef` |
| chapter-13/p17-b002-1440-light.png | 1440 × 1000 | 已查看，通过 | `e848640bc068a0edf206bc1379c8125931e105c041b702d212bf1ec9d7fdf622` |
| chapter-13/p17-b002-390-dark.png | 390 × 844 | 已查看，通过 | `32e1daa03b5fb393b5e72d43f7dba2dfd3442b23ba5aeb55497a1436e71a461f` |
| chapter-13/p18-b001-1440-light.png | 1440 × 1000 | 已查看，通过 | `52f31ee2b55b9088c5c6f86e06fc000998f8552806f33e687f349e0565578aa5` |
| chapter-13/p18-b001-390-dark.png | 390 × 844 | 已查看，通过 | `fad951f9370be93925fecd380a40c14e1eba82e59791fae64f827679b48133f6` |
| chapter-13/p19-b003-1440-light.png | 1440 × 1000 | 已查看，通过 | `f5972db292f8fa84ba5ecf34306d67f656495ed3f3dfad33f43ab15066632894` |
| chapter-13/p19-b003-390-dark.png | 390 × 844 | 已查看，通过 | `c41ba8b6aa7d90308628f056536edab58dd8717f3a503e274bad16b75a96f54b` |
| chapter-13/p23-b009-1440-light.png | 1440 × 1000 | 已查看，通过 | `3e7e11830c40f574c87cf36c353ea029cc712836c196ec7b0aba501541d8d017` |
| chapter-13/p23-b009-390-dark.png | 390 × 844 | 已查看，通过 | `045b2eedf3fbe92c5f67c0a494411b61f5cbe36a7c7a4c66c55c58ed83e7f866` |
| references/p01-b002-1440-light.png | 1440 × 1000 | 已查看，通过 | `54163c42a5e570efe551c96d5d5cb3568157e5107816b1e8acece847abe08ba1` |
| references/p01-b002-390-dark.png | 390 × 844 | 已查看，通过 | `a694b8717573f38108722b223b4873b873811dc4c12807161e6df6febbed7840` |
| references/p01-b009-1440-light.png | 1440 × 1000 | 已查看，通过 | `3b15e02293927698c6b3e304ca5880ed6852153f278ee2c41f04ab46ee9f079f` |
| references/p01-b009-390-dark.png | 390 × 844 | 已查看，通过 | `78bbdad217f3ecb45d154294ba3c3f9241b0c2fc2af5a55d437dd042993450da` |
| references/p01-b017-1440-light.png | 1440 × 1000 | 已查看，通过 | `aa887262d97e7aa573ad5911a13d10474b660e677c276845b01448ec49af0091` |
| references/p01-b017-390-dark.png | 390 × 844 | 已查看，通过 | `2fbc6143e3452c4d213aa384843ab8c84eeacf8e3a1ea78a1a2b060f0bbdd596` |
| references/p02-b005-1440-light.png | 1440 × 1000 | 已查看，通过 | `fff087ef9c1872032a3689caf7d48f879d02d6ccef96b67b25cf5bd4fce09fb9` |
| references/p02-b005-390-dark.png | 390 × 844 | 已查看，通过 | `6b3efb759aaf5c3fe8b0881ac410cf6ba86e0685f42c41cf1fccc3316a515a7e` |
| references/p08-b021-1440-light.png | 1440 × 1000 | 已查看，通过 | `57a1554442b52aa5ee551c7ba9b346c96a21cbfe982f75e2dc8f1cb538e84e6c` |
| references/p08-b021-390-dark.png | 390 × 844 | 已查看，通过 | `ff8069fbcad03e14cd98d273230f25100bcb5f897440831a489a4bf8739ec02f` |
| references/p08-b023-1440-light.png | 1440 × 1000 | 已查看，通过 | `bba9b5ae1c264d966dc3f7cfbc61a65d7409ede5f0a7b0ade6c90fa3e37b7574` |
| references/p08-b023-390-dark.png | 390 × 844 | 已查看，通过 | `bfd838c20c33d85e4fb6e11e012bd417368eed52c520121bc0862d2d7d414155` |
