import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
from db.setting import *
import traceback


class Mysql(object):
    """
    MYSQL库连接 , 此类中的连接采数据库对象，负责产生数据用连接池实现获取连接对象：conn = Mysql.getConn()
            释放连接对象;conn.close()或del conn
    """

    # 连接池对象
    # __pool = None
    def __init__(self):
        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        print("*************************************")
        self.pool = self.getPool()
        self._conn = None
        self._cursor = None

    def getPool(self):
        print("init mysql conn pool... ...")
        pool = PooledDB(creator=MySQLdb, mincached=5, maxcached=50,
                        host=LAE_JDBC_HOST, port=LAE_JDBC_PORT,
                        user=LAE_JDBC_USER, passwd=LAE_JDBC_PASSWD,
                        db=LAE_JDBC_DEFAULT_DB, use_unicode=False,
                        charset='utf8', cursorclass=DictCursor)
        return pool

    # @staticmethod
    # def __getConn():
    #     """
    #     @summary: 静态方法，从连接池中取出连接
    #     @return MySQLdb.connection
    #     """
    #     print "**************__getConn111***********************"
    #     if Mysql.__pool is None:
    #         print "**************__getConn2222***********************"
    #         __pool = PooledDB(creator=MySQLdb, mincached=5 , maxcached=50 ,
    #                           host=settings.LAE_JDBC_HOST , port=settings.LAE_JDBC_PORT ,
    #                           user=settings.LAE_JDBC_USER , passwd=settings.LAE_JDBC_PASSWD ,
    #                           db=settings.LAE_JDBC_DEFAULT_DB,use_unicode=False,
    #                           charset='utf8',cursorclass=DictCursor)
    #     print "**************__getConn333***********************"
    #     return __pool.connection()

    def getMyConn(self):
        # if self._conn is None or self._cursor is None or self._conn == '' or self._cursor == '':
        self._conn = self.pool.connection()
        self._cursor = self._conn.cursor()

    def getAll(self, sql, param=None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        result = False
        try:
            print("mysql_conn_getAll...")
            self.getMyConn()
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            if count > 0:
                result = self._cursor.fetchall()
            else:
                result = False
        except:
            print("except,sql:", sql)
            traceback.print_exc()
        finally:
            self.dispose()
        return result

    def getCount(self, sql):
        count = 0
        try:
            self.getMyConn()
            count = self._cursor.execute(sql)
        except:
            traceback.print_exc()
        finally:
            self.dispose()
        return count

    def getOne(self, sql, param=None):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        self.getMyConn()
        result = False
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            if count > 0:
                result = self._cursor.fetchone()
            else:
                result = False
        except:
            traceback.print_exc()
        finally:
            self.dispose()
        return result

    def getMany(self, sql, num, param=None):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        self.getMyConn()
        result = False
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            if count > 0:
                result = self._cursor.fetchmany(num)
            else:
                result = False
        except:
            traceback.print_exc()
        finally:
            self.dispose()
        return result

    def insertOne(self, sql, value):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        self.getMyConn()
        id = -1
        try:
            self._cursor.execute(sql, value)
            id = self.__getInsertId()
        except:
            traceback.print_exc()
        finally:
            self.dispose()
        return id

    def insertMany(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        self.getMyConn()
        count = 0
        try:
            count = self._cursor.executemany(sql, values)
        except:
            traceback.print_exc()
        finally:
            self.dispose()
        return count

    def __getInsertId(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def __query(self, sql, param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        return count

    def update(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        self.getMyConn()
        result = 0
        try:
            result = self.__query(sql, param)
        except:
            traceback.print_exc()
        finally:
            self.dispose()
        return result

    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        self.getMyConn()
        result = 0
        try:
            result = self.__query(sql, param)
        except:
            traceback.print_exc()
        finally:
            self.dispose()
        return result

    def begin(self):
        """
        @summary: 开启事务
        """
        try:
            self._conn.autocommit(0)
        except:
            traceback.print_exc()
        finally:
            self.dispose()

    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self, isEnd=1):
        """
        @summary: 释放连接池资源
        """
        try:
            if isEnd == 1:
                self.end('commit')
            else:
                self.end('rollback')
        except:
            traceback.print_exc()
        self._cursor.close()
        self._conn.close()
        self._cursor = None
        self._conn = None

