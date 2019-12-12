# coding=utf-8

import random
import time

class Stats(object):
    # 求和
    @staticmethod
    def summation(l):
        return sum(l)

    # 求最大值
    @staticmethod
    def maximum(l):
        return max(l)

    # 求极差
    @staticmethod
    def range(l):
        return max(l) - min(l)

    # 求平均数
    @staticmethod
    def avg(l):
        try:
            res = float(sum(l)) / len(l)
        except ZeroDivisionError:
            res = 0

        return float("%.2f" % res)

    # 求中位数
    @staticmethod
    def median(l):
        l = sorted(l)  # 先排序
        if len(l) % 2 == 1:
            return l[int(len(l) / 2)]
        else:
            return round((l[int(len(l) / 2 - 1)] + l[int(len(l) / 2)]) / 2.0, 2)

    # 求众数
    @staticmethod
    def mode(l):
        # 统计list中各个数值出现的次数
        count_dict = {}
        for i in l:
            if i in count_dict:
                count_dict[i] += 1
            else:
                count_dict[i] = 1
        # 求出现次数的最大值
        max_appear = 0
        for v in list(count_dict.values()):
            if v > max_appear:
                max_appear = v
        if max_appear == 1:
            return
        mode_list = []
        for k, v in list(count_dict.items()):
            if v == max_appear:
                mode_list.append(k)
        return mode_list

    # 求方差2
    @staticmethod
    def variance2(l):  # 平方的期望-期望的平方
        s1 = 0
        s2 = 0
        for i in l:
            s1 += i ** 2
            s2 += i
        return float(s1) / len(l) - (float(s2) / len(l)) ** 2

    # 求方差
    @staticmethod
    def variance(l):  # 平方-期望的平方的期望
        ex = Stats.avg(l)
        s = 0
        for i in l:
            s += (i - ex) ** 2
        return float(s) / len(l)

    # 标准方差
    @staticmethod
    def stdev(l):
        return Stats.variance(l) ** 0.5

    # 离差
    @staticmethod
    def deviation(l):
        if len(l) == 0:
            return 0.0

        avg = Stats.avg(l)
        dev_sum = 0
        for i in l:
            dev_sum += abs(i - avg)
        
        return round(dev_sum / len(l), 2)


if __name__ == "__main__":
    pass