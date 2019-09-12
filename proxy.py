import requests
from bs4 import BeautifulSoup
import pandas as pd


def getProxyPool():
    """Generate a list of https proxies from https://www.us-proxy.org/"""
    # proxy handling
    page = requests.get('https://www.us-proxy.org/')
    soup = BeautifulSoup(page.text, 'lxml')
    proxyTable = pd.read_html(str(soup.find_all('table', {'id': 'proxylisttable'})))[0]
    proxyPool = []
    for row in (proxyTable[
        (proxyTable['Https']=='yes') & ((proxyTable['Anonymity']=='elite proxy') | (proxyTable['Anonymity']=='anonymous'))
        ].iterrows()):
        proxyPool.append(f"https://{row[1]['IP Address']}:{int(row[1]['Port'])}")
    return proxyPool
