import json
from templateText import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

class MultiScreenGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Brewer's Scale")
        self.root.geometry("1200x650")

        # Load the background image for the content frame
        background_image = ImageTk.PhotoImage(Image.open("Assets/background.png").resize((1200, 650)))

        # Creates a frame for the buttons on the left
        menuContainer = tk.Frame(root, width=200, bg='lightgray')
        menuContainer.pack(side=tk.LEFT, fill=tk.Y)

        menuCanvas = tk.Canvas(menuContainer, bg='lightgray', width=200, highlightthickness=0)
        menuCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(menuContainer, orient=tk.VERTICAL, command=menuCanvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        menuCanvas.configure(yscrollcommand=scrollbar.set)
        menuCanvas.bind('<Configure>', lambda e: menuCanvas.configure(scrollregion=menuCanvas.bbox("all")))

        self.menuFrame = tk.Frame(menuCanvas, bg='lightgray')
        menuCanvas.create_window((0, 0), window=self.menuFrame, anchor="nw")


        self.mainFrame = tk.Frame(root, bg='blue')
        self.mainFrame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
       

        # Creating images
        mainMenuImage = ImageTk.PhotoImage(Image.open("Assets/logo-removebg-preview.png"))
        buttonNormal = ImageTk.PhotoImage(Image.open("Assets/GreyButton.png").resize((100, 30)))

        # value to store what button is active to show different button
        self.activeButton = None
        
        # creates buttons
        self.screens = {}
        self.buttonList = []

        for i, name in enumerate(coffeeNames, start=1):
            btn = tk.Button(self.menuFrame, text=name, font=("Georgia", 12), bg='lightgray', image=buttonNormal, borderwidth=0, height = 45, width= 190, compound='center')
            btn.image = buttonNormal
            btn.pack(pady=1, fill=tk.X)
            btn.configure(command=lambda i=i, b=btn: self.buttonPressed(i, b))
            self.buttonList.append(btn)

        # creates screens
        for i, (name, description, image, drink) in enumerate(zip(coffeeNames, ingredientDescriptions, imagePaths, drinkDescriptions), start=1):
            frame = tk.Frame(self.mainFrame)
            bg_image = Image.open("Assets/background.png").resize((1200, 650))  # or whatever your frame size is
            bg_image_tk = ImageTk.PhotoImage(bg_image)
            background_label = tk.Label(frame, image=bg_image_tk)
            background_label.image = bg_image_tk  # prevent garbage collection
            background_label.place(x=0, y=0, relwidth=1, relheight=1)

            coffeeName = tk.Label(frame, text=name, height=2, width=22, borderwidth=10, relief='ridge', font=("Georgia", 33), bg='lightgrey')

            # Load image for the specific coffee
            coffeeImage = ImageTk.PhotoImage(Image.open(imagePaths[i-1]).resize((150, 150)))  # Resize image to fit better
            coffeeImageLabel = tk.Label(frame, image=coffeeImage, bg='WHITE', borderwidth=6, relief='ridge')
            coffeeImageLabel.image = coffeeImage  # Keep reference to the image to prevent garbage collection

            backButton = tk.Button(frame, text="Back to Main Menu", command=lambda: self.showScreen(0))

            lightButton = tk.Button(frame, text="Light", width=19)
            standardButton = tk.Button(frame, text="Standard", width=19)
            strongButton = tk.Button(frame, text="Strong", width=19)

            groundsButton = tk.Button(frame, text="Beans / Grounds", width=19)
            waterButton = tk.Button(frame, text="Water", width=19)

            ratioDisplay = tk.Label(frame, text="X:X", height=3, width=9, borderwidth=5, relief='ridge', font=("georgia", 19), bg='orange', wraplength=600)

            strengthLabel = tk.Label(frame, text="Strength", height=2, width=9, borderwidth=5, relief='ridge', font=("georgia", 19), bg='lightblue', wraplength=600)

            weightLabel = tk.Label(frame, text="Weighed", height=2, width=9, borderwidth=5, relief='ridge', font=("georgia", 19), bg='lightblue', wraplength=600)

            descriptionText = tk.Label(frame, text=drink, height=7, width=36, borderwidth=5, relief='ridge', font=("georgia", 20), bg='lightgrey', anchor='nw', wraplength=570)

            ingredientText = tk.Label(frame, text=description, height=5, width=34, borderwidth=5, relief='ridge', font=("georgia", 22), bg='lightgrey', anchor='nw', wraplength=570)

            # Positioning widgets
            coffeeImageLabel.place(x=60, y=20)
            coffeeName.place(x=370, y=30)
            backButton.place(x=500, y=0)
            ingredientText.place(x=372, y=181)
            descriptionText.place(x=372, y=382)
            ratioDisplay.place(x=67, y=200)
            strengthLabel.place(x=67, y=320)
            weightLabel.place(x=67, y=500)
            lightButton.place(x=68, y=390)
            standardButton.place(x=68, y=415)
            strongButton.place(x=68, y=440)
            groundsButton.place(x=68, y=570)
            waterButton.place(x=68, y=595)

            self.screens[i] = frame

        # Main menu screen
        self.mainScreen = tk.Frame(self.mainFrame, bg='white')
        mainLabel = tk.Label(self.mainScreen, text="Brewer's Scale", font=("Georgia", 20), bg='white')
        mainLabel.pack(pady=20)
        my_label = tk.Label(self.mainScreen, image=mainMenuImage, bg='WHITE')
        my_label.image = mainMenuImage
        my_label.pack()
        self.screens[0] = self.mainScreen

        self.showScreen(0)  # shows main screen

    def showScreen(self, screenNumber):
        # removes current frame so it can display new screen
        for widget in self.mainFrame.winfo_children():
            widget.pack_forget()
        # displays the selected screen
        self.screens[screenNumber].pack(expand=True, fill=tk.BOTH)
    
    # function for detecting if button is pressed
    def buttonPressed(self, screenNumber, button):
        # Reset previous active button color
        if self.activeButton:
            self.activeButton.config(bg='lightgray')

        # Highlight the new active button
        button.config(bg='darkgray')
        self.activeButton = button

        # Show the corresponding screen
        self.showScreen(screenNumber)


##############################################################################
                            ### MAIN ###
##############################################################################

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiScreenGui(root)
    root.mainloop()
