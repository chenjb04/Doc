#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/20 15:59
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/20 15:59
 * @Desc: 异步
"""
import asyncio


# async关键字定义一个协程
async def hello(name):
    print('hello ', name)


# 协程的调用不会直接执行，而是返回一个协程对象
coroutine = hello('world')

# 定义事件循环
loop = asyncio.get_event_loop()
# 转换为task
task = loop.create_task(coroutine)
print(task)

# task 任务加入到事件循环
"""
协程对象不能直接运行，在注册事件循环时， run_until_complete 将协程包装成了一个 task 。 
task 对象是 Future 类的子类，保存了协程运行后的状态，用于未来获取协程的结果。
"""
loop.run_until_complete(task)
print(task)