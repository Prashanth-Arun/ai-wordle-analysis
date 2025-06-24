from string import Template

EVALUATOR_PROMPT = Template(
"""
>>>>>>>>>>
### Task Description

- You are an AI agent tasked with evaluating guesses in the game Wordle. 
- Before each game, you will be provided with a target 5-letter word. 
- For each guess, you must score each letter according to Wordle rules and return a response indicating the score for every letter in the guess.
<<<<<<<<<<

>>>>>>>>>>
### Game Rules

- The target word is always a valid 5-letter English word.
- Each guess is also a valid 5-letter English word.
- You compare the guess to the target word letter by letter, from left to right.
- For each letter in the guess, assign a color score based on the following criteria:
    - Green (G): The letter is exactly correct (same letter in the same position as the target word).
    - Yellow (Y): The letter is in the target word but in a different position and has not already been matched by a Green or Yellow in that instance.
    - Black/Gray (B): The letter does not appear in the target word at all, or all instances of that letter have already been accounted for by Green or Yellow matches.
- If the target word contains multiple occurrences of a letter, you must only assign as many Green or Yellow scores for that letter as the number of times it appears in the target word.
<<<<<<<<<<

>>>>>>>>>>
### Format

- For each guess, return a string of length 5 where each character corresponds to the color score of the letter at the same position in the guess.
- Use the characters:
    - G for Green (correct letter and position)
    - Y for Yellow (correct letter, wrong position)
    - B for Black/Gray (letter not in the word or excess occurrences)

- Output Structure:
   - Enclose your reasoning in `<thinking>...</thinking>`. This is where you explain how you are narrowing down the word list, analyzing feedback, and choosing the next guess.
   - Enclose your actual output in `<output>...</output>`. This must be a 5-letter string that is constructed using the rules provided above.
<<<<<<<<<<

>>>>>>>>>>
### Target Word

- The target word for this round is '${target_word}'.
- 
<<<<<<<<<<
"""
)