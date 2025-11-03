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

logger = init_logger()

# 1103 Mon continue reviewing
class PymysqlTest:
    def __init__(self, config):
        self.connection = None  # Database connection (set to None initially, assigned value when connecting later)
        self.config = config  # Save database configuration

    # Connect to the database
    def _connect(self):
        try:
            logger.info("Connection preparation started")
            start_connect_time = time.time()  # Connection start time
            self.connection = pymysql.connect(**self.config)
            connect_time = round(time.time() - start_connect_time, 3)  # round(..., 3):keep 3 decimal places
            logger.info(f"Connection successful, time taken:{connect_time}seconds\n")
            return True
        except Exception as connect_e:
            logger.error(f"Connection error: {connect_e}")
            return False

    # Query kg_id and kg_code based on kg_name
    def _get_kg_info(self, kg_name):
        # If not connected to the database, return empty directly
        if not self.connection:
            return [], 0
        start_kg_query_time = time.time()  # kg query start time
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT kg_id, kg_code FROM xj_kg_space_info_tb WHERE kg_name = %s", (kg_name,))
                kg_query_result = cursor.fetchall()  # kg query result
                kg_query_time = round(time.time() - start_kg_query_time, 3)  # kg query time taken
                return kg_query_result, kg_query_time  # Return kg query result and time taken
        except Exception as kg_query_e:  # kg query error
            logger.error(f"Error querying kg_info（{kg_name}）: {kg_query_e}")
            return [], round(time.time() - start_kg_query_time, 3)

    def _get_category_code(self, kg_id):
        # If not connected to the database, return empty directly
        if not self.connection:
            return [], 0
        start_category_query_time = time.time()  # category_code query start time
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT category_code FROM xj_kg_file_info_tb WHERE kg_id = %s", (kg_id,))
                category_query_result = cursor.fetchall()  # category_code query result
                category_query_time = round(time.time() - start_category_query_time, 3)  # category_code time taken
                return category_query_result, category_query_time  # Return category_code query result and time taken
        except Exception as category_query_e:  # category_code query error
            logger.error(f"Error querying category_code（{kg_id}）: {category_query_e}")
            return [], round(time.time() - start_category_query_time, 3)
