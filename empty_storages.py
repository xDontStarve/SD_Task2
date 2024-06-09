import os

script_dir = os.path.dirname(os.path.realpath(__file__))

file_list = [
    os.path.join(script_dir, "storage_0"),
    os.path.join(script_dir, "storage_1"),
    os.path.join(script_dir, "storage_master")
]

def empty_files(file_list):
    for file_path in file_list:
        open(file_path, 'w').close()

empty_files(file_list)
