import os
import shutil


source_dir = r"D:\OK"
# Traverse through the folder and its subfolders
for root, dirts, files in os.walk(source_dir):
    # Iterate over all files in the current folder
    for filename in files:
        # Concatenate the path to get the full path of the file (folder + filename）
        file_full_path = os.path.join(root, filename)
        # Calculate the relative path: the path of the current folder (root) relative to the source folder (source_dir)
        # For example, if the source folder is A and the current folder is A/B/C, the relative path will be B/C
        relative_folder = os.path.relpath(root, source_dir)
        # Split the filenam and extension using os.path.splitext(), [1]gets the extension part, lower() converts to lowercase (for uniform format)
        # For example, "test.XLSX" will become ".xlsx"
        file_ext = os.path.splitext(filename)[1].lower()
        # Check if the file extension is of Excel format
        if file_ext in [".xls", ".xlsx"]:
            # Concatenate the target folder path: "Excel File" folder under the source folder
            target_type_folder = os.path.join(source_dir, "Excel Flie")
        # Check if it's of Word format
        elif file_ext in [".doc", "docx"]:
            target_type_folder = os.path.join(source_dir, "Word File")
        elif file_ext == ".pdf":
            target_type_folder = os.path.join(source_dir, "PDF File")
        # For files not in the above formats, skip the current loop (do not process)
        else:
            continue # Skip other types of files
        # Concatenate the final target folder path: type folder + original relative path (to maintain the folder structure)
        target_folder = os.path.join(target_type_folder, relative_folder)
        # Create the target folder (if it doesn't exist) using os.makedirs()
        # exist_ok=True means no error will be reported if the folder already exists
        os.makedirs(target_folder, exist_ok=True)
        # Concatenate the full path of the target file (target folder + filename)
        target_file_path = os.path.join(target_folder, filename)
        # Copy the file using shutil.copy2(): copy from the source path (file_full_path) to the target path (target_file_path)
        # It will preserve the file's metadate (such as creation time, modification time, etc.)
        shutil.copy2(file_full_path, target_file_path)
        # This line is code for printing copy information, currently commented out
        # print(f"Copied: {file_full_path} -> {target_file_path}")
    # Print a prompt message after all files are processed
    print("All files have been classified and copied, and the original folder structure has benn preserved")