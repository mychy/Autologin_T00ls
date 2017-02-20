#!/usr/bin/python
#coding:utf-8
# @Author: neo
# @Date:   2016-12-17T22:28:36+08:00
# @Last modified by:   neo
# @Last modified time: 2016-12-18T17:57:59+08:00

import requests
import time,datetime
import logging as log
import multiprocessing, signal

LogLevel = log.INFO
log.basicConfig(level = LogLevel,
    format = '%(asctime)s [%(levelname)s] at %(filename)s,%(lineno)d: %(message)s',
    datefmt = '%Y-%m-%d(%a)%H:%M:%S',
    filename = 'log/log.'+datetime.date.today().strftime('%y%m%d')+'.txt')

Headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
     'Content-Type': 'application/x-www-form-urlencoded',
     'Connection' : 'keep-alive',
     'Cookie':'',
     'Referer':'https://www.t00ls.net/login.html',
     'Content-Type':'application/x-www-form-urlencoded',
     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

LoginPage = 'https://www.t00ls.net/login.html'
NoticePage = 'https://www.t00ls.net/notice.php'
LoginParam = {
   'username'   : '',   #login id
   'password'   : '',   #md5(password)
   'questionid' : 1,    #questionid. e.g. 1
   'answer'     : '',   #question answer
   'formhash'   : '',
   'loginsubmit': '登录'
}

def get_login_page():
    response = requests.get(url = LoginPage, headers = Headers)
    text = response.text
    formhash = text[text.find('formhash" value="')+17:text.find('formhash" value="')+25]
    log.debug('formash is : ' + formhash)
    LoginParam['formhash'] = formhash

def post_login():
    log.info("Loging...")
    response = requests.post(url = LoginPage, headers = Headers, data = LoginParam, allow_redirects=False)
    Headers['Cookie'] = response.headers['Set-Cookie']
    log.debug('Cookie in headers : ' + Headers['Cookie'])

def keep_online():
    response = requests.get(url = NoticePage, headers = Headers, allow_redirects=False)
    failure_str = '对不起，您还未登录，无法进行此操作。'
    if response.text.encode('utf-8').find(failure_str) == -1:
        log.info('Check session... Valid ? : [ YES ]')
        time.sleep(60)
        keep_online()
    else:
        log.info('Check session... Valid ? : [ NO ]')
        t00lsKeepOnline()

def t00lsKeepOnline():
    log.info('Start...')
    get_login_page()
    post_login()
    keep_online()

def main():
    log.info('Hello Python')
    thread = multiprocessing.Process(target=t00lsKeepOnline)
    while(1):
        if thread.is_alive() is False :
            log.warning("Warning, thread is terminated !!! ")
            thread.start()
            time.sleep(120)
        else:
            time.sleep(1800)


if __name__ == '__main__':
    main()
