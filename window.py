from testcases import Testcases
import tkinter as tk
from tkinter import *
import asyncio
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
import os
from tkinter import ttk
from settings import settings_window

background_color = '#F59C24'
approve_button_color_enable = '#5DDC49'
reject_button_color = '#EA4C1D'
review_button_color = '#FDED11'

def main() -> None:

    All_entries = Testcases(filedialog.askopenfilename())
    #All_entries = Testcases("cockpit.csv")

    root = tk.Tk()
    root.grid_rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.title("Sweetpea")
    root.geometry("450x300")

    frame_main = tk.Frame(root)
    frame_main.grid(row=0, column=0, sticky='news')
    frame_main.configure(bg=background_color)

    settings = tk.Button(frame_main, text="Settings", command = lambda: settings_window(All_entries))
    settings.grid(row=0, column=0, padx=30, pady=30)

    def import_file(All_entries):
        File_name = filedialog.askopenfilename()
        if File_name:
            All_entries = Testcases(File_name)

    upload = tk.Button(frame_main, text="Import", command = lambda All_entries: import_file(All_entries))
    upload.grid(row=0, column=1, padx=30, pady=30)


    def update_progress_bar(progress_bar, value):
        progress_bar['value'] = value
        root.update_idletasks()  # Update the UI to reflect the change

    async def gen_all(progress_bar):
        total_entries = len(All_entries.entries)
        for i, entry in enumerate(All_entries.entries):
            await entry.generate_text()
            print("Did an entry")
            entry.set_Status("Generated")
            buttons[i][1].config(text=entry.Status)  # Update the status button textGT
            buttons[i][2].config(bg="grey", state="disabled")  # Disable the 'Approve' button
            update_progress_bar(progress_bar, (i + 1) / total_entries * 100)  # Update progress bar

    generate = tk.Button(frame_main, text="Generate", command = lambda: asyncio.run(gen_all(progress_bar)))
    generate.grid(row=0, column=2, padx=30, pady=30)

    def save_csv(All_entries):
    # Define the options for the save file dialog
        options = {
            'defaultextension': '.csv',
            'filetypes': [('CSV files', '*.csv')],
            'initialdir': os.path.expanduser('~/Downloads'), # You can set this to any default directory
        }
        
        # Open the save file dialog and get the selected file name
        filename = filedialog.asksaveasfilename(**options)
        
        # Check if a file name was selected
        if filename:
            All_entries.export_all(filename)

    def check_approval_and_update_button():
        # Check if any entry has the status 'Approved'
        is_approved = any(entry.Status == "Approved" for entry in All_entries.entries)
        
        # If at least one entry is approved, enable the 'Export' button
        if is_approved:
            export.config(state="normal")
        else:
            export.config(state="disabled")


    export = tk.Button(frame_main, text="Export", command= lambda: save_csv(All_entries))
    export.grid(row=0, column=3, padx= 30, pady= 30)

    check_approval_and_update_button()

    def display_review(All_entries, i):
        text_window = Toplevel(root)
        text_window.title(All_entries.entries[i].ID)
        gen_text = Label(text_window, text= "Prompt: " + All_entries.entries[i].Requirment + "\n" + All_entries.entries[i].Response, bg=background_color, wraplength=300, justify="left")
        gen_text.grid(row=0, column=0, columnspan=3)
        buttons[i][2].config(bg=approve_button_color_enable, state= "normal")
        update_status(i, "Reviewed")
        

    def update_status(i, new_status):
        All_entries.entries[i].set_Status(new_status)
        buttons[i][1].config(text=new_status)
        check_approval_and_update_button()

    async def async_update_text(i):
        update_status(i, "Generated")
        buttons[i][2].config(bg="grey", state="disabled")  # Disable the Approve button
        await All_entries.entries[i].generate_text()



    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(frame_main)
    frame_canvas.grid(row=1, column=0, pady=(30, 0), columnspan=4, rowspan= 5)
    frame_canvas.grid_rowconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(0, weight=1)

    # Set grid_propagate to False to allow 5-by-5 buttons resizing later
    frame_canvas.grid_propagate(False)

    # Add a canvas in that frame
    canvas = tk.Canvas(frame_canvas, bg="yellow")
    canvas.grid(row=0, column=0, sticky="news")

    # Link a scrollbar to the canvas
    vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=vsb.set)

    # Create a frame to contain the buttons
    frame_buttons = tk.Frame(canvas, bg="blue")
    canvas.create_window((0, 0), window=frame_buttons, anchor='nw')


    if All_entries is None:
        rows = 5
    else:
        rows = All_entries.get_line_count()

    columns = 5

    buttons = [[tk.Button() for j in range(columns)] for i in range(rows)]


    buttons[0][0] = tk.Button(frame_buttons, text="ID")
    buttons[0][0].grid(row=0, column=0, sticky='news')

    buttons[0][1] = tk.Button(frame_buttons, text="Status")
    buttons[0][1].grid(row=0, column=1, sticky='news')

    buttons[0][2] = tk.Button(frame_buttons, text="Action")
    buttons[0][2].grid(row=0, column=2, sticky='news', columnspan=3,)


    for i in range(0, rows):
        buttons[i][0] = tk.Button(frame_buttons, text=(All_entries.entries[i].ID))
        buttons[i][0].grid(row=i + 1, column=0, sticky='news')

        buttons[i][1] = tk.Button(frame_buttons, text=(All_entries.entries[i].Status))
        buttons[i][1].grid(row=i + 1, column=1, sticky='news')

        buttons[i][2] = tk.Button(frame_buttons, text="Approve", state= "disabled", bg = "grey", command=lambda i=i: update_status(i, "Approved"))
        buttons[i][2].grid(row=i + 1, column=2, sticky='news')

        buttons[i][3] = tk.Button(frame_buttons, text=("Reject"), bg=reject_button_color, command = lambda i=i: asyncio.run(async_update_text(i)))
        buttons[i][3].grid(row=i + 1, column=3, sticky='news')

        buttons[i][4] = tk.Button(frame_buttons, text=("Review"), bg=review_button_color, command=lambda i=i: display_review(All_entries, i))
        buttons[i][4].grid(row=i + 1, column=4, sticky='news')

    # Update buttons frames idle tasks to let tkinter calculate buttons sizes
    frame_buttons.update_idletasks()

    # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
    first5columns_width = sum([buttons[0][j].winfo_width() for j in range(0, 5)])
    first5rows_height = sum([buttons[i][0].winfo_height() for i in range(0, 5)])
    frame_canvas.config(width=first5columns_width + vsb.winfo_width(),
                        height=first5rows_height)

    # Set the canvas scrolling region
    canvas.config(scrollregion=canvas.bbox("all"))

    progress_bar = ttk.Progressbar(frame_main, orient='horizontal', length=200, mode='determinate')
    progress_bar.grid(row=10, column=1, pady=10, columnspan=2)  # Adjust the position as needed

    root.mainloop()

if __name__ == "__main__":
    main()


