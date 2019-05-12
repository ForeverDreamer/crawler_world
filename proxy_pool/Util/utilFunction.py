# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     utilFunction.py
   Description :  tool function
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: 添加robustCrawl、verifyProxy、getHtmlTree
-------------------------------------------------
"""
import requests
import time
from bs4 import BeautifulSoup
import re

from Util.LogHandler import LogHandler
from Util.WebRequest import WebRequest


# logger = LogHandler(__name__, stream=False)

def tcpConnect(proxy):
    """
    TCP 三次握手
    :param proxy:
    :return:
    """
    from socket import socket, AF_INET, SOCK_STREAM
    s = socket(AF_INET, SOCK_STREAM)
    ip, port = proxy.split(':')
    result = s.connect_ex((ip, int(port)))
    return True if result == 0 else False


# noinspection PyPep8Naming
def robustCrawl(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            pass
            # logger.info(u"sorry, 抓取出错。错误原因:")
            # logger.info(e)

    return decorate


# noinspection PyPep8Naming
def verifyProxyFormat(proxy):
    """
    检查代理格式
    :param proxy:
    :return:
    """
    import re
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}:https?"
    _proxy = re.findall(verify_regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


# noinspection PyPep8Naming
def getHtmlTree(url, **kwargs):
    """
    获取html树
    :param url:
    :param kwargs:
    :return:
    """

    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              }
    # TODO 取代理服务器用代理服务器访问
    wr = WebRequest()

    # delay 2s for per request
    time.sleep(2)

    html = wr.get(url=url, header=header).text
    # return etree.HTML(html)
    return BeautifulSoup(html, features='lxml')


def extract_ip(ip_info):
    ip = re.findall(r'\d+\.\d+\.\d+\.\d+', ip_info)
    if len(ip) > 0:
        ip = ip[0]

    port = re.findall(r'(\d{4,5})<', ip_info)
    if len(port) > 0:
        port = port[0]

    protocol = re.findall(r'https?|HTTPS?', ip_info)
    if len(protocol) > 0:
        protocol = protocol[0].lower()
    else:
        protocol = 'http'

    return "{}:{}:{}".format(ip, port, protocol)


# noinspection PyPep8Naming
# def validUsefulProxy(proxy):
#     url = "http://ip.tool.chinaz.com/"  # 查自己的ip
#     # url = "http://www.ip138.com/"  # 查自己的ip
#     ip, port, prot = proxy.split(':')
#
#     try:
#         proxies = {
#             'protocol': '{}://{}:{}'.format(prot, ip, port)
#         }
#         r = requests.get(url, proxies=proxies, timeout=10, verify=False)
#         soup = BeautifulSoup(r.text, 'lxml')
#
#         parent_node = soup.find(class_="IpMRig-tit")
#
#         if ip == soup.find(class_="fz24").get_text():
#             for i in parent_node.find_all('dd'):
#                 print(i.get_text())
#
#             return True
#     except Exception as e:
#         print(e)
#
#     return False

def validUsefulProxy(proxy):
    url = "http://crawleruniverse.com:8000/ct/ri"  # 查自己的ip
    ip, port, prot = proxy.split(':')

    try:
        proxies = {
            prot: '{}://{}:{}'.format(prot, ip, port)
        }
        r = requests.get(url, proxies=proxies, timeout=10, verify=False)
        soup = BeautifulSoup(r.text, 'lxml')

        http_x_forwarded_for = re.findall(r'\d+.\d+.\d+.\d+', str(soup.find("h4")))
        remote_addr = re.findall(r'\d+.\d+.\d+.\d+', str(soup.find("h5")))[0]
        if ip == remote_addr:
            print('http_x_forwarded_for: {}, remote_addr: {}, ip: {}, pass: {}'.format(http_x_forwarded_for,
                                                                                       remote_addr,
                                                                                       ip,
                                                                                       ip == remote_addr))
            return True
    except Exception as e:
        print(e)

    return False
