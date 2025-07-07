
def wordle_evaluate(target: str, guess: str) -> str:
    assert len(target) == len(guess)
    target_letters: list[str] = list(target)
    guess_letters: list[str] = list(guess)

    match_result = ['' for i in range(len(target_letters))]

    # Match greens first
    for i, (tgt_letter, guess_letter) in enumerate(zip(target_letters, guess_letters)):
        if tgt_letter == guess_letter:
            match_result[i] = "G"
    
    # Remove matched letters from target and guess letter lists
    for i, match_res in enumerate(match_result):
        if match_res == "G":
            target_letters[i] = ''
            guess_letters[i] = ''

    # Match yellows next
    for i, guess_letter in enumerate(guess_letters):
        if guess_letter == '':
            continue
        try:
            tgt_idx = target_letters.index(guess_letter)
        except:
            continue
        match_result[i] = 'Y'
        guess_letters[i] = ''
        target_letters[tgt_idx] = ''

    # Fill in B (Black/Gray) for anything else
    for i in range(len(match_result)):
        if match_result[i] == '':
            match_result[i] = 'B'

    return ''.join(match_result)


def letter_partition(
    guess: str,
    evaluation: str,
    present: list[str],
    absent: list[str],
    unused: list[str]
) -> None:
    
    assert len(guess) == len(evaluation), f"ERROR: len({guess}) = {len(guess)} != len({evaluation})"
    for letter_char, eval_char in zip(guess, evaluation):
        if letter_char in unused:
            if eval_char == "B":
                absent.append(letter_char)
            else:
                present.append(letter_char)
            unused.remove(letter_char)

    absent.sort()
    present.sort()
    unused.sort()


def interpret_score(guess: str, evaluation: str) -> str:
    """
    Returns a text interpretation of the score that a Wordle player receives.

    Example (for guess="TARTS" and evaluation="GGBYB"):
        'T' -> In the correct position (1)
        'A' -> In the correct position (2)
        'R' -> Not in the word
        'T' -> In the word but not in position (4)
        'S' -> Not in the word

    Reason: Input tokens are cheaper than output tokens; cheaper to do this instead of having the LLM reason through it.
    """
    assert len(guess) == len(evaluation) == 5
    interpretation: list[str] = []
    for i, (guess_char, eval_char) in enumerate(zip(guess, evaluation)):
        match eval_char:
            case "B":
                interpretation.append(f"'{guess_char}' -> Not in the word")
            case "G":
                interpretation.append(f"'{guess_char}' -> In the correct position ({i+1})")
            case "Y":
                interpretation.append(f"'{guess_char}' -> In the word but not in position ({i+1})")
            case _:
                raise ValueError(f"ERROR: Invalid evaluation character '{eval_char}' @ idx {i} (evaluation='{evaluation}', guess={guess})")
            
    return "; ".join(interpretation)