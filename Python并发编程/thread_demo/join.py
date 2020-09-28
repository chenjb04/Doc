#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/9/28 14:47
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/9/28 14:47
 * @Desc: 主线程结束，子线程继续执行
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
        t.start()
    print('main threading {} done use time {}'.format(threading.current_thread().name, time.time() - start_time))
