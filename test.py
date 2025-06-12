import csv
import os

file_path = "input.csv"
output_file_path = "input_update.csv"


grade_data_to_add_or_update = [{"Grade": "A"}, {"Grade": "B"}, {"Grade": "C"}]

new_column_to_add = "Grade"

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

# *** အပြောင်းအလဲ အပိုင်း - Address Column ကို ဖယ်ရှားပြီး Grade Column ထည့်သွင်းခြင်း ***
# လက်ရှိ fieldnames ထဲက "Address" ကို ဖယ်ရှားပါ
if "Address" in current_fieldnames:
    current_fieldnames.remove("Address")

if new_column_to_add not in current_fieldnames:
    current_fieldnames.append(new_column_to_add)
# ***************************************************************


updated_rows_for_write = []
grade_data_index = 0

for row in existing_data_rows:
    temp_row = row.copy()

    # Address column ကို temp_row ကနေ ဖယ်ရှားပါ (ရှိခဲ့ရင်)
    if "Address" in temp_row:
        del temp_row["Address"]

    if new_column_to_add not in temp_row:
        temp_row[new_column_to_add] = ""

    if not temp_row[new_column_to_add] and grade_data_index < len(
        grade_data_to_add_or_update
    ):
        temp_row[new_column_to_add] = grade_data_to_add_or_update[grade_data_index].get(
            "Grade", ""
        )
        grade_data_index += 1

    for field in current_fieldnames:
        if field not in temp_row:
            temp_row[field] = ""

    updated_rows_for_write.append(temp_row)

while grade_data_index < len(grade_data_to_add_or_update):
    new_row_dict = {}
    for field in current_fieldnames:
        if field == new_column_to_add:
            new_row_dict[field] = grade_data_to_add_or_update[grade_data_index].get(
                "Grade", ""
            )
        else:
            new_row_dict[field] = ""
    updated_rows_for_write.append(new_row_dict)
    grade_data_index += 1


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
