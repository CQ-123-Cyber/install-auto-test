from utils.sql_tools import SqlExecutor
import models


class Mysql:
    def __init__(self):
        self.sql_executor = SqlExecutor()
        self.connect = self.sql_executor.connect(models.SqlTypeEnum.MYSQL)

    def create_database(self, database_name):
        sql = f"CREATE DATABASE {database_name} CHARACTER SET utf8mb4;"
        self.sql_executor.execute(self.connect, sql, models.SqlTypeEnum.MYSQL)
        self.sql_executor.close()


if __name__ == "__main__":
    s = Mysql()
    s.create_database('test')
