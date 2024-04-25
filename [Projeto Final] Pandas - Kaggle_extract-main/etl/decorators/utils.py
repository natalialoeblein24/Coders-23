import time
from functools import wraps
from sys import stdout

from loguru import logger

logger.remove()

logger.add(
    sink=stdout,
    format="{time: YYYY-MM-DD HH:mm:ss} | <r>{level}</r> | {module}:{function}:{line} | <g>{message}</g> {file}",
    level="INFO",
)

logger.add(
    sink="logs/info.log",
    format="{time: YYYY-MM-DD HH:mm:ss} | <r>{level}</r> | {module}:{function}:{line} | <g>{message}</g> {file}",
    level="INFO",
    rotation="10 MB",
)

logger.add(
    sink="logs/debug.log",
    format="{time: YYYY-MM-DD HH:mm:ss} | <r>{level}</r> | {module}:{function}:{line} | <g>{message}</g> {file}",
    level="DEBUG",
    rotation="10 MB",
)


def log_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Only log to stdout
        logger.opt(depth=1).info(
            f"Chamando função {func.__name__} com argumentos: {args}, kwargs: {kwargs}"
        )
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.opt(depth=1).exception(
                f"Exceção ao chamar a função {func.__name__}: {e}", exc_info=True
            )
            raise
        logger.opt(depth=1).info(f"Função {func.__name__} retornou: {result}")
        return result

    return wrapper


def time_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(
            f"Função {func.__name__} demorou {end - start} segundos para ser executada"
        )

        return result

    return wrapper
