#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/12 17:10
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/12 17:10
 * @Desc: map
"""
import time
from concurrent.futures import ThreadPoolExecutor


def spider(page):
    time.sleep(page)
    return page


executor = ThreadPoolExecutor(max_workers=4)

i = 1
for result in executor.map(spider, [2, 3, 4, 1]):
    print("task{}:{}".format(i, result))
    i += 1