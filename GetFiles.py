import os
import glob

def get_files_from_folder(folder_path, file_extension='*'):
    # Get a list of all files in the folder with the specified extension
    search_pattern = os.path.join(folder_path, f'*.{file_extension}')
    files = glob.glob(search_pattern)
    
    # Extract the file names from the file paths
    file_names = [os.path.basename(file_path) for file_path in files]
    
    return file_names

# Example usage
folder_path = 'InputFiles'  # Replace with the path to your folder
file_extension = '*'  # Replace with the desired file extension or '*' for all files
file_names = get_files_from_folder(folder_path, file_extension)

for file_name in file_names:
    print(file_name)
