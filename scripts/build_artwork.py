#!/usr/bin/env python3
"""Build the profile's small vector graphics. The raster cover is AI-generated."""

from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"
FONT = "'Trebuchet MS', 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, monospace"
THEMES = {
    "light": dict(bg="#fbf7ee", ink="#2f4339", muted="#6c786e", line="#cecdbd", accent="#b96d42", chip="#e8ecdf"),
    "dark": dict(bg="#192721", ink="#eee9dc", muted="#b1bbaa", line="#435647", accent="#eda775", chip="#2b3e31"),
}


def svg(width, height, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title, quote=True)}">
<title>{escape(title)}</title>
{body}
</svg>\n'''


def text(x, y, content, size=18, fill="#2f4339", family=FONT, extra=""):
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" fill="{fill}" {extra}>{escape(content)}</text>'


def icon(kind, t):
    ink, accent, chip = t["ink"], t["accent"], t["chip"]
    art = {
        "claim": f'''<path d="M5 8L43 5 48 56 10 60Z" fill="{chip}"/><path d="M13 18l22-2m-21 11 19-2m-18 11 13-2m-12 11 16-2"/><circle cx="47" cy="38" r="15" fill="{t['bg']}"/><path d="M57 50l13 16" stroke="{accent}" stroke-width="5"/><path d="m39 38 5 5 10-12" stroke="{accent}"/>''',
        "rl": f'''<rect x="2" y="8" width="60" height="56" rx="4" fill="{chip}"/><path d="M17 8v56M32 8v56M47 8v56M2 22h60M2 36h60M2 50h60" stroke="{t['line']}"/><path d="M9 57V29h31V15h15" stroke="{accent}" stroke-dasharray="3 5"/><path d="m53 9 3 5 6 1-4 4 1 6-6-3-5 3 1-6-4-4 6-1Z" fill="{accent}" stroke="{accent}"/><circle cx="9" cy="57" r="4" fill="{ink}"/>''',
        "notes": f'''<path d="M1 17Q18 11 32 19Q48 10 65 15L67 62Q47 57 33 65Q17 57 3 63Z" fill="{chip}"/><path d="M32 20l1 45M10 28l14-1m-13 10 13-1m-12 10 12-1m19-14 15-3m-15 13 16-2m-15 11 14-2"/><path d="M43 18Q36-2 51 2Q53 14 43 18ZM43 18Q61 9 66 0Q48-3 43 18Z" fill="{accent}" stroke="{accent}"/>''',
        "product": f'''<path d="m5 27 27-13 28 13-28 14Z" fill="{chip}"/><path d="M5 27v28l27 15 28-15V27M32 41v29M18 21l28 14v14l-8 4V39"/><path d="M55 4v13m-6-7h13M4 5v9m-4-4h8" stroke="{accent}"/><path d="m13 46 10 5" stroke="{accent}"/>''',
    }[kind]
    return f'<g transform="translate(370 26) rotate(3 35 35)" fill="none" stroke="{ink}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{art}</g>'


PROJECTS = [
    ("claim", "01 / EVIDENCE & CRAFT", "Claim Chart", ["让专利要素、技术证据", "与 Word 文档严丝合缝。"], "PYTHON · RESEARCH · DOCX"),
    ("rl", "02 / LEARNING BY DOING", "RL Playground", ["从 Q-learning 到 Actor-Critic，", "把强化学习算法亲手跑一遍。"], "PYTHON · DQN · POLICY GRADIENT"),
    ("notes", "03 / NOTES IN THE MARGINS", "Learning Notes", ["沿着公式、代码与 Tensor 图，", "留下一条可以重走的学习路径。"], "ASTRO · MDX · MODEL ARCHITECTURE"),
    ("product", "04 / LANGUAGE INTO TOOLS", "Product Release", ["把中文 NLP 与商品发布连接起来，", "让一个模型走进具体的使用场景。"], "PYTHON · BERT · FASTAPI"),
]


def build_cards():
    for theme, t in THEMES.items():
        for kind, label, title, description, tags in PROJECTS:
            body = f'''<rect x="7" y="10" width="466" height="211" rx="13" fill="{t['chip']}"/>
<path d="M20 5Q8 5 7 18L5 199Q5 212 20 213L458 215Q473 215 474 199L472 20Q472 6 458 7Z" fill="{t['bg']}" stroke="{t['line']}" stroke-width="1.3"/>
{text(28, 34, label, 11, t['muted'], MONO, 'letter-spacing="1.1"')}
{text(28, 76, title, 29, t['ink'], "Georgia, serif")}
<path d="M29 87q47-3 80 0" fill="none" stroke="{t['accent']}" stroke-width="2" stroke-linecap="round"/>
{text(28, 119, description[0], 17, t['ink'])}
{text(28, 146, description[1], 17, t['ink'])}
{icon(kind, t)}
<path d="M28 166q217 1 421-1" fill="none" stroke="{t['line']}" stroke-dasharray="2 4"/>
{text(28, 193, tags, 11, t['muted'], MONO, 'letter-spacing="0.3"')}
<g fill="none" stroke="{t['accent']}" stroke-width="1.8" stroke-linecap="round"><path d="m423 194 18-16m-16 0h16v15"/></g>'''
            (ASSETS / f"project-{kind}-{theme}.svg").write_text(svg(480, 224, f"{title} — {''.join(description)}", body), encoding="utf-8")


def build_accents():
    for theme, t in THEMES.items():
        greeting = "Learning by building. Sharing along the way."
        body = f'''<style>
@keyframes reveal {{0%,8% {{clip-path:inset(0 100% 0 0)}} 52%,94% {{clip-path:inset(0 0 0 0)}} 100% {{clip-path:inset(0 100% 0 0)}}}}
@keyframes blink {{0%,46% {{opacity:1}} 47%,100% {{opacity:.25}}}}
.line {{animation:reveal 12s steps(43,end) infinite}}
.dot {{animation:blink 2.4s ease-in-out infinite}}
@media (prefers-reduced-motion: reduce) {{.line,.dot {{animation:none}}}}
</style>
<circle class="dot" cx="30" cy="23" r="4" fill="{t['accent']}"/>
<g class="line">{text(48, 29, greeting, 18, t['ink'], MONO)}</g>'''
        (ASSETS / f"hello-{theme}.svg").write_text(svg(640, 46, greeting, body), encoding="utf-8")

        body = text(340, 22, "ON MY DESK", 10, t["muted"], MONO, 'letter-spacing="2.6" text-anchor="middle"')
        chips = [("Python", 90), ("PyTorch", 98), ("Transformers", 152), ("Astro", 82), ("Markdown", 122)]
        x = (680 - sum(width for _, width in chips) - 4 * 11) / 2
        for label, width in chips:
            body += f'<rect x="{x}" y="35" width="{width}" height="32" rx="16" fill="{t["chip"]}"/>'
            body += text(x + width / 2, 56, label, 13, t["ink"], FONT, 'text-anchor="middle"')
            x += width + 11
        (ASSETS / f"toolbox-{theme}.svg").write_text(svg(680, 83, "On my desk: Python, PyTorch, Transformers, Astro, Markdown", body), encoding="utf-8")

        body = f'''<path d="M28 36C94 8 119 73 175 38S244 16 277 41 353 57 380 29" fill="none" stroke="{t['line']}" stroke-width="1.3" stroke-dasharray="5 7"/>
<g transform="translate(372 16) rotate(-9)" stroke="{t['accent']}" stroke-width="1.2" stroke-linejoin="round"><path d="m0 10 38-9-16 29-5-13Z" fill="{t['chip']}"/><path d="M17 17 38 1" fill="none"/></g>
{text(448, 42, 'Stay curious. Keep making.', 21, t['ink'], 'Georgia, serif')}
<path d="M772 28v12m-6-6h12" stroke="{t['accent']}" stroke-width="1.3"/>'''
        (ASSETS / f"footer-{theme}.svg").write_text(svg(820, 79, "Stay curious. Keep making.", body), encoding="utf-8")


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    build_cards()
    build_accents()
    print("Built 14 theme-aware vector assets.")
