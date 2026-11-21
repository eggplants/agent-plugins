# japanese-oss-handbook

任意の OSS について、日本語のハンドブック（使い方の解説書）を [HonKit](https://github.com/honkit/honkit) で書き、GitHub Pages で公開できるリポジトリに整える Claude Code のスキルです。

## 入れ方

```text
/plugin marketplace add nanaism/yomiyasu
/plugin marketplace add anthropics/claude-plugins-community
/plugin install japanese-oss-handbook --marketplace eggplants/agent-plugins
```

最初の 2 行で、[依存するプラグイン](#依存するプラグイン)のマーケットプレイスを追加します。追加してあれば、japanese-oss-handbook を入れるときに yomiyasu と eli5 も一緒に入ります。追加せずに入れると、japanese-oss-handbook は読み込まれません。その場合も、あとからマーケットプレイスを追加すれば、そのときに依存が入ります。

## 頼み方の例

| 頼み方 | 内容 |
|---|---|
| 「junegunn/fzf のハンドブックを作って」 | 最新のリリースを調べ、章立ての案を見せてから書きます |
| 「この目次に沿って acme-cli の本を作りたい」 | 添えた目次の章立てを、今のバージョンに合わせて書きます |
| `/japanese-oss-handbook:japanese-oss-handbook https://github.com/acme/acme-cli` | スキルを直接呼びます |
| 「このハンドブックの見出しを規則どおりに直して」 | 見出し、目次、本文のリンクをまとめて直します |
| 「できたハンドブックを公開して」 | 確認を取ってから、GitHub に Public なリポジトリを作り、GitHub Pages に公開します |

## すること

- 対象のソースを読み、隔離した環境で実際に動かした出力だけを実行例に載せます。
- 見出しの形、ページどうしのリンク、HonKit の落とし穴（テンプレートの構文、目次の `<` と `>`）を、同梱のスクリプトで検査します。
- 図は SVG で描き、PNG にして見た目を確かめます。
- リポジトリには、mise のタスク、rumdl・tombi・actionlint の設定、lint とビルドと GitHub Pages への公開を行う GitHub Actions、Dependabot を用意します。

## 必要なもの

| もの | 使いみち |
|---|---|
| [mise](https://mise.jdx.dev) | Node.js、pnpm、linter の導入と、タスクの実行 |
| Python 3 | 同梱のスクリプト |
| Git と [GitHub CLI](https://cli.github.com) | 対象のクローン、リリースの確認、公開 |
| curl | [併用するスキル](#併用するスキル)の取得 |
| Google Chrome か Chromium | 図とページの見た目の確認。なければ、rsvg-convert か ImageMagick で図だけを確かめます |
| 対象をビルドする道具 | Go や Rust など、対象の OSS に合わせて |

## 依存するプラグイン

推敲と図の方針は、次のプラグインに任せています。どちらも必須で、入っていないか無効になっていると、japanese-oss-handbook は読み込まれません。

| プラグイン | マーケットプレイス |
|---|---|
| `yomiyasu` | [nanaism/yomiyasu](https://github.com/nanaism/yomiyasu)（`yomiyasu`） |
| `eli5` | [anthropics/claude-plugins-community](https://github.com/anthropics/claude-plugins-community)（`claude-community`） |

## 併用するスキル

文章の規範は、gist で配られている次のスキルに任せています。

| スキル | 入手先 |
|---|---|
| `japanese-tech-writing` | [k16shikano 氏の gist](https://gist.github.com/k16shikano/fd287c3133457c4fd8f5601d34aa817d) |
| `cognitive-rhythm-writing` | [k16shikano 氏の gist](https://gist.github.com/k16shikano/eb2929f13ed19c97188393d297be8432) |

入っていなければ、スキルを使い始めるときに [`install_skills.sh`](skills/japanese-oss-handbook/scripts/install_skills.sh) が gist の最新版を curl で取得し、`~/.claude/skills/<名前>/SKILL.md` に置きます。すでに置いてあるスキルには触りません。取得できなかったときは残りのスキルで進みますが、文章の質が下がります。

## 中身

```text
skills/japanese-oss-handbook/
├── SKILL.md      # 手順と、必ず守る規則
├── references/   # 調査、本文、図、HonKit の注意、公開の手順
├── scripts/      # 併用するスキルの導入、雛形の作成、規則の検査、図とページの撮影
└── assets/       # リポジトリの雛形と、図のひな形
```
