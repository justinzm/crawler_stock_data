#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/4 0004
# @Author  : justin.郑 3907721@qq.com
# @File    : crawler_stock_index.py
# @Desc    :
import re
import requests
from app.spider.cons import INDEX_URL


class StockIndex:
    def __init__(self):
        self.url = INDEX_URL
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

    def crawler(self):
        r = requests.get(self.url, headers=self.headers)
        r.encoding = 'gb2312'
        con = r.text
        con_list = con.split(';')

        data = {}

        #红筹
        doc = con_list[0]
        doc = re.findall('hq_str_rt_hkHSCCI="(.+?)"', doc)[0]
        doc = doc.split(',')
        data['红筹指数'] = {'code': doc[0], 'open': doc[2], 'offer': doc[6], 'ratio': doc[8]}

        # 国企
        doc = con_list[1]
        doc = re.findall('var hq_str_rt_hkHSCEI="(.+?)"', doc)[0]
        doc = doc.split(',')
        data['国企指数'] = {'code': doc[0], 'open': doc[2], 'offer': doc[6], 'ratio': doc[8]}

        # 恒生
        doc = con_list[2]
        doc = re.findall('var hq_str_rt_hkHSI="(.+?)"', doc)[0]
        doc = doc.split(',')
        data['恒生指数'] = {'code': doc[0], 'open': doc[2], 'offer': doc[6], 'ratio': doc[8]}

        # 道琼斯
        doc = con_list[6]
        doc = re.findall('var hq_str_gb_\$dji="(.+?)"', doc)[0]
        doc = doc.split(',')
        data['道琼斯'] = {'code': 'DJI', 'open': doc[5], 'offer': doc[1], 'ratio': doc[2]}

        # 纳斯达克
        doc = con_list[5]
        doc = re.findall('var hq_str_gb_ixic="(.+?)"', doc)[0]
        doc = doc.split(',')
        data['纳斯达克'] = {'code': 'IXIC', 'open': doc[5], 'offer': doc[1], 'ratio': doc[2]}

        # 标普指数
        doc = con_list[4]
        doc = re.findall('var hq_str_gb_\$inx="(.+?)"', doc)[0]
        doc = doc.split(',')
        data['标普指数'] = {'code': 'INX', 'open': doc[5], 'offer': doc[1], 'ratio': doc[2]}

        # 凤凰卫视
        doc = con_list[3]
        doc = re.findall('var hq_str_rt_hk02008="(.+?)"', doc)[0]
        doc = doc.split(',')
        data['凤凰卫视'] = {'code': '02008', 'close': doc[3], 'open': doc[2], 'offer': doc[6], 'ratio': doc[8], 'high': doc[4],
                        'low': doc[5], 'vol': doc[11], 'turn': doc[12]}

        # 凤凰新媒体
        doc = con_list[7]
        doc = re.findall('var hq_str_gb_feng="(.+?)"', doc)[0]
        doc = doc.split(',')
        data['凤凰新媒体'] = {'code': 'FENG', 'offer': doc[1], 'ratio': doc[2], 'close': '', 'open': doc[5], 'high': '',
                        'low': '', 'vol': '', 'turn': ''}

        # print(data)
        return data


if __name__ == '__main__':
    StockIndex().crawler()

