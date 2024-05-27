import pandas as pd

file_path = 'MycroftMind_challenge_dataset.xlsx'
data_file = pd.ExcelFile(file_path)
sheet_names = list(data_file.sheet_names)

print(f'Sheet names: {sheet_names[1:]}')
for name in sheet_names:
    sheet_data = pd.read_excel(file_path, name)
    print(f'{name}\'s headers: {sheet_data.columns.to_list()}')