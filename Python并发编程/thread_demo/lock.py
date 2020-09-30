#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/9/29 15:55
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/9/29 15:55
 * @Desc: 锁
"""
import threading

shard_recorce_with_lock = 0
shard_recorce_no_lock = 0

# 定义锁
shard_recorce_lock = threading.Lock()


def increment_with_lock():
    """
    加1操作
    :return:
    """
    global shard_recorce_with_lock
    for _ in range(100000):
        # 获取锁
        shard_recorce_lock.acquire()
        # 加1操作
        shard_recorce_with_lock += 1
        # 释放锁
        shard_recorce_lock.release()


def decrement_with_lock():
    """
    减一操作
    :return:
    """
    global shard_recorce_with_lock
    for _ in range(100000):
        # 获取锁
        shard_recorce_lock.acquire()
        # 加1操作
        shard_recorce_with_lock -= 1
        # 释放锁
        shard_recorce_lock.release()


def increment_no_lock():
    """
    加1操作
    :return:
    """
    global shard_recorce_no_lock
    for _ in range(1000000):
        # 加1操作
        shard_recorce_no_lock += 1


def decrement_no_lock():
    """
    减一操作
    :return:
    """
    global shard_recorce_no_lock
    for _ in range(1000000):
        # 加1操作
        shard_recorce_no_lock -= 1


if __name__ == '__main__':
    t1 = threading.Thread(target=increment_with_lock)
    t2 = threading.Thread(target=decrement_with_lock)
    t3 = threading.Thread(target=increment_no_lock)
    t4 = threading.Thread(target=decrement_no_lock)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    print('with lock result: ', shard_recorce_with_lock)
    print('no lock result: ', shard_recorce_no_lock)