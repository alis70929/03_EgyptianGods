
from tkinter import *

class Start:
    def __init__(self, parent):

        
        full_background = "#A88770"
        button_background = "#F1DCA7"
        self.game_box = Toplevel()
        self.game_box.overrideredirect(True) # turns off title bar, geometry

        # make a frame for the title bar
        self.title_bar = Frame(self.game_box,bg='white')
        self.title_bar.grid(sticky="ew")
        # Make the frame sticky for every case
        self.title_bar.grid_rowconfigure(0, weight=1)
        self.title_bar.grid_columnconfigure(0, weight=1)

        self.title_bar_buttons = Frame(self.title_bar,bg="white")
        self.title_bar_buttons.grid(sticky="e")

        self.minimize_button = Button(self.title_bar,text='_', command=self.game_box.iconify)
        self.minimize_button.grid(row=0,column=0)
        self.close_button = Button(self.title_bar,text='X', command=self.game_box.destroy)
        self.close_button.grid(row=0,column=1)



        self.title_bar.bind("<B1-Motion>", move_window)
        self.title_bar.bind("<Button-1>", get_pos)

        self.start_frame = Frame(self.game_box,padx=10, pady=10,bg=full_background)
        self.start_frame.grid()

        self.egyptian_gods_label = Label(self.start_frame, text="Egyptian Gods Quiz", font="arial 24 bold", wrap=250,bg=full_background)
        self.egyptian_gods_label.grid(row=1)

        self.egyptian_gods_label = Label(self.start_frame, text="Test how well you know the egyptian gods", font = "arial 14",wrap=250,bg=full_background)
        self.egyptian_gods_label.grid(row=2)

        self.play_button = Button(self.start_frame, text="Play",font="arial 16 bold",pady=5,padx=30,bg=button_background,command=self.to_game)
        self.play_button.grid(row=3, pady=10)

        self.help_button = Button(self.start_frame, text="Instructions",font = "arial 12 bold",bg=button_background)
        self.help_button.grid(row=4, pady=10)

    def to_game(self):
            Game(self)


class Game:
    def __init__(self, partner):


        self.balance = IntVar()


        self.game_box = Toplevel()
        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        self.heading_label = Label(self.game_frame, text="Heading",
                                   font="Arial 24 bold", padx=10, pady=10)
        self.heading_label.grid(row=0)

        self.balance_frame = Frame(self.game_frame)
        self.balance_frame.grid(row=1)

        self.balance_label = Label(self.game_frame, text="Balance...")
        self.balance_label.grid(row=2)

        self.play_button = Button(self.game_frame, text="Gain", padx=10,
                                  pady=10, command=self.reveal_boxes)
        self.play_button.grid(row=3)

    def reveal_boxes(self):
        current_balance = self.balance.get()
        current_balance += 2

        self.balance.set(current_balance)

        self.balance_label.configure(text="Balance: {}".format(current_balance))

def get_pos(event):
    global xwin
    global ywin

    xwin = event.x
    ywin = event.y

def move_window(event):
    root.geometry("+{}+{}".format(event.x_root - xwin,event.y_root - ywin))



# main routine
if __name__ == "__main__":
    root = Tk()
    window = Start(root)
    root.mainloop()