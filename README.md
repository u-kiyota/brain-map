# brain-map

個人の思考プロセス・作業プロセス・スキル・口癖を AI が参照できるマークダウン形式の知識ベース（ブレインマップ）として体系化・蓄積するリポジトリ。

`brain-map` スキル本体と、生成されたブレインマップファイル（リポジトリ直下に配置）を git で版管理する。**1 リポジトリ＝1 ブレインマップ**を前提とし、`index.md` などの出力はすべてルート直下に置く（GitHub Pages をルートフォルダから配信できるようにするため）。

## このリポジトリの目的

組織やチームで「特定の人の判断・指摘・コミュニケーション様式を AI に学ばせたい」ケースは多い。Slack、Notion、Obsidian、Gmail などに散らばった発言・思考を一度収集し、AI が文脈として読みやすい単位（カテゴリ別マークダウン）に体系化する。差分更新で継続的に蓄積される。

## ディレクトリ構成

1 リポジトリ＝1 ブレインマップ。ブレインマップファイルはすべてリポジトリ直下（ルート）に置く。

```
brain-map/                      # = 1 ブレインマップ
├── README.md                          # このファイル
├── .gitignore                         # 機密ファイルの除外設定
├── index.md                           # 全体サマリ・接する際の注意点
├── _manifest.yaml                     # 情報源と最終取得状態
├── _anonymization.yaml                # 匿名化マッピング（gitignore推奨）
├── work-philosophy.md                 # 仕事哲学
├── communication-style.md             # コミュニケーションスタイル
├── project-management.md              # PM 手法
├── ...                                # カテゴリ別ファイル
└── skills/
    └── brain-map/              # スキル本体
        ├── SKILL.md
        └── references/
            ├── templates.md           # ファイルテンプレートと書き方例
            ├── subagents.md           # サブエージェント実行モデル（取得・抽出）
            └── reorganize.md          # 再整理モードの手順
```

別の対象者を扱う場合は、別リポジトリ（別フォルダ）を用意する。

## 初期セットアップ

### 1. リポジトリをクローン

```bash
git clone <this-repo-url> ~/Documents/brain-map
cd ~/Documents/brain-map
```

### 2. Cowork（Claude Desktop）に Brain Map スキルをインストール

`.skill` ファイルは中身が ZIP のフォルダなので、エクスプローラ操作だけで作れる。

#### 手順（Windows）

1. エクスプローラで `skills\brain-map` フォルダを開く
2. 中の `SKILL.md` と `references` フォルダを **複数選択**
3. 右クリック → **送る → 圧縮（zip 形式）フォルダー**
4. できた `SKILL.zip`（または `references.zip` 等）を `brain-map.skill` にリネーム
   - 拡張子変更の警告が出たら「はい」を選ぶ
   - 拡張子が見えない場合はエクスプローラの「表示 → ファイル名拡張子」をオンにする
5. その `brain-map.skill` を Claude Desktop のウィンドウへドラッグ&ドロップ

#### 手順（macOS）

1. Finder で `skills/brain-map` フォルダを開く
2. `SKILL.md` と `references` フォルダを選択
3. 右クリック → **項目を圧縮**
4. できた `アーカイブ.zip` を `brain-map.skill` にリネーム（拡張子変更の警告は「.skill を使用」）
5. Claude Desktop へドラッグ&ドロップ

#### 重要な注意

- `skills/brain-map` **フォルダごと** 圧縮すると、zip の中に `brain-map/SKILL.md` のような階層ができてしまい認識されないことがある。**フォルダの中身（SKILL.md と references/）を選択して圧縮する**のがコツ
- うまくいかないときは zip の中身を確認し、ルートに `SKILL.md` が直接置かれている構成にする

### 3. Cowork でリポジトリをマウント

Claude Desktop の Cowork セッションで、このリポジトリをフォルダとして接続。

「`~/Documents/brain-map` を開いて」と話すか、フォルダ選択 UI から選ぶ。

スキルはマウント済みフォルダ直下に `_manifest.yaml` や既存のブレインマップファイルがあることを検出し、自動的にこのルート直下を保存先とする。

### 4. 必要なコネクタの接続

ブレインマップ抽出に使う情報源に応じて、以下のコネクタを Claude Desktop で連携：

- **Slack** - Slack コネクタ
- **Notion** - Notion コネクタ
- **Obsidian** - Obsidian MCP（ローカル vault へのアクセス）
- **Gmail** - Gmail コネクタ
- **Google Drive** - Google Drive コネクタ

未連携のコネクタが情報源に含まれる場合、スキルはユーザーに案内する。

## 使い方

### ブレインマップを新規作成

Cowork で以下のように話す：

> 清田のブレインマップを作って

スキルが起動し、以下を聞き取る：

1. 対象者の表示名（slug は `_manifest.yaml` 内の識別子としてのみ使う）
2. 情報源（Slack チャンネル、Notion ページ、Obsidian パス等）

その後、各情報源からデータ取得 → 匿名化 → カテゴリ分類 → ファイル生成を実行する。取得は情報源ごとにサブエージェントへ分割し、メインには圧縮済みダイジェストだけ返す（コンテキスト肥大を防ぐ map-reduce 方式）。

### ブレインマップを更新

> 清田のブレインマップを更新して

リポジトリ直下の `_manifest.yaml` から前回の取得状態を読み込み、差分のみ取得して既存ファイルにマージする。差分取得も情報源ごとのサブエージェントで行う。

### ブレインマップを再整理

> 清田のブレインマップを再整理して

新規データ取得は行わず、既存ファイルの構造だけを整え直す。肥大したカテゴリの分割、薄いファイルの統合、同趣旨の重複解消、`index.md` の作り直しを行う。情報は移送・統合のみで欠落しない。実行前に作業ツリーをコミットしておくと安全。詳細は `skills/brain-map/references/reorganize.md`。

### 出力されるカテゴリ例

スキルはデータ内容に応じて柔軟にカテゴリを分けるが、典型的には以下：

- `work-philosophy.md` - 仕事哲学・大事にしていること
- `life-philosophy.md` - 人生哲学・価値観
- `communication-style.md` - コミュニケーションスタイル・口癖
- `project-management.md` - PM 手法
- `task-management.md` - タスク管理・優先順位付け
- `code-review.md` - ソースレビューの観点
- `requirements-definition.md` - 要件定義の進め方
- `work-approach.md` - 仕事の進め方・成長の仕方
- `people-development.md` - 人材育成・フィードバック方針

## ブレインマップを AI のコンテキストとして使う

生成したブレインマップファイルを AI への指示の前段に読み込ませることで、その人物のスタイル・観点で出力させられる。

### 例: 清田としてコードレビューを書いてもらう

```
以下のファイルを参照してください：
- index.md
- code-review.md

このスタイル・観点で、添付の PR をレビューしてください。
```

### 例: Claude プロジェクトの「指示」に登録

Claude Desktop のプロジェクト機能で、`index.md` と必要なカテゴリファイルを「ファイル」として追加。プロジェクト指示に「常に清田のスタイルで応答する」と書く。

### コンテキスト効率

各ファイルは独立して読めるよう設計されているので、用途に応じて必要なカテゴリだけ読み込む。`index.md` だけで全体像は把握できる。

## 匿名化ポリシー

**対象者本人以外の人名は必ず匿名化される。** スキルが自動的に：

- 他メンバーは `メンバーA`、`上司B`、`クライアントC` 等に置換
- メアド、電話番号、SNS アカウントは除去
- 同一人物には文書全体で同じ匿名 ID を割り当て（`_anonymization.yaml` でマッピング管理）

### 機密ファイル

`_anonymization.yaml` は実名と匿名 ID の対応表であり、機密性が高い。`.gitignore` で除外することを推奨。

ただし、個人 repo で他デバイス間で同期したい場合は、private repo であることを確認のうえ、`.gitignore` から外して commit してもよい。

## トラブルシューティング

### スキルが起動しない

- Claude Desktop の skill 一覧に `brain-map` が表示されているか確認
- インストール後は Cowork セッションを再起動

### 情報取得でエラーが出る

- 該当コネクタ（Slack/Notion/Obsidian/Gmail）が Claude Desktop で接続されているか確認
- Obsidian は vault のローカルパスへのアクセス権が必要

### 差分更新が効かない

- リポジトリ直下の `_manifest.yaml` が壊れていないか確認
- 壊れている場合は manifest を手動編集 or 削除して再作成

### 匿名化漏れに気づいたとき

1. リポジトリ直下の `_anonymization.yaml` を開き、漏れた人物を `anonymized:` に追加
2. スキルを再実行すると、検証サブエージェントが全ファイルを再走査し、未匿名化箇所を検出してメインが修正する（更新・再整理いずれのモードでも検証が走る）

## GitHub Pages で配信する

生成したブレインマップ（リポジトリ直下の `index.md` 等）を GitHub Pages で配信し、ブラウザから閲覧可能にできる。ファイルがルート直下にあるため、Pages の source フォルダを `/`（ルート）に設定するだけで配信できる。

### ⚠️ 公開前の必須チェック

GitHub Pages はデフォルトで **公開（public）** になる。以下を必ず確認：

1. **匿名化漏れがないか** - リポジトリ直下の全ブレインマップファイルを目視確認。対象者本人以外の実名・メアド・電話番号が残っていないか
2. **`.gitignore` が機能しているか** - `git status` で `_anonymization.yaml` が untracked にも tracked にも入っていないことを確認
3. **対象者本人の同意** - 本人が公開を承諾しているか
4. **組織情報の取り扱い** - 所属組織のセキュリティポリシーに違反しないか

社外公開できない場合は **private repo + GitHub Pages の private 公開**（GitHub Enterprise または有料 Pro プラン）を使う。

### セットアップ手順

GitHub Pages は markdown を自動で HTML にレンダリングするので、追加の設定ファイルは不要。

#### 1. GitHub Pages を有効化

GitHub の repo 画面で：

1. **Settings → Pages** を開く
2. **Source** を「Deploy from a branch」に設定
3. **Branch** を `main`、フォルダを `/`（ルート）に設定
4. **Save** をクリック

数分後、`https://<username>.github.io/<repo-name>/` で公開される。ルート直下の `index.md` がトップページとして自動レンダリングされる。

#### 2. 動作確認

ブラウザで `https://<username>.github.io/<repo-name>/` にアクセス。`index.md` がトップページとして HTML レンダリングされ、各カテゴリファイル（`https://<username>.github.io/<repo-name>/code-review` 等）も閲覧できる。

### 更新フロー

ブレインマップを更新したら：

```bash
git add .
git commit -m "Update brain-map"
git push origin main
```

push 後、数分でサイトに反映される。

### カスタムドメインを使う場合

`Settings → Pages → Custom domain` にドメインを設定。DNS の CNAME を `<username>.github.io` に向ける。HTTPS を有効化（推奨）。

## ライセンス・運用上の注意

- このリポ