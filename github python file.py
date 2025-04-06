
import tkinter as tk
# imports updated buttons and labels
from tkinter import ttk
from PIL import ImageTk, Image


class MultiScreenGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Brewer's Scale")
        self.root.geometry("1200x650")

        # creates a frame for the buttons on the left
        self.menuFrame = tk.Frame(root, width=200, bg='lightgray')
        self.menuFrame.pack(side=tk.LEFT, fill=tk.Y)

        # creates a frame for the content on the right
        self.contentFrame = tk.Frame(root, bg='white')
        self.contentFrame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        # Creating images
        mainMenuImage = ImageTk.PhotoImage(Image.open("Assets/logo-removebg-preview.png"))
        buttonNormal = ImageTk.PhotoImage(Image.open("Assets/GreyButton.png").resize((100, 30)))
        placeholder = ImageTk.PhotoImage(Image.open("Assets/placeholder.png").resize((200, 200)))
        

        # coffee names for different buttons
        coffeeNames = ["Americano", "Cappuccino", "Frappuccino", "Dalgona", "Long Black", 
                        "Macchiato", "Cortado", "Ristretto", "Affogato", "Frappe", "Red Eye", "Irish",]

        # creates buttons
        self.screens = {}
        for i, name in enumerate(coffeeNames, start=1):
            btn = tk.Button(self.menuFrame, text=name, font=("Georgia", 12), bg='lightgray', image=buttonNormal, borderwidth = 0, command=lambda i=i: self.showScreen(i), compound = 'center')
            btn.image = buttonNormal
            btn.pack(pady=5, fill=tk.X)

        # creates screens 
        for i, name in enumerate(coffeeNames, start=1):
            frame = tk.Frame(self.contentFrame, bg='white')
            
            coffeeName = tk.Label(frame, text=name, height = 2, width = 22, borderwidth = 10, relief='ridge', font=("Georgia", 33), bg='grey')

            # (ignore this line) for i, image in enumerate(images, start=1):
            coffeeImage = tk.Label(frame, image=placeholder, bg='WHITE', borderwidth=6, relief='ridge')
            coffeeImage.image = placeholder
            
            backButton = tk.Button(frame, text="Back to Main Menu", command=lambda: self.showScreen(0))
 
            # time for place
            coffeeImage.place(x=20, y=20)
            coffeeName.place(x=330, y=30)
            
            
            self.screens[i] = frame

        # Main menu screen
        self.mainScreen = tk.Frame(self.contentFrame, bg='white')
        mainLabel = tk.Label(self.mainScreen, text="Brewer's Scale", font=("Georgia", 20), bg='white')
        mainLabel.pack(pady=20)
        my_label = tk.Label(self.mainScreen, image=mainMenuImage, bg='WHITE')
        my_label.image = mainMenuImage
        my_label.pack()
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