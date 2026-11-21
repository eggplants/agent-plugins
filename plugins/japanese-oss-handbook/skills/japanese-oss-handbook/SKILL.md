---
name: japanese-oss-handbook
description: 任意の OSS について、日本語のハンドブック（使い方の解説書）を HonKit で書き、Public な GitHub リポジトリとして公開できる状態まで整える。対象のソースを読み、隔離した環境で実際に動かした出力だけを実行例に使い、eli5 の方針で SVG の図を描き、japanese-tech-writing・cognitive-rhythm-writing・yomiyasu の規範で書いて推敲する。mise・rumdl・tombi・actionlint の設定、lint とビルドと GitHub Pages への公開を行う GitHub Actions、Dependabot も用意する。「〇〇 の book / handbook / 解説書 / 入門書 / 日本語ドキュメントを作りたい」「honkit で〇〇 の本を書いて」「既存のハンドブックと同じ形で〇〇 の本を」のような依頼で使う。参考にする目次や既存の本は、添えられていてもいなくてもよい。HonKit で作った日本語のハンドブックの見出しや章を直すとき、公開するときにも使う。
---

# OSS の日本語ハンドブックを作る

対象の OSS を調べ、実際に動かして確かめた内容だけで、日本語のハンドブックを HonKit で書く。リポジトリは公開を前提に整え、最後にユーザーの承認を得てから GitHub に公開する。

このスキルの例には、架空の CLI である acme-cli（コマンドは `acme`、設定ファイルは `acme.toml`）の本を使う。

以下、このスキルのディレクトリ（読み込んだときに表示されるベースディレクトリ）を `$SKILL`、スクラッチパッドの絶対パスを `$S`、作業ディレクトリを `$BOOK` と書く。

## 入力

依頼から次を読み取る。対象の OSS が分からないときだけ聞く。引数があれば、それを対象の OSS とする。

| 項目 | 読み取れないときの既定 |
|---|---|
| 対象の OSS | 聞く。GitHub の URL、`owner/repo`、手元のクローンのどれでもよい |
| 対象のバージョン | 最新のリリース。リリースがなければ既定ブランチの先頭 |
| 参考にする章立て | なし。既存の本の目次などが添えられていれば、それに沿う |
| 作業ディレクトリ | 今のディレクトリが、参考資料やクローンを置いた `*-handbook` ならそこ。そうでなければ `./<リポジトリ名>-handbook/` |
| 公開先 | `github.com/<gh api user の login>/<作業ディレクトリ名>` |

作業ディレクトリに参考の目次（例: `index`）や対象のクローン（例: `acme-cli/`）が置かれていたら、それらを使う。

## 進め方

1. 規範のスキルを読み込む
2. 対象を調べる（references/research.md）
3. 章立てを決める
4. 雛形を作る
5. 本文を書く（references/writing.md）
6. 図を描く（references/figures.md）
7. 点検する
8. 報告する
9. 公開する。ユーザーが承認したときだけ（references/publishing.md）

HonKit 固有の注意は references/honkit.md にある。本文を書く前と、ビルドの結果がおかしいときに読む。

### 1. 規範のスキルを読み込む

Skill ツールで次の四つを読み込み、執筆と推敲のあいだ従う。

- `japanese-tech-writing`: 段落と論証、読み手の負荷、空句の禁止
- `cognitive-rhythm-writing`: 緩急、ページの冒頭、節の入り方
- `yomiyasu:yomiyasu`: 推敲と、検査のスクリプト
- `eli5:eli5`: 図の方針（大きな絵と少ない言葉）

eli5 は HTML の Artifact を作る指示を含むが、ここでは方針だけを借り、図は本の中の SVG として描く。yomiyasu は、名前だけで呼ばれると手元のファイルを推敲しはじめる指示を含むが、ここでは原稿を書き終えてからの推敲と検査に使う。yomiyasu と eli5 はこのプラグインの依存なので、必ず入っている。

japanese-tech-writing と cognitive-rhythm-writing は gist で配られているスキルなので、入っていないことがある。使えるスキルの一覧にどちらかがなければ、読み込む前に次のスクリプトで入れる。スクリプトは gist の最新版を curl で取得し、front matter の `name` がスキル名と合うことを確かめてから `~/.claude/skills/<名前>/SKILL.md` に置く。すでに置いてあるスキルには触らない。

```console
$ "$SKILL/scripts/install_skills.sh"
```

入れたばかりのスキルは、Skill ツールから呼べないことがある。そのときは、スクリプトが表示したパスの SKILL.md を Read ツールで読み、スキルとして読み込んだときと同じように従う。取得に失敗したら残りで進め、報告で触れる。

### 2. 対象を調べる

本に書く事実はすべて、ソースか実行結果で裏を取る。手順は references/research.md にある。要点は次のとおり。

- 対象を `$BOOK/<repo>/` にクローンし、対象バージョンのタグに合わせる。このクローンは参照専用である。
- README、ドキュメント、コマンドやオプションの定義、各コマンドの実装、設定と環境変数を読むところ、CHANGELOG、テストを読む。
- 対象バージョンをビルドし、隔離した HOME（ユーザー名 `alice`）で、本に載せる実行例をすべて動かす。出力は色とパスを整えるだけで、そのまま載せる。
- 対象と、参考にする本や目次のライセンスを確かめる。本文は参考資料の文章を写したり訳したりせず、新しく書く。
- 確かめている途中で見つけた、気をつけたい挙動は本文に書き、報告にも挙げる。

### 3. 章立てを決める

参考の章立てがあれば、その順番と意図を保ったまま、対象バージョンに合わせて直す。

- 新しいコマンドやオプションの章と節を足す。
- 廃止された機能は、読者が探しそうな節で一言触れるだけにする。
- 終了したサービスに頼るレシピは外し、代わりになる題材を入れる。
- 見出しを、下の「見出しの形」に直す。

参考の章立てがなければ、次の構成に倣う。

```text
はじめに                     README.md
第 1 部 イントロダクション
  イントロダクション         intro/README.md
    `<cmd>` とはなにか、動作環境、`<cmd>` の導入
  基本的な使い方             basics/README.md（日々の操作の大半を占める 2〜3 の操作）
第 2 部 使い方               コマンドや機能ごとに 1 章。章の下に、オプションや目的ごとの節
第 3 部 レシピ               ほかのコマンドと組み合わせる実例
付録                         設定と環境変数の一覧など
```

ライブラリなら第 2 部を API や用途ごとの章に、サーバーなら設定・運用・トラブルの対処の章に置き換える。節はフラグ一つごとではなく、読者のやりたいこと一つごとに分ける。規模の目安は、サブコマンドが六つほどの CLI で 40 ページ弱、図 10 枚ほどである。

参考の章立てがないときは、書き始める前に SUMMARY.md の案をユーザーに見せ、承認を得る。章立てを後から変えると、本文、リンク、図をまとめて直すことになるためである。依頼に「確認せずに進めてよい」とあれば省く。

章は `src/<章>/README.md` と `src/<章>/<節>.md` に、節のない章は `src/<名前>.md` に置く。図は `src/images/` に置く。

### 4. 雛形を作る

```console
$ python3 "$SKILL/scripts/scaffold.py" "$BOOK" \
    --oss-url https://github.com/acme/acme-cli \
    --description "設定ファイルに書いたタスクを実行する acme-cli の使い方"
$ cd "$BOOK" && mise trust && mise install
$ pnpm add -D honkit gitbook-plugin-search-pro
$ mise run lint && mise run build
```

scaffold.py は `$SKILL/assets/template/` の設定一式を書き、既にあるファイルは残す。`pnpm-workspace.yaml` の `minimumReleaseAge` により、pnpm は公開から 7 日以上たったバージョンを選ぶ。mise の `minimum_release_age` と同じく、出たばかりのバージョンを入れないための設定である。

| ファイル | 役割 |
|---|---|
| `book.json` | 題名（`<名前> handbook`）、説明、`language: ja`、日本語で検索できる search-pro、`src/styles/website.css` |
| `mise.toml` | ツール（node、pnpm、rumdl、tombi、actionlint、shellcheck ほか）と、`init`、`serve`、`build`、`fmt`、`lint`、`ci`、`pinup` のタスク |
| `.rumdl.toml`、`tombi.toml` | Markdown と TOML の lint。参照用のクローンを除外する |
| `.github/workflows/ci.yml` | `mise run ci` を実行し、既定ブランチなら GitHub Pages に公開する |
| `.github/dependabot.yml` | Actions と npm を月に 1 回、7 日のクールダウン付きで更新する |
| `README.md` | `Unofficial [<名前>](<URL>) Handbook`、CI のバッジ、mise のコマンドだけの英語の README |

`git init` と `mise run init`（pre-commit フックの設定）は、公開の手順で行う。

### 5. 本文を書く

ページの型と細かい表記は references/writing.md にある。次の規則は必ず守る。

#### 文体と実行例

- 常体（である調）で書く。和文と英数字のあいだに半角スペースを入れる。
- 各ページは読者の場面や疑問から入る。「本章では〜を扱う」と宣言しない。
- 実行例は `console` のコードブロックに、入力行を `$` と半角スペースで始めて書く。出力は実際に動かしたものだけを載せる。
- 例のユーザー名は `alice`、ホームは `/home/alice`、架空の組織は `acme`、架空のホストは `example.com` にする。
- 対象バージョンとリリース日は、「はじめに」の「対象バージョン」の節に一度だけ書く。「はじめに」には謝辞の節を置かない。参考にした資料は報告で伝える。

#### 見出しの形

見出しは次の四つの規則に従う。

| 規則 | よい例 | 避ける例 |
|---|---|---|
| コマンドやオプションが主題なら「`コード`: 説明」 | `` `acme rm`: タスクを削除する `` | タスクを削除する（acme rm） |
| 複数のオプションは「 / 」で区切る | `` `--env` / `--env-file`: 環境変数を渡す `` | `` `--env`、`--env-file`: … `` |
| 見出しの中のコマンド、オプション、設定キー、環境変数、ツールのコマンド名はコードにする | `` `cache_dir` でキャッシュの置き場所を変える ``、`` `fzf` や `jq` と組み合わせる `` | cache_dir でキャッシュの置き場所を変える |
| 導入方法の見出しに対応 OS などの注記を付けない | Homebrew | Homebrew（macOS、Linux） |

- 製品名（Git、GitHub、Homebrew、Go）と一般名詞（SSH、URL、VCS）はコードにしない。コマンドが文の途中にある見出しは、語順を変えずにコードにする（`` まとめて `acme sync` する ``）。
- 「（1.6.0 以降）」のようなバージョンの注記は、見出しにも本文にも書かない。動作環境で必要なバージョンを文として書くこと（「Git 2.30 以降が必要になる」）と、廃止の説明（「`acme shell` は 2.0.0 で廃止された」）は注記ではないので書いてよい。

#### ページのつながりと HonKit

- 各ページの H1 と、SUMMARY.md の項目名を同じにする。見出しを変えたら、SUMMARY.md と、その題名を引いている本文のリンクも直す。
- ほかのページに触れるときは、題名を「」で囲んでリンクにする: ``[「`--dry-run`: 実行せずに手順を表示する」](../run/dry-run.md)``。
- SUMMARY.md の項目名では `<` と `>` を `&lt;` と `&gt;` と書く（`` `tasks.&lt;name&gt;.timeout` ``）。
- `{{` と `{%` はコードの中にだけ書く。リスト、表、引用の中のインラインコードは HonKit が保護しないので、`{% raw %}` で包む（references/honkit.md）。

本文は一人で書く。章ごとにサブエージェントへ分けると、文体と用語がずれる。

### 6. 図を描く

eli5 の方針で、構造や流れを一目で見せる図を SVG で描く。概念を初めて出す段落の直後に置き、図の内容は本文でも言葉で説明する。手順、ひな形（`$SKILL/assets/figure-skeleton.svg`）、確かめ方は references/figures.md にある。描いたら `$SKILL/scripts/render_svg.sh` で PNG にし、Read ツールで見て、重なりやはみ出しを直す。

### 7. 点検する

次の順に進める。見つけたものを直してから、次へ移る。

1. 規則の検査。ERROR はすべて直し、WARN は一つずつ見て判断する。`--command` には対象のコマンド名と、本文で扱うほかのツールのコマンド名を渡す（acme-cli の本なら `acme`、`fzf`、`jq`、`mise`、`zsh`）。`--headings` を付けると、見出しを本の順に一覧できる。

   ```console
   $ python3 "$SKILL/scripts/check_book.py" "$BOOK" --command acme --command jq
   ```

2. yomiyasu の lint を全ページにかけ、候補を規範に照らして直す。候補をすべて機械的に直すことはしない。続けて、全ページをつないだファイルを yomiyasu の検査にかける。コマンドは references/writing.md の「yomiyasu の検査」にある。
3. 通読する。`check_book.py --concat "$S/book.md"` でつないだ本を、japanese-tech-writing と cognitive-rhythm-writing の点検の観点で、本の順に読む。通読では、数の食い違い（「三つの利点」のあとに四項目）、主語と述語のずれ、設定の順番のあいまいな説明のような、ページごとの推敲では見落としやすいものが見つかる。
4. `mise run ci`（依存の導入、lint、ビルド）を通す。
5. ビルドのあとに、もう一度 `check_book.py` を実行する。今度は `_book` も調べ、コードの中の `{{ }}` や `<name>`、見出し、サイドバーの項目がそのまま表示されたかを確かめる。HonKit はリストや表の中の `{{Task}}` を、エラーを出さずに空にするので、ビルドが通っただけでは分からない。
6. ページを撮って、Read ツールで見る。「はじめに」、図のあるページ、表やコードの多いページを選ぶ。

   ```console
   $ "$SKILL/scripts/shoot_pages.sh" "$BOOK" "$S/png" index.html run/index.html run/dry-run.html
   ```

### 8. 報告する

日本語で、次の見出しに分けて報告する。

- 内容: ページ数と図の数、対象バージョン、実行例をどう得たか
- 参考資料から変えたところ: 外した節、足した節、見出しを変えた理由
- 確かめていて見つけた挙動: 本文に注意として書いたもの
- 開発環境: 雛形から変えたところ（なければ省く）
- 確認してほしいこと: 決めていないこと（本のライセンス）、参考にした資料の名前とライセンス、動かしていない実行例、7 日の制限で最新ではないバージョンを入れたもの
- 次の操作: `mise run serve` で <http://localhost:4000> から読めること、公開してよいか

### 9. 公開する

GitHub にリポジトリを作って push する操作は外に出るので、ユーザーが承認したときだけ行う。公開できる状態かの点検、承認の取り方、`gh repo create --public` から GitHub Pages の有効化、CI の確認までの手順は references/publishing.md にある。

## 作ったハンドブックを直すとき

見出しの形を変えるなど、既存のハンドブックを直す依頼にも同じ規則を使う。見出し、SUMMARY.md、本文のリンクをまとめて直し、`check_book.py` と `mise run ci` を通し、変えたページをビルドした画面で確かめる。依頼と同じ形のものを範囲の外で見つけたら（例: 見出しのオプションを「 / 」区切りに直す依頼で見つけた、表の中の「、」区切り）、勝手に直さず、報告で尋ねる。
