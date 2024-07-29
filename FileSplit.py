import os
import pandas as pd

def split_file(input_file, delimiter, primary_key_column, n, chunksize=10000):
    # Initialize a dictionary to store file handlers
    file_handlers = {}

    try:
        # Read the input file in chunks
        for chunk in pd.read_csv(input_file, delimiter=delimiter, chunksize=chunksize):
            # Extract primary key column
            primary_key = chunk[[primary_key_column]]
            
            # Drop primary key column from the chunk
            chunk = chunk.drop(columns=[primary_key_column])
            
            # Split the remaining columns into groups of n columns
            num_files = (chunk.shape[1] + n - 1) // n  # Ceiling division

            for i in range(num_files):
                start_col = i * n
                end_col = min((i + 1) * n, chunk.shape[1])

                # Extract the columns for the current file
                sub_chunk = chunk.iloc[:, start_col:end_col]

                # Add the primary key column
                sub_chunk = pd.concat([primary_key, sub_chunk], axis=1)

                folder_name = 'FileChunks'

                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)

                # Determine the output file name
                output_file = f'FileChunks\output_file_{i+1}.csv'

                # If file handler doesn't exist, create it and write header
                if output_file not in file_handlers:
                    file_handlers[output_file] = open(output_file, 'w')
                    sub_chunk.to_csv(file_handlers[output_file], index=False, header=True)
                else:
                    sub_chunk.to_csv(file_handlers[output_file], index=False, header=False)
                
        print("Files created successfully.")

    finally:
        # Ensure all file handlers are closed
        for f in file_handlers.values():
            f.close()

# Example usage
input_file = 'InputFiles\sample1.csv'  # Replace with your input file path
delimiter = ','  # Replace with your delimiter
primary_key_column = 'OrderID'  # Replace with your primary key column name
n = 2  # Number of non-primary key columns per file

split_file(input_file, delimiter, primary_key_column, n)
