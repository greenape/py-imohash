#!/usr/bin/env python
from __future__ import division

import binascii
import glob
import os
import sys

import mmh3
import varint

SAMPLE_THRESHOLD = 128 * 1024
SAMPLE_SIZE = 16 * 1024

def hashfile(filename, sample_threshhold=SAMPLE_THRESHOLD, sample_size=SAMPLE_SIZE, hexdigest=False):
    size = os.path.getsize(filename)

    with open(filename, 'rb') as f:
        if size < sample_threshhold or sample_size < 1:
            data = f.read()
        else:
            data = f.read(sample_size)
            f.seek(size//2)
            data += f.read(sample_size)
            f.seek(-sample_size, os.SEEK_END)
            data += f.read(sample_size)

    hash_tmp = mmh3.hash_bytes(data)
    hash_ = hash_tmp[7::-1] + hash_tmp[16:7:-1]
    enc_size = varint.encode(size)
    digest = enc_size + hash_[len(enc_size):]

    return binascii.hexlify(digest) if hexdigest else digest


def imosum():
    if len(sys.argv) == 1:
        print('imosum filenames')
        return

    files = set()

    for x in sys.argv[1:]:
        files.update(glob.glob(x))

    for fn in files:
        if not os.path.isdir(fn):
            print('{}  {}'.format(hashfile(fn, hexdigest=True), fn))
