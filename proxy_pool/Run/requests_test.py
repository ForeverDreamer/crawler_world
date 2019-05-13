import requests
from bs4 import BeautifulSoup
import re

url = "http://crawleruniverse.com:8000/ct/ri"  # 查自己的ip
ip, port, prot = '189.196.168.78:30880:http'.split(':')

try:
    proxies = {
        prot: '{}://{}:{}'.format(prot, ip, port)
    }
    r = requests.get(url, proxies=None, timeout=10, verify=False)
    soup = BeautifulSoup(r.text, 'lxml')

    http_x_forwarded_for = re.findall(r'\d+.\d+.\d+.\d+', str(soup.find("h4")))
    remote_addr = re.findall(r'\d+.\d+.\d+.\d+', str(soup.find("h5")))[0]
    print('http_x_forwarded_for: {}, remote_addr: {}, ip: {}, equal: {}'.format(http_x_forwarded_for,
                                                                                remote_addr,
                                                                                ip,
                                                                                ip == remote_addr))

except Exception as e:
    print(e)
