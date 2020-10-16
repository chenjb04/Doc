#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/16 14:52
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/16 14:52
 * @Desc: 进程池
"""
from multiprocessing import Pool


def func(data):
    res = data * data
    return res


if __name__ == "__main__":
    inputs = list(range(100))
    pool = Pool(processes=4)
    pool_outputs = pool.map(func, inputs)
    pool.close()
    pool.join()
    print('pool: ', pool_outputs)