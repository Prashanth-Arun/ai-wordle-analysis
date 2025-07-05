from argparse import ArgumentParser
from collections import Counter
import pandas as pd

# In-group words (consecutive double letters OR starts with E/I/O/U)
HYPOTHESIS_WORDS = [
    ("oddly", "Double 'd'"),
    ("eerie", "Starts with 'E'"),
    ("upper", "Double 'p' + starts with 'U'"),
    ("issue", "Double 's' + starts with 'I'"),
    ("oozed", "Starts with 'O' + double 'o'"),
    ("egged", "Double 'g'"),
    ("offer", "Double 'f' + starts with 'O'"),
    ("iller", "Double 'l' + starts with 'I'"),
    ("orbit", "Starts with 'O'"),
    ("onion", "Starts with 'O'"),
    ("elite", "Starts with 'E'"),
    ("utter", "Double 't' + starts with 'U'"),
    ("added", "Double 'd'"),
    ("emote", "Starts with 'E'"),
    ("error", "Double 'r'"),
    ("oppen", "Double 'p' + starts with 'O'"),
    ("edger", "Starts with 'E'"),
    ("inner", "Double 'n' + starts with 'I'"),
    ("oomph", "Double 'o' + starts with 'O'"),
    ("eject", "Starts with 'E'"),
    ("input", "Starts with 'I'"),
    ("occur", "Double 'c' + starts with 'O'"),
    ("ozone", "Starts with 'O'"),
    ("udder", "Double 'd' + starts with 'U'"),
    ("usher", "Starts with 'U'")
]

# Control words (no double letters, don't start with E/I/O/U)
CONTROL_WORDS = [
    ("crank", "No double, starts with 'C'"),
    ("table", "No double, starts with 'T'"),
    ("smash", "No double, starts with 'S'"),
    ("bland", "No double, starts with 'B'"),
    ("chest", "No double, starts with 'C'"),
    ("grain", "No double, starts with 'G'"),
    ("plant", "No double, starts with 'P'"),
    ("shark", "No double, starts with 'S'"),
    ("brave", "No double, starts with 'B'"),
    ("cloak", "No double, starts with 'C'"),
    ("doubt", "No double, starts with 'D'"),
    ("fling", "No double, starts with 'F'"),
    ("mound", "No double, starts with 'M'"),
    ("spark", "No double, starts with 'S'"),
    ("trail", "No double, starts with 'T'"),
    ("draft", "No double, starts with 'D'"),
    ("climb", "No double, starts with 'C'"),
    ("spore", "No double, starts with 'S'"),
    ("prank", "No double, starts with 'P'"),
    ("brick", "No double, starts with 'B'"),
    ("groan", "No double, starts with 'G'"),
    ("shunt", "No double, starts with 'S'"),
    ("flint", "No double, starts with 'F'"),
    ("broad", "No double, starts with 'B'"),
    ("glean", "No double, starts with 'G'")
]


if __name__ == "__main__":

    # Create DataFrame
    data = pd.DataFrame(
        HYPOTHESIS_WORDS + CONTROL_WORDS,
        columns=["word", "group_reason"]
    )
    data["group"] = ["hypothesis"] * len(HYPOTHESIS_WORDS) + ["control"] * len(CONTROL_WORDS)

    # Add metadata
    data["starts_with"] = data["word"].str[0]
    data["letter_counts"] = data["word"].apply(lambda w: dict(Counter(w)))
    data["unique_letters"] = data["word"].apply(lambda w: len(set(w)))
    data["has_double_letter"] = data["word"].apply(
        lambda w: any(w[i] == w[i+1] for i in range(len(w)-1))
    )

    # Reorder columns
    data = data[["word", "group", "group_reason", "starts_with", "has_double_letter", "unique_letters", "letter_counts"]]

    # Save to CSV
    data.to_csv("./words/words_with_metadata.csv", index=False)

    # Save only words to a .txt file
    hypothesis_words: list[str] = [entry[0] + "\n" for entry in HYPOTHESIS_WORDS]
    control_words: list[str] = [entry[0] + "\n" for entry in CONTROL_WORDS]
    with open("./words/hypothesis_words.txt", "w") as f:
        f.writelines(hypothesis_words)
    with open("./words/control_words.txt", "w") as f:
        f.writelines(control_words)
