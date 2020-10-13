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
S -> NPVP | NPVP PNAN CNVP | NPVP DAN | NPVP PN | NPVP NPNP VPRNP | NPVP VPNP | NPVP PNVP NP
VPRNP -> VPR NP
NPNP -> NP NP
PNVP -> PN VP
VPNP -> VP NP
NPPN -> NP PN
NPVP -> NP VP | NPVP NP
PNAN -> PN AN
CNVP -> CN VP
VPR -> V P
VP -> V | V NP | V Adv | Conj V
NP -> N | Det N | N Adv | Conj N | Det N Adv | NP NP | P N  | Det Adj N | P Det Adj N | NP NP | P Det N | Det Adj Adj Adj N | Adj N
CN -> Conj N

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
    word_list = []
    tokenized_sentence = nltk.tokenize.word_tokenize(sentence)

    # exclude words that dont include atleast one alphabetical character
    for word in tokenized_sentence:
        if word.lower().islower():
            word_list.append(word.lower())
    
    print(word_list)
    return word_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks_list = []
    for subtree in tree.subtrees(lambda tree: tree.label() == "NP"):
        if len(list(subtree.subtrees(lambda tree: tree.label() == "NP"))) == 1:
            np_chunks_list.append(subtree)
        else:
            chunks = np_chunk(subtree)
            np_chunks_list.append(chunks)

    

    return np_chunks_list

def filt(tree):
    return tree.label() == "NP"


if __name__ == "__main__":
    main()
