from argparse import ArgumentParser
from typing import TypeVar, Mapping
import json
import os

WordleOutcome = TypeVar("WordleOutcome")

def register_start_word(current_count: Mapping[str, int], guesses: list[str]) -> None:
    assert len(guesses) > 0
    first_guess = guesses[0]
    if first_guess in current_count:
        current_count[first_guess] += 1
    else:
        current_count[first_guess] = 1

def main():

    parser = ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    args = parser.parse_args()

    BASE_PRED_PATH = os.path.join(os.getcwd(), "data", "predictions")
    BASE_RESULTS_PATH = os.path.join(os.getcwd(), "analysis", "results")

    outcomes: list[WordleOutcome] = []
    file_names = [
        os.path.join(BASE_PRED_PATH, f"{args.model}_{experiment}.json") 
        for experiment in ['control', 'hypothesis']
    ]

    for outfile in file_names:
        with open(outfile, "r") as f:
            results = json.load(f)
        assert "win_rate" in results
        assert "guess_results" in results
        outcomes += results["guess_results"]

    start_word_counts: Mapping[str, int] = {}
    for outcome in outcomes:
        assert "guesses" in outcome, f"Outcome: {outcome}"
        register_start_word(start_word_counts, outcome["guesses"])

    with open(os.path.join(BASE_RESULTS_PATH, f"{args.model}_start_counts.json"), "w") as f:
        json.dump(start_word_counts, f, indent=4)


if __name__ == "__main__":
    main()