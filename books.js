// The shelf is a manifest. Reading content lives in one JSON file per book.
const books = [
  {
    id: "bishop-deep-learning-2024",
    title: "深度学习：基础与概念",
    originalTitle: "Deep Learning: Foundations and Concepts",
    author: "Christopher M. Bishop · Hugh Bishop",
    category: "Machine Learning",
    year: "2024",
    language: "中英双语导读",
    description: "从第 1 章的曲线拟合例子开始，理解模型、误差与泛化。现已上架 1 篇双语样章。",
    content: "books/bishop-deep-learning-2024.json",
    accent: "#3c6856",
    coverTitle: "DEEP\nLEARNING",
    coverSymbol: "∑",
    coverSeries: "FOUNDATIONS & CONCEPTS",
    status: "样章",
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
