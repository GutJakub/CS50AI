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

#NONTERMINALS = """
"""
S -> NP VP | NP VP NP | VP NP | S Conj S | S P S
NP -> N | P NP | AN N | Det AN N | NP P NP | Det N 
VP -> V | VP Adv | Adv VP | V NP
AN -> Adj | Adj AN
"""
NONTERMINALS = """
S -> NP VP | NP VP Conj NP VP | NP VP Conj VP
NP -> N | Det N | Det AP N | P NP | NP P NP | NP Adv
VP -> V | Adv VP | V Adv | VP NP | V NP Adv | VP P
AP -> Adj | AP Adj
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
    s=sentence.casefold()
    s=nltk.word_tokenize(s)
    s=[slowo for slowo in s if slowo.isalpha()]
    return s
    


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    
    lista=[]
    Parent_tree=nltk.ParentedTree.convert(tree)

    for chunk in Parent_tree.subtrees(lambda t: t.label()=="NP"):
        logic=True
        for child_chunk in chunk.subtrees():
            if child_chunk==chunk:
                continue
            if child_chunk.label()=="NP":
                logic=False
        if logic:
            lista.append(chunk)


    return lista



if __name__ == "__main__":
    main()
