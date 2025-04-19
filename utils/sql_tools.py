import os
import re
import traceback
from typing import List
from sqlalchemy import create_engine
import jaydebeapi  # 安装<<微软VC++运行库集合>>，可以直接使用360软件管家搜索安装，问题直接解决！

from conf import constant
import models

os.environ['JAVA_HOME'] = constant.JAVA_HOME


class SqlExecutor:
    def __init__(self):
        self.scheduler = dict()
        self.register()
        self.conn_close_list = []

    def connect(self, sql_type: models.SqlTypeEnum):
        return self.scheduler[sql_type]()

    def register(self):
        self.scheduler = {
            models.SqlTypeEnum.MYSQL: self.mysql,
            models.SqlTypeEnum.ORACLE: self.oracle,
            # models.SqlTypeEnum.DM: self.dm,
            # models.SqlTypeEnum.KINGBASE: self.kingbase8,
            # models.SqlTypeEnum.GBASE: self.gbasedbt,
            # models.SqlTypeEnum.OSCAR: self.oscar,
            # models.SqlTypeEnum.SQLSERVER: self.sqlserver,
            # models.SqlTypeEnum.POSTGRESQL: self.pgsql,
        }

    def mysql(self):
        try:
            engine = create_engine(constant.settings['sql'][models.SqlTypeEnum.MYSQL.value]['url'])
            conn = engine.connect()
            self.conn_close_list.append(conn)
            return conn
        except:
            print(f"mysql连接出错，跳过sql执行")
            print(traceback.format_exc())
            return None

    def dm(self):
        try:
            jar_dir = os.path.dirname(os.path.abspath(__file__))
            jars = [os.path.join(jar_dir, 'DmJdbcDriver18.jar'),
                    os.path.join(jar_dir, 'kingbase8-8.6.0.jar'),
                    os.path.join(jar_dir, 'gbasedbtjdbc_3.5.0_2ZY3_1_89a58a.jar'),
                    os.path.join(jar_dir, 'oscarJDBC.jar'),
                    os.path.join(jar_dir, 'ojdbc8.jar'),
                    os.path.join(jar_dir, 'mssql-jdbc-12.2.0.jre8.jar')]
            print(constant.settings)
            url = constant.settings['sql'][models.SqlTypeEnum.DM.value]['url']
            user = constant.settings['sql'][models.SqlTypeEnum.DM.value]['user']
            password = constant.settings['sql'][models.SqlTypeEnum.DM.value]['password']
            jclassname = 'dm.jdbc.driver.DmDriver'
            conn = jaydebeapi.connect(jclassname, url, driver_args=[user, password], jars=jars)
            cursor = conn.cursor()
            self.conn_close_list.append(cursor)
            self.conn_close_list.append(conn)
            return cursor
        except:
            print(f"达梦连接出错，跳过sql执行")
            print(traceback.format_exc())
            return None

    def kingbase8(self):
        try:
            jar_dir = os.path.dirname(os.path.abspath(__file__))
            jars = [os.path.join(jar_dir, 'DmJdbcDriver18.jar'),
                    os.path.join(jar_dir, 'kingbase8-8.6.0.jar'),
                    os.path.join(jar_dir, 'gbasedbtjdbc_3.5.0_2ZY3_1_89a58a.jar'),
                    os.path.join(jar_dir, 'oscarJDBC.jar'),
                    os.path.join(jar_dir, 'ojdbc8.jar'),
                    os.path.join(jar_dir, 'mssql-jdbc-12.2.0.jre8.jar')]
            url = constant.settings['sql'][models.SqlTypeEnum.KINGBASE.value]['url']
            user = constant.settings['sql'][models.SqlTypeEnum.KINGBASE.value]['user']
            password = constant.settings['sql'][models.SqlTypeEnum.KINGBASE.value]['password']
            jclassname = 'com.kingbase8.Driver'
            conn = jaydebeapi.connect(jclassname, url, driver_args=[user, password], jars=jars)
            cursor = conn.cursor()
            self.conn_close_list.append(cursor)
            self.conn_close_list.append(conn)
            return cursor
        except:
            print(f"人大金仓连接出错，跳过sql执行")
            print(traceback.format_exc())
            return None

    def gbasedbt(self):
        try:
            jar_dir = os.path.dirname(os.path.abspath(__file__))
            jars = [os.path.join(jar_dir, 'DmJdbcDriver18.jar'),
                    os.path.join(jar_dir, 'kingbase8-8.6.0.jar'),
                    os.path.join(jar_dir, 'gbasedbtjdbc_3.5.0_2ZY3_1_89a58a.jar'),
                    os.path.join(jar_dir, 'oscarJDBC.jar'),
                    os.path.join(jar_dir, 'ojdbc8.jar'),
                    os.path.join(jar_dir, 'mssql-jdbc-12.2.0.jre8.jar')]
            url = constant.settings['sql'][models.SqlTypeEnum.GBASE.value]['url']
            user = constant.settings['sql'][models.SqlTypeEnum.GBASE.value]['user']
            password = constant.settings['sql'][models.SqlTypeEnum.GBASE.value]['password']
            jclassname = 'com.gbasedbt.jdbc.Driver'
            conn = jaydebeapi.connect(jclassname, url, driver_args=[user, password], jars=jars)
            cursor = conn.cursor()
            self.conn_close_list.append(cursor)
            self.conn_close_list.append(conn)
            return cursor
        except:
            print(f"南大通用连接出错，跳过sql执行")
            print(traceback.format_exc())
            return None

    def oscar(self):
        try:
            jar_dir = os.path.dirname(os.path.abspath(__file__))
            jars = [os.path.join(jar_dir, 'DmJdbcDriver18.jar'),
                    os.path.join(jar_dir, 'kingbase8-8.6.0.jar'),
                    os.path.join(jar_dir, 'gbasedbtjdbc_3.5.0_2ZY3_1_89a58a.jar'),
                    os.path.join(jar_dir, 'oscarJDBC.jar'),
                    os.path.join(jar_dir, 'ojdbc8.jar'),
                    os.path.join(jar_dir, 'mssql-jdbc-12.2.0.jre8.jar')]
            url = constant.settings['sql'][models.SqlTypeEnum.OSCAR.value]['url']
            user = constant.settings['sql'][models.SqlTypeEnum.OSCAR.value]['user']
            password = constant.settings['sql'][models.SqlTypeEnum.OSCAR.value]['password']
            jclassname = 'com.oscar.Driver'
            conn = jaydebeapi.connect(jclassname, url, driver_args=[user, password], jars=jars)
            cursor = conn.cursor()
            self.conn_close_list.append(cursor)
            self.conn_close_list.append(conn)
            return cursor
        except:
            print(f"神通连接出错，跳过sql执行")
            print(traceback.format_exc())
            return None

    def oracle(self):
        try:
            jar_dir = os.path.dirname(os.path.abspath(__file__))
            jars = [os.path.join(jar_dir, 'DmJdbcDriver18.jar'),
                    os.path.join(jar_dir, 'kingbase8-8.6.0.jar'),
                    os.path.join(jar_dir, 'gbasedbtjdbc_3.5.0_2ZY3_1_89a58a.jar'),
                    os.path.join(jar_dir, 'oscarJDBC.jar'),
                    os.path.join(jar_dir, 'ojdbc8.jar'),
                    os.path.join(jar_dir, 'mssql-jdbc-12.2.0.jre8.jar')]
            url = constant.settings['sql'][models.SqlTypeEnum.ORACLE.value]['url']
            user = constant.settings['sql'][models.SqlTypeEnum.ORACLE.value]['user']
            password = constant.settings['sql'][models.SqlTypeEnum.ORACLE.value]['password']
            jclassname = 'oracle.jdbc.driver.OracleDriver'
            conn = jaydebeapi.connect(jclassname, url, driver_args=[user, password], jars=jars)
            cursor = conn.cursor()
            self.conn_close_list.append(cursor)
            self.conn_close_list.append(conn)
            return cursor
        except:
            print(f"oracle连接出错，跳过sql执行")
            print(traceback.format_exc())
            return None

    def sqlserver(self):
        try:
            jar_dir = os.path.dirname(os.path.abspath(__file__))
            jars = [os.path.join(jar_dir, 'DmJdbcDriver18.jar'),
                    os.path.join(jar_dir, 'kingbase8-8.6.0.jar'),
                    os.path.join(jar_dir, 'gbasedbtjdbc_3.5.0_2ZY3_1_89a58a.jar'),
                    os.path.join(jar_dir, 'oscarJDBC.jar'),
                    os.path.join(jar_dir, 'ojdbc8.jar'),
                    os.path.join(jar_dir, 'mssql-jdbc-12.2.0.jre8.jar')]
            url = constant.settings['sql'][models.SqlTypeEnum.SQLSERVER.value]['url']
            user = constant.settings['sql'][models.SqlTypeEnum.SQLSERVER.value]['user']
            password = constant.settings['sql'][models.SqlTypeEnum.SQLSERVER.value]['password']
            jclassname = 'com.microsoft.sqlserver.jdbc.SQLServerDriver'
            conn = jaydebeapi.connect(jclassname, url, driver_args=[user, password], jars=jars)
            cursor = conn.cursor()
            self.conn_close_list.append(cursor)
            self.conn_close_list.append(conn)
            return cursor
        except:
            print(f"sqlserver连接出错，跳过sql执行")
            print(traceback.format_exc())
            return None

    def pgsql(self):
        try:
            engine = create_engine(constant.settings['sql'][models.SqlTypeEnum.POSTGRESQL.value])
            conn = engine.connect()
            self.conn_close_list.append(conn)
            return conn
        except:
            print(f"pgsql连接出错，跳过sql执行")
            print(traceback.format_exc())
            return None

    def execute(self, conn, sql, sql_type: models.SqlTypeEnum):
        print("sql实际执行")
        sql_list = self.format_sql(sql, sql_type)
        if self.check_sql(sql_list):
            raise RuntimeError('sql中包含危险操作，drop或者update没有where条件')
        for sub_sql in sql_list:
            print(sub_sql)
            conn.execute(sub_sql)

    @staticmethod
    def check_sql(sql_list: List[str]) -> bool:
        for sql_line in sql_list:
            cleaned_line = sql_line.lower().strip()
            if cleaned_line.startswith('drop'):
                return True
            if cleaned_line.startswith('delete'):
                if not re.search(r'\bwhere\b', cleaned_line):
                    return True
        return False

    @staticmethod
    def format_sql(sql, sql_type: models.SqlTypeEnum):
        sql_list = []
        sub_sql = ""
        for line in sql.replace("\r\n", "\n").split("\n"):
            line = line.rstrip()
            if line.endswith(";"):
                sub_sql += line
                if sql_type == models.SqlTypeEnum.ORACLE:
                    sub_sql = sub_sql.rstrip(";")
                sql_list.append(sub_sql)
                sub_sql = ""
            else:
                sub_sql += line + "\n"
        return sql_list

    def close(self):
        for conn in self.conn_close_list:
            conn.close()
