#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/13 15:37
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/13 15:37
 * @Desc: 杀死进程
"""
import time
import multiprocessing


def foo():
    print('starting function')
    time.sleep(0.1)
    print('finished function')


if __name__ == '__main__':
    p = multiprocessing.Process(target=foo)
    print('process before execution', p,  p.is_alive())
    p.start()
    print('Process running:', p, p.is_alive())
    p.terminate()
    print('Process terminated:', p, p.is_alive())
    p.join()
    print('Process joined:', p, p.is_alive())
    print('Process exit code:', p.exitcode)