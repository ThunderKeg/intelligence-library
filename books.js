// Each book points to its own text content file.
const books = [
  {
    id: "bishop-deep-learning-2024",
    title: "深度学习：基础与概念",
    originalTitle: "Deep Learning: Foundations and Concepts",
    author: "Christopher M. Bishop · Hugh Bishop",
    year: "2024",
    description: "《深度学习：基础与概念》中文译文",
    legacyPageChapter: "01",
    referenceIndex: "books/bishop-deep-learning-2024/reference-index.json",
    referencePreview: true,
    offlineImages: "books/bishop-deep-learning-2024/offline-images.json",
    chapters: [
      { id: "frontmatter", number: "", title: "封面与出版信息", content: "books/bishop-deep-learning-2024/frontmatter.json" },
      { id: "00", number: "序", title: "前言", content: "books/bishop-deep-learning-2024/chapter-00.json" },
      { id: "contents", number: "", title: "原书目录", content: "books/bishop-deep-learning-2024/contents.json" },
      { id: "01", number: "1", title: "深度学习革命", content: "books/bishop-deep-learning-2024/chapter-01.json" },
      { id: "02", number: "2", title: "概率", content: "books/bishop-deep-learning-2024/chapter-02.json" },
      { id: "03", number: "3", title: "标准分布", content: "books/bishop-deep-learning-2024/chapter-03.json" },
      { id: "04", number: "4", title: "单层网络：回归", content: "books/bishop-deep-learning-2024/chapter-04.json" },
      { id: "05", number: "5", title: "单层网络：分类", content: "books/bishop-deep-learning-2024/chapter-05.json" },
      { id: "06", number: "6", title: "深层神经网络", content: "books/bishop-deep-learning-2024/chapter-06.json" },
      { id: "07", number: "7", title: "梯度下降", content: "books/bishop-deep-learning-2024/chapter-07.json" },
      { id: "08", number: "8", title: "反向传播", content: "books/bishop-deep-learning-2024/chapter-08.json" },
      { id: "09", number: "9", title: "正则化", content: "books/bishop-deep-learning-2024/chapter-09.json" },
      { id: "10", number: "10", title: "卷积网络", content: "books/bishop-deep-learning-2024/chapter-10.json" },
      { id: "11", number: "11", title: "结构化分布", content: "books/bishop-deep-learning-2024/chapter-11.json" },
      { id: "12", number: "12", title: "Transformer", content: "books/bishop-deep-learning-2024/chapter-12.json" },
      { id: "13", number: "13", title: "图神经网络", content: "books/bishop-deep-learning-2024/chapter-13.json" },
      { id: "14", number: "14", title: "采样", content: "books/bishop-deep-learning-2024/chapter-14.json" },
      { id: "15", number: "15", title: "离散潜变量", content: "books/bishop-deep-learning-2024/chapter-15.json" },
      { id: "16", number: "16", title: "连续潜变量", content: "books/bishop-deep-learning-2024/chapter-16.json" },
      { id: "17", number: "17", title: "生成对抗网络", content: "books/bishop-deep-learning-2024/chapter-17.json" },
      { id: "18", number: "18", title: "归一化流", content: "books/bishop-deep-learning-2024/chapter-18.json" },
      { id: "19", number: "19", title: "自编码器", content: "books/bishop-deep-learning-2024/chapter-19.json" },
      { id: "20", number: "20", title: "扩散模型", content: "books/bishop-deep-learning-2024/chapter-20.json" },
      { id: "A", number: "附录 A", title: "线性代数", content: "books/bishop-deep-learning-2024/appendix-a.json" },
      { id: "B", number: "附录 B", title: "变分法", content: "books/bishop-deep-learning-2024/appendix-b.json" },
      { id: "C", number: "附录 C", title: "拉格朗日乘子", content: "books/bishop-deep-learning-2024/appendix-c.json" },
      { id: "bibliography", number: "", title: "参考文献", content: "books/bishop-deep-learning-2024/bibliography.json" },
      { id: "index", number: "", title: "索引", content: "books/bishop-deep-learning-2024/index.json" },
    ],
  },
  {
    "id": "bishop-pattern-recognition-2006",
    "title": "模式识别与机器学习",
    "originalTitle": "Pattern Recognition and Machine Learning",
    "author": "Christopher M. Bishop",
    "year": "2006",
    "description": "《模式识别与机器学习》中文译文",
    "referenceIndex": "books/bishop-pattern-recognition-2006/reference-index.json",
    "offlineImages": "books/bishop-pattern-recognition-2006/offline-images.json",
    "chapters": [
      {
        "id": "frontmatter",
        "number": "",
        "title": "封面与出版信息",
        "content": "books/bishop-pattern-recognition-2006/frontmatter.json"
      },
      {
        "id": "preface",
        "number": "",
        "title": "前言",
        "content": "books/bishop-pattern-recognition-2006/preface.json"
      },
      {
        "id": "notation",
        "number": "",
        "title": "数学记号",
        "content": "books/bishop-pattern-recognition-2006/notation.json"
      },
      {
        "id": "contents",
        "number": "",
        "title": "原书目录",
        "content": "books/bishop-pattern-recognition-2006/contents.json"
      },
      {
        "id": "chapter-01",
        "number": "1",
        "title": "绪论",
        "content": "books/bishop-pattern-recognition-2006/chapter-01.json"
      },
      {
        "id": "chapter-02",
        "number": "2",
        "title": "概率分布",
        "content": "books/bishop-pattern-recognition-2006/chapter-02.json"
      },
      {
        "id": "chapter-03",
        "number": "3",
        "title": "用于回归的线性模型",
        "content": "books/bishop-pattern-recognition-2006/chapter-03.json"
      },
      {
        "id": "chapter-04",
        "number": "4",
        "title": "用于分类的线性模型",
        "content": "books/bishop-pattern-recognition-2006/chapter-04.json"
      },
      {
        "id": "chapter-05",
        "number": "5",
        "title": "神经网络",
        "content": "books/bishop-pattern-recognition-2006/chapter-05.json"
      },
      {
        "id": "chapter-06",
        "number": "6",
        "title": "核方法",
        "content": "books/bishop-pattern-recognition-2006/chapter-06.json"
      },
      {
        "id": "chapter-07",
        "number": "7",
        "title": "稀疏核机器",
        "content": "books/bishop-pattern-recognition-2006/chapter-07.json"
      },
      {
        "id": "chapter-08",
        "number": "8",
        "title": "图模型",
        "content": "books/bishop-pattern-recognition-2006/chapter-08.json"
      },
      {
        "id": "chapter-09",
        "number": "9",
        "title": "混合模型与 EM",
        "content": "books/bishop-pattern-recognition-2006/chapter-09.json"
      },
      {
        "id": "chapter-10",
        "number": "10",
        "title": "近似推断",
        "content": "books/bishop-pattern-recognition-2006/chapter-10.json"
      },
      {
        "id": "chapter-11",
        "number": "11",
        "title": "采样方法",
        "content": "books/bishop-pattern-recognition-2006/chapter-11.json"
      },
      {
        "id": "chapter-12",
        "number": "12",
        "title": "连续潜变量",
        "content": "books/bishop-pattern-recognition-2006/chapter-12.json"
      },
      {
        "id": "chapter-13",
        "number": "13",
        "title": "序列数据",
        "content": "books/bishop-pattern-recognition-2006/chapter-13.json"
      },
      {
        "id": "chapter-14",
        "number": "14",
        "title": "模型组合",
        "content": "books/bishop-pattern-recognition-2006/chapter-14.json"
      },
      {
        "id": "appendix-a",
        "number": "附录 A",
        "title": "数据集",
        "content": "books/bishop-pattern-recognition-2006/appendix-a.json"
      },
      {
        "id": "appendix-b",
        "number": "附录 B",
        "title": "概率分布",
        "content": "books/bishop-pattern-recognition-2006/appendix-b.json"
      },
      {
        "id": "appendix-c",
        "number": "附录 C",
        "title": "矩阵的性质",
        "content": "books/bishop-pattern-recognition-2006/appendix-c.json"
      },
      {
        "id": "appendix-d",
        "number": "附录 D",
        "title": "变分法",
        "content": "books/bishop-pattern-recognition-2006/appendix-d.json"
      },
      {
        "id": "appendix-e",
        "number": "附录 E",
        "title": "拉格朗日乘子",
        "content": "books/bishop-pattern-recognition-2006/appendix-e.json"
      },
      {
        "id": "references",
        "number": "",
        "title": "参考文献",
        "content": "books/bishop-pattern-recognition-2006/references.json"
      },
      {
        "id": "index",
        "number": "",
        "title": "索引",
        "content": "books/bishop-pattern-recognition-2006/index.json"
      }
    ]
  },
  {
    id: "shannon-mathematical-theory-1948",
    title: "通信的数学理论",
    originalTitle: "A Mathematical Theory of Communication",
    author: "C. E. Shannon",
    year: "1948",
    description: "引言、五篇正文与七个附录的完整中文译文",
    chapters: [
      { id: "00", number: "序", title: "引言", content: "books/shannon-mathematical-theory-1948/chapter-00.json" },
      { id: "01", number: "I", title: "无噪离散系统", content: "books/shannon-mathematical-theory-1948/chapter-01.json" },
      { id: "02", number: "II", title: "有噪离散信道", content: "books/shannon-mathematical-theory-1948/chapter-02.json" },
      { id: "a1-a4", number: "附录", title: "1—4", content: "books/shannon-mathematical-theory-1948/chapter-a1-a4.json" },
      { id: "03", number: "III", title: "数学预备知识", content: "books/shannon-mathematical-theory-1948/chapter-03.json" },
      { id: "04", number: "IV", title: "连续信道", content: "books/shannon-mathematical-theory-1948/chapter-04.json" },
      { id: "05", number: "V", title: "连续信源的速率", content: "books/shannon-mathematical-theory-1948/chapter-05.json" },
      { id: "a5-a7", number: "附录", title: "5—7", content: "books/shannon-mathematical-theory-1948/chapter-a5-a7.json" },
    ],
  },
  {
    id: "sutton-barto-reinforcement-learning-2e",
    title: "强化学习：导论",
    originalTitle: "Reinforcement Learning: An Introduction",
    author: "Richard S. Sutton · Andrew G. Barto",
    year: "2018／2020",
    description: "卷首、三部分引言、17 章及书后材料的中文译编",
    referenceIndex: "books/sutton-barto-reinforcement-learning-2e/reference-index.json",
    offlineImages: "books/sutton-barto-reinforcement-learning-2e/offline-images.json",
    chapters: [
      { id: "00", number: "卷首", title: "目录、前言与记号表", content: "books/sutton-barto-reinforcement-learning-2e/chapter-00.json" },
      { id: "01", number: "1", title: "绪论", content: "books/sutton-barto-reinforcement-learning-2e/chapter-01.json" },
      { id: "I", number: "第一部分", title: "表格型求解方法", content: "books/sutton-barto-reinforcement-learning-2e/chapter-I.json" },
      { id: "02", number: "2", title: "多臂赌博机", content: "books/sutton-barto-reinforcement-learning-2e/chapter-02.json" },
      { id: "03", number: "3", title: "有限马尔可夫决策过程", content: "books/sutton-barto-reinforcement-learning-2e/chapter-03.json" },
      { id: "04", number: "4", title: "动态规划", content: "books/sutton-barto-reinforcement-learning-2e/chapter-04.json" },
      { id: "05", number: "5", title: "蒙特卡洛方法", content: "books/sutton-barto-reinforcement-learning-2e/chapter-05.json" },
      { id: "06", number: "6", title: "时序差分学习", content: "books/sutton-barto-reinforcement-learning-2e/chapter-06.json" },
      { id: "07", number: "7", title: "n 步自举", content: "books/sutton-barto-reinforcement-learning-2e/chapter-07.json" },
      { id: "08", number: "8", title: "用表格型方法规划与学习", content: "books/sutton-barto-reinforcement-learning-2e/chapter-08.json" },
      { id: "II", number: "第二部分", title: "近似求解方法", content: "books/sutton-barto-reinforcement-learning-2e/chapter-II.json" },
      { id: "09", number: "9", title: "用近似方法做同策略预测", content: "books/sutton-barto-reinforcement-learning-2e/chapter-09.json" },
      { id: "10", number: "10", title: "用近似方法做同策略控制", content: "books/sutton-barto-reinforcement-learning-2e/chapter-10.json" },
      { id: "11", number: "11", title: "带函数近似的异策略方法", content: "books/sutton-barto-reinforcement-learning-2e/chapter-11.json" },
      { id: "12", number: "12", title: "资格迹", content: "books/sutton-barto-reinforcement-learning-2e/chapter-12.json" },
      { id: "13", number: "13", title: "策略梯度方法", content: "books/sutton-barto-reinforcement-learning-2e/chapter-13.json" },
      { id: "III", number: "第三部分", title: "深入探讨", content: "books/sutton-barto-reinforcement-learning-2e/chapter-III.json" },
      { id: "14", number: "14", title: "心理学", content: "books/sutton-barto-reinforcement-learning-2e/chapter-14.json" },
      { id: "15", number: "15", title: "神经科学", content: "books/sutton-barto-reinforcement-learning-2e/chapter-15.json" },
      { id: "16", number: "16", title: "应用与案例研究", content: "books/sutton-barto-reinforcement-learning-2e/chapter-16.json" },
      { id: "17", number: "17", title: "前沿问题", content: "books/sutton-barto-reinforcement-learning-2e/chapter-17.json" },
      { id: "REF", number: "书后", title: "参考文献", content: "books/sutton-barto-reinforcement-learning-2e/chapter-REF.json" },
      { id: "IDX", number: "书后", title: "索引", content: "books/sutton-barto-reinforcement-learning-2e/chapter-IDX.json" },
      { id: "SERIES", number: "书后", title: "系列书目", content: "books/sutton-barto-reinforcement-learning-2e/chapter-SERIES.json" },
    ],
  },
  {
    id: "mackay-information-theory-2003",
    title: "信息论、推断与学习算法",
    originalTitle: "Information Theory, Inference, and Learning Algorithms",
    author: "David J. C. MacKay",
    year: "2003／2005",
    description: "前置内容、第 1–50 章、相关导页、七部分扉页、附录 A–C、参考文献、索引及神经网络后记中文译文",
    referenceIndex: "books/mackay-information-theory-2003/reference-index.json",
    offlineImages: "books/mackay-information-theory-2003/offline-images.json",
    chapters: [
      { id: "00", number: "前置", title: "前言与第一章预备知识", content: "books/mackay-information-theory-2003/chapter-00.json" },
      { id: "01", number: "1", title: "信息论导论", content: "books/mackay-information-theory-2003/chapter-01.json" },
      { id: "02", number: "2", title: "概率、熵与推断", content: "books/mackay-information-theory-2003/chapter-02.json" },
      { id: "03-intro", number: "导页", title: "关于第 3 章", content: "books/mackay-information-theory-2003/chapter-03-intro.json" },
      { id: "03", number: "3", title: "进一步讨论推断", content: "books/mackay-information-theory-2003/chapter-03.json" },
      { id: "I", number: "第一部分", title: "数据压缩", content: "books/mackay-information-theory-2003/chapter-I.json" },
      { id: "04-intro", number: "导页", title: "关于第 4 章", content: "books/mackay-information-theory-2003/chapter-04-intro.json" },
      { id: "04", number: "4", title: "信源编码定理", content: "books/mackay-information-theory-2003/chapter-04.json" },
      { id: "05-intro", number: "导页", title: "关于第 5 章", content: "books/mackay-information-theory-2003/chapter-05-intro.json" },
      { id: "05", number: "5", title: "符号编码", content: "books/mackay-information-theory-2003/chapter-05.json" },
      { id: "06-intro", number: "导页", title: "关于第 6 章", content: "books/mackay-information-theory-2003/chapter-06-intro.json" },
      { id: "06", number: "6", title: "流编码", content: "books/mackay-information-theory-2003/chapter-06.json" },
      { id: "07", number: "7", title: "整数编码", content: "books/mackay-information-theory-2003/chapter-07.json" },
      { id: "II", number: "第二部分", title: "有噪信道编码", content: "books/mackay-information-theory-2003/chapter-II.json" },
      { id: "08", number: "8", title: "相依随机变量", content: "books/mackay-information-theory-2003/chapter-08.json" },
      { id: "09-intro", number: "导页", title: "关于第 9 章", content: "books/mackay-information-theory-2003/chapter-09-intro.json" },
      { id: "09", number: "9", title: "有噪信道上的通信", content: "books/mackay-information-theory-2003/chapter-09.json" },
      { id: "10-intro", number: "导页", title: "关于第 10 章", content: "books/mackay-information-theory-2003/chapter-10-intro.json" },
      { id: "10", number: "10", title: "有噪信道编码定理", content: "books/mackay-information-theory-2003/chapter-10.json" },
      { id: "11-intro", number: "导页", title: "关于第 11 章", content: "books/mackay-information-theory-2003/chapter-11-intro.json" },
      { id: "11", number: "11", title: "纠错码与实值信道", content: "books/mackay-information-theory-2003/chapter-11.json" },
      { id: "III", number: "第三部分", title: "信息论的更多主题", content: "books/mackay-information-theory-2003/chapter-III.json" },
      { id: "12-intro", number: "导页", title: "关于第 12 章", content: "books/mackay-information-theory-2003/chapter-12-intro.json" },
      { id: "12", number: "12", title: "哈希码：用于高效信息检索的编码", content: "books/mackay-information-theory-2003/chapter-12.json" },
      { id: "13-intro", number: "导页", title: "关于第 13 章", content: "books/mackay-information-theory-2003/chapter-13-intro.json" },
      { id: "13", number: "13", title: "二元码", content: "books/mackay-information-theory-2003/chapter-13.json" },
      { id: "14-intro", number: "导页", title: "关于第 14 章", content: "books/mackay-information-theory-2003/chapter-14-intro.json" },
      { id: "14", number: "14", title: "存在非常好的线性码", content: "books/mackay-information-theory-2003/chapter-14.json" },
      { id: "15", number: "15", title: "信息论补充习题", content: "books/mackay-information-theory-2003/chapter-15.json" },
      { id: "16", number: "16", title: "消息传递", content: "books/mackay-information-theory-2003/chapter-16.json" },
      { id: "17", number: "17", title: "受约束的无噪信道上的通信", content: "books/mackay-information-theory-2003/chapter-17.json" },
      { id: "18", number: "18", title: "填字游戏与密码破解", content: "books/mackay-information-theory-2003/chapter-18.json" },
      { id: "19", number: "19", title: "为什么有性生殖？信息获取与进化", content: "books/mackay-information-theory-2003/chapter-19.json" },
      { id: "IV", number: "第四部分", title: "概率与推断", content: "books/mackay-information-theory-2003/chapter-IV.json" },
      { id: "IV-intro", number: "导页", title: "关于第四部分", content: "books/mackay-information-theory-2003/chapter-IV-intro.json" },
      { id: "20", number: "20", title: "一个推断任务示例：聚类", content: "books/mackay-information-theory-2003/chapter-20.json" },
      { id: "21", number: "21", title: "通过完全枚举进行精确推断", content: "books/mackay-information-theory-2003/chapter-21.json" },
      { id: "22", number: "22", title: "最大似然与聚类", content: "books/mackay-information-theory-2003/chapter-22.json" },
      { id: "23", number: "23", title: "常用的概率分布", content: "books/mackay-information-theory-2003/chapter-23.json" },
      { id: "24", number: "24", title: "精确边缘化", content: "books/mackay-information-theory-2003/chapter-24.json" },
      { id: "25", number: "25", title: "格形图中的精确边缘化", content: "books/mackay-information-theory-2003/chapter-25.json" },
      { id: "26", number: "26", title: "图中的精确边缘化", content: "books/mackay-information-theory-2003/chapter-26.json" },
      { id: "27", number: "27", title: "拉普拉斯方法", content: "books/mackay-information-theory-2003/chapter-27.json" },
      { id: "28", number: "28", title: "模型比较与奥卡姆剃刀", content: "books/mackay-information-theory-2003/chapter-28.json" },
      { id: "29-intro", number: "导页", title: "关于第 29 章", content: "books/mackay-information-theory-2003/chapter-29-intro.json" },
      { id: "29", number: "29", title: "蒙特卡罗方法", content: "books/mackay-information-theory-2003/chapter-29.json" },
      { id: "30", number: "30", title: "高效蒙特卡罗方法", content: "books/mackay-information-theory-2003/chapter-30.json" },
      { id: "31-intro", number: "导页", title: "关于第 31 章", content: "books/mackay-information-theory-2003/chapter-31-intro.json" },
      { id: "31", number: "31", title: "Ising 模型", content: "books/mackay-information-theory-2003/chapter-31.json" },
      { id: "32", number: "32", title: "精确蒙特卡罗采样", content: "books/mackay-information-theory-2003/chapter-32.json" },
      { id: "33", number: "33", title: "变分方法", content: "books/mackay-information-theory-2003/chapter-33.json" },
      { id: "34", number: "34", title: "独立成分分析与隐变量建模", content: "books/mackay-information-theory-2003/chapter-34.json" },
      { id: "35", number: "35", title: "若干推断专题", content: "books/mackay-information-theory-2003/chapter-35.json" },
      { id: "36", number: "36", title: "决策理论", content: "books/mackay-information-theory-2003/chapter-36.json" },
      { id: "37", number: "37", title: "贝叶斯推断与抽样理论", content: "books/mackay-information-theory-2003/chapter-37.json" },
      { id: "V", number: "第五部分", title: "神经网络", content: "books/mackay-information-theory-2003/chapter-V.json" },
      { id: "38", number: "38", title: "神经网络导论", content: "books/mackay-information-theory-2003/chapter-38.json" },
      { id: "39", number: "39", title: "作为分类器的单个神经元", content: "books/mackay-information-theory-2003/chapter-39.json" },
      { id: "40-prelude", number: "导页", title: "阅读第 40 章之前的习题", content: "books/mackay-information-theory-2003/chapter-40-prelude.json" },
      { id: "40", number: "40", title: "单个神经元的容量", content: "books/mackay-information-theory-2003/chapter-40.json" },
      { id: "41", number: "41", title: "将学习视为推断", content: "books/mackay-information-theory-2003/chapter-41.json" },
      { id: "41-postscript", number: "后记", title: "有监督神经网络附记", content: "books/mackay-information-theory-2003/chapter-41-postscript.json" },
      { id: "42", number: "42", title: "Hopfield 网络", content: "books/mackay-information-theory-2003/chapter-42.json" },
      { id: "43", number: "43", title: "玻尔兹曼机", content: "books/mackay-information-theory-2003/chapter-43.json" },
      { id: "44", number: "44", title: "多层网络中的监督学习", content: "books/mackay-information-theory-2003/chapter-44.json" },
      { id: "45-prelude", number: "导页", title: "关于第 45 章", content: "books/mackay-information-theory-2003/chapter-45-prelude.json" },
      { id: "45", number: "45", title: "高斯过程", content: "books/mackay-information-theory-2003/chapter-45.json" },
      { id: "46", number: "46", title: "去卷积", content: "books/mackay-information-theory-2003/chapter-46.json" },
      { id: "VI", number: "第六部分", title: "稀疏图码", content: "books/mackay-information-theory-2003/chapter-VI.json" },
      { id: "VI-intro", number: "导页", title: "关于第六部分", content: "books/mackay-information-theory-2003/chapter-VI-intro.json" },
      { id: "47", number: "47", title: "低密度奇偶校验码", content: "books/mackay-information-theory-2003/chapter-47.json" },
      { id: "48", number: "48", title: "卷积码与 Turbo 码", content: "books/mackay-information-theory-2003/chapter-48.json" },
      { id: "49", number: "49", title: "重复—累积码", content: "books/mackay-information-theory-2003/chapter-49.json" },
      { id: "50-intro", number: "导页", title: "关于第 50 章", content: "books/mackay-information-theory-2003/chapter-50-intro.json" },
      { id: "50", number: "50", title: "数字喷泉码", content: "books/mackay-information-theory-2003/chapter-50.json" },
      { id: "VII", number: "第七部分", title: "附录", content: "books/mackay-information-theory-2003/chapter-VII.json" },
      { id: "A", number: "附录 A", title: "记号", content: "books/mackay-information-theory-2003/chapter-A.json" },
      { id: "B", number: "附录 B", title: "一些物理学知识", content: "books/mackay-information-theory-2003/chapter-B.json" },
      { id: "C", number: "附录 C", title: "一些数学知识", content: "books/mackay-information-theory-2003/chapter-C.json" },
      { id: "REF", number: "书后", title: "参考文献", content: "books/mackay-information-theory-2003/chapter-REF.json" },
      { id: "IDX", number: "书后", title: "索引", content: "books/mackay-information-theory-2003/chapter-IDX.json" },
    ],
  },
  {
    "id": "boyd-vandenberghe-convex-optimization-2004",
    "title": "凸优化",
    "originalTitle": "Convex Optimization",
    "author": "Stephen Boyd · Lieven Vandenberghe",
    "year": "2004",
    "description": "《凸优化》中文译文",
    "offlineImages": "books/boyd-vandenberghe-convex-optimization-2004/offline-images.json",
    "chapters": [
      {
        "id": "frontmatter",
        "number": "",
        "title": "书名、出版信息与献词",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-frontmatter.json"
      },
      {
        "id": "contents",
        "number": "",
        "title": "原书目录",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-contents.json"
      },
      {
        "id": "preface",
        "number": "",
        "title": "前言",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-preface.json"
      },
      {
        "id": "01",
        "number": "1",
        "title": "绪论",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-01.json"
      },
      {
        "id": "part-I",
        "number": "",
        "title": "第一部分 理论",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-part-I.json"
      },
      {
        "id": "02",
        "number": "2",
        "title": "凸集",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-02.json"
      },
      {
        "id": "03",
        "number": "3",
        "title": "凸函数",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-03.json"
      },
      {
        "id": "04",
        "number": "4",
        "title": "凸优化问题",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-04.json"
      },
      {
        "id": "05",
        "number": "5",
        "title": "对偶性",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-05.json"
      },
      {
        "id": "part-II",
        "number": "",
        "title": "第二部分 应用",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-part-II.json"
      },
      {
        "id": "06",
        "number": "6",
        "title": "逼近与拟合",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-06.json"
      },
      {
        "id": "07",
        "number": "7",
        "title": "统计估计",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-07.json"
      },
      {
        "id": "08",
        "number": "8",
        "title": "几何问题",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-08.json"
      },
      {
        "id": "part-III",
        "number": "",
        "title": "第三部分 算法",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-part-III.json"
      },
      {
        "id": "09",
        "number": "9",
        "title": "无约束最小化",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-09.json"
      },
      {
        "id": "10",
        "number": "10",
        "title": "等式约束最小化",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-10.json"
      },
      {
        "id": "11",
        "number": "11",
        "title": "内点法",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-11.json"
      },
      {
        "id": "appendices",
        "number": "",
        "title": "附录",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-appendices.json"
      },
      {
        "id": "A",
        "number": "附录 A",
        "title": "数学基础",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-A.json"
      },
      {
        "id": "B",
        "number": "附录 B",
        "title": "涉及两个二次函数的问题",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-B.json"
      },
      {
        "id": "C",
        "number": "附录 C",
        "title": "数值线性代数基础",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-C.json"
      },
      {
        "id": "references",
        "number": "",
        "title": "参考文献",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-references.json"
      },
      {
        "id": "notation",
        "number": "",
        "title": "符号表",
        "content": "books/boyd-vandenberghe-convex-optimization-2004/chapter-notation.json"
      }
    ]
  },
];
