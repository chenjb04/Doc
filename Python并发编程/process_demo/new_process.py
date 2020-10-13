#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/12 17:29
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/12 17:29
 * @Desc: 创建进程
"""

import multiprocessing


def foo(i):
    print('called function in process: ', i)


if __name__ == '__main__':
    for i in range(5):
        p = multiprocessing.Process(target=foo, args=(i, ))
        p.start()
        p.join()