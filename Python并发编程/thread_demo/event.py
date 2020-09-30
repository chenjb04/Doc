#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/9/29 13:48
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/9/29 13:48
 * @Desc: event对象 等待事件的触发
"""
import threading
import time

# 创建event对象
event = threading.Event()


def cal(name: str):
    print("{} start".format(threading.current_thread().name))
    print('{} ready cal'.format(name))
    # 阻塞状态
    event.wait()
    print('{} recv'.format(threading.current_thread().name))
    print('{} runing cal'.format(name))


for i in range(2):
    t = threading.Thread(target=cal, args=('num' + str(i), ))
    t.start()
time.sleep(2)
print('main threading send event')
event.set()