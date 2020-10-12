#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/12 17:02
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/12 17:02
 * @Desc: as_completed方法
"""
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def spider(page):
    time.sleep(page)
    print(f"crawl task{page} finished")
    return page


def main():
    with ThreadPoolExecutor(max_workers=5) as t:
        obj_list = []
        for page in range(1, 5):
            obj = t.submit(spider, page)
            obj_list.append(obj)
        for future in as_completed(obj_list):
            data = future.result()
            print(f'main: {data}')


main()