import csv
import os

input_csv_file = "input.csv"
output_csv_file = "output.csv"

export_data = [
    {"Name": "Aung Aung", "Age": "30", "City": "Yangon"},
    {"Name": "Mya Mya", "Age": "25", "City": "Mandalay"},
    {"Name": "Kyaw Kyaw", "Age": "35", "City": "Nay Pyi Taw"},
]

export_fieldnames = ["Name", "Age", "City"]

print(f"Exporting data to '{output_csv_file}'...")

try:
    with open(output_csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=export_fieldnames)

        writer.writeheader()

        writer.writerows(export_data)

    print(f"Data successfully exported to '{output_csv_file}'.")

except IOError as e:
    print(f"Error writing to file '{output_csv_file}': {e}")
except Exception as e:
    print(f"An unexpected error occurred during export: {e}")

print(f"\nImporting data from '{output_csv_file}'...")

imported_data = []

if os.path.exists(input_csv_file):
    try:
        with open(input_csv_file, "r", newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            print(f"File Headers: {reader.fieldnames}")

            for row in reader:
                imported_data.append(row)

        print(f"Data successfully imported from '{input_csv_file}'.")
        print("\n--- Imported Data ---")
        for row in imported_data:
            print(row)
        print("---------------------\n")

    except FileNotFoundError:
        print(f"Error: Input file '{output_csv_file}' not found.")
    except IOError as e:
        print(f"Error reading from file '{output_csv_file}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred during import: {e}")
else:
    print(
        f"Error: Output file '{output_csv_file}' does not exist to import from. Please run the export section first."
    )
