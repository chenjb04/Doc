#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/9/29 16:33
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/9/29 16:33
 * @Desc: 重复锁
"""
import threading
import time


class Box:
    rlock = threading.RLock()

    def __init__(self):
        self.total_items = 0

    def execute(self, n):
        Box.rlock.acquire()
        self.total_items += n
        Box.rlock.release()

    def add(self):
        Box.rlock.acquire()
        self.execute(1)
        Box.rlock.release()

    def remove(self):
        Box.rlock.acquire()
        self.execute(-1)
        Box.rlock.release()


def adder(box, item):
    while item > 0:
        print("adding 1 item in the box")
        box.add()
        time.sleep(1)
        item -= 1


def remover(box, item):
    while item > 0:
        print("removeing 1 item in the box")
        box.remove()
        time.sleep(1)
        item -= 1


if __name__ == '__main__':
    items = 5
    print('putting %s items in the box' % items)
    box = Box()
    t1 = threading.Thread(target=adder, args=(box, items))
    t2 = threading.Thread(target=remover, args=(box, items))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("%s items still remain in the box " % box.total_items)
