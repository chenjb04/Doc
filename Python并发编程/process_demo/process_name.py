#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/12 17:35
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/12 17:35
 * @Desc: 进程命名
"""

import multiprocessing
import time


def foo():
    name = multiprocessing.current_process().name
    print('staring: ', name)
    time.sleep(3)
    print('exiting: ', name)


if __name__ == '__main__':
    process_with_name = multiprocessing.Process(target=foo, name='foo_process')
    process_with_default_name = multiprocessing.Process(target=foo)
    process_with_name.start()
    process_with_default_name.start()
    process_with_name.join()
    process_with_default_name.join()