#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/9 14:43
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/9 14:43
 * @Desc: 线程同步方式 信号量
"""
import threading
import time
import random


# 初始化信号量
semaphore = threading.Semaphore(0)


def consumer():
    """消费者"""
    print("consumer is waiting")
    semaphore.acquire()
    print("Consumer notify: consumed itme number %s" % item)


def producer():
    """生产者"""
    global item
    time.sleep(10)
    item = random.randint(0, 1000)
    print("producer notify: produced item number %s" % item)
    semaphore.release()


if __name__ == '__main__':
    for i in range(5):
        t1 = threading.Thread(target=producer)
        t2 = threading.Thread(target=consumer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    print("over")