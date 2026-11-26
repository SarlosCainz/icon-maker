# テスト用のフォント

`Roboto-Regular.ttf` はテストでだけ使うフォント。アプリが使うフォントは `misc/fonts/` に置く
(リポジトリには含まれない。リポジトリ直下の `README.md` の「フォントを用意する」を参照)。

| 項目 | 内容 |
|---|---|
| フォント | Roboto Regular |
| 著作権 | Copyright 2011 Google Inc. All Rights Reserved. |
| ライセンス | Apache License, Version 2.0 (`LICENSE.txt` が全文) |

`tests/conftest.py` がこの 1 本を 6 ウェイト分のファイル名 (`Roboto-Thin.ttf` 〜 `Roboto-Black.ttf`) に
コピーして、テスト用の作業ディレクトリに `fonts/` を作る。見た目は検証しないため、
どのウェイトも同じ字形になって構わない。
