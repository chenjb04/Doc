#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/20 17:26
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/20 17:26
 * @Desc: 协程嵌套
"""
import asyncio


# 内部协程
async def do_something(x):
    print('Waiting:', x)
    await asyncio.sleep(x)
    return "done after {}s".format(x)


# 外部协程

async def main():
    coroutine1 = do_something(1)
    coroutine2 = do_something(2)
    coroutine3 = do_something(4)
    tasks = [asyncio.ensure_future(coroutine1), asyncio.ensure_future(coroutine2), asyncio.ensure_future(coroutine3)]
    results = await asyncio.gather(*tasks)
    for result in results:
        print('Task ret: ', result)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
