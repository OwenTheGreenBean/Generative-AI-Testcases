from testcases import Testcases
import tkinter as tk
from tkinter import *


def settings_window(All_entries):

    def setcreds(in_user, in_password):
        print("Username:", in_user.get())
        print("Password:", in_password.get())
        All_entries.set_credentials(in_user.get(), in_password.get())

    priority_map = {
        10: (False, ', "Test Setup in number: "'),
        9: (False, ', "Test Steps in number: "'),
    }




    

    text_window = tk.Toplevel()
    text_window.title("Settings")
    text_window.geometry('280x300')
    text_window.configure(bg='orange')  # Set the background color to orange

    # Create and place the username label and entry
    username_label = tk.Label(text_window, text="User: ")
    username_label.grid(row=0, column=0, padx=10, pady=10)


    user = StringVar()
    username_entry = tk.Entry(text_window, textvariable=user)
    username_entry.grid(row=0, column=1, padx=10, pady=10)
        
    # Create and place the password label and entry
    password_label = tk.Label(text_window, text="Password:")
    password_label.grid(row=1, column=0, padx=10, pady=10)

    password = StringVar()
    password_entry = tk.Entry(text_window, textvariable=password)
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    # Login button
    loginButton = tk.Button(text_window, text="Login: ", command=lambda: setcreds(user, password))
    loginButton.grid(row=2, column=0, pady = 10, columnspan=2)  



    password_label = tk.Label(text_window, text="Generation Prompt Settings")
    password_label.grid(row=3, column=0, pady=10, columnspan=2)


    checkbutton_steps_state = tk.IntVar()
    checkbutton_setup_state = tk.IntVar()

    checkbutton_setup = tk.Checkbutton(text_window, text="Test Setup", variable=checkbutton_setup_state)
    checkbutton_setup.grid(row=4, column=0, padx=10, pady=2)

    checkbutton_steps = tk.Checkbutton(text_window, text="Test Steps", variable=checkbutton_steps_state)
    checkbutton_steps.grid(row=4, column=1, padx=10, pady=2)

    def update_prompt(priority_map, checkbutton_setup_state, checkbutton_steps_state):
        priority_map[10] = (checkbutton_setup_state, priority_map[10][1])
        priority_map[9] = (checkbutton_steps_state, priority_map[9][1])
        postfix = ''

        for boolean, (priority, description) in priority_map.items():
            if boolean:
                postfix += description  # Append the description string
                print(description)

        print(postfix)

        All_entries.change_all_prompts(postfix, 1)
        

    loginButton = tk.Button(text_window, text="Apply Settings", command=lambda: update_prompt(priority_map, checkbutton_setup_state, checkbutton_steps_state))
    loginButton.grid(row=5, column=0, pady = 10, columnspan=2)  
   
