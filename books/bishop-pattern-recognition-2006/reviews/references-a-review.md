# 参考文献 a 分片独立审查

状态：**PDF 731–738 的源文与译文独审通过**；本报告不代替 b、整合 JSON 或网页验收。审查者 root 未参与此分片初译。

root 实际重新打开四张双页原图 pair-731/733/735/737，按每页左栏至右栏逐条对照最终译稿。183 条书目及 183 个中文题名完整；逐页起点数为 16、23、20、26、27、25、23、23。没有新增原书不存在的书目，没有以网络书目或印象改写信息。

逐项检查了作者及其顺序、姓名字形、年份/后缀、原题与译题、编辑者、期刊/会议/书名、卷期、页码、出版社/地点、版次、报告/学位信息和附注。中文题名忠实且可理解，技术术语未引入语义变化。论文标题正体、书刊及会议录标题斜体、原卷号粗体均按原页核对；Elkan 题名的 k 保留斜体。

731→732 的 Attias (1999b) 为唯一跨页续条，使用 join 标记，未把续行算新书目。733 的 VIBES、738 的 Hinton 等 (2001) 跨栏续行均完整。738 末 Ito (1991) 完整结束，与 b 首条 Jaakkola / Jordan (2000) 不合并。本分片无图片、表格、显示公式、习题、代码或脚注。

原印细节另核：Attias 的 Fifth Conference；Besag 的 Hidgon/Megersen；Bishop 等 (1997a) 的 Petche；Bishop/Nabney (2008) 的 In preparation；Blei 的 J. M. B. et al. (Ed.)；Box 的 Tao；Cardoso 的 9(10)；Dawid 的卷 4；Cover/Hart 的 IT-11；Feynman 的 Lectures of Physics；Frey/MacKay 无页码及 M. J. Kearns；Ghahramani/Jordan 的 appproach；Golub 的 John Hopkins；Hastie/Stuetzle 的 84(106)。全部保持本书所印内容，没有用常见拼写或外部年份替换。另实际查看 4 倍局部 page-735-accents.png，确认 Csiszàr/Tusnàdy 为原印 grave à，不能据通常人名写法改作 á。

最终审过快照在 `tmp/prml-root-review/references/reviewed-a-final.md`；四张实际原页查看记录及 SHA 在同目录 `viewed-a-pages.json`。源码原始字节及 LF SHA-256 均为 `541c4ef760046754b4a5f1903b69829afa57bb1a90252085be807addf9b9f18e`。源页/题名/字段/格式未发现遗留问题，后续由另一 reviewer 核整合 JSON、续段守恒，并由 root 检查整份书目网页。

## RA-01 跨章术语修复复核

整合审查发现 Adler (1981) 的 over-relaxation 译“超松弛”，与第11章首次解释和Neal(1999)有序过松弛不一致。作者a仅将“用超松弛方法”改为“用过松弛方法”。root反向替换后与审过旧稿字节完全相同（同为44290字节），英文和强调无任何变化；旧快照保留为reviewed-a-before-RA01.md，新快照为reviewed-a-final.md，限定差异证据见RA01-diff.json。最终raw/LF SHA-256为 `e4d0f1bdfacb09c855edbd8bcc4d981d665ca784005dca4fa8eea6ced0b1120e`。修复复核通过，排版增量在整份网页报告中记录。
