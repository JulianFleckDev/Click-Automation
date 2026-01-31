import time
import pyautogui
from pynput import mouse
from pynput.keyboard import Listener as KeyboardListener
from pynput.keyboard import Key
import tkinter as tk
from tkinter import ttk
import threading

record = False
posText = None
clicksPos = []

delay_text = None
delay = 2

running = False
stopRun = False

limit_text = None
limit = 1

def recordingActivity():
    global record
    record = not record

def startStop():
    global running
    global record
    global posText

    record = False
    running = True
    print("Run")
    on_runWithLimit()

def on_runWithLimit():
    for i in range(limit):
        if stopRun:
            break

        print("Cycle " + str(i) + " of " + str(range(limit)))
        global clicksPos
        for pos in clicksPos:
            pyautogui.click(pos)
            time.sleep(delay)

def on_mouseClick(x, y, button, pressed):
    if pressed & record:
        global posText
        clicksPos.append((x, y))
        posText.set(str(clicksPos))

def on_press(key):
    if key == Key.space:
        global  stopRun
        stopRun = True
        print(str(stopRun))
    elif key == Key.alt:
        recordingActivity()

def start_listeners():
    with mouse.Listener(on_click=on_mouseClick): #as listener:
        with KeyboardListener(on_press=on_press) as listener:
            listener.join()


def read_and_store_limit():
    """
    Reads the number from the entry field, attempts to convert it to an int,
    and stores it in the global 'user_number' variable.
    Handles potential ValueError if input is not a valid integer.
    """
    global limit  # Declare user_number as global to modify it
    global limit_text
    input_text = limit_text.get() # Get the string from the StringVar

    try:
        # Attempt to convert the string to an integer
        limit = int(input_text)
        print(f"Successfully read number: {limit} (Type: {type(limit)})")
        #messagebox.showinfo("Success", f"Number read: {new_limit}")
    except ValueError:
        # If conversion fails, it means the input was not a valid integer
        limit = None # Or keep its previous value, or set to a default
        print(f"Error: '{input_text}' is not a valid integer.")
        #messagebox.showerror("Invalid Input", "Please enter a valid whole number.")

def read_and_store_delay():
    """
    Reads the number from the entry field, attempts to convert it to an int,
    and stores it in the global 'user_number' variable.
    Handles potential ValueError if input is not a valid integer.
    """
    global delay  # Declare user_number as global to modify it
    global delay_text
    input_text = delay_text.get() # Get the string from the StringVar

    try:
        # Attempt to convert the string to an integer
        delay = int(input_text)
        print(f"Successfully read number: {delay} (Type: {type(delay)})")
        #messagebox.showinfo("Success", f"Number read: {new_limit}")
    except ValueError:
        try:
            # Attempt to convert the string to an integer
            delay = float(input_text)
            print(f"Successfully read number: {delay} (Type: {type(delay)})")
        except ValueError:
            # If conversion fails, it means the input was not a valid integer
            delay = None  # Or keep its previous value, or set to a default
            print(f"Error: '{input_text}' is not a valid integer.")
            # messagebox.showerror("Invalid Input", "Please enter a valid whole number.")

def start_tkinter_app():
    window = tk.Tk()
    window.title("Auto Clicker")
    window.geometry("400x500")

    #Labels -----------------------------------------------------------------------------------------------------------
    # Create a frame to hold the labels
    labels_frame = ttk.Frame(window)
    labels_frame.pack(side="top", anchor="nw", padx=0, pady=0)

    label1 = ttk.Label(labels_frame, text="1. Press Record to Start Recording clicks", padding=0, font=('Arial', 12, 'bold'))
    label1.pack()

    label2 = ttk.Label(labels_frame, text="2. Press Alt to Stop recording clicks", padding=0, font=('Arial', 12, 'bold'))
    label2.pack()

    label3 = ttk.Label(labels_frame, text="3. Press Start (Space = Force Stop)", padding=0, font=('Arial', 12, 'bold'))
    label3.pack()

    #Show Pos
    global posText
    posText = tk.StringVar()
    label4 = ttk.Label(labels_frame, textvariable=posText, font=("Arial", 10), wraplength=600, justify="left", borderwidth=2)
    label4.pack(pady=20)

    #Buttons ----------------------------------------------------------------------------------------------------------

    # Create a frame to hold the buttons
    button_frame = ttk.Frame(window)
    button_frame.pack(side="bottom", anchor="sw", padx=10, pady=10)  # Pack frame to the bottom-left corner

    # Create a Style object
    style = ttk.Style()

    # You might need to set a theme that allows background changes.
    # 'clam' and 'alt' themes are often more flexible for styling.
    style.theme_use("default")  # Try 'alt' or 'default' if 'clam' doesn't work for your OS

    # Configure a new style for the button.
    # The style name typically follows the pattern 'Name.TButton'.
    # 'My.TButton' is a custom style name.
    style.configure("My.TButton",
                    background="darkblue",  # Set the background color to red
                    foreground="white",  # Set the text color to white for contrast
                    font=('Arial', 12, 'bold'))  # You can also set font, etc.

    # Map colors for different states
    style.map("My.TButton",
              background=[('active', "blue")])  # Color when mouse is over the button


    # Button Events ---------------------------------------------------------------------------------------------------
    button1 = ttk.Button(button_frame, text="Record", padding=10, command=recordingActivity, style="My.TButton")#lambda:
    button2 = ttk.Button(button_frame, text="Start", padding=10, command=startStop , style="My.TButton")
    button1.pack(side="left", padx=5)
    button2.pack(side="left", padx=5)

    #Input ------------------------------------------------------------------------------------------------------------
    # Create a frame to hold the buttons
    input_frame = ttk.Frame(window)
    input_frame.pack(side="bottom", anchor="se", padx=5, pady=5)  # Pack frame to the corner

    # 2. Create a StringVar to hold the entry's text
    global limit_text
    global delay_text

    limit_text = tk.StringVar()
    delay_text = tk.StringVar()
    # You can set an initial value if you want:
    # number_str_var.set("0")

    # 3. Create a Label
    label = ttk.Label(input_frame, text="Count:", font=('Arial', 12))
    label.pack() # Add some padding pady=0

    # 4. Create an Entry widget and link it to the StringVar
    number_entry = tk.Entry(input_frame, textvariable=limit_text, width=10)
    number_entry.pack(pady=5)
    number_entry.focus_set()  # Give focus to the entry field initially

    # 5. Create a Button to trigger the read function
    read_button = ttk.Button(input_frame, text="Confirm", command=read_and_store_limit, style="My.TButton")
    read_button.pack(pady=5)

    #--------------------------

    label2 = ttk.Label(input_frame, text="Delay:", font=('Arial', 12))
    label2.pack() # Add some padding pady=0

    # 4. Create an Entry widget and link it to the StringVar
    delay_entry = tk.Entry(input_frame, textvariable=delay_text, width=10)
    delay_entry.pack(pady=5)
    delay_entry.focus_set()  # Give focus to the entry field initially

    # 5. Create a Button to trigger the read function
    read2_button = ttk.Button(input_frame, text="Confirm", command=read_and_store_delay, style="My.TButton")
    read2_button.pack(pady=5)

    window.mainloop()

if __name__ == "__main__":
    # Start the mouse listener in a separate thread
    listener_thread = threading.Thread(target=start_listeners)
    listener_thread.daemon = True # Allow the program to exit even if listener is running
    listener_thread.start()

    # Start the Tkinter app in the main thread
    start_tkinter_app()
    # The listener thread will keep running in the background until the main program exits
