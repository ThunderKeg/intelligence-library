// The shelf is a manifest. Reading content lives in one JSON file per book.
const books = [
  {
    id: "bishop-deep-learning-2024",
    title: "深度学习：基础与概念",
    originalTitle: "Deep Learning: Foundations and Concepts",
    author: "Christopher M. Bishop · Hugh Bishop",
    category: "Machine Learning",
    year: "2024",
    language: "中英对照译本",
    description: "第 1 章《深度学习革命》完整中英对照：原书页图、逐页译文、图注与公式均可对照阅读。",
    content: "books/bishop-deep-learning-2024/chapter-01.json",
    accent: "#3c6856",
    coverTitle: "DEEP\nLEARNING",
    coverSymbol: "∑",
    coverSeries: "FOUNDATIONS & CONCEPTS",
    status: "第 1 章",
    links: [{ label: "作者网站", url: "https://www.bishopbook.com/" }],
  },
];

const categories = [
  { value: "all", label: "全部学科" },
  { value: "Machine Learning", label: "机器学习" },
  { value: "Artificial Intelligence", label: "人工智能" },
  { value: "Mathematics", label: "数学" },
  { value: "Information Theory", label: "信息论" },
];
