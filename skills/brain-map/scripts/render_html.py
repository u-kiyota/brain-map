#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""brain-map: カテゴリ別 md → スタイル付き単一 HTML 変換 + summary.html リンク補正。

使い方:
    python3 scripts/render_html.py [REPO_ROOT]

REPO_ROOT を省略するとカレントディレクトリをブレインマップのリポジトリ直下とみなす。

やること:
  1. `_` 始まり・README.md・index.md を除く全 *.md を <同名>.html へ変換する。
  2. 各ページは summary.html と統一した配色・カード調の共通 CSS でラップし、
     上部に「← サマリへ戻る」ナビと兄弟カテゴリへのピルリンク（現在ページを
     ハイライト）を付ける。サイトとして回遊できる。
  3. 仕上げに summary.html 内のカテゴリへの href="./xxx.md" / href="xxx.md" を
     href="./xxx.html" に書き換える（手書きで .md のまま残っていても自動補正）。
     index.md（AI 用）のリンクは触らない。

設計上の注意:
  - 入力 md は匿名化済みである前提。本スクリプトは変換するだけで匿名化はしない。
  - markdown パッケージが無い場合は pip で自動導入を試みる（--break-system-packages）。
    導入できない環境では簡易フォールバック変換に切り替える。
"""

import os
import re
import sys
import html as _html
import subprocess

# ---- カテゴリ判定 ---------------------------------------------------------

EXCLUDE_EXACT = {"index.md", "readme.md"}


def is_category_md(filename: str) -> bool:
    low = filename.lower()
    if not low.endswith(".md"):
        return False
    if filename.startswith("_"):
        return False
    if low in EXCLUDE_EXACT:
        return False
    return True


# ---- markdown 変換 --------------------------------------------------------

def _get_md_converter():
    """markdown ライブラリの convert 関数を返す。無ければ導入を試み、
    それも失敗したら簡易フォールバックを返す。"""
    try:
        import markdown  # type: ignore
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "markdown",
             "--quiet", "--break-system-packages"],
            check=False,
        )
        try:
            import markdown  # type: ignore
        except ImportError:
            markdown = None

    if markdown is not None:
        def convert(text: str) -> str:
            return markdown.markdown(
                text,
                extensions=["tables", "fenced_code", "sane_lists", "toc"],
            )
        return convert

    # --- 最小フォールバック（見出し・段落・箇条書き・コードのみ） ---
    def fallback(text: str) -> str:
        out = []
        in_code = False
        in_list = False
        for line in text.splitlines():
            if line.strip().startswith("```"):
                if not in_code:
                    out.append("<pre><code>")
                    in_code = True
                else:
                    out.append("</code></pre>")
                    in_code = False
                continue
            if in_code:
                out.append(_html.escape(line))
                continue
            m = re.match(r"^(#{1,6})\s+(.*)$", line)
            if m:
                if in_list:
                    out.append("</ul>")
                    in_list = False
                lvl = len(m.group(1))
                out.append(f"<h{lvl}>{_html.escape(m.group(2))}</h{lvl}>")
                continue
            m = re.match(r"^\s*[-*]\s+(.*)$", line)
            if m:
                if not in_list:
                    out.append("<ul>")
                    in_list = True
                out.append(f"<li>{_html.escape(m.group(1))}</li>")
                continue
            if in_list:
                out.append("</ul>")
                in_list = False
            if line.strip():
                out.append(f"<p>{_html.escape(line)}</p>")
        if in_list:
            out.append("</ul>")
        if in_code:
            out.append("</code></pre>")
        return "\n".join(out)

    return fallback


# ---- タイトル抽出 ---------------------------------------------------------

def first_heading(path: str, default: str) -> str:
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                m = re.match(r"^#\s+(.*)$", line.strip())
                if m:
                    return m.group(1).strip()
    except OSError:
        pass
    return default


def find_meta_line(path: str, key: str) -> str:
    """index.md 内の `> 最終更新: ...` のような行から値を拾う。"""
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                if key in line:
                    return line.split(key, 1)[1].lstrip(": ：").strip(" >")
    except OSError:
        pass
    return ""


# ---- カテゴリ順序（index.md の知識ベースリンク順を優先） -------------------

def ordered_categories(root: str):
    cats = [f for f in os.listdir(root) if is_category_md(f)]
    order = []
    index_path = os.path.join(root, "index.md")
    if os.path.exists(index_path):
        with open(index_path, encoding="utf-8") as f:
            text = f.read()
        for m in re.finditer(r"\]\(\.?/?([A-Za-z0-9._-]+\.md)\)", text):
            name = m.group(1)
            if name in cats and name not in order:
                order.append(name)
    for f in sorted(cats):
        if f not in order:
            order.append(f)
    return order


# ---- HTML テンプレート -----------------------------------------------------

PAGE_CSS = """
:root{
  --bg:#f6f7f9; --panel:#ffffff; --ink:#1c2430; --muted:#5f6b7a;
  --line:#e6e9ee; --accent:#2f6f6b; --accent-soft:#e7f1f0;
  --warn:#b4612a; --warn-soft:#fbeee2;
  --shadow:0 1px 2px rgba(20,30,45,.04),0 8px 24px rgba(20,30,45,.06);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);line-height:1.85;
  font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN","Yu Gothic",Meiryo,sans-serif;
  -webkit-font-smoothing:antialiased;}
.topbar{position:sticky;top:0;z-index:10;background:rgba(255,255,255,.92);
  backdrop-filter:saturate(180%) blur(8px);border-bottom:1px solid var(--line);}
.topbar .inner{max-width:880px;margin:0 auto;padding:12px 20px;display:flex;
  align-items:center;gap:14px;flex-wrap:wrap;}
.topbar .home{font-weight:700;color:var(--accent);text-decoration:none;font-size:14px;
  white-space:nowrap;padding:6px 12px;border:1px solid var(--accent-soft);border-radius:999px;background:var(--accent-soft);}
.topbar .home:hover{background:var(--accent);color:#fff}
.topbar .site{font-size:13px;color:var(--muted);white-space:nowrap}
.pills{max-width:880px;margin:0 auto;padding:10px 20px 0;display:flex;gap:8px;flex-wrap:wrap}
.pills a{font-size:12.5px;text-decoration:none;color:var(--muted);background:var(--panel);
  border:1px solid var(--line);border-radius:999px;padding:5px 12px;transition:.15s;}
.pills a:hover{border-color:var(--accent);color:var(--accent)}
.pills a.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.wrap{max-width:880px;margin:0 auto;padding:8px 20px 80px}
.article{background:var(--panel);border:1px solid var(--line);border-radius:16px;
  padding:30px 34px;margin-top:18px;box-shadow:var(--shadow);}
.article h1{font-size:27px;letter-spacing:.03em;margin:0 0 8px;border-bottom:2px solid var(--accent-soft);padding-bottom:12px}
.article h2{font-size:19px;margin:34px 0 12px;color:var(--accent);
  border-left:4px solid var(--accent);padding-left:12px}
.article h3{font-size:16px;margin:24px 0 8px}
.article h4{font-size:14.5px;margin:18px 0 6px;color:var(--muted)}
.article p{margin:10px 0}
.article ul,.article ol{margin:8px 0;padding-left:1.4em}
.article li{margin:4px 0}
.article a{color:var(--accent)}
.article blockquote{margin:14px 0;padding:10px 16px;background:var(--accent-soft);
  border-left:4px solid var(--accent);border-radius:0 8px 8px 0;color:#244f4c}
.article code{background:#eef1f5;padding:2px 6px;border-radius:5px;font-size:.9em;
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.article pre{background:#1c2430;color:#e6e9ee;padding:16px 18px;border-radius:10px;overflow:auto}
.article pre code{background:none;color:inherit;padding:0}
.article table{border-collapse:collapse;width:100%;margin:14px 0;font-size:14px}
.article th,.article td{border:1px solid var(--line);padding:8px 12px;text-align:left}
.article th{background:var(--accent-soft);color:#244f4c}
.article hr{border:none;border-top:1px solid var(--line);margin:26px 0}
footer{max-width:880px;margin:26px auto 0;padding:0 20px;text-align:center;
  font-size:12px;color:var(--muted)}
footer a{color:var(--accent)}
"""

PAGE_TMPL = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — {site}</title>
<style>{css}</style>
</head>
<body>
<div class="topbar"><div class="inner">
  <a class="home" href="./summary.html">← サマリへ戻る</a>
  <span class="site">{site}・ブレインマップ</span>
</div></div>
<nav class="pills">{pills}</nav>
<div class="wrap">
  <article class="article">{body}</article>
</div>
<footer>このページは <code>{md_name}</code> から自動生成 — <a href="./summary.html">サマリへ戻る</a></footer>
</body>
</html>
"""


def build_pills(categories, titles, current):
    parts = []
    for f in categories:
        stem = f[:-3]
        cls = " class=\"active\"" if f == current else ""
        label = _html.escape(titles.get(f, stem))
        parts.append(f'<a href="./{stem}.html"{cls}>{label}</a>')
    return "\n".join(parts)


def fix_summary_links(root, categories):
    summ = os.path.join(root, "summary.html")
    if not os.path.exists(summ):
        return False
    with open(summ, encoding="utf-8") as f:
        text = f.read()
    original = text
    for f in categories:
        stem = re.escape(f[:-3])
        # href="./xxx.md" / href="xxx.md" -> .html （クエリ/アンカー無しの単純形のみ）
        text = re.sub(r'(href=")(\.?/?)' + stem + r'\.md(")',
                      lambda m: m.group(1) + m.group(2) + f[:-3] + ".html" + m.group(3),
                      text)
    if text != original:
        with open(summ, "w", encoding="utf-8") as f:
            f.write(text)
        return True
    return False


def main():
    root = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
    if not os.path.isdir(root):
        print(f"[render_html] ディレクトリが見つかりません: {root}", file=sys.stderr)
        sys.exit(1)

    convert = _get_md_converter()
    categories = ordered_categories(root)
    if not categories:
        print("[render_html] 変換対象のカテゴリ md がありません。")
        return

    site = first_heading(os.path.join(root, "index.md"), "ブレインマップ")
    titles = {f: first_heading(os.path.join(root, f), f[:-3]) for f in categories}
    updated = find_meta_line(os.path.join(root, "index.md"), "最終更新")

    generated = []
    for f in categories:
        with open(os.path.join(root, f), encoding="utf-8") as fh:
            md_text = fh.read()
        body = convert(md_text)
        page = PAGE_TMPL.format(
            title=_html.escape(titles[f]),
            site=_html.escape(site),
            css=PAGE_CSS,
            pills=build_pills(categories, titles, f),
            body=body,
            md_name=_html.escape(f),
        )
        out = os.path.join(root, f[:-3] + ".html")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(page)
        generated.append(os.path.basename(out))

    fixed = fix_summary_links(root, categories)

    print(f"[render_html] 生成: {len(generated)} ページ")
    for g in generated:
        print(f"  - {g}")
    print(f"[render_html] summary.html リンク補正: {'あり' if fixed else 'なし（変更不要）'}")
    if updated:
        print(f"[render_html] index.md 最終更新: {updated}")


if __name__ == "__main__":
    main()
