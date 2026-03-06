# OddsPark 自動化 GitHub Actions 設定ガイド

## 目次
1. [事前準備](#1-事前準備)
2. [GitHubリポジトリの作成](#2-githubリポジトリの作成)
3. [ファイルの配置](#3-ファイルの配置)
4. [Secretsの登録](#4-secretsの登録)
5. [実行スケジュールの設定](#5-実行スケジュールの設定)
6. [動作確認](#6-動作確認)
7. [ログの確認方法](#7-ログの確認方法)
8. [トラブルシューティング](#8-トラブルシューティング)

---

## 1. 事前準備

### 必要なもの
- GitHubアカウント（無料）
  - 持っていない場合：https://github.com/signup から作成
- OddsSparkのログイン情報（2アカウント分）
  - ログインID
  - パスワード
  - 暗証番号（PIN）

---

## 2. GitHubリポジトリの作成

1. GitHubにログインし、右上の **「+」** → **「New repository」** をクリック

2. 以下を入力して **「Create repository」** をクリック

   | 項目 | 設定値 |
   |------|--------|
   | Repository name | `oddspark-auto`（任意） |
   | Visibility | **Private**（必ずプライベートにすること） |

   > ⚠️ **重要：必ずPrivateリポジトリにしてください。**
   > Publicにすると第三者にコードが見えてしまいます。

---

## 3. ファイルの配置

リポジトリに以下の2ファイルを作成します。

### ディレクトリ構成

```
oddspark-auto/
├── task.py
└── .github/
    └── workflows/
        └── monthly-task.yml
```

### 3-1. `task.py` の作成

1. リポジトリのトップページで **「Add file」** → **「Create new file」** をクリック
2. ファイル名に `task.py` と入力
3. 以下のコードを貼り付け

```python
import os
from playwright.sync_api import sync_playwright


def process_account(page, context, id, password, confirmPass, amount):
    # ======================================================
    # ログイン処理
    # ======================================================
    page.goto('https://www.oddspark.com/')
    page.wait_for_timeout(2000)

    page.fill('[name="SSO_ACCOUNTID"]', id)
    page.fill('[name="SSO_PASSWORD"]', password)
    page.click('#btn_login')
    page.wait_for_timeout(2000)

    # 追加認証
    page.fill('[name="INPUT_PIN"]', confirmPass)
    page.click('[name="送信"]')
    page.wait_for_timeout(2000)

    # ======================================================
    # 振込指示処理
    # ======================================================

    # 入金・精算ボタン押下（ポップアップ対応）
    with context.expect_page() as new_page_info:
        page.click('/html/body/div[1]/div[1]/div/ul[2]/li[6]/a')
    popup = new_page_info.value
    popup.wait_for_load_state()

    # 入金するボタン
    popup.click('//*[@id="leftNyukinMenu"]/ul[1]/li/a')

    # 入金額入力
    popup.fill('[name="nyukin"]', str(amount))
    popup.click('//*[@id="confirm"]/li[2]/a')
    popup.wait_for_timeout(2000)

    # 暗証番号入力 → 入金実行
    popup.fill('[name="touhyoPassword"]', confirmPass)
    popup.click('//*[@id="confirm"]/li[2]/a')
    popup.wait_for_timeout(2000)
    popup.close()

    # 精算処理
    with context.expect_page() as new_page_info:
        page.click('/html/body/div[1]/div[1]/div/ul[2]/li[6]/a')
    popup2 = new_page_info.value
    popup2.wait_for_load_state()

    popup2.click('/html/body/div[1]/div[2]/div/div[2]/ul[2]/li/a')
    popup2.wait_for_timeout(2000)

    popup2.fill('[name="touhyoPassword"]', confirmPass)
    popup2.click('//*[@id="confirm"]/li[2]/a')
    popup2.wait_for_timeout(3000)

    # ======================================================
    # ログアウト処理
    # ======================================================
    page.click('text=ログアウト')
    page.wait_for_timeout(2000)


if __name__ == "__main__":
    accounts = [
        {
            'id':       os.getenv('SITE_ID_1'),
            'password': os.getenv('SITE_PASSWORD_1'),
            'pin':      os.getenv('SITE_PIN_1'),
            'amount':   2000,  # アカウント1の入金額
        },
        {
            'id':       os.getenv('SITE_ID_2'),
            'password': os.getenv('SITE_PASSWORD_2'),
            'pin':      os.getenv('SITE_PIN_2'),
            'amount':   2000,  # アカウント2の入金額
        },
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        for i, acc in enumerate(accounts, 1):
            print(f"アカウント {i} の処理開始")
            process_account(page, context, acc['id'], acc['password'], acc['pin'], acc['amount'])
            print(f"アカウント {i} の処理完了")

        browser.close()

    print("全処理完了")
```

4. 画面下部の **「Commit new file」** をクリック

---

### 3-2. `monthly-task.yml` の作成

1. 再度 **「Add file」** → **「Create new file」** をクリック
2. ファイル名に `.github/workflows/monthly-task.yml` と入力
   - `.github/` と入力すると自動でディレクトリが作られます
3. 以下のコードを貼り付け

```yaml
name: OddsPark Monthly Task

on:
  schedule:
    - cron: '0 0 1 * *'  # 毎月1日 9:00 JST
  workflow_dispatch:      # 手動実行ボタン

jobs:
  run-task:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install playwright
          playwright install chromium --with-deps

      - name: Run task
        env:
          SITE_ID_1: ${{ secrets.SITE_ID_1 }}
          SITE_PASSWORD_1: ${{ secrets.SITE_PASSWORD_1 }}
          SITE_PIN_1: ${{ secrets.SITE_PIN_1 }}
          SITE_ID_2: ${{ secrets.SITE_ID_2 }}
          SITE_PASSWORD_2: ${{ secrets.SITE_PASSWORD_2 }}
          SITE_PIN_2: ${{ secrets.SITE_PIN_2 }}
        run: python task.py
```

4. **「Commit new file」** をクリック

---

## 4. Secretsの登録

2アカウント分のログイン情報をGitHubに安全に保存します。

1. リポジトリページの **「Settings」** タブをクリック

2. 左メニューの **「Secrets and variables」** → **「Actions」** をクリック

3. **「New repository secret」** をクリックして以下を1つずつ登録

   | Name | Secret（値） |
   |------|-------------|
   | `SITE_ID_1` | アカウント1のログインID |
   | `SITE_PASSWORD_1` | アカウント1のパスワード |
   | `SITE_PIN_1` | アカウント1の暗証番号 |
   | `SITE_ID_2` | アカウント2のログインID |
   | `SITE_PASSWORD_2` | アカウント2のパスワード |
   | `SITE_PIN_2` | アカウント2の暗証番号 |

   > ℹ️ 登録後はSecretの値は表示されなくなりますが、正しく保存されています。

   > ℹ️ 入金額は `task.py` 内に直接記載されています。変更する場合はファイルを直接編集してください。

---

## 5. 実行スケジュールの設定

`monthly-task.yml` の `cron` 行を変更することで実行日時を調整できます。

### cron書式

```
'分 時 日 月 曜日'
```

GitHub ActionsのcronはUTC（世界標準時）なので、JSTに変換するには **-9時間** します。

### よくある設定例

| 実行したい日時（JST） | cron設定 |
|----------------------|----------|
| 毎月1日 9:00 | `0 0 1 * *` |
| 毎月15日 9:00 | `0 0 15 * *` |
| 毎月末日 12:00 | `0 3 28-31 * *` |
| 毎月5日 18:00 | `0 9 5 * *` |

### 変更方法

1. リポジトリの `.github/workflows/monthly-task.yml` を開く
2. 右上の鉛筆アイコン（Edit）をクリック
3. `cron:` の行を上記表を参考に変更
4. **「Commit changes」** をクリック

---

## 6. 動作確認

本番実行前に手動でテスト実行できます。

1. リポジトリの **「Actions」** タブをクリック

2. 左メニューの **「OddsPark Monthly Task」** をクリック

3. 右側の **「Run workflow」** → **「Run workflow」** をクリック

4. 実行中のジョブが表示されるのでクリックして進捗を確認

5. ✅ 緑チェックになれば成功、❌ 赤バツは失敗（ログで原因確認）

---

## 7. ログの確認方法

1. **「Actions」** タブをクリック
2. 実行済みのワークフローをクリック
3. **「run-task」** をクリック
4. 各ステップの▶をクリックすると詳細ログが見られる

---

## 8. トラブルシューティング

### ❌ ログインに失敗する

- Secretsの値に余分なスペースや改行が入っていないか確認
- OddsSparkのサイト仕様が変わっていないか確認（セレクタが変更されている場合あり）

### ❌ ログアウトに失敗する

- OddsSparkのログアウトボタンのテキストが変わっている可能性があります
- `task.py` 内の `page.click('text=ログアウト')` のテキストを実際のボタン文言に合わせて修正してください

### ❌ playwright install でエラーになる

- `monthly-task.yml` の `playwright install chromium --with-deps` が正しく記載されているか確認

### ❌ スケジュール通りに実行されない

- GitHub ActionsのcronはUTC基準のため、JST変換が正しいか再確認
- GitHubの仕様上、スケジュール実行は数分〜数十分遅延する場合があります

### ❌ ポップアップが開かない

- OddsSparkのページ構造が変わった可能性があります
- `task.py` 内のXPathやセレクタを最新のHTMLに合わせて修正してください

---

## 補足：無料枠について

GitHub Actionsの無料枠（パブリックリポジトリは無制限、プライベートは月2,000分）で十分に運用できます。本スクリプトの実行時間は約2〜3分程度です。
