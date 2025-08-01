import logging
import sys
from typing import ClassVar

from colorlog import ColoredFormatter

from src.core.config import config


class Logger:
    FMT: ClassVar[str] = "%(asctime)s | %(levelname)-5s | %(name)-35s | %(message)s"
    DATEFMT: ClassVar[str] = "%Y-%m-%d %H:%M:%S"
    LOG_COLORS: ClassVar[dict[str, str]] = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }

    @classmethod
    def setup(cls, name: str = __name__) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        if logger.hasHandlers():
            logger.handlers.clear()

        formatter = cls._get_formatter()

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger

    @classmethod
    def _get_formatter(cls) -> logging.Formatter:
        if not config.ENABLE_LOGGER:
            return logging.Formatter("%(message)s")

        if config.ENABLE_COLORED_LOGS:
            try:
                return ColoredFormatter(
                    fmt=f"%(log_color)s{cls.FMT}",
                    datefmt=cls.DATEFMT,
                    log_colors=cls.LOG_COLORS,
                    force_color=True,
                )
            except ImportError:
                pass

        return logging.Formatter(fmt=cls.FMT, datefmt=cls.DATEFMT)
