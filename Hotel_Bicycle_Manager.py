import customtkinter as ctk
from tkinter import messagebox
import datetime  # Required to get the current date and time
import threading  # Required for implementing timers
import json  # Required for saving and loading booking data
import os  # Required for checking if file exists
import time  # Required for timestamp calculations

# Define color constants
COLOR_AVAILABLE = "#66FF66"  # Green
COLOR_HOVER_AVAILABLE = "#006400"  # Dark green
COLOR_OCCUPIED = "#FF0000"  # Red
COLOR_BUTTON_RED = "red" # Red
COLOR_HOVER_OCCUPIED = "#8B0000"  # Dark red

COLOR_YELLOW = "#FFFF00"  # Yellow
COLOR_HOVER_YELLOW = "#FFA500"  # Orange

COLOR_FRAME = "#5B99C2"
COLOR_FRAME_ALT = "#1A4870"
COLOR_TEXT = "#F9DBBA"
COLOR_BUTTON_BORDER = "#1F316F"

booking_data = {}
button_grid = []  # List to hold references to the buttons for color checking
data_file = "booking_data.json"  # File to store booking data
timer = 36000 # Timer in seconds: after 10 hours of booking, the button color changes to yellow

# Function to update the count of available and occupied bicycles
def update_bicycle_counts():
    available_count = sum(button.cget("fg_color") == COLOR_AVAILABLE for row in button_grid for button in row)
    available_bicycles_label.configure(text=f"AVAILABLE: {available_count}")
    occupied_bicycles_label.configure(text=f"OCCUPIED: {total_bicycles - available_count}")

def save_booking_data():
    with open(data_file, "w") as file:
        json.dump(booking_data, file)

def load_booking_data():
    global booking_data
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            booking_data = json.load(file)
    else:
        booking_data = {}

def delete_booking(details_window, button):
    button_text = button._text
    if button_text in booking_data:
        del booking_data[button_text]  # Remove the booking data
        button.configure(fg_color=COLOR_AVAILABLE, hover_color=COLOR_HOVER_AVAILABLE)  # Reset color to green and hover to dark green
        save_booking_data()

    details_window.destroy()
    app.attributes('-disabled', False)
    app.focus_force()

    update_bicycle_counts()

def open_details_window(clicked_button, button_text):
    details_window = ctk.CTkToplevel(app)
    details_window.title(f"{button_text} - Booking")
    details_window.geometry("350x450")
    details_window.resizable(False, False)
    details_window.grab_set()
    details_window.focus_force()

    # Entry fields and labels
    name_label = ctk.CTkLabel(details_window, text="NAME:")
    name_label.pack(pady=(10, 2))
    name_entry = ctk.CTkEntry(details_window)
    name_entry.pack(pady=(0, 10))

    surname_label = ctk.CTkLabel(details_window, text="SURNAME:")
    surname_label.pack(pady=(0, 2))
    surname_entry = ctk.CTkEntry(details_window)
    surname_entry.pack(pady=(0, 10))

    room_label = ctk.CTkLabel(details_window, text="ROOM NUMBER:")
    room_label.pack(pady=(0, 2))
    room_entry = ctk.CTkEntry(details_window)
    room_entry.pack(pady=(0, 10))

    # Labels for time and date, initially empty
    time_label = ctk.CTkLabel(details_window, text="BOOKING TIME:")
    time_label.pack(pady=(10, 2))
    time_value_label = ctk.CTkLabel(details_window, text="")
    time_value_label.pack()

    date_label = ctk.CTkLabel(details_window, text="BOOKING DATE:")
    date_label.pack(pady=(0, 2))
    date_value_label = ctk.CTkLabel(details_window, text="")
    date_value_label.pack()

    if button_text in booking_data:
        data = booking_data[button_text]
        name_entry.insert(0, data['name'])
        surname_entry.insert(0, data['surname'])
        room_entry.insert(0, data['room_number'])
        time_value_label.configure(text=data['time'])
        date_value_label.configure(text=data['date'])
        delete_button = ctk.CTkButton(details_window, text="DELETE",
            command=lambda: delete_booking(details_window, clicked_button))
        delete_button.pack(side="left", padx=20, pady=10)
    else:
        confirm_button = ctk.CTkButton(details_window, text="CONFIRM",
            command=lambda: confirm_details(
                name_entry, surname_entry, room_entry, time_value_label, date_value_label, details_window, clicked_button))
        confirm_button.pack(side="left", padx=20, pady=10)

    close_button = ctk.CTkButton(details_window, text="CLOSE",
        command=lambda: close_details_window(details_window))
    close_button.pack(side="right", padx=20, pady=10)

    details_window.protocol("WM_DELETE_WINDOW", lambda: close_details_window(details_window))

def confirm_details(name_entry, surname_entry, room_entry, time_value_label, date_value_label, details_window, button):
    name = name_entry.get()
    surname = surname_entry.get()
    room_number = room_entry.get()

    if not name or not surname or not room_number:
        messagebox.showerror("Error", "All fields must be filled.")
        return

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")
    current_timestamp = time.time()  # Get the current timestamp

    time_value_label.configure(text=current_time)
    date_value_label.configure(text=current_date)

    button_text = button._text
    booking_data[button_text] = {'name': name, 'surname': surname, 'room_number': room_number, 'time': current_time, 'date': current_date, 'timestamp': current_timestamp}
    button.configure(fg_color=COLOR_OCCUPIED, hover_color=COLOR_HOVER_OCCUPIED)

    # Start a timer to change the button color to yellow after 10 hours
    threading.Timer(timer, change_button_color_to_yellow, [button]).start()
    save_booking_data()

    details_window.destroy()
    app.attributes('-disabled', False)
    app.focus_force()
    update_bicycle_counts()

def change_button_color_to_yellow(button):
    if button.cget("fg_color") == COLOR_OCCUPIED:
        button.configure(fg_color=COLOR_YELLOW, hover_color=COLOR_HOVER_YELLOW)

def close_details_window(details_window):
    details_window.destroy()
    app.attributes('-disabled', False)
    app.focus_force()

def clear_all_bookings():
    if messagebox.askyesno("Confirm", "Are you sure you want to delete all bookings?"):
        for row in button_grid:
            for button in row:
                button.configure(fg_color=COLOR_AVAILABLE, hover_color=COLOR_HOVER_AVAILABLE)
        booking_data.clear()
        save_booking_data()
        update_bicycle_counts()

# Set CustomTkinter style
ctk.set_appearance_mode("dark")

# Create the main window object
app = ctk.CTk()
app.title("HOTEL Bicycle Management - By LuBaSp")
app.geometry("1280x720")
icon_path = "icon1.ico"
app.iconbitmap(icon_path)
app.resizable(False, False)

# Left Frames
titles = ["- WOMEN'S BICYCLES", "- MEN'S BICYCLES", "- BICYCLES WITH FRONT CHILDREN SEAT", "- BICYCLES WITH REAR CHILDREN SEAT"]
divisors = 5
frame_width = 850
frame_height = (720 // 4) - divisors * 4

# Customize button names and counts per frame
button_font = ("Andes", 25)  # Choose font family and size, increase size as needed
button_names = [
    [f"B{i}" for i in range(1, 11)],  # 10 buttons, 1 to 10
    [f"B{i}" for i in range(11, 21)],  # 10 buttons, 10 to 20
    [f"B{i}" for i in range(21, 26)],  # 5 buttons
    [f"B{i}" for i in range(26, 31)]  # 5 buttons
]

button_space = 10  # Space between buttons
button_width = frame_height // 2.5  # Button width based on frame height

# Right Frame
right_frame = ctk.CTkFrame(master=app, width=400, height=720, fg_color=COLOR_FRAME)
right_frame.pack(side="right", fill="y", expand=False, padx=(0, 10), pady=10)

title_label1 = ctk.CTkLabel(master=right_frame, text="HOTEL BICYCLE\nMANAGEMENT", font=("Andes", 45, "bold"), fg_color=COLOR_FRAME, text_color=COLOR_TEXT)
title_label1.place(relx=0.5, rely=0.05, anchor="n")

# Calculate the total number of buttons
total_bicycles = sum(len(button_list) for button_list in button_names)

# Label to display the total number of bicycles
label_font = ("Andes", 35, "bold")
total_bicycles_label = ctk.CTkLabel(master=right_frame, text=f"Number of TOTAL\nbicycles: {total_bicycles}", font=label_font, fg_color=COLOR_FRAME, text_color=COLOR_TEXT)
total_bicycles_label.place(relx=0.5, rely=0.375, anchor="center")

available_bicycles_label = ctk.CTkLabel(master=right_frame, text="AVAILABLE: ", font=label_font, fg_color=COLOR_FRAME, text_color='#66FF66')
available_bicycles_label.place(relx=0.5, rely=0.61, anchor="center")

occupied_bicycles_label = ctk.CTkLabel(master=right_frame, text="OCCUPIED: ", font=label_font, fg_color=COLOR_FRAME, text_color='#D53032')
occupied_bicycles_label.place(relx=0.5, rely=0.66, anchor="center")

# Add the Clear All Bookings button
clear_button = ctk.CTkButton(
    master=right_frame, 
    text="CLEAR ALL BOOKINGS", 
    font=("Andes", 30, "bold"),
    command=clear_all_bookings, 
    fg_color='#D53032', 
    text_color=COLOR_TEXT, 
    hover_color="darkred",
    border_width=3,
    border_color=COLOR_BUTTON_BORDER
)
clear_button.place(relx=0.5, rely=0.893, anchor="center")

border_size = 2  # Set border size

for i, title in enumerate(titles):
    frame = ctk.CTkFrame(master=app, width=frame_width, height=frame_height, fg_color=COLOR_FRAME_ALT)
    frame.pack(fill="x", expand=True, padx=10, pady=divisors)

    label = ctk.CTkLabel(master=frame, text=title, font=("Andes", 30, "bold"), fg_color=COLOR_FRAME_ALT, text_color=COLOR_TEXT)
    label.place(relx=0.02, rely=0.065, anchor="nw")

    row_buttons = []  # List to store the buttons for this row
    total_buttons_width = len(button_names[i]) * (button_width + 2 * border_size) + (len(button_names[i]) - 1) * button_space
    starting_x = (frame_width - total_buttons_width) // 2

    for j, name in enumerate(button_names[i]):
        button_border_frame = ctk.CTkFrame(master=frame, width=button_width + 2 * border_size, height=button_width + 2 * border_size, fg_color="black")
        button_border_frame.place(x=starting_x + j * (button_width + 2 * border_size + button_space), y=65-border_size)

        button = ctk.CTkButton(
            master=button_border_frame, 
            text=name, 
            width=button_width, 
            height=button_width,
            fg_color=COLOR_AVAILABLE, 
            text_color="black", 
            corner_radius=5,
            font=("Andes", 25, "bold"),
            hover_color=COLOR_HOVER_AVAILABLE,  # Dark green
            border_width=1,  # Add border width
            border_color=COLOR_BUTTON_BORDER
        )
        button.pack(padx=border_size, pady=border_size)
        button.configure(command=lambda b=button: open_details_window(b, b._text))
        row_buttons.append(button)
    button_grid.append(row_buttons)

# Load the booking data when the application starts
load_booking_data()

# Apply the loaded booking data to the buttons
current_time = time.time()
for row in button_grid:
    for button in row:
        button_text = button._text
        if button_text in booking_data:
            data = booking_data[button_text]
            if 'timestamp' in data:
                elapsed_time = current_time - data['timestamp']
                if elapsed_time >= timer:
                    button.configure(fg_color=COLOR_YELLOW, hover_color=COLOR_HOVER_YELLOW)  # Yellow with orange hover
                else:
                    button.configure(fg_color=COLOR_OCCUPIED, hover_color=COLOR_HOVER_OCCUPIED)  # Red with darkred hover
                    threading.Timer(timer - elapsed_time, change_button_color_to_yellow, [button]).start()
            else:
                button.configure(fg_color=COLOR_OCCUPIED, hover_color=COLOR_HOVER_OCCUPIED)  # Red with darkred hover
                threading.Timer(timer, change_button_color_to_yellow, [button]).start()
        else:
            button.hover_color = COLOR_HOVER_AVAILABLE  # Dark green

# Update the count of available bicycles at startup
update_bicycle_counts()

def on_closing():
    save_booking_data()
    app.destroy()

# Save the booking data when the application closes
app.protocol("WM_DELETE_WINDOW", on_closing)

app.mainloop()
