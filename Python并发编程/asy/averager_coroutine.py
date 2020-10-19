#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/19 17:16
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/19 17:16
 * @Desc: 使用协程计算移动平均值
"""


def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total / count


if __name__ == "__main__":
    coro_avg = averager()

    print(next(coro_avg))
    print(coro_avg.send(10))
    print(coro_avg.send(30))
    print(coro_avg.send(5))
