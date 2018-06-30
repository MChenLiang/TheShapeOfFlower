#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time : 2018/5/14 22:34
# @email : spirit_az@foxmail.com
__author__ = 'miaochenliang'

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import os
import sqlite3


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
class ctSql(object):
    __sql_name = os.path.join(os.path.dirname(__file__), 'sqlName.db').replace('\\', '/')
    __table_name = 'image'
    __conn, __cursor = None, None

    def __init__(self):
        pass

    def connectSql(self):
        self.__conn = sqlite3.connect(self.__sql_name)
        self.__cursor = self.__conn.cursor()

    @property
    def conn(self):
        if not self.__conn:
            self.connectSql()
        return self.__conn

    @property
    def cursor(self):
        if not self.__cursor:
            self.connectSql()

        return self.__cursor

    def initTable(self):
        keyword = 'id TEXT NOT NULL, ' \
                  'chineseName TEXT NOT NULL,' \
                  'spell TEXT NOT NULL,' \
                  'otherName TEXT NOT NULL,' \
                  'SName TEXT NOT NULL,' \
                  'genera TEXT NOT NULL,' \
                  'place TEXT NOT NULL,' \
                  'description TEXT NOT NULL,' \
                  'imagePath TEXT,' \
                  'title TEXT NOT NULL,' \
                  'typeG TEXT'

        sql = "create table if not exists {0}({1})".format(self.__table_name, keyword)
        self.execute(sql)

    def execute(self, sql):
        print isinstance(sql.decode('UTF-8'), unicode)
        print 'in --->>', sql.decode('UTF-8')
        try:
            c = self.__cursor.execute(sql.decode('UTF-8'))
            self.__conn.commit()
            print 'Success >> '
        except (Exception, IOError) as e:
            print e
            print 'Error >> '
            c = self.__conn.rollback()
        finally:
            print 'sql -- >> ', sql.decode('UTF-8')
            return c

    def addCol(self, key, val):
        sql = """ALTER  TABLE   {0}  ADD COLUMN  {1} {2}""".format(self.__table_name, key, val)
        self.execute(sql)

    def insertItem(self, **kwargs):
        tempKStr = ', '.join(kwargs.keys())
        tempVStr = ', '.join(str('"%s"') % _ for _ in kwargs.values())
        kStr = '(' + tempKStr + ')'
        vStr = '(' + tempVStr + ')'
        sql = """INSERT INTO {0} {1} VALUES {2}""".format(self.__table_name, kStr, vStr)
        self.execute(sql)

    def queryItem(self, beG=None):
        sql = """SELECT * FROM {0}""".format(self.__table_name)
        if beG:
            sql += """ WHERE {0}""".format(beG)
        return self.execute(sql)

    def updateItem(self, beG, editG):
        sql = """UPDATE %s set %s where %s""" % (self.__table_name, editG, beG)
        self.execute(sql)

    def deleteItem(self, beG):
        sql = """DELETE FROM {0} WHERE {1}""".format(self.__table_name, beG)
        self.execute(sql)

    def __del__(self):
        self.__conn.commit()
        self.__conn.close()

    @property
    def c(self):
        return self.__cursor

    @property
    def conn(self):
        return self.__conn


if __name__ == '__main__':
    ct = ctSql()
    ct.connectSql()
    ct.initTable()
    # ct.execute('delete from image;')

