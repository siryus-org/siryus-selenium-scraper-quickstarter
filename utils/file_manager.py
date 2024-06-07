import logging
import os
import re

def clear_directory(directory):
    # Check if the directory exists
    if os.path.exists(directory):
        # Iterate over files in directory
        for file_name in os.listdir(directory):
            # Create the full path to the file
            file_path = os.path.join(directory, file_name)
            try:
                # Check if the item is a file
                if os.path.isfile(file_path):
                    # Delete the file
                    os.remove(file_path)
                # If it is a directory, recursively delete its contents
                elif os.path.isdir(file_path):
                    clear_directory(file_path)
            except Exception as e:
                logging.info(f"Could not delete {file_path}: {e}")
    else:
        logging.info(f"The directory {directory} does not exist")


def create_download_directory(directory_name):

    # Creates a directory for downloading files within the current working directory.

    # Args:
    #     directory_name (str): Name of the directory to be created.

    current_directory = os.getcwd()
    download_dir = os.path.join(current_directory, directory_name)
    os.makedirs(download_dir, exist_ok=True)
    return download_dir


def clean_filename(filename):
    # Defines a regular expression that matches any character that is not a letter, number, space, or underscore
    invalid_chars_regex = r'[^\w\s-]'
    # Replaces invalid characters with an empty string
    cleaned_filename = re.sub(invalid_chars_regex, '', filename)
    return cleaned_filename
