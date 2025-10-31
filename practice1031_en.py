# Review 1024 step3
import pymysql
import time
import logging
from concurrent.futures import ThreadPoolExecutor


# logging library
def init_logger():
    # time.strftime(): Format time to specified string format
    log_filename = time.strftime("%Y-%m-%d_%H-%M-%S") + "_test.log"
    logger = logging.getLogger()  # Get root logger
    # Set log level to INFO (will record INFO and higher level logs)
    logger.setLevel(logging.INFO)  # DEBUG < INFO < WARNING < ERROR < CRITICAL
    if logger.handlers:  # Prevent duplicate handlers
        return logger

    # Console log format: Time - Log Level - Message
    console_handler = logging.StreamHandler()  # Create console output handler
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)  # Set formatter for handler
    logger.addHandler(console_handler)  # Add handler to logger

    # Write to txt file
    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",
                                       datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger