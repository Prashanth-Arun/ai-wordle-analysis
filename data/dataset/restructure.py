import csv
import json

def construct_item(month: str, date: str, id: str, word: str, dtype: str) -> dict:
    return {
        word : {
            "month": month,
            "date": date,
            "wordle_id": id,
            "category": dtype
        }
    }

if __name__ == "__main__":

    files_to_read: list[str] = ['list_control.csv', 'list_hypothesis.csv']
    dataset_types: list[str] = ['control', 'hypothesis']
    formatted_word_list: list[dict] = []

    for filename, dtype in zip(files_to_read, dataset_types):
        with open(filename, "r") as f:
            rows = csv.reader(f)
            for row in rows:
                formatted_word_list.append(construct_item(*row, dtype))

    with open("past_wordle.json", "w") as f:
        json.dump(formatted_word_list, f, indent=4)