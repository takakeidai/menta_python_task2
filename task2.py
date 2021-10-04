
import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


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



def find_target_tC_body(th_elms, tb_elms, target_1:str, target_2:str):
    for th_elm, tb_elm in zip(th_elms, tb_elms):
        if th_elm.text == target_1 or th_elm.text == target_2:
            return tb_elm.text



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

    while True:
        recruit_contents = driver.find_elements_by_css_selector('.cassetteRecruit')
        for recruit_content in recruit_contents:

            name_and_others = recruit_content.find_element_by_css_selector('.cassetteRecruit__name')
            target = ' '
            idx = name_and_others.text.find(target)
            company_name = name_and_others.text[:idx]
            
            title = recruit_content.find_element_by_css_selector('.cassetteRecruit__copy')
            job_title = title.text

            table_content = recruit_content.find_element_by_css_selector('.tableCondition')
            initial_pay = find_target_tC_body(table_content.find_elements_by_css_selector(
                '.tableCondition__head'),table_content.find_elements_by_css_selector('.tableCondition__body'), '初年度年収', '給与')

            if initial_pay == None:
                df = df.append(
                    {'会社名':company_name,
                    'タイトル':job_title,
                    "初年度年収/給与":'None'}, 
                    ignore_index=True)
            else:
                df = df.append(
                    {'会社名':company_name,
                    'タイトル':job_title,
                    "初年度年収/給与":initial_pay}, 
                    ignore_index=True)        

        try:
            next_page = driver.find_element_by_css_selector(".iconFont--arrowLeft")
            next_page_link = next_page.get_attribute('href')
            driver.get(next_page_link)            
        except:
            print('最終ページです')
            break          
    
    df.to_csv("全企業情報一覧_task2.csv", encoding = "utf-8_sig")



    




# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()

















