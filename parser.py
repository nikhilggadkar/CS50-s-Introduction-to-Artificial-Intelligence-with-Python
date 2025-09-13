import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> N V
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = nltk.word_tokenize(sentence)

    # Keep only words that contain at least one alphabet character
    # and lowercase them
    clean_words = []
    for word in words:
        if any(char.isalpha() for char in word):
            clean_words.append(word.lower())
    return clean_words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    # Initialize an empty list to store noun phrase chunks
    np_chunks = []

    # Safety check: tree must be a Tree object and not None
    if tree is None or not isinstance(tree, nltk.Tree):
        return np_chunks
    # Loop through all subtrees in the parse tree
    for subtree in tree.subtrees():
        # Check if the subtree is a noun phrase (NP)
        if subtree.label() == "NP":
            # Initialize a flag to check for nested NP inside this NP
            has_inner_np = False
            # Loop through the immediate children of this NP subtree
            for child in subtree:
                # If any child is a subtree and also labeled NP, mark as nested NP
                if isinstance(child, nltk.Tree) and child.label() == "NP":
                    has_inner_np = True
                    break
            if not has_inner_np:
                np_chunks.append(subtree)

    return np_chunks


if __name__ == "__main__":
    main()
