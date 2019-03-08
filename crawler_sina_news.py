#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/26 0026
# @Author  : justin.郑 3907721@qq.com
# @File    : crawler_sina_news.py
# @Desc    : 采集新浪财经新闻数据
# 智通财经网 中新经纬 投资界 环球网 北京商报 澎湃新闻 新华网 TechWeb 虎嗅网 新浪港股 21世纪经济报道 Bianews
# 北京青年报 界面 中国新闻网 第一财经 企业观察报 格隆汇 界面新闻 中证网 新浪科技 智通财经 新京报 中国基金报
# 香港财华社集团 东方财富网 证券日报 中关村在线 新浪财经
import html
import time

import requests
import re
from app.spider.cons import SINA_STOCK_NEWS, SINA_HK_STOCK_NEWS, SINA_US_STOCK_NEWS
from app.spider.util import replace_tag, str_to_timestamp
from lxml import etree


class SinaNews:
    def __init__(self):
        self.news_url = SINA_STOCK_NEWS
        self.hk_news_url = SINA_HK_STOCK_NEWS
        self.us_news_url = SINA_US_STOCK_NEWS
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

    def news_crawler(self, code, date=None):
        """
        采集 新浪财经 国内股票新闻数据
        :param code:
        :param date:
        :return:
        """
        page = 1
        data = []

        url = self.news_url % (code, page)
        # print(url)
        r = requests.get(url, headers=self.headers)
        r.encoding = 'gb2312'
        html = etree.HTML(r.text)
        news_href = html.xpath('//div[@class=\"datelist\"]/ul/a/@href')
        news_list = html.xpath('//div[@class=\"datelist\"]/ul/a/text()')

        for i in range(len(news_list)):
            ds = {}
            ds['title'] = news_list[i]
            ds['code'] = code
            ds['url'] = news_href[i]
            ds['publish_date'] = self._get_date(news_href[i])
            ds['timestamp'] = str_to_timestamp(self._get_date(news_href[i]))
            ds['source'] = self._get_content(news_href[i])[0]
            ds['content'] = self._get_content(news_href[i])[1]
            ds['site'] = '新浪财经'
            ds['type'] = 'CN'
            if ds['content'] != '':
                data.append(ds)
        return data

    def hk_news_crawler(self, code, date=None):
        # page = 1
        data = []
        for page in range(2):
            time.sleep(3)
            url = self.hk_news_url % (page, code)
            r = requests.get(url, headers=self.headers)
            r.encoding = 'gb2312'
            html = etree.HTML(r.text)
            news_title = html.xpath('//ul[@id=\"js_ggzx\"]/li/a//text()')
            news_url = html.xpath('//ul[@id=\"js_ggzx\"]/li/a/@href')
            news_date = html.xpath('//ul[@id=\"js_ggzx\"]/li/span//text()')
            for i in range(len(news_title)):
                ds = {}
                ds['title'] = news_title[i]
                ds['code'] = code
                ds['url'] = news_url[i]
                ds['publish_date'] = news_date[i]
                ds['timestamp'] = str_to_timestamp(news_date[i])
                ds['source'] = self._get_content(news_url[i])[0]
                ds['content'] = self._get_content(news_url[i])[1]
                ds['site'] = '新浪财经'
                ds['type'] = 'HK'
                if ds['content'] != '':
                    data.append(ds)
        return data

    def us_news_crawler(self, code, date=None):
        # page = 1
        data = []
        for page in range(3):
            time.sleep(3)
            url = self.us_news_url % (page+1, code)
            r = requests.get(url, headers=self.headers)
            r.encoding = 'gb2312'
            html = etree.HTML(r.text)
            news_title = html.xpath('//ul[@class=\"xb_list\"][2]/li/a//text()')
            news_url = html.xpath('//ul[@class=\"xb_list\"][2]/li/a/@href')
            news_tmp = html.xpath('//ul[@class=\"xb_list\"][2]/li/span//text()')
            for i in range(len(news_title)):
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
    SinaNew().us_news_crawler('FENG')
