#!/usr/bin/env python
# -*- coding:UTF-8 -*-
__author__ = 'miaochenliang'

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# import++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ↓+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import os
import glob
import subprocess


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def qrc_to_py(in_path):
    qrc_path, file_flag = os.path.splitext(in_path)
    print qrc_path.replace('\\', '/')
    pipe = subprocess.Popen('pyrcc4 -o {0}_rc.py {0}.qrc'.format(qrc_path.replace('\\', '/')),
                            stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=0x08)


if __name__ == '__main__':
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'UI/').replace('\\', '/')
    func = lambda x: qrc_to_py(x)
    map(func, glob.glob(file_path + '*.qrc'))
