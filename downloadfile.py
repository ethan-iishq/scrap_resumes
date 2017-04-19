'''
downloadfile.py
'''
# coding: utf-8
import os
import logging
import urllib.request
import gzip



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
    #'Cookie':'dywez=95841923.1491457692.2.2.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/; _jzqx=1.1491457698.1491457698.1.jzqsr=zhaopin%2Ecom|jzqct=/.-; LastCity=%e5%8c%97%e4%ba%ac; LastCity%5Fid=530; ensurew=1; _jzqa=1.1374015042996734200.1491457698.1492143890.1492475721.9; _jzqc=1; _jzqckmp=1; _jzqb=1.1.10.1492475721.1; urlfrom=121126445; urlfrom2=121126445; adfcid=none; adfcid2=none; adfbid=0; adfbid2=0; __utmt=1; JsOrglogin=2009773235; at=c50e8962d42d4bbab147808b77118bc3; Token=c50e8962d42d4bbab147808b77118bc3; rt=2e571929bb844e2c92f923bd8e48575a; uiioit=2264202C55795C690E374C79516B4564502C5C795B6909374E792A6B3364592C5C795D690C3741795B6B4664512C5A7951695; xychkcontr=47443152%2c0; lastchannelurl=https%3A//passport.zhaopin.com/org/login; JsNewlogin=669924411; cgmark=2; NewPinLoginInfo=; ihrtkn=; RDpUserInfo=; isNewUser=1; NewPinUserInfo=; __utma=269921210.1697237847.1490920066.1492143889.1492475728.10; __utmb=269921210.6.9.1492475744302; __utmc=269921210; __utmz=269921210.1491457692.2.2.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/; getMessageCookie=1; ensure=1; RDsUserInfo=3D692E695671417153775075506A567544775C695B695A714C7129772775546A1C7516771B691F6918711271177752753C6A2A754D7710690C691871027116770C751B6A5F753E772669576950713571217754755D6A537544775C6959695A714271577752752B6A2A754D770438E33283E1FF1D56E1E1185BFC700D060D280B51693F713A71587752752C6A29754D7759695B695D714E7153775A75596A5D75427750692A691A7106714B770A75066A09754B773B693E69567146715E7728753D6A5975447745695B69537157715D7753755A6A52754B772C692E695671467154775A755B6A5075497759695F695D714C7121772775546A7EE59138CC32516927713A7158775975596A5475417758695A695B7143715E772A752D6A597545775B695A695071367129775475596A5F7525772969576950713471247754752A6A277544775F695E695F71447154775C755B6A5D754B772C692B695671347126775D755E6A507544775B695B695E7145715C772D75506A547542775D695A695B71477151775975596A54754B772C692969567147715E773A75206A59754377536923693B714A7157775D755B6A4A7541775B6952694E714571067758755C6A5775437753693F693F714A71547759755A6A5F756; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1491870096,1492080017,1492143890,1492475718; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1492475798; dywea=95841923.181721880832821730.1490920036.1492143889.1492475717.11; dywec=95841923; dyweb=95841923.22.9.1492475816821'
    'Cookie':cookie_str
    }
    req = urllib.request.Request(dlurl, headers=headers)
    #req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')

    response = urllib.request.urlopen(req)
    return response.read()

def save_resume_file(filepath, filename, dlurl, cookie_str=""):
    '''
    把下载后的文件保存到下载目录
    :param dlurl: 真实的下载链接
    :param filepath: 下载目录
    :param filename: 保存的文件名字
    :return: None
    '''
    if not os.path.isdir(filepath):
        os.makedirs(filepath)
    os.chdir(filepath)
    if os.path.exists(filename):
        return None
    dlfile = download_file(dlurl, cookie_str)
    with open(filename, 'wb') as f:
        f.write(dlfile)
        f.close()
    return None

