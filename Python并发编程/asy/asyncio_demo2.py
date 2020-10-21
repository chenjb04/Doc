#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/20 16:37
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/20 16:37
 * @Desc: task 回调
"""
import asyncio


async def do_something(x):
    print('waiting: ', x)
    return "done after {}s".format(x)


def callback(future):
    print('callback,', future.result())


coroutine = do_something(2)

loop = asyncio.get_event_loop()

task = asyncio.ensure_future(coroutine)

# 绑定回调函数，在task执行完毕后获取结果
task.add_done_callback(callback)

loop.run_until_complete(task)
