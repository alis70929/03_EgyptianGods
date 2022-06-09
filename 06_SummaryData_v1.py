from functools import partial
from tkinter import *
import csv
import random




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
        self.game_history = []
        self.correct = 0
        self.lives = lives
        self.difficulty = difficulty
        self.round = 0

        self.correct_answer_index = 0
        # Create New Window
        self.Game_box = Toplevel()
        self.Game_box.geometry("600x350")
        # Assign custom function to the closing of the window so that on close it goes to summany page instead of fully closing
        self.Game_box.protocol('WM_DELETE_WINDOW', partial(self.to_summary))

        # Initialize Frame
        self.Game_box.columnconfigure(index=0,weight=1)
        self.Game_box.rowconfigure(index=0,weight=1)
        self.Game_frame = Frame(self.Game_box,bg=full_background)
        self.Game_frame.grid(sticky=NSEW)

        
        # Game Question label
        self.question_heading_label = Label(self.Game_frame, text="Question {} | Lives: {}".format(self.round,self.lives), font="Arial 24 bold", padx=10, pady=10,bg=full_background)
        self.question_heading_label.grid(row=0,sticky=NW)

        self.question_label = Label(self.Game_frame, text="This is where the question goes", font="Arial 12", padx=10,wrap=300,justify=LEFT,bg=full_background)
        self.question_label.grid(row=0,rowspan=3,column=0,sticky=NW,pady=50)

        self.Game_frame.columnconfigure(index=1,weight=1)
        self.answer_buttons_frame = Frame(self.Game_frame,bg=full_background)
        self.answer_buttons_frame.grid(row=0,column=1,sticky=E,rowspan=4)

        button_font = "Arial 14 "
        self.answer_buttons = []
        self.answer_button1 = Button(self.answer_buttons_frame,text="button 1", font=button_font,width=20,height=2,bg=button_background,command=lambda :self.answer_question(0))
        self.answer_button1.grid(row=0,column=1,pady=(20,10), padx=20)
        self.answer_buttons.append(self.answer_button1)

        self.answer_button2 = Button(self.answer_buttons_frame,text="button 2", font=button_font,width=20,height=2,bg=button_background,command=lambda :self.answer_question(1))
        self.answer_button2.grid(row=1,column=1,pady=10,padx=20)
        self.answer_buttons.append(self.answer_button2)

        self.answer_button3 = Button(self.answer_buttons_frame,text="button 3", font=button_font,width=20,height=2,bg=button_background,command=lambda :self.answer_question(2))
        self.answer_button3.grid(row=2,column=1,pady=10,padx=20)
        self.answer_buttons.append(self.answer_button3)

        self.answer_button4 = Button(self.answer_buttons_frame,text="button 4", font=button_font,width=20,height=2,bg=button_background,command=lambda :self.answer_question(3))
        self.answer_button4.grid(row=3,column=1,pady=10,padx=20)
        self.answer_buttons.append(self.answer_button4)

        self.Game_frame.rowconfigure(index=2,weight=1)
        self.continue_button = Button(self.Game_frame, text="Continue",font = "arial 15 bold",width=15,height=1,bg=button_background, command=self.next_question)
        self.continue_button.grid(row=2,sticky=S,pady=10)

        self.help_button = Button(self.Game_frame, text="Instructions",font = "arial 12 bold",width=10,height=1,bg=button_background, command=self.to_instructions)
        self.help_button.grid(row=3,pady=10)

        # Set up question and wrong answer lists
        # Open csv file and get all data from it. 
        file = open("03_EgyptianGods\Egyptian_gods.csv",newline="")
        reader = csv.reader(file)
        self.question_list = list(reader)
        file.close()

        # Get all gods from the above csv file
        self.gods_list  = []
        for row in self.question_list:
            self.gods_list.append(row[0])
        
        self.next_question()
    # open instructions window
    def to_instructions(self):
        Instructions(self)
    
    def next_question(self):

        # exit to summary if completely out of lives
        if self.lives <= 0:
                self.to_summary()
        
        round_data = []
        # Set qeustion heading label, add to round counter
        self.round += 1
        self.question_heading_label.config(text="Question {} | Lives: {}".format(self.round,self.lives))
        round_data.append(self.round)
        round_data.append(self.lives)
        # random question
        current_question =  random.choice(self.question_list)
        self.question_list.remove(current_question)

        question_text = "What is the name of {}".format(current_question[1])
        self.question_label.config(text=question_text)
        round_data.append(question_text)

        correct_answer = current_question[0]
        print(correct_answer)
        round_data.append(correct_answer)
        random_answers = []
        while len(random_answers) < 3:
            random_answer = self.gods_list[random.randrange(0,len(self.gods_list) - 1)]
            if random_answers.count(random_answer) >= 1:
                continue
            
            if random_answer == correct_answer:
                continue

            random_answers.append(random_answer)


        answers_summary_list = []
        buttons_indexes  = [0,1,2,3]
        chosen_button_index = random.choice(buttons_indexes)
        self.answer_buttons[chosen_button_index].config(text=correct_answer,bg = "#F1DCA7",state=NORMAL)
        self.correct_answer_index = chosen_button_index
        answers_summary_list.append([self.correct_answer_index,correct_answer,"Correct"])
        buttons_indexes.remove(chosen_button_index)
        for x in range(0,3):
            chosen_button_index = random.choice(buttons_indexes)
            chosen_random_answer = random.choice(random_answers)
            
            self.answer_buttons[chosen_button_index].config(text=chosen_random_answer,bg="#F1DCA7",state=NORMAL)

            answers_summary_list.append([chosen_button_index,chosen_random_answer,"Incorrect"])

            buttons_indexes.remove(chosen_button_index)
            random_answers.remove(chosen_random_answer)
        
        round_data.append(answers_summary_list)

        self.continue_button.grid_remove()
        
        self.game_history.append(round_data)
       
        
    def answer_question(self,answer_index):
        if answer_index == self.correct_answer_index:
            self.answer_buttons[answer_index].config(bg="#9bdd98")
            self.correct += 1
        else:
            self.answer_buttons[answer_index].config(bg="#e78a85")
            self.answer_buttons[self.correct_answer_index].config(bg="#ce9745")
            self.lives -= 1
        
        self.game_history[len(self.game_history) - 1].append(answer_index)
        
        for item in range(0,4):
            self.answer_buttons[item].config(state=DISABLED)

        self.question_heading_label.config(text="Question {} | Lives: {}".format(self.round,self.lives))
        self.continue_button.grid()

    def to_summary(self):
        self.Game_box.withdraw()
        Summary(self,self.game_history,self.correct,self.round - self.correct,self.difficulty)

class Summary():
    def __init__(self,partner,game_history,correct,incorrect,difficulty):
        print(game_history)
        partner.help_button.config(state=DISABLED)
        self.summary_box = Toplevel()
        self.summary_box.protocol('WM_DELETE_WINDOW', partial(self.close_summary, partner))
        self.summary_frame = Frame(self.summary_box)
        self.summary_frame.grid()
        self.heading_label = Label(self.summary_frame, text="Game Over",
                                    font="Arial 24 bold", padx=10, pady=10)
        self.heading_label.grid(row=0)

        self.correct_label = Label(self.summary_frame, text="Questions Answered :{}".format(correct + incorrect),
                                    font="Arial 12 bold", padx=10, pady=2)
        self.correct_label.grid(row=1)

        self.correct_label = Label(self.summary_frame, text="Correct:{}".format(correct),
                                    font="Arial 12 bold", padx=10, pady=2)
        self.correct_label.grid(row=2)

        self.incorrect_label = Label(self.summary_frame, text="Incorrect:{}".format(incorrect),
                                    font="Arial 12 bold", padx=10, pady=2)
        self.incorrect_label.grid(row=3)

        self.score_label = Label(self.summary_frame, text="Score:{}".format(correct * difficulty),
                                    font="Arial 12 bold", padx=10, pady=2)
        self.score_label.grid(row=4)

        self.play_again_button = Button(self.summary_frame, text="Play Again",font = "arial 16 bold",width=10,height=1, command=self.to_difficulty)
        self.play_again_button.grid(row=5,pady=(10,5))

        self.export_button = Button(self.summary_frame, text="Export to file",font = "arial 12 bold",height=1, command=self.to_export)
        self.export_button.grid(row=6,pady=5)
        
        self.quit_button = Button(self.summary_frame, text="Quit",font = "arial 12 bold",height=1, command=self.close_summary)
        self.quit_button.grid(row=7,pady=5)

    def close_summary(self,partner):
        root.destroy()
    # Open Difficuulty window
    def to_difficulty(self):
        Difficulty(self)
        self.summary_box.destroy()
    
    def to_export(self):
        Export(self)

class Export():
    def __init__(self,partner):
        partner.export_button.config(state=DISABLED)
        self.export_box = Toplevel()
        self.export_box.protocol('WM_DELETE_WINDOW', partial(self.close_export, partner))
        self.export_frame = Frame(self.export_box)
        self.export_frame.grid()
        self.heading_label = Label(self.export_frame, text="Export To File Box",
                                    font="Arial 24 bold", padx=10, pady=10)
        self.heading_label.grid(row=0)
    def close_export(self,partner):
         partner.export_button.config(state=NORMAL)
         self.export_box.destroy()

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Egyptian Gods")
    root.geometry("300x300")
    root.columnconfigure(index=0,weight=1)
    root.rowconfigure(index=0,weight=1)
    something = Start(root)
    root.mainloop()