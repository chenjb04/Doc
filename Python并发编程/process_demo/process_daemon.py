#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/12 17:40
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/12 17:40
 * @Desc:守护进程
"""
import multiprocessing
import time


def foo():
    name = multiprocessing.current_process().name
    print('starting: ', name)
    time.sleep(3)
    print('exiting: ', name)


if __name__ == '__main__':
    daemon_process = multiprocessing.Process(target=foo, name='daemon_process')
    daemon_process.daemon = True
    no_daemon = multiprocessing.Process(target=foo, name='no_daemon')
    no_daemon.daemon = False
    daemon_process.start()
    no_daemon.start()
    daemon_process.join()
    no_daemon.join()

