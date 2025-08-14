import json
import wordle_stat

def set_date_back_by_1(month, date):
    if date == "01":
        if month == "07":
            return ("06", "30")
        elif month == "06":
            return ("05", "31")
        elif month == "05":
            return ("04", "30")
        elif month == "04":
            return ("03", "31")
    else:
        date = int(date) - 1
        return (month, f'{date:02}')


json_file = 'past_wordle.json'

with open(json_file) as json_data:
    data = json.load(json_data)
    for word_entry in data:
        word = list(word_entry.keys())[0]
        month = word_entry[word]['month']
        date = word_entry[word]['date']
        number = word_entry[word]['wordle_id']
        group = word_entry[word]['category']
        month, date = set_date_back_by_1(month, date)
        print(word, month, date, number)
        print(wordle_stat.get_stat(month, date, number))

