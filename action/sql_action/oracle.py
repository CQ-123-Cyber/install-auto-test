from utils.sql_tools import SqlExecutor
import models


class Oracle:
    def __init__(self):
        self.sql_executor = SqlExecutor()
        self.connect = self.sql_executor.connect(models.SqlTypeEnum.ORACLE)

    def create_database(self, database_name, password):
        sql = f"CREATE USER {database_name} PROFILE DEFAULT IDENTIFIED BY {password} DEFAULT TABLESPACE V3XSPACE TEMPORARY TABLESPACE TEMP ACCOUNT UNLOCK;"
        self.sql_executor.execute(self.connect, sql, models.SqlTypeEnum.ORACLE)
        sql = f"GRANT CREATE VIEW,ALTER SESSION,CONNECT,RESOURCE,UNLIMITED TABLESPACE TO {database_name};"
        self.sql_executor.execute(self.connect, sql, models.SqlTypeEnum.ORACLE)
        self.sql_executor.close()


if __name__ == "__main__":
    s = Oracle()
    s.create_database('install_20250418162751', 'Seeyon123456')
