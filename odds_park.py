import os
from playwright.sync_api import sync_playwright

def io_money_oddspark(id, password, confirmPass, amount):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # ======================================================
        # オッズパーク ログイン処理
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

        browser.close()
        print("処理完了")

if __name__ == "__main__":
    io_money_oddspark(
        id=os.getenv("SITE_ID"),
        password=os.getenv("SITE_PASSWORD"),
        confirmPass=os.getenv("SITE_PIN"),
        amount=os.getenv("SITE_AMOUNT")
    )