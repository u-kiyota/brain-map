# Templates and Examples

各ファイルのテンプレートと、書き方の具体例。

## ディレクトリ構成

1 リポジトリ＝1 ブレインマップ。ブレインマップファイルはすべてリポジトリ直下（ルート）に置く。

```
<repo>/                    # = 1 ブレインマップ
├── index.md
├── _manifest.yaml
├── _anonymization.yaml
├── _salience.yaml         # 重要度メタ（頻度・情報源・最終観測。出力には出さない）
├── _archive.md            # 退避した低重要度の観察（復元・昇格用）
├── work-philosophy.md
├── communication-style.md
├── project-management.md
├── code-review.md
├── ... (他カテゴリ)
└── skills/brain-map/   # スキル本体
```

`_` で始まるファイルは管理用、それ以外は AI の知識ベース本体。`_archive.md` は管理用だが匿名化対象に含める。

---

## index.md テンプレート

```markdown
# <表示名>

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
    