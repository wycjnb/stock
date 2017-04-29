import server


def add_resource(api):
    api.add_resource(server.handlers.task.instantinform, '/getstockinform')

    api.add_resource(server.handlers.task.StockList, '/getstocklist')

    api.add_resource(server.handlers.task.addstockinform, '/test3')

    api.add_resource(server.handlers.task.delstockinform, '/test4')

    api.add_resource(server.handlers.task.GetPanel, '/getpanel')