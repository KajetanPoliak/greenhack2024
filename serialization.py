import pandas as pd

file_path = 'MycroftMind_challenge_dataset.xlsx'
data_file = pd.ExcelFile(file_path)
sheet_names = list(data_file.sheet_names)[1:]

print(f'Sheet names: {sheet_names}')
for name in sheet_names:
    sheet_data = pd.read_excel(file_path, name)
    print(f'{name}\'s headers: {sheet_data.columns.to_list()}')

merged_data = pd.read_excel(file_path, sheet_names[0]) #Imported and exported Energy
next_data = pd.read_excel(file_path, sheet_names[1]) #Predicted energy
merged_data = pd.merge(merged_data, next_data, on=['DeviceID', 'Timestamp'])
next_data = pd.read_excel(file_path, sheet_names[2]) #Flexibility
merged_data = pd.merge(merged_data, next_data, on=['DeviceID', 'Timestamp'])
next_data = pd.read_excel(file_path, sheet_names[3]) #Battery
merged_data = pd.merge(merged_data, next_data, on=['DeviceID', 'Timestamp'])
next_data = pd.read_excel(file_path, sheet_names[4]) #Battery params 
merged_data = pd.merge(merged_data, next_data, on=['DeviceID'], how='left')
next_data = pd.read_excel(file_path, sheet_names[5]) #Weather
merged_data = pd.merge(merged_data, next_data, on=['Timestamp'], how='left')
next_data = pd.read_excel(file_path, sheet_names[6]) #Market prices
merged_data = pd.merge(merged_data, next_data, on=['Timestamp'], how='left')

print("Merged DataFrame:")
print(merged_data.head())