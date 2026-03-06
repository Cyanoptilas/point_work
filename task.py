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
