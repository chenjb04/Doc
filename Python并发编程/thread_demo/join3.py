#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/9/28 16:44
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/9/28 16:44
 * @Desc: timeout参数
"""
import time
import threading


def run():
    time.sleep(2)
    print('current threading is: ', threading.current_thread().name)
    time.sleep(2)


if __name__ == '__main__':
    start_time = time.time()
    print("main threading is ", threading.current_thread().name)
    thread_list = []
    for i in range(5):
        t = threading.Thread(target=run)
        thread_list.append(t)
    for t in thread_list:
        t.setDaemon(True)
        t.start()
    for t in thread_list:
        t.join(timeout=1)
    print('main threading {} done use time {}'.format(threading.current_thread().name, time.time() - start_time))