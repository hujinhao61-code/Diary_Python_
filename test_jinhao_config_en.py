"""
OCR Test Configuration File
Simply modify this file to use text_jinhao01.py
"""
TEST_URL = "http://0.0.0.0:9002/process"  # Test address, service endpoint process

GLOBAL_CONFIG = {
    "is_photo": 1,
    "is_ocr": 1,
    "is_table": 1,  # Table recognition (seems to have issues)
    "is_save_img": 1  # Image saving
}

# Enable automatic file discovery. If disabled, manually input test files below
AUTO_DISCOVER = 0
AUTO_DISCOVER_FOLDER = "/***"
# Modify the files to read, test file list (Ctrl+Shift+U to change case)
TEST_FILE_LIST = [
    {"file_path": "/***/new.pdf", "expected_result": "Text-only PDF"},
    {"file_path": "/***/test.jpg", "expected_result": "Image"}
    # Add more test files here
    # {"file_path": "/path/to/your/file.pdf", "expected_result": "Description"}
]

HEADER = {"Content-Type": "application/json"}  # Sending JSON format data