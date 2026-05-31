# Templates and Examples

各ファイルのテンプレートと、書き方の具体例。

## ディレクトリ構成

1 リポジトリ＝1 ブレインマップ。ブレインマップファイルはすべてリポジトリ直下（ルート）に置く。

```
<repo>/                    # = 1 ブレインマップ
├── index.md
├── summary.html           # index.md の人間閲覧用 HTML（手動キュレーション）
├── _manifest.yaml
├── _anonymization.yaml
├── _salience.yaml         # 重要度メタ（頻度・情報源・最終観測。出力には出さない）
├── _archive.md            # 退避した低重要度の観察（復元・昇格用）
├── work-philosophy.md
├── work-philosophy.html   # 各カテゴリの人間閲覧用 HTML（render_html.py が自動生成）
├── communication-style.md
├── communication-style.html
├── project-management.md
├── project-management.html
├── code-review.md
├── code-review.html
├── ... (他カテゴリ md ＋ 同名 .html)
└── skills/brain-map/       # スキル本体（scripts/render_html.py を同梱）
```

`_` で始まるファイルは管理用、それ以外は AI の知識ベース本体。`_archive.md` は管理用だが匿名化対象に含める。`summary.html`・各 `<category>.html` は人間閲覧用の派生物（`scripts/render_html.py` から再生成可能）で、AI の知識ベース本体ではない。

---

## index.md テンプレート

先頭（タイトル直下）に人間用サマリ HTML（`summary.html`）への誘導リンクを必ず入れる。

```markdown
# <表示名>

> 📄 **人間用サマリ（HTML）はこちら → [summary.html](./summary.html)**（ブラウザで開くと見やすく整理されています）

> 最終更新: YYYY-MM-DD
> 情報源: Slack（XX チャンネル）、Notion（YY DB）、Obsidian（メンバーノート）

## サマリ

<3-5 文で人物像を要約。役割・専門性・思考の特徴を凝縮する>

## 役割・立場

- <組織内のポジション>
- <主要な責任範囲>
- <意思決定権限のスコープ>

## 強み・専門領域

- <領域 1>
- <領域 2>
- ...

## 思考の特徴

- <どう考えるか、を 1 行で>
- <例: 物事を「構造」と「具体」で行き来する。抽象論の後に必ず実例を求める>
- ...

## コミュニケーションの特徴

- <例: 結論先出し。理由は後から短く>
- <例: 質問に質問で返すことが多い（背景理解の確認）>
- ...

## 接する際の注意点

> 他のメンバーが協働する際に気をつけるべき点

### 大切にしていること（仕事・人生）

> 本人が判断・行動の軸にしている価値観。協働者がまず押さえるべき土台

- <例: 「誰の何の課題か」が曖昧なまま進むことを最も嫌う。課題ドリブンを徹底する>
- <例: 短期の効率より、メンバーが自分で考えて学べる進め方を重視する>
- ...

### 誤解されやすいこと（意図と受け取りのギャップ）

> 本人の意図と、相手の受け取られ方がずれやすい言動。「実際の意図」と「誤解されがちな受け取り」をセットで書く

- <例: 端的に指摘を返すため「冷たい・否定された」と受け取られがちだが、本人は論点を早く前に進めたいだけで人格評価の意図はない>
- <例: 「なぜ？」を重ねるのは詰問ではなく、背景理解と前提合わせのため>
- ...

### その他の協働上の注意点

- <例: 情報が不足した状態での提案は嫌う。事前調査を必ず添える>
- <例: 数値・根拠を求められるので、感覚値だけで話さない>
- ...

## 知識ベース

- [仕事哲学](./work-philosophy.md)
- [コミュニケーションスタイル](./communication-style.md)
- [プロジェクトマネジメント](./project-management.md)
- [コードレビュー](./code-review.md)
- [人材育成](./people-development.md)
- ...
```

---

## summary.html テンプレート

`index.md` の人間閲覧用 HTML。`index.md` を作成・変更したら必ず同じ内容で再出力する（派生物なので常に index.md と一致させる）。外部依存なしの自己完結した単一 HTML（CSS インライン）にし、ぱっとスキャンできるよう以下の構成にする:

- **ヘッダー**: 表示名・役割・最終更新・情報源
- **サマリ**: index.md「サマリ」を強調表示
- **プロフィールのカードグリッド**: 強み／思考の特徴／コミュニケーションの特徴／役割・立場
- **接する際の注意点**: 「大切にしていること」「誤解されやすいこと」「その他の協働上の注意点」を色分け（最重要セクションとして目立たせる）
- **知識ベース**: 各カテゴリの `<category>.html`（人間閲覧用ページ）へのリンクカード。`.md` ではなく `.html` に張る（閲覧者が HTML だけで回遊できるように）。手書き段階で `.md` のまま書いても `render_html.py` が `.html` に補正する
- 匿名化は index.md と同じく適用（実名・社名等を入れない）

下記を雛形として、`index.md` の実内容で各プレースホルダ・リストを差し替える。

```html
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title><表示名> — ブレインマップ サマリ</title>
<style>
  :root{
    --bg:#f6f7f9; --panel:#ffffff; --ink:#1c2430; --muted:#5f6b7a;
    --line:#e6e9ee; --accent:#2f6f6b; --accent-soft:#e7f1f0;
    --warn:#b4612a; --warn-soft:#fbeee2;
    --shadow:0 1px 2px rgba(20,30,45,.04),0 8px 24px rgba(20,30,45,.06);
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);line-height:1.75;
    font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN","Yu Gothic",Meiryo,sans-serif;
    -webkit-font-smoothing:antialiased;}
  .wrap{max-width:960px;margin:0 auto;padding:32px 20px 80px}
  header.hero{background:linear-gradient(135deg,#2f6f6b 0%,#27585a 100%);color:#fff;
    border-radius:18px;padding:34px;box-shadow:var(--shadow);}
  header.hero h1{margin:0;font-size:32px;letter-spacing:.04em}
  header.hero .role{margin:8px 0 0;font-size:15px;opacity:.92}
  header.hero .meta{margin-top:16px;font-size:12px;opacity:.78;line-height:1.6}
  .summary{background:var(--panel);border:1px solid var(--line);border-left:5px solid var(--accent);
    border-radius:14px;padding:22px 24px;margin:22px 0;box-shadow:var(--shadow);font-size:15.5px;}
  .summary strong{color:var(--accent)}
  section{margin-top:34px}
  h2.sec{font-size:13px;letter-spacing:.14em;color:var(--accent);font-weight:700;
    text-transform:uppercase;margin:0 0 14px;display:flex;align-items:center;gap:10px;}
  h2.sec::before{content:"";width:22px;height:2px;background:var(--accent);border-radius:2px}
  .grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
  @media(max-width:680px){.grid{grid-template-columns:1fr}}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px 20px;box-shadow:var(--shadow);}
  .card h3{margin:0 0 10px;font-size:15px}
  .card ul{margin:0;padding-left:0;list-style:none}
  .card li{position:relative;padding:5px 0 5px 18px;font-size:14px;border-top:1px solid var(--line)}
  .card li:first-child{border-top:none}
  .card li::before{content:"";position:absolute;left:2px;top:13px;width:6px;height:6px;border-radius:50%;background:var(--accent)}
  .card li b{color:var(--accent);font-weight:600}
  .attn{background:var(--panel);border:1px solid var(--line);border-radius:16px;box-shadow:var(--shadow);overflow:hidden}
  .attn .group{padding:20px 24px;border-top:1px solid var(--line)}
  .attn .group:first-child{border-top:none}
  .glabel{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.06em;padding:4px 12px;border-radius:999px;margin-bottom:12px}
  .glabel.core{background:var(--accent-soft);color:var(--accent)}
  .glabel.warn{background:var(--warn-soft);color:var(--warn)}
  .glabel.note{background:#eef1f5;color:var(--muted)}
  .attn dl{margin:0}
  .attn dt{font-weight:600;font-size:14.5px;margin-top:14px}
  .attn dt:first-of-type{margin-top:0}
  .attn dd{margin:3px 0 0;font-size:13.5px;color:var(--muted);line-height:1.7}
  .attn .flat{font-size:14px;padding:6px 0 6px 18px;position:relative;border-top:1px solid var(--line)}
  .attn .flat:first-of-type{border-top:none}
  .attn .flat::before{content:"";position:absolute;left:2px;top:14px;width:6px;height:6px;border-radius:50%;background:var(--warn)}
  .attn .flat b{font-weight:600}
  .kb{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
  @media(max-width:680px){.kb{grid-template-columns:1fr}}
  .kb a{display:block;background:var(--panel);border:1px solid var(--line);border-radius:12px;
    padding:14px 16px;text-decoration:none;color:var(--ink);box-shadow:var(--shadow);transition:.15s;}
  .kb a:hover{border-color:var(--accent);transform:translateY(-1px)}
  .kb a .t{font-weight:600;font-size:14.5px;color:var(--accent)}
  .kb a .d{font-size:12.5px;color:var(--muted);margin-top:4px;line-height:1.6}
  .lede{font-size:13px;color:var(--muted);margin:-6px 0 14px}
  footer{margin-top:40px;text-align:center;font-size:12px;color:var(--muted)}
</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <h1><表示名></h1>
    <p class="role"><役割・立場を1行で></p>
    <p class="meta">最終更新: YYYY-MM-DD<br>情報源: <情報源の要約></p>
  </header>

  <div class="summary"><index.md「サマリ」を <strong> で要点強調しつつ転記></div>

  <section>
    <h2 class="sec">人物プロフィール</h2>
    <div class="grid">
      <div class="card"><h3>強み・専門領域</h3><ul><!-- li を列挙 --></ul></div>
      <div class="card"><h3>思考の特徴</h3><ul><!-- li を列挙 --></ul></div>
      <div class="card"><h3>コミュニケーションの特徴</h3><ul><!-- li を列挙 --></ul></div>
      <div class="card"><h3>役割・立場</h3><ul><!-- li を列挙 --></ul></div>
    </div>
  </section>

  <section>
    <h2 class="sec">接する際の注意点</h2>
    <p class="lede">他のメンバーが協働・対話するうえで押さえておくべきこと</p>
    <div class="attn">
      <div class="group">
        <span class="glabel core">大切にしていること（仕事・人生）</span>
        <dl><!-- dt（見出し）+ dd（説明）を列挙 --></dl>
      </div>
      <div class="group">
        <span class="glabel warn">誤解されやすいこと（意図と受け取りのギャップ）</span>
        <dl><!-- dt + dd を列挙 --></dl>
      </div>
      <div class="group">
        <span class="glabel note">その他の協働上の注意点</span>
        <!-- <div class="flat"><b>...</b> ...</div> を列挙 -->
      </div>
    </div>
  </section>

  <section>
    <h2 class="sec">知識ベース（詳細ページ）</h2>
    <div class="kb">
      <!-- <a href="./xxx.html"><span class="t">カテゴリ名</span><span class="d">概要</span></a> を列挙（.html に張る） -->
    </div>
  </section>

  <footer><表示名> ブレインマップ — サマリ（人間閲覧用）｜ 詳細は各カテゴリページを参照</footer>
</div>
</body>
</html>
```

---

## カテゴリ HTML と render_html.py

各カテゴリ別 md を人間閲覧用の HTML に変換する処理は、スキル同梱の `scripts/render_html.py` に集約してある。手書きしない（大きいファイルでもコスト一定・体裁が揃う）。

```bash
python3 skills/brain-map/scripts/render_html.py <repo_root>
# <repo_root> 省略時はカレントディレクトリを対象にする
```

挙動:

- `_` 始まり・`README.md`・`index.md` を除く全 `*.md` を `<同名>.html` に変換する（`_archive.md` 等は対象外）。
- 各ページは `summary.html` と統一した配色（同じ CSS 変数 `--accent` 等）・カード調でラップされ、上部に固定ナビを持つ:
  - 「← サマリへ戻る」リンク（`summary.html` へ）
  - 兄弟カテゴリへのピルリンク一覧（現在ページを `active` でハイライト）。並び順は `index.md` の「知識ベース」リンク順を優先し、無いものは末尾にファイル名順で追加。
- 見出し・表・コードブロック・引用・リンクを Markdown として描画する（`markdown` パッケージを使用。未導入なら `pip install markdown --break-system-packages` を自動試行し、失敗時は簡易フォールバック変換）。
- ページタイトルは各 md 冒頭の `# 見出し`、サイト名は `index.md` の `# 見出し` から取る。
- 仕上げに `summary.html` 内のカテゴリへの `href="./xxx.md"` / `href="xxx.md"` を `href="./xxx.html"` に書き換える（`index.md` のリンクは触らない）。

生成される各カテゴリページの骨格（イメージ）:

```html
<!DOCTYPE html>
<html lang="ja">
<head>... <title><カテゴリ名> — <表示名></title> <style>/* summary.html と同系統 */</style></head>
<body>
  <div class="topbar"><div class="inner">
    <a class="home" href="./summary.html">← サマリへ戻る</a>
    <span class="site"><表示名>・ブレインマップ</span>
  </div></div>
  <nav class="pills">
    <a href="./work-philosophy.html" class="active">仕事哲学</a>
    <a href="./communication-style.html">コミュニケーションスタイル</a>
    <!-- 兄弟カテゴリを列挙 -->
  </nav>
  <div class="wrap"><article class="article"><!-- md を変換した本文 --></article></div>
  <footer>このページは <code>work-philosophy.md</code> から自動生成 — <a href="./summary.html">サマリへ戻る</a></footer>
</body>
</html>
```

`summary.html`（手動キュレーション）と `<category>.html`（自動生成）は、いずれも `index.md`／各 md が更新されたら作り直す。古い HTML を残さない。

---

## カテゴリファイル テンプレート

重要度順に構成する。先頭に「コア」、その下に「補助的なパターン」。各節内も重要度降順。周辺の些末は本ファイルに置かず `_archive.md` へ退避する。本文にスコアや出現回数は書かない（重みは節構造と並び順で表す）。

```markdown
# <カテゴリ名>

<このカテゴリの概要を 1-3 文。何について書かれているか>

## コア — 最も大切にしている／繰り返し現れる

> 高頻度・強い確信で一貫して観測される、本人を最も特徴づける項目。重要度の高い順に。

- **<原則タイトル>**: <内容>
  - 例: <具体例>
  - > 「<実際の発言>」 — 文脈: <どんな状況で発したか>
- **<原則タイトル>**: <内容>
  - 例: <具体例>

## 補助的なパターン

> 複数回観測されるが、コアほど中心的ではない／状況依存の項目。

- **<原則タイトル>**: <内容>
  - 例: <具体例>

## 典型的な発言・口癖

> 上のコア／補助に対応する代表的な言い回し。重要度順。

> 「<実際の発言>」
> — 文脈: <どんな状況で発したか>

## アンチパターン（嫌がること）

- <避けるべき行動>
- <受け入れない提案の型>
```

> 周辺（一回きり・弱い・状況限定で本人像にほぼ寄与しない観察）はこのテンプレートに載せず `_archive.md` に退避する。再出現して頻度が上がれば補助／コアへ昇格する。

---

## 良い書き方の例

### Good: 抽象原則 + 具体例 + 引用

```markdown
## 要件定義の進め方

- **「誰の何の問題か」を最初に固定する**: スコープ議論よりも前に課題の主語を明確化する
  - 例: 「経理の月次締めを早める」と言われたら、「経理担当の誰が何時間使っているか」を先に確認する

> 「機能の話の前に、誰の何の問題かを 1 文で言ってほしい」
> — 文脈: 新機能の要件レビューで、解決対象が曖昧なときの定型質問
```

### Bad: 抽象論だけ（AI が再現できない）

```markdown
## 要件定義の進め方

- 課題を明確にすることを重視する
- 解決策より問題を優先する
```

→ これだけでは「どう質問するか」「どこで止めるか」が分からない。具体例・引用を必ず添える。

---

## 発言・口癖の記録ルール

引用ブロックで囲み、必ず**文脈**を添える。文脈なしの発言は AI が誤適用する。

```markdown
> 「で、結局これって何の課題を解いてるんだっけ？」
> — 文脈: 議論が解決策に偏ったときの軌道修正

> 「数値で言うと？」
> — 文脈: 定性的な報告に対する追加質問の定型
```

複数の言い回しがある場合は、バリエーションとして列挙：

```markdown
### 「課題の明確化を促す」言い回し
> 「で、結局これって何の課題を解いてるんだっけ？」
> 「誰の何の問題？」
> 「それ、本当にやる必要ある？」
— 全て、議論が手段先行になったときに使う
```

---

## _manifest.yaml 完全例

```yaml
target:
  display: 清田
  slug: kiyota

created_at: 2026-05-30T12:00:00+09:00
updated_at: 2026-05-30T12:00:00+09:00

sources:
  # Slack チャンネル
  - id: slack-general
    type: slack
    description: "#general"
    channel_id: C01234567
    last_fetched: 2026-05-30T12:00:00+09:00
    last_message_ts: "1716100000.123456"

  # Slack ユーザー横断検索（from: フィルタ）
  - id: slack-from-user
    type: slack
    description: "対象者の全発言（from:フィルタ）"
    user_id: U01234567
    last_fetched: 2026-05-30T12:00:00+09:00
    last_message_ts: "1716100000.123456"

  # Notion ページ単体
  - id: notion-philosophy
    type: notion
    description: "対象者の個人的な仕事理論ノート"
    url: https://www.notion.so/xxxx
    page_id: 1234abcd5678efgh
    last_edited_time: 2026-05-28T10:00:00+09:00

  # Notion データベース（複数ページ）
  - id: notion-review-db
    type: notion
    description: "振り返りシート DB"
    data_source_url: https://www.notion.so/xxxx
    pages:
      - page_id: aaaa1111
        last_edited_time: 2026-05-20T10:00:00+09:00
      - page_id: bbbb2222
        last_edited_time: 2026-05-25T10:00:00+09:00

  # Obsidian
  - id: obsidian-member-note
    type: obsidian
    description: "メンバーノート"
    paths:
      - path: "members/kiyota.md"
        content_hash: "a1b2c3d4e5f6"
        last_fetched: 2026-05-30T12:00:00+09:00
      - path: "members/kiyota-presentation-fb.md"
        content_hash: "f6e5d4c3b2a1"
        last_fetched: 2026-05-30T12:00:00+09:00

  # Gmail
  - id: gmail-from-user
    type: gmail
    description: "対象者からのメール"
    query: "from:user@example.com"
    last_fetched: 2026-05-30T12:00:00+09:00
    last_message_id: "1234abcdef"
    last_internal_date: "1716100000000"

files:
  - index.md
  - work-philosophy.md
  - communication-style.md
  - project-management.md
  - code-review.md
  - people-development.md
  - decision-making.md
```

---

## _anonymization.yaml 完全例

```yaml
# 対象者本人（匿名化しない）
target:
  display: 清田
  aliases:
    - 清田
    - 清田さん
    - きよた
    - キヨタ

# 人名の匿名化対象（他の人物）
anonymized:
  - id: メンバーA
    role: エンジニア（部下）
    aliases:
      - 山田
      - 山田太郎
      - 山田さん
      - やまちゃん
      - ymd

  - id: メンバーB
    role: デザイナー
    aliases:
      - 佐藤
      - 佐藤花子
      - 佐藤さん

  - id: 上司D
    role: CEO
    aliases:
      - 田中
      - 田中CEO

# 組織・固有名詞の汎化対象（会社が特定できる固有名詞）
# type: company-self / company-client / product / project / jargon
entities:
  - id: 自社
    type: company-self
    aliases:
      - 株式会社アクメ
      - アクメ
      - ナントカ社

  - id: クライアントA社
    type: company-client
    aliases:
      - 株式会社サンプル
      - サンプル社
      - サンプル株式会社

  - id: 主力プロダクト
    type: product
    aliases:
    