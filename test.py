import csv
import os

file_path = "input.csv"
output_file_path = "input_update.csv"

address_data_to_add_or_update = [{"Address": "Yangon"}, {"Address": "Mandalay"}]

new_column_to_add = "Address"

existing_data_rows = []
current_fieldnames = []

if os.path.exists(file_path):
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        current_fieldnames = list(reader.fieldnames) if reader.fieldnames else []
        for row in reader:
            existing_data_rows.append(row)
else:
    print(
        f"Error: Input file '{file_path}' not found. Please create it first (e.g., with Name,Age)."
    )
    exit()

if new_column_to_add not in current_fieldnames:
    current_fieldnames.append(new_column_to_add)

updated_rows_for_write = []
address_data_index = 0

for row in existing_data_rows:
    temp_row = row.copy()
    if new_column_to_add not in temp_row:
        temp_row[new_column_to_add] = ""

    if not temp_row[new_column_to_add] and address_data_index < len(
        address_data_to_add_or_update
    ):
        temp_row[new_column_to_add] = address_data_to_add_or_update[
            address_data_index
        ].get("Address", "")
        address_data_index += 1

    for field in current_fieldnames:
        if field not in temp_row:
            temp_row[field] = ""

    updated_rows_for_write.append(temp_row)

while address_data_index < len(address_data_to_add_or_update):
    new_row_dict = {}
    for field in current_fieldnames:
        if field == new_column_to_add:
            new_row_dict[field] = address_data_to_add_or_update[address_data_index].get(
                "Address", ""
            )
        else:
            new_row_dict[field] = ""
    updated_rows_for_write.append(new_row_dict)
    address_data_index += 1


with open(output_file_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=current_fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows_for_write)
print("Successful")
print(
    f"'{new_column_to_add}' column has been added/updated and data written to '{output_file_path}'."
)


print(f"\n--- Current content of {output_file_path} ---")
try:
    with open(output_file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
except FileNotFoundError:
    print(f"Error: {output_file_path} not found.")
print("-------------------------------------")
