#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/9/28 16:30
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/9/28 16:30
 * @Desc:主线程结束，子线程被迫也结束
"""
import threading
import time


def run():
    time.sleep(2)
    print("current threading is: ", threading.current_thread().name)
    time.sleep(2)


if __name__ == '__main__':
    start_time = time.time()
    print("main threading is ", threading.current_thread().name)
    thread_list = []
    for _ in range(5):
        t = threading.Thread(target=run)
        thread_list.append(t)
    for t in thread_list:
        # 设置守护进程
        t.setDaemon(True)
        t.start()
    print('main threading {} done use time {}'.format(threading.current_thread().name, time.time() - start_time))