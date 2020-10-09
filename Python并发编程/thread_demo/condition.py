#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/9 15:06
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/9 15:06
 * @Desc:线程同步方式 条件
"""
import time
from threading import Thread, Condition


# 初始化条件
condition = Condition()
items =[]


class Consumer(Thread):
    def __init__(self):
        super().__init__()

    def consume(self):
        global items
        global condition
        # 获取共享资源
        condition.acquire()
        if len(items) == 0:
            # 如果队列为0，等待通知
            condition.wait()
            print("consumer notify: no item to consume")
        # 如果队列有数据 消费1个
        items.pop()
        print("Consumer notify : consumed 1 item")
        print("Consumer notify : items to consume are " + str(len(items)))

        # 消费者通知生产者
        condition.notify()
        # 释放共享资源
        condition.release()
        
    def run(self):
        for i in range(20):
            time.sleep(2)
            self.consume()


class Producer(Thread):
    def __init__(self):
        super().__init__()

    def produce(self):
        global items
        global condition
        # 获取共享资源
        condition.acquire()
        if len(items) == 10:
            # 如果队列中满了 进入等待状态
            condition.wait()
            print("Producer notify : items producted are " + str(len(items)))
            print("Producer notify : stop the production!!")
        # 否则生产1个
        items.append(1)
        print("Producer notify : total items producted " + str(len(items)))
        # 生产者通知消费者
        condition.notify()
        # 释放共享资源
        condition.release()

    def run(self):
        for i in range(20):
            time.sleep(1)
            self.produce()


if __name__ == '__main__':
    consumer = Consumer()
    producer = Producer()
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()