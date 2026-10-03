# 全书修订复核：卷首、第 7 章术语与第 10 章导读

复核范围：`frontmatter/page-08.md`、`page-09.md`、`page-14.md` 至 `page-16.md`，`translation/chapter-07/page-141.md` 至 `page-157.md`，以及 `translation/chapter-10/page-243.md` 的导读。以仓库原书 PDF 可视页面和 `TERMS.md` 为依据；另核对卷首第 15、16 页源稿与 `chapter-00.json`，以及第 10 章导读在网站桌面、窄屏、浅色及深色模式下的显示。此文件只记录复核结果，不代表以上页面已完成全章审查。

## 修订复核结论

**通过，无残余问题。** `frontmatter/page-15.md` 已将原文 *Monte Carlo Tree Search* 译为“蒙特卡洛树搜索”；`frontmatter/page-16.md:3` 已将 *off-policy Monte Carlo methods* 译为“异策略蒙特卡洛方法”。两处均与原书 PDF 物理页 16 的可视文字相符，“蒙特卡洛”与卷首目录一致，后一处的“异策略”也符合 `TERMS.md:20`。原书的 *Monte Carlo Tree Search* 位于物理页 16，但属于物理页 15 开始的连续段落；完整段落归入 `page-15.md`，接续关系正确。`chapter-00.json` 中对应第 15 页的 4 个阅读块、第 16 页的 3 个阅读块与源稿逐块文字一致，均不含“蒙特卡罗”。

## 通过项

- **原书目录的策略术语：**对照 PDF 物理页 8–9，`frontmatter/page-08.md` 的 5.5、5.7、6.4、6.5 节，及 `page-09.md` 的 7.3、7.5 节和第 9 章标题，`on-policy`／`off-policy` 分别对应“同策略”／“异策略”；章节号、页码和选读节标记与原页一致。第 7 章标题的 `bootstrapping` 译为“自举”，符合 `TERMS.md:21`。
- **卷首前言的策略术语：**对照 PDF 物理页 14、16，`frontmatter/page-14.md` 中两处 *off-policy learning* 和 `page-16.md:3` 中 *off-policy Monte Carlo methods*、*off-policy learning* 均译为“异策略”，没有把目标策略与行为策略混淆。
- **第 7 章：**对照 PDF 印刷页 141、148–157 的相应章首、7.3–7.7 节、算法框、图注及习题，当前 `page-141.md` 至 `page-157.md` 可检出 28 处“异策略”，未检出“离策略”；逐处语境均对应原文 *off-policy* 或对其方法的准确指称。现稿的可检出数量为 28，复核结果按当前文件记录。
- **第 10 章导读：**`translation/chapter-10/page-243.md:3` 与 PDF 印刷页 243 的章首结构吻合：先从状态价值扩展到动作价值及回合式半梯度 Sarsa，再讨论山地车结果、持续式任务中的平均奖励和差分价值。图 10.3、10.4 确实比较一步与多步方法，故导读没有超出本章内容；`> 导读：` 与译文正文明确区分。
- **网页导读样式：**生成的 `chapter-10.json` 将导读保留为独立的 `intro` 块；网站实际渲染为 `reading-intro`。在 1280×900 桌面浅色及 390×844 窄屏浅色、深色模式中，导读有独立底色和左侧边线，文字可读，未见水平溢出（窄屏文档宽度与视口同为 390 px）。
