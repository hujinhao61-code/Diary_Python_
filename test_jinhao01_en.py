"""
1117 Mon - Testing objectives:
Batch processing of multiple files, different file formats, time statistics
requests library:
    requests.post(url, headers=, json=)
    response.json()
    result_data.get('minio_path', 'No path')
    response.status_code
1118 Tue
os library (local):
    os.listdir(path) - List all files and folders in a directory
    os.path.join(path1, path2) - Safely join paths
    os.path.splitext(filename) - Split filename and extension
    os.path.isdir(path) - Check if it's a directory
    os.path.isfile(path) - Check if it's a file
1119 Wed
minIO library:
    minio.Minio(): Initialize MinIO client (requires endpoint, access_key, secret_key, etc.)
    list_objects(bucket_name, prefix, recursive): List objects (files) with specified prefix in the bucket
    stat_objects(bucket_name, object_name): Get object metadata (including file size, etc.)
1121 Friday
OCR accuracy comparison,
Idea: Consider both the accuracy of text content and tolerate a certain degree of order difference
Use two metrics:
1. Bag-of-words similarity (tolerates order differences)
2. Edit distance similarity (considers order)
re library:
    re.sub(pattern, replacement, string)
"""
import time  # Required library
import requests
import os
from minio import Minio
from minio.error import S3Error
import re
# Import configuration file
from test_jinhao_config_en import (
    GLOBAL_CONFIG, TEST_FILE_LIST, TEST_URL, HEADER,
    AUTO_DISCOVER, AUTO_DISCOVER_FOLDER, MINIO_CLIENT,
    LARGE_FILE_THRESHOLD, SUPPORTED_FORMATS,
    TEXT_FORMATS, DOC_FORMATS, TABLE_FORMATS, POWERPOINT_FORMATS, IMAGE_FORMATS
)


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
    success_i = 0  # Success counter
    fail_i = 0  # Failure counter
    error_i = 0  # Error counter
    total_time = 0
    for test_file in test_file_lists:
        i += 1
        try:
            result = _test_singlefile(test_file)
            total_time += result['cost_time']
            if result['success']:
                print(f"Success | File {i}, Original path: {test_file['file_path']}, Time: {result['cost_time']}s")
                success_i += 1
                # print(f"Success | File {i}, Original path: {test_file['file_path']}, Time: {result['cost_time']}s,
                # Result: {result['message']}, Stored at: {result['minio_path']}")
            else:
                print(f"Failed~")
                fail_i += 1
                print(f"Failed | File {i}, Original path: {test_file['file_path']}, "
                      f"Time: {result['cost_time']}s, Result: {result['message']}, Stored at: {result['minio_path']}")
        except Exception as e:
            print(f"Exception | File {i}, Original path: {test_file['file_path']}, Error: {str(e)}")
            error_i += 1

    print(f"\nTest Summary:")
    print(f"    Total files: {i}")
    print(f"    Success: {success_i}")
    print(f"    Failed: {fail_i}")
    print(f"    Errors: {error_i}")
    if i > 0:
        print(f"    Average time: {total_time / i:.2f}s")
    pass


# Automatically discover files in folder, filter for OCR-compatible ones
def _auto_discover_test_files(test_folder):
    minio_client = Minio(
        endpoint=MINIO_CLIENT["endpoint"],
        access_key=MINIO_CLIENT["access_key"],
        secret_key=MINIO_CLIENT["secret_key"],
        secure=MINIO_CLIENT["secure"]
    )
    bucket_name = MINIO_CLIENT["bucket_name"]
    discovered_test_files = []
    objects = minio_client.list_objects(bucket_name, prefix=test_folder, recursive=True)
    for obj in objects:
        try:
            if obj.is_fir:  # Skip directories
                continue
            file_path = obj.object_name
            file_ext = os.path.splitext(file_path)[1].lower()  # Get extension
            # Get file size
            try:
                stat = minio_client.stat_object(bucket_name, file_path)
                file_size = stat.size
            except S3Error as e:
                print(f"Failed to get info for file {file_path}: {e.code}, skipping this file")
                continue  # Skip current file, proceed to next
            # Check if format is supported
            if file_ext in SUPPORTED_FORMATS:
                if file_ext in TEXT_FORMATS:
                    print("Text type")
                elif file_ext in DOC_FORMATS:
                    print("Document type")
                elif file_ext in TABLE_FORMATS:
                    print("Spreadsheet type")
                elif file_ext in POWERPOINT_FORMATS:
                    print("Presentation type")
                elif file_ext in IMAGE_FORMATS:
                    print("Image type")
                file_desc = f"Supported format---{file_ext[1].upper()}"
                # Check for large files
                if file_size > LARGE_FILE_THRESHOLD:
                    file_desc += "---Oversized file"
            else:
                file_desc = f"Unsupported format---{file_ext[1].upper()}"
            # Add to test list (all format)
            discovered_test_files.append({
                "file_path": file_path,
                "expected_result": file_desc
            })
        except Exception as e:
            print(f"Unknown error: {str(e)}, skipping this file")
            continue  # Continue processing next file
    return discovered_test_files


# Whether to auto-discover test files
def _get_test_files():
    if AUTO_DISCOVER == 1:
        return _auto_discover_test_files(AUTO_DISCOVER_FOLDER)
    else:
        return TEST_FILE_LIST


# Text preprocessing: Unify format for easy comparison
def preprocess_text(text):
    # Convert full-width letters/numbers to half-width
    result = []
    for char in text:
        code = ord(char)  # Get Unicode value of the character
        if (0xFF10 <= code <= 0xFF19) or (0xFF21 <= code <= 0xFF3A) or (0xFF41 <= code <= 0xFF5A):
            result.append(chr(code - 0xFEE0))  # ord and chr are inverse operations
        elif code == 0x3000:  # Full-width space
            result.append(' ')
        else:
            result.append(char)
    text = ''.join(result)  # Concatenate with empty string (direct splicing)

    # Special format: retain Chinese punctuation marks: ，。：；！？（）【】《》“”‘’%、¥
    # (depends on the company's specific OCR capabilities)
    text = re.sub(r'[~`!@#$^&*_\-+={}|\\;:"\'<>,.?/]', '', text)

    # Convert Chinese numerals (e.g., "壹贰叁") to Arabic numerals
    chinese_number = {
        '壹': '1', '贰': '2', '叁': '3', '肆': '4', '伍': '5',
        '陆': '6', '柒': '7', '捌': '8', '玖': '9', '拾': '十',
        '佰': '百', '仟': '千', '萬': '万', '億': '亿'
    }
    for cn_num, digit in chinese_number.items():
        text = text.replace(cn_num, digit)

    # Merge multiple spaces into one
    text = re.sub(r'\s+', ' ', text)  # \s+ → match "one or more consecutive whitespace characters"
    text = text.strip()  # Remove all whitespace characters from the start and end of the string
    return text


if __name__ == "__main__":
    print("Starting OCR automated testing...")
    print("Configuration source: test_jinhao_config.py")
    # Start testing
    test_file_list = _get_test_files()
    _multi_test(test_file_list)
