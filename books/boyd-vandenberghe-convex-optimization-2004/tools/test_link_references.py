"""Regression checks for book references versus details of a cited work."""
from copy import deepcopy
import unittest
from bs4 import BeautifulSoup
from link_references import linked_documents, strip_generated


def document(chapter, heading, body=""):
    blocks = [{"id":"p001-b001","kind":"heading","level":1,"text":heading,"html":f"<h1>{heading}</h1>"}]
    if body:
        blocks.append({"id":"p001-b002","kind":"rich","text":BeautifulSoup(body,"html.parser").get_text(),"html":body})
    return {"chapterId":chapter,"blocks":blocks}


def section(chapter, number):
    doc = document(chapter,f"第 {int(chapter)} 章")
    doc["blocks"].append({"id":"p001-b002","kind":"heading","level":2,
        "text":f"{number} 标题","html":f"<h2>{number} 标题</h2>"})
    return doc


class ReferenceTests(unittest.TestCase):
    def test_bibliography_title_parts_are_not_this_books_parts(self):
        body = '<p><strong>[Gup00]</strong> WSMP：Watson 稀疏矩阵软件包。第一部分：对称稀疏方程组的直接求解。第二部分：一般稀疏方程组的直接求解（<em>WSMP: Watson Sparse Matrix Package. Part I — Direct Solution of Symmetric Sparse Systems. Part II — Direct Solution of General Sparse Systems</em>）。</p>'
        docs = [document("references", "参考文献", body),
                document("part-I", "第一部分 理论"), document("part-II", "第二部分 应用")]
        linked, _ = linked_documents(docs)
        self.assertFalse(BeautifulSoup(linked[0]['blocks'][1]['html'],'html.parser').select('a'))
        self.assertEqual(strip_generated(linked[0]), docs[0])
        self.assertEqual(linked_documents(linked)[0], linked)

    def test_superscript_bibliography_keys_preserve_typography_and_targets(self):
        keys = ["ABB+99", "GMS+86", "MDW+02", "Bjö96", "Löf04", "Löw34", "Pré71", "Pré73", "Pré80"]
        bibliography = document("references", "参考文献")
        for index, key in enumerate(keys, 2):
            html = '<p class="reference-entry"><strong>[' + key.replace('+', '<sup>+</sup>') + ']</strong> 原条目。</p>'
            bibliography["blocks"].append({"id": f"p699-b{index:03}", "kind": "rich",
                "text": BeautifulSoup(html,"html.parser").get_text(), "html": html})
        body = '<p>[' + ', '.join(keys) + ', §4.3]；<math data-tex="x"><mi>x</mi></math>。</p>'
        docs = [document("01", "第 1 章", body), section("04", "4.3"), bibliography]
        original = deepcopy(docs)
        linked, _ = linked_documents(docs)
        soup = BeautifulSoup(linked[0]["blocks"][1]["html"], "html.parser")
        self.assertEqual([a.get_text() for a in soup.find_all("a")], keys)
        self.assertEqual([a["href"].split('#')[-1] for a in soup.find_all("a")],
                         [f"read-p699-b{index:03}" for index in range(2,11)])
        self.assertTrue(all('chapter=references' in a['href'] for a in soup.find_all('a')))
        self.assertEqual(linked[2], bibliography)
        self.assertEqual(strip_generated(linked[0]), docs[0])
        self.assertEqual(docs, original)
        self.assertEqual(linked_documents(linked)[0], linked)

    def test_leading_exercise_reference_does_not_define_a_target(self):
        doc = document("04", "第 4 章", "<p>习题 4.31 和 4.58 将给出具体例子。</p>")
        doc["blocks"].extend([
            {"id":"p002-b001","kind":"heading","level":2,"text":"习题","html":"<h2>习题</h2>"},
            {"id":"p002-b002","kind":"rich","text":"4.31 最优梁设计问题的递推形式。",
             "html":"<p><strong>4.31 最优梁设计问题的递推形式。</strong> 证明。</p>"},
        ])
        linked,_ = linked_documents([doc])
        soup = BeautifulSoup(linked[0]["blocks"][1]["html"], "html.parser")
        self.assertEqual(soup.a.get_text(), "习题 4.31")
        self.assertEqual(soup.a["href"], "#read-p002-b002")
        self.assertEqual(strip_generated(linked[0]), doc)

    def test_leading_algorithm_reference_uses_the_styled_title(self):
        doc = document("04", "第 4 章", "<p>算法 4.1 给出求解方法。</p>")
        doc["blocks"].append({"id":"p002-b001","kind":"rich","text":"算法 4.1 二分法。",
            "html":'<div class="algorithm"><p><strong>算法 4.1 二分法。</strong></p><p>步骤。</p></div>'})
        linked,_ = linked_documents([doc])
        soup = BeautifulSoup(linked[0]["blocks"][1]["html"], "html.parser")
        self.assertEqual(soup.a["href"], "#read-p002-b001")
        self.assertEqual(linked_documents(linked)[0], linked)

    def test_chapter_of_dantzig_book_is_not_this_books_chapter(self):
        text = "Dantzig [Dan63, 第 2 章] 包含一篇线性不等式的历史综述。"
        docs = [document("02","第 2 章",f"<p>{text}</p>")]
        linked,_ = linked_documents(docs)
        soup = BeautifulSoup(linked[0]["blocks"][1]["html"],"html.parser")
        self.assertEqual(soup.get_text(),text)
        self.assertFalse(soup.find_all("a"))

    def test_source_citation_detail_does_not_link_to_this_book(self):
        # The citation with §4.3 occurs in this book's chapter 1 bibliography.
        text = "见第 4 章以及 §4.3。Ben-Tal 与 Nemirovski 的书 [BTN01, §4.3]。"
        docs = [document("01","第 1 章",f"<p>{text}</p>"),section("04","4.3")]
        linked,_ = linked_documents(docs)
        soup = BeautifulSoup(linked[0]["blocks"][1]["html"],"html.parser")
        self.assertEqual(soup.get_text(),text)
        self.assertEqual([a.get_text() for a in soup.find_all("a")],["第 4 章","§4.3"])
        self.assertEqual(strip_generated(linked[0]),docs[0])

    def test_book_key_links_but_its_section_detail_does_not(self):
        text = "Luenberger [Lue69, 第 8.2 节]；本书第 8.2 节。"
        docs = [document("03","第 3 章",f"<p>{text}</p>"),section("08","8.2"),
            document("references","参考文献","<p>[Lue69] 原书完整书目条目。</p>")]
        linked,_ = linked_documents(docs)
        soup = BeautifulSoup(linked[0]["blocks"][1]["html"],"html.parser")
        anchors = soup.find_all("a")
        self.assertEqual([(a.get_text(),a["data-convex-reference"]) for a in anchors],
            [("Lue69","reference"),("第 8.2 节","section")])
        self.assertIn("chapter=references",anchors[0]["href"])
        self.assertIn("chapter=08",anchors[1]["href"])
        self.assertEqual(soup.get_text(),text)

    def test_grouped_unicode_citations_and_math_are_preserved(self):
        body = '<p>[Löw34, BTN01, §4.3] 与 <math><mi>x</mi></math>；式 (4.3)。</p>'
        docs = [document("03","第 3 章",body),section("04","4.3"),
            document("references","参考文献","<p>[Löw34] 条目一。</p><p>[BTN01] 条目二。</p>")]
        original = deepcopy(docs)
        linked,_ = linked_documents(docs)
        soup = BeautifulSoup(linked[0]["blocks"][1]["html"],"html.parser")
        self.assertEqual([a.get_text() for a in soup.find_all("a")],["Löw34","BTN01"])
        self.assertEqual(str(soup.math),"<math><mi>x</mi></math>")
        self.assertEqual(docs,original)
        self.assertEqual(linked_documents(linked)[0],linked)

    def test_chinese_citation_punctuation_keeps_external_details_external(self):
        for punctuation in ["，", "；"]:
            with self.subTest(punctuation=punctuation):
                text = f"Luenberger [Lue69{punctuation}第 8 章]；本书第 8 章和 §8.2；[BTN01{punctuation}§8.2]。"
                docs = [document("05", "第 5 章", f"<p>{text}</p>"), section("08", "8.2"),
                    document("references", "参考文献", "<p>[Lue69] 条目一。</p><p>[BTN01] 条目二。</p>")]
                linked, _ = linked_documents(docs)
                soup = BeautifulSoup(linked[0]["blocks"][1]["html"], "html.parser")
                self.assertEqual([(a.get_text(), a["data-convex-reference"]) for a in soup.find_all("a")],
                    [("Lue69", "reference"), ("第 8 章", "chapter"), ("§8.2", "section"), ("BTN01", "reference")])
                self.assertEqual(soup.get_text(), text)
                self.assertEqual(strip_generated(linked[0]), docs[0])
                self.assertEqual(linked_documents(linked)[0], linked)


if __name__ == "__main__":
    unittest.main()
