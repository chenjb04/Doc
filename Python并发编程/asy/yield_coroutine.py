#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/19 16:22
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/19 16:22
 * @Desc: 基于生成器的协程
"""
from inspect import getgeneratorstate


def simple_coroutine():
    print('coroutine start')
    x = yield
    print('coroutine recv：', x)


def simple_coroutine2(a):
    print('coroutine2 start: a=', a)
    b = yield a
    print('recv: b=', b)
    c = yield a + b
    print("recv: c=", c)


if __name__ == "__main__":
    # my_coroutine = simple_coroutine()
    # print(my_coroutine)
    # next(my_coroutine)
    # print(my_coroutine.send(100))

    my_coroutine = simple_coroutine2(14)
    # 此时的协程没有激活，处于GEN_CREATED状态
    print(getgeneratorstate(my_coroutine))

    # 激活协程，next返回值为yield右边表达式返回值
    print(next(my_coroutine))

    # yield产出a的值之后，暂停，等待为b赋值，所以状态是GEN_SUSPENDED
    print(getgeneratorstate(my_coroutine))

    # 把数字28发送给暂停的协程，计算出 a+b的值，协程暂停，等待为b赋值
    print(my_coroutine.send(28))

    # 把 数字99发送给暂停的协程，产出c的值，协程终止，抛出StopIteration异常
    print(my_coroutine.send(99))

    # 此时协程已经结束，状态应该是GEN_CLOSED状态
    print(getgeneratorstate(my_coroutine))
