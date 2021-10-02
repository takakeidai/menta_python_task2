


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


    df = pd.DataFrame()
    company_name = []
    title = []
    first_year_fee_list = []

    for _ in range(1,14):
        name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        title_list = driver.find_elements_by_css_selector('.cassetteRecruit__copy')
        table_list = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition")

        for name in name_list:
            target = ' '
            idx = name.text.find(target) 
            company_name.append(name.text[:idx])
        
        for job_title in title_list:
            title.append(job_title.text)
        
        for table in table_list:
            first_year_fee = find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "初年度年収")
            first_year_fee_list.append(first_year_fee)

        if _ != 13:
            next_page = driver.find_element_by_css_selector(".iconFont--arrowLeft")
            next_page_link = next_page.get_attribute('href')
            driver.get(next_page_link)
        else:
            pass

    for i in range(0, len(company_name)):
        if first_year_fee_list[i] == None:
            df = df.append(
                {'会社名':company_name[i],
                'タイトル':title[i],
                "初年度年収":'None'}, 
                ignore_index=True)
        else:
            df = df.append(
                {'会社名':company_name[i],
                'タイトル':title[i],
                "初年度年収":first_year_fee_list[i]}, 
                ignore_index=True)

    df.to_csv("企業情報一覧.csv", encoding = "utf-8_sig")



# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()


# cassetteRecruit__content






