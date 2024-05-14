import csv
import re

import pdfplumber

pdf_filenames = ["OSHA_2020.pdf", "OSHA_2021.pdf", "OSHA_2022.pdf", "OSHA_2023.pdf", "OSHA_2024.pdf"]

for filename in pdf_filenames:
    with pdfplumber.open(filename) as pdf:
        employee_data = []
        # Iterate over each page of the PDF
        pattern = r"(\d+)\s+(.*?)\s+(\d+)\s+(\d+)\s+(.*?)\s+(.*?)\s+(\d+)"
        for page in pdf.pages:
            # Extract text from the current page
            text = page.extract_text()

            # Split the text into lines and process each line
            for line in text.split('\n'):
                # Check if the line matches the pattern
                match = re.match(pattern, line)
                if match:
                    # Extract information from the matched groups
                    case_no = match.group(1)
                    employee_name = match.group(2).replace(" Warehouse", "").replace(" Amazon", "")
                    # Extract month and day and construct date_of_injury
                    month = match.group(3)
                    day = match.group(4)
                    date_of_injury = f"{month}/{day}"

                    # Extract location and description based on their positions in the PDF
                    location_description = match.group(5)
                    description = match.group(6)

                    # Split location and description based on known patterns
                    location_match = re.match(r"(\d+)\s+(.*?)\s+(\d+/\d+)", location_description)
                    if location_match:
                        location = location_match.group(2)
                        date_location = location_match.group(3)
                        description = date_location + " " + description
                    else:
                        location = ""
                        description = location_description + " " + description

                    employee_entry = {
                        "case_no": case_no,
                        "employee_name": employee_name.strip(),
                        "date_of_injury": date_of_injury,
                        "location": location.strip(),
                        "description": description.strip(),
                    }
                    # Append the extracted data to the list
                    employee_data.append(employee_entry)

    # Define the path for the CSV file
    csv_file_path = f"{filename.split('.')[0]}_employee_data.csv"

    # Define the fieldnames for the CSV file
    fieldnames = ["case_no", "employee_name", "date_of_injury", "location", "description"]

    # Write the extracted data to a CSV file
    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(employee_data)

    print(f"CSV file for {filename} saved successfully.")
