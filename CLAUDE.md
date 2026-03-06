# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OddsPark（オッズパーク）への毎月の入金・精算処理を自動化するツール。GitHub Actions で定期実行するサーバーレス構成。

## Architecture

The intended production structure (per README and `github_setup.md`):

```
.
├── task.py                              # Main script (Playwright, headless Chromium)
├── .github/workflows/monthly-task.yml  # GitHub Actions cron workflow
└── odds_park.py                         # Legacy Selenium prototype (reference only)
```

`odds_park.py` は Selenium ベースのプロトタイプで本番では使用しない。本番の `task.py` は Playwright を使用し、ポップアップウィンドウを `context.expect_page()` でネイティブに処理する。

## Running Locally

```bash
pip install playwright
playwright install chromium --with-deps

SITE_ID=xxx SITE_PASSWORD=xxx SITE_PIN=xxx SITE_AMOUNT=10000 python task.py
```

## GitHub Actions

Secrets に `SITE_ID`, `SITE_PASSWORD`, `SITE_PIN`, `SITE_AMOUNT` を登録。ワークフローは `schedule`（cron）と `workflow_dispatch`（手動）でトリガー。cron は UTC 基準（JST = UTC+9）。

## Key Implementation Notes

- メイン関数: `io_money_oddspark(id, password, confirmPass, amount)`
- フロー: ログイン → 追加認証（PIN）→ 入金ポップアップ → 精算ポップアップ
- XPath セレクタを多用しているため、OddsPark のサイト変更時はセレクタの更新が必要
- 認証情報を扱うためリポジトリは必ず **Private** にすること
