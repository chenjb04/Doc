#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/19 10:45
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/19 10:45
 * @Desc: 事件循环
"""
import asyncio


def function1(end_time, loop):
    print('function1 called')
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, function2, end_time, loop)
    else:
        loop.stop()


def function2(end_time, loop):
    print('function2 called')
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, function3, end_time, loop)
    else:
        loop.stop()


def function3(end_time, loop):
    print('function3 called')
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, function1, end_time, loop)
    else:
        loop.stop()


def function4(end_time, loop):
    print('function4 called')
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, function4, end_time, loop)
    else:
        loop.stop()


# 定义事件循环对象
loop = asyncio.get_event_loop()
end_loop = loop.time() + 9.0

loop.call_soon(function1, end_loop, loop)

loop.run_forever()
loop.close()
