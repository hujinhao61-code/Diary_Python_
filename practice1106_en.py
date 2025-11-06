# 1106 Thu start
import os
import logging
from matplotlib import pyplot as plt
from datetime import datetime

# Ensure log directory exists
LOG_DIR = "log"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging
log_file = os.path.join(LOG_DIR, f"folder_size_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(message)s",
    handlers = [
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)


def _get_folder_size(folder_path):
    total_size = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.exists(file_path):
                total_size += os.path.getsize(file_path)
    return total_size


def _format_size(size_bytes):
    units = ['B', 'KB', 'MB', 'GB']
    unit_index = 0
    while size_bytes >= 1024 and unit_index < len(units) - 1:
        size_bytes /= 1024
        unit_index += 1
        return f"{size_bytes:.2f} {units[unit_index]}"

# Key words:
# while size_bytes >= 1024 and unit_index < len(units) - 1:
#     size_bytes /= 1024
#     unit_index += 1
#     return f"{size_bytes:.2f} {units[unit_index]}"
# if not os.path.exists(LOG_DIR):
#     os.makedirs(LOG_DIR)
# (so many is important, because i first use os, (^///^))
