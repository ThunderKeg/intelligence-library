"""Focused regressions for reader math, source page provenance, and figure guards."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from bs4 import BeautifulSoup

import build
from common import CHAPTER_BY_ID


class CompilerTests(unittest.TestCase):
    def compile_source(self, text: str) -> tuple[dict, dict]:
        with tempfile.TemporaryDirectory(prefix="convex-compiler-") as temporary:
            source_dir = Path(temporary)
            (source_dir / "chapter-01.md").write_text(text, encoding="utf-8")
            return build.compile_chapter(CHAPTER_BY_ID["01"], source_dir=source_dir, partial=True)

    def test_native_math_keeps_script_bold_and_plain_symbols_distinct(self) -> None:
        tex = r"R+\mathcal{R}+\mathbf{R}+\mathbf{dom}+\mathbf{1}+\mathbf{21}"
        markup = build.compile_math({"x": {"tex": tex, "display": False}})["x"]
        soup = BeautifulSoup("", "html.parser")
        math = build.math_node(soup, {"sourceTex": tex, "display": False}, markup)
        self.assertEqual(math["data-tex"], tex)
        self.assertEqual(math.annotation.get_text(), tex)
        self.assertIn("ℛ", math.get_text())
        self.assertIn("𝐑", math.get_text())
        self.assertIn("𝐝𝐨𝐦", math.get_text())
        self.assertIn("𝟏", math.get_text())
        self.assertIn("𝟐𝟏", math.get_text())
        for token in math.select("[data-source-glyph]"):
            self.assertEqual(token["mathvariant"], "normal")
            token.string = token["data-source-glyph"]
            token["mathvariant"] = token["data-source-mathvariant"]
            del token["data-source-glyph"]
            del token["data-source-mathvariant"]
        original = BeautifulSoup(markup, "html.parser").math
        self.assertEqual(math.semantics.mrow.decode_contents(), original.decode_contents())

    def test_bold_named_operators_are_single_tokens_with_function_spacing(self) -> None:
        tex = r"\operatorname{\mathbf{dom}} f+\operatorname{\mathbf{tr}}(X)+\operatorname{PV}(x)"
        for display in [False, True]:
            markup = build.compile_math({"x": {"tex": tex, "display": display}})["x"]
            math = build.math_node(BeautifulSoup("", "html.parser"),
                                   {"sourceTex": tex, "display": display}, markup)
            operators = math.select("[data-source-operator-mathml]")
            self.assertEqual([token.get_text() for token in operators], ["𝐝𝐨𝐦", "𝐭𝐫"])
            self.assertFalse(math.select("mi mrow, mi mi"))
            self.assertEqual(math["data-tex"], tex)
            self.assertEqual(math.annotation.get_text(), tex)
            self.assertEqual(math.find("mi", string="PV")["mathvariant"], "normal")
            for token in operators:
                self.assertEqual(token.find_next_sibling().get_text(), "\u2061")
                application = token.find_next_sibling()
                if token["data-source-glyph"] == "dom":
                    self.assertEqual(application["rspace"], "0.1667em")
                    original_application = BeautifulSoup(application["data-source-operator-spacing"], "html.parser").mo
                    application.replace_with(original_application)
                else:
                    self.assertFalse(application.has_attr("rspace"))
                original = BeautifulSoup(token["data-source-operator-mathml"], "html.parser").mi
                token.replace_with(original)
            self.assertEqual(math.semantics.mrow.decode_contents(),
                             BeautifulSoup(markup, "html.parser").math.decode_contents())

    def test_scripted_operator_spacing_follows_the_entire_name(self) -> None:
        tex = r"\operatorname{\mathbf{epi}}_K f"
        markup = build.compile_math({"x": {"tex": tex, "display": False}})["x"]
        math = build.math_node(BeautifulSoup("", "html.parser"),
                               {"sourceTex": tex, "display": False}, markup)
        spacer = math.select_one('[data-source-operator-script-spacing]')
        self.assertEqual(spacer.get('width'), '0.1667em')
        self.assertIs(spacer.find_previous_sibling(), math.msub)
        self.assertEqual(spacer.find_next_sibling().get_text(), 'f')
        self.assertFalse(math.msub.select('[rspace], mspace'))
        self.assertEqual(math.annotation.get_text(), tex)
        spacer.decompose()
        token = math.select_one('[data-source-operator-mathml]')
        token.replace_with(BeautifulSoup(token['data-source-operator-mathml'], 'html.parser').mi)
        self.assertEqual(math.semantics.mrow.decode_contents(),
                         BeautifulSoup(markup, 'html.parser').math.decode_contents())

    def test_variable_A_in_a_heading_is_not_an_appendix_number(self) -> None:
        source = '''# 第 1 章 测试

<aside class="chapter-guide">本章导读：标题编号检查。</aside>

<!-- pdf-page: 15 -->

## A.1 范数

### C.3.1 矩阵分解

#### $A$ 最优设计

#### $A$ 奇异时的 Schur 补
'''
        document, _ = self.compile_source(source)
        self.assertEqual([(h['number'], h['title']) for h in document['toc'][1:]],
                         [('A.1', '范数'), ('C.3.1', '矩阵分解'),
                          ('', 'A 最优设计'), ('', 'A 奇异时的 Schur 补')])
        self.assertEqual(document['toc'][0]['number'], '1')

    def test_orthogonal_direct_sum_has_a_real_stacked_operator(self) -> None:
        tex = r"\mathbin{\overset{\perp}{\oplus}}"
        for display in [False, True]:
            markup = build.compile_math({"x": {"tex": tex, "display": display}})["x"]
            soup = BeautifulSoup("", "html.parser")
            math = build.math_node(soup, {"sourceTex": tex, "display": display}, markup)
            self.assertFalse(math.select("mo mover"))
            self.assertEqual([child.get_text() for child in math.mover.find_all(True, recursive=False)], ["⊕", "⊥"])
            self.assertEqual(math.mover.mo["lspace"], "0.22em")
            self.assertEqual(math.annotation.get_text(), tex)
            original = BeautifulSoup(markup, "html.parser").math
            stored = BeautifulSoup(math.mover["data-source-mathml"], "html.parser").find(True)
            math.mover.replace_with(stored)
            self.assertEqual(math.semantics.mrow.decode_contents(), original.decode_contents())

    def test_math_scroller_tags_copy_source_and_literal_code(self) -> None:
        document, report = self.compile_source(r"""<!-- pdf-page: 15 -->

# 第 1 章 测试

<aside class="chapter-guide">本章导读：测试编译器结构。</aside>

内联 $x_1^2$ 与 `price=$5`。

$$
\begin{aligned} f(x)&=x^2 \\ g(x)&=x+1 \end{aligned}\tag{1.1}
$$

```python
literal = "$not_math$"
```

#### 四级标题
""")
        markup = "".join(block.get("html", "") for block in document["blocks"])
        soup = BeautifulSoup(markup, "html.parser")
        self.assertEqual(report["displayMath"], 1)
        self.assertEqual(report["inlineMath"], 1)
        self.assertEqual(soup.select_one(".formula-number").get_text(), "(1.1)")
        self.assertIsNotNone(soup.select_one(".book-formula > .formula-scroll > math"))
        self.assertIn(r"\tag{1.1}", soup.select_one("math[display=block]")["data-tex"])
        self.assertIn(r"\begin{aligned}", soup.select_one("math[display=block] annotation").get_text())
        for row in soup.select("math[display=block] mtable > mtr"):
            self.assertEqual([cell.get("style") for cell in row.find_all("mtd", recursive=False)],
                             ["text-align:right;text-align:-webkit-right", "text-align:left;text-align:-webkit-left"])
        self.assertIn("$not_math$", soup.find("pre").get_text())
        self.assertIsNotNone(soup.find("h4"))

    def test_inline_page_boundary_does_not_split_paragraph(self) -> None:
        document, _ = self.compile_source("""<!-- pdf-page: 15 -->

# 第一章

<aside class="chapter-guide">本章导读：结构测试。</aside>

同一段的前半句 <!-- pdf-page: 16 --> 同一段的后半句。

下一段。
""")
        paragraph = next(block for block in document["blocks"] if "前半句" in block["text"])
        following = next(block for block in document["blocks"] if block["text"] == "下一段。")
        self.assertIn("后半句", paragraph["text"])
        self.assertEqual(paragraph["pdfPage"], 15)
        self.assertEqual(following["pdfPage"], 16)

    def test_missing_pages_are_not_accepted_as_complete(self) -> None:
        with self.assertRaisesRegex(ValueError, "Missing original PDF page markers"):
            build.source_coverage("<!-- pdf-page: 15 -->\n# 标题", CHAPTER_BY_ID["01"], build.inventory_pages(), False)

    def test_duplicate_page_markers_fail(self) -> None:
        with self.assertRaisesRegex(ValueError, "increasing and unique"):
            build.source_coverage("<!-- pdf-page: 15 --><!-- pdf-page: 15 -->", CHAPTER_BY_ID["01"], build.inventory_pages(), True)

    def test_nearly_whole_page_image_rejected(self) -> None:
        tag = BeautifulSoup('<img data-source-page="15" data-source-rect="0,0,560,690">', "html.parser").img
        with self.assertRaisesRegex(ValueError, "Whole-page or nearly whole-page"):
            build.validate_crop(tag, Path("no-such-image.png"), {15: {"sizePoints": [600, 720]}})

    def test_duplicate_equation_labels_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Duplicate displayed equation numbers"):
            self.compile_source(r"""<!-- pdf-page: 15 -->

# 第一章

<aside class="chapter-guide">本章导读：结构测试。</aside>

$$x=1\tag{1.1}$$

$$x=2\tag{1.1}$$
""")

    def test_contents_table_is_local_and_narrow_screen_ready(self) -> None:
        soup = BeautifulSoup("<table><tr><th>标题</th><th>页码</th></tr><tr><td>长标题</td><td>123</td></tr></table>", "html.parser")
        build.validate_and_style(soup, {}, "contents")
        self.assertIn("min-width:0", soup.table["style"])
        self.assertIn("width:6em", soup.find_all("td")[-1]["style"])
        other = BeautifulSoup("<table><tr><td>普通表格</td></tr></table>", "html.parser")
        build.validate_and_style(other, {}, "02")
        self.assertNotIn("style", other.table.attrs)

    def test_floating_figures_preserve_provenance_and_relative_order(self) -> None:
        soup = BeautifulSoup('''<!-- pdf-page: 50 -->
<p id="start">跨页句子的前半段</p>
<!-- pdf-page: 51 -->
<figure id="first" data-reader-after="end">图一</figure>
<figure id="second" data-reader-after="end">图二</figure>
<!-- pdf-page: 52 -->
<p id="end">跨页句子的后半段</p>
<p id="next">下一段</p>''', "html.parser")
        pages = build.arrange_floating_figures(soup, 50)
        nodes = soup.find_all(recursive=False)
        self.assertEqual([node["id"] for node in nodes], ["start", "end", "first", "second", "next"])
        self.assertEqual([pages[id(node)] for node in nodes], [50, 52, 51, 51, 52])
        self.assertFalse(soup.select("[data-reader-after]"))

    def test_nested_figure_stays_within_its_example(self) -> None:
        soup = BeautifulSoup('''<!-- pdf-page: 313 -->
<div class="example" id="example"><p>例子的公式。</p><!-- pdf-page: 314 -->
<figure id="fig" data-reader-after="example-end">图</figure>
<p id="example-end">公式的说明。</p></div><p id="next">下一段。</p>''', "html.parser")
        pages = build.arrange_floating_figures(soup, 313)
        self.assertEqual([node.get("id") for node in soup.div.find_all(recursive=False)], [None, "example-end", "fig"])
        self.assertEqual(pages[id(soup.div)], 313)
        self.assertEqual(pages[id(soup.find(id="next"))], 314)
        self.assertIs(soup.figure.parent, soup.div)

    def test_paragraph_continuation_preserves_math_and_source_pages(self) -> None:
        soup = BeautifulSoup('''<!-- pdf-page: 312 -->
<p id="start">遗憾的是，罚函数</p><!-- pdf-page: 313 -->
<figure id="fig" data-reader-after="end">图</figure>
<p id="end" data-reader-continue="start"><math><mi>f</mi></math>不是凸函数。</p>
<p id="next">下一段。</p>''', "html.parser")
        math_before = str(soup.math)
        pages = build.arrange_floating_figures(soup, 312)
        self.assertEqual([node.get("id") for node in soup.find_all(recursive=False)], ["start", "fig", "next"])
        self.assertEqual(soup.find(id="start").get_text(), "遗憾的是，罚函数f不是凸函数。")
        self.assertEqual(str(soup.math), math_before)
        self.assertIs(soup.find(id="end").parent, soup.find(id="start"))
        self.assertEqual(pages[id(soup.find(id="start"))], 312)
        self.assertEqual(pages[id(soup.figure)], 313)
        self.assertFalse(soup.select("[data-reader-continue], [data-reader-after]"))

    def test_list_continuation_keeps_all_items_and_figure_order(self) -> None:
        soup = BeautifulSoup('''<!-- pdf-page: 310 -->
<ul id="start"><li>一</li></ul><!-- pdf-page: 311 -->
<figure id="first" data-reader-after="end">图一</figure><!-- pdf-page: 312 -->
<figure id="second" data-reader-after="end">图二</figure>
<ul id="end" data-reader-continue="start"><li>二</li><li>三</li><li>四</li></ul>
<h4 id="next">下一节</h4>''', "html.parser")
        pages = build.arrange_floating_figures(soup, 310)
        self.assertEqual([li.get_text() for li in soup.select("ul > li")], ["一", "二", "三", "四"])
        self.assertEqual(len(soup.find_all("ul")), 1)
        self.assertEqual([node.get("id") for node in soup.find_all(recursive=False)], ["start", "first", "second", "next"])
        self.assertEqual([pages[id(node)] for node in soup.find_all(recursive=False)], [310, 311, 312, 312])
        self.assertEqual(soup.find(id="end").parent.name, "li")

    def test_float_and_continuation_cannot_skip_or_cross_containers(self) -> None:
        cases = [
            '<div class="example"><figure data-reader-after="outside">图</figure></div><p id="outside">正文</p>',
            '<p id="old">在前面</p><figure data-reader-after="old">图</figure>',
            '<p id="first">前段</p><h4>不可跳过的标题</h4><p data-reader-continue="first">后段</p>',
            '<p id="first">前段</p><ul data-reader-continue="first"><li>不是同类元素</li></ul>',
        ]
        for source in cases:
            with self.subTest(source=source), self.assertRaises(ValueError):
                build.arrange_floating_figures(BeautifulSoup(source, "html.parser"), 312)

    def test_moved_floats_and_joined_lists_survive_linker_html_round_trip(self) -> None:
        soup = BeautifulSoup('''<div class="example">
<p>说明 <math><mi>x</mi></math> 的正文。</p>
<figure data-reader-after="end">图</figure>
<p id="end">完整说明。</p>
</div>
<ul id="first">
<li>一</li>
</ul>
<figure data-reader-after="last">图二</figure>
<ul id="last" data-reader-continue="first">
<li>二</li>
</ul>''', "html.parser")
        original_math = str(soup.math)
        build.arrange_floating_figures(soup, 312)
        for node in soup.find_all(recursive=False):
            markup = str(node)
            self.assertEqual(str(BeautifulSoup(markup, "html.parser")), markup)
        self.assertEqual(str(soup.math), original_math)
        self.assertEqual(soup.p.get_text(), "说明 x 的正文。")
        self.assertEqual([li.get_text() for li in soup.select("ul > li")], ["一", "二"])

    def test_delayed_float_returns_to_its_explicit_preceding_example(self) -> None:
        soup = BeautifulSoup('''<!-- pdf-page: 376 -->
<div class="example" id="owner"><p>例 7.2，结果见图 7.3。</p></div>
<!-- pdf-page: 377 -->
<div class="example" id="following"><p id="start">例 7.3 的前半句，</p>
<!-- pdf-page: 378 -->
<figure id="figure" data-figure="7.3" data-reader-owner="owner"><img data-source-page="378"/></figure>
<p data-reader-continue="start">后半句。</p></div>
<h2 id="next">下一节</h2>''', "html.parser")
        pages = build.arrange_floating_figures(soup, 376)
        self.assertIs(soup.figure.parent, soup.find(id="owner"))
        self.assertEqual(soup.img["data-source-page"], "378")
        self.assertEqual(pages[id(soup.find(id="owner"))], 376)
        self.assertEqual(pages[id(soup.find(id="following"))], 377)
        self.assertEqual(pages[id(soup.find(id="next"))], 378)
        self.assertEqual(soup.find(id="start").get_text(), "例 7.3 的前半句，后半句。")
        self.assertFalse(soup.select("[data-reader-owner]"))
        for node in soup.find_all(recursive=False):
            self.assertEqual(str(BeautifulSoup(str(node), "html.parser")), str(node))

    def test_chapter_illustration_can_leave_its_printed_remark_float(self) -> None:
        soup = BeautifulSoup('''<!-- pdf-page: 442 -->
<p>分类结果见图 8.12。</p>
<div class="remark" id="remark-8-1"><p>独立的贝叶斯解释。</p>
<math><mi>x</mi></math><!-- pdf-page: 443 -->
<figure id="figure" data-figure="8.12" data-reader-after-container="remark-8-1"><img data-source-page="443"/></figure>
<p>解释的最后一句。</p></div><h3 id="next">下一节</h3>''', "html.parser")
        math_before = str(soup.math)
        pages = build.arrange_floating_figures(soup, 442)
        container = soup.find(id="remark-8-1")
        self.assertIs(soup.figure.find_previous_sibling(True), container)
        self.assertIs(soup.figure.parent, soup)
        self.assertEqual(container.find_all("p")[-1].get_text(), "解释的最后一句。")
        self.assertEqual(str(soup.math), math_before)
        self.assertEqual(pages[id(container)], 442)
        self.assertEqual(pages[id(soup.figure)], 443)
        self.assertEqual(pages[id(soup.find(id="next"))], 443)
        self.assertEqual(soup.img["data-source-page"], "443")
        self.assertFalse(soup.select("[data-reader-after-container]"))
        for node in soup.find_all(recursive=False):
            self.assertEqual(str(BeautifulSoup(str(node), "html.parser")), str(node))

    def test_outside_float_cannot_leave_an_unrelated_or_uncited_container(self) -> None:
        cases = [
            '<p>图 8.12</p><div class="remark" id="first"></div><div class="remark" id="second">'
            '<figure data-figure="8.12" data-reader-after-container="first">图</figure></div>',
            '<p>未引用此图</p><div class="remark" id="remark">'
            '<figure data-figure="8.12" data-reader-after-container="remark">图</figure></div>',
            '<p>图 8.12</p><div id="arbitrary">'
            '<figure data-figure="8.12" data-reader-after-container="arbitrary">图</figure></div>',
            '<p>图 8.12</p><div class="remark" id="remark">'
            '<figure data-figure="8.12" data-reader-after="end" data-reader-after-container="remark">图</figure>'
            '<p id="end">正文</p></div>',
        ]
        for source in cases:
            with self.subTest(source=source), self.assertRaises(ValueError):
                build.arrange_floating_figures(BeautifulSoup(source, "html.parser"), 442)

    def test_late_chapter_figures_return_to_cited_examples_with_original_pages(self) -> None:
        soup = BeautifulSoup('''<!-- pdf-page: 555 -->
<p id="first">简单算例<!-- pdf-page: 556 -->，见图 10.1 和图 10.2。</p>
<h4 id="infeasible">不可行算例</h4><p id="second">结果见图 10.3 和图 10.4。</p>
<h4 id="game">博弈</h4><p id="third">结果见图 10.5。</p>
<h2 id="implementation">10.4 实现</h2><h3 id="kkt">10.4.2 求解方程组</h3>
<p id="start">线性方程组</p><!-- pdf-page: 557 -->
<figure id="one" data-figure="10.1" data-reader-after-previous="first"><img data-source-page="557" alt="第一幅"/></figure>
<figure id="two" data-figure="10.2" data-reader-after-previous="first"><img data-source-page="557" alt="第二幅"/></figure>
<!-- pdf-page: 558 -->
<figure id="three" data-figure="10.3" data-reader-after-previous="second"><img data-source-page="558"/></figure>
<figure id="four" data-figure="10.4" data-reader-after-previous="second"><img data-source-page="558"/></figure>
<!-- pdf-page: 559 -->
<figure id="five" data-figure="10.5" data-reader-after-previous="third"><img data-source-page="559"/></figure>
<p data-reader-continue="start">具有 KKT 形式。</p><p id="equation"><math><mi>H</mi><mi>v</mi></math></p>''', "html.parser")
        images_before = [str(image) for image in soup.find_all("img")]
        math_before = str(soup.math)
        pages = build.arrange_floating_figures(soup, 555)
        self.assertEqual([node.get("id") for node in soup.find_all(recursive=False)],
                         ["first", "one", "two", "infeasible", "second", "three", "four", "game", "third", "five", "implementation", "kkt", "start", "equation"])
        self.assertEqual([pages[id(figure)] for figure in soup.find_all("figure")], [557, 557, 558, 558, 559])
        self.assertEqual(pages[id(soup.find(id="first"))], 555)
        self.assertEqual(pages[id(soup.find(id="start"))], 556)
        self.assertEqual(pages[id(soup.find(id="equation"))], 559)
        self.assertEqual(soup.find(id="start").get_text(), "线性方程组具有 KKT 形式。")
        self.assertEqual([str(image) for image in soup.find_all("img")], images_before)
        self.assertEqual(str(soup.math), math_before)
        self.assertFalse(soup.select("[data-reader-after-previous], [data-reader-continue]"))
        for node in soup.find_all(recursive=False):
            self.assertEqual(str(BeautifulSoup(str(node), "html.parser")), str(node))

    def test_returning_and_forward_figures_keep_matrix_explanations_adjacent(self) -> None:
        soup = BeautifulSoup('''<!-- pdf-page: 562 -->
<p id="primal">第一种方法见图 10.6。</p><p id="dual">第二种方法见图 10.7。</p>
<p id="matrix"><math><mi>H</mi></math></p><!-- pdf-page: 563 -->
<figure id="six" data-figure="10.6" data-reader-after-previous="primal">图六</figure>
<figure id="seven" data-figure="10.7" data-reader-after-previous="dual">图七</figure>
<!-- pdf-page: 564 -->
<figure id="eight" data-figure="10.8" data-reader-after="residual-end">图八</figure>
<p id="where">其中 H 是 Hessian 矩阵。</p><p id="residual">残差定义</p>
<p id="residual-end">图 10.8 的完整说明。</p><p id="comparison">三种方法比较。</p>''', "html.parser")
        pages = build.arrange_floating_figures(soup, 562)
        self.assertEqual([node.get("id") for node in soup.find_all(recursive=False)],
                         ["primal", "six", "dual", "seven", "matrix", "where", "residual", "residual-end", "eight", "comparison"])
        self.assertEqual([pages[id(figure)] for figure in soup.find_all("figure")], [563, 563, 564])
        self.assertEqual(pages[id(soup.find(id="matrix"))], 562)
        self.assertEqual(pages[id(soup.find(id="where"))], 564)
        self.assertFalse(soup.select("[data-reader-after-previous], [data-reader-after]"))

    def test_returning_float_rejects_uncited_ambiguous_or_wrong_scope_targets(self) -> None:
        cases = [
            '<figure data-figure="10.1" data-reader-after-previous="p"></figure><p id="p">图 10.1</p>',
            '<p>图 10.1</p><figure data-figure="10.1" data-reader-after-previous="missing"></figure>',
            '<p id="p">图 10.1</p><p id="p">图 10.1</p><figure data-figure="10.1" data-reader-after-previous="p"></figure>',
            '<p id="p">图 10.10</p><figure data-figure="10.1" data-reader-after-previous="p"></figure>',
            '<h4 id="p">图 10.1</h4><figure data-figure="10.1" data-reader-after-previous="p"></figure>',
            '<div class="example"><p id="p">图 10.1</p><figure data-figure="10.1" data-reader-after-previous="p"></figure></div>',
            '<p id="p">图 10.1</p><div class="example"><figure data-figure="10.1" data-reader-after-previous="p"></figure></div>',
            '<p id="start">前段</p><p id="p" data-reader-continue="start">图 10.1</p><figure data-figure="10.1" data-reader-after-previous="p"></figure>',
            '<p id="p">图 10.1</p><figure data-figure="10.1" data-reader-after-previous="p"></figure><figure data-figure="10.1"></figure>',
            '<p id="p">图 10.1</p><figure data-reader-after-previous="p"></figure>',
        ]
        for other in ("data-reader-after", "data-reader-owner", "data-reader-after-container"):
            cases.append(f'<p id="p">图 10.1</p><figure data-figure="10.1" data-reader-after-previous="p" {other}="p"></figure>')
        for source in cases:
            with self.subTest(source=source), self.assertRaises(ValueError):
                build.arrange_floating_figures(BeautifulSoup(source, "html.parser"), 556)

    def test_returning_float_cannot_invert_moved_or_unmoved_figures(self) -> None:
        cases = [
            '<p id="p2">图 10.2</p><p id="p1">图 10.1</p>'
            '<figure data-figure="10.1" data-reader-after-previous="p1"></figure>'
            '<figure data-figure="10.2" data-reader-after-previous="p2"></figure>',
            '<p id="p">图 10.1 和图 10.3</p>'
            '<figure data-figure="10.1" data-reader-after-previous="p"></figure>'
            '<figure data-figure="10.2"></figure>'
            '<figure data-figure="10.3" data-reader-after-previous="p"></figure>',
        ]
        for source in cases:
            with self.subTest(source=source), self.assertRaises(ValueError):
                build.arrange_floating_figures(BeautifulSoup(source, "html.parser"), 556)

    def test_figure_owner_cannot_skip_examples_or_ignore_the_figure_reference(self) -> None:
        cases = [
            '<div class="example" id="owner"><p>图 7.3</p></div><h2>分隔标题</h2>'
            '<div class="example"><figure data-figure="7.3" data-reader-owner="owner">图</figure></div>',
            '<div class="example" id="owner"><p>未引用此图</p></div>'
            '<div class="example"><figure data-figure="7.3" data-reader-owner="owner">图</figure></div>',
            '<div class="example" id="owner"><p>图 7.3</p></div>'
            '<figure data-figure="7.3" data-reader-owner="owner">图</figure>',
        ]
        for source in cases:
            with self.subTest(source=source), self.assertRaises(ValueError):
                build.arrange_floating_figures(BeautifulSoup(source, "html.parser"), 376)

    def test_chapter_float_returns_to_its_citing_example_and_keeps_proof_continuous(self) -> None:
        soup = BeautifulSoup('''<!-- pdf-page: 577 -->
<figure id="one" data-figure="11.1" data-reader-after="barrier"><img data-source-page="577"/></figure>
<p id="barrier">完整定义与图 11.1 的说明。</p><!-- pdf-page: 579 -->
<div class="example" id="example"><p>例 11.1 的几何解释，见图 11.2。</p><math><mi>c</mi></math></div>
<h4 id="dual">由中心路径得到对偶点</h4><p id="proof-start">将最优性条件写成</p>
<div id="equation" class="book-formula"><math><mi>x</mi></math></div><!-- pdf-page: 580 -->
<figure id="two" data-figure="11.2" data-reader-return-to-example="example"><img data-source-page="580" alt="中心路径"/></figure>
<p id="proof-end">可见它最小化拉格朗日函数。</p>
<div class="example" id="force"><p>例 11.3 的力场。</p><!-- pdf-page: 582 -->
<figure id="three" data-figure="11.3" data-reader-after="force-end"><img data-source-page="582"/></figure>
<p id="force-end">完整解释图 11.3。</p></div>''', "html.parser")
        original_images = [str(node) for node in soup.find_all("img")]
        original_math = [str(node) for node in soup.find_all("math")]
        pages = build.arrange_floating_figures(soup, 577)
        self.assertEqual([node.get("id") for node in soup.find_all("figure")], ["one", "two", "three"])
        self.assertIs(soup.find(id="two").parent, soup.find(id="example"))
        self.assertIs(soup.find(id="equation").find_next_sibling(True), soup.find(id="proof-end"))
        self.assertIs(soup.find(id="one").find_previous_sibling(True), soup.find(id="barrier"))
        self.assertIs(soup.find(id="three").find_previous_sibling(True), soup.find(id="force-end"))
        self.assertEqual([pages[id(node)] for node in soup.find_all("figure")], [577, 580, 582])
        self.assertEqual(pages[id(soup.find(id="example"))], 579)
        self.assertEqual(pages[id(soup.find(id="proof-end"))], 580)
        self.assertEqual([str(node) for node in soup.find_all("img")], original_images)
        self.assertEqual([str(node) for node in soup.find_all("math")], original_math)
        self.assertFalse(soup.select("[data-reader-return-to-example], [data-reader-after]"))
        for node in soup.find_all(recursive=False):
            self.assertEqual(str(BeautifulSoup(str(node), "html.parser")), str(node))

    def test_example_return_rejects_wrong_scope_missing_citation_and_intervening_frames(self) -> None:
        figure = '<figure data-figure="11.2" data-reader-return-to-example="owner">图</figure>'
        owner = '<div class="example" id="owner"><p>例 11.1，见图 11.2。</p></div>'
        cases = [figure+owner, owner.replace('id="owner"','id="different"')+figure,
                 owner+owner+figure, owner.replace('图 11.2','图 11.20')+figure,
                 owner.replace('class="example"','class="remark"')+figure,
                 owner+'<div class="example">'+figure+'</div>',
                 '<div class="remark">'+owner+'</div>'+figure,
                 '<div class="example" id="owner"><figure><p>图 11.2</p></figure></div>'+figure,
                 owner+figure+'<figure data-figure="11.2">重号</figure>',
                 owner+figure.replace('data-figure="11.2"','')]
        for tag in ['h1','h2','h3']:
            cases.append(owner+f'<{tag}>后面的章节</{tag}>'+figure)
        for frame in ['example','remark','exercise','algorithm']:
            cases.append(owner+f'<div class="{frame}">另一个框</div>'+figure)
        for attribute in ['data-reader-after','data-reader-owner','data-reader-after-container','data-reader-after-previous']:
            cases.append(owner+figure.replace('>图',f' {attribute}="owner">图'))
        for source in cases:
            with self.subTest(source=source), self.assertRaises(ValueError):
                build.arrange_floating_figures(BeautifulSoup(source, "html.parser"), 579)

    def test_example_return_cannot_reverse_any_original_figures(self) -> None:
        soup = BeautifulSoup('''<div class="example" id="owner"><p>图 11.2</p></div>
<figure data-figure="11.1">前一幅</figure>
<figure data-figure="11.2" data-reader-return-to-example="owner">回移图</figure>''', "html.parser")
        with self.assertRaisesRegex(ValueError, "order of all figures"):
            build.arrange_floating_figures(soup, 579)

    def test_returning_figures_follow_complete_model_explanations_with_explicit_citations(self) -> None:
        soup = BeautifulSoup('''<!-- pdf-page: 597 -->
<p id="cite-ten">图 11.10 的实验构造以下 LP：</p>
<div class="book-formula" id="model"><math><mi>s</mi></math></div>
<p id="cite-eleven">图 11.11 说明接近边界时所需步数。</p>
<p id="complete">至此完整说明两种结果。</p>
<h4 id="new-method">另一种方法</h4><p id="new-prose">与前一方法不同。</p>
<!-- pdf-page: 598 -->
<figure id="ten" data-figure="11.10" data-reader-after-previous="complete" data-reader-citation="cite-ten"><img data-source-page="598"/></figure>
<figure id="eleven" data-figure="11.11" data-reader-after-previous="complete" data-reader-citation="cite-eleven"><img data-source-page="598"/></figure>
<!-- pdf-page: 599 --><figure id="twelve" data-figure="11.12"><img data-source-page="599"/></figure>''', "html.parser")
        images = [str(node) for node in soup.find_all("img")]
        math = str(soup.math)
        pages = build.arrange_floating_figures(soup, 597)
        self.assertEqual([node.get("id") for node in soup.find_all(recursive=False)],
                         ["cite-ten", "model", "cite-eleven", "complete", "ten", "eleven", "new-method", "new-prose", "twelve"])
        self.assertEqual([pages[id(node)] for node in soup.find_all("figure")], [598, 598, 599])
        self.assertEqual([str(node) for node in soup.find_all("img")], images)
        self.assertEqual(str(soup.math), math)
        self.assertFalse(soup.select("[data-reader-citation], [data-reader-after-previous]"))
        for node in soup.find_all(recursive=False):
            self.assertEqual(str(BeautifulSoup(str(node), "html.parser")), str(node))

    def test_separate_figure_citation_cannot_cross_sections_frames_or_other_content(self) -> None:
        citation = '<p id="cite">实验见图 11.10。</p>'
        target = '<p id="end">完整解释。</p>'
        figure = '<figure data-figure="11.10" data-reader-after-previous="end" data-reader-citation="cite"></figure>'
        cases = [target+figure, citation+citation+target+figure, target+citation+figure,
                 citation.replace('图 11.10','图 11.100')+target+figure,
                 '<div class="example">'+citation+'</div>'+target+figure,
                 citation.replace('p id','h4 id').replace('</p>','</h4>')+target+figure,
                 citation.replace('id="cite"','id="cite" data-reader-continue="earlier"')+target+figure,
                 citation+target+figure.replace('data-reader-after-previous="end"','data-reader-after="end"'),
                 citation+target+'<p data-reader-citation="cite">wrong node</p>',
                 citation+target+figure+'<figure data-figure="11.10"></figure>',
                 citation+target.replace('id="end"','id="end" data-reader-continue="cite"')+figure,
                 citation+target+figure.replace('data-reader-citation="cite"','')]
        for separator in ['<h1>标题</h1>','<h2>标题</h2>','<h3>标题</h3>','<h4>标题</h4>',
                          '<figure data-figure="11.9">另一幅</figure>', '<img src="other.png"/>',
                          '<ul><li>另一组</li></ul>', '<table><tr><td>表</td></tr></table>',
                          '<div class="book-formula"><figure>嵌套图</figure></div>']:
            cases.append(citation+separator+target+figure)
        for frame in ['example','remark','exercise','algorithm']:
            cases.append(citation+f'<div class="{frame}">框</div>'+target+figure)
        for source in cases:
            with self.subTest(source=source), self.assertRaises(ValueError):
                build.arrange_floating_figures(BeautifulSoup(source, "html.parser"), 597)


if __name__ == "__main__":
    unittest.main()
