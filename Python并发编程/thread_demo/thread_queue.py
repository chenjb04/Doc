#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/9/29 14:08
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/9/29 14:08
 * @Desc: 线程间通信 队列
"""
import threading
import time
from queue import Queue


def producer():
    for i in range(10):
        data_queue.put(i)
        print('production data ', i)


def consumer():
    while True:
        i = data_queue.get()
        data_queue.task_done()
        print('threading {} consumer {}'.format(threading.current_thread().name, i))


if __name__ == '__main__':
    data_queue = Queue(10)
    for _ in range(3):
        t = threading.Thread(target=consumer)
        t.start()

    for _ in range(1):
        t = threading.Thread(target=producer)
        t.start()