import uuid
import heapq
import os

def external_merge_sort(input_file, output_file, memory_limit=5242880):
    temp_files = split_and_sort_file(input_file, memory_limit)
    merge_sorted_files(temp_files, output_file)
    clean_up_temp_files(temp_files)

def split_and_sort_file(input_file, memory_limit):
    temp_files = []
    buffer = []
    buffer_size = 0
    uuid_length_with_newline = 37

    with open(input_file, 'r') as file:
        for line in file:
            buffer.append(line.strip())
            buffer_size += uuid_length_with_newline
            if buffer_size >= memory_limit:
                temp_files.append(sort_and_save(buffer))
                buffer = []
                buffer_size = 0

    if buffer:
        temp_files.append(sort_and_save(buffer))

    return temp_files

def sort_and_save(buffer):
    buffer.sort()
    temp_file_name = str(uuid.uuid4())
    with open(temp_file_name, 'w') as temp_file:
        for uuid_str in buffer:
            temp_file.write(uuid_str + '\n')
    return temp_file_name

def merge_sorted_files(temp_files, output_file):
    file_pointers = [open(file, 'r') for file in temp_files]
    with open(output_file, 'w') as out_file:
        for line in heapq.merge(*file_pointers):
            out_file.write(line)
    for fp in file_pointers:
        fp.close()

def clean_up_temp_files(temp_files):
    for file in temp_files:
        os.remove(file)

input_file = '1m.txt'
output_file = 'sorted_uuids.txt'

external_merge_sort(input_file, output_file, memory_limit=5 * 1024 * 1024)
#external_merge_sort(input_file, output_file, memory_limit=100 * 1024 * 1024)

