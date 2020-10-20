#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/20 9:39
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/20 9:39
 * @Desc: 生成器throw和close方法 异常处理和终止协程
"""
from inspect import getgeneratorstate


class DemoException(Exception):
    pass


def demo_exc_handing():
    print('coroutine start')
    while True:
        try:
            x = yield
        except DemoException:
            print('DemoException handled')
        else:
            print("coroutine recv: {!r}".format(x))

    # 这一行代码永远不会执行，因为只有未处理的异常才会终止无限循环，而出现未处理的异常，协程会立马终止
    raise RuntimeError('this line should never run')


if __name__ == "__main__":
    exc_coro = demo_exc_handing()
    next(exc_coro)
    exc_coro.send(11)
    exc_coro.send(22)
    # exc_coro.close()
    # print(getgeneratorstate(exc_coro))

    # 把DemoException异常传入demo_exc_handing协程，他会处理，然后继续执行
    exc_coro.throw(DemoException)
    print(getgeneratorstate(exc_coro))

    # 如果传入未处理的异常，协程会停止
    exc_coro.throw(ZeroDivisionError)

    