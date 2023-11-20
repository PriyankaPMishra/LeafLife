import pandas as pd

# Read the CSV file into a DataFrame
disease_info = pd.read_csv('disease_info.csv', encoding='cp1252')

# Display the first few rows of the DataFrame to verify the data is read correctly
print(disease_info.head())

# Accessing the cell values in the DataFrame
row_index = 0  # The index you want to access

# Accessing specific cells based on index and column names
index_value = disease_info.loc[row_index, 'index']
disease_name = disease_info.loc[row_index, 'disease_name']
description = disease_info.loc[row_index, 'description']

# Displaying the retrieved values
print("Index:", index_value)
print("Disease Name:", disease_name)
print("Description:", description)
