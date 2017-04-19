import subprocess
import sqlite3
import win32crypt

SOUR_COOKIE_FILENAME = r'C:\Users\ethan\AppData\Local\Google\Chrome\User Data\Default\Cookies'
DIST_COOKIE_FILENAME = '.\python-chrome-cookies'


def get_chrome_cookies(url):
    subprocess.call(['copy', SOUR_COOKIE_FILENAME, DIST_COOKIE_FILENAME], shell=True)
    conn = sqlite3.connect(".\python-chrome-cookies")
    ret_dict = {}
    for row in conn.execute("SELECT host_key, name, path, value, encrypted_value FROM cookies"):
        # if row[0] not in url:
        if row[0] != url:
            continue
        #print(row)
        ret = win32crypt.CryptUnprotectData(row[4], None, None, None, 0)
        ret_dict[row[1]] = ret[1].decode()
    conn.close()
    subprocess.call(['del', '.\python-chrome-cookies'], shell=True)
    return ret_dict


def get_chrome_cookies_list(url):
    subprocess.call(['copy', SOUR_COOKIE_FILENAME, DIST_COOKIE_FILENAME], shell=True)
    conn = sqlite3.connect(".\python-chrome-cookies")
    ret_list = []
    for row in conn.execute("SELECT host_key, name, path, value, encrypted_value FROM cookies"):
        # if row[0] not in url:
        if row[0] != url:
            continue
        #print(row)
        ret = win32crypt.CryptUnprotectData(row[4], None, None, None, 0)
        cookie_dict = {"name": row[1], "value": ret[1].decode(), "path": row[2], "domain": row[0]}
        ret_list.append(cookie_dict)
    conn.close()
    subprocess.call(['del', '.\python-chrome-cookies'], shell=True)
    return ret_list


def save_in_file(filename, content):
    out = open(filename, "w", encoding="utf-8")
    out.write(content)
    out.flush()
    out.close()


if __name__ == '__main__' :
    print(get_chrome_cookies(".baidu.com"))

