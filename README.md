# 🏇 OddsPark 自動入金・精算ツール

OddsSparkへの毎月の入金・精算処理を自動化するツールです。  
GitHub Actionsを使ったサーバーレス構成で、指定した日時に自動実行されます。

---

## 機能

- OddsSparkへの自動ログイン
- 毎月指定日に自動で入金処理
- 入金後に自動で精算処理
- GitHub Actionsによるサーバーレス実行（PC不要）

---

## 技術スタック

| 用途 | 技術 |
|------|------|
| ブラウザ自動化 | [Playwright](https://playwright.dev/python/) |
| 定期実行 | GitHub Actions (cron) |
| 認証情報管理 | GitHub Secrets |

---

## ファイル構成

```
.
├── task.py                          # メイン処理スクリプト
├── .github/
│   └── workflows/
│       └── monthly-task.yml         # GitHub Actions ワークフロー定義
└── README.md
```

---

## セットアップ

詳細な手順は [github_actions_setup.md](./github_actions_setup.md) を参照してください。

### 1. リポジトリを Private で作成

> ⚠️ 認証情報を扱うため、必ず **Private** リポジトリにしてください。

### 2. GitHub Secrets を登録

`Settings` → `Secrets and variables` → `Actions` から以下を登録します。

| Secret名 | 内容 |
|----------|------|
| `SITE_ID` | OddsSparkのログインID |
| `SITE_PASSWORD` | OddsSparkのパスワード |
| `SITE_PIN` | OddsSparkの暗証番号 |
| `SITE_AMOUNT` | 毎月の入金額（例：`10000`） |

### 3. 実行日時を設定

`.github/workflows/monthly-task.yml` の `cron` を変更します。  
※ GitHub ActionsのcronはUTC基準です（JST = UTC+9）

```yaml
# 例：毎月1日 9:00 JST に実行
- cron: '0 0 1 * *'
```

---

## 手動実行

`Actions` タブ → `OddsPark Monthly Task` → `Run workflow` から手動実行できます。

---

## 注意事項

- 本ツールの使用はOddsSparkの利用規約の範囲内でご利用ください
- 認証情報はGitHub Secretsで管理し、コードに直接記載しないでください
- GitHubの無料枠（月2,000分）で十分運用可能です
