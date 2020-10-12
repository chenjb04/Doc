#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/12 16:21
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/12 16:21
 * @Desc: 线程池
"""
import time
from concurrent.futures import ThreadPoolExecutor, wait


def spider(page):
    time.sleep(page)
    print(f'crawl task{page} finished')
    return page


# 创建容量为5的线程池
with ThreadPoolExecutor(max_workers=5) as t:
    # 通过submit提交执行的函数到线程池中
    task1 = t.submit(spider, 1)
    task2 = t.submit(spider, 2)
    task3 = t.submit(spider, 3)

    # 通过done来判断线程是否完成
    print(f'task1:{task1.done()}')
    print(f'task2:{task2.done()}')
    print(f'task3:{task3.done()}')

    time.sleep(2)
    print(f'task1:{task1.done()}')
    print(f'task2:{task2.done()}')
    print(f'task3:{task3.done()}')

    # 通过result获取返回值
    print(task1.result())
