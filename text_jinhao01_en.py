"""
1117 Mon - Testing objectives:
Batch processing of multiple files, different file formats, time statistics
requests library:
    requests.post(url, headers=, json=)
    response.json()text_jinhao01.py
    result_data.get('minio_path', 'No path')
    response.status_code
1118 Tue
os library (local):
    os.listdir(path) - List all files and folders in a directory
    os.path.join(path1, path2) - Safely join paths
    os.path.splitext(filename) - Split filename and extension
    os.path.isdir(path) - Check if it's a directory
    os.path.isfile(path) - Check if it's a file
"""
import time  # Required library
import requests
# Import configuration file
from test_jinhao_config import GLOBAL_CONFIG, TEST_FILE_LIST, TEST_URL, HEADER, AUTO_DISCOVER, AUTO_DISCOVER_FOLDER


# First define single file test
def _test_singlefile(test_files):
    print(f"Starting test file: {test_files['file_path']}")
    start_time = time.time()  # Record time

    # Send request
    request_config = GLOBAL_CONFIG.copy()
    request_config["file_path"] = test_files['file_path']
    response = requests.post(TEST_URL, headers=HEADER, json=request_config)

    # Record results (success) (time)
    end_time = time.time()
    cost_time = round(end_time - start_time, 2)
    print(f"Response status code: {response.status_code}")
    result_data = response.json()  # response.json() is formatted, original is response.text
    result_success = result_data['success']
    result_filepath = result_data.get('minio_path', 'No path')  # get method is safer
    return {
        "success": result_success,
        "minio_path": result_filepath,
        "message": result_data,
        "cost_time": cost_time
    }


# Loop through multiple tests
def _multi_test(test_file_lists):
    i = 0
    success_i = 0
    total_time = 0
    for test_file in test_file_lists:
        i += 1
        result = _test_singlefile(test_file)
        if result['success']:
            print(f"Success | File {i}, Original path: {test_file['file_path']}, Time: {result['cost_time']}s")
            success_i += 1
            # print(f"Success | File {i}, Original path: {test_file['file_path']}, Time: {result['cost_time']}s,
            # Result: {result['message']}, Stored at: {result['minio_path']}")
        else:
            print(f"Failed~")
            # print(f"Failed | File {i}, Original path: {test_file['file_path']}, Time: {result['cost_time']}s,
            # Result: {result['message']}, Stored at: {result['minio_path']}")
        total_time += result['cost_time']
    if i != 1:
        print(f"\nTest Summary:")
        print(f"    Total files: {i}")
        print(f"    Success: {success_i}")
        print(f"    Failed: {i - success_i}")
        print(f"    Average time: {total_time / i:.2f}s")
    pass


# Automatically discover files in folder, filter for OCR-compatible ones
def _auto_discover_test_files(test_folder):
    discovered_test_files = []
    """
    for filename in file_list:
    if should_test_this_file(filename):
        file_path = os.path.join(folder_path, filename)  # Join full path
        file_description = generate_file_description(filename)
        
        test_files.append({
            "file_path": file_path,
            "expected_result": file_description
        })
    """
    return discovered_test_files


# Whether to auto-discover test files
def _get_test_files():
    if AUTO_DISCOVER == 1:
        return _auto_discover_test_files(AUTO_DISCOVER_FOLDER)
    else:
        return TEST_FILE_LIST


if __name__ == "__main__":
    print("Starting OCR automated testing...")
    print("Configuration source: test_jinhao_config.py")
    # Start testing
    test_file_list = _get_test_files()
    _multi_test(test_file_list)