#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/20 10:52
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/20 10:52
 * @Desc: yield from 双向通道
"""
from collections import namedtuple


Result = namedtuple('Result', 'count average')


# 子生成器
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


# 委派生成器
def grouper(results, key):
    while True:
        results[key] = yield from averager()


# 调用方
def main(data):
    results = {}
    for key, values in data.items():
        # group发送的每个值都会由yield from处理，通过管道传给averager实例。
        group = grouper(results, key)
        next(group)
        for value in values:
            group.send(value)
        # 如果子生成器不终止，委派生成器会在yield from表达式处永远暂停
        group.send(None)
    report(results)


def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} average {:.2f}{}'.format(result.count, group, result.average, unit))


data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}


if __name__ == '__main__':
    main(data)