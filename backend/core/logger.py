# backend/core/logger.py
import logging
from backend.core.config import settings

def setup_logger():
    logger = logging.getLogger(settings.APP_NAME)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(settings.LOG_LEVEL.upper())
    return logger

logger = setup_logger()
