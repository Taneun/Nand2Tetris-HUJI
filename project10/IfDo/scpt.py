import sys
import os
from termcolor import colored

def remove_whitespace(content):
    return ''.join(content.split())

def read_file(path):
    with open(path, 'r') as file:
        return file.read()

def compare_files(file1, file2):
    content1 = remove_whitespace(read_file(file1))
    content2 = remove_whitespace(read_file(file2))
    return content1 == content2

def process_directory(directory):
    for file in os.listdir(directory):
        if file.endswith(".xml") and os.path.isfile(os.path.join(directory, file)):
            cmp_file = f"{file}.cmp"
            cmp_file_path = os.path.join(directory, cmp_file)

            if os.path.isfile(cmp_file_path):
                file_path = os.path.join(directory, file)
                if compare_files(file_path, cmp_file_path):
                    print(colored(f"The files {file} and {cmp_file} are identical (ignoring whitespace).", "green"))
                else:
                    print(colored(f"The files {file} and {cmp_file} are different (ignoring whitespace).", "red"))
            else:
                print(colored(f"Comparison file not found for {file}", "red"))

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(colored(f"Directory not found: {directory}", "red"))
        sys.exit(1)

    process_directory(directory)

if __name__ == "__main__":
    main()
