# CSV File Unifier

This application consolidates multiple CSV files into a single unified file using Python and the pandas library. It's designed to handle large datasets efficiently by processing files in chunks. The unified file uses tabulation as the delimiter for compatibility with systems requiring this format.

## Features

- **Directory Sorting**: Processes files in a specified directory and automatically sorts them numerically based on numbers in their filenames.
- **Chunk Processing**: Reads and writes large files in manageable chunks to minimize memory usage.
- **Column Consistency Check**: Ensures all files have consistent column headers before appending to the unified file.
- **Whitespace Correction**: Automatically trims any leading or trailing whitespace from column headers.

## Prerequisites

Before you start using this application, ensure you have the following installed:
- Python 3.6 or higher
- pandas library

You can install pandas using pip if you don't have it already:

```bash
pip install pandas
```

## Usage

1. **Prepare Your Files**: Place all the CSV files you want to unify in the `files` directory located in the same directory as the script. These files should be tab-delimited CSV files (or adjust the delimiter in the script as needed).

2. **Run the Script**: Execute the script by running the following command in the terminal:

```bash
python unify_csv.py
```

3. **Check the Output**: The unified file will be saved in the `result` directory as `unified.csv`. This file will contain all the data from the input files consolidated into one, separated by tabs.

## Configuration

- **Input Directory**: Default is `./files`. You can change this by modifying the `csv_directory` path in the script.
- **Output Directory**: Default is `./result`. Modify the `result_directory` path to change the output location.
- **Delimiter**: The default set for reading and writing is tab (`'	'`). Change the `delimiter` parameter in the `pd.read_csv()` and `to_csv()` functions if your files use a different delimiter.

## Troubleshooting

- **Column Inconsistencies**: If the script skips files, it might be due to inconsistent columns. Check your CSV files for matching header rows.
- **Memory Issues**: If running into memory issues, try reducing the `chunksize` in the `pd.read_csv()` function call.

## Contributing

Feel free to fork this project and submit pull requests. You can also open an issue if you find bugs or have feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For support or to contact the maintainer, please reach out via GitHub.
