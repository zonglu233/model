# coding:utf-8
from getData import getPucks, getGates

import random
import copy
import math
import numpy as np
from functools import reduce

# 参数
'''
ALPHA:信息启发因子，值越大，则蚂蚁选择之前走过的路径可能性就越大
      ，值越小，则蚁群搜索范围就会减少，容易陷入局部最优
BETA:Beta值越大，蚁群越就容易选择局部较短路径，这时算法收敛速度会
     加快，但是随机性不高，容易得到局部的相对最优
'''

if __name__ == "__main__":

    citys = getPucks()      # 航班（城市 - 船舶）
    ants = getGates()      # 登机口（蚂蚁 - 泊位）

    # 城市数，蚁群
    (city_num, ant_num) = (len(citys), len(ants))

    alpha = 1  # 信息素重要程度因子
    beta = 5  # 启发函数重要程度因子
    rho = 0.1  # 信息素的挥发速度
    Q = 1

    iter = 0
    itermax = 250

    pathtable = np.ones((ant_num, city_num)).astype(int)  # 路径记录表

    t = 0

    while iter < itermax:
        # 随机产生各个蚂蚁的起点城市
        if ant_num <= city_num:  # 城市数比蚂蚁数多
            pathtable[:, 0] = np.random.permutation(range(0, city_num))[:ant_num]
        else:  # 蚂蚁数比城市数多，需要补足
            pathtable[:city_num, 0] = np.random.permutation(range(0, city_num))[:]
            pathtable[city_num:, 0] = np.random.permutation(range(0, city_num))[:ant_num - city_num]

        length = np.zeros(ant_num)  # 计算各个蚂蚁的路径距离

        for i in range(ant_num):
            ant = ants[t]
            city = range(city_num)  # 随机找下一个航班（城市）
            city = citys[city]
            print(city)
            print(ant)
            # 判断是否满足停机条件
            unvisited = set(range(city_num))  # 未访问的城市

            if ant.open < city.arrive_point and city.body_type == ant.body_type and (ant.arrive_type == 'A' or ant.arrive_type == city.arrive_type) and (ant.leave_type == 'A' or ant.leave_type == city.leave_type):
                visiting = pathtable[i, 0]  # 当前所在的城市
                unvisited.remove(visiting)  # 删除元素
                pathtable[t, 0] = 0
                ant['city_num'] = int(ant['city_num'] + 1)
                ant.open = city.leave_point + 45

            # for j in range(1, city_num):
                # 每次用轮盘法选择下一个船舶
                # listunvisited = list(un)























