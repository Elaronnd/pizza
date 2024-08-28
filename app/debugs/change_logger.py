from sys import stdout

from loguru import logger

logger.remove(0)
log_format = "<green>{time}</green> | <level>{level:5}</level> | <level>{message}</level>"
logger.add(stdout,
           level="DEBUG",
           enqueue=True,
           format=log_format)
logger.add("logs/{time}.log",
           level="DEBUG",
           rotation="5 MB",
           enqueue=True,
           format=log_format)