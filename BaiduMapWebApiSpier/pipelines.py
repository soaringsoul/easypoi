# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from BaiduMapWebApiSpier.settings import engine
from pandas import DataFrame
from pypinyin import lazy_pinyin
from shapely.geometry import Polygon, Point
import logging
from BaiduMapWebApiSpier.settings import MYSQL_TableName


class BaidumapwebapispierPipeline(object):
    def process_item(self, item, spider):
        poly = item['poly']
        if item['results']:
            results = item['results']
            rows = []
            for result in results:
                row = []
                keys1 = ['name', 'province', 'city', 'area', 'address', 'telephone', 'uid', 'street_id', 'detail',
                         'detail_info', 'location']

                for key in keys1:
                    # d[key] = result.get(key)
                    row.append(result.get(key))

                keys2 = ['detail_url', 'tag', 'type']
                for key in keys2:
                    detail_info = result.get('detail_info')
                    if detail_info is None:
                        row.append(None)
                    else:
                        row.append(detail_info.get(key))
                keys3 = ['search_word', 'region', 'requests_url']

                for key in keys3:
                    row.append(item[key])
                rows.append([str(x) for x in row])
                print('获取到的pois:%s' % row[0])

            df = DataFrame(rows, columns=keys1 + keys2 + keys3)
            # region_pinyin = ''.join(lazy_pinyin(item['region']))
            region_pinyin = str(item['region'])
            # 判断点是否在指定poly区域内，使用到了shapely polygon.contains函数
            try:
                df['isin_region'] = df['location'].apply(
                    lambda x: poly.contains(Point(float(eval(x)['lng']), float(eval(x)['lat']))))
            except Exception as e:
                logging.info(e)
                df['isin_region'] = 999
            if MYSQL_TableName == "":
                MYSQL_TableName = '{region}_bd_map_pois'.format(region=region_pinyin)
            else:
                pass
            df.to_sql(MYSQL_TableName, engine, if_exists='append',
                      index=False)
