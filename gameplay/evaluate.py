
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