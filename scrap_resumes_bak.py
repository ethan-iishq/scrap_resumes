from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
from scrap_util import get_chrome_cookies_list
from scrap_util import save_in_file
from downloadfile import save_resume_file


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

      function f() {scrap_resumes_bak.py
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


# 获取Google的cookie，并设置到driver
def set_login_cookies_zhiliansize():
    new_cookie_list = get_chrome_cookies_list(DOMAIN_NAME)
    driver = webdriver.PhantomJS(executable_path=r'D:\Programs\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    driver.delete_all_cookies()
    for cookie in new_cookie_list:
        driver.add_cookie(cookie)
    cookie_str = get_cookie_str(driver.get_cookies())
    return driver, cookie_str


def get_joblist(driver):
    try:
        driver.get(URL2)
    except:
        print("异常，请检查网络等...")
        exit(-1)
    try:
        #print(driver.get_cookies())
        ajob_td_list = driver.find_elements_by_class_name("bolditem")
        if len(ajob_td_list) == 0:
            print("cookie失效，请在chrome浏览器登陆后再运行！")
            exit(-2)
    except:
        print("find_elements_by_class_name bolditem got an exception")
        return None
    return ajob_td_list


def get_cookie_str(cookie_list):
    cookie_str = ""
    for cookie_item in cookie_list:
        cookie_str += cookie_item["name"]+"="+cookie_item["value"] + "; "
    cookie_str = cookie_str[0:-2]
    return cookie_str


def download_resumes(driver,cookie_str, filepath):
    main_win_handle = driver.current_window_handle
    # print("main window title : %s, main window  url : %s" % (driver.title, driver.current_url))
    a_link_list = driver.find_elements_by_css_selector("a.link")
    print(a_link_list)
    for a_link in a_link_list:
        print("filename: %s .doc" % a_link.text)
        filename = a_link.text + ".doc"
        a_link.click()

        win_handles = driver.window_handles
        print("personlist handle : %s" % main_win_handle)

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
                # save_in_file("after_click.html", driver.page_source)
                next_btn = driver.find_element_by_class_name("popupConfirmBtn")
                next_btn.click()

                download_link = driver.find_element_by_css_selector(".popupConfirmBtn").find_element_by_tag_name("a")
                download_url = download_link.get_attribute("href")

                # print("download url:%s \n cookie_str : %s" % download_url, driver.get_cookies())
                # save_resume_file(download_url, cookie_str)
                # print(cookie_str)
                # print(download_link.get_attribute("href"))
                save_resume_file(filepath, filename, download_url, cookie_str)
                driver.close()
                driver.switch_to.window(main_win_handle)
                break



def get_job_resumes(driver, ajob_td_list):
    if ajob_td_list == None:
        print("暂时没有发布职位！")
    # print("first title : %s, first url : %s" % (driver.title, driver.current_url))

    for ajob_td in ajob_td_list:
        print("职位名称为：%s" % ajob_td.text)
        filepath = "G:\\scrap_files\\" + ajob_td.text
        #进入该职位的页面
        try:
            ajob_td.find_element_by_tag_name("a").click()
            download_resumes(driver, cookie_str, filepath)
            # print("after download_resumes title : %s, after download_resumes url : %s" % (driver.title, driver.current_url))
            driver.back()
            # print("after back title : %s, after back url : %s" % (driver.title, driver.current_url))
            break
        except:
            print("get_job_resumes got a exception")
            break


if __name__ == '__main__' :
    driver, cookie_str = set_login_cookies_zhiliansize()
    joblist = get_joblist(driver)
    # print(joblist)
    get_job_resumes(driver, joblist)
    driver.quit()
