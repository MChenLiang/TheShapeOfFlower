#!/usr/bin/env python
# -*- coding:UTF-8 -*-
__author__ = 'miaochenliang'

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# import++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ↓+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import os

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
rootPath = os.path.dirname(os.path.dirname(__file__))
commandTool = 'C:/Program Files/ImageMagick-7.0.6-Q16/magick.exe'


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def FindExamAllFiles():
    for root, dirs, files in os.walk(rootPath):
        for filepath in files:
            imgFileFullPath = os.path.join(root, filepath).replace('\\', '/')
            if imgFileFullPath.endswith('.png'):
                yield imgFileFullPath


if __name__ == "__main__":
    for pngPath in FindExamAllFiles():
        command = '"{0}" {1} {2}'.format(commandTool, pngPath, pngPath.replace('.png', '.png'))
        os.system(command)
