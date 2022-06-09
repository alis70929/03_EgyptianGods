from functools import partial
from tkinter import *



class Start:
    def __init__(self, parent):
        full_background = "#A88770"
        button_background = "#F1DCA7"

        # Setup start frame
        self.start_frame = Frame(padx=10, pady=10,bg=full_background)
        self.start_frame.grid(sticky=NSEW)
        
        self.start_frame.columnconfigure(index=0,weight=1)
        self.start_frame.columnconfigure(index=1,weight=1)
        self.start_frame.columnconfigure(index=2,weight=1)

        # Title Label
        self.start_frame.rowconfigure(index=0,weight=1)
        
        self.egyptian_gods_title_label = Label(self.start_frame, text="Egyptian Gods Quiz", font="arial 24 bold", wrap=250,bg=full_background)
        self.egyptian_gods_title_label.grid(row=0,column=1,sticky=N)
        
        # Sub title label
        self.start_frame.rowconfigure(index=1,weight=2)
        self.egyptian_gods_label = Label(self.start_frame, text="Test how well you know the egyptian gods", font = "arial 14",wrap=250,bg=full_background)
        self.egyptian_gods_label.grid(row=1,column=1,sticky=N)

        # Play button
        self.start_frame.rowconfigure(index=2,weight=1)
        play_button_font = "arial {} bold".format(int(40 * percent_width))
        self.play_button = Button(self.start_frame, text="Play",font=play_button_font,width=10, height=2,bg=button_background,command=self.to_difficulty)
        self.play_button.grid(row=2, column=1,pady=10,sticky=S)

        #Help button
        self.start_frame.rowconfigure(index=3,weight=1)
        help_button_font = "arial {} bold".format(int(30 * percent_width))
        self.help_button = Button(self.start_frame, text="Instructions",width=9 ,height=2 ,font = help_button_font,bg=button_background, command=self.to_instructions)
        self.help_button.grid(row=3,column=1, pady=10,sticky=S)
    # Open Difficuulty window
    def to_difficulty(self):
        Difficulty(self)
        root.withdraw()
    # open instructions window
    def to_instructions(self):
        Instructions(self)


class Difficulty:
    def __init__(self, partner):

        # Create Difficulty window
        self.difficulty_box = Toplevel()

        # Make closing using corner button use custom functionality
        self.difficulty_box.protocol('WM_DELETE_WINDOW', partial(self.close_difficulty, partner))

        # Populate window
        # Base Frame
        self.difficulty_frame = Frame(self.difficulty_box)
        self.difficulty_frame.grid()

        # Heading label
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
global percent_height,percent_width
if __name__ == "__main__":
    root = Tk()
    target_height = 1080
    target_width = 1920
    screen_width = 1080
    screen_height = 720
    percent_width = (screen_width/target_width )
    percent_height = (screen_height/target_height)
    root.geometry("{}x{}".format(screen_width,screen_height))
    #root.wm_state('zoomed')
    
    root.columnconfigure(index=0,weight=1)
    root.rowconfigure(index=0,weight=1)
    root.title("Egyptian Gods")
    something = Start(root)
    root.mainloop()
    