import csv
import random

# Open csv file and get all data from it. 
file = open("03_EgyptianGods\Egyptian_gods.csv",newline="")
reader = csv.reader(file)
question_list = list(reader)
file.close()

# Get all gods from the above csv file
gods_list  = []
for row in question_list:
    gods_list.append(row[0])

# random question
current_question =  random.choice(question_list)
print("length of question list before: {}".format(len(question_list)))
question_list.remove(current_question)

print("What is the name of {}".format(current_question[1]))

correct_answer = current_question[0]
random_answers = []
while len(random_answers) < 3:
    random_answer = gods_list[random.randrange(0,len(gods_list) - 1)]
    if random_answers.count(random_answer) >= 1:
        continue
    
    if random_answer == correct_answer:
        continue

    random_answers.append(random_answer)

print(correct_answer)
print(random_answers)
print("length of question list after: {}".format(len(question_list)))

    

