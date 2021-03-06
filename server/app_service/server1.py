# -*- coding:utf-8 -*-
from base.app_base import BaseAppServer
from urllib import request,parse
from functools import reduce
import json

class server1(object):
    _ins = None
    def __init__(self):
        self.db = BaseAppServer.instance().getMysql()
        self.init()

    @classmethod
    def instance(cls):
        if not cls._ins:
            cls._ins = server1()

        return cls._ins

    def init(self):
        db_stocks_list = self.db.getAll('select stid,panel_id from stock_idlist')
        distinct_panels_id = set([db_stock_list['panel_id'] for db_stock_list in db_stocks_list])
        self.panels_stocks = []
        for distinct_panel_id in distinct_panels_id:
            panel_stocks = [db_stock_list['stid'].decode() for db_stock_list in db_stocks_list if db_stock_list['panel_id'] == distinct_panel_id]
            self.panels_stocks.append({'panel_id': distinct_panel_id, 'list': panel_stocks})
        self.stocks_list_add = [db_stock_list['stid'].decode() for db_stock_list in db_stocks_list]

    def instantinfrom(self):
        # url = 'http://qt.gtimg.cn/q=sh000001,sz399001,'
        url = 'http://qt.gtimg.cn/q='
        stocks_list_add_til = ['sh%s' % code if code[:1] in ['5', '6', '9'] else 'sz%s' % code for code in self.stocks_list_add]
        url_add = reduce(lambda x, y: x + ',' + y, stocks_list_add_til)
        url += url_add
        datas = request.urlopen(url)
        datas = datas.read().decode('gbk').strip(';\n').split(';')
        datas_split = [data.split('~') for data in datas]
        result = []
        for panel_stocks in self.panels_stocks:
            list_result = []
            for panel_stock in panel_stocks['list']:
                for data_split in datas_split:
                    if panel_stock == data_split[2]:
                        list_result.append({'a': data_split[1], 'b':data_split[2], 'c':data_split[3], 'd': data_split[32], 'e': data_split[6], 'f': data_split[38]})
            result.append({'panel_id': panel_stocks['panel_id'], 'list': list_result})
        # result = [{'a': data_split[1], 'b':data_split[2], 'c':data_split[3], 'd': data_split[32], 'e': data_split[6], 'f': data_split[38]} for data_split in datas_split]
        return result


    # def stocklist(self):
    #     stocks_list = ['000001', '399001']
    #     stocks_list += self.stocks_list_add
    #     result = {'a': stocks_list}
    #     return result

    def stock_list(self):
        result = self.panels_stocks
        return result

    def addstockinform(self, body):
        data = json.loads(body.decode())
        panel_id = data['panel_id']
        stock_id = data['stock_id']
        self.db.insertOne('insert into stock_idlist (stid,panel_id) value(%s,%s)', [stock_id, panel_id])
        self.init()

    def delstockinform(self, body):
        data = json.loads(body.decode())
        panel_id = data['panel_id']
        stock_id = data['stock_id']
        self.db.delete('DELETE FROM stock_idlist WHERE stid=%s and panel_id=%s', [stock_id, panel_id])
        self.init()

    def get_panel(self):
        panels_list = self.db.getAll('Select * from panel_id')
        panel = [{'name': panel_list['name'].decode(), 'panel_id': panel_list['panel_id']}for panel_list in panels_list]
        return panel

    def add_panel(self, body):
        data = json.loads(body.decode())
        panel_name = data['panel_name']
        self.db.insertOne('insert into panel_id (name) value(%s)', [panel_name])

    def del_panel(self, body):
        data = json.loads(body.decode())
        panel_id = data['panel_id']
        self.db.delete('DELETE FROM stock_idlist WHERE panel_id=%s', [panel_id])
        self.db.delete('DELETE FROM panel_id WHERE panel_id=%s', [panel_id])

    def suggest(self, args):
        url = 'http://smartbox.gtimg.cn/s3/'
        case = {'q': args['q'], 't': 'all', 'v': 2}
        opener = request.build_opener()
        req = request.Request(url+'?'+parse.urlencode(case))
        datas = opener.open(req).read().decode('unicode-escape')
        datas = datas.split('=')[1].split('^')
        result = []
        for data in datas:
            data_split = data.split('~')
            result.append({'stock_id': data_split[1], 'stock_name': data_split[2], 'stock_title': data_split[3]})
        return result
