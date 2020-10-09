#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/9/29 13:48
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/9/29 13:48
 * @Desc: event对象 等待事件的触发
"""
import random
import threading
import time

# 创建event对象
event = threading.Event()
items = []


class Consumer(threading.Thread):
    def __init__(self, items, event):
        super().__init__()
        self.items = items
        self.event = event

    def run(self):
        while True:
            time.sleep(2)
            self.event.wait()
            item = self.items.pop()
            print('Consumer notify : %d popped from list by %s' % (item, self.name))


class Producer(threading.Thread):
    def __init__(self, items, event):
        super().__init__()
        self.items = items
        self.event = event

    def run(self):
        global item
        for i in range(100):
            time.sleep(2)
            item = random.randint(0, 256)
            self.items.append(item)
            print('Producer notify : item N° %d appended to list by %s' % (item, self.name))
            print('Producer notify : event set by %s' % self.name)
            # 发出通知
            self.event.set()
            print('Produce notify : event cleared by %s ' % self.name)
            self.event.clear()
# def cal(name: str):
#     print("{} start".format(threading.current_thread().name))
#     print('{} ready cal'.format(name))
#     # 阻塞状态
#     event.wait()
#     print('{} recv'.format(threading.current_thread().name))
#     print('{} runing cal'.format(name))
#
#
# for i in range(2):
#     t = threading.Thread(target=cal, args=('num' + str(i), ))
#     t.start()
# time.sleep(2)
# print('main threading send event')
# event.set()


if __name__ == '__main__':
    t1 = Producer(items, event)
    t2 = Consumer(items, event)
    t1.start()
    t2.start()
    t1.join()
    t2.join()