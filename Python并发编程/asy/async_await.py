#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/20 16:58
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/20 16:58
 * @Desc: async  await
"""
import asyncio


async def do_something(x):
    print('Waiting: ', x)
    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)


coroutine = do_something(2)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(coroutine)
loop.run_until_complete(task)
print(task.result())
