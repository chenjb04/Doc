#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 * @Author: chenjb
 * @Date: 2020/10/16 14:29
 * @Last Modified by:   chenjb
 * @Last Modified time: 2020/10/16 14:29
 * @Desc: 管道交换数据
"""
import multiprocessing


def create_items(pipe):
    output_pipe, _ = pipe
    for item in range(10):
        output_pipe.send(item)
    output_pipe.close()


def multiply_items(pipe_1, pipe_2):
    close, input_pipe = pipe_1
    close.close()
    output_pipe, _ = pipe_2
    try:
        while True:
            item = input_pipe.recv()
            output_pipe.send(item * item)
    except EOFError:
        output_pipe.close()


if __name__ == '__main__':
    # 第一个管道发出数字
    pipe_1 = multiprocessing.Pipe(True)
    process_pipe1 = multiprocessing.Process(target=create_items, args=(pipe_1, ))
    process_pipe1.start()
    # 第二个接受并计算
    pipe_2 = multiprocessing.Pipe(True)
    process_pipe2 = multiprocessing.Process(target=multiply_items, args=(pipe_1, pipe_2))
    process_pipe2.start()
    pipe_1[0].close()
    pipe_2[0].close()
    try:
        while True:
            print(pipe_2[1].recv())
    except EOFError:
        print('end')