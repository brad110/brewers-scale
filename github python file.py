import json
from tkinter import filedialog, messagebox
from templateText import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import os

CUSTOMDRINKSFILE = "customDrinks.json"

class MultiScreenGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Brewer's Scale")
        self.root.geometry("1200x650")

        # Load the background image for the content frame
        background_image = ImageTk.PhotoImage(Image.open("Assets/background.png").resize((1200, 650)))

        # Creates a frame for the buttons on the left with a scroll bar
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
        self.buttonNormal = ImageTk.PhotoImage(Image.open("Assets/GreyButton.png").resize((100, 30)))
        self.homebutton = ImageTk.PhotoImage(Image.open("Assets/homebutton.png").resize((60, 60)))

        # value to store what button is active to show different button
        self.activeButton = None
        
        # creates buttons
        self.screens = {}
        self.buttonList = []
        self.customDrinks = self.loadCustomDrinks()

        for i, name in enumerate(coffeeNames, start=1):
            btn = tk.Button(self.menuFrame, text=name, font=("Georgia", 12), bg='lightgray', image=self.buttonNormal, borderwidth=0, height = 45, width= 190, compound='center')
            btn.image = self.buttonNormal
            btn.pack(pady=1, fill=tk.X)
            btn.configure(command=lambda i=i, b=btn: self.buttonPressed(i, b))
            self.buttonList.append(btn)

        # loop creates drink screen for just the default drinks
        for i, (name, description, image, drink) in enumerate(zip(coffeeNames, ingredientDescriptions, imagePaths, drinkDescriptions), start=1):
            self.createScreen(i, name, description, drink, image)

        # loop creates screens for custom drinks in json file
        customDrinkIndex = len(coffeeNames) + 1
        for name, data in self.customDrinks.items():
            self.createCustomScreen(customDrinkIndex, name, data)
            customDrinkIndex += 1

        # button for adding new drink
        addNewBtn = tk.Button(self.menuFrame, text= "New Drink", font=("Georiga", 12),  bg='lightgray', image=self.buttonNormal, borderwidth=0, height = 45, width= 190, compound='center', command = self.customDrinkPopup)
        addNewBtn.pack(pady=10, fill=tk.X)

        

        # Main menu screen
        self.mainScreen = tk.Frame(self.mainFrame, bg='white')
        mainLabel = tk.Label(self.mainScreen, text="Brewer's Scale", font=("Georgia", 20), bg='white')
        mainLabel.pack(pady=20)
        my_label = tk.Label(self.mainScreen, image=mainMenuImage, bg='WHITE')
        my_label.image = mainMenuImage
        my_label.pack()
        self.screens[0] = self.mainScreen

        self.showScreen(0)  # shows main screen

    # loads data from json file for saved drinks
    def loadCustomDrinks(self):
        if os.path.exists(CUSTOMDRINKSFILE):
            with open(CUSTOMDRINKSFILE, 'r') as file:
                return json.load(file)
        return {}
    
    # save custom drinks to json file
    def saveCustomDrinks(self):
        with open(CUSTOMDRINKSFILE, 'w') as file:
            json.dump(self.customDrinks, file, indent=4)
    
    
    # pop up screen for adding drink
    def customDrinkPopup(self):
        top = tk.Toplevel(self.root)
        top.title("Add New Drink")

        # entry fields for name, decription, ingredients
        tk.Label(top, text="Name:").pack()
        nameEntry = tk.Entry(top)
        nameEntry.pack()

        tk.Label(top, text="Description:").pack()
        dscEntry = tk.Entry(top)
        dscEntry.pack()

        tk.Label(top, text="Ingredients:").pack()
        ingredientEntry = tk.Entry(top)
        ingredientEntry.pack()

        # setting up default image used for custom drinks
        defaultImgPath = "Assets/customDefault.png"
        # save drink button
        def saveDrink():
            name = nameEntry.get()
            description = dscEntry.get()
            ingredients = ingredientEntry.get()
            image = defaultImgPath

            if name and image:
                self.customDrinks[name] = {
                    "description": description,
                    "ingredients": ingredients,
                    "image": image
                }
                self.saveCustomDrinks()
                index = len(self.screens)
                self.createCustomScreen(index, name, self.customDrinks[name])
                top.destroy()

        tk.Button(top, text = "Save", command = saveDrink).pack(pady = 10)
    
    # deletes custom drink by name and screen
    def delCustomDrink(self, name, screenID):
        if messagebox.askyesno("Delete", f"Delete '{name}'?"):
            if name in self.customDrinks:
                # remove from data and save
                del self.customDrinks[name]
                self.saveCustomDrinks()

                # destroys the screen
                if screenID in self.screens:
                    self.screens[screenID].destroy()
                    del self.screens[screenID]

                # finds and removes the button by name
                for i, btn in enumerate(self.buttonList):
                    if btn.cget("text") == name:
                        btn.destroy()
                        del self.buttonList[i]
                        break  

                self.showScreen(0)
                self.activeButton = None

                # re-bind buttons with correct indices
                for i, btn in enumerate(self.buttonList, start=1):
                    btn.configure(command=lambda i=i, b=btn: self.buttonPressed(i, b))
    
    # creates button and new screen for custom drinks
    def createCustomScreen(self, screenID, name, data):
        btn = tk.Button(self.menuFrame, text=name, font=("Georgia", 12), bg='lightgray', image=self.buttonNormal, borderwidth=0, height=60, width=190, compound='center')
        btn.image = self.buttonNormal
        btn.pack(pady=1, fill=tk.X)
        btn.configure(command=lambda i=screenID, b=btn: self.buttonPressed(i, b))
        self.buttonList.append(btn)
        self.createScreen(screenID, name, data["ingredients"], data["description"], data["image"], is_custom=True)
    
    # create drink screen for defaults and customs
    def createScreen(self, index, name, ingredients, description, imagePath, is_custom = False):
        frame = tk.Frame(self.mainFrame)
        bg_image = Image.open("Assets/background.png").resize((1200, 650))  # or whatever your frame size is
        bg_image_tk = ImageTk.PhotoImage(bg_image)
        background_label = tk.Label(frame, image=bg_image_tk)
        background_label.image = bg_image_tk  # prevent garbage collection
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        coffeeName = tk.Label(frame, text=name, height=2, width=22, borderwidth=10, relief='ridge', font=("Georgia", 33), bg='lightgrey')

        # Load image for the specific coffee
        coffeeImage = ImageTk.PhotoImage(Image.open(imagePath).resize((150, 150)))  # Resize image to fit better
        coffeeImageLabel = tk.Label(frame, image=coffeeImage, bg='WHITE', borderwidth=6, relief='ridge')
        coffeeImageLabel.image = coffeeImage  # Keep reference to the image to prevent garbage collection

        backButton = tk.Button(frame, text="Back to Main Menu", bg="blue", image=self.homebutton, borderwidth=0, height=57, width=57, command=lambda: self.showScreen(0))
        backButton.image = self.homebutton
        delButton = tk.Button(frame, text="Delete Drink", fg="red", command=lambda: self.delCustomDrink(name, index)) if is_custom else None

        lightButton = tk.Button(frame, text="Light", width=19)
        standardButton = tk.Button(frame, text="Standard", width=19)
        strongButton = tk.Button(frame, text="Strong", width=19)

        groundsButton = tk.Button(frame, text="Beans / Grounds", width=19)
        waterButton = tk.Button(frame, text="Water", width=19)

        ratioDisplay = tk.Label(frame, text="X:X", height=3, width=9, borderwidth=5, relief='ridge', font=("georgia", 19), bg='orange', wraplength=600)

        strengthLabel = tk.Label(frame, text="Strength", height=2, width=9, borderwidth=5, relief='ridge', font=("georgia", 19), bg='lightblue', wraplength=600)

        weightLabel = tk.Label(frame, text="Weighed", height=2, width=9, borderwidth=5, relief='ridge', font=("georgia", 19), bg='lightblue', wraplength=600)

        descriptionText = tk.Label(frame, text=description, height=7, width=36, borderwidth=5, relief='ridge', font=("georgia", 20), bg='lightgrey', wraplength=570)

        ingredientText = tk.Label(frame, text=ingredients, height=5, width=34, borderwidth=5, relief='ridge', font=("georgia", 22), bg='lightgrey', wraplength=570)

        # Positioning widgets
        coffeeImageLabel.place(x=70, y=20)
        coffeeName.place(x=370, y=30)
        backButton.place(x=2, y=00)
        ingredientText.place(x=372, y=181)
        descriptionText.place(x=372, y=382)
        ratioDisplay.place(x=77, y=200)
        strengthLabel.place(x=77, y=320)
        weightLabel.place(x=77, y=500)
        lightButton.place(x=78, y=390)
        standardButton.place(x=78, y=415)
        strongButton.place(x=78, y=440)
        groundsButton.place(x=78, y=570)
        waterButton.place(x=78, y=595)
        if delButton:
            delButton.place(x=700, y=0)

        self.screens[index] = frame

    
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
