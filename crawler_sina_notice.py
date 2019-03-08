#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/26 0026
# @Author  : justin.郑 3907721@qq.com
# @File    : crawler_sina_news.py
# @Desc    : 采集新浪财经 公司公告数据


import html
import time
from html.parser import HTMLParser
import requests
import re
from app.spider.cons import SINA_HK_STOCK_NOTICE, SINA_US_STOCK_NOTICE
from app.spider.util import replace_tag, str_to_timestamp, replace_tag_html
from lxml import etree


class SinaNotice:
    def __init__(self):
        self.hk_notice_url = SINA_HK_STOCK_NOTICE
        self.us_notice_url = SINA_US_STOCK_NOTICE
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}


    def hk_notice_crawler(self, code, date=None):
        # page = 1
        data = []
        for page in range(1):
            page = page + 1
            time.sleep(3)
            url = self.hk_notice_url % (page, code)
            r = requests.get(url, headers=self.headers)
            r.encoding = 'gb2312'
            html = etree.HTML(r.text)
            # print(html)
            news_title = html.xpath('//ul[@class=\"list01\"]/li/a//text()')
            news_url = html.xpath('//ul[@class=\"list01\"]/li/a/@href')
            news_date = html.xpath('//ul[@class=\"list01\"]/li/span//text()')

            for i in range(len(news_title)):
                print(news_title[i])
                ds = {}
                ds['title'] = news_title[i]
                ds['code'] = code
                ds['url'] = news_url[i]
                ds['publish_date'] = news_date[i]
                ds['timestamp'] = str_to_timestamp(news_date[i])
                ds['content'] = self._get_hk_notice_content(news_url[i])
                ds['site'] = '新浪财经'
                ds['type'] = 'HK'
                if ds['content'] != '':
                    data.append(ds)

        return data

    def us_notice_crawler(self, code, date=None):
        # page = 1
        data = []
        for page in range(3):
            time.sleep(3)
            url = self.us_notice_url % (page+1, code)
            print(url)
            r = requests.get(url, headers=self.headers)
            r.encoding = 'gb2312'
            html = etree.HTML(r.text)
            news_title = html.xpath('//ul[@class=\"xb_list\"][1]/li/a//text()')
            news_url = html.xpath('//ul[@class=\"xb_list\"][1]/li/a/@href')
            news_tmp = html.xpath('//ul[@class=\"xb_list\"][1]/li/span[1]//text()')

            for i in range(len(news_title)):
                print(news_title[i])
                ds = {}
                ds['title'] = news_title[i]
                ds['code'] = code
                ds['url'] = news_url[i]
                ds['publish_date'] = self._get_time(news_tmp[i].split(" | ")[1])
                ds['timestamp'] = str_to_timestamp(self._get_time(news_tmp[i].split(" | ")[1]))
                ds['source'] = news_tmp[i].split(" | ")[0]
                ds['content'] = self._get_content(news_url[i])[1]
                ds['site'] = '新浪财经'
                ds['type'] = 'US'
                if ds['content'] != '':
                    data.append(ds)
                # else:
                #     print(ds['title'])
                #     print(ds['url'])

        return data

    def _get_hk_notice_content(self, url):
        r = requests.get(url, headers=self.headers)
        r.encoding = 'gb2312'
        htmls = etree.HTML(r.text)

        content = htmls.xpath('//*[@class="part02"]')[0]
        content = etree.tostring(content).decode('gb2312')
        content = html.unescape(content)
        content = replace_tag_html(content)
        # print(content)
        # HTMLParser().unescape(content)
        return content



    def _get_content(self, url):
        if url.startswith('https://cj.sina.com.cn') or url.startswith('http://cj.sina.com.cn'):
            try:
                r = requests.get(url, headers=self.headers)
                r.encoding = 'utf-8'
                htmls = etree.HTML(r.text)
                source = htmls.xpath('//*[@class="time-source"]/a//text()')[0]
                content = htmls.xpath('//*[@id="artibody"]')[0]
                content = etree.tostring(content).decode('utf-8')
                content = html.unescape(content)
                content = replace_tag(content)
                return source, content.strip()
            except:
                return '', ''
        else:
            try:
                r = requests.get(url, headers=self.headers)
                r.encoding = 'utf-8'
                htmls = etree.HTML(r.text)
                try:
                    source = htmls.xpath('//*[@class="date-source"]/a/text()')[0]
                except:
                    source = htmls.xpath('//*[@class="date-source"]/span//text()')[1]
                content = htmls.xpath('//*[@class="article"]')[0]
                content = etree.tostring(content).decode('utf-8')
                content = html.unescape(content)
                content = replace_tag(content)
                return source, content.strip()
            except:
                return '', ''


    def _get_date(self, str):
        try:
            dl = re.findall(r"\d{4}-\d{1,2}-\d{1,2}", str)
            return dl[0]
        except Exception:
            return ''

    def _get_time(self, date):
        tmp = date.replace('年', '-')
        tmp = tmp.replace('月', '-')
        tmp = tmp.replace('日', '')
        return '%s:00' % tmp


if __name__ == '__main__':
    SinaNotice().us_notice_crawler('FENG')
    # SinaNotice().get_hk_notice_content('http://stock.finance.sina.com.cn/hkstock/go/CompanyNoticeDetail/code/02008/aid/943967.html')
