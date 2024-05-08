import tkinter as tk
from tkinter import font as tkfont
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
import os
from PIL import Image, ImageTk
import numpy as np
from datetime import datetime
import csv
import shutil
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from itertools import cycle

# pass
current_pass = "5801"
# random number from 1000 to 9999
bypass_code = "1126"


class CheckImage(tk.Canvas):
    def __init__(self, parent, name, image_path, value=0, *args, **kwargs):
        super().__init__(parent, width=100, height=100, bd=0, highlightthickness=0, *args, **kwargs)
        self.name = name
        self.value = value
        self.checked = tk.BooleanVar(value=bool(value))
        img = Image.open(image_path).resize((100, 90))
        self.image = ImageTk.PhotoImage(img)
        self.create_image(52, 40, image=self.image, anchor='center')
        self.create_text(50, 94, text=name, font=('Arial', 12))
        self.config(highlightbackground='white', highlightthickness=2)
        self.bind("<Button-1>", self.toggle)

    def toggle(self, event=None):
        self.checked.set(not self.checked.get())
        if self.checked.get():
            self.create_image(52, 40, image=self.image, anchor='center')
            self.config(highlightbackground='blue', highlightthickness=2)
            self.value = 1
        else:
            self.create_image(52, 40, image=self.image, anchor='center')
            self.config(highlightbackground='white', highlightthickness=2)
            self.value = 0

    def get(self):
        return self.value



class App(tk.Tk):

    # vars
    container = None

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='arial', size=40, weight="bold")
        self.title("Ridgewood Checkin")
        self.minsize(860, 480)
        self.resizable(False, False)

        # the container is where we'll stack a bunch of frames
        App.container = tk.Frame(self)
        App.container.pack(side="top", fill="both", expand=True)
        App.container.grid_rowconfigure(0, weight=1)
        App.container.grid_columnconfigure(0, weight=1)

        self.show_frame(StartPage).tkraise()
        self.check_log_file()
        # update guests list
        StartPage.update_guests()

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = page_name(parent=App.container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        return frame
    
    def check_log_file(self):
        # if log file with current date does not exist, create it
        if not os.path.exists("logs/members/" + datetime.now().strftime("%m-%d-%Y") + ".csv"):
            with open("logs/members/" + datetime.now().strftime("%m-%d-%Y") + ".csv", "w") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Time", "Member ID", "Name"])
                print("Created log file for " + datetime.now().strftime("%m-%d-%Y") + ".csv")



class StartPage(tk.Frame):

    # auth
    auth = False
    # vars
    mem_num = ""
    name = ""
    member_exists = False
    current_guests = []

    def update_guests():
        # add all guest names to array
        StartPage.current_guests = []
        with open('logs/guests/guests.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                StartPage.current_guests.append(row[1] + " " + row[2])
        print(StartPage.current_guests)
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        error = tk.Label(self, text="Please enter a valid ID or last name.", font=("Arial", 20))

        def search():
            # check for bypass code
            if search_info.get() == bypass_code:
                error.config(text="Manager bypass, please allow access to this member.", fg="green")
                error.place(x=50, y=265)
                search_info.delete(0, END)
            else:
                # if search info is number
                if search_info.get().isdigit():
                    StartPage.mem_num = search_info.get()
                    StartPage.name = ""
                else:
                    StartPage.name = search_info.get()
                    StartPage.mem_num = ""

                mem_num = StartPage.mem_num
                name = StartPage.name

                # remove spaces from mem_num and name
                mem_num = mem_num.replace(" ", "")
                name = name.replace(" ", "")

                # check if id is number less than 5 digits
                if mem_num.isdigit() and len(mem_num) < 4:
                    # search for id
                    if error.winfo_exists():
                        error.config(text="")
                    
                    # check if mem_num is in list of image filenames
                    for filename in os.listdir("images"):
                        filename = filename.split("_")
                        if filename[0] == str(int(mem_num)):
                            print("Member " + mem_num + " exists.")
                            StartPage.member_exists = True
                            frame = controller.show_frame(MemberLookup)
                            frame.tkraise()
                            break
                        else:
                            StartPage.member_exists = False
                            # display error on window
                            error.config(text="Member " + mem_num + " does not exist.", fg="red")
                            error.place(x=50, y=265)

                    search_info.delete(0, END)
                    search_info.focus()
                # if last name is not empty
                elif name != "":
                    # search for last name
                    if error.winfo_exists():
                        error.config(text="")
                    
                    # check if name is in list of image filenames
                    for filename in os.listdir("images"):
                        if name.lower() in filename.lower():
                            frame = controller.show_frame(MemberLookup)
                            frame.tkraise()
                            break
                        else:
                            StartPage.member_exists = False
                            # display error on window
                            error.config(text="Member " + name + " does not exist.", fg="red")
                            error.place(x=50, y=265)

                    search_info.delete(0, END)
                    search_info.focus()
                # if both are empty
                else:
                    # display error on window
                    error.config(text="Please enter a valid ID or last name.", fg="red")
                    error.place(x=50, y=265)

        def not_auth():
            StartPage.auth = False
            controller.show_frame(StartPage)

        # ridgewood logo
        logo = tk.PhotoImage(file="bin/ridgewood_logo.png")
        logo_label = tk.Label(self, image=logo)
        logo_label.image = logo
        logo_label.pack(pady=(20,0))
        
        # text description
        description = tk.Label(self, text="Enter the member's ID or last name to search for them.", font=("Arial", 20))
        description.pack(pady=0)

        # label for user id on the top left
        search_label = tk.Label(self, text="Member Info:", font=("Arial", 20))
        search_label.place(x=150, y=210)
        # text box for user id
        search_info = tk.Entry(self, width=15, font=("Arial", 20))
        search_info.place(x=340, y=210)
        search_info.focus()

        # search button under to search for user
        search_button = tk.Button(self, text="Search", font=("Arial", 20), command=search)
        controller.bind("<Return>", lambda event: search())
        search_button.place(x=590, y=200)

        # auth button
        if not StartPage.auth:
            auth_button = tk.Button(self, text="Admin", font=("Arial", 20), width=6, command=lambda: controller.show_frame(auth_check))
            auth_button.place(x=50, y=360)
        else:
            auth_button = tk.Button(self, text="Logout", font=("Arial", 20), width=6, command=not_auth)
            auth_button.place(x=50, y=360)

        # add guest button
        add_guest_button = tk.Button(self, text="Add Guest", font=("Arial", 20), command=lambda: controller.show_frame(AddGuest))
        add_guest_button.place(x=165, y=360)

        # add member button to right of search button
        if StartPage.auth:
            add_member_button = tk.Button(self, text="Add Member", font=("Arial", 20), width=11, command=lambda: controller.show_frame(AddMember))
            add_member_button.place(x=325, y=360)
            # delete member button to right of search button
            delete_member_button = tk.Button(self, text="Delete Member", font=("Arial", 20), width=12, command=lambda: controller.show_frame(DeleteMember))
            delete_member_button.place(x=520, y=360)
            stats_button = tk.Button(self, text="Stats", font=("Arial", 20), command=lambda: controller.show_frame(Stats))
            stats_button.place(x=730, y=360)
            # show bypass code
            bypass_code_label = tk.Label(self, text="Bypass Code: " + bypass_code, font=("Arial", 20))
            bypass_code_label.place(x=50, y=425)



class MemberLookup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        guests = []
        already_logged_list = []

        # guest notice
        def popup_notice(event):
            win = tk.Toplevel()
            win.wm_title("Notice")
            win.minsize(250, 150)
            win.resizable(False, False)

            # done
            def done(admin=False, guest="", event=""):
                if admin:
                    if guest != "":
                        guests.append(guest)
                        # dispay guest added label
                        guest_error.config(text="+ Guest added.", fg="green")
                        guest_error.place(x=425, y=375)
                        print("guest added to list")
                    elif event == "no_member" or event == "already_logged":
                        now = datetime.now()
                        date = now.strftime("%m/%d/%Y")
                        # log guest
                        if guests:
                            for guest in guests:
                                # find guest in csv file
                                with open('logs/guests/guests.csv', 'r') as file:
                                    reader = csv.reader(file)
                                    for row in reader:
                                        if row == guest:
                                            num_of_visits = int(guest[8]) + 1
                                            new_row = [date, guest[1], guest[2], guest[3], guest[4], guest[5], guest[6], guest[7], num_of_visits]
                                            # replace old row with new row
                                            with open('logs/guests/guests.csv', 'r') as file:
                                                reader = csv.reader(file)
                                                lines = list(reader)
                                                for line in lines:
                                                    if line == guest:
                                                        lines[lines.index(line)] = new_row
                                            # write new row to csv file
                                            with open('logs/guests/guests.csv', 'w', newline='') as file:
                                                writer = csv.writer(file)
                                                writer.writerows(lines)
                                                print("guest logged")
                            guest_cost_amount()
                        else:
                            controller.show_frame(StartPage)
                # show main page
                win.destroy()
            # admin password check
            def pass_check(password, guest="", event=""):
                if password == current_pass:
                    done(admin=True, guest=guest, event=event)
            # override
            def override(guest="", event=""):
                # clear window
                for widget in win.winfo_children():
                    widget.destroy()

                if StartPage.auth:
                    pass_check(current_pass, guest=guest, event=event)
                else:
                    # admin header
                    l = tk.Label(win, text="Override", font=controller.title_font)
                    l.pack()
                    # admin password
                    l = tk.Label(win, text="Admin password:")
                    l.place(x=25, y=64)
                    # admin password entry
                    admin_pass = ttk.Entry(win, width=5, font=("Arial", 20))
                    admin_pass.place(x=140, y=60)
                    admin_pass.focus()
                    # admin password submit button
                    admin_button = ttk.Button(win, text="Submit", command=lambda: pass_check(admin_pass.get(), guest=guest, event=event))
                    win.bind("<Return>", lambda e: pass_check(admin_pass.get(), guest=guest, event=event))
                    admin_button.place(x=125, y=115)
                    # close button
                    close_button = ttk.Button(win, text="Close", command=win.destroy)
                    close_button.place(x=25, y=115)

            # header
            if event == "guest_limit_warning":
                l = tk.Label(win, text="Warning", fg="yellow", font=controller.title_font)
                l.pack()
            else:
                l = tk.Label(win, text="Error", fg='red', font=controller.title_font)
                l.pack()

            # warning message
            if event == "limit_exceeded":
                guests_num_of_visits = 0
                guest_name = guest_entry.get().split(" ")
                for guest in guests:
                    if guest[1] == guest_name[0] and guest[2] == guest_name[1]:
                        guests_num_of_visits = guest[8]
                        temp_guest = guest
                        guests.pop(guests.index(guest))
                l = tk.Label(win, text="Guest limit exceeded.\nThis guest, " + guest_entry.get() + ", has\ncome " + str(guests_num_of_visits) + " times.")
                l.pack()
                # override button
                b = ttk.Button(win, text="Override", command=lambda: override(guest=temp_guest))
                b.place(x=125, y=115)
            elif event == "no_member":
                l = tk.Label(win, text="You must select a member to continue.")
                l.pack()
                # override button
                b = ttk.Button(win, text="Override", command=lambda: override(event="no_member"))
                b.place(x=125, y=115)
            elif event == "already_logged":
                l = tk.Label(win, text="Member(s) already logged.\nTo log guest, you must\noverride.")
                l.pack(pady=0)
                # override button
                b = ttk.Button(win, text="Override", command=lambda: override(event="already_logged"))
                b.place(x=125, y=115)
            elif event == "guest_already_logged":
                l = tk.Label(win, text="Guest already logged.")
                l.pack()
                # override button
                b = ttk.Button(win, text="Cancel", command=lambda: controller.show_frame(StartPage))
                b.place(x=125, y=115)
            elif event == "guest_limit_warning":
                l = tk.Label(win, text="Guest limit reached.\nThis is the last time\nthis guest can come.")
                l.pack()
            # okay button
            if event == "guest_limit_warning":
                b = ttk.Button(win, text="Okay", command=lambda: [win.destroy(), guest_error.config(text="+ Guest added.", fg="green"), guest_error.place(x=425, y=375)])
                win.bind("<Return>", lambda e: [win.destroy(), guest_error.config(text="+ Guest added.", fg="green"), guest_error.place(x=425, y=375)])
                b.place(x=75, y=115)
            else:
                b = ttk.Button(win, text="Okay", command=win.destroy)
                win.bind("<Return>", lambda e: win.destroy())
                b.place(x=25, y=115)
        # find guest in csv file
        def findGuest():
            # look in guest.csv for first and last name
            with open('logs/guests/guests.csv', 'r') as file:
                reader = csv.reader(file)
                guest_name = guest_entry.get().split(" ")
                for row in reader:
                    if row[1].lower() == guest_name[0].lower() and row[2].lower() == guest_name[1].lower():
                        if row[0] == datetime.now().strftime("%m/%d/%Y"):
                            popup_notice("guest_already_logged")
                            return
                        else:
                            if int(row[8]) >= 5:
                                guests.append(row)
                                popup_notice("limit_exceeded")
                            elif int(row[8]) == 4:
                                guests.append(row)
                                popup_notice("guest_limit_warning")
                            else:
                                guest_error.config(text="+ Guest added.", fg="green")
                                guest_error.place(x=535, y=445)
                                guests.append(row)
                            return
                # if guest is not found, display error
                guest_error.config(text="Guest not found.", fg="red")
                guest_error.place(x=535, y=445)
        # pass back to Lookup
        def pass_to_lookup(num):
            StartPage.mem_num = num
            StartPage.member_exists = True
            frame = controller.show_frame(MemberLookup)
            frame.tkraise()
        # log member to csv file
        def logMember(num):
            # get current date and time
            now = datetime.now()
            date = now.strftime("%m/%d/%Y")
            time = now.strftime("%H:%M:%S")

            # open csv file
            logged = False
            with open("logs/members/" + datetime.now().strftime("%m-%d-%Y") + ".csv", 'a', newline='') as file:
                writer = csv.writer(file)                
                # write date, time, and member number to csv file
                index = 0
                for check in checkboxs:
                    already_logged = False
                    if check.get() == 1:
                        # if name is already in csv file at todays date, do not log
                        with open("logs/members/" + datetime.now().strftime("%m-%d-%Y") + ".csv", 'r') as file:
                            reader = csv.reader(file)
                            for row in reader:
                                if not row:
                                    continue
                                elif row[0] == date and row[2] == num and row[3].lower() == name_in_checkbox[index].lower():
                                    already_logged_list.append(name_in_checkbox[index].split(" ")[0])
                                    print("already logged")
                                    already_logged = True
                        if not already_logged:
                            writer.writerow([date, time, num, name_in_checkbox[index]])
                            logged = True
                    index += 1

            # if member is logged, log guest
            if logged:
                # if guests array is not empty, log guests
                if guests:
                    for guest in guests:
                        # find guest in csv file
                        with open('logs/guests/guests.csv', 'r') as file:
                            reader = csv.reader(file)
                            for row in reader:
                                if row == guest:
                                    num_of_visits = int(guest[8]) + 1
                                    new_row = [date, guest[1], guest[2], guest[3], guest[4], guest[5], guest[6], guest[7], num_of_visits]
                                    # replace old row with new row
                                    with open('logs/guests/guests.csv', 'r') as file:
                                        reader = csv.reader(file)
                                        lines = list(reader)
                                        for line in lines:
                                            if line == guest:
                                                lines[lines.index(line)] = new_row
                                    # write new row to csv file
                                    with open('logs/guests/guests.csv', 'w', newline='') as file:
                                        writer = csv.writer(file)
                                        writer.writerows(lines)
                # go back to start page
                guest_cost_amount()
                print("member logged")
            else:
                if guests:
                    now = datetime.now()
                    date = now.strftime("%m/%d/%Y")
                    # log guest
                    if guests:
                        for guest in guests:
                            # find guest in csv file
                            with open('logs/guests/guests.csv', 'r') as file:
                                reader = csv.reader(file)
                                for row in reader:
                                    if row == guest:
                                        num_of_visits = int(guest[8]) + 1
                                        new_row = [date, guest[1], guest[2], guest[3], guest[4], guest[5], guest[6], guest[7], num_of_visits]
                                        # replace old row with new row
                                        with open('logs/guests/guests.csv', 'r') as file:
                                            reader = csv.reader(file)
                                            lines = list(reader)
                                            for line in lines:
                                                if line == guest:
                                                    lines[lines.index(line)] = new_row
                                        # write new row to csv file
                                        with open('logs/guests/guests.csv', 'w', newline='') as file:
                                            writer = csv.writer(file)
                                            writer.writerows(lines)
                                            print("guest logged")
                        guest_cost_amount()
                # if there is a check box selected
                elif any(check.get() == 1 for check in checkboxs):
                    #if not already_logged:
                    popup_notice("already_logged")
                else:
                    popup_notice("no_member")
                print("member not logged")

        def switch():
            # Determine is on or off
            if select_all_button.cget('text') == "Deselect All":
                for checkbox in checkboxs:
                    if checkbox.get() == 1:
                        checkbox.toggle()
                select_all_button.config(text="Select All")
            else:
                for checkbox in checkboxs:
                    if checkbox.get() == 0:
                        checkbox.toggle()
                select_all_button.config(text="Deselect All")

        def search():
            value_to_search = var.get()
            if value_to_search == "" or value_to_search == " ":
                guest_entry['values'] = StartPage.current_guests
            else:
                value_to_siplay = []
                for value in StartPage.current_guests:
                    if value_to_search.lower() in value.lower():
                        value_to_siplay.append(value)
                guest_entry['values'] = value_to_siplay

        def is_search():
            '''if search entry is not empty, search for guest'''
            if search_entry.get() != "":
                search()
                print("search")
            else:
                logMember(StartPage.mem_num)
            
        def guest_cost_amount():
            guest_cost = 0
            actual_guests = []
            for guest in guests:
                if guest not in actual_guests:
                    actual_guests.append(guest)
            for guest in actual_guests:
                charged_zip_codes = [27455, 27214, 27358, 27357, 27310, 27410, 27408, 27405, 27401, 27403, 27409, 27235, 27282, 27406, 27301, 27249, 27377, 27283, 27313, 27320, 27260]
                if int(guest[7]) in charged_zip_codes:
                    guest_cost += 8
            if guest_cost > 0:
                # new popup window for guest cost
                guest_cost_window = tk.Toplevel()
                guest_cost_window.title("Guest Cost")
                guest_cost_window.minsize(250, 200)
                guest_cost_window.resizable(False, False)

                # header
                l = tk.Label(guest_cost_window, text="Charge", fg='red', font=controller.title_font)
                l.pack()

                # guest cost label
                guest_message_label = tk.Label(guest_cost_window, text="Please collect cash for guest(s).")
                guest_message_label.pack(pady=(10, 5))
                guest_cost_label = tk.Label(guest_cost_window, text="Guest Cost: $" + str(guest_cost))
                guest_cost_label.pack()
                # guest cost button
                guest_cost_button = ttk.Button(guest_cost_window, text="Okay", command=lambda: [guest_cost_window.destroy(), controller.show_frame(StartPage)])
                guest_cost_button.place(x=25, y=150)
                b = ttk.Button(guest_cost_window, text="Override", command=lambda: [override_cost(guest_cost_window)])
                b.place(x=125, y=150)
            else:
                controller.show_frame(StartPage)

        # override guest charge to not log
        def override_cost(win):
            # admin password check
            def pass_check(password, guest="", event=""):
                if password == current_pass:
                    done()
            # override
            def override(guest="", event=""):
                # clear window
                for widget in win.winfo_children():
                    widget.destroy()

                if StartPage.auth:
                    pass_check(current_pass, guest=guest, event=event)
                else:
                    # admin header
                    l = tk.Label(win, text="Override", font=controller.title_font)
                    l.pack()
                    # admin password
                    l = tk.Label(win, text="Admin password:")
                    l.place(x=25, y=64)
                    # admin password entry
                    admin_pass = ttk.Entry(win, width=5, font=("Arial", 20))
                    admin_pass.place(x=140, y=60)
                    admin_pass.focus()
                    # admin password submit button
                    admin_button = ttk.Button(win, text="Submit", command=lambda: pass_check(admin_pass.get()))
                    win.bind("<Return>", lambda e: pass_check(admin_pass.get(), guest=guest, event=event))
                    admin_button.place(x=125, y=115)
                    # close button
                    close_button = ttk.Button(win, text="Close", command=win.destroy)
                    close_button.place(x=25, y=115)
            
            def done():
            # find guest and write to csv file
                for guest in guests:
                    # find guest in csv file
                    with open('logs/guests/guests.csv', 'r') as file:
                        reader = csv.reader(file)
                        for row in reader:
                            if row[1:6] == guest[1:6]:
                                row.append("override")
                                print(row)
                                # replace old row with new row
                                with open('logs/guests/guests.csv', 'r') as file:
                                    reader = csv.reader(file)
                                    lines = list(reader)
                                    for line in lines:
                                        if line[1:6] == guest[1:6]:
                                            lines[lines.index(line)] = row
                                # write new row to csv file
                                with open('logs/guests/guests.csv', 'w', newline='') as file:
                                    writer = csv.writer(file)
                                    writer.writerows(lines)
                # close window
                win.destroy()
                # go back to start page
                controller.show_frame(StartPage)
            # call override
            override()
        
        # header
        header = tk.Label(self, text="Member Lookup", font=controller.title_font)
        header.place(x=200, y=10)

        # make a canvas to place text and buttons on
        canvas = tk.Canvas(self, width=830, height=237)
        canvas.pack(side="left")
        canvas_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

        # make the scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.place(x=844, y=120, height=237)
        canvas.configure(yscrollcommand=scrollbar.set, highlightthickness=0)

        # check csv file for member number or last name
        if StartPage.mem_num != "":
            # look through images
            images = {}
            for file in os.listdir("images"):
                filenum = file.split("_")
                if filenum[0] == str(int(StartPage.mem_num)):
                    images[file] = file
                    StartPage.name = filenum[2].replace(".jpg", "")

            # check boxes for images
            name_in_checkbox = []
            checkboxs = []
            index = 0
            row = 0

            # display images
            for image in images:
                # get first name from image filename
                image = "images/" + image
                image_name = image.replace(".jpg", "")
                image_name = image_name.split("_")
                name = image_name[1] + " " + image_name[2]

                name_in_checkbox.append(name)

                #imageVar = tk.IntVar() (done know why this is here...)

                # get first name from image filename
                member_name = image_name[1] # use for checkbox thing

                # make check boxes
                image_checkbox = CheckImage(canvas_frame, name=member_name, image_path=image, value=0)
                checkboxs.append(image_checkbox)
                if index == 6:
                    row += 1
                    index = 0
                # pack them side by side
                if index == 0:
                    image_checkbox.grid(column=index, row=row, padx=(50,10), pady=(10,0))
                else:
                    image_checkbox.grid(column=index, row=row, padx=10, pady=(10,0))

                if row == 2:
                    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
                    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                index += 1
        elif StartPage.name != "":
            # look in image filenames for last name
            images = {}
            index = 0
            for file in os.listdir("images"):
                if file == ".DS_Store":
                    continue
                elif file.startswith('._'):
                    continue
                else:
                    if StartPage.name.lower() in file.lower():
                        images[file] = file
                        # display member info
                        file = file.replace(".jpg", "")
                        info_cut_up = file.split("_")
                        # label for check-in button
                        check_in_label = tk.Label(canvas_frame, text="Member, " + info_cut_up[1] + " " + info_cut_up[2] + ", has number: " + info_cut_up[0] + "", font=("Arial", 20))
                        check_in_label.grid(column=0, row=index, padx=25, pady=5)
                        # button for member found
                        member_info = tk.Button(canvas_frame, text="Select", font=("Arial", 20), command=lambda info=info_cut_up[0]: pass_to_lookup(info), width=8, height=1)
                        member_info.grid(column=1, row=index, padx=0, pady=5)
                        if index == 4:
                            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
                            canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                        index += 1
        else:
            print("error")

        # display last name
        if StartPage.member_exists:
            last_name_label = tk.Label(self, text="Last Name: " + StartPage.name, font=("Arial", 20))
        else:
            last_name_label = tk.Label(self, text="Search: " + StartPage.name, font=("Arial", 20))
        last_name_label.place(x=290, y=80)

        # button to select all check boxes
        if StartPage.member_exists:
            select_all_button = tk.Button(self, text="Select All", font=("Arial", 20), command=lambda: switch(), width=9, height=1)
            select_all_button.place(x=350, y=380)

        # guest number entry
        if StartPage.member_exists:
            guest_entry = ttk.Combobox(self, state='readonly', width=18)
            guest_entry['values'] = StartPage.current_guests
            guest_entry.place(x=680, y=412)

            var=StringVar()
            search_entry = Entry(self, textvariable=var, width=13)
            search_entry.place(x=680, y=385)
            search_entry.focus()

            search_button = tk.Button(self, text="search", command=search)
            search_button.place(x=765, y=382)

        # button to add guest to member
        if StartPage.member_exists:
            guest_button = tk.Button(self, text="Add Guest", font=("Arial", 20), width=8, command=findGuest)
            guest_button.place(x=515, y=380)

        # guest error label
        guest_error = tk.Label(self, text="Guest not found.", fg="red")


        # button to go back to main page
        back_button = tk.Button(self, text="Back", font=("Arial", 20), width=8, command=lambda: controller.show_frame(StartPage))
        if StartPage.member_exists:
            back_button.place(x=50, y=380)
        else:
            back_button.place(x=350, y=390)

        # check in button
        if StartPage.member_exists:
            check_in_button = tk.Button(self, text="Check In", font=("Arial", 20), width=8, command=lambda: logMember(StartPage.mem_num))
            controller.bind("<Return>", lambda event: is_search())
            check_in_button.place(x=200, y=380)



class AddMember(tk.Frame):

    file = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        file_label = tk.Label(self, text="", font=("Arial", 20))
        file_label.place(x=250, y=250)
        
        # add member
        def addMember():
            # make sure all fields are filled
            if first_name.get() != "" and last_name.get() != "" and mem_num.get() != "" and AddMember.file != "":
                # make sure member number is 4 digits
                if len(mem_num.get()) != 4 and not mem_num.get().isdigit():
                    # display error message in red
                    error = tk.Label(self, text="Member number must be 4 digits.", font=("Arial", 20), fg="red")
                    error.place(x=50, y=325)
                    return
                # format info
                first_name_var = first_name.get()
                last_name_var = last_name.get()
                # create image name
                image_name = mem_num.get() + "_" + first_name_var + "_" + last_name_var + ".jpg"

                # check if image_name already exists in images folder
                if os.path.exists("images/" + image_name):
                    # display error message in red
                    error = tk.Label(self, text="Member already exists.", font=("Arial", 20), fg="red")
                    error.place(x=50, y=325)
                    return

                # if file is not a jpg, convert it to jpg
                if not AddMember.file.endswith(".jpg"):
                    # open image
                    image = Image.open(AddMember.file)
                    # convert image to jpg
                    image = image.convert("RGB")
                    # save image as jeg
                    image.save("images/" + image_name)
                else:
                    # copy image to images folder
                    shutil.copy(AddMember.file, "images/" + image_name)
                # display success message in green
                success = tk.Label(self, text="Member added successfully!", font=("Arial", 20), fg="green")
                success.place(x=50, y=325)
                # clear all fields
                first_name.delete(0, 'end')
                last_name.delete(0, 'end')
                mem_num.delete(0, 'end')
                AddMember.file = ""
                # set file label to empty
                file_label.config(text="")
                # focus on first name
                first_name.focus()
            else:
                # display error message in red
                error = tk.Label(self, text="Please fill out all fields.", font=("Arial", 20), fg="red")
                error.place(x=50, y=325)


        # open file
        def openfile():
            # all file types
            filetypes = (("jpeg files", "*.jpg"), ("jpg files", "*.jpeg"), ("png files", "*.png"), ("all files", "*.*"))
            AddMember.file = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = filetypes)
            # show filename on screen
            # split by / and get last value
            filename = AddMember.file.split("/")[len(AddMember.file.split("/")) - 1]
            file_label.config(text=filename)

        # header
        header = tk.Label(self, text="Add Member", font=controller.title_font)
        header.pack(pady=20)

        # label for first name
        first_name_label = tk.Label(self, text="First Name:", font=("Arial", 20))
        first_name_label.place(x=50, y=100)
        # text box for first name
        first_name = tk.Entry(self, width=20, font=("Arial", 20))
        first_name.place(x=275, y=100)
        first_name.focus()

        # label for last name
        last_name_label = tk.Label(self, text="Last Name:", font=("Arial", 20))
        last_name_label.place(x=50, y=150)
        # text box for last name
        last_name = tk.Entry(self, width=20, font=("Arial", 20))
        last_name.place(x=275, y=150)

        # label for member number
        mem_num_label = tk.Label(self, text="Member Number:", font=("Arial", 20))
        mem_num_label.place(x=50, y=200)
        # text box for member number
        mem_num = tk.Entry(self, width=20, font=("Arial", 20))
        mem_num.place(x=275, y=200)

        # location to drag and drop image
        image_label = tk.Button(self, text="Upload image", font=("Arial", 20), command=openfile)
        image_label.place(x=50, y=250)

        # add member button
        add_member_button = tk.Button(self, text="Add Member", font=("Arial", 20), command=addMember)
        controller.bind("<Return>", lambda event: addMember())
        add_member_button.place(x=380, y=390)

        # back button
        back_button = tk.Button(self, text="Back", font=("Arial", 20), command=lambda: controller.show_frame(StartPage))
        back_button.place(x=290, y=390)



class DeleteMember(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        member_objects = {}

        def findMember():

            # clear items in canvas
            for widget in canvas_frame.winfo_children():
                widget.destroy()

            mem_found = False
            # if mem_num is not empty
            if mem_num.get() != "":
                # look through image files in images folder
                index = 0
                canvas.configure(yscrollcommand=scrollbar.set, highlightthickness=0)
                canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                for file in os.listdir("images"):
                    # if file starts with mem_num
                    filenum = file.split("_")
                    if filenum[0] == mem_num.get():
                        # display file info on screen
                        file = file.replace(".jpg", "")
                        text_to_display = file.split("_")

                        first_name = text_to_display[1]
                        first_name = first_name[0].upper() + first_name[1:]

                        last_name = text_to_display[2]
                        last_name = last_name[0].upper() + last_name[1:]

                        member_info = tk.Label(canvas_frame, text="Member, " + first_name + " " + last_name + ", has number: " + text_to_display[0] + "", font=("Arial", 20))
                        member_info.grid(row=index, column=0, pady=5, padx=25)
                        # button to delete this member
                        delete_button = tk.Button(canvas_frame, text="Delete Member", font=("Arial", 20), command=lambda file=file: deleteMember(file))
                        delete_button.grid(row=index, column=1, pady=5, padx=(0,20))
                        member_objects[file] = {'info': member_info, 'button': delete_button}

                        if index == 4:
                            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

                        index += 1
                        mem_found = True
                if mem_found == False:
                    # display error message in red
                    canvas.config(yscrollcommand=None)
                    canvas.unbind_all("<MouseWheel>")
                    error = tk.Label(canvas_frame, text="Member not found.", font=("Arial", 20), fg="red")
                    error.grid(row=0, column=0, pady=5, padx=(50,0))
                    print("Member not found.")
            else:
                # display error message in red
                canvas.config(scrollcommand=None)
                canvas.unbind_all("<MouseWheel>")
                error = tk.Label(canvas_frame, text="Please enter a number.", font=("Arial", 20), fg="red")
                error.grid(row=0, column=0, pady=5, padx=(50,0))

            canvas.update_idletasks()
            canvas.config(scrollregion=canvas_frame.bbox())

        def deleteMember(my_file):
            # remove deleted member
            deleted_member_info = member_objects[my_file]['info']
            deleted_delete_button = member_objects[my_file]['button']
            deleted_y = deleted_member_info.winfo_y()
            # remove the member info and delete button objects from the GUI
            deleted_member_info.destroy()
            deleted_delete_button.destroy()
            del member_objects[my_file]

            my_file = my_file + ".jpg"
            os.remove("images/" + my_file)

            # move all buttons below deleted member up
            index = 0
            for key in member_objects:
                member_info = member_objects[key]['info']
                delete_button = member_objects[key]['button']
                # get current y position of member info
                current_y = member_info.winfo_y()
                
                if current_y > deleted_y:
                    # move member info and delete button up
                    member_info.grid(row=index, column=0, pady=5, padx=50)
                    delete_button.grid(row=index, column=1, pady=5, padx=(0,20))
                index += 1

            # display success message in green
            success = tk.Label(self, text="Member deleted.", font=("Arial", 20), fg="green")
            success.place(x=500, y=350)
            # fix scrollbar
            canvas.update_idletasks()
            canvas.config(scrollregion=canvas_frame.bbox())
            # clear member number
            mem_num.delete(0, 'end')
            mem_num.focus()

        
        # header
        header = tk.Label(self, text="Delete Member", font=controller.title_font)
        # center it with grid
        header.place(x=240, y=10)

        # label for member number
        mem_num_label = tk.Label(self, text="Member Number:", font=("Arial", 20))
        mem_num_label.place(x=240, y=75)
        # text box for member number
        mem_num = tk.Entry(self, width=10, font=("Arial", 20))
        mem_num.place(x=465, y=75)
        mem_num.focus()

        # make a canvas to place text and buttons on
        canvas = tk.Canvas(self, width=830, height=237)
        canvas.pack(side="left")
        canvas_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

        # make the scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.place(x=844, y=120, height=237)

        # find member button
        find_member_button = tk.Button(self, text="Find Member", font=("Arial", 20), command=findMember)
        controller.bind("<Return>", lambda event: findMember())
        find_member_button.place(x=380, y=390)

        # back button
        back_button = tk.Button(self, text="Back", font=("Arial", 20), command=lambda: controller.show_frame(StartPage))
        back_button.place(x=290, y=390)



class AddGuest(tk.Frame):
    
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller

            message = tk.Label(self, text="", font=("Arial", 20), fg="red")
            message.place(x=50, y=300)

    
            def exit():
                StartPage.update_guests()
                controller.show_frame(StartPage)

            def addGuest():
                try:
                    message.config(text="")
                except:
                    pass
                # make sure all fields are filled out
                if first_name.get() == "" or last_name.get() == "" or phone_num.get() == "" or address.get() == "" or city.get() == "" or state.get() == "" or zip_code.get() == "":
                    # display error message in red
                    message.config(text="Please fill out all fields.", fg="red")
                else:
                # check if last name and phone number exist in logs/guests/guests.csv
                    number = phone_num.get()
                    for c in number:
                        if c not in "0123456789":
                            # remove c from number
                            number = number.replace(c, "")

                    # make sure number is 10 digits
                    if len(number) != 10:
                        # display error message in red
                        message.config(text="Please enter a 10 digit phone number.", fg="red")
                        return
                    else:
                    
                        with open("logs/guests/guests.csv", "r") as f:
                            for line in f:
                                line = line.split(",")
                                if line[1].lower() == first_name.get().lower() and line[3] == number:
                                    # display error message in red
                                    if line[0] == "00/00/0000":
                                        line[0] = "recently"
                                    message.config(text="Guest already exists, created " + line[0], fg="red")
                                    return
                        # format guest info and write to guest.csv
                        ccity = city.get().lower().replace(' ', '')
                        ccity = ccity[0].upper() + ccity[1:]
                        guest_info = "00/00/0000" + "," + first_name.get().replace(' ', '') + "," + last_name.get().replace(' ', '') + "," + number + "," + address.get().lower() + "," + ccity + "," + state.get() + "," + zip_code.get() + ",0"
                        guest_info = guest_info
                        with open("logs/guests/guests.csv", "a") as f:
                            # write to new line
                            f.write(guest_info)
                            f.write("\n")
                        # display success message in green
                        message.config(text="Guest added successfully!", fg="green")

                        # clear all fields
                        first_name.delete(0, 'end')
                        first_name.focus()

            def clear_fields():
                try:
                    message.config(text="")
                except:
                    pass
                # make sure all fields are filled out
                if first_name.get() == "" or last_name.get() == "" or phone_num.get() == "" or address.get() == "" or city.get() == "" or state.get() == "" or zip_code.get() == "":
                    # display error message in red
                    message.config(text="Please fill out all fields.", fg="red")
                else:
                # check if last name and phone number exist in logs/guests/guests.csv
                    number = phone_num.get()
                    for c in number:
                        if c not in "0123456789":
                            # remove c from number
                            number = number.replace(c, "")

                    # make sure number is 10 digits
                    if len(number) != 10:
                        # display error message in red
                        message.config(text="Please enter a 10 digit phone number.", fg="red")
                        return
                    else:
                    
                        with open("logs/guests/guests.csv", "r") as f:
                            for line in f:
                                line = line.split(",")
                                if line[1].lower() == first_name.get().lower() and line[3] == number:
                                    # display error message in red
                                    if line[0] == "00/00/0000":
                                        line[0] = "recently"
                                    message.config(text="Guest already exists, created " + line[0], fg="red")
                                    return
                        # format guest info and write to guest.csv
                        ccity = city.get().lower().replace(' ', '')
                        ccity = ccity[0].upper() + ccity[1:]
                        guest_info = "00/00/0000" + "," + first_name.get().replace(' ', '') + "," + last_name.get().replace(' ', '') + "," + number + "," + address.get().lower() + "," + ccity + "," + state.get() + "," + zip_code.get() + ",0"
                        guest_info = guest_info
                        with open("logs/guests/guests.csv", "a") as f:
                            # write to new line
                            f.write(guest_info)
                            f.write("\n")
                        # display success message in green
                        message.config(text="Guest added successfully!", fg="green")

                        first_name.delete(0, 'end')
                        last_name.delete(0, 'end')
                        phone_num.delete(0, 'end')
                        address.delete(0, 'end')
                        city.delete(0, 'end')
                        state.set("North Carolina")
                        zip_code.delete(0, 'end')
                        first_name.focus()
    
            # header
            header = tk.Label(self, text="Add Guest", font=controller.title_font)
            header.pack(pady=20)
    
            # label for first name
            first_name_label = tk.Label(self, text="First Name:", font=("Arial", 20))
            first_name_label.place(x=50, y=100)
            # text box for first name
            first_name = tk.Entry(self, width=11, font=("Arial", 20))
            first_name.place(x=200, y=100)
            first_name.focus()

            # label for last name
            last_name_label = tk.Label(self, text="Last Name:", font=("Arial", 20))
            last_name_label.place(x=50, y=150)
            # text box for last name
            last_name = tk.Entry(self, width=11, font=("Arial", 20))
            last_name.place(x=200, y=150)

            # label for phone number
            phone_num_label = tk.Label(self, text="Phone #:", font=("Arial", 20))
            phone_num_label.place(x=50, y=200)
            # text box for phone number
            phone_num = tk.Entry(self, width=11, font=("Arial", 20))
            phone_num.place(x=200, y=200)

            # label for address
            address_label = tk.Label(self, text="Address:", font=("Arial", 20))
            address_label.place(x=375, y=100)
            # text box for address
            address = tk.Entry(self, width=18, font=("Arial", 20))
            address.place(x=500, y=100)

            # label for city
            city_label = tk.Label(self, text="City:", font=("Arial", 20))
            city_label.place(x=375, y=150)
            # text box for city
            city = tk.Entry(self, width=18, font=("Arial", 20))
            city.place(x=500, y=150)

            # drop down menu for state
            state_label = tk.Label(self, text="State:", font=("Arial", 20))
            state_label.place(x=375, y=200)
            state = tk.StringVar(self)
            state.set("North Carolina")
            state_menu = tk.OptionMenu(self, state, "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming")
            state_menu.config(width=12, font=("Arial", 20))
            state_menu.place(x=525, y=195)

            # field for zip code max 5 digits
            zip_label = tk.Label(self, text="Zip:", font=("Arial", 20))
            zip_label.place(x=375, y=250)
            zip_code = tk.Entry(self, width=18, font=("Arial", 20))
            zip_code.place(x=500, y=250)

            # submit button
            submit_button = tk.Button(self, text="Submit", font=("Arial", 20), command=addGuest)
            controller.bind("<Return>", lambda event: addGuest())
            submit_button.place(x=410, y=360)

            # clear button
            submit_button = tk.Button(self, text="Submit & Clear", font=("Arial", 20), command=clear_fields)
            submit_button.place(x=575, y=360)

            # back button
            back_button = tk.Button(self, text="Back", font=("Arial", 20), command=exit)
            back_button.place(x=310, y=360)



class auth_check(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        def checkPasscode():
            if passcode.get() == current_pass:
                StartPage.auth = True
                controller.show_frame(StartPage)
            else:
                error.place(x=50, y=225)
                passcode.delete(0, 'end')
                passcode.focus()

        # header for auth login
        header = tk.Label(self, text="Admin Login", font=controller.title_font)
        header.pack(pady=20)

        # text for auth login
        auth_text = tk.Label(self, text="Please enter the passcode to access the admin panel.", font=("Arial", 20))
        auth_text.pack()

        # label for passcode
        passcode_label = tk.Label(self, text="Passcode:", font=("Arial", 20))
        passcode_label.place(x=50, y=175)
        # text box for passcode
        passcode = tk.Entry(self, width=10, font=("Arial", 20))
        passcode.place(x=200, y=175)
        passcode.focus()

        # error message
        error = tk.Label(self, text="Incorrect passcode. Please try again.", font=("Arial", 20), fg="red")

        # submit button
        submit_button = tk.Button(self, text="Submit", font=("Arial", 20), command=checkPasscode)
        controller.bind("<Return>", lambda event: checkPasscode())
        submit_button.place(x=410, y=360)

        # back button
        back_button = tk.Button(self, text="Back", font=("Arial", 20), command=lambda: controller.show_frame(StartPage))
        back_button.place(x=310, y=360)



class Stats(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
    
        # header
        header = tk.Label(self, text="Statistics", font=controller.title_font)
        header.pack(pady=20)

        # error message
        date_error = tk.Label(self, text="", font=("Arial", 20), fg="red")
        date_error.place(x=50, y=175)

        def run_stats(date=datetime.now().strftime("%m/%d/%Y")):

            # check if file directory exists
            if not os.path.exists("logs/members/" + date.replace("/", "-") + ".csv"):
                try:
                    date_error.config(text="No data for " + date)
                    total_today_label = tk.Label(self, text="Checked In: 0", font=("Arial", 20))
                    total_cost_label = tk.Label(self, text="Cash collected: $0", font=("Arial", 20))
                    total_guest_label = tk.Label(self, text="Guests Checked In: 0", font=("Arial", 20))
                    total_today_label.place(x=350, y=75)
                    total_cost_label.place(x=575, y=75)
                    total_guest_label.place(x=550, y=110)
                except:
                    pass
            else:
                print(f"running stats " + date)
                family_count = 0
                today_count = 0
                member_count = 0
                guest_count = 0

                # find amount of member
                numbers = []
                for file in os.listdir("images"):
                    if file.endswith(".jpg"):
                        member_count += 1
                        file = file.split("_")
                        if file[0] not in numbers:
                            family_count += 1
                            numbers.append(file[0])

                # find amount of members checked in today
                with open("logs/members/" + date.replace("/", "-") + ".csv", "r") as log:
                    for line in log:
                        line = line.split(",")
                        if line[0] == date:
                            today_count += 1

                # find amount of guest logged in today
                guest_count = 0
                # guest.csv
                with open("logs/guests/guests.csv", "r") as guest:
                    for line in guest:
                        line = line.split(",")
                        if line[0] == date:
                            guest_count += 1

                # find total cost of guests
                total_cost = 0
                with open("logs/guests/guests.csv", "r") as guest:
                    for line in guest:
                        line = line.split(",")
                        if line[0] == date:
                            if line[5] == "Greensboro" or line[5] == "Summerfield" or line[5] == "Oak Ridge" or line[5] == "Browns summit" or line[5] == "Stokesdale":
                                if len(line) == 8:
                                    total_cost += 8

                # label for all counts
                total_member_label = tk.Label(self, text="Total Members: " + str(member_count), font=("Arial", 20))
                total_families_label = tk.Label(self, text="Total Families: " + str(family_count), font=("Arial", 20))
                total_today_label = tk.Label(self, text="Checked In: " + str(today_count) + "    ", font=("Arial", 20))
                total_guest_label = tk.Label(self, text="Guests Checked In: " + str(guest_count) + "    ", font=("Arial", 20))
                total_cost_label = tk.Label(self, text="Cash collected: $" + str(total_cost) + "   ", font=("Arial", 20))
                total_member_label.place(x=50, y=75)
                total_families_label.place(x=50, y=110)
                total_today_label.place(x=350, y=75)
                total_guest_label.place(x=550, y=110)
                total_cost_label.place(x=575, y=75)


                def save_confirm(fig):
                    '''Confirm save of graph with information.'''
                    confirm = tk.Toplevel()
                    confirm.wm_title("Notice")
                    confirm.minsize(300, 250)
                    confirm.resizable(False, False)
                    confirm.focus_force()

                    # header
                    l = tk.Label(confirm, text="Continue?", fg='red', font=controller.title_font)
                    l.pack()

                    # label
                    l = tk.Label(confirm, text="Are you sure you want to save this graph.\nThis should only be done once a day.")
                    l.pack()

                    # label for weather
                    l = tk.Label(confirm, text="Weather:")
                    l.place(x=35, y=100)
                    # text box for weather
                    weather = tk.Entry(confirm, width=15)
                    weather.place(x=115, y=100)
                    weather.focus()

                    # label for chemical levels
                    l = tk.Label(confirm, text="Chemicals:")
                    l.place(x=35, y=130)
                    # text box for chemical levels
                    chemical = tk.Entry(confirm, width=15)
                    chemical.insert(0, 'ph: , cl: , al: ')
                    chemical.place(x=115, y=130)

                    # label for comment
                    l = tk.Label(confirm, text="Comment:")
                    l.place(x=35, y=160)
                    # text box for comment
                    comment = tk.Text(confirm, width=20, height=3)
                    comment.place(x=115, y=160)

                    # buttons
                    b = ttk.Button(confirm, text="Save", command=lambda: [format_save(fig, weather, chemical, comment), confirm.destroy()])
                    b.place(x=150, y=215)
                    confirm.bind("<Return>", lambda e: [format_save(fig, weather, chemical, comment), confirm.destroy()])
                    c = ttk.Button(confirm, text="Cancel", command=confirm.destroy)
                    c.place(x=50, y=215)
                    confirm.bind("<Escape>", lambda e: confirm.destroy())

                def format_save(fig, weather, chemical, comment):
                    '''Format data and save it.'''
                    # format data
                    weather = weather.get()
                    chemical = chemical.get()
                    comment = comment.get("1.0", "end-1c")
                    data = "Weather: " + weather + "\nChecmicals: " + chemical + "\nComment: " + comment + "\nMembers Checked In: " + str(today_count) + "\nGuests Checked In: " + str(guest_count) + "\nCash Collected: $" + str(total_cost)
                    # save data
                    save_data(fig, data)

                def save_data(fig, data):
                    '''Save data to file.'''
                    save_date = date.replace("/", "-")
                    fig.savefig("data/" + save_date + "_histogram.png")

                    # create txt file and save data if it doesn't exist
                    if not os.path.exists("data/" + save_date + "_data.txt"):
                        with open("data/" + save_date + "_data.txt", "w") as file:
                            file.write(save_date + "\nMorning Log:\n" + data)
                    else:
                        with open("data/" + save_date + "_data.txt", "a") as file:
                            file.write("\n\nNight Log:\n" + data)

                    print("Saved.")

                def get_data():
                    '''Get data from log.csv.'''
                    # get data from log.csv
                    data = []
                    with open("logs/members/" + date.replace("/", "-") + ".csv", "r") as log:
                        for line in log:
                            line = line.split(",")
                            if line[0] == date:
                                data.append(int(line[1].split(":")[0]))
                    return data
                
                # Create a figure and a subplot for the histogram
                fig = Figure(figsize=(6, 2), dpi=100)
                ax = fig.add_subplot(111)
                ax.set_ylabel('Total Members')
                canvas = FigureCanvasTkAgg(fig, master=self)

                def plot():
                    '''Plot the histogram.'''
                    # get data
                    data = get_data()

                    # find unique values in data
                    unique = []
                    for i in data:
                        if i not in unique:
                            unique.append(i)

                    # Create the histogram
                    if not len(unique) == 0:
                        # Create a canvas for the figure and add it to the tkinter window
                        n, bins, patches = ax.hist(data, bins=len(unique))
                        ax.set_xticks([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
                        ax.set_xticklabels([10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8])
                        canvas.draw()
                        canvas.get_tk_widget().place(x=50, y=165)
                    else:
                        # display empty log message
                        date_error.config(text="No one has checked in " + date)

                    return fig
                
                def destory_graph():
                    '''Destory the 'old' graph.'''
                    canvas.get_tk_widget().destroy()
                    ax.clear()

                fig = plot()

                # save button
                save_button = tk.Button(self, text="Save", font=("Arial", 20), command=lambda: save_confirm(fig))
                save_button.place(x=735, y=390)
                # other date button
                other_date_button = tk.Button(self, text="Go", font=("Arial", 20), command=lambda: [run_stats(date=other_date_entry.get() + "/2023"), destory_graph(), total_today_label.destroy(), total_guest_label.destroy()])
                other_date_button.place(x=540, y=390)
                controller.bind("<Return>", lambda e: [run_stats(date=other_date_entry.get() + "/2023"), destory_graph(), total_today_label.destroy(), total_guest_label.destroy()])
                # other date entry
                other_date_entry = tk.Entry(self, width=8, font=("Arial", 20))
                other_date_entry.place(x=405, y=400)
                if date == datetime.now().strftime("%m/%d/%Y"):
                    other_date_entry.insert(0, datetime.now().strftime("%m/%d/%Y").replace("/2023", ""))
                else:
                    other_date_entry.insert(0, date.replace("/2023", ""))
                other_date_entry.focus()

        run_stats()
    
        # back button
        back_button = tk.Button(self, text="Back", font=("Arial", 20), command=lambda: controller.show_frame(StartPage))
        back_button.place(x=50, y=390)
        # other date label
        other_date_label = tk.Label(self, text="Other Date:", font=("Arial", 20))
        other_date_label.place(x=250, y=400)



if __name__ == "__main__":
    app = App()
    app.mainloop()