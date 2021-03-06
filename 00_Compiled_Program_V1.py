from functools import partial
from tkinter import *
import csv
import random
import re


from numpy import append, diff, full



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
        # Colour Pallete
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

        # Difficulty buttons that open main game and pass through a number that corresponds to teh difficulty multiplier(1 = easy, 2 = medium, 3= hard)
        # and also passed along the corresponding amount of lives(easy = 3, medium = 2, hard = 1)

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

    # Closing difficulty fully closes game
    def close_difficulty(self,partner):
        root.destroy()
    
    # function to open main game window with lives and difficulty multiplier passed through
    def to_game(self, difficulty, lives):
        Game(self, difficulty, lives)
        self.difficulty_box.withdraw()

# Instructions Window
class Instructions:
    def __init__(self,partner):
        
        # Colour Palette
        full_background = "#A88770"
        button_background = "#F1DCA7"
        # Disable button that opened this window to stop multiple of the same window
        partner.help_button.config(state=DISABLED)

        # Create new window
        self.instructions_box = Toplevel()
        # assign custom function to closing window to make it enable the button used to open this window
        self.instructions_box.protocol('WM_DELETE_WINDOW', partial(self.close_instructions, partner))

        # Frame Init
        self.instructions_frame = Frame(self.instructions_box,bg=full_background)
        self.instructions_frame.grid()

        # Heading Label 
        self.heading_label = Label(self.instructions_frame, text="Instructions",
                                    font="Arial 24 bold", padx=10, pady=10,bg=full_background)
        self.heading_label.grid(row=0)

        # Main Instructions Label 
        instructions_text = "After pressing play the difficulty selector will open, chose a difficulty and you will get the corresponding amount of lives. "\
                            "The harder the difficulty you chose the less lives you will have but you will have a higher score multiplier. \n\n"\
                            "After selecting the difficulty you will see a new window with the question on the left, with how many lives you have remaining at the top "\
                            "and you can chose an answer for the question by clicking one of the button to the right. \n\n"\
                            "Once you answer, the button will either turn red for wrong and the correct answer will be in orange, or the clicked button will go green for correct. "\
                            "A continue button will show up after answering to take you to the next question if you have lives remaining or will send you to the summary screen \n"
        self.instructions_label = Label(self.instructions_frame, text=instructions_text,
                                    font="Arial 12", padx=10, pady=10,bg=full_background,wrap=400)
        self.instructions_label.grid(row=1)

    # custom close functionality to re enable the instructions button
    def close_instructions(self,partner):
        partner.help_button.config(state=NORMAL)
        self.instructions_box.destroy()

class Game:
    def __init__(self,partner,difficulty,lives):
        
        # Colour Pallete
        full_background = "#A88770"
        button_background = "#F1DCA7"

        # Setup List for exporting
        self.game_history = []

        # Setup stats for the game
        self.correct = 0
        self.lives = lives
        self.difficulty = difficulty
        self.round = 0

        # Holds which button is the correct answer
        self.correct_answer_index = 0

        # Create New Window
        self.Game_box = Toplevel()
        self.Game_box.geometry("600x350")
        # Assign custom function to the closing of the window so that on close it goes to summany page instead of fully closing
        self.Game_box.protocol('WM_DELETE_WINDOW', partial(self.to_summary))

        # Initialize Frame to fill the entire window with the backgorund
        self.Game_box.columnconfigure(index=0,weight=1)
        self.Game_box.rowconfigure(index=0,weight=1)
        self.Game_frame = Frame(self.Game_box,bg=full_background)
        self.Game_frame.grid(sticky=NSEW)

        
        # Game Round Heading Label that shows the question you are on and lives remaining
        self.question_heading_label = Label(self.Game_frame, text="Question {} | Lives: {}".format(self.round + 1,self.lives), font="Arial 24 bold", padx=10, pady=10,bg=full_background)
        self.question_heading_label.grid(row=0,sticky=NW)

        # The Actual question label that display the randomly selected question
        self.question_label = Label(self.Game_frame, text="This is where the question goes", font="Arial 12", padx=10,wrap=300,justify=LEFT,bg=full_background)
        self.question_label.grid(row=0,rowspan=3,column=0,sticky=NW,pady=50)

        # Creates a frame for the anser buttons so they can line up vertically 
        self.Game_frame.columnconfigure(index=1,weight=1)
        self.answer_buttons_frame = Frame(self.Game_frame,bg=full_background)
        self.answer_buttons_frame.grid(row=0,column=1,sticky=E,rowspan=4)

        # Sets up the four answer buttons, they all have a different index assigned to them as a unique identifier which also corresponds to their index in the 
        # answer buttons list, when a user presses a button it passes the index of the chosen button along to the 
        # answer question function to check if the selected button was correct
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
        
        # continue button that goes to next question, only appears when the user has answered a question
        self.Game_frame.rowconfigure(index=2,weight=1)
        self.continue_button = Button(self.Game_frame, text="Continue",font = "arial 15 bold",width=15,height=1,bg=button_background, command=self.next_question)
        self.continue_button.grid(row=2,sticky=S,pady=10)

        # Opens instructions window
        self.help_button = Button(self.Game_frame, text="Instructions",font = "arial 12 bold",width=10,height=1,bg=button_background, command=self.to_instructions)
        self.help_button.grid(row=3,pady=10)

        # Set up question and wrong answer lists
        # Open csv file and get all data from it. 
        file = open("03_EgyptianGods\Egyptian_gods.csv",newline="")
        reader = csv.reader(file)
        self.question_list = list(reader)
        file.close()

        # Get all gods from the above csv file for the random worng answers
        self.gods_list  = []
        for row in self.question_list:
            self.gods_list.append(row[0])
        
        # Run throught the question creation on first window init
        self.next_question()
    # open instructions window
    def to_instructions(self):
        Instructions(self)
    
    def next_question(self):

        # exit to summary if completely out of lives
        if self.lives <= 0:
            self.to_summary()
            return
        
        # Store this rounds data to store for the game summary
        round_data = []
        # Set qeustion heading label, add to round counter
        self.question_heading_label.config(text="Question {} | Lives: {}".format(self.round + 1,self.lives))
        round_data.append(self.round)
        round_data.append(self.lives)
        # get random question from question list
        current_question =  random.choice(self.question_list)
        # Remove question from question list so that it does not repeat
        self.question_list.remove(current_question)

        # display question
        question_text = "What is the name of {}".format(current_question[1])
        self.question_label.config(text=question_text)
        # Append question to round data
        round_data.append(question_text)

        # Get correct answer
        correct_answer = current_question[0]
        print(correct_answer)
        # Append correct answer to round data
        round_data.append(correct_answer)

        # Generate 3 random answers, do not use randomly generated answer if it has already been chosen or if it is the correct answer
        # stop once 3 valid incorrect answers are generated
        random_answers = []
        while len(random_answers) < 3:
            random_answer = self.gods_list[random.randrange(0,len(self.gods_list) - 1)]
            if random_answers.count(random_answer) >= 1:
                continue
            
            if random_answer == correct_answer:
                continue

            random_answers.append(random_answer)

        # setup a list that will hold all the random answers and which button it is assigned to
        answers_summary_list = []
        
        # List of buttons indexes, so that i can chose and remove button indexes already used
        buttons_indexes  = [0,1,2,3]
        # Assign the correct answer to a button
        chosen_button_index = random.choice(buttons_indexes)
        self.answer_buttons[chosen_button_index].config(text=correct_answer,bg = "#F1DCA7",state=NORMAL)
        # Store that this button index is the correct answer to compare with when the user answers 
        self.correct_answer_index = chosen_button_index
        #Store Corerct answer in answer summary list
        answers_summary_list.append([self.correct_answer_index,correct_answer])
        buttons_indexes.remove(chosen_button_index)
        # now assign the randomly chosen wrong asnwers from before to the remaining buttons
        for x in range(0,3):
            chosen_button_index = random.choice(buttons_indexes)
            chosen_random_answer = random.choice(random_answers)
            
            self.answer_buttons[chosen_button_index].config(text=chosen_random_answer,bg="#F1DCA7",state=NORMAL)

            # Append what button has what answer to the answer summary list
            answers_summary_list.append([chosen_button_index,chosen_random_answer])

            buttons_indexes.remove(chosen_button_index)
            random_answers.remove(chosen_random_answer)
        
        # Append button/answer data to the overall round summary list
        round_data.append(answers_summary_list)

        # Remove continue button
        self.continue_button.grid_remove()
        
        # Append All of this round info to the overall game history
        self.game_history.append(round_data)
       
        
    def answer_question(self,answer_index):

        # after question is answered append to round
        # appending here and rather than when question is generated means that it does not count as a wrong answer in the summary data
        self.round += 1

        # Check if chosen asnwer is correct by comparing the button index to the correct answer index,
        # Change button to green if correct answer, if not chosen correct answer then change colour of correct answer to Orange and chosen answer to red
        if answer_index == self.correct_answer_index:
            self.answer_buttons[answer_index].config(bg="#9bdd98")
            self.correct += 1
        else:
            self.answer_buttons[answer_index].config(bg="#e78a85")
            self.answer_buttons[self.correct_answer_index].config(bg="#ce9745")
            self.lives -= 1
        
        # Add the correct answer to the end index to the end of the list of the last round
        self.game_history[len(self.game_history) - 1].append(answer_index)
        
        # Disable all the buttons so that user cannot input more than one answer.
        for item in range(0,4):
            self.answer_buttons[item].config(state=DISABLED)

        # Update Heading Label
        self.question_heading_label.config(text="Question {} | Lives: {}".format(self.round,self.lives))
        # Make the continue button reappear
        self.continue_button.grid()

    # Opens summary window while passing along, full game history and some summary stats(rounds, correct incorrect and difficulty)
    def to_summary(self):
        Summary(self,self.game_history,self.correct,self.round - self.correct,self.difficulty)
        self.Game_box.destroy()

class Summary():
    def __init__(self,partner,game_history,correct,incorrect,difficulty):
        full_background = "#A88770"
        button_background = "#F1DCA7"

        # Setup Summary Window
        self.summary_box = Toplevel()
        # Custom Close function that completely stops program
        self.summary_box.protocol('WM_DELETE_WINDOW', partial(self.close_summary))

        # Frame Setup
        self.summary_frame = Frame(self.summary_box,bg = full_background)
        self.summary_frame.grid()
        # Heading Label
        self.heading_label = Label(self.summary_frame, text="Game Over",
                                    font="Arial 24 bold", padx=10, pady=10,bg = full_background)
        self.heading_label.grid(row=0)

        # How many questions answered label
        self.questions_answered_label = Label(self.summary_frame, text="Questions Answered :{}".format(correct + incorrect),
                                    font="Arial 12 bold", padx=10, pady=2,bg = full_background)
        self.questions_answered_label.grid(row=1)

        # how many correct answers
        self.correct_label = Label(self.summary_frame, text="Correct:{}".format(correct),
                                    font="Arial 12 bold", padx=10, pady=2,bg = full_background)
        self.correct_label.grid(row=2)

        # How many Incorrect answers label
        self.incorrect_label = Label(self.summary_frame, text="Incorrect:{}".format(incorrect),
                                    font="Arial 12 bold", padx=10, pady=2,bg = full_background)
        self.incorrect_label.grid(row=3)

        # Score Label(correct * difficulty)
        self.score_label = Label(self.summary_frame, text="Score:{}".format(correct * difficulty),
                                    font="Arial 12 bold", padx=10, pady=2,bg = full_background)
        self.score_label.grid(row=4)

        # Play Again button that opens difficulty window again
        self.play_again_button = Button(self.summary_frame, text="Play Again",font = "arial 16 bold",width=10,height=1, command=self.to_difficulty,
                                        bg = button_background)
        self.play_again_button.grid(row=5,pady=(10,5))

        # Export button that opens the Export window
        self.export_button = Button(self.summary_frame, text="Export to file",font = "arial 12 bold",height=1, command=lambda : self.to_export(game_history,correct,incorrect,difficulty),bg = button_background)
        self.export_button.grid(row=6,pady=5)
        
        # Quit button that quits game fully
        self.quit_button = Button(self.summary_frame, text="Quit",font = "arial 12 bold",height=1, command=self.close_summary, bg = button_background)
        self.quit_button.grid(row=7,pady=5)

    # Quits application fully
    def close_summary(self):
        root.destroy()
    # Open Difficuulty window
    def to_difficulty(self):
        Difficulty(self)
        self.summary_box.destroy()
    
    # Opens Export with summary stats and full game history passed through
    def to_export(self,game_history,correct,incorrect,difficulty):
        Export(self,game_history,correct,incorrect,difficulty)

class Export():
    def __init__(self,partner,game_history,correct,incorrect,difficulty):
        # Disable export button on Summary window so that multiple export windows do not open
        partner.export_button.config(state=DISABLED)
        background = "#A88770"
        button_background = "#F1DCA7"

        # Window setup
        self.export_box = Toplevel()

        # Custom close function assigned to the x so that it re enables the export buton in Summary window
        self.export_box.protocol('WM_DELETE_WINDOW', partial(self.close_export, partner))
        
        self.export_frame = Frame(self.export_box, bg=background)
        self.export_frame.grid()

        # Heading
        self.export_heading = Label(self.export_frame, text="export / instructions",
                                    font="arial 10 bold", bg=background)
        self.export_heading.grid(row=0)
        # Text
        self.export_text = Label(self.export_frame, text="Enter a filename below "
                                                         "and press save to save your history "
                                                         "to a text file",
                                 justify=LEFT, width=40, bg=background, wrap=250)
        self.export_text.grid(row=1)

        self.filename_entry = Entry(self.export_frame, width=20,
                                    font="Arial 14 bold", justify=CENTER)
        self.filename_entry.grid(row=3, pady=10)

        self.save_error_label = Label(self.export_frame, text="", fg="maroon",
                                      bg=background)
        self.save_error_label.grid(row=4)

        self.save_cancel_frame = Frame(self.export_frame)
        self.save_cancel_frame.grid(row=5, pady=10)

        self.save_button = Button(self.save_cancel_frame, text="Save",
                                  width=10, bg=button_background, font="arial 10 bold",
                                  command=partial(lambda: self.save_history(partner,game_history,correct,incorrect,difficulty)))
        self.save_button.grid(row=0, column=0)

        # Cancel Button
        self.cancel_button = Button(self.save_cancel_frame, text="Cancel",
                                    width=10, bg=button_background, font="arial 10 bold",
                                    command=partial(self.close_export, partner))
        self.cancel_button.grid(row=0, column=1)

    def close_export(self, partner):
        partner.export_button.config(state=NORMAL)
        self.export_box.destroy()

    def save_history(self, partner, game_history,correct,incorrect,difficulty):
        print(game_history)
        has_error = "no"
        filename = self.filename_entry.get()

        valid_char = "[A-za-z0-9_]"
        for letter in filename:
            if re.match(valid_char, letter):
                continue
            
            elif letter == " ":
                problem = "no spaces allowed"
            else:
                problem = "no {}'s allowed".format(letter)
            has_error = "yes"
            break
        
        if filename == "":
            problem = "can't be blank"
            has_error = "yes"

        if has_error == "yes":
            self.save_error_label.config(text="Invalid filename - {}".format(problem))
            self.filename_entry.config(bg="#ffafaf")
        else:
            filename = filename + ".html"
            difficulty_name = ""
            if difficulty == 1:
                difficulty_name = "Easy"
            elif difficulty == 2:
                difficulty_name = "Medium"
            elif difficulty == 3:
                difficulty_name = "Hard"

            f = open(filename, "w+",encoding="utf-8")
            f.write(
            '<!doctype html>\n'
            '<html>\n'
            '<head>\n'
            '<title>Egyptian Gods Quiz Summary</title>\n'
            '<meta name="description" content="Our first page">\n'
            '<meta name="keywords" content="html tutorial template">\n'
            '</head>\n'
            '<body style="background-color: #A88770;">\n'
            '    <h1>Egyptian Gods Quiz Summary</h1>\n'
            '    <span>\n'
            '    <div >\n'
            '        <h2 >Game Statistics</h2>\n'
            '        <h3>Difficulty: {}({}x score multiplier)</h3>\n'
            '        <h3>Questions Answered: {}</h3>\n'
            '        <h3>Correct: {}</h3>\n'
            '        <h3>Incorrect: {}</h3>\n'
            '        <h3>Score: {}</h3>\n'
            '    </div>\n'
            '    </span>\n'
            '    <div>\n'
            '    <h2>Round Summaries</h2>\n'.format(difficulty_name,difficulty,correct+incorrect,correct,incorrect,correct * difficulty)
            )
            
            for item in range(0,correct+incorrect):
                round_data = game_history[item]
                f.write(
                '    <hr style="border-color: black;">\n'
                '    <h3> Question {} |Lives {}</h3>\n'
                '    <h3>{}</h3>\n'.format(round_data[0],round_data[1],round_data[2])
                )

                for item in round_data[4]:
                    background_colour = "#F1DCA7"
                    if round_data[5] == item[0] and round_data[3] == item[1]:
                        background_colour = "#9bdd98"
                    elif round_data[3] == item[1]:
                        background_colour = "#ce9745"
                    elif round_data[5] == item[0]:
                        background_colour = "#e78a85"

                    # Html for each answer
                    f.write('    <h3 style="display: inline-block;'
                            '                width: 200px;'
                            '                border: solid #020202;'
                            '                padding: 10px;'
                            '                margin: 20px;'
                            '                text-align: center;'
                            '                background-color: {};">{}</h3>\n'.format(background_colour, item[1]))
               
            # Finishing Html tags
            f.write(
            '    </div>  \n'

            '</body>\n'
            '</html>\n'

            )
           

            f.close()
            self.close_export(partner)

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Egyptian Gods")
    root.geometry("300x300")
    root.columnconfigure(index=0,weight=1)
    root.rowconfigure(index=0,weight=1)
    something = Start(root)
    root.mainloop()


