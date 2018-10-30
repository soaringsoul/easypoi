# 解决Fatal Python error: Cannot recover from stack overflow 的治标不治本的庐江
import sys
# from multiprocessing import Pool, Queue, Process, Lock
from multiprocessing.dummy import Pool

import logging
from shapely.geometry import Polygon
from BaiduMapWebApiSpier.settings import ak
from BaiduMapWebApiSpier.util.geo.amap_get_geopolylines import get_region_polyline
from BaiduMapWebApiSpier.util.geo.split_rectangle_area import split_rectanle_area
from BaiduMapWebApiSpier.spiders.PlaceApi import PlaceApiByBounds
from BaiduMapWebApiSpier.TailRecurseException import tail_call_optimized

global bounds_lst
bounds_lst = []


class GetBoundsList(object):
    def __init__(self, query_word, region_poly):
        self.poly = region_poly
        self.query_word = query_word
        minx, miny, maxx, maxy = self.poly.bounds
        self.bounds = ','.join([str(x) for x in [miny, minx, maxy, maxx]])
        print(self.bounds)
        self.global_poly_lst = []

    def get_bounds_lst(self):
        poly_lst = split_rectanle_area(self.poly)
        params_tuple = poly_lst, self.query_word
        global_poly_lst = self.get_bounds_lst_iter(params_tuple)
        bounds_lst = [self.poly_lst_convert2_bounds_lst(x) for x in global_poly_lst]
        return bounds_lst

    def poly_lst_convert2_bounds_lst(self, poly):
        minx, miny, maxx, maxy = poly.bounds
        # 调整矩形分割精度, 后续再设置
        # 在原有分割矩形的基础上扩大10%
        deviation_x = (maxx - minx) * 0
        deviation_y = (maxy - miny) * 0
        bounds = ','.join(
            [str(x) for x in [miny - deviation_y, minx - deviation_x, maxy + deviation_y, maxx + deviation_x]])
        return bounds

    @tail_call_optimized
    def get_single_poly_bounds(self, params_tuple):
        """
        :param params_tuple: (poly, query_word)
        :return: [bounds1,bounds2, ……]
        """
        # bounds_lst默认为空列表
        poly, query_word = params_tuple
        minx, miny, maxx, maxy = poly.bounds
        # 调整矩形分割精度, 后续再设置
        # 在原有分割矩形的基础上扩大10%
        deviation_x = (maxx - minx) * 0.1
        deviation_y = (maxy - miny) * 0.1
        bounds = ','.join(
            [str(x) for x in [miny - deviation_y, minx - deviation_x, maxy + deviation_y, maxx + deviation_x]])
        url = "http://api.map.baidu.com/place/v2/search?output=json" \
              "&query={query_word}" \
              "&page_size=20" \
              "&scope=2" \
              "&bounds=%s" \
              "&ak={ak}" \
              "&page_num={page_num}" % bounds
        data = PlaceApiByBounds(query_word=query_word, url=url).get_response()
        try:
            total = data['total']
        except Exception as e:
            logging.info(e)
            logging.info(data)

        if total >= 400:
            # print('当前区域的兴趣点数量:%s，>400,将再次进行分割' % bounds)
            # params_tuple = poly, query_word

            return False, poly
        else:
            bounds_lst.append(bounds)
            return True, poly

    def get_polys_bounds(self, params_tuple):
        poly, query_word = params_tuple
        poly_lst = split_rectanle_area(poly)
        params_tuple_lst = []
        for poly2 in poly_lst:
            params_tuple = poly2, query_word
            params_tuple_lst.append(params_tuple)
        p = Pool(processes=12)
        p.map(self.get_single_poly_bounds, params_tuple_lst)
        print('当前bounds_lst数量：%s' % len(bounds_lst))

    @tail_call_optimized
    def get_bounds_lst_iter(self, params_tuple):
        print('当前global_poly_list数量：%s' % len(self.global_poly_lst))
        poly_lst, query_word = params_tuple
        new_poly_lst = []
        poly_lst_iter = []
        # 将列表中的poly分割，一个变4个
        for poly in poly_lst:
            tmp_lst = split_rectanle_area(poly)
            poly_lst_iter.extend(tmp_lst)
        # 定义传入的参数列表
        params_tuple_lst = []
        for poly2 in poly_lst_iter:
            params_tuple = poly2, query_word
            params_tuple_lst.append(params_tuple)
        # 使用多线程
        p = Pool(processes=len(poly_lst_iter))
        results = p.map(self.get_single_poly_bounds, params_tuple_lst)
        for result in results:
            check, poly = result
            # 若poly区域内兴趣点小于400个
            if check:
                self.global_poly_lst.append(poly)
            # 若小于400个，加入新列表中准备递归分割
            else:
                new_poly_lst.append(poly)
        if new_poly_lst:
            # 开始递归分割
            new_params_tuple = (new_poly_lst, query_word)
            return self.get_bounds_lst_iter(new_params_tuple)
        else:
            return self.global_poly_lst


if __name__ == "__main__":
    region = '温江区'
    poly = get_region_polyline(region)
    print(poly)
    obj = GetBoundsList('购物', poly)
    bounds = obj.get_rectangle_bounds(poly, '购物')
    p = Pool(processes=4)
    for bound in bounds:
        bounds_lst = [x for x in bound]
        print(bounds_lst)
