# -*- coding: utf-8 -*-

'''
downloadfile.py
'''

import os
import logging
import urllib.request


def download_file(dlurl, cookie_str):
    '''
    从真实的下载链接下载文件
    :param dlurl: 真实的下载链接
    :return: 下载后的文件
    '''
    headers = {
    'Host': 'rd.zhaopin.com',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cookie':cookie_str
    }
    req = urllib.request.Request(dlurl, headers=headers)
    try:
        response = urllib.request.urlopen(req)
        file_content = response.read()
    except BaseException as e:
        logging.INFO("Download resume failed!")
        raise e
    return file_content

def save_resume_file(filepath, filename, dlurl, cookie_str=""):
    '''
    把下载后的文件保存到下载目录
    :param dlurl: 真实的下载链接
    :param filepath: 下载目录
    :param filename: 保存的文件名字
    :return: 0 success -1 failed
    '''
    if not os.path.isdir(filepath):
        os.makedirs(filepath)
    os.chdir(filepath)
    if os.path.exists(filename):
        return None
    try:
        dlfile = download_file(dlurl, cookie_str)
    except BaseException as e:
        print("下载 %s 简历失败" % filename)
        return -1
    else:
        with open(filename, 'wb') as f:
            f.write(dlfile)
            f.close()
    return 0

