from .evaluate import wordle_evaluate, letter_partition
from argparse import ArgumentParser
from model import Chatbot, ClaudeChatbot, MistralChatbot, GPTChatbot, GroqChatbot
from util import SOLVER_PROMPT, cprint
from typing import Mapping, TypeAlias
import re

MODEL_MAPPING : Mapping[str, Chatbot] = {
    "claude": ClaudeChatbot,
    "llama": GroqChatbot,
    "gpt": GPTChatbot,
    "mistral": MistralChatbot
}

GuessResult: TypeAlias = tuple[str, str]


def get_guess(response: str) -> str:
    guess = re.findall(f"<guess>(.*?)</guess>", response, re.DOTALL)
    if len(guess) == 0:
        raise ValueError(f"No guesses: {response}")
    elif len(guess) > 1:
        raise ValueError(f"Too many guesses: {guess}")
    return guess[0]


def valid_guess(guess: str) -> bool:
    """Return whether a guess is 5 letters long and all characters are in uppercase"""
    return (len(guess) == 5) and (guess.upper() == guess)


def initialize_model(model_name: str, system_prompt: str) -> Chatbot:
    """Initialize the model with the provided system prompt"""
    assert model_name in MODEL_MAPPING
    return MODEL_MAPPING[model_name](system_prompt=system_prompt)


def construct_feedback(
    guess_history: list[GuessResult], 
    present: list[str], 
    absent: list[str], 
    unused: list[str]
) -> str:
    
    assert len(guess_history) > 0
    last_guess, last_eval = guess_history[-1]
    letter_partition(guess=last_guess, evaluation=last_eval, present=present, absent=absent, unused=unused)
    feedback: list[str] = [
        f"Feedback: {last_eval}",
        f"Past Guesses: {guess_history}",
        f"Unused: {unused}",
        f"Absent: {absent}",
        f"Present: {present}"
    ]
    return "\n".join(feedback)


def execute(model: str, target: str, verbose: bool = True, guess_limit: int = 15) -> list[str]:
    solver = initialize_model(model, SOLVER_PROMPT)

    guess_history: list[GuessResult] = []
    present: list[str] = []
    absent: list[str] = []
    unused: list[str] = [chr(ord('A') + i) for i in range(26)]
    evaluation: str = ""

    while True:
        if len(guess_history) == 0:
            solver_response, _ = solver.post_query("Begin")
        else:
            feedback: str = construct_feedback(guess_history, present, absent, unused)
            solver_response, _ = solver.post_query(feedback)
            if verbose: cprint(feedback, color="yellow")
        print(solver_response)
        try:
            guess = get_guess(solver_response)
            if verbose: print("Guess: " + guess)
            if not valid_guess(guess): 
                evaluation = f"Invalid {len(guess)}-letter word: {guess}. Your guess must be 5 letters long, uppercase."
                continue
        except ValueError as e:
            print(e.__str__())
            continue
        evaluation = wordle_evaluate(target=target, guess=guess)
        if verbose: print("Result: " + evaluation)
        guess_history.append((guess, evaluation))
        if (evaluation == "GGGGG") or (len(guess_history) > guess_limit):
            break

    return [guess for guess, _ in guess_history]
