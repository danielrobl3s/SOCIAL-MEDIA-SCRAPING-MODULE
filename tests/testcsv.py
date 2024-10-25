import csv

# Sample data for a single column
column_data = ["Data1", "Data2", "Data3", "Data4", "Data5"]

# Define the fieldnames (column names)
fieldnames = ["Column1"]

# Specify the filename
filename = "column_data.csv"

# Write data to the CSV file
with open(filename, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write the header (field names)
    writer.writeheader()

    # Write the data in the specified column
    for data in column_data:
        writer.writerow({"Column1": data})

print("Data has been written to", filename)
