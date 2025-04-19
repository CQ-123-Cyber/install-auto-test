import os

if os.name == "nt":
    JAVA_HOME = "D:\Java\jdk_win64"
else:
    JAVA_HOME = "/code/jdk"



settings = {
    "sql": {
        "mysql": {
                "url": "mysql+pymysql://root:Seeyoncom.123@192.168.225.11:3306?charset=utf8mb4",
                "user": "root",
                "password": "Seeyoncom.123",
                "host": "192.168.225.11",
                "port": "3306"
            },
        "oracle": {
            "url": "jdbc:oracle:thin:@192.168.225.11:1521/xe",
            "user": "system",
            "password": "oracle",
            "host": "192.168.225.11",
            "port": "1521"
        }
    }
}
