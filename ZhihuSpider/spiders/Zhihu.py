# -*- coding: utf-8 -*-
# coding: utf-8
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from ZhihuSpider.items import ZhihuspiderItem
import json
import logging


class ZhihuSpider(CrawlSpider):
    name = "Zhihu"
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/people/zhang-jia-wei/about']
    host = 'http://www.zhihu.com'

    def __init__(self):
        self.headers = {
            "Host": "www.zhihu.com",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36",
            "Referer": "http://www.zhihu.com/people/raymond-wang",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2",
        }
        self.cookies = {
            'l_cap_id': r'"NmZiNzAxNjExODU0NGIxOGFmNDViYzI4Y2I5OTE2YmI=|1467025892|d688187f21247000c202f0e75ef289ab518fb8d0"',
            'cap_id': r'"NjM0NDZhZTM1YjQ4NDkyNDhkYzE2Nzg2ZDQ2YmRiNmQ=|1467025892|dd62fc28b7f766fc3d64e515263ec521758b07d4"',
            'd_c0': r'"ABCAm1d3JAqPTsD9AFkiFJt9hseOxHj2X_k=|1467025895"',
            '_za': r'47da0294-3276-4224-949a-856b6ced4c67',
            '_zap': r'23ad6af6-0b13-48d6-8c8f-9b12dc15273e',
            'z_c0': r'Mi4wQUFBQUF1VWdBQUFBRUlDYlYzY2tDaGNBQUFCaEFsVk43NWFZVndCZWZCRk1kWTlxU2pFTlJKSDlqLTVSYThEWVpR|1467025903|6eedff4f4cb602d7c11443c4bef2fc53f52713ee',
            '_xsrf': r'aa9317a652ce891e9e6d3f140d43c969',
            'a_t': r'"2.0AAAAAuUgAAAXAAAAWdGiVwAAAALlIAAAABCAm1d3JAoXAAAAYQJVTe-WmFcAXnwRTHWPakoxDUSR_Y_uUWvA2GWUPoXYYLpZCBaXbAgNKLgprJOrWw=="',
            '__utmt': r'1',
            '__utma': r'51854390.848817227.1467455131.1467455131.1467696220.2',
            '__utmb': r'51854390.4.10.1467696220',
            '__utmz': r'51854390.1467455122.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100-1|2=registration_date=20131118=1^3=entry_date=20131118=1'
        }
        super(ZhihuSpider, self).__init__()

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield FormRequest(url, meta={'cookiejar': i}, headers=self.headers, cookies=self.cookies,
                              callback=self.parse_about)

    # 解析每个用户的基本信息
    def parse_about(self, response):
        selector = Selector(response)

        item = ZhihuspiderItem()

        # http://www.zhihu.com/people/jiang-xiao-fan-92-14/about
        # 取jiang-xiao-fan-92-14作为userID
        item['userid'] = response.url.split('/')[-2]
        # 用户名
        item['name'] = selector.css('div>.name').xpath('text()').extract()
        # 地址
        item['location'] = selector.css('.location>a').xpath('text()').extract()
        # 所在行业
        item['business'] = selector.css('.business>a').xpath('text()').extract()
        # 性别
        item['gender'] = selector.css('.gender>i').xpath('@class').extract()
        # 公司
        item['employment'] = selector.css('.employment>a').xpath('text()').extract()
        # 职位
        item['position'] = selector.css('.position>a').xpath('text()').extract()
        # 教育
        item['education'] = selector.css('.education>a').xpath('text()').extract()
        # 专业
        item['major'] = selector.css('.education-extra>a').xpath('text()').extract()
        # 关注了
        item['follower_num'] = selector.xpath('/html/body/div[3]/div[2]/div[1]/a[1]/strong/text()').extract()
        # 关注者
        item['followee_num'] = selector.xpath('/html/body/div[3]/div[2]/div[1]/a[2]/strong').xpath('text()').extract()
        # 提问数
        item['ask_num'] = selector.xpath('//a[@href="/people/xie-xi-ming/asks"]/span').xpath('text()').extract()
        # 回答数
        item['answer_num'] = selector.xpath('//a[@href="/people/xie-xi-ming/answers"]/span').xpath('text()').extract()
        # 文章数
        item['post_num'] = selector.xpath('//a[@href="/people/xie-xi-ming/posts"]/span').xpath('text()').extract()
        # 赞同
        item['agree_num'] = selector.xpath('/html/body/div[3]/div[1]/div/div[1]/div[2]/div/span[2]/strong').xpath('text()').extract()
        # 感谢
        item['thanks_num'] = selector.xpath('/html/body/div[3]/div[1]/div/div[1]/div[2]/div/span[3]/strong').xpath('text()').extract()


        for (key, val) in item.items():
            if isinstance(val, list) and len(val) > 0:
                item[key] = val[0]
            elif len(val) == 0:
                item[key] = ''

        if item['gender'].find('female') != -1:
            item['gender'] = u'female'
        elif item['gender'].find('male') != -1:
            item['gender'] = u'male'
        else:
            item['gender'] = u'unknown'

        # 解析完后,获得关注列表和被关注列表的链接,生成新的请求
        followeesHref = selector.xpath('/html/body/div[3]/div[2]/div[1]/a[1]/@href').extract()[0]
        followersHref = selector.xpath('/html/body/div[3]/div[2]/div[1]/a[2]/@href').extract()[0]
        yield FormRequest(self.host + followeesHref, meta={'cookiejar': 'followeesCookie'}, headers=self.headers,
                          cookies=self.cookies, callback=self.parse_followees)
        yield FormRequest(self.host + followersHref, meta={'cookiejar': 'followersCookie'}, headers=self.headers,
                          cookies=self.cookies, callback=self.parse_followers)

        yield item

    def parse_followees(self, response):
        selector = Selector(response)

        # 知乎上的关注了列表一次显示20条,后面的是通过ajax动态获取的,每次获取20条
        followees_or_followers = selector.xpath(
            '//*[@id="zh-profile-follows-list"]/div/div/div[2]/h2/a/@href').extract()
        for i in range(0, len(followees_or_followers)):
            yield FormRequest(followees_or_followers[i] + '/about', meta={'cookiejar': 'followersCookie'},
                              headers=self.headers, cookies=self.cookies, callback=self.parse_about)

    def parse_followers(self, response):
        selector = Selector(response)
        # 知乎上的关注者列表一次显示20条,后面的是通过ajax动态获取的,每次获取20条
        followees_or_followers = selector.xpath(
            '//*[@id="zh-profile-follows-list"]/div/div/div[2]/h2/a/@href').extract()
        for i in range(0, len(followees_or_followers)):
            yield FormRequest(followees_or_followers[i] + '/about', meta={'cookiejar': 'followersCookie'},
                              headers=self.headers, cookies=self.cookies, callback=self.parse_about)
