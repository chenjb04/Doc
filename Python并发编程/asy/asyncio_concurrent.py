#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/20 17:03
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/20 17:03
 * @Desc:协程并发
"""
import asyncio
import time


async def do_something(x):
    print('Waiting:', x)
    await asyncio.sleep(x)
    return "done after {}s".format(x)


start = time.time()

coroutine1 = do_something(1)
coroutine2 = do_something(2)
coroutine3 = do_something(4)
loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(coroutine1), asyncio.ensure_future(coroutine2), asyncio.ensure_future(coroutine3)]

loop.run_until_complete(asyncio.wait(tasks))
end = time.time()

for task in tasks:
    print(task.result())

print('total time:', end - start)

