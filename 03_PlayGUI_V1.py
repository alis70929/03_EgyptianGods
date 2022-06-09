from functools import partial
from tkinter import *
from tkinter.messagebox import QUESTION



class Start:
    def __init__(self, parent):
        full_background = "#A88770"
        button_background = "#F1DCA7"

        # Setup start frame
        self.start_frame = Frame(padx=10, pady=10,bg=full_background)
        self.start_frame.grid(sticky=NSEW)
  
        self.start_frame.columnconfigure(index=0,weight=1)
        

        # Title Label
        self.start_frame.rowconfigure(index=0,weight=1)
        self.egyptian_gods_title_label = Label(self.start_frame, text="Egyptian Gods Quiz", font="arial 24 bold", wrap=250,bg=full_background)
        self.egyptian_gods_title_label.grid(row=0)
        
        # Sub title label
        self.start_frame.rowconfigure(index=1,weight=1)
        self.egyptian_gods_label = Label(self.start_frame, text="Test how well you know the egyptian gods", font = "arial 14",wrap=250,bg=full_background)
        self.egyptian_gods_label.grid(row=1)

        # Play button
        self.start_frame.rowconfigure(index=2,weight=1)
        self.play_button = Button(self.start_frame, text="Play",font="arial 16 bold",width=10,height=2,bg=button_background,command=self.to_difficulty)
        self.play_button.grid(row=2, pady=10)

        # Help button
        self.start_frame.rowconfigure(index=3,weight=1)
        self.help_button = Button(self.start_frame, text="Instructions",font = "arial 12 bold",width=10,height=1,bg=button_background, command=self.to_instructions)
        self.help_button.grid(row=3, pady=10)

    # Open Difficuulty window
    def to_difficulty(self):
        Difficulty(self)
        root.withdraw()
    # open instructions window
    def to_instructions(self):
        Instructions(self)


class Difficulty:
    def __init__(self, partner):
        full_background = "#A88770"
        button_background = "#F1DCA7"
        # Create Difficulty window
        self.difficulty_box = Toplevel()

        # Make closing using corner button use custom functionality
        self.difficulty_box.protocol('WM_DELETE_WINDOW', partial(self.close_difficulty, partner))

        # Populate window
        # Base Frame
        self.difficulty_frame = Frame(self.difficulty_box,bg = full_background)
        self.difficulty_frame.grid()
        # Heading labeldw
        self.heading_label = Label(self.difficulty_frame, text="Difficulty",
                                font="Arial 24 bold", bg=full_background,padx=10, pady=10)
        self.heading_label.grid(row=0)

        # Easy Button
        self.pad_frame = Frame(self.difficulty_frame)
        self.pad_frame.grid(row=1)
        self.easy_button = Button(self.difficulty_frame, text="Easy 3 lives \n 1x score multiplier", padx=10,
                                  pady=10, bg="#b4e0b2", command=lambda: self.to_game(1,3))
        self.easy_button.grid(row=1,pady=5)

        # medium Button
        self.medium_button = Button(self.difficulty_frame, text="medium 2 lives \n 2x score multiplier", padx=10,
                                  pady=10, bg="#e0d1a2", command=lambda: self.to_game(2,2))
        self.medium_button.grid(row=2,pady=5)

        # Hard Button
        self.Hard_button = Button(self.difficulty_frame, text="Hard 1 lives \n 3x score multiplier", padx=10,
                                  pady=10, bg="#e9b3b0", command=lambda: self.to_game(3,1))
        self.Hard_button.grid(row=3,pady=5)

    def close_difficulty(self,partner):
        root.destroy()
        
    def to_game(self, difficulty, lives):
        Game(self, difficulty, lives)
        self.difficulty_box.withdraw()

class Instructions:
    def __init__(self,partner):
        # Disable button that opened this window to stop multiple of the same window
        partner.help_button.config(state=DISABLED)

        # Create new window
        self.instructions_box = Toplevel()
        # assign custom function to closing window to make it enable the button used to open this window
        self.instructions_box.protocol('WM_DELETE_WINDOW', partial(self.close_instructions, partner))

        # Frame Init
        self.instructions_frame = Frame(self.instructions_box)
        self.instructions_frame.grid()

        # Heading Label 
        self.heading_label = Label(self.instructions_frame, text="Instructions Box",
                                    font="Arial 24 bold", padx=10, pady=10)
        self.heading_label.grid(row=0)

    # custom close functionality to re enable the instructions button
    def close_instructions(self,partner):
        partner.help_button.config(state=NORMAL)
        self.instructions_box.destroy()

class Game:
    def __init__(self,partner,difficulty,lives):

        full_background = "#A88770"
        button_background = "#F1DCA7"
        # Create New Window
        self.Game_box = Toplevel()
        self.Game_box.geometry("600x350")
        # Assign custom function to the closing of the window so that on close it goes to summany page instead of fully closing
        self.Game_box.protocol('WM_DELETE_WINDOW', partial(self.close_game, partner))

        # Initialize Frame
        
        self.Game_box.columnconfigure(index=0,weight=1)
        self.Game_box.rowconfigure(index=0,weight=1)
        self.Game_frame = Frame(self.Game_box,bg=full_background)
        self.Game_frame.grid(sticky=NSEW)

        self.round = 1
        # Game Question label
        self.question_heading_label = Label(self.Game_frame, text="Question {}".format(self.round), font="Arial 24 bold", padx=10, pady=10,bg=full_background)
        self.question_heading_label.grid(row=0,sticky=NW)

        self.question_label = Label(self.Game_frame, text="This is where the question goes", font="Arial 12", padx=10,wrap=300,justify=LEFT,bg=full_background)
        self.question_label.grid(row=0,rowspan=3,column=0,sticky=NW,pady=50)

        self.Game_frame.columnconfigure(index=1,weight=1)
        self.answer_buttons_frame = Frame(self.Game_frame,bg=full_background)
        self.answer_buttons_frame.grid(row=0,column=1,sticky=E,rowspan=4)

        button_font = "Arial 14 "
        self.answer_button1 = Button(self.answer_buttons_frame,text="button 1", font=button_font,width=20,height=2,bg=button_background)
        self.answer_button1.grid(row=0,column=1,pady=(20,10), padx=20)

        self.answer_button2 = Button(self.answer_buttons_frame,text="button 2", font=button_font,width=20,height=2,bg=button_background)
        self.answer_button2.grid(row=1,column=1,pady=10,padx=20)

        self.answer_button3 = Button(self.answer_buttons_frame,text="button 3", font=button_font,width=20,height=2,bg=button_background)
        self.answer_button3.grid(row=2,column=1,pady=10,padx=20)

        self.answer_button4 = Button(self.answer_buttons_frame,text="button 4", font=button_font,width=20,height=2,bg=button_background)
        self.answer_button4.grid(row=3,column=1,pady=10,padx=20)
        
        self.help_button = Button(self.Game_frame, text="Instructions",font = "arial 12 bold",width=10,height=1,bg=button_background, command=self.to_instructions)
        self.help_button.grid(row=3, pady=(175,10))

    # custom close functionality that opens summary page rather than fully ending the game
    def close_game(self,partner):
        root.destroy()

    # open instructions window
    def to_instructions(self):
        Instructions(self)

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Egyptian Gods")
    root.geometry("300x300")
    root.columnconfigure(index=0,weight=1)
    root.rowconfigure(index=0,weight=1)
    something = Start(root)
    root.mainloop()