# 测试脚本，调用chromedriver，下载简历，并存储到数据库

from selenium import webdriver
from scrap_util import get_chrome_cookies_list
from selenium.webdriver.support.ui import WebDriverWait
import pymysql
import time

DOMAIN_NAME = '.zhaopin.com'
URL = r"https://passport.zhaopin.com/org/login"
URL2 = r'http://rd2.zhaopin.com/s/resuadmi/vacancyList.asp'
CHROME_EDRIVER_PATH = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
INSERT_SQL = "insert into resume_info(filename, jobname, downloadurl)  values('%s', '%s', '%s');"


def get_resume_links():
    #点击标签页显示待沟通简历列表
    browser.find_element_by_css_selector("span#submitBack").click()
    time.sleep(2)
    WebDriverWait(browser, 5).until(lambda the_broswer:the_broswer.find_elements_by_class_name("link").is_displayed())
    # 获取该职位下的简历列表
    resume_as = browser.find_elements_by_class_name("link")
    for resume_a in resume_as:
        print(resume_a.text)
    print()

    for name_link in resume_as:

        filename = name_link.text #简历所属者的名字
        # 打开标签页显示一个应聘者的详情页
        name_link.click()

        main_handle = browser.current_window_handle
        for handle in browser.window_handles:
            if handle != main_handle:
                browser.switch_to.window(handle)
                pre_save_btn_span = browser.find_element_by_css_selector("span.resume-preview-button-span.preview-icon1")
                pre_save_btn_span.click()

                WebDriverWait(browser, 20).until(lambda the_broswer:the_broswer.find_element_by_css_selector("span.popupConfirmBtn").is_displayed())
                next_step_btn_span = browser.find_element_by_css_selector("span.popupConfirmBtn")
                next_step_btn_span.click()
                WebDriverWait(browser, 10).until(lambda the_broswer:the_broswer.find_element_by_css_selector("span.popupConfirmBtn").is_displayed())
                save_btn_span = browser.find_element_by_css_selector("span.popupConfirmBtn")
                download_url = save_btn_span.find_element_by_tag_name("a").get_attribute("href")
                values = (filename, job_name, download_url)
                try:
                    print(INSERT_SQL % values)
                    # cursor.execute(INSERT_SQL % values)
                    conn.commit()
                except BaseException as e:
                    print("insert failed")
                    conn.rollback()

                browser.close()
                break
            else:
                continue

        browser.switch_to.window(main_handle)
        break

def judge_scrap_continue(job_access_dict):
    can_continue = False
    for (k,v) in job_access_dict.items():
        if v == 0:
            can_continue = True
            break
        else:
            continue
    return can_continue

if __name__ == '__main__' :

    browser = webdriver.Chrome(executable_path=CHROME_EDRIVER_PATH)
    browser.get(URL)
    print(browser.get_cookies())
    # time.sleep(5)

    # 获取chrome存储的cookie，设置cookie
    cookie_list = get_chrome_cookies_list(DOMAIN_NAME)
    # cookie_dict = get_chrome_cookies(DOMAIN_NAME)
    browser.delete_all_cookies()

    print(browser.get_cookies())
    for cookie in cookie_list:
        browser.add_cookie(cookie)

    # # 创建数据库连接，
    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='ethan123',
        db='resumes',
        charset='utf8')

    # 获得游标
    cursor = conn.cursor()

    # 访问智联网职位列表
    browser.get(URL2)


    # 获取职位列表
    job_tds = browser.find_elements_by_class_name("bolditem")
    if len(job_tds) == 0:
        print("请登录")
        time.sleep(15)
        browser.get(URL2)
        job_tds = browser.find_elements_by_class_name("bolditem")
        if len(job_tds) == 0:
            print("请先完成登录，再试！")
            exit(1)

    job_access_dict = dict()
    for job_td in job_tds:
        job_access_dict[job_td.text] = 0

    # 打印职位列表
    for job_name in job_access_dict:
        print(job_name)
    print()
    print(job_access_dict)

    while judge_scrap_continue(job_access_dict):
        job_tds = browser.find_elements_by_class_name("bolditem")
        for job_td in job_tds:
            job_name = job_td.text
            if job_access_dict[job_name] != 0:
                continue
            else:
                job_access_dict[job_name] = 1
                job_link = job_td.find_element_by_tag_name("a")
                job_link.click()
                get_resume_links()
                browser.back()
                break
    browser.quit()


