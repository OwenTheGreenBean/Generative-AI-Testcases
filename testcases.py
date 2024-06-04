import csv
from entry import Entry
import re

class Testcases:
    def __init__(self, filepath):
        self.filepath = filepath
        self.entries = self.initialize_entries()


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
                writer.writerow(['Test Steps:','','','','','','','','','','','\n','Step ','Items Tested','','Action','','Expected Results','','','Actual Results','','','Status','Recorded By'])

                # This pattern matches a number followed by a dot and captures all text until the next newline
                pattern = r'\d+\.\s*([^\n]+)'

                matches = re.findall(pattern, self.entries[1].Response)

                print(self.entries[1].Response)

                i = 1
                for term in matches:
                    writer.writerow([str(i), self.entries[1].ID, '', term.strip(), self.entries[1].Requirment, '', '', '', '', '', ''])
                    i += 1

                writer.writerow(['Test Case Name','',"Select Organization to begin with data upload.\n<organation selection",'Test Case Description','',
                                 self.entries[1].Description,'','','','','','','\nCreated By','','','Reviewed By','','','','Version','','','','','',])



        print(f'File {filename} has been saved successfully.')
        
        
