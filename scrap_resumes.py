# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
from scrap_util import get_chrome_cookies_list
from downloadfile import save_resume_file
import logging

logging.basicConfig(level=logging.ERROR,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='my_scrap_resumes.log',
                filemode='w')

DOMAIN_NAME = '.zhaopin.com'
URL = r'http://www.zhaopin.com'
URL1 = r"http://rd2.zhaopin.com/s/homepage.asp"
URL2 = r'http://rd2.zhaopin.com/s/resuadmi/vacancyList.asp'


# 网页截图
def capture(browser, save_fn="files\capture.png"):
    browser.set_window_size(1200, 900)
    browser.execute_script("""
        (function () {
          var y = 0;
          var step = 100;
          window.scroll(0, 0);

          function f() {
            if (y < document.body.scrollHeight) {
              y += step;
              window.scroll(0, y);
              setTimeout(f, 50);
            } else {
              window.scroll(0, 0);
              document.title += "scroll-done";
            }
          }

          setTimeout(f, 1000);
        })();
        """)
    for i in range(30):
        if "scroll-done" in browser.title:
            break
        time.sleep(1)
    browser.save_screenshot(save_fn)


def get_cookie_str(cookie_list):
    """
    :param cookie_list: cookie list , each cookie is a dict object  contain name, value, path, domain attrs.
    :return: cookie string such as name1=value1; name2=value2
    """
    """
    :param cookie_list:
    :return:
    """
    cookie_str = ""
    for cookie_item in cookie_list:
        cookie_str += cookie_item["name"]+"="+cookie_item["value"] + "; "
    if len(cookie_str) >= 2:
        cookie_str = cookie_str[0:-2]
    return cookie_str


# 获取Google的cookie，并设置到driver
def set_login_cookies_zhiliansize():
    cookie_list = get_chrome_cookies_list(DOMAIN_NAME)
    driver = webdriver.PhantomJS(executable_path=r'D:\Programs\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    driver.delete_all_cookies()
    for cookie in cookie_list:
        driver.add_cookie(cookie)
    cookie_str = get_cookie_str(cookie_list)
    return driver, cookie_str


def get_joblist(driver):
    try:
        driver.get(URL2)
    except BaseException as e:
        logging.error(u"异常，请检查网络等...")
        exit(-1)
    try:
        ajob_td_list = driver.find_elements_by_class_name("bolditem")
        if len(ajob_td_list) == 0:
            logging.error(u"cookie失效，请在chrome浏览器登陆后再运行！")
            exit(-2)
    except BaseException as e:
        logging.info(u"找不到职位列表")
        exit(-3)
    else:
        job_title_dict = dict()
        for ajob_td in ajob_td_list:
            if ajob_td.text not in job_title_dict:
                job_title_dict[ajob_td.text] = 0
    logging.debug(u"职位列表为：%s" % job_title_dict.keys())
    return job_title_dict


def download_resumes(driver, filepath):
    main_win_handle = driver.current_window_handle
    success_num = fail_num = 0
    # print("main window title : %s, main window  url : %s" % (driver.title, driver.current_url))
    a_link_list = driver.find_elements_by_css_selector("a.link")
    #print(a_link_list)
    for a_link in a_link_list:
        logging.debug("filename: %s .doc" % a_link.text)
        filename = a_link.text + ".doc"
        a_link.click()

        win_handles = driver.window_handles
        logging.debug("personlist handle : %s" % main_win_handle)

        for handle in win_handles:
            if handle != main_win_handle:
                print("choosed handles %s" % handle)
                driver.switch_to.window(handle)
                # print("current title : %s, current url : %s" % (driver.title, driver.current_url))

                div_prepare_down = driver.find_element_by_css_selector(".resume-preview-button.previewLayer1.smpevent")
                #capture(driver)

                driver.execute_script("""
                $('.resume-preview-button.previewLayer1.smpevent').click();

                """)
                time.sleep(1)

                next_btn = driver.find_element_by_class_name("popupConfirmBtn")
                next_btn.click()

                download_link = driver.find_element_by_css_selector(".popupConfirmBtn").find_element_by_tag_name("a")
                download_url = download_link.get_attribute("href")

                logging.debug("file downloding with params ==> %s: %s " % (filename, download_url))
                ret = save_resume_file(filepath, filename, download_url, cookie_str)
                if ret < 0:
                    fail_num += 1
                else:
                    success_num += 1
                driver.close()
                driver.switch_to.window(main_win_handle)
                break
    return success_num, fail_num


def will_continue_scrap(jobtitle_dict):
    for k in jobtitle_dict:
        if jobtitle_dict[k] == 0:
            return True
        else:
            continue
    return False


def get_job_resumes(driver, jobtitle_dict):
    """
    获取各个职位下的简历
    :param driver:
    :param jobtitle_dict: 职位的字典，key为职位名，value表示该职位是否已下载过
    :return: 无
    """
    jobtitle_down_fail_dict = dict()
    jobtitle_down_success_dict = dict()
    print(jobtitle_dict)
    while will_continue_scrap(jobtitle_dict):
        tdtag_job_list = driver.find_elements_by_class_name("bolditem")
        for tdtag_job in tdtag_job_list:
            if jobtitle_dict[tdtag_job.text] != 0:
                continue
            cur_jobtitle = tdtag_job.text
            jobtitle_down_success_dict[cur_jobtitle] = jobtitle_down_fail_dict[cur_jobtitle] = 0
            print(u"职位名称为：%s" % cur_jobtitle)
            logging.info(u"职位名称为：%s" % cur_jobtitle)
            jobtitle_dict[cur_jobtitle] = 1
            filepath = "G:\\scrap_files\\" + cur_jobtitle
            #进入该职位的页面
            try:
                tdtag_job.find_element_by_tag_name("a").click()
                try:
                    success_num, faile_num = download_resumes(driver, filepath)
                except BaseException as e:
                    print(u"[%s]职位简历的下载出现异常: %s" % (cur_jobtitle, repr(e)))
                    logging.error(u"[%s]职位简历的下载出现异常" % cur_jobtitle)
                    driver.refresh()
                    break
                else:
                    jobtitle_down_success_dict[cur_jobtitle] = success_num
                    jobtitle_down_fail_dict[cur_jobtitle] = faile_num
                logging.debug("after download_resumes title : %s, after download_resumes url : %s" % (driver.title, driver.current_url))
                driver.back()
                logging.debug("after back title : %s, after back url : %s" % (driver.title, driver.current_url))
                break
            except:
                print("get_job_resumes got a exception")
                break


if __name__ == '__main__' :
    driver, cookie_str = set_login_cookies_zhiliansize()
    job_title_dict = get_joblist(driver)
    # print(joblist)
    get_job_resumes(driver, job_title_dict)
    driver.quit()
