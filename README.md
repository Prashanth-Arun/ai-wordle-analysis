## Hypothesis

I tested the hypothesis that "AI would generally perform worse on words with $\geq 2$ occurrences of 1 or more letters in a word".

The hypothesis and control sets were constructed based on this hypothesis and can be found in `data/words`.

## Analysis

We analyzed each guess on the following metrics:

1. **Entropy**: Let $G$ be our guess, and let $L$ be our word list. We calculate entropy as follows:
    - $p_i = \frac {\text{count of pattern } i} {\text{total possible targets}}$
    - $H = - \sum_{i} p_i \log_2 p_i$

    Here, "pattern $i$" refers to a 5-letter string (e.g., "GYGBB") that represents the colors associated with each letter in a guess.

2. **Effectiveness**: This is a lighter version of entropy, where we calculate the percentage of words in our list $L$ that a guess $G$ eliminates.
    - We say that a guess $G$ eliminates a word $w$ from our list if $\text{strcmp}(E(G), E(w)) \neq 0$, where $E$ is an evaluation function.