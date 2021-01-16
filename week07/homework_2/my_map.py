#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File      : my_map.py
@Time      : 2021/01/16 17:25:30
@Author    : Goal
@Release   : 1.0
@Desc      : 自定义一个 python 函数，实现 map() 函数的功能。
@Reference : 
"""

class Map_(object):
    """
    自实现 map 操作
    用迭代器协议实现 map 功能
    """

    def __init__(self, func, iterables):
        self.func = func
        self.iterables = iterables
        self.idx = 0
        self.size = len(self.iterables)

    @classmethod
    def map(cls, func, iterables):
        return cls(func, iterables)

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx < self.size:
            item = self.func(self.iterables[self.idx])
            self.idx += 1
            return item
        else:
            raise StopIteration


def map(func,*iterators):
    """
    用函数方式实现 map 的功能
    """
    if len(iterators) > 0:
        minlen = min(len(subseq) for subseq in iterators)
        for i in range(minlen):
            yield func(*[list(subseq)[i] for subseq in iterators])
            
# func
def square(x):
    """
    自定义函数
    :param x: (int)
    :return: (int)
    """
    return x * x

# main
if __name__ == '__main__':
    iters = Map_.map(square, list(range(5)) ) 
    print( list(iters) )

    iters2 = map(square, [1, 2, 3, 4, 5, 6] )
    print( list(iters2) )
