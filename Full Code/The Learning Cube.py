import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
from tkinter.messagebox import showerror, askokcancel, showinfo
from tkinter import filedialog
import sqlite3
import random
from random import randint, shuffle
import time
from fractions import *

conn = sqlite3.connect('TLC.db')
c = conn.cursor()
REALLY_LARGE_FONT = ("Verdana", 30)
LARGE_FONT = ("Verdana", 12)
HUGE_FONT = ("Verdana", 10)
BIG_FONT = ("Verdana", 20)
Med_Font = ("Verdana", 15)
Card_FONT = ("Verdana", 9)
Title_Font = ("Verdana", 45, "bold")

class LogIn(tk.Tk): # I have inherited the tk class from tkinter.
    def __init__(self): # The method is inialisation, when LogIn runs so to will the method
        tk.Tk.__init__(self) # Initalise tkinter

        tk.Tk.title(self, "Log In") # The title of the page
        self.configure(background="#a1dbcd") # Settting the background and the components for the GUI
        TitleImage = tk.PhotoImage(file=r"The Learning CubeTitle.gif")
        TitleImageLabel = tk.Label(self, image=TitleImage, bg="#a1dbcd")
        TitleImageLabel.image = TitleImage # Must be referneced in order to work, that is why later I have to use global with profile picture
        TitleImageLabel.grid(pady=10, padx=10, column=1) # the title images is place and shown

        tk.Label(self, text=("PLEASE LOGIN TO YOUR *THELEARNINGCUBE* ACCOUNT"), font=LARGE_FONT, bg="#a1dbcd").grid\
            (pady=10, padx=10, row=1, column=1) # Pady & Padx means the space that the button leaves to next element. So if there was another button next to it, it would leave a space of 10

        tk.Label(self, text="Username", font=LARGE_FONT, bg="#a1dbcd").grid(row=2, column=1)  # as these are both Lael's they do not need to be assigned variables
        self.UsernameEntry = tk.Entry(self) # Here is the input for the password in order to log int"
        self.UsernameEntry.grid(row=3, column=1)

        tk.Label(self, text="Password", font=LARGE_FONT, bg="#a1dbcd").grid(row=4, column=1)
        self.PasswordEntry = tk.Entry(self, show = "*",) # Here the password is starred out so no-one can see it, this is one of my objectives
        self.PasswordEntry.grid(row=5, column=1)

        tk.Button(self, text="Login", fg="orange", bg="#a1dbcd", command=lambda: self.Validation()).grid(row=7, column=1)# When the Button above is pressed, it sends the user through to the method Validation which will determine if User credientals are correct
        Logo = tk.PhotoImage(file=r"JustTheLogo.gif") # Other appearance tools, that place the logo on either side of
        LogoLabel1 = tk.Label(self, image=Logo, background="#a1dbcd") # the title
        LogoLabel1.image = Logo
        LogoLabel1.grid(row=0, column=0)
        LogoLabel2 = tk.Label(self, image=Logo, background="#a1dbcd")
        LogoLabel2.image = Logo
        LogoLabel2.grid(row=0, column=3)

        LogoandTitle = tk.PhotoImage(file=r"TheLearningCube1.gif")
        LogoandTitleLabel = tk.Label(self, image=LogoandTitle, background="#a1dbcd")
        LogoandTitleLabel.image = LogoandTitle
        LogoandTitleLabel.grid(row=9, column=1)

    def Validation(self):
        # Originally, this was the main problem to my program. I could not get the program to run because the class LogIn inhertied from the TLC App, this meant that global Username had no value as Python runs the entire code in runtime, and thus when it got to Customisation, and recieving the user's chosen colour, because there was no user there was no colour and thus the program crashed. In order to correct this, I created a whole new frame for LogIn, where instead of inheriting from the TLCApp, it inhertied directly from tk.Tk. The framewould be destroyed if the LogIn was correct and run the TLCApp class where the program starts.
        global Username # Username is set to global, as the Username will be vital throughout the program, which is why it MUST be unique
        global FrameToBeShown # This is so the program knows which frame to show, if it is an administrator then it will show the UserManagement page, otherwise it will show the Student Hub
        Username = self.UsernameEntry.get() # Getting the information from the Log In form
        Password = self.PasswordEntry.get() #Pa
        c.execute("SELECT * FROM Users WHERE username = ? and password = ?", (Username, Password)) # Check in the database for the user
        self.CorrectUser = c.fetchone() # Return the query's value
        if self.CorrectUser: # If there is a result then
            Authenication = "True" # We know that there is a user, not sure wherther it is an admin or not yet
            c.execute("SELECT Admin FROM Users WHERE  username = ? and password = ?", (Username, Password)) # Check if user is admin
            IsAdmin = c.fetchone() # Return if the user is an admin
            if IsAdmin == ('TRUE',): # If the database has the username entered as an admin
                AuthenicationForAdmin = "True" # The program knows that a user is logged in
            else:
                AuthenicationForAdmin = "False" # Student is logged in
        else: # If self.CorreectUser is empty, then
            showerror("Error!", "Login Failed") # Show Pop Up Error Message
            self.UsernameEntry.delete('0', END) # Clear form, in order for user to try again
            self.PasswordEntry.delete('0', END)
            return # back to inialise
        if Authenication == "True" and AuthenicationForAdmin == "True": # If user is admin
            showinfo("Success", ("You Are Logged In")) # Tell the user that they are logged in. This is because as soon as you log in, the window is destoryed and opened with a new one
            FrameToBeShown = (UserManagement) # If user is a admin, then take user to Admin Choice page
        elif Authenication == "True" and AuthenicationForAdmin == "False":
            showinfo("Success", ("You Are Logged In"))
            FrameToBeShown = (Student_Hub) # If the user is a student, take the user to the Student_Hub
        conn.commit()
        TLCAppMain(self) # Go to TLCAppMain, to destroy the frame and create the program

class TLCApp(tk.Tk): # I have inherited the tk class from tkinter.
    def __init__(self): # Initalise
        tk.Tk.__init__(self) # Initalise tkinter

        tk.Tk.wm_title(self, "The Learning Cube")

        Framecontainer = tk.Frame(self) # The Frame is the window, assiging the framecontainer the window
        Framecontainer.pack(side="top", fill="both", expand=True) # Fills the frame completlely, without it there would be no frame

        self.frames = {} # Here I have used a Dictonary. It references all the frames that will be defined below, and in F would call the name in the dictonary. Here is where all the frames are shown
        self.title("The Learning Cube")

        for F in (Student_Hub, CustomisationChoice, Appearance, MyAccountChoice, ShowScores, ShowUserDetails,
            ProfilePicture, UserManagement, ChoiceForGame, Level1, showLv1LeaderBoard, Level2, showLv2LeaderBoard, Level3, showLv3LeaderBoard, Level4, showLv4LeaderBoard): # All the names in the dictonary correspon to a class, so when it is called with show_frame it works.
            frame = F(Framecontainer, self) # defines frame
            self.frames[F] = frame  # Saves Frame in dictonary.

            frame.grid(row=0, column=0, sticky="nsew") # Stretch in centre, covering the entire screen

        self.show_frame(FrameToBeShown) # That has come from LoggingIn, isn't used when the frame is raised.

    def show_frame(self, controller): #
        frame = self.frames[controller] # controller is the frame that is being called. It seaches the dictonary for the frame returns it
        frame.tkraise() # Brings the frame that is wanted to the front, raise the chosen frame

class Student_Hub(tk.Frame): # Inherits from the frame from TLCApp
    def __init__(self, parent, controller):  # Here, the Parent is equal to the TLCApp, and the controller is "show frame", and it will be used later when I am bringing the frame forward
        tk.Frame.__init__(self, parent) # Initalise the frame
        ColourChosen = Appearance.GetUserColour(Appearance) # Gets the user colour from database
        self.configure(background= ColourChosen) # Sets the background of the colour to the user's option that is saved in the database

        TitleImage = tk.PhotoImage(file=r"The Learning CubeTitle.gif")
        TitleImageLabel = tk.Label(self, image=TitleImage, bg=ColourChosen)
        TitleImageLabel.image = TitleImage
        TitleImageLabel.grid(pady=10, padx=10, column=2) # Shows title

        tk.Button(self, text="PLAY", fg="orange", height=3, width=50, command=lambda: controller.show_frame(ChoiceForGame)).grid(row=1, column=2)  # If button clicked, then ChoiceForGame will be raised to the top

        tk.Button(self, text="CUSTOMISATION", fg="orange", height=3, width=50, command=lambda: controller.show_frame(     CustomisationChoice)).grid(row=3, column=2) # If button clicked, then CustomisationChoice will be raised to the top

        tk.Button(self, text="MY ACCOUNT", fg="orange", height=3, width=50, command=lambda: controller.show_frame(MyAccountChoice)).grid(row=5, column=2) # If button clicked, then MyAccountChoice will be raised to the top

        tk.Button(self, text="EXIT", fg="orange", height=3, width=50, command=self.quit).grid(row=7, column=2) # If button clicked, then CustomisationChoice will be raised to the top

        Logo = tk.PhotoImage(file=r"JustTheLogo.gif")
        LogoLabel1 = tk.Label(self, image=Logo, background=ColourChosen)
        LogoLabel1.image = Logo
        LogoLabel1.grid(row=0, column=0)
        LogoLabel2 = tk.Label(self, image=Logo, background=ColourChosen)
        LogoLabel2.image = Logo
        LogoLabel2.grid(row=0, column=3) # Logos are shown

class CustomisationChoice(tk.Frame):# Inherits from the frame from TLCApp
    def __init__(self, parent, controller): # Parent is TLCApp, controller is "show frame".
        tk.Frame.__init__(self, parent)
        ColourChosen = Appearance.GetUserColour(Appearance)
        self.configure(background= ColourChosen) # Gets User from query and sets the backgroun colour to that

        TitleImage = tk.PhotoImage(file=r"The Learning CubeTitle.gif") # Images
        TitleImageLabel = tk.Label(self, image=TitleImage, bg=ColourChosen)
        TitleImageLabel.image = TitleImage
        TitleImageLabel.grid(pady=10, padx=10, column=1, columnspan=2)

        AppearanceOption = tk.Button(self, text="APPEARANCE OF LEARNING CUBE", fg="orange", height=10, width=50,
                                     command=lambda: controller.show_frame(Appearance))  # If button pressed takes user to the Appearance page
        AppearanceOption.grid(row=3, column=1)
        ChangeAvatarOption = tk.Button(self, text="CHANGE AVATAR", fg = "orange", height=10, width=50,
                                       command=lambda: controller.show_frame(ProfilePicture))  # If button pressed takes user to where they can change their password
        ChangeAvatarOption.grid(row=3, column=2)

        ReturnButton = tk.Button(self, text = "RETURN", height = 3 , width = 50, command=lambda: controller.show_frame(Student_Hub))
        ReturnButton.grid(row = 8, column = 1, pady = 50) # takes the user back to the Student Hub
        tk.Button(self, text = "EXIT", height = 3 , width = 50, command= self.quit).grid(row = 8, column = 2, pady = 50)# quits the game

        Logo = tk.PhotoImage(file=r"JustTheLogo.gif") # Logo's are shown
        LogoLabel1 = tk.Label(self, image=Logo, background= ColourChosen)
        LogoLabel1.image = Logo
        LogoLabel1.grid(row=0, column=0)
        LogoLabel2 = tk.Label(self, image=Logo, background= ColourChosen)
        LogoLabel2.image = Logo
        LogoLabel2.grid(row=0, column=3)

class Appearance(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self,parent)

        TitleImage = tk.PhotoImage(file=r"The Learning CubeTitle.gif")
        TitleImageLabel = tk.Label(self, image=TitleImage)
        TitleImageLabel.image = TitleImage
        TitleImageLabel.grid(pady=10, padx=10, column=1, columnspan=5)

        self.var = tk.StringVar() # the variable is set, self.var is the variable that will change the colour, tk.StringVar is which button will be pressed.
        DefaultColour = tk.Label(self, bg="#a1dbcd", height=5, width=10)
        DefaultColour.grid(row=1, column=1)
        DefaultColourChoice = tk.Radiobutton(self, text="Default", variable=self.var, value="#a1dbcd",
                                             command=self.samplecolour)# if pressed, then the backgroun colour will instantly change to that colour
        DefaultColourChoice.grid(row=2, column=1)

        Black = tk.Label(self, bg="black", height=5, width=10)
        Black.grid(row=1, column=2)
        BlackChoice = tk.Radiobutton(self, text="Black", variable=self.var, value="Black", command=self.samplecolour)
        BlackChoice.grid(row=2, column=2)

        Red = tk.Label(self, bg="Red", height=5, width=10)
        Red.grid(row=1, column=3)
        RedChoice = tk.Radiobutton(self, text="Red", variable=self.var, value="Red", command=self.samplecolour)
        RedChoice.grid(row=2, column=3)

        Orange = tk.Label(self, bg="Orange", height=5, width=10)
        Orange.grid(row=1, column=4)
        OrangeChoice = tk.Radiobutton(self, text="Orange", variable=self.var, value="Orange", command=self.samplecolour)
        OrangeChoice.grid(row=2, column=4)

        Purple = tk.Label(self, bg="Purple", height=5, width=10)
        Purple.grid(row=1, column=5)
        PurpleChoice = tk.Radiobutton(self, text="Purple", variable=self.var, value="Purple", command=self.samplecolour)
        PurpleChoice.grid(row=2, column=5)

        Blue = tk.Label(self, bg="Blue", height=5, width=10)
        Blue.grid(row=3, column=1)
        BlueChoice = tk.Radiobutton(self, text="Blue", variable=self.var, value="Blue", command=self.samplecolour)
        BlueChoice.grid(row=4, column=1)

        Yellow = tk.Label(self, bg="Yellow", height=5, width=10)
        Yellow.grid(row=3, column=2)
        YellowChoice = tk.Radiobutton(self, text="Yellow", variable=self.var, value="Yellow", command=self.samplecolour)
        YellowChoice.grid(row=4, column=2)

        Pink = tk.Label(self, bg="Pink", height=5, width=10)
        Pink.grid(row=3, column=3)
        PinkChoice = tk.Radiobutton(self, text="Pink", variable=self.var, value="Pink", command=self.samplecolour)
        PinkChoice.grid(row=4, column=3)

        Green = tk.Label(self, bg="Green", height=5, width=10)
        Green.grid(row=3, column=4)
        GreenChoice = tk.Radiobutton(self, text="Green", variable=self.var, value="Green", command=self.samplecolour)
        GreenChoice.grid(row=4, column=4)

        White = tk.Label(self, bg="White", height=5, width=10)
        White.grid(row=3, column=5)
        WhiteChoice = tk.Radiobutton(self, text="White", variable=self.var, value="White", command=self.samplecolour)
        WhiteChoice.grid(row=4, column=5)

        Change = tk.Button(self, text="CHANGE", fg="orange", height=3, width=50, command=self.changecolour) # when button pressed that method will change the database
        Change.grid(row=5, column=1, columnspan=5)

        tk.Button(self, text = "RETURN", height = 3 , width = 50, command=lambda: controller.show_frame(CustomisationChoice)).grid(row = 8, column = 1, columnspan = 2) # RETURNS to Choice Option
        tk.Button(self, text = "EXIT", height = 3 , width = 50, command= self.quit).grid(row = 8, column = 4, columnspan = 2) # QUITS

        Logo = tk.PhotoImage(file=r"JustTheLogo.gif") # Logos Shown
        LogoLabel1 = tk.Label(self, image=Logo)
        LogoLabel1.image = Logo
        LogoLabel1.grid(row=0, column=0)
        LogoLabel2 = tk.Label(self, image=Logo)
        LogoLabel2.image = Logo
        LogoLabel2.grid(row=0, column=6)

    def samplecolour(self):
        self.ColourChosen = self.var.get() # the variable that was set earlier to the result of the radiobutton now
        self.configure(background=self.ColourChosen) # equals Colour Chosen which will be the background until the next colour is pressed on.


    def changecolour(self):
        c.execute("UPDATE User_Information SET Colour_Chosen = (?) WHERE Username = (?)", (self.ColourChosen, Username)) # Changes it in the databasr, no validation is needed here, as the program is oing all of the inputs as supposed to giving the user control of what colour to type
        conn.commit()

    def GetUserColour(self): # THIS IS USED FOR OTHER CLASSES. Other classes call this method in order to get the
        c.execute('SELECT Colour_Chosen FROM User_Information WHERE Username = ?', (Username,))#background colour of the
        ColourChosen = c.fetchone()# User.
        conn.commit()
        return ColourChosen # returns the variable to wherever it was called from.

class MyAccountChoice(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ColourChosen = Appearance.GetUserColour(Appearance) # Calls the GetUserColour method to get the User colour
        self.configure(background= ColourChosen) # changes the colour

        TitleImage = tk.PhotoImage(file=r"The Learning CubeTitle.gif") # Inserts the pictures
        TitleImageLabel = tk.Label(self, image=TitleImage, bg = ColourChosen)
        TitleImageLabel.image = TitleImage
        TitleImageLabel.grid(pady=10, padx=10, column=1, columnspan=5)

        ViewScores = tk.Button(self, text="VIEW SCORES", fg="orange", height=3, width=50,
                               command=lambda: controller.show_frame(ShowScores)) # Takes the user to the Show Score page
        ViewScores.grid(row=1, column=1, padx = 10, columnspan = 2)

        ViewUserDetails = tk.Button(self, text="CHANGE USER DETAILS", fg="orange", height=3, width=50,
                                    command=lambda: controller.show_frame(ShowUserDetails)) # Takes the user to the View User Details Page
        ViewUserDetails.grid(row=2, column=1, padx = 10, columnspan = 2)


        tk.Button(self, text = "RETURN", height = 3 , width = 50, command=lambda: controller.show_frame(Student_Hub)).grid(row = 8, column = 1, pady = 50)# Returns to the Student_Hub
        tk.Button(self, text = "EXIT", height = 3 , width = 50, command= self.quit).grid(row = 8, column = 2, pady = 50) # Exits

        Logo = tk.PhotoImage(file=r"JustTheLogo.gif") # The Logos
        LogoLabel1 = tk.Label(self, image=Logo, background=ColourChosen)
        LogoLabel1.image = Logo
        LogoLabel1.grid(row=0, column=0)
        LogoLabel2 = tk.Label(self, image=Logo, background=ColourChosen)
        LogoLabel2.image = Logo
        LogoLabel2.grid(row=0, column=6)

class ShowScores(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ColourChosen = Appearance.GetUserColour(Appearance)
        self.configure(background= ColourChosen)
        self.Photo = tk.PhotoImage(file="JustTheLogo.gif")
        photo = tk.PhotoImage(file=r"The Learning CubeTitle.gif")
        Title = tk.Label(self, image=photo, background=ColourChosen)
        Title.image = photo
        Title.grid(row=0, column=1, columnspan=2)
        c.execute("SELECT MAX(Lv1Score) FROM Level1Score WHERE Username = (?)", (Username,))
        HighestLevel1Result = c.fetchone() # Aggregate SQL Query, quicker for the program than the original merge sort,
        c.execute("SELECT MAX(Lv2Score) FROM Level2Score WHERE Username = (?)", (Username,)) # merge sort is still needed
        HighestLevel2Result = c.fetchone() # later on. Here, I select the highest score from each table where the
        c.execute("SELECT MAX(Lv3Score) FROM Level3Score WHERE Username = (?)", (Username,)) # username is the same one
        HighestLevel3Result = c.fetchone() # that is logged in.
        c.execute("SELECT MAX(Lv4Score) FROM Level4Score WHERE Username = (?)", (Username,))
        HighestLevel4Result = c.fetchone()
        Logo = tk.PhotoImage(file = r"JustTheLogo.gif")
        LogoLabel1 = tk.Label(self, image = Logo, background = ColourChosen)
        LogoLabel1.image = Logo
        LogoLabel1.grid(row = 0, column = 0)
        LogoLabel2 = tk.Label(self, image = Logo, background = ColourChosen)
        LogoLabel2.image = Logo
        LogoLabel2.grid(row = 0, column = 5)
        tk.Label(self, text = "LEADERBOARD", font=Title_Font, bg=ColourChosen, fg = "white").grid(row = 2, column = 1, columnspan =2)
        tk.Label(self, text = "HIGHEST LEVEL ONE RESULT", font=BIG_FONT, bg=ColourChosen, fg = "white").grid(row = 3, column = 1, padx = 50) # padx means leavae a distance of 50 vertically between that and whatever is on its sides.
        tk.Label(self, text = HighestLevel1Result, font=BIG_FONT, bg=ColourChosen, fg = "white").grid(row = 3, column = 2, padx = 50) # Could have it all on one line but that would ruin the view of the message as it would be in {brackets}
        tk.Label(self, text = "HIGHEST LEVEL TWO RESULT", font=BIG_FONT, bg=ColourChosen, fg = "white").grid(row = 4, column = 1, padx = 50)
        tk.Label(self, text = HighestLevel2Result, font=BIG_FONT, bg=ColourChosen, fg = "white").grid(row = 4, column = 2, padx = 50)
        tk.Label(self, text = "HIGHEST LEVEL THREE RESULT", font=BIG_FONT, bg=ColourChosen, fg = "white").grid(row = 5, column = 1, padx = 50)
        tk.Label(self, text = HighestLevel3Result, font=BIG_FONT, bg=ColourChosen, fg = "white").grid(row = 5, column = 2, padx = 50)
        tk.Label(self, text = "HIGHEST LEVEL FOUR RESULT", font=BIG_FONT, bg=ColourChosen, fg = "white").grid(row = 6, column = 1, padx = 50)
        tk.Label(self, text = HighestLevel4Result, font=BIG_FONT, bg=ColourChosen, fg = "white").grid(row = 6, column = 2, padx = 50)

        tk.Button(self, text = "RETURN", height = 3 , width = 50, command=lambda: controller.show_frame(MyAccountChoice)).grid(row = 8, column = 1, pady = 50) # RETUNS
        tk.Button(self, text = "EXIT", height = 3 , width = 50, command= self.quit).grid(row = 8, column = 2, pady = 50) # EXITS

class ShowUserDetails(tk.Frame): # This is to give the student the opporunity to change their own password
    def __init__(self, parent, controller,):
        tk.Frame.__init__(self, parent)
        ColourChosen = Appearance.GetUserColour(Appearance)
        self.configure(background= ColourChosen)
        TitleImage = tk.PhotoImage(file=r"The Learning CubeTitle.gif")
        TitleImageLabel = tk.Label(self, image=TitleImage, bg=ColourChosen)
        TitleImageLabel.image = TitleImage
        TitleImageLabel.grid(pady=10, padx=10, column=1, columnspan = 3)

        tk.Label(self, text=("CHANGE PASSWORD"), font=REALLY_LARGE_FONT, bg= ColourChosen).grid(row=2, column = 1 , columnspan = 3)
        tk.Label(self, text=("Password is case sensitive"), font=REALLY_LARGE_FONT, bg= ColourChosen).grid(row=3, column = 1 , columnspan = 3)
        tk.Label(self, text="Password must be more than 6 letters", font=LARGE_FONT).grid(row=4, column=1, columnspan=3)
        tk.Label(self, text="Old Password", font=LARGE_FONT, bg=ColourChosen).grid(row=5, column=1)
        self.OldPasswordEntry = tk.Entry(self, show = "*",) # Getting information about the old password
        self.OldPasswordEntry.grid(row=6, column=1)
        tk.Label(self, text="New Password", font=LARGE_FONT, bg=ColourChosen).grid(row=5, column=2)
        self.PasswordEntry = tk.Entry(self, show = "*",) # Getting information about the new password
        self.PasswordEntry.grid(row=6, column=2)
        tk.Label(self, text="Confirm New Password", font=LARGE_FONT, bg=ColourChosen).grid(row=5, column=3)
        self.ConfirmPasswordEntry = tk.Entry(self, show="*") # Asking to confirm the message
        self.ConfirmPasswordEntry.grid(row=6, column=3)
        tk.Button(self, text="CHANGE", fg="orange", height=3, width=57, command=self.EnsuringInputsAreValid).grid(row = 7, column=  1, columnspan = 3) # When the Button is pressed, Validation begins
        tk.Button(self, text = "RETURN", height = 3 , width = 50, command=lambda: controller.show_frame(MyAccountChoice)).grid(row = 10, column = 1, columnspan = 3)# RETURNS USER
        tk.Button(self, text = "EXIT", height = 3 , width = 50, command= self.quit).grid(row = 11, column = 1, columnspan = 3) # USER QUITS

        Logo = tk.PhotoImage(file=r"JustTheLogo.gif") # Logos
        LogoLabel1 = tk.Label(self, image=Logo, background= ColourChosen)
        LogoLabel1.image = Logo
        LogoLabel1.grid(row=0, column=0)
        LogoLabel2 = tk.Label(self, image=Logo, background=ColourChosen)
        LogoLabel2.image = Logo
        LogoLabel2.grid(row=0, column=4)

    def EnsuringInputsAreValid(self): # Validation is here
        c.execute("SELECT Password FROM Users WHERE username = ? and password = ?", (Username, self.OldPasswordEntry.get())) # Firs off, ensuring the user exits
        conn.commit()
        CorrectUser = c.fetchone() # This means that if the user exists they equal the row in the table
        if CorrectUser: # User does exist
            if len(self.PasswordEntry.get()) <= 5: # If user is less tha or equal to 5
                tk.Label(self, text="Password must be more than 6 letters", font=LARGE_FONT).grid(row=8, column=1, columnspan=3) # Error, must be more than 6 letter long
                return
            else:
                if self.PasswordEntry.get() == self.ConfirmPasswordEntry.get(): # Ensuring the confirm new password and
                    c.execute("SELECT * FROM Users WHERE username = ? and password = ?", (Username, self.OldPasswordEntry.get())) # new password match, an then check database to see if user's username and password exist
                    CorrectPassword = c.fetchone()
                    if not CorrectPassword: # If they don't
                        return
                    else: # If they do
                        if askokcancel("Are You Sure?", ("Are you sure?")): # MessageBox to enure password wants to be changed
                            c.execute("UPDATE Users SET Password = ? WHERE Username = ?", (self.PasswordEntry.get(), Username)) # Password is change
                            conn.commit()
                        else:
                            return
                        tk.Label(self, text="You Have A New Password", font=LARGE_FONT).grid(row=9 , column = 1 , columnspan = 3) # message is shown to the user letting them know
                else:
                    tk.Label(self, text="Passwords do not match", font=LARGE_FONT).grid(row=9, column=1, columnspan=3)
                    return
                conn.commit()
        else:
            tk.Label(self, text="Old Password Is Not Valid", font=LARGE_FONT).grid(row=9, column=1, columnspan=3)

class ProfilePicture(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ColourChosen = Appearance.GetUserColour(Appearance) # Background Colour
        self.configure(background= ColourChosen)

        TitleImage = tk.PhotoImage(file=r"The Learning CubeTitle.gif") # Photos
        TitleImageLabel = tk.Label(self, image=TitleImage, bg=ColourChosen)
        TitleImageLabel.image = TitleImage
        TitleImageLabel.grid(row = 0, column = 1,columnspan = 3)

        tk.Label(self, text="PROFILE PICTURE",font=LARGE_FONT, bg = ColourChosen).grid(pady = 10, padx = 10, row = 1, column = 1, columnspan = 3)
        tk.Button(self, text="UPLOAD IMAGE", fg="orange", height=3, width=50, command=lambda: self.GetPicture(ProposedPicture)).grid(row = 2, column = 3) # when pressed the function is called with the Proposed Picture label, to over load it with the picture that will be uploaded by the user

        ProposedPicture = tk.Label(self, text = "Please Upload A Picture", height = 10, width = 25)
        ProposedPicture.grid(column=3, row=3) # This orignally will be just text, but as the user uploas a picture, the text will not be able to be seen

        c.execute('SELECT Profile_Pic FROM User_Information WHERE Username = ?',(Username,)) # Reading the database for the Profile Picture file
        conn.commit()
        global CP #Has to be here, as we do not want to be defing global varibale later on
        CPPicture = (c.fetchone()[0]) # the [0] is there to remove the brackets and just have the filepath
        CurrentProfilePicture = tk.PhotoImage(file=CPPicture) # Referneced It
        CurrentProfilePictureLabel = tk.Label(self,image = CurrentProfilePicture)
        CurrentProfilePictureLabel.image = CurrentProfilePicture
        CurrentProfilePictureLabel.grid(column = 1, row = 2, rowspan = 3)

        ConfirmImage = tk.Button(self, text="CONFIRM IMAGE", fg="orange", height=3, width=50, command=lambda: self.AddPictureToDatabase(CurrentProfilePictureLabel)) # When Pressed, add new picture to database
        ConfirmImage.grid(row = 4, column = 3)

        tk.Button(self,text = "RETURN", fg = "orange", height = 3 , width = 57, command=lambda: controller.show_frame
        (CustomisationChoice)).grid(row = 6, column = 1, pady = 10) # Return to previous page
        tk.Button(self,text = "EXIT", fg = "orange", height = 3 , width = 57,command = self.quit).grid(row = 6, column = 3, pady = 10) # Exit the system

        Logo = tk.PhotoImage(file=r"JustTheLogo.gif") # Logos
        LogoLabel1 = tk.Label(self, image=Logo, background= ColourChosen)
        LogoLabel1.image = Logo
        LogoLabel1.grid(row=0, column=0)
        LogoLabel2 = tk.Label(self, image=Logo, background= ColourChosen)
        LogoLabel2.image = Logo
        LogoLabel2.grid(row=0, column=4)


    def AddPictureToDatabase(self,LabelToBeCleared):
        c.execute("UPDATE User_Information SET Profile_Pic = ? WHERE Username = ?", (self.filename, Username,))
        conn.commit() # Add New Picture file path to the database
        self.ClearLabel(LabelToBeCleared) # Clear The Label
        self.UpdatePictureShown()


    def GetPicture(self,LabelToBeCleared):
        self.filename = filedialog.askopenfilename(filetypes=(("GIF files", "*.gif"),)) # Window pop up allows uers to pick the file of their choice
        self.filename = str(self.filename) # converts the file name to be a string
        self.ClearLabel(LabelToBeCleared) # Ensures the Label is cleared
        self.ChosenPicture = tk.PhotoImage(file=str(self.filename)) # Updates the picture shown
        ProposedPicture = tk.Label(self, image = self.ChosenPicture, background = "#a1dbcd")
        ProposedPicture.grid(column=3, row=3)
        return self.filename # returns the file path

    def ClearLabel(self,LabelToBeCleared):
        LabelToBeCleared.configure(image = "") # Clears the label
        return

    def UpdatePictureShown(self):
        c.execute('SELECT Profile_Pic FROM User_Information WHERE Username = ?', ([Username])) # Fund User
        conn.commit()
        self.ProfilePicture = tk.PhotoImage(file= c.fetchone()[0]) #
        CurrentProfilePicture = tk.Label(self, text = "Current Picture", image = self.ProfilePicture) # Show the current picture.
        CurrentProfilePicture.grid(column = 1, row = 2, rowspan = 3)
        return

class UserManagement(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self, parent)
        ColourChosen = Appearance.GetUserColour(Appearance) # Colour is set
        self.configure(background= ColourChosen)

        TitleImage = tk.PhotoImage(file=r"The Learning CubeTitle.gif") # Titles are made
        TitleImageLabel = tk.Label(self, image=TitleImage, bg=ColourChosen)
        TitleImageLabel.image = TitleImage
        TitleImageLabel.grid(pady=10, padx=10, column=2)

        UserManagementLabel = tk.Label(self, text=("USER MANAGEMENT")
                                       , font=REALLY_LARGE_FONT, bg= ColourChosen)
        UserManagementLabel.grid(pady=10, padx=10, row=2, column=2)

        NoteBook = ttk.Notebook(self) # The nootebook is defined, this is where the User Management will take place so instead of having different pages, this will be different tabs
        self.Frames(NoteBook) # Assiging the notebook to the frame
        NoteBook.grid(row=3, column=2) # And where to put it

        Exit = tk.Button(self, text="EXIT", fg="orange", height=3, width=57, command=self.quit)
        Exit.grid(row=5, column=2, pady=10)  # Exits , no return because the Admin has no where else to go.

        Logo = tk.PhotoImage(file=r"JustTheLogo.gif") # Logos
        LogoLabel1 = tk.Label(self, image=Logo, background= ColourChosen)
        LogoLabel1.image = Logo
        LogoLabel1.grid(row=0, column=0)
        LogoLabel2 = tk.Label(self, image=Logo, background=ColourChosen)
        LogoLabel2.image = Logo
        LogoLabel2.grid(row=0, column=3)

    def Frames(self, notebook):
        AddAUserFrame = ttk.Frame(notebook) # Adds a Tab called Add A User
        notebook.add(AddAUserFrame, text='Add A User')
        self.AddANewUserLabel = tk.Label(AddAUserFrame, text=("ADD A NEW USER")
                                         , font=BIG_FONT)
        self.AddANewUserLabel.grid(pady=10, padx=45, row=0, column=0, columnspan=3)  # pady is horiztonal. padx is vertical

        self.AAUFirstNameLabel = tk.Label(AddAUserFrame, text="FIRST NAME")
        self.AAUFirstNameLabel.grid(row=1, column=0)
        self.AAUFirstNameEntry = tk.Entry(AddAUserFrame)
        self.AAUFirstNameEntry.grid(row=2, column=0)

        self.AAULastNameLabel = tk.Label(AddAUserFrame, text="LAST NAME")
        self.AAULastNameLabel.grid(row=1, column=1)
        self.AAULastNameEntry = tk.Entry(AddAUserFrame)
        self.AAULastNameEntry.grid(row=2, column=1)

        self.AAUUsernameLabel = tk.Label(AddAUserFrame, text="USERNAME")
        self.AAUUsernameLabel.grid(row=3, pady=10)
        self.AAUUsernameEntry = tk.Entry(AddAUserFrame)
        self.AAUUsernameEntry.grid(row=3, column=1)

        self.AAURestrictionLabels = tk.Label(AddAUserFrame, text="(more than 8 characters)")
        self.AAURestrictionLabels.grid(row=4, column=1)

        self.AAUPasswordLabel = tk.Label(AddAUserFrame, text="PASSWORD")
        self.AAUPasswordLabel.grid(row=5)
        self.AAUPasswordEntry = tk.Entry(AddAUserFrame)  # GAINING THE INFORMATION.
        self.AAUPasswordEntry.grid(row=5, column=1)

        self.AAURestrictionLabels1 = tk.Label(AddAUserFrame, text="(more than 8 characters)")
        self.AAURestrictionLabels1.grid(row=6, column=1)
        self.choice = tk.IntVar()
        self.AAUCheckIsAnAdmin = ttk.Checkbutton(AddAUserFrame, variable=self.choice)
        self.AAUCheckIsAnAdmin.grid(row=7, column=0)
        self.AAUCIALabel = tk.Label(AddAUserFrame, text="Is An Admin?")
        self.AAUCIALabel.grid(row=7, column=1)

        self.AAUSumbit = tk.Button(AddAUserFrame, text="CREATE", fg="orange", height=3, width=57,
                                   command=self.addUsertoDatabase) # Takes to addUsertoDatabase
        self.AAUSumbit.grid(row=9, column=0, columnspan=3)


        DeleteUser = ttk.Frame(notebook)
        notebook.add(DeleteUser, text='Delete User')
        self.DeleteUserLabel = tk.Label(DeleteUser, text=("DELETE USER")
                                        , font=BIG_FONT)
        self.DeleteUserLabel.grid(pady=10, padx=75, row=0, column=0, columnspan=2)

        self.DUFirstNameLabel = tk.Label(DeleteUser, text="FIRST NAME")
        self.DUFirstNameLabel.grid(row=3, pady=10)
        self.DUFirstNameEntry = tk.Entry(DeleteUser)# GAINING THE INFORMATION
        self.DUFirstNameEntry.grid(row=4)

        self.DULastNameLabel = tk.Label(DeleteUser, text="LAST NAME")
        self.DULastNameLabel.grid(row=3, column=1, pady=10)
        self.DULastNameEntry = tk.Entry(DeleteUser)
        self.DULastNameEntry.grid(row=4, column=1)

        self.DUDeleteUser = tk.Button(DeleteUser, text="DELETE USER", fg="orange", height=3, width=57,
                                      command=self.deleteuser)
        self.DUDeleteUser.grid(row=5, column=0, columnspan=2)



        ViewUserDetails = ttk.Frame(notebook)
        notebook.add(ViewUserDetails, text='View User Details')
        self.ViewUserDetails = tk.Label(ViewUserDetails, text=("VIEW USER DETAILS")
                                        , font=LARGE_FONT)
        self.ViewUserDetails.grid(pady=10, row=0, column=0, columnspan=4)
        ListOfData = []
        c.execute('SELECT * FROM Users') # Gaining all the information from the Table
        conn.commit()
        Headings = [tuple[0] for tuple in c.description] # Gaining the heading of each coloumn from a dictonary
        for row in c.fetchall():
            ListOfData.append(row)
        self.VUDFirstNameLabel = tk.Label(ViewUserDetails, text=("First Name"))
        self.VUDFirstNameLabel.grid(row=1, column=1)
        self.VUDLastNameLabel = tk.Label(ViewUserDetails, text=("Last Name"))
        self.VUDLastNameLabel.grid(row=1, column=2)
        self.Search = tk.Label(ViewUserDetails, text=("Search for User"))
        self.Search.grid(row=2, column=0)
        self.SearchFNEntry = tk.Entry(ViewUserDetails)
        self.SearchFNEntry.grid(row=2, column=1)
        self.SearchLNEntry = tk.Entry(ViewUserDetails)
        self.SearchLNEntry.grid(row=2, column=2)
        self.SearchButton = tk.Button(ViewUserDetails, text="SEARCH", bg="orange", height=2, width=5,
                                      command=lambda: self.SearchUser(ViewUserDetails))  # lambda is used as it is a throwaway function. So that it only runs when pressed and rit uns everytime it is called.
        self.SearchButton.grid(row=2, column=3)
        self.IntroductionLabel = ttk.Label(ViewUserDetails, text="Here is the information", font=Med_Font)
        self.IntroductionLabel.grid(row=3, column=0, columnspan=4)
        self.tabs = ttk.Treeview(columns=Headings, show="headings") # self.tabs is created with the heading of the sqlite statement
        self.ScrollBar = ttk.Scrollbar(orient="vertical", command=self.tabs.yview) # A scrollbar is made to scroll up and down
        self.tabs.configure(yscrollcommand = self.ScrollBar.set) # Getting the tree to move with the bar
        self.tabs.grid(column=0, row=4, sticky='nsew', in_= ViewUserDetails, columnspan=4) # Here I set the tree in the middle of the frame, to expand north,south,east and west.
        self.ScrollBar.grid(column=4, row=4, sticky='ns', in_=ViewUserDetails)# Here I keep the scrollbar to the right side.
        for column in Headings:
            self.tabs.heading(column, text=column.title()) # Get the title
            self.tabs.column(column, width=tkFont.Font().measure(column.title())) # and how long it is, this is to know how long each column has to be
        for item in ListOfData:
            self.tabs.insert('', 'end', values=item)


        ChangeUserDetails = ttk.Frame(notebook)
        notebook.add(ChangeUserDetails, text='Change User Details')
        tk.Label(ChangeUserDetails, text=("CHANGE USER DETAILS"), font=BIG_FONT).grid(pady=10, row=0, column=0, columnspan=2)

        tk.Label(ChangeUserDetails, text="Username").grid(row=1, column=0)
        self.CUDUsernameEntry = tk.Entry(ChangeUserDetails)
        self.CUDUsernameEntry.grid(row=2, column=0)

        tk.Label(ChangeUserDetails, text= "Old Password").grid(row=1, column=1)
        self.CUDOldPasswordEntry = tk.Entry(ChangeUserDetails)
        self.CUDOldPasswordEntry.grid(row=2, column=1)

        tk.Label(ChangeUserDetails, text="New Password").grid(row=3, pady=10)
        self.CUDNewPasswordEntry = tk.Entry(ChangeUserDetails)
        self.CUDNewPasswordEntry.grid(row=3, column=1)

        tk.Label(ChangeUserDetails, text="Confirm New Password").grid(row=5, pady=10)
        self.CUDConfirmNewPasswordEntry = tk.Entry(ChangeUserDetails)
        self.CUDConfirmNewPasswordEntry.grid(row=5, column=1)

        tk.Button(ChangeUserDetails, text="CHANGE", fg="orange", height=3, width=57,
                                   command=self.UpdateUser).grid(row=9, column=0, columnspan=3) # when presse, call UpdateUser


        ViewUserScores = ttk.Frame(notebook)
        notebook.add(ViewUserScores, text='View Scores')
        notebook = ttk.Notebook(ViewUserScores)
        self.ViewScores(notebook) # calls a new function that will contain another notenook
        notebook.grid(row = 3, column = 5)

    def UpdateUser(self):
        ChosenUsername = self.CUDUsernameEntry.get()
        NewPassword = self.CUDNewPasswordEntry.get()
        OldPassword = self.CUDOldPasswordEntry.get()
        c.execute("SELECT * FROM Users WHERE username = ? and password = ?", (ChosenUsername, OldPassword))
        conn.commit()
        CorrectUser = c.fetchone() # If the sqlite query is true, then this will contain the user
        if CorrectUser: # If user exists
            if not self.CUDNewPasswordEntry.get() == self.CUDConfirmNewPasswordEntry.get(): # if the passwords do not match
                tk.Label(self, text="Passwords do not match", font=LARGE_FONT).grid(row=7, column = 1 , columnspan = 3)
                return
            else:
                if len(self.CUDNewPasswordEntry.get()) <= 5: # if password is less than 6 lettters
                    tk.Label(self, text="Password must be more than 6 letters", font=LARGE_FONT).grid(row=8, column=1, columnspan=3)
                    return
                else:
                    if askokcancel("Are You Sure?", ("Are you sure?")): # Confirmation the admin wants to update detials
                        c.execute("UPDATE Users SET Password = ? WHERE Username = ?", (NewPassword, ChosenUsername))
                        conn.commit() # Update User
                        tk.Label(self, text="Password Changed", font=LARGE_FONT).grid(row=7, column = 1 , columnspan = 3)
                conn.commit()
            return
        else:  # User does not exist
            tk.Label(self, text="User does not exist", font=LARGE_FONT).grid(row=7, column=1, columnspan=3)
            return

    def addUsertoDatabase(self):
        c.execute(
            'CREATE TABLE IF NOT EXISTS Users(FirstName TEXT, LastName TEXT, Username TEXT, Password TEXT, Admin TEXT)')
        FirstName = self.AAUFirstNameEntry.get()
        self.AAUFirstNameEntry.delete('0', END)
        LastName = self.AAULastNameEntry.get()
        self.AAULastNameEntry.delete('0', END)
        AAUUsername = self.AAUUsernameEntry.get()
        self.AAUUsernameEntry.delete('0', END)
        c.execute('SELECT Username FROM Users WHERE Username = (?)', (AAUUsername,))
        UniqueUsername = c.fetchone() # THIS IS EXTREMELY IMPORTNAT. It ensure, the user does not have an idnetical username to someone else
        Password = self.AAUPasswordEntry.get()
        self.AAUPasswordEntry.delete('0', END)
        self.IsAdmin = self.choice.get()
        if self.IsAdmin == 1:
            Admin = 'TRUE'
        else:
            Admin = 'FALSE'
        if not UniqueUsername: # If user does not already share a username
            if not FirstName or not LastName or not AAUUsername or not Password:  # If either slate is blank
                showerror("Error!", "User Creditenals are not valid")
            elif len(self.AAUPasswordEntry.get()) >= 5: # Less than 6 characters
                showerror("Error!", "Password must be more than 6 characters")
            else:
                if askokcancel("Are You Sure?", ("Are the user Creditenals correct")): # Confirmation
                    c.execute("INSERT INTO Users(FirstName, LastName, Username, Password, Admin) VALUES (?, ?, ?, ?, ?)",
                              (FirstName, LastName, AAUUsername, Password, Admin)) # Add User
                    c.execute("CREATE TABLE IF NOT EXISTS User_Information(ID INTEGER PRIMARY KEY, Username TEXT, Profile_Pic BLOB DEFAULT 'Profile Picture.gif')") # Instnatly create User Informatoin
                    c.execute("INSERT INTO User_Information(Username) VALUES (?)", (AAUUsername,)) # and insert into it the username that links the tables together
                    tk.Label(self, text="User Added", font=LARGE_FONT).grid(row=3, column=3)
                    conn.commit()
                else:
                    return
        else:
            tk.Label(self, text="Username is invalid", font=LARGE_FONT).grid(row=3, column=3)

    def SearchUser(self, ViewUserDetails):
        FirstName = self.SearchFNEntry.get()
        LastName = self.SearchLNEntry.get()  # If Can use dropdown LIST
        c.execute("SELECT * FROM Users WHERE firstname = ? and lastname = ?", (FirstName, LastName))
        User = c.fetchone()
        conn.commit()
        if User: #If user exists
            ListForData = [c.fetchone()]
            Headings = [tuple[0] for tuple in c.description]  # this is a dictonary
            conn.commit()
            self.tabs = ttk.Treeview(columns=Headings, show="headings")
            self.tabs.grid(column=0, row=4, sticky='nsew', in_=ViewUserDetails, columnspan=4)
            for column in Headings:
                self.tabs.heading(column, text=column.title())
                self.tabs.column(column, width=tkFont.Font().measure(column.title()))
            for item in ListForData:
                self.tabs.insert('', 'end', values=item)
            # REPLACES THE ALREADY CREATED TREE OF ALL THE USERS WITH A CUSTOMISED ONE TO THE USER.
        else:
            tk.Label(self, text="No User Found", font=LARGE_FONT).grid(row=3, column=3) # prints an error message
            return

    def deleteuser(self):
        FirstName = self.DUFirstNameEntry.get()
        self.DUFirstNameEntry.delete('0', END)
        LastName = self.DULastNameEntry.get()
        self.DULastNameEntry.delete('0', END)
        if not FirstName or not LastName:  # If user details are blank
            showerror("Error!", "User Creditenals are not valid") # Show Error
        else:
            if askokcancel("Are You Sure?", ("Are you sure you want to delete the user")): # Ask for confirmation
                c.execute("DELETE FROM Users WHERE FirstName = ? and LastName = ?", (FirstName,LastName))
                tk.Label(self, text="Deleted User", font=LARGE_FONT).grid(row=3, column=3)
        conn.commit()

    def ViewScores (self, notebook):
        Level1 = ttk.Frame(notebook) # THE EXACT SAME IS DONE BUT FOR THE LEVEL TABLES INSTEAD
        notebook.add(Level1, text='Level 1')
        self.AddANewUserLabel = tk.Label(Level1, text=("LEVEL 1") ,font=BIG_FONT)
        self.AddANewUserLabel.grid(pady = 10, padx = 45, row = 0, column = 0, columnspan = 3)
        ListForData = []
        c.execute('SELECT FirstName, LastName, Lv1Score FROM Users CROSS JOIN Level1Score')
        Headings = [tuple[0] for tuple in c.description]
        for row in c.fetchall():
            ListForData.append(row)
        self.IntroductionLabel = ttk.Label(Level1, text = "Here is the information", font = Med_Font).grid(row = 3 , column = 0, columnspan = 4)
        self.tabs = ttk.Treeview(columns=Headings, show="headings")
        self.ScrollBar = ttk.Scrollbar(orient="vertical", command=self.tabs.yview)
        self.tabs.configure(yscrollcommand=self.ScrollBar.set)
        self.tabs.grid(column= 0, row=4, sticky='nsew', in_= Level1, columnspan = 4)
        self.ScrollBar.grid(column=4, row=4, sticky='ns', in_=Level1)
        for column in Headings:
            self.tabs.heading(column, text=column.title())
            self.tabs.column(column, width=tkFont.Font().measure(column.title()))
        for item in ListForData:
            self.tabs.insert('', 'end', values=item)

        Level2 = ttk.Frame(notebook)
        notebook.add(Level2, text='Level 2')
        self.AddANewUserLabel = tk.Label(Level2, text=("LEVEL 2") ,font=BIG_FONT)
        self.AddANewUserLabel.grid(pady = 10, padx = 45, row = 0, column = 0, columnspan = 3)
        ListForData = []
        c.execute('SELECT FirstName, LastName, Lv2Score FROM Users CROSS JOIN Level2Score')
        Headings = [tuple[0] for tuple in c.description]
        for row in c.fetchall():
            ListForData.append(row)
        self.IntroductionLabel = ttk.Label(Level2, text = "Here is the information", font = Med_Font).grid(row = 3 , column = 0, columnspan = 4)
        self.tabs = ttk.Treeview(columns=Headings, show="headings")
        self.ScrollBar = ttk.Scrollbar(orient="vertical", command=self.tabs.yview)
        self.tabs.configure(yscrollcommand=self.ScrollBar.set)
        self.tabs.grid(column= 0, row=4, sticky='nsew', in_= Level2, columnspan = 4)   # ADD TIME TAKEN, DATE IT WAS DONE AND THE NUMBER OF ATTEMPTS INTO THE SCORE DATABASE
        self.ScrollBar.grid(column=4, row=4, sticky='ns', in_=Level2)
        for column in Headings:
            self.tabs.heading(column, text=column.title())
            self.tabs.column(column, width=tkFont.Font().measure(column.title()))
        for item in ListForData:
            self.tabs.insert('', 'end', values=item)

        Level3 = ttk.Frame(notebook)
        notebook.add(Level3, text='Level 3')
        self.AddANewUserLabel = tk.Label(Level3, text=("LEVEL 3") ,font=BIG_FONT).grid(pady = 10, padx = 45, row = 0, column = 0, columnspan = 3)
        ListForData = []
        c.execute('SELECT FirstName, LastName, Lv3Score FROM Users CROSS JOIN Level3Score')
        Headings = [tuple[0] for tuple in c.description]
        for row in c.fetchall():
            ListForData.append(row)
        self.IntroductionLabel = ttk.Label(Level3, text = "Here is the information", font = Med_Font).grid(row = 3 , column = 0, columnspan = 4)
        self.tabs = ttk.Treeview(columns=Headings, show="headings")
        self.ScrollBar = ttk.Scrollbar(orient="vertical", command=self.tabs.yview)
        self.tabs.configure(yscrollcommand=self.ScrollBar.set)
        self.tabs.grid(column= 0, row=4, sticky='nsew', in_= Level3, columnspan = 4)
        self.ScrollBar.grid(column=4, row=4, sticky='ns', in_=Level3)
        for column in Headings:
            self.tabs.heading(column, text=column.title())
            self.tabs.column(column, width=tkFont.Font().measure(column.title()))
        for item in ListForData:
            self.tabs.insert('', 'end', values=item)

        Level4 = ttk.Frame(notebook)
        notebook.add(Level4, text='Level 4')
        self.AddANewUserLabel = tk.Label(Level4, text=("LEVEL 4") ,font=BIG_FONT).grid(pady = 10, padx = 45, row = 0, column = 0, columnspan = 3)
        ListForData = []
        c.execute('SELECT FirstName, LastName, Lv4Score FROM Users CROSS JOIN Level4Score')
        Headings = [tuple[0] for tuple in c.description]
        for row in c.fetchall():
            ListForData.append(row)
        self.IntroductionLabel = ttk.Label(Level4, text = "Here is the information", font = Med_Font).grid(row = 3 , column = 0, columnspan = 4)
        self.tabs = ttk.Treeview(columns=Headings, show="headings")
        self.ScrollBar = ttk.Scrollbar(orient="vertical", command=self.tabs.yview)
        self.tabs.configure(yscrollcommand=self.ScrollBar.set)
        self.tabs.grid(column= 0, row=4, sticky='nsew', in_= Level4, columnspan = 4)
        self.ScrollBar.grid(column=4, row=4, sticky='ns', in_=Level4)
        for column in Headings:
            self.tabs.heading(column, text=column.title())
            self.tabs.column(column, width=tkFont.Font().measure(column.title()))
        for item in ListForData:
            self.tabs.insert('', 'end', values=item)

class ChoiceForGame(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self, parent)
        ColourChosen = Appearance.GetUserColour(Appearance) # Get Colour
        self.configure(background= ColourChosen) # Change Colour

        TitleImage = tk.PhotoImage(file = r"The Learning CubeTitle.gif") # Pictures
        TitleImageLabel = tk.Label(self,image = TitleImage, bg = ColourChosen)
        TitleImageLabel.image = TitleImage
        TitleImageLabel.grid(column = 1, columnspan = 4)

        WelcomeMessage = tk.Label(self, text = ("WELCOME"), fg = "orange", bg=ColourChosen, font = HUGE_FONT)
        WelcomeMessage.grid(row = 1,column = 1, columnspan = 3)

        InformativeMessage = tk.Label(self, text = ("Please chose one of the following"), bg=ColourChosen, font = BIG_FONT)
        InformativeMessage.grid(row = 2,column = 1, columnspan = 4)

        LevelOne = tk.Button(self,text = "LEVEL 1", fg = "orange",height = 10 , width = 20,
                           command=lambda: controller.show_frame(Level1))# Play Level1
        LevelOne.grid(row = 3, column = 1)
        LevelTwo = tk.Button(self,text = "LEVEL 2", fg = "orange",height = 10 , width = 20,
                                      command=lambda: controller.show_frame(Level2))# Play Level2
        LevelTwo.grid(row = 3, column = 2)
        LevelThree= tk.Button(self,text = "LEVEL 3", fg = "orange",height = 10 , width = 20,
                                      command=lambda: controller.show_frame(Level3))# Play Level3
        LevelThree.grid(row = 3, column = 3)
        LevelFour = tk.Button(self,text = "LEVEL 4", fg = "orange",height = 10 , width = 20,
                                      command=lambda: controller.show_frame(Level4))# Play Level4
        LevelFour.grid(row = 3, column = 4)
        Exit = tk.Button(self,text = "EXIT", fg = "orange", height = 3 , width = 50, command= self.quit)
        Exit.grid(row = 4, column = 1, columnspan = 4, pady = 10)

        Logo = tk.PhotoImage(file = r"JustTheLogo.gif") #Logos
        LogoLabel1 = tk.Label(self, image = Logo, background = ColourChosen)
        LogoLabel1.image = Logo
        LogoLabel1.grid(row = 0, column = 0)
        LogoLabel2 = tk.Label(self, image = Logo, background = ColourChosen)
        LogoLabel2.image = Logo
        LogoLabel2.grid(row = 0, column = 5)

class Level1(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self,parent)
        self.configure(background= "#a1dbcd")
        self.parent = parent
        self.Photo = tk.PhotoImage(file="JustTheLogo.gif")
        photo = tk.PhotoImage(file=r"The Learning CubeTitle.gif")
        Title = tk.Label(self, image=photo, background="#a1dbcd")
        Title.image = photo
        Title.grid(row=0, column=1, columnspan=4)
        Logo = tk.PhotoImage(file = r"JustTheLogo.gif")
        LogoLabel1 = tk.Label(self, image = Logo, background = "#a1dbcd")
        LogoLabel1.image = Logo
        LogoLabel1.grid(row = 0, column = 0)
        LogoLabel2 = tk.Label(self, image = Logo, background = "#a1dbcd")
        LogoLabel2.image = Logo
        LogoLabel2.grid(row = 0, column = 5)
        LevelLabel = tk.Label(self, text=("THIS IS LEVEL ONE")
                              ,font=REALLY_LARGE_FONT, bg = "#a1dbcd")
        LevelLabel.grid(pady = 10, padx = 10, row = 1, column = 1, columnspan=4)
        self.CardPlacers = [[tk.Button(self,command=lambda row=row, column=column: self.CardPicked(row, column,controller,parent),  width=14, height= 9)
                        for column in range(4)] for row in range(3)]
        for row in range(3):
            for column in range(4):
                self.CardPlacers[row][column].grid(row=row + 2, column=column + 1)
        self.tobechecked = None
        self.Attempts = 0
        self.CreateCards()

    def CreateCards(self):
        answer = []
        count = 0
        self.CreatingAnswer(answer,count)
        answer = [row for column in answer for row in column]
        shuffle(answer)
        self.AnswersBehindCard = answer[:4],answer[4:8],answer[8:12]
        for row in self.CardPlacers:
            for button in row:
                button.config(fg="#a1dbcd", bg="#a1dbcd", state=tk.NORMAL)
        self.start_time = time.time()

    def CreatingAnswer(self, answer, count):
        ListPlaceHolder = []
        if not count < 6:
            return
        else:
            number = (randint(0, 9))
            number2 = (randint(0, 9))
            answertobeaddedtolist = number + number2
            numbertoaddtolist = (number, "+" , number2)
            ListPlaceHolder.append(numbertoaddtolist)
            ListPlaceHolder.append(answertobeaddedtolist)
            self.CreatingAnswer(answer, count + 1)
        answer.append(ListPlaceHolder)
        return answer

    def CardPicked(self, row, column,controller, parent):
        self.CardPlacers[row][column].config(bg="white", text=(self.AnswersBehindCard[row][column]), font=HUGE_FONT, width=15,
                                         height=10 , state=tk.DISABLED)  # equals the answer that is there
        if not self.tobechecked:
            self.tobechecked = row, column
        else:
            self.Attempts =  self.Attempts + 1
            to, check = self.tobechecked
            if isinstance(self.AnswersBehindCard[to][check], tuple):
                FirstNumber = (self.AnswersBehindCard[to][check][0])
                LastNumber = (self.AnswersBehindCard[to][check][2]) # orginally had sum but the addition meant that it didn't work. Had to slice the tuple to get the first and last elments, i.e the numbers that are going to be used.
                AnswerToBeChecked = FirstNumber + LastNumber
                if self.AnswersBehindCard[row][column] == AnswerToBeChecked:
                    Validation = True
                else:
                    Validation = False
            elif isinstance(self.AnswersBehindCard[row][column], tuple):
                FirstNumber = (self.AnswersBehindCard[row][column][0])
                SecondNumber = (self.AnswersBehindCard[row][column][2])
                AnswerToBeChecked = FirstNumber + SecondNumber
                if self.AnswersBehindCard[to][check] == AnswerToBeChecked:
                    Validation = True
                else:
                    Validation = False
            else:
                Validation = False
            self.Attempts = self.Attempts + 1 # if two sums were chose, 8+5 and 9+6, it would come here.
            if Validation == True:
                self.AnswersBehindCard[row][column] = ''
                self.AnswersBehindCard[to][check] = '' # orignially had .pop but .pop will not work so had to replace with ""
                if self.AnswersBehindCard == (['', '', '', ''], ['', '', '', ''], ['', '', '', '']):   # NEED TO FIX THIS; USE RECURSION
                    self.stop_time = time.time()
                    self.Time = 500 - (round(self.stop_time - self.start_time ,0))
                    self.Score = round(self.Time // self.Attempts) * 8
                    self.parent.after(4000, self.AddScoreToTable(controller))
            else:
                self.parent.after(1000, self.HideCards, row, column, to, check)
            self.tobechecked = None

    def HideCards(self, row, column, to, check):
        self.CardPlacers[row][column].config(bg="#a1dbcd", state=tk.NORMAL)
        self.CardPlacers[to][check].config(bg="#a1dbcd", state=tk.NORMAL)

    def AddScoreToTable(self,controller):
        c.execute('CREATE TABLE IF NOT EXISTS Level1Score (ID INTEGER PRIMARY KEY, Username TEXT, Lv1Score INTEGER)')
        c.execute('INSERT INTO Level1Score (Username,Lv1Score) VALUES (?,?)', (Username, self.Score))
        conn.commit()
        showinfo("Score", ("Your Score Was", self.Score))
        self.parent.after(1000, controller.show_frame(showLv4LeaderBoard))

class showLv1LeaderBoard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        Colour = (random.choice(["Black", "Red", "Orange", "Green", "Pink", "Purple", "Blue"]))
        self.configure(background = Colour)
        self.Photo = tk.PhotoImage(file="JustTheLogo.gif")
        photo = tk.PhotoImage(file=r"The Learning CubeTitle.gif")
        Title = tk.Label(self, image=photo, background=Colour)
        Title.image = photo
        Title.grid(row=0, column=1, columnspan=2)
        Logo = tk.PhotoImage(file = r"JustTheLogo.gif")
        LogoLabel1 = tk.Label(self, image = Logo, background = Colour)
        LogoLabel1.image = Logo
        LogoLabel1.grid(row = 0, column = 0)
        LogoLabel2 = tk.Label(self, image = Logo, background = Colour)
        LogoLabel2.image = Logo
        LogoLabel2.grid(row = 0, column = 5)
        conn.commit()
        c.execute("SELECT Username, Lv1Score from Level1Score")
        Scores = c.fetchall()
        MergeSortingScores(Scores)
        tk.Label(self, text = "LEADERBOARD", font=Title_Font, bg=Colour, fg = "white").grid(row = 2, column = 1, columnspan = 2)
        tk.Label(self, text = "1", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 3, column = 1, padx = 50)
        tk.Label(self, text = Scores[0], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 3, column = 2, padx = 50)
        tk.Label(self, text = "2", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 4, column = 1, padx = 50)
        tk.Label(self, text = Scores[1], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 4, column = 2, padx = 50)
        tk.Label(self, text = "3", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 5, column = 1, padx = 50)
        tk.Label(self, text = Scores[2], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 5, column = 2, padx = 50)
        tk.Label(self, text = "4", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 6, column = 1, padx = 50)
        tk.Label(self, text = Scores[3], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 6, column = 2, padx = 50)
        tk.Label(self, text = "5", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 7, column = 1, padx = 50)
        tk.Label(self, text = Scores[4], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 7, column = 2, padx = 50)

        tk.Button(self, text = "CONTINUE", height = 3 , width = 50, command=lambda: controller.show_frame(Level2)).grid\
            (row = 8, column = 1, pady = 50)#AND PUT THIS AS THE ONE PLUS THE VARIABLE SO IT NOWS TO GO TO THE NXT LVL
        tk.Button(self, text = "EXIT", height = 3 , width = 50, command= self.quit).grid(row = 8, column = 2, pady = 50)

class Level2(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self,parent)
        self.configure(background= "#a1dbcd")
        self.parent = parent
        self.Photo = tk.PhotoImage(file="JustTheLogo.gif")
        photo = tk.PhotoImage(file=r"The Learning CubeTitle.gif")
        Title = tk.Label(self, image=photo, background="#a1dbcd")
        Title.image = photo
        Title.grid(row=0, column=1, columnspan=6)
        Logo = tk.PhotoImage(file = r"JustTheLogo.gif")
        LogoLabel1 = tk.Label(self, image = Logo, background = "#a1dbcd")
        LogoLabel1.image = Logo
        LogoLabel1.grid(row = 0, column = 0)
        LogoLabel2 = tk.Label(self, image = Logo, background = "#a1dbcd")
        LogoLabel2.image = Logo
        LogoLabel2.grid(row = 0, column = 7)
        LevelLabel = tk.Label(self, text=("THIS IS LEVEL TWO")
                              , font=REALLY_LARGE_FONT, bg="#a1dbcd")
        LevelLabel.grid(pady=10, padx=10, row=1, column=1, columnspan=6)
        self.buttons = [[tk.Button(self, command=lambda row=row, column=column: self.CardPicked(row, column,controller, parent),
                                   width=14, height=9)
                         for column in range(6)] for row in range(3)]
        for row in range(3):
            for column in range(6):
                self.buttons[row][column].grid(row=row + 2, column=column + 1)
        self.tobechecked = None
        self.Attempts = 0
        self.create_cards()

    def create_cards(self):
        numberlist = []
        for i in range(9):
            number = (randint(0, 9))
            number2 = (randint(0, 9))
            signs = ("+", "*")
            self.signchosen = (random.choice(signs))
            if self.signchosen == "*":
                answertobeaddedtolist = number * number2
            else:
                answertobeaddedtolist = number + number2
            numbertoaddtolist = (number, self.signchosen, number2)
            numberlist.append(numbertoaddtolist)
            numberlist.append(answertobeaddedtolist)
        shuffle(numberlist)
        self.answer = numberlist[:6], numberlist[6:12], numberlist[12:18]
        for row in self.buttons:
            for button in row:
                button.config(fg="#a1dbcd", bg="#a1dbcd", state=tk.NORMAL)
        self.start_time = time.time()

    def CardPicked(self, row, column, controller, parent):
        self.buttons[row][column].config(bg="white", text=(self.answer[row][column]), font=HUGE_FONT, width=15,
                                         height=10, state=tk.DISABLED)  # equals the answer that is there
        if not self.tobechecked:
            self.tobechecked = row, column
        else:
            to, check = self.tobechecked
            Validation = False
            if isinstance(self.answer[to][check], tuple):
                FirstNumber = (self.answer[to][check][0])
                LastNumber = (self.answer[to][check][2])  # orginally had sum but the addition meant that it didn't work. Had to slice the tuple to get the first and last elments, i.e the numbers that are going to be used.
                blahblah = FirstNumber + LastNumber
                blahblah2 = FirstNumber * LastNumber
                sign = (self.answer[to][check][1])
                if sign == "*":
                    if self.answer[row][column] == blahblah2:
                        Validation = True
                    else:
                        Validation = False
                elif sign == "+":
                    if self.answer[row][column] == blahblah:
                        Validation = True
                    else:
                        Validation = False
            elif isinstance(self.answer[row][column], tuple):
                FirstNumber = (self.answer[row][column][0])
                LastNumber = (self.answer[row][column][2])  # orginally had sum but the addition meant that it didn't work. Had to slice the tuple to get the first and last elments, i.e the numbers that are going to be used.
                blahblah = FirstNumber + LastNumber
                blahblah2 = FirstNumber * LastNumber
                sign = (self.answer[row][column][1])
                if sign == "*":
                    if self.answer[to][check] == blahblah2:
                        Validation = True
                    else:
                        Validation = False
                elif sign == "+":
                    if self.answer[to][check] == blahblah:
                        Validation = True
                    else:
                        Validation = False
                else:
                    Validation = False
                self.Attempts = self.Attempts + 1# if two sums were chose, 8+5 and 9+6, it would come here.
            if Validation == True:
                self.answer[row][column] = ''
                self.answer[to][check] = ''  # orignially had .pop but .pop will not work so had to replace with ""
                if self.answer == (
                ['', '', '', '','',''], ['', '', '', '','',''], ['', '', '', '','','']):  # NEED TO FIX THIS; USE RECURSION
                    self.stop_time = time.time()
                    self.Time = 500 - (round(self.stop_time - self.start_time ,0))
                    self.Score = round(self.Time // self.Attempts) * 8
                    self.parent.after(4000, self.AddScoreToTable(controller, parent))
            else:
                self.parent.after(1000, self.HideCards, row, column, to, check)
            self.tobechecked = None

    def HideCards(self, row, column, to, check):
        self.buttons[row][column].config(bg="#a1dbcd", state=tk.NORMAL)
        self.buttons[to][check].config(bg="#a1dbcd", state=tk.NORMAL)

    def AddScoreToTable(self,controller, parent):
        c.execute("CREATE TABLE IF NOT EXISTS Level2Score (ID INTEGER PRIMARY KEY, Username TEXT, Lv2Score INTEGER)")
        c.execute("INSERT INTO Level2Score(Username, Lv2Score) VALUES (?, ?)",(Username, self.Score))
        conn.commit()
        showinfo("Score", ("Your Score Was", self.Score))
        self.parent.after(1000, controller.show_frame(showLv2LeaderBoard))

class showLv2LeaderBoard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        Colour = (random.choice(["Black", "Red", "Orange", "Green", "Pink", "Purple", "Blue"]))
        self.configure(background = Colour)
        self.Photo = tk.PhotoImage(file="JustTheLogo.gif")
        photo = tk.PhotoImage(file=r"The Learning CubeTitle.gif")
        Title = tk.Label(self, image=photo, background=Colour)
        Title.image = photo
        Title.grid(row=0, column=1, columnspan=2)
        Logo = tk.PhotoImage(file = r"JustTheLogo.gif")
        LogoLabel1 = tk.Label(self, image = Logo, background = Colour)
        LogoLabel1.image = Logo
        LogoLabel1.grid(row = 0, column = 0)
        LogoLabel2 = tk.Label(self, image = Logo, background = Colour)
        LogoLabel2.image = Logo
        LogoLabel2.grid(row = 0, column = 5)
        conn.commit()
        c.execute("SELECT Username, Lv2Score from Level2Score")
        Scores = c.fetchall()
        MergeSortingScores(Scores)
        tk.Label(self, text = "LEADERBOARD", font=Title_Font, bg=Colour, fg = "white").grid(row = 2, column = 1, columnspan = 2)
        tk.Label(self, text = "1", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 3, column = 1, padx = 50)
        tk.Label(self, text = Scores[0], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 3, column = 2, padx = 50)
        tk.Label(self, text = "2", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 4, column = 1, padx = 50)
        tk.Label(self, text = Scores[1], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 4, column = 2, padx = 50)
        tk.Label(self, text = "3", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 5, column = 1, padx = 50)
        tk.Label(self, text = Scores[2], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 5, column = 2, padx = 50)
        tk.Label(self, text = "4", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 6, column = 1, padx = 50)
        tk.Label(self, text = Scores[3], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 6, column = 2, padx = 50)
        tk.Label(self, text = "5", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 7, column = 1, padx = 50)
        tk.Label(self, text = Scores[4], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 7, column = 2, padx = 50)

        tk.Button(self, text = "CONTINUE", height = 3 , width = 50, command=lambda: controller.show_frame(Level3)).grid\
            (row = 8, column = 1, pady = 50)#AND PUT THIS AS THE ONE PLUS THE VARIABLE SO IT NOWS TO GO TO THE NXT LVL
        tk.Button(self, text = "EXIT", height = 3 , width = 50, command= self.quit).grid(row = 8, column = 2, pady = 50)

class Level3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background= "#a1dbcd")
        self.parent = parent
        self.Photo = tk.PhotoImage(file="JustTheLogo.gif")
        photo = tk.PhotoImage(file=r"The Learning CubeTitle.gif")
        Title = tk.Label(self, image=photo, background="#a1dbcd")
        Title.image = photo
        Title.grid(row=0, column=1, columnspan=6)
        Logo = tk.PhotoImage(file = r"JustTheLogo.gif")
        LogoLabel1 = tk.Label(self, image = Logo, background = "#a1dbcd")
        LogoLabel1.image = Logo
        LogoLabel1.grid(row = 0, column = 0)
        LogoLabel2 = tk.Label(self, image = Logo, background = "#a1dbcd")
        LogoLabel2.image = Logo
        LogoLabel2.grid(row = 0, column = 7)
        LevelLabel = tk.Label(self, text=("THIS IS LEVEL THREE")
                              ,font=REALLY_LARGE_FONT, bg = "#a1dbcd")
        LevelLabel.grid(pady = 10, padx = 10, row = 1, column = 1, columnspan=6)
        self.buttons = [[tk.Button(self,command=lambda row=row, column=column: self.CardPicked(row, column, controller, parent),  width=14, height= 9)
                        for column in range(6)] for row in range(3)]
        for row in range(3):
            for column in range(6):
                self.buttons[row][column].grid(row=row + 2, column=column + 1)
        self.tobechecked = None
        self.Attempts = 0
        self.create_cards()

    def create_cards(self):
        answer = []
        count = 0
        self.CreatingAnswer(answer, count)
        ListForNumbers = [row for column in answer for row in column]
        print(ListForNumbers)
        shuffle(ListForNumbers)
        self.answer = ListForNumbers[:6], ListForNumbers[6:12], ListForNumbers[12:18]
        for row in self.buttons:
            for button in row:
                button.config(fg="#a1dbcd", bg="#a1dbcd", state=tk.NORMAL)
        self.start_time = time.time()

    def CreatingAnswer(self, answer, count):
        numberlist = []
        if not count < 9:
            return
        else:
            number = (randint(1, 12))
            number2 = (randint(1, 12))
            signs = ("+", "*","-","/")
            signchosen = (random.choice(signs))
            if signchosen == "*":
                answertobeaddedtolist = number * number2
            elif signchosen == "/":
                 if number % number2 != 0:
                     number = number2 * (randint(1, 12))
                     answertobeaddedtolist = number // number2
                 else:
                     answertobeaddedtolist = number // number2
            elif signchosen == "-":
                if number < number2:
                    number2 = randint(1, number)
                    answertobeaddedtolist = number - number2
                else:
                    answertobeaddedtolist = number - number2
            else:
                answertobeaddedtolist = number + number2
            numbertoaddtolist = (number, signchosen, number2)
            numberlist.append(numbertoaddtolist)
            numberlist.append(answertobeaddedtolist)
            self.CreatingAnswer(answer, count + 1)
        answer.append(numberlist)
        return answer

    def CardPicked(self, row, column, controller, parent):
        self.buttons[row][column].config(bg="white", text=(self.answer[row][column]), font=HUGE_FONT, width=15,
                                         height=10 , state=tk.DISABLED)  # equals the answer that is there
        Validation = False
        if not self.tobechecked:
            self.tobechecked = row, column
        else:
            to, check = self.tobechecked
            if isinstance(self.answer[to][check], tuple):
                FirstNumber = (self.answer[to][check][0])
                LastNumber = (self.answer[to][check][2]) # orginally had sum but the addition meant that it didn't work. Had to slice the tuple to get the first and last elments, i.e the numbers that are going to be used.
                sign = (self.answer[to][check][1])
                if sign == "*":
                    MultipliedNumber = FirstNumber * LastNumber
                    if self.answer[row][column] == MultipliedNumber:
                        Validation = True
                    else:
                        Validation = False
                elif sign == "+":
                    AddedNumber = FirstNumber + LastNumber
                    if self.answer[row][column] == AddedNumber:
                        Validation = True
                    else:
                        Validation = False
                elif sign == "-":
                    SubtractedNumber = FirstNumber - LastNumber
                    if self.answer[row][column] == SubtractedNumber:
                        Validation = True
                    else:
                        Validation = False
                elif sign == "/":
                    DividedNumber = FirstNumber // LastNumber
                    if self.answer[row][column] == DividedNumber:
                        Validation = True
                    else:
                        Validation = False
            elif isinstance(self.answer[row][column], tuple):
                FirstNumber = (self.answer[row][column][0])
                LastNumber = (self.answer[row][column][2]) # orginally had sum but the addition meant that it didn't work. Had to slice the tuple to get the first and last elments, i.e the numbers that are going to be used.
                AddedNumber = FirstNumber + LastNumber
                MultipliedNumber = FirstNumber * LastNumber
                SubtractedNumber = FirstNumber - LastNumber
                DividedNumber = FirstNumber // LastNumber
                sign = (self.answer[row][column][1])
                if sign == "*":
                    if self.answer[to][check] == MultipliedNumber:
                        Validation = True
                    else:
                        Validation = False
                elif sign == "+":
                    if self.answer[to][check] == AddedNumber:
                        Validation = True
                    else:
                        Validation = False
                elif sign == "-":
                    if self.answer[to][check] == SubtractedNumber:
                        Validation = True
                    else:
                        Validation = False
                elif sign == "/":
                    if self.answer[to][check] == DividedNumber:
                        Validation = True
                    else:
                        Validation = False
# if two sums were chose, 8+5 and 9+6, it would come here.
                self.Attempts = self.Attempts + 1# if two sums were chose, 8+5 and 9+6, it would come here.
            if Validation == True:
                self.answer[row][column] = ''
                self.answer[to][check] = '' # orignially had .pop but .pop will not work so had to replace with ""
                if self.answer == (['', '', '', '','',''], ['', '', '', '','',''], ['', '', '', '','','']):
                    self.stop_time = time.time()
                    self.Time = 1000 - (round(self.stop_time - self.start_time, 0))
                    print(self.Time)
                    print(self.Attempts)
                    self.Score = round(self.Time // self.Attempts) * 12
                    self.parent.after(4000, self.AddScoreToTable(controller, parent))
            else:
                self.parent.after(1000, self.HideCards, row, column, to, check)
            self.tobechecked = None

    def HideCards(self, row, column, to, check):
        self.buttons[row][column].config(bg="#a1dbcd", state=tk.NORMAL)
        self.buttons[to][check].config(bg="#a1dbcd", state=tk.NORMAL)

    def AddScoreToTable(self, controller, parent):
        c.execute('CREATE TABLE IF NOT EXISTS Level3Score (ID INTEGER PRIMARY KEY, Username TEXT, Lv3Score INTEGER)')
        c.execute('INSERT INTO Level3Score (Username,Lv3Score) VALUES (?,?)', (Username, self.Score))
        conn.commit()
        showinfo("Score", ("Your Score Was", self.Score))
        self.parent.after(1000, controller.show_frame(showLv3LeaderBoard))

class showLv3LeaderBoard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        Colour = (random.choice(["Black", "Red", "Orange", "Green", "Pink", "Purple", "Blue"]))
        self.configure(background = Colour)
        self.Photo = tk.PhotoImage(file="JustTheLogo.gif")
        photo = tk.PhotoImage(file=r"The Learning CubeTitle.gif")
        Title = tk.Label(self, image=photo, background=Colour)
        Title.image = photo
        Title.grid(row=0, column=1, columnspan=2)
        Logo = tk.PhotoImage(file = r"JustTheLogo.gif")
        LogoLabel1 = tk.Label(self, image = Logo, background = Colour)
        LogoLabel1.image = Logo
        LogoLabel1.grid(row = 0, column = 0)
        LogoLabel2 = tk.Label(self, image = Logo, background = Colour)
        LogoLabel2.image = Logo
        LogoLabel2.grid(row = 0, column = 5)
        conn.commit()
        c.execute("SELECT Username, Lv3Score from Level3Score")
        Scores = c.fetchall()
        MergeSortingScores(Scores)
        tk.Label(self, text = "LEADERBOARD", font=Title_Font, bg=Colour, fg = "white").grid(row = 2, column = 1, columnspan = 2)
        tk.Label(self, text = "1", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 3, column = 1, padx = 50)
        tk.Label(self, text = Scores[0], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 3, column = 2, padx = 50)
        tk.Label(self, text = "2", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 4, column = 1, padx = 50)
        tk.Label(self, text = Scores[1], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 4, column = 2, padx = 50)
        tk.Label(self, text = "3", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 5, column = 1, padx = 50)
        tk.Label(self, text = Scores[2], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 5, column = 2, padx = 50)
        tk.Label(self, text = "4", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 6, column = 1, padx = 50)
        tk.Label(self, text = Scores[3], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 6, column = 2, padx = 50)
        tk.Label(self, text = "5", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 7, column = 1, padx = 50)
        tk.Label(self, text = Scores[4], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 7, column = 2, padx = 50)

        tk.Button(self, text = "CONTINUE", height = 3 , width = 50, command=lambda: controller.show_frame(Level2)).grid\
            (row = 8, column = 1, pady = 50)#AND PUT THIS AS THE ONE PLUS THE VARIABLE SO IT NOWS TO GO TO THE NXT LVL
        tk.Button(self, text = "EXIT", height = 3 , width = 50, command= self.quit).grid(row = 8, column = 2, pady = 50)

class Level4(tk.Frame): # Commenting Level 4 as it is the hardest and has Level1, 2 and 3 incoropated within.
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.configure(background= "#a1dbcd") # backgroun is set to defualt in order to see cards
        self.Photo = tk.PhotoImage(file="JustTheLogo.gif")
        photo = tk.PhotoImage(file=r"The Learning CubeTitle.gif")
        Title = tk.Label(self, image=photo, background="#a1dbcd")
        Title.image = photo
        Title.grid(row=0, column=1, columnspan=6)
        Logo = tk.PhotoImage(file = r"JustTheLogo.gif")
        LogoLabel1 = tk.Label(self, image = Logo, background = "#a1dbcd")
        LogoLabel1.image = Logo
        LogoLabel1.grid(row = 0, column = 0)
        LogoLabel2 = tk.Label(self, image = Logo, background = "#a1dbcd")
        LogoLabel2.image = Logo
        LogoLabel2.grid(row = 0, column = 7)
        LevelLabel = tk.Label(self, text=("THIS IS LEVEL FOUR")
                              ,font=REALLY_LARGE_FONT, bg = "#a1dbcd")
        LevelLabel.grid(pady = 10, padx = 10, row = 1, column = 1, columnspan=6)
        self.buttons = [[tk.Button(self,command=lambda row=row, column=column: self.CardPicked(row, column, controller),  width=14, height= 9)
                        for column in range(6)] for row in range(4)]
        for row in range(4):
            for column in range(6):
                self.buttons[row][column].grid(row=row + 2, column=column + 1)
        self.tobechecked = None
        self.Attempts = 0
        self.create_cards()

    def create_cards(self):
        answer = []
        count = 0
        self.CreatingAnswer(answer, count)
        ListForNumbers = [row for column in answer for row in column]
        print(ListForNumbers)
        shuffle(ListForNumbers)
        self.answer = ListForNumbers[:6], ListForNumbers[6:12], ListForNumbers[12:18], ListForNumbers[18:24]
        for row in self.buttons:
            for button in row:
                button.config(fg="#a1dbcd", bg="#a1dbcd", state=tk.NORMAL)
        self.start_time = time.time()

    def CreatingAnswer(self, answer, count):
        numberlist = []
        if not count < 12:
            return
        else:
            signchosen = (random.choice(("+", "*", "-", "/")))
            fractionsignchosen = (random.choice(("+", "*")))
            Decision = (random.choice(("Fraction","+", "*","-","/")))
            if Decision == "Fraction":
                numberchoice = random.choice((1, 3))
                numberchoice2 = random.choice((2, 4))
                numberchoice3 = random.choice((1, 3))
                numberchoice4 = random.choice((2, 4))
                if numberchoice > numberchoice2:
                    numberchoice = randint(1, numberchoice2)
                number = Fraction(numberchoice, numberchoice2)
                number2 = Fraction(numberchoice3, numberchoice4)
                if fractionsignchosen == "+":
                    answertobeaddedtolist = number + number2
                elif fractionsignchosen == "*":
                    answertobeaddedtolist = number * number2
            else:
                number = (randint(1, 12))
                number2 = (randint(1, 12))
                if signchosen == "*":
                    answertobeaddedtolist = number * number2
                elif signchosen == "/":
                     if number % number2 != 0:
                         number = number2 * (randint(1, 12))
                         answertobeaddedtolist = number // number2
                     else:
                         answertobeaddedtolist = number // number2
                elif signchosen == "-":
                    if number < number2:
                        number2 = randint(1, number)
                        answertobeaddedtolist = number - number2
                    else:
                        answertobeaddedtolist = number - number2
                else:
                    answertobeaddedtolist = number + number2
            if Decision == "Fraction":
                fractiontoaddtolist = (number, fractionsignchosen, number2)
                numberlist.append(fractiontoaddtolist)
            else:
                numbertoaddtolist = (number, signchosen, number2)
                numberlist.append(numbertoaddtolist)
            numberlist.append(answertobeaddedtolist)
            self.CreatingAnswer(answer, count + 1)
        answer.append(numberlist)
        return answer

    def CardPicked(self, row, column, controller):
        self.buttons[row][column].config(bg="white", text=(self.answer[row][column]), font= Card_FONT, width=15,
                                         height=10 , state=tk.DISABLED)  # equals the answer that is there
        Validation = False
        if not self.tobechecked:
            self.tobechecked = row, column
        else:
            to, check = self.tobechecked
            if isinstance(self.answer[to][check], tuple):
                FirstNumber = (self.answer[to][check][0])
                LastNumber = (self.answer[to][check][2]) # orginally had sum but the addition meant that it didn't work. Had to slice the tuple to get the first and last elments, i.e the numbers that are going to be used.
                sign = (self.answer[to][check][1])
                if sign == "*":
                    MultipliedNumber = FirstNumber * LastNumber
                    if self.answer[row][column] == MultipliedNumber:
                        Validation = True
                elif sign == "+":
                    AddedNumber = FirstNumber + LastNumber
                    if self.answer[row][column] == AddedNumber:
                        Validation = True
                elif sign == "-":
                    SubtractedNumber = FirstNumber - LastNumber
                    if self.answer[row][column] == SubtractedNumber:
                        Validation = True
                elif sign == "/":
                    DividedNumber = FirstNumber // LastNumber
                    if self.answer[row][column] == DividedNumber:
                        Validation = True
                else:
                    Validation = False
            elif isinstance(self.answer[row][column], tuple):
                FirstNumber = (self.answer[row][column][0])
                LastNumber = (self.answer[row][column][2]) # orginally had sum but the addition meant that it didn't work. Had to slice the tuple to get the first and last elments, i.e the numbers that are going to be used.
                AddedNumber = FirstNumber + LastNumber
                MultipliedNumber = FirstNumber * LastNumber
                SubtractedNumber = FirstNumber - LastNumber
                DividedNumber = FirstNumber // LastNumber
                sign = (self.answer[row][column][1])
                if sign == "*":
                    if self.answer[to][check] == MultipliedNumber:
                        Validation = True
                    else:
                        Validation = False
                elif sign == "+":
                    if self.answer[to][check] == AddedNumber:
                        Validation = True
                    else:
                        Validation = False
                elif sign == "-":
                    if self.answer[to][check] == SubtractedNumber:
                        Validation = True
                    else:
                        Validation = False
                elif sign == "/":
                    if self.answer[to][check] == DividedNumber:
                        Validation = True
                    else:
                        Validation = False
# if two sums were chose, 8+5 and 9+6, it would come here.
                self.Attempts = self.Attempts + 1
            if Validation == True:
                self.answer[row][column] = ''
                self.answer[to][check] = '' # orignially had .pop but .pop will not work so had to replace with ""
                if self.answer == (['', '', '', '', '', ''], ['', '', '', '', '', ''], ['', '', '', '', '', ''], ['', '', '', '', '', '']):
                    print(self.Attempts)
                    self.Score = self.Attempts * 10
                    self.parent.after(5000, self.AddScoreToTable, controller)
            else:
                self.parent.after(1000, self.HideCards, row, column, to, check)
            self.tobechecked = None

    def HideCards(self, row, column, to, check):
        self.buttons[row][column].config(bg="#a1dbcd", state=tk.NORMAL)
        self.buttons[to][check].config(bg="#a1dbcd", state=tk.NORMAL)

    def AddScoreToTable(self, controller):
        c.execute('CREATE TABLE IF NOT EXISTS Level4Score (ID INTEGER PRIMARY KEY, Username TEXT, Lv4Score INTEGER)')
        c.execute('INSERT INTO Level4Score (Username,Lv4Score) VALUES (?,?)', (Username, self.Score))
        conn.commit()
        showinfo("Score", ("Your Score Was", self.Score))
        self.parent.after(1000, controller.show_frame(showLv4LeaderBoard))

class showLv4LeaderBoard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        Colour = (random.choice(["Black", "Red", "Orange", "Green", "Pink", "Purple", "Blue"]))
        self.configure(background = Colour)
        self.Photo = tk.PhotoImage(file="JustTheLogo.gif")
        photo = tk.PhotoImage(file=r"The Learning CubeTitle.gif")
        Title = tk.Label(self, image=photo, background=Colour)
        Title.image = photo
        Title.grid(row=0, column=1, columnspan=2)
        Logo = tk.PhotoImage(file = r"JustTheLogo.gif")
        LogoLabel1 = tk.Label(self, image = Logo, background = Colour)
        LogoLabel1.image = Logo
        LogoLabel1.grid(row = 0, column = 0)
        LogoLabel2 = tk.Label(self, image = Logo, background = Colour)
        LogoLabel2.image = Logo
        LogoLabel2.grid(row = 0, column = 5)
        conn.commit()
        c.execute("SELECT Username, Lv4Score from Level4Score")
        Scores = c.fetchall()
        MergeSortingScores(Scores)
        tk.Label(self, text = "LEADERBOARD", font=Title_Font, bg=Colour, fg = "white").grid(row = 2, column = 1, columnspan = 2)
        tk.Label(self, text = "1", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 3, column = 1, padx = 50)
        tk.Label(self, text = Scores[0], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 3, column = 2, padx = 50)
        tk.Label(self, text = "2", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 4, column = 1, padx = 50)
        tk.Label(self, text = Scores[1], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 4, column = 2, padx = 50)
        tk.Label(self, text = "3", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 5, column = 1, padx = 50)
        tk.Label(self, text = Scores[2], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 5, column = 2, padx = 50)
        tk.Label(self, text = "4", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 6, column = 1, padx = 50)
        tk.Label(self, text = Scores[3], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 6, column = 2, padx = 50)
        tk.Label(self, text = "5", font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 7, column = 1, padx = 50)
        tk.Label(self, text = Scores[4], font=REALLY_LARGE_FONT, bg=Colour, fg = "white").grid(row = 7, column = 2, padx = 50)

        tk.Button(self, text = "CONTINUE", height = 3 , width = 50, command=lambda: controller.show_frame(ChoiceForGame)).grid\
            (row = 8, column = 1, pady = 50)#AND PUT THIS AS THE ONE PLUS THE VARIABLE SO IT NOWS TO GO TO THE NXT LVL
        tk.Button(self, text = "EXIT", height = 3 , width = 50, command= self.quit).grid(row = 8, column = 2, pady = 50)

def LogInMain():
    app = LogIn()
    app.mainloop() # Keeps the LogIn Page running, when it is initalised, it runs through the entire code and without this here it woul just continue through the rest of the program. Only LogIn an the next frame (TLCApp) need this because they have inherited a class from tkinter, whilst all the other classses inherit from tk.Frame from TLCApp

def TLCAppMain(self):
    self.destroy()
    app = TLCApp()
    app.mainloop()

def MergeSortingScores (Scores):
    if len(Scores)>1: # if the length of scores is bigger than one then
        mid = len(Scores)//2 # the middle point is the length of score divided by 2
        lefthalf = Scores[:mid] #left half equals the left half of the score, this will be used later
        righthalf = Scores[mid:] #right half equals the right half of the score, this will be used later
        MergeSortingScores(lefthalf) # I call recursion on the left half
        MergeSortingScores(righthalf) #  after I have finished
        i,j,k = 0,0,0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i][1] > righthalf[j][1]:
                Scores[k]=lefthalf[i]
                i=i+1
            else:
                Scores[k]=righthalf[j]
                j=j+1
            k=k+1
        while i < len(lefthalf):
            Scores[k]=lefthalf[i]
            i=i+1
            k=k+1
        while j < len(righthalf):
            Scores[k]=righthalf[j]
            j=j+1
            k=k+1

if __name__ == '__main__':
    LogInMain()

