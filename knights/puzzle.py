from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

genKnowledge=And(
    Not(And(AKnight, AKnave)),
    Or(AKnight, AKnave),        

    Not(And(BKnight, BKnave)),  
    Or(BKnight, BKnave),        

    Not(And(CKnight, CKnave)),  
    Or(CKnight, CKnave)
    )

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    genKnowledge,
    Implication(AKnight,And(AKnave,AKnight)),
    Implication(AKnave,Not(And(AKnave,AKnight)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    genKnowledge,
    Implication(AKnave,Not(And(BKnave,AKnave))),
    Implication(AKnight,And(AKnave,BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(And(AKnight,BKnight),
    And(AKnave,BKnight)),
    Or(And(BKnave,AKnave),
    And(BKnight,AKnave))

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."



knowledge3 = And(
    #1
    #Or(AKnight,AKnave),
    genKnowledge,
    Or(AKnave,AKnight),
    #2
    #Or(And(BKnave,AKnight),And(BKnight,AKnave),And(BKnave,AKnave)),
    Implication(BKnight, And(
        Implication(AKnight, AKnave),
        Implication(AKnave, Not(AKnave))
    )),

    Implication(BKnave, Not(And(
        Implication(AKnight, AKnave),
        Implication(AKnave, Not(AKnave))
    ))),
    #3
    Or(And(CKnave,BKnight),And(BKnave,CKnight)),
    #4
    Or(And(CKnight,AKnight),And(CKnave,AKnave))

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
