#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/21 9:56
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/21 9:56
 * @Desc: 协程中的状态
"""
import asyncio
import threading
import time


async def do_something(x):
    print('Waiting:', x)
    await asyncio.sleep(x)
    return "done after {}s".format(x)


if __name__ == '__main__':
    coroutine = do_something(2)
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(coroutine)

    print("pending状态： ", task)

    try:
        t = threading.Thread(target=loop.run_until_complete, args=(task,))
        t.start()
        time.sleep(1)
        print("running状态： ", task)
        t.join()
    except KeyboardInterrupt as e:
        task.cancel()
        print("cancel状态： ", task)
    finally:
        print("finished状态： ", task)
