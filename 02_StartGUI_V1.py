from functools import partial
from tkinter import *



class Start:
    def __init__(self, parent):
        full_background = "#A88770"
        button_background = "#F1DCA7"

        # Setup start frame
        self.start_frame = Frame(padx=10, pady=10,bg=full_background)
        self.start_frame.grid()

        # Title Label
        self.egyptian_gods_title_label = Label(self.start_frame, text="Egyptian Gods Quiz", font="arial 24 bold", wrap=250,bg=full_background)
        self.egyptian_gods_title_label.grid(row=1)
        
        # Sub title label
        self.egyptian_gods_label = Label(self.start_frame, text="Test how well you know the egyptian gods", font = "arial 14",wrap=250,bg=full_background)
        self.egyptian_gods_label.grid(row=2)

        # Play button
        self.play_button = Button(self.start_frame, text="Play",font="arial 16 bold",pady=5,padx=30,bg=button_background,command=self.to_difficulty)
        self.play_button.grid(row=3, pady=10)

        # Help button
        self.help_button = Button(self.start_frame, text="Instructions",font = "arial 12 bold",bg=button_background, command=self.to_instructions)
        self.help_button.grid(row=4, pady=10)

    # Open Difficuulty window
    def to_difficulty(self):
        Difficulty(self)
        root.withdraw()
    # open instructions window
    def to_instructions(self):
        Instructions(self)


class Difficulty:
    def __init__(self, partner):
        self.difficulty_box = Toplevel()
        self.difficulty_box.protocol('WM_DELETE_WINDOW', partial(self.close_difficulty, partner))
        self.difficulty_frame = Frame(self.difficulty_box)
        self.difficulty_frame.grid()
        self.heading_label = Label(self.difficulty_frame, text="Difficulty Box",
                                   font="Arial 24 bold", padx=10, pady=10)
        self.heading_label.grid(row=0)
        # self.easy_button = Button(self.game_frame, text="Easy 3 lives \n 1x score multiplier", padx=10,
        #                           pady=10)
        # self.easy_button.grid(row=1)
    def close_difficulty(self,partner):
        root.destroy()

class Instructions:
    def __init__(self,partner):
        partner.help_button.config(state=DISABLED)
        self.instructions_box = Toplevel()
        self.instructions_box.protocol('WM_DELETE_WINDOW', partial(self.close_instructions, partner))
        self.instructions_frame = Frame(self.instructions_box)
        self.instructions_frame.grid()
        self.heading_label = Label(self.instructions_frame, text="Instructions Box",
                                    font="Arial 24 bold", padx=10, pady=10)
        self.heading_label.grid(row=0)

    def close_instructions(self,partner):
        partner.help_button.config(state=NORMAL)
        self.instructions_box.destroy()

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Egyptian Gods")
    something = Start(root)
    root.mainloop()