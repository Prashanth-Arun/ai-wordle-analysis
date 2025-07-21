import csv

def double_letter(word):
    for i in word:
        if word.count(i) > 1:
            return True
    return False

list_control = []
list_hypothesis = []
with open('past_wordle.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['month', 'date', 'wordle_number', 'word'])
    for row in reader:
        if double_letter(row['word'].strip()):
            list_hypothesis.append(row['month'].strip() + "," + row['date'].strip() + "," + row['wordle_number'].strip() + "," + row['word'].strip())
        else:
            list_control.append(row['month'].strip() + "," + row['date'].strip() + "," + row['wordle_number'].strip() + "," + row['word'].strip())

with open("list_control.csv", "w") as f:
    for entry in list_control:
        f.write(entry + "\n")

with open("list_hypothesis.csv", "w") as f:
    for entry in list_hypothesis:
        f.write(entry + "\n")
