# Intelligence Library · 算经阁

收录机器学习、人工智能、数学与信息论书籍的小型书库，支持原著和译本并列展示。

直接在浏览器中打开 `index.html` 即可查看，无需安装依赖或构建。

## 添加书籍

编辑 `books.js`，在 `books` 数组中添加一项，例如：

```js
{
  title: "Book title",
  originalTitle: "Original title, if different",
  author: "Author name",
  category: "Machine Learning",
  edition: "translation",
  language: "简体中文",
  description: "A short note about this edition.",
  links: [{ label: "Publisher", url: "https://example.com/book" }]
}
```

`category` 可选 `Machine Learning`、`Artificial Intelligence`、`Mathematics`、`Information Theory`。`edition` 使用 `original` 或 `translation`。`links` 可填写出版社或阅读页面链接。

书架初始为空，待逐本核实书籍及译本信息后上架。
