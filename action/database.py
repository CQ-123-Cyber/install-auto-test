from abc import abstractmethod

from models.enum_model import SqlTypeEnum
from utils.time_help import datetime2str_by_format
from action.sql_action.mysql import Mysql
from action.sql_action.oracle import Oracle
from conf import constant


class Database:
    def __init__(self, sql_type: str):
        self.host = constant.settings['sql'][sql_type]['host']
        self.port = constant.settings['sql'][sql_type]['port']
        self.user = constant.settings['sql'][sql_type]['user']
        self.password = constant.settings['sql'][sql_type]['password']
        self.database_name = self.generate_database_name()
        self.default_password = "Seeyon123456"

    @staticmethod
    def generate_database_name():
        return f"install_{datetime2str_by_format(dt_format='%Y%m%d%H%M%S')}"

    @abstractmethod
    def create_database(self):
        pass

    def get_input_data(self):
        return {
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'password': self.password,
            'database_name': self.database_name
        }


class MysqlDatabase(Database):
    def create_database(self):
        s = Mysql()
        s.create_database(self.database_name)


class OracleDatabase(Database):
    def create_database(self):
        o = Oracle()
        o.create_database(self.database_name, self.default_password)

    def get_input_data(self):
        """重写input_data"""
        return {
            'host': self.host,
            'port': self.port,
            'user': self.database_name,
            'password': self.default_password,
            'database_name': 'xe'
        }


def get_database_cls(sql_type):
    cls_map = {
        SqlTypeEnum.MYSQL: MysqlDatabase(sql_type),
        SqlTypeEnum.ORACLE: OracleDatabase(sql_type)
    }
    return cls_map[SqlTypeEnum.from_value(sql_type)]
