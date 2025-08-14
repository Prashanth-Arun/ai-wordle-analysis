import json

results = []

json_file = "past_wordle.json"

with open("wordle_stat.txt", "r") as stat_file:
    word = ""
    difficulty = ""
    difficulty_level = ""
    for i, line in enumerate(stat_file.read().split("\n")):
        if i % 5 == 0 and line:
            word = line.split()[0]
            continue
        if i % 5 == 3:
            line = line.split()
            difficulty = line[line.index("guesses") - 1]
            difficulty_level = line[-2] + " " + line[-1]
            if difficulty_level[-1] == '.':
                difficulty_level = difficulty_level[:-1]
                results.append({word: {"difficulty": difficulty, "difficulty_level": difficulty_level}})

with open(json_file) as json_data:
    data = json.load(json_data)
    for i, word_entry in enumerate(data):
        word = list(word_entry.keys())[0]
        print(word == results[i].keys())
        print(word, results[i].keys())
