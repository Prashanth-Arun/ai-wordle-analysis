from argparse import ArgumentParser
from gameplay import execute
from typing import Mapping, Any
from util import cprint
import json
import os

BASE_DATASET_PATH: str = os.path.join(os.getcwd(), "data", "words")
BASE_PREDICTIONS_PATH: str = os.path.join(os.getcwd(), "data", "predictions")


def serialize_outfile_name(model: str, dataset: str) -> str:
    return f"{model}_{dataset}.json"


def count_wins(results: list[Mapping[str, Any]], guess_limit: int = 6) -> int:
    num_wins = 0
    for result in results:
        assert "num guesses" in result and "solved" in result
        num_wins += (1 if result['num_guesses'] <= guess_limit and result['solved'] else 0)
    return num_wins


def main():

    parser = ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--hypothesis", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    
    args = parser.parse_args()

    # Load dataset
    wordfile: str = f"{'control' if not args.hypothesis else 'hypothesis'}_words.txt"
    with open(os.path.join(BASE_DATASET_PATH, wordfile), "r") as f:
        word_list: list[str] = f.readlines()

    # Run the experiment
    results: list[Mapping[str, Any]] = []
    for word in word_list:
        word = word.strip()
        cprint(f"### Target = {word.upper()}", color="cyan")
        result = execute(model=args.model, target=word.upper(), verbose=args.verbose)
        results.append(result)

    # Count the number of wins and construct the final output
    win_rate: float = round(count_wins(results=results) / len(word_list), 3)
    output: Mapping[str, Any] = {
        "win rate": win_rate,
        "guess results": results
    }

    # Write trajectories to file
    outfile_name: str = serialize_outfile_name(model=args.model, dataset='control' if not args.hypothesis else 'hypothesis')
    with open(f"{BASE_PREDICTIONS_PATH}/{outfile_name}", "w") as f:
        json.dump(output, f, indent=4)


if __name__ == "__main__":
    main()
