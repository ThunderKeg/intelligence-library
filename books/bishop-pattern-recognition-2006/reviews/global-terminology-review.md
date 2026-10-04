# 全书术语与参考文献格式增量总审

状态：**通过，可重新绑定以下 7 个单元的当前验收指纹。** 本报告只覆盖第 4、5、6、8、12、13 章及参考文献的这次限定修订，接续各单元原有完整独审，不提前宣告最终目录、公共站点接入与离线验收通过。

总审者 prml_reviewer 未参与初译。按最终分工，原页语义由未初译对应分片的 root／prml_translate_a 独立复审；本总审阅读两份完整结论、作者差异记录与网页报告，并亲自复算当前源稿、JSON、图片及证据指纹。没有把其他 reviewer 实际查看的原页或网页截图计作本人的目视。

- [x] 两个分片组的原页语义独审通过，新增 GB-01 已修复并独立复核。
- [x] 9 份分片的全部差异限于授权修订，逐字节重建当前稿成功。
- [x] 7 单元合并稿逐字等于最终分片拼接；JSON 数学、代码、结构、编号、块 ID、页标与图片守恒。
- [x] 参考文献 170 处只移动新增中文译题相邻句点；原英文和强调、183 个中文译题均保留。
- [x] 117 个独立网页查看证据文件指纹全部复算一致，旧阶段与泰勒增量之间的 6 字段差异严格闭合。
- [x] 固定当前 source/render/image 指纹，交由 root 更新验收记录。

## 原文语义复审与修订边界

`global-terminology-a-review.md` 由 root 完成，实际逐张查看 24 个相关原页，并核对 a 分片全部 36 行内容增量。`global-terminology-b-review.md` 由 prml_translate_a 完成，实际查看原 7 页及补充的 PDF299，共 8 页；逐项核对 b 原 9 行和后来追加的 3 行。两位 reviewer 均未初译所审分片。作者自检记录分别为 `global-terminology-a-author.md`、`global-terminology-b-author.md`，没有以作者自检代替独审。

| 改动 | 源页独审结果与限制 |
|---|---|
| 生成式／判别式 | 第 4、6、8、12、13 章在 generative／discriminative 的具体模型语境统一。PDF212 的 linear discriminant model 保留“线性判别模型”；普通“生成样本”等动作没有机械替换。 |
| 雅可比矩阵 | 第 5 章 a 的 16 处及 b 的 4 处 Jacobian 矩阵统一，首次正文保留英文；正反向传播、变量依赖与导数方向不变。 |
| 狄利克雷 | 第 8 章四处先验／分布用词对齐第 2 章，首次保留 Dirichlet，原图及参数定义不改。 |
| 格图 | 对照 PDF434 的 lattice／trellis 定义及第 13 章原页，a 的 14 处和 b 的 8 处均为沿时间展开的状态转移图；正文、图注和 alt 统一，原英文及图结构保留。 |
| 自联想映射 | PDF613 将重复谓语改为“这种网络形成的映射称为自联想映射”，保留命名对象、隐藏单元少于输入的条件及不能完美重建的限制。 |
| 泰勒展开（GB-01） | PDF299 的 Taylor series expansion 和 PDF306 两题的 Taylor expansion 共三处统一。非作者 reviewer 重新查看原页，并核对限定三处差异与全部 6 张新增双模式截图；问题关闭。 |
| 参考文献译题句点 | 170 处 `.〔中文译题〕` 改为 `〔中文译题〕.`；其余 13 条原样保留。此前全部 183 条 a 书目的原页独审继续有效，本轮只处理新增译题的呈现位置。 |

active／inactive 的附录 E 与索引修订分别在 `appendix-e-review.md` 和 `index-b-review.md` 中关闭；它们不被重计为本轮 7 单元改动。目录标题与导航由单独的目录终审处理。

## 本人实际执行的独立守恒检查

执行脚本为 `tmp/prml-review/global/verify_increment.py`，输出 `increment-verification.json`。它不编辑源稿、JSON 或图片，也不调用作者修改脚本。以修改前原字节快照为起点，重新逐文件应用限定的词项／句子／句点规则，所得字节与当前 9 份分片完全一致；计 218 个改动源行，其中 170 行为书目格式。原换行风格没有被全文件转换。

全部 3,723 个源数学串及顺序不变，页标／跨页接段 marker 与合法 HTML 标签结构保持。参考文献移除新增中文括注后的整份英文、标点和格式源码逐字相等，全部 183 个中文译题也逐字相等；em／strong 内容与范围不变。共 109 张相关作者图片已逐文件重新计算 SHA，与修订前清单相同。

整合层对 7 单元逐个检查：当前合并稿等于 a/b 分片按既定规则拼接；旧已审 JSON 与当前 JSON 的所有叶节点路径一致，全部变化只在准许的文字字段，共 276 字段（含 text/segments 的重复表示和书目 HTML）。数学／代码节点逐对象相等，其他结构、块 ID、页标、标题层级、编号及图像路径不变；当前整章图片指纹与修订前已验收指纹一致。独立复算的差异清单及三重指纹与更新后的 `global-delta-qa.json` 完全吻合。

`content-qa-global-delta.json` 中第 5 章属于泰勒修复之前的版本，不能单独代表最终第 5 章；最终该章以 `content-qa-taylor.json` 及当前增量证明补齐。其他六个单元的结构检查仍绑定当前版本。此阶段说明避免把旧 QA 的 passed 标记不加区分地沿用。

## 独立网页证据与阶段闭合

| 实际查看者 | 实际覆盖 | 文件版本数 | 记录 |
|---|---|---:|---|
| prml_translate_b | 未由其初译的 a 内容全部 35 个改动块，参考文献 6 条格式代表；1440 浅色／390 深色及必要横移／续屏，含 2 张绘制时序复查 | 90 | `global-ui-a-parts-review.md` |
| root | 未由其初译的 b 原有全部 9 个改动块，两模式及图 13.16 横移／长段续屏 | 21 | `global-ui-b-parts-review.md` |
| prml_translate_a | 未由其初译的 b 新增三个泰勒术语块，全部两模式 | 6 | `global-terminology-b-review.md` 的 GB-01 附录 |

本总审亲自读取这些记录，并重新计算全部 117 个截图文件的 SHA，全部与各自实际查看记录相符；完整核验清单为 `tmp/prml-review/global/independent-ui-evidence-rehashed.json`。书目网页人工检查明确是 6 条代表，全部 170 条的内容／格式守恒采用独立逐条结构比较，没有将抽样扩大为逐条网页目视。

第 5 章旧截图快照至最终 JSON 的变化严格为三个块的六个字段，只把 Taylor 展开及相邻空格改为泰勒展开；数学和其他内容完全相同。本人独立复算该差异并与 `taylor-delta-qa.json` 相等，另五个 a 截图单元的去状态 JSON 与当前逐对象相等。原 GU-A01 是邻近公式绘制时序证据缺口，追加稳定截图已关闭，没有内容修补。当前没有遗留语义或网页问题。

## 当前验收指纹

以下三重指纹由本总审独立复算；允许 root 将原逐章完整审查与本增量报告共同绑定到这些版本。全部 9 分片的 raw/LF 指纹及报告文件指纹另存 `tmp/prml-review/global/increment-verification.json`。

| 单元 | sourceNormalizedSha256 | renderedContentSha256 | imagesSha256 |
|---|---|---|---|
| chapter-04 | `bb9130ea6047c9cbf72fecc768f5ececc6597891c63b91b43f2bb438582aef0f` | `d52b6e8ddf333ad97b83b4b93b9608c32ddb61ee1063708069833d3b78542328` | `6ccdc62baf5ded80114be88720082ba461733dc1f09e6eb2e4310f7d70cc30ae` |
| chapter-05 | `86d176447cd5ca6a722ea8ff20c07fe22902c5ee3a3dcab579215d69ea0e848e` | `8351fbc88cd7be5e96d14c7a6c90f91522282a2c306d77341c394ced1081c3d3` | `82c4ebb836c18944be6bf7e9e6d5a43cbfe7f8d87c4cb821267831c6a543bbe5` |
| chapter-06 | `31b710aa3db87acebb4a444ab3bd8275f51026ceba5827a95ccddc5949884080` | `209e9f4cb107e4a26b543a7579ef5a9108e5cdcc9d480b37d69c8d90b827f193` | `f2989e6bb8d7d519fd3c1901f373b22b78ed632be0f40a78f39b524292ccae62` |
| chapter-08 | `878e81ddc6642a7adb6b9eb23723969404653d3a9e4617959a792d7d0013b1c3` | `66f86d8127626a8251be8f3adfe08c87bdb17375bc97f9807736f43117f895b5` | `0e993a5c1fb3fabe561f8f6be1a1a849a0a11ac3f855727ac8813526a07d9fe0` |
| chapter-12 | `b6de66774fe90ae65b8cbb5fdd37611b133ffe4e8fb3fbe0e21bc5ebc6dbdbd7` | `35124a771ec9227f6a8e9ade2a928bf5800c8639df96e3496f5e4f3bd3b45a62` | `04a759b0addbefbda6855dd5e8989d71dc975bfbcdf5aa2906fc05280bcb02a3` |
| chapter-13 | `7a3e655c7d422a16dd1e391d275ff9832eb02b79ad4edad46ea21c08ab96fbe8` | `644b2f2598c8a7b2b985a9e89ca937323909d02b220097a41cf528ba2a4a0d43` | `e411a39da2957ee19016e30644b49f3aa4c36f80c0b27ca00aaea0992b8867fd` |
| references | `06993aaa4eeea1a892bef925a2b219430bcc7089d36c9d720bc1e413c8a9eb35` | `77a412ab80da394e2b71d5ea2646829d857385ca04e4293ba1b3018d5f94557c` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

本结论完成本轮 7 单元增量验收；全书最终目录、公共入口、跨章导航及离线行为仍需后续整体报告核验。
