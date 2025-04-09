from enum import Enum, unique


@unique
class SqlTypeEnum(Enum):
    """
    sql类型枚举
    """
    MYSQL = 'mysql'
    ORACLE = 'oracle'
    POSTGRESQL = 'postgresql'
    SQLSERVER = 'sqlserver'
    OSCAR = '神舟通用'
    KINGBASE = '人大金仓'
    DM = '达梦'
    GBASE = '南大通用'

    @classmethod
    def from_value(cls, value):
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{value} is not a valid {cls.__name__}")


if __name__ == "__main__":
    print(SqlTypeEnum.from_value('mysql'))
