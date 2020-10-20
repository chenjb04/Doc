#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/20 10:20
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/20 10:20
 * @Desc: yield from 简化for循环
"""


def gen():
    for c in 'AB':
        yield c
    for i in range(1, 3):
        yield i


def gen1():
    yield from 'AB'
    yield from range(1, 3)


if __name__ == '__main__':
    print(list(gen()))
    print(list(gen1()))