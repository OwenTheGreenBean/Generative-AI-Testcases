import csv
from entry import Entry
import re
import pandas as pd
from xlsxwriter.workbook import Workbook
import glob
import os

class Testcases:
    def __init__(self, filepath):
        self.filepath = filepath
        self.entries = self.initialize_entries()
        self.user = ''
        self.password = ''


    def initialize_entries(self):
        if self.filepath:
            print("Constructed")
            entries = []
            with open(self.filepath, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    entry_id, description, prompt = row[:3]  # Assuming the first 3 columns contain relevant data
                    my_entry = Entry(entry_id, description, prompt)
                    entries.append(my_entry)
            return entries

    async def generate_all(self):
        for entry in self.entries:
            await entry.generate_text()

    
    def get_line_count(self):
        if self.filepath:
            with open(self.filepath, newline='') as csvfile:
                return sum(1 for _ in csvfile)
        else:
            return 5
        

        

        
    def export_all(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for i, entry in enumerate(self.entries):
                if entry.Status == "Approved":


                    def extract_numbered_list_from_test_setup(input_text):
                        # Find the "Test Setup" section
                        test_setup_start = input_text.find("Test Setup:")
                        if test_setup_start == -1:
                            print("Error: 'Test Setup:' section not found.")
                            return []

                        # Find the "Test Steps" section
                        test_steps_start = input_text.find("Test Steps:")
                        if test_steps_start == -1:
                            print("Error: 'Test Steps:' section not found.")
                            return []

                        # Extract the content between "Test Setup" and "Test Steps"
                        setup_content = input_text[test_setup_start + len("Test Setup:"):test_steps_start].strip()

                        # Extract numbered list items
                        pattern = r"\d+\.\s*([^\n]+)"
                        matches = re.findall(pattern, setup_content)

                        return matches

                    writer.writerow(['Test Case Name','', entry.ID + entry.Requirment, "Test Case Descrition", '', entry.Description,'','','','','','',''])
                    writer.writerow(['Created By', self.user, '', 'Reviewed By', '', '', '', 'Version', '', '', '', '', ''])

                    numbered_list = extract_numbered_list_from_test_setup(entry.Response)
                    for i, item in enumerate(numbered_list, start=1):
                        if i == 1:
                            writer.writerow(['Test Setup:', str(i) + '. ' + item.strip(),'','','','','','','','','','',''])
                        else:
                            writer.writerow(['',str(i) + '. ' + item.strip(),'','','','','','','','','','',''])


                    writer.writerow(['Test Steps:', '', '', '', '', '', '', '', '', '', '', '', ''])
                    writer.writerow(['Step ', 'Items Tested', '', 'Action', '', 'Expected Results', '', '', 'Actual Results', '', '', 'Status', 'Recorded By'])
                    
                    pattern = r'\d+\.\s*([^\n]+)'
                    matches = re.findall(pattern, entry.Response)

                    for j, term in enumerate(matches, start=1):
                        if j == matches:
                            writer.writerow([str(j), entry.ID, '', term.strip(), '', entry.Requirment, '', '', '', '', ''])
                        else:
                            writer.writerow([str(j), entry.ID, '', term.strip(), '', '', '', '', '', '', ''])

                
    # Convert CSV files to XLSX
        #for csvfile in glob.glob(os.path.join('.', filename)):
            #output_filename = csvfile[:-4] + '.xlsx'
            #df = pd.read_csv(csvfile)
            #df.to_excel(output_filename, sheet_name="Export", index=False)
            #print(f'File {output_filename} has been saved successfully.')
    

    def set_credentials(self, user, password):
        self.user = user
        self.password = password
        print(self.user)
        print(self.password)
        