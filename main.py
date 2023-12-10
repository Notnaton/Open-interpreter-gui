from pathlib import Path
import customtkinter
import interpreter
import json

class HistoryFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, path):
        super().__init__(master)
        self.history_chats = {}
        for file in path.iterdir():
            # Extract the filename from the path using pathlib
            filename = file.name
            # Split the filename at the first double underscore '__'
            key = filename.split('__')[0].replace('_', ' ')
            # Add to the dictionary
            self.history_chats[key] = file

        self.history_frame = customtkinter.CTkScrollableFrame(master=master)
        self.history_frame.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="nsw", rowspan=2)

        self.history_label = customtkinter.CTkLabel(master=self.history_frame, text="Chat history", font=("default", 20))
        self.history_label.grid(row=0, column=0, padx=20, pady=(0,0), sticky="nw")

        self.history_buttons = []
        self.update_signal = False
        self.message_data = []

        for i, (key, path) in enumerate(self.history_chats.items()):
            # Use a lambda function to pass the specific path as an argument to load_history
            history_button = customtkinter.CTkButton(master=self.history_frame, text=key, command=lambda p=path: self.load_history(p))
            history_button.grid(row=i+1, column=0, padx=0, pady=(10,0), sticky="we")
            self.history_buttons.append(history_button)
        
    def load_history(self, path):
        print(f"\n{path}")
        with open(path, "r") as f:
            data = json.load(f)
            self.message_data = data
            self.update_signal = True

class ChatFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.chat_frame = customtkinter.CTkScrollableFrame(master=master)
        self.chat_frame.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)

        self.chat_bubbles = []

        
        self.input_frame = customtkinter.CTkFrame(master=master)
        self.input_frame.grid(row=1, column=1, pady=(0,10), padx=10, sticky="swe")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.user_input = customtkinter.CTkTextbox(master=self.input_frame, height=40)
        self.user_input.grid(row=0,column=0, padx=10,pady=10, sticky="nswe")

        self.user_input_button = customtkinter.CTkButton(master=self.input_frame, text=">", command=print("click"), width=50)
        self.user_input_button.grid(row=0, column=1, padx=(0,10), pady=10, sticky="nse")
    
    def render_messages(self, messages):
        
        # First, clear existing messages
        for widget in self.chat_bubbles:
            widget.destroy()
        self.chat_bubbles.clear()

        render_messages = []
        for message in messages:
            is_user = message["role"] == "user" or False
            if "message" in message.keys():
                render_messages.append((message["message"], is_user))

        for i, (message, is_user) in enumerate(render_messages):
            # Create the label with blue background inside the frame
            bubble = customtkinter.CTkLabel(master=self.chat_frame,
                                            text=message, 
                                            wraplength=300,
                                            justify="left",
                                            bg_color="transparent",  # Blue background
                                            corner_radius=10, # Apply rounded corners
                                            fg_color="#144870")
            # Grid the frame with appropriate padding and alignment
            padx, pady = 10, 10
            sticky = "e" if is_user else "w"
            bubble.grid(row=i, column=0, padx=padx, pady=pady, sticky=sticky)

            self.chat_bubbles.append(bubble)

        # Update the UI
        self.update()

        # Update the scroll region
        if hasattr(self.chat_frame, '_parent_canvas'):
            canvas = self.chat_frame._parent_canvas
            canvas.config(scrollregion=canvas.bbox("all"))
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        # Try to access the internal canvas and use yview_moveto
        if hasattr(self.chat_frame, '_parent_canvas'):
            self.chat_frame.update_idletasks()  # Update the UI
            canvas = self.chat_frame._parent_canvas
            canvas.yview_moveto(1.0)

class InterpreterApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Open Interpreter")
        self.geometry("600x480")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=5)

        self.interpreter = interpreter
        self.interpreter.model = "openai/local"
        self.interpreter.api_base = "http://localhost:1234/v1"

        self.path = Path(self.interpreter.conversation_history_path)

        #self.messages = []
        self.update_messages = False
        
        self.history_frame = HistoryFrame(self, self.path)
        self.chat_frame = ChatFrame(self)

        self.check_update_signal()
    
    def check_update_signal(self):
        if self.history_frame.update_signal:
            messages = self.history_frame.message_data
            print(messages)
            self.chat_frame.render_messages(messages)
            self.history_frame.update_signal = False
        self.after(500, self.check_update_signal)

        

if __name__ == "__main__":
    app = InterpreterApp()
    app.mainloop()