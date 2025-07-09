import pandas as pd
import argparse
import sys

def find_duplicates(file1, file2):
    try:
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
    except Exception as e:
        print(f"Error reading files: {e}")
        sys.exit(1)

    if 'registration_num' not in df1.columns or 'registration_num' not in df2.columns:
        print("Error: Both files must contain a 'registration_num' column")
        sys.exit(1)

    # Find duplicates
    duplicates = pd.merge(df1, df2, on='registration_num', how='inner')

    if duplicates.empty:
        print("No duplicate registration_num found.")
    else:
        print(f"Found {len(duplicates)} duplicate registration_num values:")
        print(duplicates['registration_num'].unique())

        # Optional: Save to CSV
        duplicates.to_csv("duplicate_rows.csv", index=False)
        print("Saved duplicate rows to 'duplicate_rows.csv'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find duplicate registration_num rows in two CSV files")
    parser.add_argument("file1", help="Path to the first CSV file")
    parser.add_argument("file2", help="Path to the second CSV file")
    args = parser.parse_args()

    find_duplicates(args.file1, args.file2)
