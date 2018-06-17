#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time : 2018/6/16 21:22
# @email : spirit_az@foxmail.com
__author__ = 'miaochenliang'

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# import+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import os
import re
import stat
import time
import shutil


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class baseFunc(object):
    def isSubString(self, subString, Str):
        flag = True
        for substr in subString:
            if substr not in Str:
                flag = False
        return flag

    def GetFileList(self, FindPath, flagStr):
        fileList = []
        fileNames = os.listdir(FindPath)
        if len(fileNames):
            for fn in fileNames:
                if len(flagStr):
                    if self.isSubString(flagStr, fn):
                        fullFileName = os.path.join(FindPath, fn).replace('\\', '/')
                        fileList.append(fullFileName)
                else:
                    fullFileName = os.path.join(FindPath, fn).replace('\\', '/')
                    fileList.append(fullFileName)
        if len(fileList):
            fileList.sort()
        return fileList

    def getListFlag(self, FindPath, flagStr):
        fileList = []
        fileNames = self.getListDir(FindPath, 'file')
        if len(fileNames):
            for fn in fileNames:
                if len(flagStr):
                    if os.path.splitext(fn)[-1] == flagStr:
                        fileList.append(fn)
                else:
                    fileList.append(fn)
        if len(fileList):
            fileList.sort()
        return fileList

    def getListDirK(self, filepath, mothon, keyword):
        fileList = self.getListDir(filepath, mothon)
        for each in fileList:
            if re.findall(keyword, each):
                yield os.path.join(filepath, each).replace('\\', '/')

    def getListDir(self, filepath, mothon):
        fileList = []
        if not os.path.exists(filepath):
            return fileList
        dirs = os.listdir(filepath)
        for each in dirs:
            if mothon == 'dir' and os.path.isdir(os.path.join(filepath, each)):
                fileList.append(each)

            elif mothon == 'file' and os.path.isfile(os.path.join(filepath, each)):
                fileList.append(each)

        if len(fileList):
            fileList.sort()
        return fileList

    def copyFiles(self, sourceDir, targetDir):  # 把某一目录下的所有文件复制到指定目录中
        if sourceDir.find(".svn") > 0:
            return
        for f in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir, f)
            targetFile = os.path.join(targetDir, f)
            if os.path.isfile(sourceFile):
                if not os.path.exists(targetDir):
                    os.makedirs(targetDir)
                # file size
                # if not os.path.exists(targetFile) or (
                #             os.path.exists(targetFile) and (
                #             os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                # file time
                if not os.path.exists(targetFile) or (
                            os.path.exists(targetFile) and (
                                    time.gmtime(os.path.getmtime(targetFile)) != time.gmtime(
                                    os.path.getmtime(sourceFile)))):
                    open(targetFile, "wb").write(open(sourceFile, "rb").read())
            if os.path.isdir(sourceFile):
                self.copyFiles(sourceFile, targetFile)

    def delete_file_folder(self, src):
        """
        delete files and folders
        """
        if os.path.isfile(src):
            try:
                os.remove(src)
            except WindowsError:
                os.chmod(src, stat.S_IWUSR)
                os.remove(src)
            except:
                print 'can`t delete {0}'.format(src)
        elif os.path.isdir(src):
            for item in os.listdir(src):
                itemsrc = os.path.join(src, item)
                self.delete_file_folder(itemsrc)
            try:
                os.rmdir(src)
            except WindowsError:
                os.chmod(src, stat.S_IWUSR)
                os.remove(src)
            except:
                print 'can`t delete {0}'.format(src)

    def removeFileInFirstDir(self, targetDir):  # 删除一级目录下的所有文件
        for file in os.listdir(targetDir):
            targetFile = os.path.join(targetDir, file)
            if os.path.isfile(targetFile):
                os.remove(targetFile)

    def coverFiles(self, sourceDir, targetDir):  # 复制一级目录下的所有文件到指定目录
        for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir, file)
            targetFile = os.path.join(targetDir, file)
            # cover the files
            if os.path.isfile(sourceFile):
                open(targetFile, "wb").write(open(sourceFile, "rb").read())

    def moveFileto(self, sourceDir, targetDir):  # 复制指定文件到目录
        shutil.copy(sourceDir, targetDir)

    def writeVersionInfo(self, targetDir):  # 往指定目录写文本文件
        open(targetDir, "wb").write("Revison:")

    def getCurTime(self):  # 返回当前的日期，以便在创建指定目录的时候用
        nowTime = time.localtime()
        year = str(nowTime.tm_year)
        month = str(nowTime.tm_mon)
        if len(month) < 2:
            month = '0' + month
        day = str(nowTime.tm_yday)
        if len(day) < 2:
            day = '0' + day
        return year + '-' + month + '-' + day

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    # system cmd+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    def copyText(self, text):
        os.popen(text)

    def open_sys(self, in_path):
        os.system('start %s' % in_path)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    # to publish+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    def listDel(self, lists):
        if not lists:
            return []
        newlist = []
        for each in lists:
            each in newlist or newlist.append(each)
        return newlist

    def get_new_ver(self, in_path):
        vers = list(self.getListDirK(in_path, 'dir', '^v\d{3}$'))
        if not vers:
            os.path.exists(in_path) or os.makedirs(in_path)
            return 'v001'
        new_ver = 'v%s' % (int(vers[-1][1:]) + 1)

        while len(new_ver) < 4:
            new_ver = new_ver.replace('v', 'v0')

        return new_ver
