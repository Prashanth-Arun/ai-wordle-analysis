from argparse import ArgumentParser
from gameplay import execute
from model import Chatbot
from prompt import SOLVER_PROMPT
import os

def serialize_outfile_name(model: str, dataset: str) -> str:
    return f"{model}_{dataset}.txt"

def main():

    parser = ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--hypothesis", type=str, required=True)
    parser.add_argument("--verbose", action="store_true")
    
    args = parser.parse_args()

    # Load dataset
    with open(f"{'control' if not args.hypothesis else 'hypothesis'}_words.txt", "r") as f:
        word_list: list[str] = f.readlines()

    # Run the experiment
    trajectories: list[str] = []
    for word in word_list:
        word = word.strip()
        guesses = execute(model=args.model, target=word, verbose=args.verbose)
        trajectories.append(" -> ".join(guesses))

    # Write trajectories to file
    with open(
        f"./predictions/{serialize_outfile_name(model=args.model, dataset='control' if not args.hypothesis else 'hypothesis')}", "w"
    ) as f:
        f.writelines([trajectory + "\n" for trajectory in trajectories])
