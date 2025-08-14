import json

list_of_json_data = ["claude_control.json", "gpt_control.json", "mistral_control.json", "claude_hypothesis.json", "gpt_hypothesis.json", "mistral_hypothesis.json"]

for file in list_of_json_data:
    with open("predictions/"+file, "r") as f:
        data = json.load(f)
        count = 0
        win = 0
        for guess in data['guess_results']:
            count += 1
            if guess['num_guesses'] < 7:
                win += 1
            else:
                guess['solved'] = False
        data['win_rate'] = float("{:.2f}".format(win/count))

        with open(file, "w") as fprime:
            json.dump(data, fprime)
# Manually copy the json into the predictions to fix the original problem
