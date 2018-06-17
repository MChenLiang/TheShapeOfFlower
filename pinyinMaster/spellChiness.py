#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time : 2018/5/28 22:35
# @email : spirit_az@foxmail.com
__author__ = 'miaochenliang'

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import os
import json

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
__start_path__ = os.path.dirname(__file__)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class connect(object):
    # from collections import defaultdict
    # word_dict = defaultdict()
    __data_path__ = os.path.join(__start_path__, 'wordData.js').replace('\\', '/')

    def __init__(self):
        if not os.path.exists(self.__data_path__):
            raise IOError("NotFoundFile")

        with open(self.__data_path__, 'r') as f:
            self.word_dict = json.loads(f.read())

    def write(self, **kwargs):
        for (k, vs) in kwargs.items():
            k = ord(k)
            oldV = self.word_dict[k] if self.word_dict.has_key(k) else list()

            v = list(set(oldV) ^ set(vs))

            self.word_dict.setdefault(k, v)

        with open(self.__data_path__, 'w') as f:
            f.write(json.dumps(self.word_dict))

    def find(self, key):
        k = str(ord(key))
        return key if not self.word_dict.has_key(k) else self.word_dict[k]

    def read(self, *args):
        for k in args:
            yield self.find(k)

    def split(self, spl='', *args):
        return spl.join([v[0] for v in self.read(*args)])


if __name__ == '__main__':
    ct = connect()
    print ct.split('_', u'大')
