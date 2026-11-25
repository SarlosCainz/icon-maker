# icon-maker

文字と画像を組み合わせて、アプリやサイト用のアイコン画像を作るウェブアプリ。

- 背景色・文字・文字色・フォントのウェイト・サイズ・位置をブラウザで調整しながらプレビューできる
- 画像を重ねて、拡大率・回転・位置を調整できる
- 日本語・英語・簡体字中国語・繁体字中国語のフォントを切り替えられる
- 用途に応じて 3 種類のサイズで書き出せる (汎用 256px / Web 512px / iOS 1024px)

## 構成

1 つのコンテナに静的ファイルの配信と API をまとめている。

```
ブラウザ
  │
  ▼
nginx ─ / ──────────▶ ui のビルド成果物 (/var/www/icon-maker)
   └── /api ─ uwsgi ─▶ Flask (/app)
                        ├ src/app.py   エンドポイント
                        ├ src/img.py   Pillow / Wand での画像生成
                        ├ config.ini   言語・フォント・係数 (bind マウント)
                        └ fonts/       フォント本体 (イメージに同梱)
```

| 層 | 使っているもの |
|---|---|
| フロントエンド | React 17 + Vite + Bulma (`ui/`) |
| API | Flask + Pillow + Wand (ImageMagick) (`src/`) |
| 配信 | nginx + uWSGI (`misc/nginx.conf`, `misc/app.ini`) |

API は 2 つだけ。

| メソッド | パス | 内容 |
|---|---|---|
| `GET` | `/api/lang` | 選択できる言語の一覧と、`Accept-Language` から決めた既定の言語を返す |
| `POST` | `/api/img` | フォームの値からアイコン画像を生成して返す |

デプロイの構成 (レジストリ・ホスト・リバースプロキシ) は非公開のリポジトリで管理している。

## 必要なもの

| ツール | 用途 |
|---|---|
| [Docker](https://docs.docker.com/get-started/get-docker/) | イメージのビルドと実行 |
| [Node.js](https://nodejs.org/) | `ui` のビルド (npm) |
| [uv](https://docs.astral.sh/uv/) | `requirements.txt` の生成 |
| [Task](https://taskfile.dev/) | `Taskfile.yml` の実行 |

Python のパッケージをコンテナの外で動かす場合は、Wand が参照する ImageMagick も必要になる (macOS なら `brew install imagemagick`)。

## フォントを用意する

**フォント本体はリポジトリに含めていない** (`misc/fonts/` は空で、`.gitignore` の対象)。
ビルド自体はフォントが無くても通るが、**画像の生成に失敗する**ため、先に `misc/fonts/` へ置く。

入手元は [Google Fonts](https://fonts.google.com/)。

| 置くファイル名 | フォント | 対応する言語 |
|---|---|---|
| `Roboto-{Thin,Light,Regular,Medium,Bold,Black}.ttf` | [Roboto](https://fonts.google.com/specimen/Roboto) | `en` |
| `NotoSansJP-{...}.otf` | [Noto Sans Japanese](https://fonts.google.com/noto/specimen/Noto+Sans+JP) | `ja` |
| `NotoSansSC-{...}.otf` | [Noto Sans Simplified Chinese](https://fonts.google.com/noto/specimen/Noto+Sans+SC) | `zh-hans` |
| `NotoSansTC-{...}.otf` | [Noto Sans Traditional Chinese](https://fonts.google.com/noto/specimen/Noto+Sans+TC) | `zh-hant` |

- ファイル名は `misc/config.ini` の `[fonts]` のテンプレートに従う。`NotoSansJP-{}.otf` の `{}` にウェイト名
  (`Thin` / `Light` / `Regular` / `Medium` / `Bold` / `Black`) が入る。**この命名のまま置く必要がある**
- Google Fonts の現在の配布形式は可変フォント (`.ttf`) が中心で、ファイル名と拡張子が上の表と変わる。
  その場合は `misc/config.ini` の `[fonts]` を実際のファイル名に合わせて書き換える
- Noto / Roboto のライセンスは [SIL Open Font License 1.1](https://openfontlicense.org/)

## ビルド

```bash
task build
```

`ui` のビルド → `requirements.txt` の生成 → `docker build` をまとめて実行し、`icon-maker:<VERSION>` を作る。
バージョンは `Taskfile.yml` の `VERSION` で持っている。

既定のアーキテクチャは `linux/arm64`。別のアーキテクチャで動かす場合は上書きする。

```bash
task build PLATFORM=linux/amd64
```

## ローカルでの起動

```bash
docker run --rm -p 8000:80 -v "$PWD/misc/config.ini:/app/config.ini:ro" icon-maker:1.0.10
```

`http://localhost:8000/` を開く。`config.ini` は bind マウントしているので、言語や係数を変えるときに
イメージを作り直す必要はない (コンテナの再起動だけでよい)。

## 開発

フロントエンドだけを直す場合は Vite の開発サーバーを使う。

```bash
cd ui && npm install && npm run dev
```

API の参照先は `ui/.env.development.local` の `VITE_API_URL` で切り替える (既定は `http://localhost:5000/api/`)。
API 側は Flask の開発サーバーで動かす。

```bash
uv sync && cd src && uv run flask --app app run --port 5000
```

- `src/app.py` は**カレントディレクトリの** `config.ini` と `fonts/` を参照する。`src/` で動かす場合は
  `misc/config.ini` と `misc/fonts/` へのシンボリックリンクを置く
- ビルド成果物を通して確認したいときは `task build` のあと「ローカルでの起動」の手順を使う

## 設定

`misc/config.ini` でアイコンの生成に関わる値を持っている。

| 節 | 内容 |
|---|---|
| `[lang]` | 選択できる言語のキーと表示名。`/api/lang` が返す一覧になる |
| `[fonts]` | 言語ごとのフォントのファイル名のテンプレート。`{}` にウェイト名が入る |
| `[coefficient]` | 言語ごとの文字幅の係数。文字の描画位置の計算に使う |

言語を増やす場合は 3 つの節すべてに同じキーを足し、対応するフォントを `misc/fonts/` に置く。

## ライセンス

[MIT License](LICENSE)。

フォントは同梱していない。`misc/fonts/` に置くフォントはそれぞれのライセンス (Noto / Roboto は SIL OFL 1.1) に従う。
