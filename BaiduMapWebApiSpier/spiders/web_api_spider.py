import logging
import scrapy

from scrapy.spiders import Spider
from datetime import datetime
from pandas import DataFrame
import pandas as pd

import json
from numpy.random import randint
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool

from BaiduMapWebApiSpier.settings import ak_list, query_word_list, region_name_list
from BaiduMapWebApiSpier.util.geo.amap_get_geopolylines import get_region_polyline
from BaiduMapWebApiSpier.util.geo.GetRegionBounds import GetBoundsList

from BaiduMapWebApiSpier.items import BaidumapwebapispierItem
from BaiduMapWebApiSpier.util.email.send_email import send_email_163
from BaiduMapWebApiSpier.util.geo.BaiduMapGeoConvert import BaiduMapGeoConvert


class WebApiCrawler(Spider):
    name = 'bd_map_spider'
    allowed_domains = ['api.map.baidu.com']

    def get_bounds_lst(self, query_word, poly):
        obj = GetBoundsList(query_word=query_word, region_poly=poly)
        bounds_lst = obj.get_bounds_lst()
        print('关键词：%s\n bounds_lst个数：%s' % (query_word, len(bounds_lst)))
        return bounds_lst

    def __init__(self):
        self.region_name_list = region_name_list
        self.ak_lst = ak_list

    def start_requests(self):
        """
        将符合城市的坐标遍历进url
        """
        for region_name in self.region_name_list:
            print('当前region: %s\n将获取该区域的边界坐标' % region_name)
            poly = get_region_polyline(region_name)
            bd_poly = BaiduMapGeoConvert.geo_convert_no_limit_return_polygon(poly)
            params_tuple_lst = []
            for query_word in query_word_list:
                params_tuple = (region_name, query_word, bd_poly)
                params_tuple_lst.append(params_tuple)
            p = ThreadPool(processes=20)
            yield_urls = p.map(self.get_query_word_request_urls, params_tuple_lst)

            url_lists = list(self.yield_from_iter(yield_urls))
            logging.info('当前需要解析的url共有%s个' % len(url_lists))
            for url_query_word in url_lists:
                url, query_word = url_query_word
                yield self.make_requests_from_url(url, query_word, region_name, poly)

    def yield_from_iter(self, yield_iters):
        for yield_iter in yield_iters:
            yield from yield_iter

    def get_query_word_request_urls(self, params_tuple):
        region_name, query_word, poly = params_tuple
        print('获取区域边界坐标成功，当前关键词：%s，将根据该关键词在各个矩形区域内的pois数量切割区域' % query_word)
        bounds_lst = self.get_bounds_lst(query_word, poly)
        print('已获取关键词对应的矩形区域列表，下面开始解析')
        init_url = "http://api.map.baidu.com/place/v2/search?output=json" \
                   "&query={query_word}" \
                   "&page_size=20" \
                   "&scope=2" \
                   "&bounds={bounds}" \
                   "&ak={ak}" \
                   "&page_num={page_num}"
        request_urls = []
        for bounds in bounds_lst:
            start_url = init_url.format(query_word=query_word, bounds=bounds, ak="{ak}", page_num="{page_num}")
            url_lst = [start_url.format(ak="{ak}", page_num=x) for x in range(20)]
            request_urls.extend(url_lst)
            for url in url_lst:
                # query_word和region_name只是为了记录
                yield url, query_word

    def make_requests_from_url(self, url, query_word, region_name, poly):
        # query_word和region_name只是为了记录
        if len(ak_list) < 1:
            ak = 'dASz7ubuSpHidP1oQWKuAK3q'
        else:
            ak = ak_list[randint(len(ak_list))]
        response = scrapy.Request(url.format(ak=ak), callback=self.parse_judge_success, errback=self.errback_httpbin,
                                  dont_filter=True)
        response.meta['ak'] = ak
        response.meta['raw_url'] = url
        response.meta['query_word'] = query_word
        response.meta['region'] = region_name
        response.meta['poly'] = poly
        return response

    def parse_judge_success(self, response):
        ak, raw_url, query_word, region, poly = response.meta['ak'], response.meta['raw_url'], \
                                                response.meta['query_word'], response.meta['region'], response.meta[
                                                    'poly']
        data = json.loads(response.text)
        status_code = data['status']
        if status_code != 0:
            try:
                message = data['message']
            except:
                message = ''
            if len(ak_list) <= 0:
                # 使用最后的备份
                ak = 'dASz7ubuSpHidP1oQWKuAK3q'
            # 对失效的ak进行处理
            self.bad_ak_process(ak, status_code, message)
            # 对于失效ak对应的raw_url重新进行请求
            logging.info('当前使用的ak:%s无效，请求目标url:%s，将再次request' % (ak, response.url))
            self.make_requests_from_url(raw_url, query_word=query_word, region_name=region, poly=poly)

        else:
            item = BaidumapwebapispierItem()
            item['results'] = data['results']
            item['search_word'] = query_word
            item['region'] = region
            item['requests_url'] = response.url
            item['poly'] = poly
            if item['results']:
                yield item

    def bad_ak_process(self, ak, status_code, message):

        # ak使用异常会通过邮件提醒
        email_subject = '百度地图PlaceAPi ak异常状态通知'
        email_body = """
                                   Mr Xu:
                                       当前使用的ak：{ak} 状态码为 {status}；异常信息为：{message}!
                                       使用异常！请知悉！

                                   """.format(ak=ak, status=status_code, message=message)

        try:
            bad_ak_df = pd.read_csv(r'bad_ak_lst.csv')
            bad_ak_lst = [x for x in bad_ak_df['bad_ak']]
            if ak not in bad_ak_lst:
                send_email_163(email_subject, email_body, 'bad_ak_lst.csv')
        except Exception as e:
            logging.info(e)

        write_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df_bad_ak = DataFrame([[ak, status_code, message, write_time]],
                              columns=['bad_ak', 'status_code', 'message', '写入时间'])
        df_bad_ak.to_csv('bad_ak_lst.csv', mode='a+', index=False)

    def errback_httpbin(self, failure):
        pass


if __name__ == "__main__":
    obj = WebApiCrawler()
