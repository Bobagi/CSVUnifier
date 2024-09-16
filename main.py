import pandas as pd
import os
import re

# Directory where the script is located
base_directory = os.path.dirname(os.path.abspath(__file__))

# Directory where the CSV files are (folder 'files')
csv_directory = os.path.join(base_directory, "files")

# Directory where the unified file will be saved (folder 'result')
result_directory = os.path.join(base_directory, "result")

# Create the result directory if it does not exist
os.makedirs(result_directory, exist_ok=True)

# Full path to the unified file
unified_path = os.path.join(result_directory, "unified.csv")

# Remove the target file if it already exists
if os.path.exists(unified_path):
    os.remove(unified_path)

print("Starting the process of unifying CSV files...")

# Function to extract the number from the file name
def extract_number(file_name):
    match = re.search(r"(\d+)", file_name)
    if match:
        return int(match.group(0))
    else:
        return -1 

# List of files in the directory, filtered and sorted by the number in the name
csv_files = sorted(
    [f for f in os.listdir(csv_directory) if f.endswith(".csv")],
    key=extract_number,
    reverse=True,
)

# Counter to track progress
file_counter = 0

# Iterate over all sorted files
for file in csv_files:
    file_counter += 1
    file_path = os.path.join(csv_directory, file)
    print(f"Reading file {file_counter}: {file}")

    # Read each CSV file in chunks and write to the target file
    for chunk in pd.read_csv(
        file_path, delimiter=",", chunksize=10000
    ):  # replace ',' with the correct delimiter
        print(f"Processing chunk of file {file}...")

        # Remove completely empty rows
        chunk.dropna(how="all", inplace=True)

        # Fix whitespace issues in column headers
        chunk.columns = chunk.columns.str.strip()

        # Remove extra columns that may have been created by reading errors
        chunk = chunk.loc[:, ~chunk.columns.str.contains("^Unnamed")]

        # Check if the number of columns is correct
        if file_counter == 1:
            expected_columns = chunk.columns
        else:
            if not chunk.columns.equals(expected_columns):
                print(
                    f"Attention: File {file} has inconsistent columns. Skipping this file."
                )
                continue

        # Append to avoid overwriting the previous file
        chunk.to_csv(
            unified_path,
            mode="a",
            header=not os.path.exists(unified_path),
            index=False,
        )

print(f"Processing completed! Unified file created at: {unified_path}")
