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

# 1031 Key words
# log_filename = time.strftime("%Y-%m-%d_%H-%M-%S") + "_test.log"
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)  # DEBUG < INFO < WARNING < ERROR < CRITICAL
# if logger.handlers:
#     return logger

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

# 1103 Key words:
# self.connection = pymysql.connect(**self.config)
# with self.connection.cursor() as cursor:
#     cursor.execute("abc%s", (kg_name,))
#     kg_query_result = cursor.fetchall()
    
# 1104 Tue continue reviewing
    
    # Print results and total time
    def _print_results(self, kg_name, kg_results, kg_query_time, category_results, category_query_time):
        logger.info(f"Start processing kg_name: {kg_name}")
        logger.info(f"kg_info query time: {kg_query_time}seconds")
        if kg_results:
            logger.info(f"Results for kg_name '{kg_name}'are as follows")
            for i, kg_result in enumerate(kg_results, start=1):
                kg_id, kg_code = kg_result
                logger.info(f"kg_id of the {i}th result is {kg_id}, kg_code is {kg_code}")
                logger.info(f"  -> category_code query time:{category_query_time}seconds")
                logger.info("\n")
                # Call the get_category_codes method within the class
                # category_results = self._get_category_code(kg_id)
                if category_results:
                    # print(f"Result for kg_id = '{kg_id}' are as follows")
                    for j, category_result in enumerate(category_results, start=1):
                        category_code = category_result[0]
                        logger.info(f"category_code of the {j}th result is {category_code}")
        else:  # Added else clause, in case incorrect input name leads to no results
            logger.error(f"kg_name:{kg_name} has no query results, please check for spelling errors")
        logger.info("============\n")

    # New method to replace _run()
    def _process_single_kg(self, kg_name):
        total_start_time = time.time()  # Total start time for single task
        result_dict = {  # Use result_dict to prevent TypeError: 'NoneType' object is not subscriptable
            "kg_name": kg_name,
            "success": False,
            "total_time": 0,
            "kg_query_time": 0,
            "category_query_time": 0,
            "error": "",  # Store error information, errors occur frequently
            "have_kg_result": False  # Flag indicating if there are kg query results
        }
        if not self._connect():
            result_dict["error"] = "Database connection failed (timeout or incorrect address)"
            result_dict["total_time"] = round(time.time() - total_start_time, 3)
            return result_dict
        try:
            # Use _get_kg_info function
            kg_results, kg_query_time = self._get_kg_info(kg_name)  # Inputs for _print_results function
            result_dict["kg_query_time"] = kg_query_time  # Record kg_query time
            category_results, category_query_time = [], 0  # Temporarily empty, will query category_code if kg_id exists
            # Flag indicating if there are kg query results
            if kg_results:
                result_dict["have_kg_result"] = True
            else:
                result_dict["have_kg_result"] = False
            # Use _get_category_code function
            if kg_results:
                # There seems to be an issue, can be replaced with "for i, kg_result in enumerate(kg_results, start=1)"
                first_kg_id = kg_results[0][0]
                category_results, category_query_time = self._get_category_code(first_kg_id)
            # Use _print_results function
            result_dict["category_query_time"] = category_query_time  # Record category_query time
            self._print_results(kg_name, kg_results, kg_query_time, category_results, category_query_time)
            result_dict["success"] = True
            result_dict["total_time"] = round(time.time() - total_start_time, 3)
            return result_dict
        except Exception as progress_e:
            result_dict["error"] = str(progress_e)
            result_dict["total_time"] = round(time.time() - total_start_time, 3)
            return result_dict
        finally:
            self._close()  # Close connection after single task completes to prevent streaming issues

        # Close connection
    def _close(self):
        if self.connection:
            self.connection.close()
            # print("Single task database connection closed\n")  # Too many prints in concurrent mode, can be commented out

# 1104 Key words:
# for i, kg_result in enumerate(kg_results, start=1):
# result_dict["total_time"] = round(time.time() - total_start_time, 3)

# 1105 Wen continue reviewing

# Multi_concurrency without "_", intra_class function with "_" for differentiation
def concurrent_test(config, kg_name_list, max_workers=2):
    logger.info(f"=== Multi-concurrency test started ===")
    logger.info(f"Number of test kg_name：{len(kg_name_list)}")
    logger.info(f"Maxinum concurrency：{max_workers}")
    total_test_start_time = time.time()  # Total start time for multi-tasks, corresponding to total_start_time in _process_single_kge
    # Memory aid: multi-thread concurrency function
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Create PymysqlTest instance for single task and submit to thread pool
        futures = []
        for kg_name in kg_name_list:
            db_test = PymysqlTest(config)
            future = executor.submit(db_test._process_single_kg, kg_name)
            futures.append(future)
        # Summary
        test_results = []
        for future in futures:
            result = future.result()
            test_results.append(result)
    # Statistics (add new requirements here)
    have_result_count = sum(1 for res in test_results if res["have_kg_result"])
    no_result_count = len(test_results) - have_result_count
    total_test_time = round(time.time() - total_test_start_time, 3)
    success_count = sum(1 for res in test_results if res["success"])
    fail_count = len(test_results) - success_count
    avg_total_time = round(sum(res["total_time"] for res in test_results) / len(test_results), 3) if test_results else 0
    logger.info(f"=== Multi-concurrency test completed  ===")
    logger.info(f"Total time consumed：{total_test_time} seconds")
    logger.info(f"Number of successful tasks: {success_count}, Number of failed tasks: {fail_count}")
    logger.info(f"Number of tasks with kg query results: {have_result_count}, Number of tasks without kg query results: {no_result_count}")
    logger.info(f"Average time consumed per task: {avg_total_time} seconds")


if __name__ == "__main__":
    # Database configuration
    test_config = {
        'host': '',  # Sorry, i need to protect password
        'port': '',
        'user': '',
        'password': '',
        'database': 'AGENT_FLOW',
        'charset': 'utf8mb4',
        'connect_timeout': 10  # Added connection timeout, built_in in pymysel
    }
    test_kg_names = [
        'YES-2025',
        "test-2025-11-04",
        "LX-bug_test",
        "Testkg1",  # Can add non-existent kg_name to test failure scenarios
        "Testkg2"  # Test options:"YES-2025", "test-2025-11-04", "LX-bug_test"
    ]
    concurrent_test(
        config = test_config,
        kg_name_list=test_kg_names,
        max_workers=2  # Process 2 kg_names simultaneously, can be changed to 3/4, etc.
    )
# For new requirements, add in result_dict of concurrent_test and PymysqlTest._process_single_kg
# 1105 Wen Key words:
# with ThreadPoolExecutor(max_workers=max_workers) as executor:
#     future = executor.submit(db_test._process_single_kg, kg_name)
# avg_total_time = round(sum(res["total_time"] for res in test_results) / len(test_results), 3) if test_results else 0
# if __name__ == "__main__":
