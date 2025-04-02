
import tkinter as tk
# imports updated buttons and labels
from tkinter import ttk


class MultiScreenGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Brewer's Scale")
        self.root.geometry("800x600")

        # creates a frame for the buttons on the left
        self.menuFrame = tk.Frame(root, width=200, bg='lightgray')
        self.menuFrame.pack(side=tk.LEFT, fill=tk.Y)

        # creates a frame for the content on the right
        self.contentFrame = tk.Frame(root, bg='white')
        self.contentFrame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # coffee names for different buttons
        coffeeNames = ["Americano", "Cappuccino", "Frappuccino", "Dalgona", "Long Black", 
                        "Macchiato", "Cortado", "Ristretto", "Affogato", "Frappe", "Red Eye", "Irish"]

        # creates buttons
        self.screens = {}
        for i, name in enumerate(coffeeNames, start=1):
            btn = tk.Button(self.menuFrame, text=name, command=lambda i=i: self.showScreen(i))
            btn.pack(pady=5, fill=tk.X)

        # creates screens 
        for i, name in enumerate(coffeeNames, start=1):
            frame = tk.Frame(self.contentFrame, bg='white')
            label = tk.Label(frame, text=name, font=("Arial", 16), bg='white')
            label.pack(pady=20)
            backButton = tk.Button(frame, text="Back to Main Menu", command=lambda: self.showScreen(0))
            backButton.pack()
            self.screens[i] = frame

        # Main menu screen
        self.mainScreen = tk.Frame(self.contentFrame, bg='white')
        mainLabel = tk.Label(self.mainScreen, text="Brewer's Scale", font=("Arial", 20), bg='white')
        mainLabel.pack(pady=20)
        self.screens[0] = self.mainScreen
        
        self.showScreen(0) #shows main screen

    def showScreen(self, screenNumber):
        # removes current frame so it can display new screen
        for widget in self.contentFrame.winfo_children():
            widget.pack_forget()
        # displays the selected screen
        self.screens[screenNumber].pack(expand=True, fill=tk.BOTH)


##############################################################################
                            ### MAIN ###
##############################################################################

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiScreenGui(root)
    root.mainloop()