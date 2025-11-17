"""1117 Mon Test Objectives:
Batch processing of multiple files, different file formats, time statistics
"""
import time  # Required library
import requests


# First define single file test
def test_singlefile(test_file):
    print(f"Starting test for file: {test_file['file_path']}")
    start_time = time.time()
    if test_file != None:
        request_config = {
            "file_path": test_file['file_path'],
            "is_photo": 1,
            "is_ocr": 1,
            "is_table": 1,
            "is_save_img": 1
        }
    else:
        request_config = json_config
    response = requests.post(test_url, headers=header, json=request_config)
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
def multi_test(test_file_list):
    i = 0
    success_i = 0
    total_time = 0
    for test_file in test_file_list:
        i += 1
        result = test_singlefile(test_file)
        if result['success']:
            print(f"Success | File {i}, Original path:{test_file['file_path']}, Time used:{result['cost_time']} seconds")
            success_i += 1
            # print(f"Success | File {i}, Original path:{test_file['file_path']}, Time used:{result['cost_time']} seconds, Result:{result['message']}, Stored at:{result['minio_path']}")
        else:
            print(f"Failed~")
            # print(f"Failed | File {i}, Original path:{test_file['file_path']}, Time used:{result['cost_time']} seconds, Result:{result['message']}, Stored at:{result['minio_path']}")
        total_time += result['cost_time']
    if i != 1:
        print(f"\nTest Summary:")
        print(f"    Total files: {i}")
        print(f"    Success: {success_i}")
        print(f"    Failed: {i - success_i}")
        print(f"    Average time: {total_time / i:.2f} seconds")
    pass


if __name__ == "__main__":
    # Define test configuration
    test_url = "http://0.0.0.0:9002/process"  # Test address, service function process
    test_file_list = [
        {"file_path": "/***/new.pdf", "expected_result": "Plain text PDF"},  # Test file list
        {"file_path": "/***/test.jpg", "expected_result": "Image"}
    ]
    header = {"Content-Type": "application/json"}  # Sending JSON format data
    json_config = {
        "file_path": "/***/new.pdf",
        "is_photo": 1,
        "is_ocr": 1,
        "is_table": 1,
        "is_save_img": 1
    }
    # Start testing
    multi_test(test_file_list)