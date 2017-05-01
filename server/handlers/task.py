from flask_restful import Api, Resource, reqparse
from server.app_service.server1 import server1
from server.task.taskmgr import taskmgr


class instantinform(Resource):
    def get(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('id', type=str, default='')
        # args = parser.parse_args()
        result = server1.instance().instantinfrom()
        # result = taskmgr.instance().instantinfrom()
        return result


class StockList(Resource):
    def get(self):
        result = server1.instance().stock_list()
        # result = taskmgr.instance().stocklist()
        return result


class addstockinform(Resource):
    def post(self):
        body = reqparse.request.get_data()
        server1.instance().addstockinform(body)
        # taskmgr.instance().savestockinform()


class delstockinform(Resource):
    def post(self):
        body = reqparse.request.get_data()
        server1.instance().delstockinform(body)


class GetPanel(Resource):
    def get(self):
        result = server1.instance().get_panel()
        return result

class AddPanel(Resource):
    def post(self):
        body = reqparse.request.get_data()
        server1.instance().add_panel(body)

class DelPanel(Resource):
    def post(self):
        body = reqparse.request.get_data()
        server1.instance().del_panel(body)
