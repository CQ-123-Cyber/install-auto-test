import os
import sys
import logging
from types import FrameType
from typing import cast
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING_LEVEL = logging.DEBUG
logging.getLogger().handlers = [InterceptHandler()]
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
path_log = os.path.join(os.path.join(project_root, 'logs'), 'app.log')
# 路径，每日分割时间，是否异步记录，日志是否序列化，编码格式，最长保存日志时间
logger.add(path_log, rotation='0:00', enqueue=True, serialize=False, encoding="utf-8", retention="10 days")
