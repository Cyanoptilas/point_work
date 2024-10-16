# https://www.oddspark.com/
def io_money_oddspark(id, password, confirmPass, amount):
    # 待機時間
    from time import sleep

    # Selenium
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    # オプションの設定
    options = webdriver.ChromeOptions()

    # Chromeプロファイルの指定
    options.add_argument("--user-data-dir=/Users/<ユーザ名>/Library/Application Support/Google/Chrome")

    # Selenium実行後もChromeを開いたままにする
    options.add_experimental_option('detach', False)

    # ポップアップウィンドウの許可設定
    options.add_argument('--disable-popup-blocking')

    # ======================================================
    # オッズパーク ログイン処理
    # ======================================================

    # Chromeブラウザを開く
    driver = webdriver.Chrome()

    # 指定のURLを開く
    url_top = 'https://www.oddspark.com/'
    driver.get(url_top)

    sleep(2)

    # ユーザ名入力
    user_id = id
    login_user_id = driver.find_element(By.NAME, 'SSO_ACCOUNTID')
    login_user_id.send_keys(user_id)

    # ログインパスワード入力
    password = password
    login_user_password = driver.find_element(By.NAME, 'SSO_PASSWORD')
    login_user_password.send_keys(password)

    # ログインボタン押下
    login_btn = driver.find_element(By.ID, 'btn_login')
    login_btn.click()

    sleep(2)

    # ページ遷移後
    # 追加認証 パスワード入力
    additional_password = confirmPass
    additional_password_form = driver.find_element(By.NAME, 'INPUT_PIN')
    additional_password_form.send_keys(additional_password)

    # 確認ボタン押下
    login_btn = driver.find_element(By.NAME, '送信')
    login_btn.click()


    # ======================================================
    # 振込指示処理
    # ======================================================

    # 入金・精算ボタンを押下
    xpath_payment_btn = '/html/body/div[1]/div[1]/div/ul[2]/li[6]/a'
    payment = driver.find_element(By.XPATH, xpath_payment_btn)
    driver.execute_script("arguments[0].click();", payment)

    sleep(2)

    # ウィンドウを切り替える
    handle_array = driver.window_handles
    driver.switch_to.window(handle_array[1])

    # 入金するボタンを押下
    xpath_input_money_btn = '//*[@id="leftNyukinMenu"]/ul[1]/li/a'
    payment = driver.find_element(By.XPATH, xpath_input_money_btn)
    payment.click()

    # 入金額を入力
    payment_amount = amount
    payment_amount_form = driver.find_element(By.NAME, 'nyukin')
    payment_amount_form.send_keys(payment_amount)

    # 次へボタンを押下
    next_btn = '//*[@id="confirm"]/li[2]/a'
    next = driver.find_element(By.XPATH, next_btn)
    next.click()

    sleep(2)

    # ページ遷移後
    # 暗証番号入力
    pin_password = confirmPass
    pin_password_form = driver.find_element(By.NAME, 'touhyoPassword')
    pin_password_form.send_keys(pin_password)

    # 入金ボタンを押下
    xpath_input_money_btn = '//*[@id="confirm"]/li[2]/a'
    payment = driver.find_element(By.XPATH, xpath_input_money_btn)
    payment.click()

    sleep(2)

    driver.close()

    # ウィンドウを切り替える
    handle_array = driver.window_handles
    driver.switch_to.window(handle_array[0])

    # 入金・精算ボタンを押下
    xpath_payment_btn = '/html/body/div[1]/div[1]/div/ul[2]/li[6]/a'
    payment = driver.find_element(By.XPATH, xpath_payment_btn)
    driver.execute_script("arguments[0].click();", payment)

    sleep(2)

    # ウィンドウを切り替える
    handle_array = driver.window_handles
    driver.switch_to.window(handle_array[1])

    # 精算するボタンを押下
    xpath_pull_money_btn = '/html/body/div[1]/div[2]/div/div[2]/ul[2]/li/a'
    pull_money_btn = driver.find_element(By.XPATH, xpath_pull_money_btn)
    pull_money_btn.click()

    sleep(2)

    # ページ遷移後
    # 暗証番号入力
    pin_password = confirmPass
    pin_password_form = driver.find_element(By.NAME, 'touhyoPassword')
    pin_password_form.send_keys(pin_password)

    # 精算ボタンを押下
    xpath_output_money_btn = '//*[@id="confirm"]/li[2]/a'
    output_money_btn = driver.find_element(By.XPATH, xpath_output_money_btn)
    output_money_btn.click()

    sleep(3)
    driver.quit()
