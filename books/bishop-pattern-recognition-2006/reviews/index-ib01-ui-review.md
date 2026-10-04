# 索引 IB-01 增量排版复核

root 独立复核通过。作者 b 将 PDF758 的 undetermined multiplier 中文词统一为附录 E 已用的“未定乘子”。最终 b 分片 raw/LF SHA 为 `f41a736308eefaa258d0624c66f816ab66a08186a0cd26195d58e33d616e5df8`。

root 重建索引后，在 1440px 浅色和 390px 深色下为 `p10-b004` 重新截图，并实际逐张查看两张图。中文词、英文、斜体“参见”和拉格朗日乘子链接均完整，窄屏正常换行，无新排版问题。自动报告为 `reader-qa-index-targets-ib01.json`；截图路径、SHA 及最终 source/render 指纹见 `index-ib01-qa.json`。

独立守恒验证将当前源稿和唯一改动 HTML 块中的这一字反向恢复后，与此前 56 张实际查看截图及 194 次跳转所绑定的 source/render/image 指纹全部严格相等。因此原 `index-ui-review.md` 和 `index-navigation-qa.json` 的未改动部分仍有效；1097 个 href 均未改变。此处没有把旧截图说成重新生成，也没有把未重跑的点击计为新点击。

最终结构／MathML 检查见 `content-qa-index-final.json`，通过。本增量仅覆盖 IB-01，索引全部条目的原文语义审查见 a/b 独审报告。
