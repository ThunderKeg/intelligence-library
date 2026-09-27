// Each book points to its own text content file.
const books = [
  {
    id: "bishop-deep-learning-2024",
    title: "深度学习：基础与概念",
    originalTitle: "Deep Learning: Foundations and Concepts",
    author: "Christopher M. Bishop · Hugh Bishop",
    year: "2024",
    description: "第 1 章《深度学习革命》中文译文",
    chapters: [
      { id: "01", number: "1", title: "深度学习革命", content: "books/bishop-deep-learning-2024/chapter-01.json" },
    ],
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
];
