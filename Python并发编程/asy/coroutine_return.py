#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/20 10:04
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/20 10:04
 * @Desc: 让协程返回值
"""
from collections import namedtuple


Result = namedtuple('Result', 'count average')


def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)


if __name__ == "__main__":
    coro_avg = averager()
    next(coro_avg)
    coro_avg.send(10)
    coro_avg.send(30)
    coro_avg.send(6.5)
    # 发送None终止循环，导致协程结束，生成器抛出StopIteration异常，返回结果保存在异常对象value属性中。
    # coro_avg.send(None)
    result = None
    try:
        coro_avg.send(None)
    except StopIteration as e:
        result = e.value
    print(result)


