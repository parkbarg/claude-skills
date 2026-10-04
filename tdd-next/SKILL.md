---
name: tdd-next
description: TODO.md の次の未完了TODOを1つだけ、CLAUDE.md のルールに従ってTDDで進める。
argument-hint: "[任意: 進めたいTODOの文言]"
disable-model-invocation: true
---

# 次のTODOを1つ進める

## 手順
1. `CLAUDE.md` と `TODO.md` を読む
   - 引数でTODOが指定されていればそれを、なければ `TODO.md` の先頭から最初の未完了（`- [ ]`）TODOを1つだけ選ぶ
   - `TODO.md` の確定事項と `docs/` の仕様も確認する
2. 着手前に今回の変更内容を説明する
   - `CLAUDE.md` の「各TDDサイクルの開始時」に挙げられた項目をすべて説明する
3. `CLAUDE.md` の Development style の順番どおりに進める
   - Setupタスクは無理にRed/Greenを作らず、起動・動作確認を完了条件にする
   - 確認できなかった場合は完了にせず、理由と必要な操作を報告する
4. `TODO.md` の該当項目を完了にする
5. `CLAUDE.md` の「各TDDサイクル終了時」の項目を説明して停止する
   - 次のTODOには進まない
