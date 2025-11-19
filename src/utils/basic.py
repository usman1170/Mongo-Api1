import os


def get_file_size(filepath):
    """Returns the size of a file in kilobytes"""
    size_in_bytes = os.path.getsize(filepath)
    size_in_kb = size_in_bytes / 1024
    return int(size_in_kb)

