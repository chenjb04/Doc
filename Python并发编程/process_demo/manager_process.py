#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/16 14:43
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/16 14:43
 * @Desc: 进程之间管理状态
"""
import multiprocessing


def worker(dic, key ,item):
    dic[key] = item
    print("key = %d value = %d" % (key, item))


if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    dic = mgr.dict()
    jobs = [multiprocessing.Process(target=worker, args=(dic, i, i*2)) for i in range(10)]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    print('res: ', dic)
