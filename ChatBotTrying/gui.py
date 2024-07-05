import tkinter as tk
from chatbot import Chatbot

class GUI:
    def __init__(self):
        try:
            self.chatbot = Chatbot() 

            self.root = tk.Tk()
            self.root.title("Chatbot")

            self.chat_history = tk.Text(self.root, height=20, width=50, wrap=tk.WORD)
            self.chat_history.pack(padx=10, pady=10)

            # Scrollbarr
            scrollbar = tk.Scrollbar(self.root, command=self.chat_history.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.chat_history.config(yscrollcommand=scrollbar.set)

            
            self.entry = tk.Entry(self.root, width=50)
            self.entry.pack(padx=10, pady=10)
            ##Sorunumuz chat box kısmına kullanıcı etkileşime girebiliyordu. Hallettim...
            self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
            self.send_button.pack(pady=5)
        except Exception as e:
            print("ekran açılmasında problem")

    def send_message(self):
        try:
            user_input = self.entry.get().strip()
            if not user_input:
                return

            # Kullanıcının girdiği metni chate ekleme
            self.chat_history.config(state=tk.NORMAL)
            self.chat_history.insert(tk.END, "You: " + user_input + "\n")

            # Chatbot cevabını alma chate ekleme....
            response = self.chatbot.get_response(user_input)
            self.chat_history.insert(tk.END, "Chatbot: " + response + "\n\n")

        
            self.entry.delete(0, tk.END)
            self.chat_history.config(state=tk.DISABLED)

            
            self.chat_history.see(tk.END)
        except Exception as e:
            print("Error")

    def run(self):
        try:
            print("...")
            self.root.mainloop()
        except Exception as e:
            print("Error")

if __name__ == "__main__":
    gui = GUI()
    gui.run()
