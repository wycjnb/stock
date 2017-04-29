from db.db_pool import Mysql
class BaseAppServer:
    def __init__(self):
        self.mysql = None
        self.mysqlEngine = None

    def getMysql(self):
        if self.mysql is None:
            self.mysql = Mysql()
            print("BaseAppServer getmysql 11111111111... ...")
        else:
            pass
        return self.mysql


    # def getMysqlLocalEngine(self, app_id):
    #     if self.mysqlLocalEngine is None:
    #         self.mysqlLocalEngine = MysqlLocalEngine(app_id)
    #         print "BaseAppServer getMysqlLocalEngine 11111111111... ..."
    #     else:
    #         pass
    #     return self.mysqlLocalEngine

    # def getMysqlLocal(self):
    # 	if self.mysqlLocal is None:
    # 		self.mysqlLocal = MysqlLoacl()
    # 		print "BaseAppServer getmysql 11111111111... ..."
    # 	else:
    # 		pass
    # 	return self.mysqlLocal

    _handle = None

    @classmethod
    def instance(cls):
        if not cls._handle:
            cls._handle = cls()
        return cls._handle

