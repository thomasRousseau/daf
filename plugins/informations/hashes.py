#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import hashlib

def hash_for_file(path, algorithms, human_readable=True):
    fd = os.open( "foo.txt", os.O_RDWR|os.O_CREAT )
    info = os.fstatvfs(fd)
    block_size = info.f_bsize
    os.remove("foo.txt")

    algo = []
    for i in algorithms:
        algo.append(hashlib.new(i))

    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            for i in algo:
                i.update(chunk)
    if human_readable:
        file_algo = []
        for i in algo:
            file_algo.append(i.hexdigest())
    else:
        file_algo = []
        for i in algo:
            file_algo.append(i.digest())
    return file_algo

