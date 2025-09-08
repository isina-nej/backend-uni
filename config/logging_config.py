import os
import logging
from loguru import logger

# Configure Loguru for advanced logging
logger.add(
    os.path.join('logs', 'app.log'),
    rotation='10 MB',
    retention='1 week',
    level='INFO',
    format='{time} {level} {message}'
)

# Replace Django's logging with Loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())

logging.getLogger().addHandler(InterceptHandler())
logging.getLogger().setLevel(logging.INFO)
