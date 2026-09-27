// Convert source TeX to browser-native MathML using the pinned KaTeX runtime.
const fs = require("node:fs");
const katex = require("../vendor/katex/katex.min.js");

const expressions = JSON.parse(fs.readFileSync(0, "utf8"));
const result = expressions.map(({ tex, display }) => {
  const rendered = katex.renderToString(tex, {
    output: "mathml",
    displayMode: Boolean(display),
    throwOnError: true,
    trust: false,
  });
  const match = rendered.match(/<math\b([^>]*)><semantics>([\s\S]*?)<annotation\b/);
  if (!match) throw new Error(`KaTeX returned no MathML for ${tex}`);
  return `<math${match[1]}>${match[2]}</math>`;
});
process.stdout.write(JSON.stringify(result));
