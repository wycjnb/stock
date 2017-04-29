from server.app_service.server1 import server1


class taskmgr(object):
    _ins = None
    def __init__(self):
        pass

    @classmethod
    def instance(cls):
        if not cls._ins:
            cls._ins = taskmgr()

        return cls._ins

    def instantinfrom(self):
        return server1().instantinfrom()

    def stocklist(self):
        return server1().stocklist()

    def savestockinform(self):
        return server1.savestockinform()
