from .evaluate import wordle_evaluate
from argparse import ArgumentParser
from model import Chatbot, ClaudeChatbot, MistralChatbot, GPTChatbot, GroqChatbot
from prompt import SOLVER_PROMPT
from typing import Mapping
import re

MODEL_MAPPING : Mapping[str, Chatbot] = {
    "claude": ClaudeChatbot,
    "llama": GroqChatbot,
    "gpt": GPTChatbot,
    "mistral": MistralChatbot
}

def get_guess(response: str) -> str:
    guess = re.findall(f"<guess>(.*?)</guess>", response, re.DOTALL)
    if len(guess) == 0:
        raise ValueError(f"No guesses: {response}")
    elif len(guess) > 1:
        raise ValueError(f"Too many guesses: {guess}")
    return guess[0]


def initialize_model(model_name: str, system_prompt: str) -> Chatbot:
    """Initialize the model with the provided system prompt"""
    assert model_name in MODEL_MAPPING
    return MODEL_MAPPING[model_name](system_prompt=system_prompt)


def execute(model: str, target: str, verbose: bool = True, guess_limit: int = 15) -> list[str]:
    solver = initialize_model(model, SOLVER_PROMPT)

    guesses: list[str] = []
    evaluation: str = ""

    while True:
        if len(guesses) == 0:
            solver_response, _ = solver.post_query("Begin")
        else:
            solver_response, _ = solver.post_query(f"Feedback for last guess: {evaluation}")
        print(solver_response)
        try:
            guess = get_guess(solver_response, "guess")
            if verbose: print("Guess: " + guess)
        except ValueError as e:
            print(e.__str__())
            continue
        evaluation = wordle_evaluate(target=target, guess=guess)
        if verbose: print("Result: " + evaluation)
        guesses.append(guess)
        if (evaluation == "GGGGG") or (len(guesses) > guess_limit):
            break
