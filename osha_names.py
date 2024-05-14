import re

import pdfplumber

# Open the PDF file
with pdfplumber.open("OSHA_2021.pdf") as pdf:
    employee_data = []
    # Iterate over each page of the PDF
    pattern = r"(\d+)\s+(.*?)\s+(\d+)\s+(\d+)\s+(.*?)\s+(.*?)\s+(.*?)\s+(\d+)"

    for page in pdf.pages:
        # Extract text from the current page
        text = page.extract_text()

        # Split the text into lines and process each line
        for line in text.split('\n'):
            # Check if the line starts with a 4-digit ID followed by a space
            if re.match(r"^\d{4}\s", line):
                print("Processing line:", line)  # Debugging print statement
                # Check if the line matches the pattern
                match = re.match(pattern, line)
                if match:
                    month = match.group(3).strip()  # Remove any whitespace around the month
                    day = match.group(4).strip()    # Remove any whitespace around the day
                    # Construct the date string with the correct format
                    date_of_injury = f"{month}/{day}"
                    # Extract information from the matched groups
                    employee_name = match.group(2).replace(" Warehouse", "").replace(" Amazon", "").replace( " Fulfillment", "").replace(" FC Associate", "").replace("QC Auditor", "").replace("Yard Specialist", "").replace("Process", "")
                    employee_entry = {
                        "case_no": match.group(1),
                        "employee_name": employee_name.strip(),
                        "date_of_injury": date_of_injury,
                        "location": match.group(5),
                        "description": match.group(6),
                        "days_away": match.group(7)
                    }
                    # Append the extracted data to the list
                    employee_data.append(employee_entry)

    # Print the extracted data
    for employee in employee_data:  
        print(employee)
