# agent-plugins

[![ci](https://github.com/eggplants/agent-plugins/actions/workflows/ci.yml/badge.svg)](https://github.com/eggplants/agent-plugins/actions/workflows/ci.yml)

eggplants' Claude Code Plugin Marketplace

## Installation

`japanese-oss-handbook` depends on `yomiyasu` and `eli5` from other
marketplaces. Add those marketplaces first, and the dependencies are installed
along with it:

```bash
claude plugin marketplace add nanaism/yomiyasu
claude plugin marketplace add anthropics/claude-plugins-community
```

```bash
claude plugin install japanese-oss-handbook --marketplace eggplants/agent-plugins
claude plugin install commit --marketplace eggplants/agent-plugins
claude plugin install copilot-review --marketplace eggplants/agent-plugins

claude plugin update japanese-oss-handbook --marketplace eggplants/agent-plugins
claude plugin update commit --marketplace eggplants/agent-plugins
claude plugin update copilot-review --marketplace eggplants/agent-plugins
```

```text
/plugin marketplace add eggplants/agent-plugins

/plugin install japanese-oss-handbook@agent-plugins-for-eggplants
/plugin install commit@agent-plugins-for-eggplants
/plugin install copilot-review@agent-plugins-for-eggplants

/plugin marketplace update agent-plugins-for-eggplants

/plugin update japanese-oss-handbook@agent-plugins-for-eggplants
/plugin update commit@agent-plugins-for-eggplants
/plugin update copilot-review@agent-plugins-for-eggplants
```

## Plugin

| Plugin | Description |
|---|---|
| [`japanese-oss-handbook`](plugins/japanese-oss-handbook) | Write a Japanese handbook for any OSS with HonKit and set up a repository ready to publish on GitHub Pages |
| [`commit`](plugins/commit) | Split git changes into logical units and commit each with a short `type: subject` message |
| [`copilot-review`](plugins/copilot-review) | Verify each unresolved Copilot review comment on a PR, then fix, reply to and resolve it |

## License

[MIT](LICENSE)
