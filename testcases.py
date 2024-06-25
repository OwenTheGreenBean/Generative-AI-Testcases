import csv
from entry import Entry
import re
import os
from tkinter import filedialog
import time

# import pyexcel.ext.xlsx # no longer required if you use pyexcel >= 0.2.2 

class TestCases:
    def __init__(self):
        self.filepath = None
        #allows for multiple instialation calls so that in the future when import works better that either more file can be uploaded,
        #or that the format is changed or user wants to remove file and retry.
        self.entries = self.initialize_entries()
        self.user = ''
        self.password = ''



# takes csv file and fills the entrys with the data if parsing happens in the future it will happen 
    def initialize_entries(self) -> list:
        """Will initialize the class with a list of entries"""
        try:
            # Assures that the imported file is of the correct format
            self.ask_for_file()
            # Makes sure the file can be opened
            if not os.path.exists(self.filepath):
                # error if it does not exist
                raise FileNotFoundError(f"File '{self.filepath}' does not exist.")
            entries = []
            with open(self.filepath, newline='') as csvfile:
                reader = csv.reader(csvfile)
                # reads eachrow in a new entry
                for row in reader:
                    if len(row) < 3 or len(row) > 3:
                        # error if the format does not match expected
                        raise ValueError(f"Invalid row format in '{self.filepath}'. Expected at least 3 columns.")
                    entry_id, description, prompt = row[:3]
                    my_entry = Entry(entry_id, description, prompt)
                    # adds the gathered data as a entry class into the testcases list
                    entries.append(my_entry)
            return entries
        except FileNotFoundError as e:
            print(f"Error: {e}")
            # fails returns empty list
            return []
        except ValueError as e:
            print(f"Error: {e}")
            # fails returns empty list
            return []
        


    def ask_for_file(self):
        """Brings up the tkinter file menu the will allow the user to select a file and then is made sure that it
        has three collums and is a CSV"""
        while True:
            self.filepath = filedialog.askopenfilename()
            if os.path.exists(self.filepath):
                try:
                    with open(self.filepath, newline='') as csvfile:
                        reader = csv.reader(csvfile)
                        for row in reader:
                            if len(row) != 3:
                                print(f"Invalid row format in '{self.filepath}'. Expected exactly 3 columns.")
                                break
                        else:
                            break  # All rows are valid, exit the loop
                except ValueError as e:
                    print(f"Error reading CSV file: {e}")
            else:
                print(f"File '{self.filepath}' does not exist. Please choose a valid file.")
        

    async def generate_all(self):
        '''#Precondtion: none
        #Postcondition: assings the entry with the text generated.'''
        for entry in self.entries:
            time.sleep(10)
            await entry.generate_text()


    def get_line_count(self):
        """Precondtion: none
        Postcondition: returns the total amount of lines in the csv file"""   
        if self.filepath:
            with open(self.filepath, newline='') as csvfile:
                return sum(1 for _ in csvfile)
        else:
            return 5
        

    def export_all(self, filename):
        '''Precondition: The function needs to have a instance of testcases class created and then the function can be calle with a string input
        Postcondition: It then returns a CSV file and XLSX file in the location of the inputed string'''
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
                    # writes to the csv file in the formate the Cockpit expects with the leading , 
                    writer.writerow(['Test Case Name','', entry.ID + entry.Requirment, "Test Case Descrition", '', entry.Description,'','','','','','',''])
                    writer.writerow(['Created By', self.user, '', 'Reviewed By', '', '', '', 'Version', '', '', '', '', ''])

                    # gets a list of all the test setup cases generated and puts them into the format the cockpit expects
                    numbered_list = extract_numbered_list_from_test_setup(entry.Response)
                    for i, item in enumerate(numbered_list, start=1):
                        if i == 1:
                            #first test setup must be written on the same line as the title others can get a new line, (cockpit format)
                            writer.writerow(['Test Setup:', str(i) + '. ' + item.strip(),'','','','','','','','','','',''])
                        else:
                            writer.writerow(['',str(i) + '. ' + item.strip(),'','','','','','','','','','',''])

                    # titles for each step in the test steps
                    writer.writerow(['Test Steps:', '', '', '', '', '', '', '', '', '', '', '', ''])
                    writer.writerow(['Step ', 'Items Tested', '', 'Action', '', 'Expected Results', '', '', 'Actual Results', '', '', 'Status', 'Recorded By'])
                    
                    pattern = r'\d+\.\s*([^\n]+)'
                    matches = re.findall(pattern, entry.Response)

                    for j, term in enumerate(matches, start=1):
                        if j == matches:
                            writer.writerow([str(j), entry.ID, '', term.strip(), '', entry.Requirment, '', '', '', '', ''])
                        else:
                            writer.writerow([str(j), entry.ID, '', term.strip(), '', '', '', '', '', '', ''])

        print(f'File {filename} has been saved successfully.')

    def set_credentials(self, user, password):
        """precondition: two strings and an already created testcases object
        postcondition: set the user password and name to the inputed strings"""
        self.user = user
        self.password = password
        print(self.user)
        print(self.password)


    def change_all_prompts(self, postfix, add):
        """#back inserts all of the prompts with a given string and removes the given string if the bool is false"""
        for entry in self.entries:
            entry.change_prompt(postfix, add)
      