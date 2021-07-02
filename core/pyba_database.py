import pymysql


class PybaDatabase:
    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.user = "root"
        self.password = "root"
        self.database = "panpanbd"
        self.connection = self.createConnection()
        self.cursor = self.createCursor()

    def createConnection(self):
        con = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.password,
            database=self.database,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        return con

    def createCursor(self):
        con = self.connection
        cursor = None
        if con is not None:
            cursor = con.cursor()
        else:
            print("app is disconnected from database")
        return cursor

    # usar este metodo solo con SELECT
    def executeQuery(self, sql):
        cursor = self.cursor
        result = None
        if cursor is not None:
            cursor.execute(sql)
            result = cursor.fetchall()
        return result

    # usar este metodo con INSERT, UPDATE, DELETE u otros
    # retorna un bool true is funciono
    def executeNonQueryBool(self, sql):
        cursor = self.cursor
        con = self.connection
        success = False
        if cursor is not None:
            cursor.execute(sql)
            con.commit()
            rows = cursor.rowcount
            if rows > 0:
                success = True
        return success

    # usar este metodo con INSERT, UPDATE, DELETE u otros
    # retorna el numero de filas afectadas
    def executeNonQueryRows(self, sql):
        cursor = self.cursor
        con = self.connection
        if cursor is not None:
            cursor.execute(sql)
            con.commit()
            rows = cursor.rowcount
        return rows
