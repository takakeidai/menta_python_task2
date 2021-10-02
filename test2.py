


import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd



def find_table_target_word(th_elms, td_elms, target:str):
    # tableのthからtargetの文字列を探し一致する行のtdを返す
    for th_elm,td_elm in zip(th_elms,td_elms):
        if th_elm.text == target:
            return td_elm.text


def set_driver(driver_path, headless_flg):

    if "chrome" in driver_path:
          options = ChromeOptions()
    else:
      options = Options()

    if headless_flg == True:
        options.add_argument('--headless')

    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')        

    driver_path = ChromeDriverManager().install()
    return Chrome(executable_path=driver_path, options=options)



def main():
    search_keyword = "高収入"
    driver_path = ChromeDriverManager().install()
    driver = set_driver(driver_path, False)
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(5)
    driver.execute_script('document.querySelector(".karte-close").click()')
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    driver.find_element_by_class_name("topSearch__button").click()


    company_name = []    
    total_company_list = []

    # 2ページ分：これは148になる。
    i = 0
    while i < 2:
        # driver.find_element_by_css_selector(".iconFont--arrowLeft").click()
        name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        for name in name_list:
            target = ' '
            idx = name.text.find(target)
            company_name.append(name.text[:idx])
        total_company_list += company_name
        # driver.find_element_by_css_selector(".iconFont--arrowLeft").click()
        i += 1
    print(len(total_company_list))

    # 1ページ目：50
    i = 0
    while i < 1:
        name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        for name in name_list:
            target = ' '
            idx = name.text.find(target)
            company_name.append(name.text[:idx])
        total_company_list += company_name
        # driver.find_element_by_css_selector(".iconFont--arrowLeft").click()
        i += 1
    print(len(total_company_list))


    # 2ページ目：50
    i = 0
    while i < 1:
        # driver.find_element_by_css_selector(".iconFont--arrowLeft").click()
        name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        for name in name_list:
            target = ' '
            idx = name.text.find(target)
            company_name.append(name.text[:idx])
        total_company_list += company_name
        # driver.find_element_by_css_selector(".iconFont--arrowLeft").click()
        i += 1
    print(len(total_company_list))

"""
高収入で調べたとき、ページ1とページ2の2ページ分の会社名のリストを用意した時、会社名の数(そのリストの要素数)が148になる。
ということは、各ページで74社の名前が記載されていないとおかしいにもかかわらず、1ページ目と2ページ目を別々に取得するとそれぞれ同様に50社しか会社名が抽出されない。
その2つを総計しても148にはならない。
内部で何が起きているのか。
"""






# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()




