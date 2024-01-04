from sys import stdout
from loguru import logger

logger.add(stdout, level="INFO", colorize=False)

Logger = logger
