#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/13 15:44
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/13 15:44
 * @Desc: 继承进程
"""
from multiprocessing import Process


class MyProcess(Process):
    def __init__(self):
        super().__init__()

    def run(self):
        print('called run method in process: %s' % self.name)
        return


if __name__ == '__main__':
    for _ in range(5):
        p = MyProcess()
        p.start()
        p.join()

