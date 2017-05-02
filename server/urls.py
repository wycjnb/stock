import server


def add_resource(api):
    api.add_resource(server.handlers.task.instantinform, '/getstockinform')

    api.add_resource(server.handlers.task.StockList, '/getstocklist')

    api.add_resource(server.handlers.task.addstockinform, '/addstock')

    api.add_resource(server.handlers.task.delstockinform, '/deletestock')

    api.add_resource(server.handlers.task.GetPanel, '/getpanel')

    api.add_resource(server.handlers.task.AddPanel, '/addpanel')

    api.add_resource(server.handlers.task.DelPanel, '/delpanel')

    api.add_resource(server.handlers.task.Suggest, '/suggest')
