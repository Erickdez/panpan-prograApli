from core.pyba_database import PybaDatabase


class PybaLogic:
    def __init__(self):
        self.databaseObj = self.createDatabaseObj()

    def createDatabaseObj(self):
        database = PybaDatabase()
        return database
