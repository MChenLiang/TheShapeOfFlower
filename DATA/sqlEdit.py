#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time : 2018/5/15 21:39
# @email : spirit_az@foxmail.com
__author__ = 'miaochenliang'

import uuid
from sql import initSql

reload(initSql)


class sqlEdit(object):
    def __init__(self):
        self.ctSql = initSql.ctSql()
        self.ctSql.connectSql()

        self.conn = self.ctSql.conn
        self.cursor = self.ctSql.cursor

    def insertItem(self, **kwargs):
        if not kwargs.has_key('ID'):
            kwargs.setdefault('ID', u'%s' % uuid.uuid1())
        # for (k, v) in kwargs.items():
        #     print k, ' -- ', v
        self.ctSql.insertItem(**kwargs)

    def queryItem(self, beG):
        return self.ctSql.queryItem(beG).fetchall()

    def updateItem(self, beG, **kwargs):
        editG = ','.join(['%s="%s"' % (k, v.replace('"', "'")) for (k, v) in kwargs.items()])

        self.ctSql.updateItem(beG, editG)

    def deleteItem(self, beG):
        self.ctSql.deleteItem(beG)



if __name__ == '__main__':
    sql = sqlEdit()
    for (i, each) in enumerate(sql.queryItem("""typeG like "%多肉%" """)):
        print i, '--- >> ', each[1]
