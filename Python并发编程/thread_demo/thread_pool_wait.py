#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/12 16:54
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/12 16:54
 * @Desc: 线程池wait方法
"""
import time
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, as_completed


def spider(page):
    time.sleep(page)
    print(f"crawl task{page} finished")
    return page


with ThreadPoolExecutor(max_workers=5) as t:
    all_tasks = [t.submit(spider, page) for page in range(1, 5)]
    wait(all_tasks, return_when=FIRST_COMPLETED)
    print("finished")
    print(wait(all_tasks, timeout=2.5))

