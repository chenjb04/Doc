#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/9/28 14:19
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/9/28 14:19
 * @Desc:创建线程
"""
import threading
import time


def countdown(n):
    while n > 0:
        print("t", n)
        n -= 1
        time.sleep(2)


# 创建线程
t = threading.Thread(target=countdown, args=(5, ))
# 启动线程
t.start()

# 查看线程对象状态
if t.is_alive():
    print('running')
else:
    print('done')
t.join()