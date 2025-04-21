from utils.sql_tools import SqlExecutor
import models


class SqlServer:
    def __init__(self):
        self.sql_executor = SqlExecutor()
        self.connect = self.sql_executor.connect(models.SqlTypeEnum.SQLSERVER)

    def create_database(self, database_name):
        """
-- USE master 设置最大内存
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'max server memory', <MemoryInMB>;
RECONFIGURE;
        """
        sql = f"""
create database {database_name};
ALTER DATABASE {database_name} SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
ALTER DATABASE {database_name} SET READ_COMMITTED_SNAPSHOT ON;
ALTER DATABASE {database_name} SET MULTI_USER;
"""
        self.sql_executor.execute(self.connect, sql, models.SqlTypeEnum.SQLSERVER)
        self.sql_executor.close()


if __name__ == "__main__":
    s = SqlServer()
    s.create_database('install_20250421170000')
