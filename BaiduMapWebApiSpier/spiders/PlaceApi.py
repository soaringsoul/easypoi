import requests
import time
from numpy.random import randint
from BaiduMapWebApiSpier.settings import ak_list
import logging


class PlaceApiByBounds(object):
    def __init__(self, query_word, url):
        self.query_word = query_word
        self.ak = ak_list[randint(len(ak_list))]
        self.url = url

    def check_ak_status(self, status_code):
        # 检测使用的ak是否异常
        error_code_list = [x for x in range(201, 500)] + [2, 3, 4, 5, 101, 102]
        is_ok = True
        if status_code in error_code_list:
            is_ok = False
        return is_ok

    def get_response(self, page_num=0, ak=ak_list[randint(len(ak_list))]):
        # 根据输入的页数，返回第page_num页面的解析数据，返回的是一个字典

        url = self.url.format(query_word=self.query_word, ak=ak, page_num=page_num)
        try:
            response = requests.get(url, timeout=20)
        except Exception as e:
            print(e)
            time.sleep(2)
            ak = ak_list[randint(len(ak_list))]
            return self.get_response(page_num=page_num, ak=ak)

        data = response.json()
        status_code = data['status']
        is_ak_ok = self.check_ak_status(status_code)
        if not is_ak_ok:
            logging.info('异常ak:%s' % ak)
            ak = 'dASz7ubuSpHidP1oQWKuAK3q'
            # ak使用异常会通过邮件提醒
            # print(response.url)
            return self.get_response(page_num=page_num, ak=ak)
        else:
            # print('传入的关键词为【%s】' % self.query_word)
            # print('当前请求地址：%s' % response.url)
            return data
