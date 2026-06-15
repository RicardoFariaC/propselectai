import pandas as pd
import os

path = '../../data/planilhas'
for file in os.listdir(path):
    if file.endswith('.xlsx'):
        file_path = os.path.join(path, file)
        print(f"\n{'='*40}\nFile: {file}\n{'='*40}")
        try:
            xl = pd.ExcelFile(file_path)
            for sheet in xl.sheet_names:
                df = xl.parse(sheet, nrows=5)
                print(f"\n--- Sheet: {sheet} ---")
                print(f"Columns: {list(df.columns)}")
                print(df.head(2))
        except Exception as e:
            print(f"Error reading {file}: {e}")
