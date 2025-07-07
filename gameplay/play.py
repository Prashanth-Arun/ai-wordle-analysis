from .evaluate import wordle_evaluate, letter_partition, interpret_score
from argparse import ArgumentParser
from model import Chatbot, ClaudeChatbot, MistralChatbot, GPTChatbot, GroqChatbot
from util import SOLVER_PROMPT, cprint
from typing import Any, Mapping, TypeAlias
import json
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
) -> Mapping[str, str]:
    
    assert len(guess_history) > 0
    last_guess, last_eval = guess_history[-1]
    letter_partition(guess=last_guess, evaluation=last_eval, present=present, absent=absent, unused=unused)
    interpretation: str = interpret_score(guess=last_guess, evaluation=last_eval)
    feedback: Mapping[str, str] = {
        "feedback": last_eval,
        "interpretation": interpretation,
        "past guesses": guess_history,
        "unused letters": unused,
        "absent letters": absent,
        "present letters": present
    }
    return feedback


def format_output(
    guess_history: list[GuessResult],
    target: str
) -> Mapping[str, Any]:
    """Formats output as a dict so that it can be written to a JSON file"""
    assert len(guess_history) >= 1
    num_guesses = len(guess_history)
    guesses: list[str] = [guess for guess, _ in guess_history]
    evals: list[str] = [evaluation for _, evaluation in guess_history]
    solved = False
    if guesses[-1] == target:
        solved = True
    return {
        "guesses": guesses,
        "evaluations": evals,
        "num guesses": num_guesses,
        "solved": solved
    }


def execute(model: str, target: str, verbose: bool = True, guess_limit: int = 7) -> Mapping[str, Any]:
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
            feedback: Mapping[str, str] = construct_feedback(guess_history, present, absent, unused)
            solver_response, _ = solver.post_query(json.dumps(feedback))
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
        if (evaluation == "GGGGG") or (len(guess_history) >= guess_limit):
            break

    result = format_output(guess_history=guess_history, target=target)
    return result
