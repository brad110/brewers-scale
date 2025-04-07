
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
        americano = ImageTk.PhotoImage(Image.open("Assets/americano.png").resize((200, 200)))
        

        # coffee names for different buttons
        coffeeNames = ["Americano", "Cappuccino", "Frappuccino", "Dalgona", "Long Black", 
                        "Macchiato", "Cortado", "Ristretto", "Affogato", "Frappe", "Red Eye", "Irish", "New"]

        # creates buttons
        self.screens = {}
        for i, name in enumerate(coffeeNames, start=1):
            btn = tk.Button(self.menuFrame, text=name, font=("Georgia", 12), bg='lightgray', image=buttonNormal, borderwidth = 0, command=lambda i=i: self.showScreen(i), compound = 'center')
            btn.image = buttonNormal
            btn.pack(pady=5, fill=tk.X)

        ingredientDescriptions = ["Ingredients: Americano", "Ingredients: Cappuchino", "Ingredients: Frappuchino", 
                        "Ingredients: Dalgona", "Ingredients: Long Black", "Ingredients: Macchiato", "Ingredients: Cortado",
                        "Ingredients: Ristretto", "Ingredients: Affogato", "Ingredients: Frappe", "Ingredients: Red Eye", 
                        "Ingredients: Irish", "[Insert text]"]
        
        # creates screens
        for i, (name, description) in enumerate(zip(coffeeNames, ingredientDescriptions), start=1):
            frame = tk.Frame(self.contentFrame, bg='white')
            
            coffeeName = tk.Label(frame, text=name, height = 2, width = 22, borderwidth = 10, relief='ridge', font=("Georgia", 33), bg='grey')

            # (ignore this line) for i, image in enumerate(images, start=1):
            coffeeImage = tk.Label(frame, image=americano, bg='WHITE', borderwidth=6, relief='ridge')
            coffeeImage.image = americano
            
            backButton = tk.Button(frame, text="Back to Main Menu", command=lambda: self.showScreen(0))
            
            historyText = tk.Label(frame, text='History', height =5, width =34, borderwidth = 5, relief='ridge', font=("georgia", 22), bg='grey', anchor='nw')
            
            ingredientText = tk.Label(frame, text=description, height =5, width =34, borderwidth = 5, relief='ridge', font=("georgia", 22), bg='grey', anchor='nw')
            # time for place
            coffeeImage.place(x=60, y=20)
            coffeeName.place(x=370, y=30)
            backButton.place(x=500, y=0)
            ingredientText.place(x=372, y=181)
            historyText.place(x=372, y=382)
            
            
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