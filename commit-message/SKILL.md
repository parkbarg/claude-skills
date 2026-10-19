---
name: commit-message
description: 現在のgitの変更内容を読み取り、英語のコミットメッセージを提案する（git add / git commit は実行しない）。変更が論理的に複数ある場合はコミットごとに分けて提案し、それぞれ「本文（description）付き版」と「件名のみ版」の2パターンを出す。ユーザーが「コミットメッセージ作って」「コミットメッセージ考えて」「commit message」「何てコミットすればいい？」などと言ったとき、または変更をコミットする前にメッセージ案を求めているときは必ずこのスキルを使うこと。
---

# Commit Message Proposer

現在の変更を分析し、英語のコミットメッセージを提案する。**提案するだけ**で、リポジトリの状態は変えない。

## やらないこと

- `git add` / `git commit` / `git stash` / `git reset` など、インデックスや履歴を変更するコマンドは実行しない。
  ユーザーは自分でステージングとコミットを行いたいので、こちらが状態を変えると意図しないコミットやステージングの混乱につながる。
- 読み取り専用のコマンド（`git status`, `git diff`, `git log` など）だけを使う。

## 手順

### 1. 変更を把握する

以下を実行して全体像をつかむ:

```bash
git status --short
git diff --staged        # ステージ済みの変更
git diff                 # 未ステージの変更
git log --format='%s' -15  # 既存のコミットスタイル確認
```

未追跡ファイル（`??`）がある場合は中身を読んで何のファイルか把握する。差分が大きい場合は `git diff --stat` で全体を見てから、重要なファイルを個別に読む。

**対象範囲:** ステージ済みの変更がある場合でも、未ステージ・未追跡を含めた作業ツリー全体を対象にする。ただし、どのファイルがステージ済みかは出力で明示する（ユーザーがすでに意図を持ってステージングしている可能性があるため）。

変更がまったくない場合は、その旨を伝えて終了する。

### 2. 論理的なまとまりに分ける

1コミット = 1つの目的、になるように変更をグルーピングする。分ける目安:

- 種類が違う（機能追加 / テスト基盤 / ドキュメント / 設定・依存関係 / リファクタ / バグ修正）
- 互いに独立して revert できる
- 1つのメッセージにまとめると "and" で無関係なものを繋ぐことになる

逆に、機能実装とそのテストのように**一緒でないと意味をなさないもの**は1コミットにまとめる（TDDで書いたテストと実装は通常セット）。

変更が1つのまとまりしかなければ、無理に分けず1コミットとして提案する。

### 3. Conventional Commits に従って書く

[Conventional Commits 1.0.0](https://www.conventionalcommits.org/) に準拠する。既存履歴のスタイルが異なっていても、こちらを優先する（ツールでのCHANGELOG生成やcommitlintとの互換性を保つため）。

構造:

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

**type** — 以下から選ぶ:

| type | 用途 |
|---|---|
| `feat` | 新機能の追加 |
| `fix` | バグ修正 |
| `docs` | ドキュメントのみの変更 |
| `style` | 動作に影響しない書式変更（空白、フォーマット等） |
| `refactor` | 機能追加でもバグ修正でもないコード変更 |
| `perf` | パフォーマンス改善 |
| `test` | テストの追加・修正のみ |
| `build` | ビルドシステム・依存関係の変更（pip, npm 等） |
| `ci` | CI設定の変更 |
| `chore` | 上記に当てはまらない雑務（src/testに触れない変更） |
| `revert` | 以前のコミットの取り消し |

迷ったときの判断: 実装＋テストのセットはテストではなく `feat`/`fix`。依存関係追加は `chore` ではなく `build`。

**scope**（任意）— 変更範囲が明確なときだけ付ける（例: `feat(api):`, `fix(frontend):`, `build(backend):`）。リポジトリに `backend/` `frontend/` のような明確な区分があれば使う。無理に付けない。

**description（件名）**:
- 英語、命令形（"add", "fix" — "added" や "adds" ではない）
- **小文字で始める**（`feat: add goal model`。commitlintのデフォルト設定に合わせる。固有名詞・コード識別子はそのまま）
- 末尾にピリオドを付けない
- ヘッダー全体（type/scope含む）で72文字以内
- 何を変えたかが具体的に分かるように（"update files" のような曖昧な件名は避ける）

**body（本文）**:
- ヘッダーとの間に空行を1行
- **なぜ**変えたか、何が含まれるかを箇条書き（`- `）で2〜5行程度
- 1行72文字程度で折り返す
- 差分を逐一なぞらず、レビュアーが知りたい要点に絞る

**破壊的変更**: APIのレスポンス形式変更、DBスキーマの非互換変更などがある場合は、type/scopeの後に `!` を付け（`feat(api)!: ...`）、さらにfooterに `BREAKING CHANGE: <説明>` を書く。件名のみ版でも `!` は必ず残す。

**footer**: 関連するIssueがdiffやブランチ名から分かる場合のみ `Refs: #123` のように付ける。推測で付けない。

### 4. 注意点をチェックする

メッセージを書く前に、変更内容に以下がないか確認する。コミットされると取り消しが面倒なものを事前に止めるため。

- **秘密情報**: `.env`、APIキー、パスワード、トークン、秘密鍵らしき文字列
- **生成物・不要ファイル**: `__pycache__/`, `node_modules/`, `dist/`, `.venv/`, `*.log`, エディタの設定ファイルなど（`.gitignore` 追加の提案もする）
- **デバッグ用コード**: 追加行にある `print(`, `console.log(`, `debugger`, `breakpoint()`、コメントアウトされた大きなコードブロック
- **大きなファイル**: バイナリや数MB以上のファイル

また、**1つのファイルの中に別のコミットに属する変更が混ざっていないか**を確認する。混ざっている場合、ファイル単位の `git add` では分けられないので、そのファイルは `git add -p` での部分ステージが必要になる。

### 5. 出力する

以下のフォーマットで出力する。説明文は日本語、コミットメッセージ本体は英語。各メッセージはコピーしやすいようにコードブロックに入れる。

````markdown
## ⚠️ 注意点
- `backend/app/main.py` 42行目にデバッグ用の `print(` が追加されています
- `.env` が未追跡ファイルに含まれています。コミット対象から外し、`.gitignore` への追加を推奨します

## コミット 1/N: <このコミットの内容を日本語で一言>

**type/scopeの理由:** Goalモデルという新機能の追加で、変更がbackend配下に閉じているため `feat(backend)`

**対象ファイル:**
- `backend/app/models/goal.py` (staged)
- `backend/tests/test_goal.py`
- `backend/app/main.py` ⚠️ 一部のみ（Goalルーター登録部分。ログ設定の変更はコミット2へ）

**A. description付き**
```
feat(backend): add Goal model with name and color fields

- Define Goal table per docs/03 database design
- Add NOT NULL and length constraints at the DB level
```

**B. 件名のみ**
```
feat(backend): add Goal model with name and color fields
```

**コマンド例（参考・未実行）:**
```bash
git add backend/app/models/goal.py backend/tests/test_goal.py
git add -p backend/app/main.py   # Goalルーター登録の hunk だけ y を選ぶ
git commit -m 'feat(backend): add Goal model with name and color fields' \
  -m '- Define Goal table per docs/03 database design
- Add NOT NULL and length constraints at the DB level'
```

## コミット 2/N: ...
````

各項目の書き方:

- **⚠️ 注意点**: ステップ4で何か見つかったときだけ、先頭にまとめて出す。何もなければこのセクション自体を省略する（毎回「問題なし」と出すとノイズになるため）。
- **type/scopeの理由**: 1行で、なぜそのtype（とscope）を選んだかを日本語で書く。ユーザーがConventional Commitsの使い分けを身につけられるようにするため。
- **対象ファイル**: ステージ済みのものは `(staged)` を付ける。部分ステージが必要なファイルには `⚠️ 一部のみ` を付け、どの変更がこのコミットに含まれ、残りがどのコミットへ行くかを書く。
- **コマンド例**: `git add`（部分ステージが必要なファイルは `git add -p` と、選ぶべき hunk の説明）と、description付き版をそのまま使える `git commit` コマンドを出す。
  - ヘッダーを最初の `-m`、本文を2つ目の `-m` に入れる（git が間に空行を入れてくれる）。破壊的変更のfooterがあれば3つ目の `-m` にする。
  - `$` やバッククォートが展開されないよう、シングルクォートで囲む。メッセージにシングルクォート（`'`）が含まれる場合は `'\''` にエスケープする。
  - これは**表示するだけ**で、実行はしない。件名のみ版を使いたい場合は2つ目の `-m` を削ればよいことは自明なので、コマンドは description付き版の分だけ出す。

複数コミットの場合は、依存関係を考えた**推奨コミット順**で並べる（例: build → feat/fix → test → docs）。コマンド例もその順に実行すればよい形にする。

### 6. まとめ案も出す

コミットが2つ以上に分かれたときは、個別案のあとに「1コミットにまとめる場合」の案も出す。ユーザーが細かく分けずにまとめてコミットしたい場合もあるため。

まとめ案は次の2パターン:

- **列挙型**: 各コミットの scope をカンマでつなぎ、description を `; ` で並べる
  （例: `docs(ideas,work): add AI-era video ideas; add minimal-setup tip`）
  - type がすべて同じときだけ使う（type が違うものは1つのヘッダーに並べられないため）
  - ヘッダーが72文字を超えるときは、各 description を短く言い換える
  - `docs(ideas) and docs(work):` のように type(scope) を複数書く形は Conventional Commits の形式から外れるので使わない
- **要約型**: 変更全体を1つの description に要約する
  （例: `docs: add work tip and new video ideas`）
  - type が違うものが混ざる場合は、いちばん重要な変更の type を使う
  - scope が複数ディレクトリにまたがる場合は scope を省略してよい

出力フォーマット（個別案の後ろに付ける）:

````markdown
## まとめる場合（1コミット）

**対象ファイル:** 個別案の全ファイル

**列挙型 A. description付き**
```
docs(ideas,work): add AI-era video ideas; add minimal-setup tip

- Add video idea on self-worth in the AI era with visual sketches
- Add tip to experiment with a minimal setup when stuck
```

**列挙型 B. 件名のみ**
```
docs(ideas,work): add AI-era video ideas; add minimal-setup tip
```

**要約型 A. description付き**
```
docs: add work tip and new video ideas

- Add tip to experiment with a minimal setup when stuck
- Add video idea on self-worth in the AI era with visual sketches
```

**要約型 B. 件名のみ**
```
docs: add work tip and new video ideas
```

**コマンド例（参考・未実行）:**
```bash
git add <全対象ファイル>
git commit -m '<列挙型または要約型のヘッダー>' -m '<本文>'
```
````
