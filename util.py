import os


def get_absolute_path_of_file_parent_directory(file_name: str) -> str:
    return os.sep.join(__file__.split(os.sep)[:-1])
