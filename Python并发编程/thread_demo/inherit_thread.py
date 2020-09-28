#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/9/28 17:07
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/9/28 17:07
 * @Desc: 继承线程
"""
import threading
import time


class Mythread(threading.Thread):
    def __init__(self, n):
        super().__init__()
        self.n = n

    def run(self):
        while self.n > 0:
            print('t', self.n)
            self.n -= 1
            time.sleep(2)


if __name__ == '__main__':
    t = Mythread(5)
    t.start()


