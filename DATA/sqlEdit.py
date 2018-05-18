#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time : 2018/5/15 21:39
# @email : spirit_az@foxmail.com
__author__ = 'miaochenliang'

import uuid
from sql import initSql


class sqlEdit(object):
    def __init__(self):
        self.ctSql = initSql.ctSql()
        self.ctSql.connectSql()

        self.conn = self.ctSql.conn
        self.cursor = self.ctSql.cursor

    def insertItem(self, **kwargs):
        kwargs.setdefault('ID', str(uuid.uuid1()))
        # for (k, v) in kwargs.items():
        #     print k, ' -- ', v
        self.ctSql.insertItem(**kwargs)

    def queryItem(self, beG):
        return self.ctSql.queryItem(beG).fetchall()


if __name__ == '__main__':
    sql = sqlEdit()
    for (i, each) in enumerate(sql.queryItem("""typeG like "%多肉%" """)):
        print i, '--- >> ', each[1]

