from argparse import ArgumentParser
from gameplay.evaluate import wordle_evaluate
from typing import Mapping, TypedDict
import json
import os

class WordleGame(TypedDict):
    guesses: list[str]
    evaluations: list[str]
    num_guesses: int
    solved: bool


class ExperimentResult(TypedDict):
    win_rate: float
    guess_results: list[WordleGame]


class GameAnalysis(TypedDict):
    pass


def calculate_entropy(
    guess: str,
    word_list: list[str]
) -> float:
    """Calculates the entropy of the guess given the list of possible words"""
    guess_categories: Mapping[str, int] = []

    for word in word_list: continue


def analyze_game(
    game: WordleGame,
    target: str,
    word_list: list[str]
) -> GameAnalysis:
    pass
        

def main():

    parser = ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--hypothesis", action="store_true")
    args = parser.parse_args()

    # Initialize the two base paths
    BASE_DATA_PATH = os.path.join(os.getcwd(), "data")
    BASE_ANALYSIS_PATH = os.path.join(os.getcwd(), "analysis")

    word_set: str = "hypothesis" if args.hypothesis else "control"

    # Read in the list of valid words
    with open(os.path.join(BASE_ANALYSIS_PATH, ".data", "word_list.txt"), "r") as f:
        word_list: list[str] = f.readlines()
        
    word_list = [word.strip() for word in word_list]

    # Read in the list of target words
    with open(os.path.join(BASE_DATA_PATH, "words", f"{word_set}_words.txt"), "r") as f:
        target_words: list[str] = f.readlines()

    target_words = [word.upper().strip() for word in target_words]

    # Read the results for the model and test set
    with open(os.path.join(BASE_DATA_PATH, "predictions", f"{args.model}_{word_set}.json"), "r") as f:
        exp_results: ExperimentResult = json.load(f)
    
    guess_results: list[WordleGame] = exp_results['guess_results']

    # Run analysis on each game
    assert len(guess_results) == len(target_words)
    game_analyses: list[GameAnalysis] = []
    for game, target in zip(guess_results, target_words):
        analysis: GameAnalysis = analyze_game(game, target, word_list.copy())
        game_analyses.append(analysis)