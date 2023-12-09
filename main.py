import customtkinter
import interpreter

interpreter.model = "openai/local"
interpreter.api_base = "http://localhost:1234/v1"

from pathlib import Path
import os

path = Path(interpreter.conversation_history_path)
history_chats = {}

for file in path.iterdir():
    # Extract the filename from the path using pathlib
    filename = file.name
    # Split the filename at the first double underscore '__'
    key = filename.split('__')[0].replace('_', ' ')
    # Add to the dictionary
    history_chats[key] = file

def button_callback():
    print("button pressed")

def load_history(path):
    print(path)
    pass

app = customtkinter.CTk()
app.title("my app")
app.geometry("600x480")
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=5)

history_frame = customtkinter.CTkScrollableFrame(master=app)
history_frame.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="nsw", rowspan=2)

history_label = customtkinter.CTkLabel(master=history_frame, text="Chat history", font=("default", 20))
history_label.grid(row=0, column=0, padx=20, pady=(0,0), sticky="nw")

history_buttons = []

for i, (key, path) in enumerate(history_chats.items()):
    # Use a lambda function to pass the specific path as an argument to load_history
    history_button = customtkinter.CTkButton(master=history_frame, text=key, command=lambda p=path: load_history(p))
    history_button.grid(row=i+1, column=0, padx=0, pady=(10,0), sticky="we")
    history_buttons.append(history_button)

chat_frame = customtkinter.CTkScrollableFrame(master=app)
chat_frame.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")
chat_frame.grid_columnconfigure(0, weight=1)

# Sample data: List of tuples with (message, is_user) 
# Replace this with your actual chat data
messages = [("Hello, how are you? we need a longer message to see what happens when it overflows and \nchanges to new line", False),
            ("I'm fine, thank you!", True),
            ("Great to hear that!", False)]

for i, (message, is_user) in enumerate(messages):
    # Create the label with blue background inside the frame
    bubble = customtkinter.CTkLabel(master=chat_frame,
                                    text=message, 
                                    wraplength=300,
                                    bg_color="transparent",  # Blue background
                                    corner_radius=10, # Apply rounded corners
                                    fg_color="#144870")

    # Grid the frame with appropriate padding and alignment
    padx, pady = 10, 5
    sticky = "e" if is_user else "w"
    bubble.grid(row=i, column=0, padx=padx, pady=pady, sticky=sticky)

input_frame = customtkinter.CTkFrame(master=app)
input_frame.grid(row=1, column=1, pady=(0,10), padx=10, sticky="swe")
input_frame.grid_columnconfigure(0, weight=1)

user_input = customtkinter.CTkTextbox(master=input_frame, height=40)
user_input.grid(row=0,column=0, padx=10,pady=10, sticky="nswe")

user_input_button = customtkinter.CTkButton(master=input_frame, text=">", command=print("click"), width=50)
user_input_button.grid(row=0, column=1, padx=(0,10), pady=10, sticky="nse")


app.mainloop()