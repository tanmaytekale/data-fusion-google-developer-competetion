import os
import re
import csv
import gemini

def extract_amount(value):
    value = str(value)
    # Identify and replace commas with decimal points
    if ',' in value and '.' in value:
        if value.index('.') < value.index(','):
            t = value.index(',')
            value = value.replace('.', ',')      
            value = value[:t] + '.' + value[t+1:]

    # Remove all non-numeric characters except for decimal points and numbers 
    cleaned_value = re.sub(r"[^\d\-+.]", "", value)

    # Convert to float & format to two decimal points
    amount = "{:.2f}".format(float(cleaned_value))

    return amount

def format_amount(amount):
    amount_parts = amount.split('.')
    formatted_amount = '{:,}'.format(int(amount_parts[0])) + '.' + amount_parts[1]
    return formatted_amount

def process_csv_files_in_folder(upload_folder, data_folder):
    # Ensure data folder exists
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Iterate through files in the upload folder
    for filename in os.listdir(upload_folder):
        if filename.endswith(".csv"):
            input_file_path = os.path.join(upload_folder, filename)
            output_file_path = os.path.join(data_folder, f"processed_{filename}")

            with open(input_file_path, mode='r', newline='') as infile, open(output_file_path, mode='w', newline='') as outfile:
                reader = csv.reader(infile)
                writer = csv.writer(outfile)
                
                # Read the header row to get column names
                headers = next(reader)
                
                # Get the column name(s) with money from gemini.py
                money_columns = gemini.identify_money_column(headers)
                
                # Split money_columns if it's a single string with '\n' separating multiple columns
                if isinstance(money_columns, str):
                    money_columns = money_columns.split('\n')
                
                # Write headers to the output file
                writer.writerow(headers)
                
                # Process each row in the CSV file
                for row in reader:
                    for money_column_name in money_columns:
                        money_column_name = money_column_name.strip()  # Remove any leading/trailing whitespace
                        
                        if money_column_name and money_column_name in headers:
                            money_column_index = headers.index(money_column_name)
                            
                            try:
                                cleaned_amount = extract_amount(row[money_column_index])
                                formatted_amount = format_amount(cleaned_amount)
                                row[money_column_index] = formatted_amount  # Replace the original value with the formatted value
                            except (IndexError, ValueError) as e:
                                print(f"Error processing row for column '{money_column_name}' in file '{filename}': {e}")
                                continue
                            
                    writer.writerow(row)  # Write each processed row to the output file
                
                print(f"Processed file '{filename}' for column(s) {money_columns} saved to '{output_file_path}'")

# Define folders
upload_folder = "./uploads"
data_folder = "./data"

# Process all CSV files found in the upload folder
process_csv_files_in_folder(upload_folder, data_folder)
