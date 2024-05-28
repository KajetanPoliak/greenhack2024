import pandas as pd

MERGED_DATA_PATH = 'merged_data.csv'
DATE_CN = "Timestamp"

data = pd.read_csv(MERGED_DATA_PATH)
data[DATE_CN] = pd.to_datetime(data[DATE_CN])

# Compute differences between imported and exported energy
data["import_export_diff"] = data["Imported_energy (kWh)"] - data["Exported_energy (kWh)"]

# Compute the percentage error for the energy consumption/generation plan fulfillment
data["import_fulfillment"] = (data["Imported_energy (kWh)"] - data["Predicted_Imported_energy (kWh)"]) / data["Predicted_Imported_energy (kWh)"]
data["export_fulfillment"] = (data["Exported_energy (kWh)"] - data["Predicted_Exported_energy (kWh)"]) / data["Predicted_Exported_energy (kWh)"]

# Define the flags for the energy consumption/generation plan fulfillment
# if import_export_diff positive and flexibility positive --> good
# if import_export_diff negative and flexibility negative --> good
data["import_export_diff_flag"] = ((data["import_export_diff"] >= 0) & (data["Flexibility_demand_amount [-1;1]"] > 0)) | ((data["import_export_diff"] <= 0) & (data["Flexibility_demand_amount [-1;1]"] < 0)) 

# Compute the difference between the stored energy at time t and t-1
full_battery_diff = pd.DataFrame()
for dev_id in data["DeviceID"].unique():
    dev_data = data[data["DeviceID"] == dev_id]
    stored_battery_diff = dev_data["Stored_energy (kWh)"].diff()
    stored_battery_diff = stored_battery_diff.bfill()
    stored_battery_diff = stored_battery_diff.to_frame()
    stored_battery_diff.rename(columns={'Stored_energy (kWh)': 'stored_energy_time_diff'}, inplace=True)
    stored_battery_diff['DeviceID'] = dev_id
    stored_battery_diff['Timestamp'] = dev_data["Timestamp"]
    full_battery_diff = pd.concat([full_battery_diff, stored_battery_diff], axis=0)

# Merge the stored energy difference with the main data
data = pd.merge(data, full_battery_diff, on=["DeviceID", "Timestamp"], how="left")

# Define the flags for the stored energy difference
# if stored_energy_time_diff positive and flexibility positive --> good
# if stored_energy_time_diff negative and flexibility negative --> good
data['stored_battery_time_diff_flag'] = ((data["stored_energy_time_diff"] >= 0) & (data["Flexibility_demand_amount [-1;1]"] > 0)) | ((data["stored_energy_time_diff"] <= 0) & (data["Flexibility_demand_amount [-1;1]"] < 0))


data["battery_charge"] = data["Battery_capacity (kWh)" ] / data["Stored_energy (kWh)"]

restricted_df = data[["DeviceID" ,"Timestamp", "import_export_diff","import_export_diff_flag", "import_fulfillment", "export_fulfillment", "Flexibility_demand_amount [-1;1]", "stored_energy_time_diff", "stored_battery_time_diff_flag"]]


restricted_df.to_csv("restricted_data.csv", index=False)
print(restricted_df.head())
