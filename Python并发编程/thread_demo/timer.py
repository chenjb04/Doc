#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/9 17:20
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/9 17:20
 * @Desc: Timer 定时器
"""
import threading
import time


def say_time(name):
    print("{} now time: {}".format(name, time.time()))
    global timer
    timer = threading.Timer(3, say_time, [name])
    timer.start()


if __name__ == '__main__':
    timer = threading.Timer(2, say_time, ['tom'])
    timer.start()