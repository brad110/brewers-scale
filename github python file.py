import json
from tkinter import filedialog, messagebox
from templateText import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import os

CUSTOMDRINKSFILE = "customDrinks.json"

strengthValue = strengthStandard
sizeValue = sizeNormal

class MultiScreenGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Brewer's Complement")
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
        self.homebuttonWhiteBG = ImageTk.PhotoImage(Image.open("Assets/homebuttonWhiteBG.png").resize((60, 60)))
        self.strengthbutton = ImageTk.PhotoImage(Image.open("Assets/strengthbutton.png").resize((141, 19)))
        self.pressedButtonImage = ImageTk.PhotoImage(Image.open("Assets/buttonPressed.png").resize((100, 30)))

        # value to store what button is active to show different button
        self.activeButton = None
        
        

        # creates buttons
        self.screens = {}
        self.buttonList = []
        self.customDrinks = self.loadCustomDrinks()


        for i, name in enumerate(coffeeNames, start=1):
            btn = tk.Button(self.menuFrame, text=name, font=("Georgia", 12), bg='lightgray', image=self.buttonNormal, borderwidth=0, height = 45, width= 190, compound='center')
            btn.normalImage = self.buttonNormal
            btn.pressedImage = self.pressedButtonImage
            btn.pack(pady=1, fill=tk.X)
            btn.configure(command=lambda i=i, b=btn: self.buttonPressed(i, b))
            self.buttonList.append(btn)

        # loop creates drink screen for just the default drinks
        for i, (name, description, image, drink, r1, r2) in enumerate(zip(coffeeNames, ingredientDescriptions, imagePaths, drinkDescriptions, ratioCounterValues1, ratioCounterValues2), start=1):
            self.createScreen(i, name, description, drink, image, r1, r2)

        # button for adding new drink
        self.addNewBtn = tk.Button(self.menuFrame, text= "New Drink", font=("Georiga", 12),  bg='lightgray', image=self.buttonNormal, borderwidth=0, height = 45, width= 190, compound='center', command = self.customDrinkPopup)
        self.addNewBtn.pack(pady=1, fill=tk.X)
        # loop creates screens for custom drinks in json file
        customDrinkIndex = len(coffeeNames) + 1
        for name, data in self.customDrinks.items():
            self.createCustomScreen(customDrinkIndex, name, data)
            customDrinkIndex += 1

        

        # Main menu screen
        self.mainScreen = tk.Frame(self.mainFrame, bg='white')
        mainLabel = tk.Label(self.mainScreen, text="Brewer's Complement", font=("Segoe UI", 30, "bold"), bg='white')
        mainLabel.pack(pady=20)
        my_label = tk.Label(self.mainScreen, image=mainMenuImage, bg='WHITE')
        my_label.image = mainMenuImage
        my_label.pack()
        infoButton = tk.Button(self.mainScreen, text="Info", font=("Arial", 12, "bold"), bg="lightgray", command=self.showInfoWindow)
        infoButton.pack(pady=10)
        self.screens[0] = self.mainScreen

        self.showScreen(0)  # shows main screen

    def showInfoWindow(self):
        infoFrame = tk.Frame(self.mainFrame, bg='white')
        title = tk.Label(infoFrame, text="About Brewer's Complement", font=("Segoe UI", 26, "bold"), bg="white")
        title.pack(pady=20)

                                    # put info text here #
        description = tk.Label(infoFrame, text="The Brewer's Scale is an application designed for use during the coffee brewing process. Some additional information is needed in order to accurately use this application. For each template, the ratios of ingredients will not have specifications for what order they appear in. This is because the ratios are meant to be read in the order that they appear in the 'ingredients' section of each template, from left to right. The size measurements changed by the 'size' buttons are as follows: Small: 8oz, Normal: 12oz, Large: 16oz.", font=("Georgia", 16), justify="center", height=305, width=76, borderwidth=5, relief='ridge', bg='lightgrey', wraplength=570)
        description.pack(pady=10)

        closeButton = tk.Button(infoFrame, text="Back to Main Menu", font=("Georgia", 14), bg="lightgray", image=self.homebuttonWhiteBG, borderwidth=0, height=57, width=57, command=lambda: self.closeInfoWindow(infoFrame))
        closeButton.image = self.homebuttonWhiteBG
        closeButton.place(x=2, y=00)
        self.screens['info'] = infoFrame
        self.showScreen('info')
    
    def closeInfoWindow(self, infoFrame):
        infoFrame.destroy()
        self.showScreen(0)

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
    
    def changeStrengthValue(self, newStrength, ratioDisplay, r1, r2):
            global strengthValue
            strengthValue = newStrength
            ratio1 = round(r1 * strengthValue * sizeValue, 1)
            ratio2 = round(r2 * strengthValue * sizeValue, 1)
            ratioDisplay.config(text=f"{ratio1}:{ratio2}")
            
    def changeSizeValue(self, newSize, ratioDisplay, r1, r2):
            global sizeValue
            sizeValue = newSize
            ratio1 = round(r1 * strengthValue * sizeValue, 1)
            ratio2 = round(r2 * strengthValue * sizeValue, 1)
            ratioDisplay.config(text=f"{ratio1}:{ratio2}")
    
    # pop up screen for adding drink
    def customDrinkPopup(self):
        top = tk.Toplevel(self.root)
        top.title("Add New Drink")
        top.geometry("350x250+600+300")
        top.resizable(False, False)

        # validation command for character limit
        vcnd = (top.register(self.validate_name), '%P')
        vcdd = (top.register(self.validate_description), '%P')
        vcid = (top.register(self.validate_ingredients), '%P')
        vcr1d = (top.register(self.validate_ingredientratio), '%P')
        vcr2d = (top.register(self.validate_ingredientratio2), '%P')

        # entry fields for name, decription, ingredients
        tk.Label(top, text="Name:").pack()
        nameEntry = tk.Entry(top, validate='key', validatecommand=vcnd)
        nameEntry.pack()

        tk.Label(top, text="Description:").pack()
        dscEntry = tk.Entry(top, validate='key', validatecommand=vcdd)
        dscEntry.pack()

        tk.Label(top, text="Ingredients:").pack()
        ingredientEntry = tk.Entry(top, validate='key', validatecommand=vcid)
        ingredientEntry.pack()

        tk.Label(top, text="Ingredient 1 Ratio:").pack()
        r1Entry = tk.Entry(top, validate='key', validatecommand=vcr1d)
        r1Entry.pack()

        tk.Label(top, text="Ingredient 2 Ratio:").pack()
        r2Entry = tk.Entry(top, validate='key', validatecommand=vcr2d)
        r2Entry.pack()

        # setting up default image used for custom drinks
        defaultImgPath = "Assets/customDefault.png"
        # save drink button
        def saveDrink():
            name = nameEntry.get()
            description = dscEntry.get()
            ingredients = ingredientEntry.get()
            image = defaultImgPath
            try:
                r1 = float(r1Entry.get())
                r2 = float(r2Entry.get())
            except ValueError:
                messagebox.showerror("Invalid Input", "Ratio values must be numbers.")
                return

            if name and image:
                self.customDrinks[name] = {
                    "description": description,
                    "ingredients": ingredients,
                    "image": image,
                    "r1": r1,
                    "r2": r2
                    }
                self.saveCustomDrinks()
                index = len(self.screens)
                self.createCustomScreen(index, name, self.customDrinks[name])
                top.destroy()

        tk.Button(top, text = "Save", command = saveDrink).pack(pady = 10)
    
    # validation method for limiting name length
    def validate_name(self, new_value):
        return len(new_value) <= 20
    
    # validation method for limiting description length
    def validate_description(self, new_value):
        return len(new_value) <= 350
    
    # validaiton method for limiting ingredients length
    def validate_ingredients(self, new_value):
        return len(new_value) <= 60
    
    # validaiton method for limiting ingredient 1 ratio length
    def validate_ingredientratio(self, new_value):
        return len(new_value) <= 3
    
    # validaiton method for limiting ingredients length
    def validate_ingredientratio2(self, new_value):
        return len(new_value) <= 3
    
    # deletes custom drink by name and screen
    def delCustomDrink(self, name, screenID):
        if messagebox.askyesno("Delete", f"Delete '{name}'?"):
            if name in self.customDrinks:
                # Remove from data and save
                del self.customDrinks[name]
                self.saveCustomDrinks()

                # Destroy the screen
                if screenID in self.screens:
                    self.screens[screenID].destroy()
                    del self.screens[screenID]

                # Remove the button from buttonList
                for i, btn in enumerate(self.buttonList):
                    if btn.cget("text") == name:
                        btn.destroy()
                        del self.buttonList[i]
                        break  

                # Repack all buttons to adjust layout
                self.repackMenuButtons()

                # Show the main screen
                self.showScreen(0)
                self.activeButton = None

    def repackMenuButtons(self):
        # this function handles the error it causes after deleting custom drinks and the buttons not packing correctly
        for widget in self.menuFrame.winfo_children():
            widget.pack_forget()

        for btn in self.buttonList:
            btn.pack(pady=1, fill=tk.X)

        self.addNewBtn.pack(pady=1, fill=tk.X)

    # creates button and new screen for custom drinks
    def createCustomScreen(self, screenID, name, data):
        btn = tk.Button(self.menuFrame, text=name, font=("Georgia", 12), bg='lightgray', image=self.buttonNormal, borderwidth=0, height=45, width=190, compound='center')
        btn.normalImage = self.buttonNormal
        btn.pressedImage = self.pressedButtonImage
        btn.pack(pady=1, fill=tk.X, before=self.addNewBtn)
        btn.configure(command=lambda i=screenID, b=btn: self.buttonPressed(i, b))
        self.buttonList.append(btn)
        self.menuFrame.update_idletasks()
        self.menuFrame.master.configure(scrollregion=self.menuFrame.master.bbox("all"))
        self.repackMenuButtons()
        self.createScreen(screenID, name, data["ingredients"], data["description"], data["image"], data["r1"], data["r2"], is_custom=True)

        
    
    # create drink screen for defaults and customs
    def createScreen(self, index, name, ingredients, description, imagePath, r1, r2, is_custom = False):
        frame = tk.Frame(self.mainFrame)
        bg_image = Image.open("Assets/background.png").resize((1200, 650))
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

        lightButton = tk.Button(frame, image=self.strengthbutton, text="Light", compound='center', command=lambda: self.changeStrengthValue(strengthLight, ratioDisplay, r1, r2))
        standardButton = tk.Button(frame, text="Standard",compound='center', image=self.strengthbutton, command=lambda: self.changeStrengthValue(strengthStandard, ratioDisplay, r1, r2))
        strongButton = tk.Button(frame, text="Strong",compound='center', image=self.strengthbutton, command=lambda: self.changeStrengthValue(strengthStrong, ratioDisplay, r1, r2))

        smallButton = tk.Button(frame, image=self.strengthbutton, compound='center', text="Small", command=lambda: self.changeSizeValue(sizeSmall, ratioDisplay, r1, r2))
        normalButton = tk.Button(frame, image=self.strengthbutton, compound='center', text="Normal", command=lambda: self.changeSizeValue(sizeNormal, ratioDisplay, r1, r2))
        largebutton= tk.Button(frame, image=self.strengthbutton, compound='center', text="Large", command=lambda: self.changeSizeValue(sizeLarge, ratioDisplay, r1, r2))

        ratioDisplay = tk.Label(frame, text=f"{r1 * strengthValue * sizeValue}:{r2 * strengthValue * sizeValue}", height=3, width=9, borderwidth=5, relief='ridge', font=("georgia", 19), bg='orange', wraplength=600)

        strengthLabel = tk.Label(frame, text="Strength", height=2, width=9, borderwidth=5, relief='ridge', font=("georgia", 19), bg='lightblue', wraplength=600)

        weightLabel = tk.Label(frame, text="Size", height=2, width=9, borderwidth=5, relief='ridge', font=("georgia", 19), bg='lightblue', wraplength=600)

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
        lightButton.place(x=76, y=390)
        standardButton.place(x=76, y=415)
        strongButton.place(x=76, y=440)
        smallButton.place(x=76, y=570)
        normalButton.place(x=76, y=595)
        largebutton.place(x=76, y=620)
        if delButton:
            delButton.place(x=700, y=0)

        self.screens[index] = frame

    
    def showScreen(self, screenNumber):
        # removes current frame so it can display new screen
        if screenNumber == 0 or screenNumber == 'info':
            if self.activeButton:
                try:
                    self.activeButton.config(bg='lightgray', image=self.activeButton.normalImage)
                except tk.TclError:
                    pass
                self.activeButton = None

        for widget in self.mainFrame.winfo_children():
            widget.pack_forget()


        self.screens[screenNumber].pack(expand=True, fill=tk.BOTH)
    
    # function for detecting if button is pressed
    def buttonPressed(self, screenNumber, button):
        # Reset previous active button color
        if self.activeButton:
            self.activeButton.config(bg='lightgray', image = self.activeButton.normalImage)
            
        # Highlight the new active button
        button.config(bg='darkgray', image = button.pressedImage)
        
    
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
