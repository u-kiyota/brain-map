# サブエージェント実行モデル

情報源の生データはコンテキストを肥大させる。Slack の全発言・Notion の DB・Obsidian のノート群を全部メインのコンテキストに読み込むと、すぐに破綻する。これを防ぐため、**重い取得・抽出はサブエージェントの内側に閉じ込め、メインには圧縮済みのダイジェストだけ返す** map-reduce 構造で実行する。

このスキルでは「常に 1 ソース = 1 サブエージェント」を基本とする。小規模なソースでもサブエージェント起動のオーバーヘッドは許容し、一貫した挙動を優先する。

## 全体フロー

```
メイン（オーケストレーター）
  ├─ 準備: _manifest.yaml / _anonymization.yaml を読む。差分カーソルと既知の匿名化マップを確定
  ├─ Map: ソースごとにサブエージェントを起動（読取・抽出専用）
  │     └─ 各サブ → 生データを読む（重い）→ 観察ダイジェスト（軽い）＋登場人物リストを返す
  ├─ Reduce: メインがダイジェストを集約
  │     ├─ 新規登場人物に匿名 ID、新規の組織・固有名詞に汎化ラベルを採番し _anonymization.yaml を更新
  │     ├─ ダイジェスト上で最終匿名化・汎化を適用（生テキストはここには来ない）
  │     ├─ 重要度を集計し核／補助／周辺に格付け、_salience.yaml を更新
  │     └─ 核・補助はカテゴリファイルへ統合、周辺は _archive.md へ退避（書き込みは全てメイン）
  ├─ index.md 合成: 確定したカテゴリ群をサブエージェントに読ませ index.md 草案を受け取る（書き込みはメイン）
  ├─ 検証: 匿名化漏れチェック（必要なら検証サブエージェント）
  └─ manifest 更新 → present_files
```

## 破綻を防ぐ 2 つの不変条件

### 不変条件 1: 匿名化はメインが中央集権で行う

サブエージェントが各自で匿名化すると、同一人物が片方で `メンバーA`、別方で `メンバーC` になり一貫性が壊れる。同じことは会社名・製品名・案件名にも起こる。サブは ID／汎化ラベルを採番しない。

- **サブの責務**: 生テキストを読み、観察を抽出する。本文中の人物・組織固有名詞（会社名・製品名・サービス名・案件名・社内固有用語）は **実名のまま** ダイジェスト内の引用に残し、別途「登場人物リスト（`people_seen`）」「組織・固有名詞リスト（`entities_seen`）」として列挙して返す。サブには既知の `_anonymization.yaml` を渡しておき、既存 ID／ラベルが判明するものにはそれを併記させる（新規は実名のまま `未採番` と報告）。
- **メインの責務**: 全サブのダイジェストが揃ったら、新規人物に匿名 ID、新規の組織・固有名詞に汎化ラベルを採番、`_anonymization.yaml`（`anonymized`／`entities`）を更新し、ダイジェスト本文へ最終置換を適用してからカテゴリファイルへ書く。

ダイジェストは軽いので、実名がメインに一時的に来てもコンテキストはほぼ膨らまない。膨らむのは生メッセージ本文であり、それはサブの内側に留まる。

### 不変条件 2: ファイル書き込みはメインが独占する

複数サブが同じカテゴリファイル（例 `communication-style.md`）に並列書込すると競合し、内容が失われる。

- サブは出力ファイル（リポジトリ直下のブレインマップ md・`index.md`・`_manifest.yaml` など）を **一切書かない・編集しない**（読取専用）。
- カテゴリファイルの作成・追記・統合・`index.md` 更新・`_manifest.yaml` 更新は全てメインが行う。

## 観察ダイジェストの schema

各 fetch+extract サブエージェントは、自然文の散文ではなく次の構造で返す。これにより Reduce が機械的にマージできる。

```yaml
source_id: slack-from-user          # manifest の id
fetched_range:                      # 差分更新の起点・終点
  from: "1716100000.123456"
  to:   "1765337149.503899"
items_seen: 312                     # 読んだ生アイテム数（メッセージ/ページ/ファイル）

observations:                       # カテゴリ候補ごとの抽出。空のカテゴリは省く
  - category: communication-style   # SKILL.md のカテゴリ命名に従う
    principle: "結論を先に出し、理由は後から短く添える"
    salience:                       # 重要度シグナル（メインの格付け材料。SKILL.md「重要度モデル」参照）
      occurrences: 7                # このソース内で同趣旨が観測された回数（≒頻度）
      intensity: strong             # strong/medium/weak。強調語・反復・感情の強さ
      consistency: stable           # stable=文脈をまたいで一貫 / situational=状況限定の一回性
    evidence:                       # 具体例・引用。文脈必須
      - quote: "で、結局これって何の課題を解いてるんだっけ？"
        context: "議論が手段先行になったときの軌道修正"
        people_refs: []             # この引用に出てくる本人以外の人物（実名）
        entity_refs: []             # この引用に出てくる会社/製品/案件名（実名）
  - category: feedback-style
    principle: "良い点を具体で挙げてから改善点に入る"
    salience:
      occurrences: 1               # 一回きり
      intensity: weak
      consistency: situational     # 一回性・状況限定 → メインが周辺=退避候補と判断しうる
    evidence:
      - quote: "ここの設計判断、理由まで書けてるのが良い。次は代替案も一行で"
        context: "PR レビューコメント"
        people_refs: ["山田"]
        entity_refs: []

people_seen:                        # このソースで言及された本人以外の人物
  - name: "山田"
    known_id: メンバーA              # 渡した _anonymization.yaml で判明すれば記入、なければ "未採番"
    role_hint: "エンジニア（部下）"   # 役割推定（匿名 ID 採番の参考）
  - name: "佐藤"
    known_id: 未採番
    role_hint: "デザイナー"

entities_seen:                      # 会社が特定できる固有名詞（会社/製品/案件/社内固有用語）
  - name: "株式会社サンプル"
    type: company-client            # company-self/company-client/product/project/jargon など
    known_label: クライアントB社     # 渡した _anonymization.yaml で判明すれば記入、なければ "未採番"
  - name: "[abc]"
    type: project
    known_label: 未採番
    note: "案件タグ。Slack の角括弧表記で頻出"

data_gaps:                          # 観測量が薄い領域。メインが「データ不足」と明記する材料
  - "意思決定の具体例はこのソースには乏しい"

cursor_update:                      # manifest に書き戻す最新位置
  last_message_ts: "1765337149.503899"
```

ルール:
- `observations` は SKILL.md のカテゴリ命名（`communication-style` 等）に従う。サブが新カテゴリを思いついたら `category: 新規:<案>` の形で提案し、採否はメインが判断する。
- 推測で埋めない。観測がなければそのカテゴリは出さない。薄い領域は `data_gaps` に書く。
- 引用は必ず `context` 付き。文脈なしの引用は AI が誤適用するため返さない。
- `salience` は観察ごとに必ず付ける。`occurrences` はこのソース内で同趣旨が現れた実数（数えられないときは概数）。`intensity`/`consistency` は観測に即して判定し、推測で盛らない。サブは階層（核／補助／周辺）の最終判定はしない（メインが全ソース横断で行う）。

## fetch+extract サブエージェントのプロンプト雛形

メインが Agent ツールで起動する際の指示テンプレート。`{...}` をメインが埋める。サブはこの 1 通で自己完結する必要がある（会話履歴を見ていない前提）。

```
あなたはブレインマップ抽出の調査担当です。対象者「{表示名}」（別名: {aliases}）の
思考・作業プロセス・口癖・観点を、1 つの情報源から抽出してください。

【情報源】
- 種別: {slack | notion | obsidian | gmail | gdrive}
- 識別子: {channel_id / url / path / query など}
- 取得範囲: {差分カーソル以降のみ。初回は全期間}
- 取得手順: {下の「ソース別取得手順」を該当分だけ転記}

【既知の匿名化マップ】（人物特定の参考。あなたは ID を新規採番しない）
{_anonymization.yaml の anonymized 抜粋}

【あなたの責務】
1. 上記手順で生データを取得し、全件に目を通す。
2. 対象者本人の発言・記述から、思考/コミュニケーション/PM/レビュー/FB 等の
   パターンを抽出する。抽象原則と、それを裏づける具体的な引用（文脈付き）をセットにする。
   各原則に salience（occurrences=このソース内の同趣旨の出現回数、intensity=言い方の強さ、
   consistency=一貫/状況限定）を必ず付ける。階層（核/補助/周辺）の判定はしない。
3. 本文中の人物は実名のまま引用に残し、別途 people_seen に列挙する。
   既知マップで ID が分かる人物は known_id に記入、不明なら "未採番"。
4. 本文中の会社が特定できる固有名詞（会社名・製品名・サービス名・案件名/コード・
   社内固有の制度名や用語）も実名のまま引用に残し、entities_seen に列挙する。
   既知マップでラベルが分かるものは known_label に記入、不明なら "未採番"。
   汎用ツール名（Slack/GitHub/Notion 等の一般的なツール）は固有の社内文脈がなければ列挙不要。
5. 観測が薄い領域は data_gaps に書く。推測で埋めない。

【禁止事項】
- 出力ファイル（リポジトリ直下のブレインマップ md・index.md・_manifest.yaml 等）を書いたり編集したりしない（あなたは読取専用）。
- 匿名 ID・汎化ラベルを新規に採番しない（メインが行う）。固有名詞は実名のまま残し列挙する。
- 観測のない事柄を創作しない。

【出力】
references/subagents.md の「観察ダイジェストの schema」の YAML 形式のみを返す。
前置き・要約文は不要。生メッセージ本文の全文は返さない（引用は要点のみ）。
```

## ソース別取得手順（サブに転記する断片）

メインは該当ソースの手順だけをサブのプロンプトに埋め込む。詳細仕様は SKILL.md「情報源別の取得ガイド」と freee-api-skill 等の各コネクタ参照。

- **Slack**: `slack_search_public_and_private` で `from:<user_id>` 指定。テーマ別クエリ（報連相 / 課題 / FB / レビュー 等）で横断サンプリング。スレッドは `slack_read_thread` で深掘り。差分は `last_message_ts` 以降。
- **Notion（ページ）**: `notion-fetch` で URL 指定。差分は `last_edited_time` 比較。
- **Notion（DB）**: data_source を fetch → 各ページを fetch。ページ単位で `last_edited_time` を見て差分のみ。
- **Obsidian**: ディレクトリは `obsidian_list_files_in_dir` → `obsidian_batch_get_file_contents`。差分は本文ハッシュ（`md5`）比較。新規ファイルも取り込む。
- **Gmail**: `search_threads` でクエリ実行。差分は `internalDate` / メッセージ ID 以降。
- **Gmail（Gemini 会議メモ → 文字起こし）**: `from:gemini-notes@google.com` で会議を列挙 → 各 thread を `get_thread(FULL_CONTENT)` し本文から会議メモ Doc リンク `docs.google.com/document/d/<DOC_ID>` を抽出 → Drive `read_file_content(<DOC_ID>)` で Doc 全文取得（後半の `# 文字起こし` セクションに `**発言者名:**` ラベル付きで全発言）。**発言者が明確に対象者本人とラベルされた発言のみ**抽出（曖昧・混線箇所は不使用）。要約部の記述は補助、引用は実発言から。**1 会議 = 1 サブエージェント**で全文をサブ内に閉じ込める。差分は `internalDate` 以降。
- **Google Drive**: `read_file_content` / `download_file_content`。差分は `modifiedTime`。

## Reduce（メインによる合成）の手順

1. 全サブのダイジェストを受け取る。
2. `people_seen` を横断的に突合。`未採番` の人物に役割ベースの匿名 ID（`メンバーA`, `上司B`, `クライアントC` 等）を採番。表記ゆれを alias として束ねる。`_anonymization.yaml` の `anonymized` を更新。
2.5. `entities_seen` を横断的に突合。`未採番` の組織・固有名詞に種別ベースの汎化ラベル（`自社`, `クライアントA社`, `主力プロダクト`, `案件P` 等）を採番。表記ゆれ（正式名・略称・英字・カナ・角括弧タグ）を alias として束ねる。`_anonymization.yaml` の `entities` を更新。汎用ツール名は対象外。
3. ダイジェスト内の引用・本文に最終置換を�
