"""Assemble the original two PDF bitmaps with the intervening channel diagram.

The source bitmaps are copied without resampling.  The output is one SVG so the
reader can show the three components of Figure 1.5 as one numbered figure.
"""

from base64 import b64encode
from pathlib import Path


ASSETS = Path(__file__).resolve().parents[1] / "assets" / "chapter-01"
before = b64encode((ASSETS / "figure-1-5-source.png").read_bytes()).decode("ascii")
after = b64encode((ASSETS / "figure-1-5-received.png").read_bytes()).decode("ascii")

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="760" height="270" viewBox="0 0 760 270" role="img" aria-labelledby="title desc">
  <title id="title">图 1.5：二元对称信道中的图像传输</title>
  <desc id="desc">左边为原书中清晰的二值漫画，右边为通过噪声水平 f=0.1 的信道之后带噪声的同一漫画；中间是 0 和 1 经信道传送及以概率 f 翻转的示意。</desc>
  <rect width="760" height="270" fill="#ffffff"/>
  <image x="22" y="24" width="200" height="200" href="data:image/png;base64,{before}"/>
  <image x="538" y="24" width="200" height="200" href="data:image/png;base64,{after}"/>
  <g fill="#18261e" font-family="Georgia, serif" font-size="21" text-anchor="middle">
    <text x="315" y="78">0</text><text x="445" y="78">0</text>
    <text x="315" y="199">1</text><text x="445" y="199">1</text>
    <text x="380" y="55">1 − f</text><text x="380" y="240">1 − f</text>
    <text x="354" y="137">f</text><text x="406" y="137">f</text>
  </g>
  <g stroke="#18261e" stroke-width="2" fill="none">
    <path d="M330 72H430M330 193H430M330 79L430 185M330 186L430 80"/>
  </g>
  <g fill="#18261e">
    <path d="m430 72-10-5v10zm0 121-10-5v10zm0-8-12-2 7-8zm0-105-5 10-7-7z"/>
  </g>
  <g fill="#315d47" font-family="Noto Sans CJK SC, Microsoft YaHei, sans-serif" font-size="15" text-anchor="middle">
    <text x="122" y="252">发送前</text><text x="638" y="252">接收后</text>
  </g>
</svg>
"""
(ASSETS / "figure-1-5.svg").write_text(svg, encoding="utf-8")
