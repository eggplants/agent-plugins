# HonKit の注意

HonKit 6.2.5 で確かめたことをまとめる。

## テンプレートの構文

HonKit は Markdown を Nunjucks のテンプレートとして処理してから HTML にする。

- フェンスで囲んだコードブロックと、段落や見出しの中のインラインコードは、HonKit が自動で `{% raw %}` に包む。
- リスト、表、引用の中のインラインコードは包まれない。`{{.Args}}` はビルドのエラーになり、`{{Task}}` はエラーも出さずに空になる。
- リスト、表、引用の中に書くときは、``{% raw %}`{{Task}}`{% endraw %}`` のようにコードごと包む。段落やフェンスのコードブロックに移してもよい。
- コードの外（地の文）には書かない。例えば「acme run {{Task}} での引数の展開」という見出しは、「タスク名を渡したときの引数の展開」のように言い換える。

`check_book.py` はビルドの前にこの書き方を見つけ、ビルドの後にコードがそのまま表示されたかを確かめる。

## SUMMARY.md

- 項目名に書いた `<name>` はバッククォートの中でも HTML のタグとして消える。`&lt;name&gt;` と書く。ページの見出しでは、バッククォートの中に `<name>` とそのまま書いてよい。

  ```markdown
  - [`tasks.&lt;name&gt;.timeout`: タスクごとに制限時間を変える](config/task-timeout.md)
  ```

- サイドバーは項目名をプレーンテキストで表示する。コードの書式が見えるのはページの見出しだけである。
- 部は `## 第 1 部 イントロダクション` のような見出しで分ける。
- SUMMARY.md に載っていないページはビルドされない。

## 検索

既定の lunr は日本語を単語に分けられず、日本語で検索できない。`book.json` で `"plugins": ["-lunr", "-search", "search-pro"]` とし、gitbook-plugin-search-pro を使う。

## バージョン

`pnpm-workspace.yaml` の `minimumReleaseAge` により、pnpm は公開から 7 日以上たったバージョンだけを選ぶ。そのため、HonKit の新しいバージョンが出た直後は、一つ前のバージョンが入る。Dependabot が上げたときや、手で上げたときは、`mise run ci` と画面（検索、図、サイドバー）を確かめる。

## 出力

ビルドの結果は `_book/` に出る。`README.md` は `index.html`、`dir/README.md` は `dir/index.html`、`x.md` は `x.html` になる。`mise run serve` は <http://localhost:4000> で配信し、原稿を変えるたびに作り直す。
