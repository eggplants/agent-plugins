# 公開する

## 公開できる状態か

報告の前に、次をすべて確かめる。公開しない場合でも、リポジトリは公開できる状態にしておく。

- README の題名が `Unofficial [<名前>](<URL>) Handbook` になっていて、公式の文書と取り違えられない。
- 本文と図に、参考資料の文章や公式の画像を使っていない。
- 参考に渡された目次などのファイル（例: `index`）をコミットしない。作業ディレクトリに残っていれば、消してよいかを聞く。
- 参照用のクローンが `.gitignore` に入っている（`/<repo>/`）。
- `check_book.py` の privacy と publish に何も出ない（実際のホームディレクトリ、メールアドレス、トークン、スクラッチパッドのパス、雛形の置き換え漏れ）。
- `mise run pinup` で、Actions のピン留めを 7 日以上たったバージョンに更新した。
- `mise run ci` が通る。

## 承認を得る

リポジトリを作って push する操作は外に出るので、ユーザーが承認したときだけ行う。AskUserQuestion で、次をまとめて聞く。

- 公開してよいか。リポジトリ名（`<owner>/<repo>`）と、公開される URL（`https://<owner>.github.io/<repo>/`）を示す。
- 本のライセンス。LICENSE がなければ選んでもらう（例: CC BY 4.0、CC BY-SA 4.0、付けない）。こちらで決めない。

## 手順

承認されたら、次の順に進める。

```console
$ git init                       # まだリポジトリでなければ
$ mise run init                  # pnpm install と、git の pre-commit フック
$ git add -A && git status --short
```

`node_modules/`、`_book/`、参照用のクローン、参考の目次ファイルが入っていないことを確かめてから、コミットする。コミットの規約を定めたスキル（同じマーケットプレイスの `commit` プラグインなど）が入っていれば、それに従う。規約がなければ、最初のコミットのメッセージは `init` にする。

```console
$ gh repo create <owner>/<repo> --public --source . --remote origin \
    --description "<book.json の description>"
$ gh api -X POST repos/<owner>/<repo>/pages -f build_type=workflow
$ git push -u origin HEAD
```

- Pages は push の前に有効にする。CI の deploy ジョブは、Pages が有効になっていないと失敗する。先に push して失敗したときは、Pages を有効にしてから `gh workflow run ci.yml -R <owner>/<repo>` で実行し直す。
- Pages の API が拒否されたら、Settings の Pages で Source を「GitHub Actions」にするよう、ユーザーに頼む。

CI の実行を待つ。

```console
$ gh run list -R <owner>/<repo> -L 1
$ gh run watch <run-id> -R <owner>/<repo> --exit-status
```

終わったら、公開した URL が開けることを確かめ（`curl -sIL https://<owner>.github.io/<repo>/`）、リポジトリの Homepage にも設定する。アカウントに独自ドメインを設定していると、`github.io` の URL はそちらへ転送されるので、転送先の URL を使う。

```console
$ gh repo edit <owner>/<repo> --homepage <公開した URL>
```

最後に、リポジトリの URL と公開した URL をユーザーに伝える。
