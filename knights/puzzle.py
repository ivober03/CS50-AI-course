from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(

    Or(AKnight, AKnave), # A is a Knight or a Knave

    Implication(AKnight, And(AKnight, AKnave)), # If A is a Knight then it's saying the truth
    Implication(AKnave, Not(And(AKnight, AKnave))) # If A is a Knave then it's lying

)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(

    Or(AKnight, AKnave), # A is a Knight or a Knave
    Or(BKnight, BKnave), # B is a Knight or a Knave

    Implication(AKnight, And(AKnave, BKnave)), # If A is a knight then both of them are knights
    Implication(AKnave, Not(And(AKnave, BKnave))) # If A is a knave then he's lying, so they can't be both knaves

)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave), # A is a Knight or a Knave
    Or(BKnight, BKnave), # B is a Knight or a Knave

    Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))), # If A is a knight then both of them can be Knights or Knaves
    Implication(AKnave, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))), # If A is a knave then he'S lying, so they can´t be both of the same kind
    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))), # If B is a knight then one of them is the knight and the other the knave
    Implication(BKnave,  Not(Or(And(AKnave, BKnight), And(AKnight, BKnave)))) # If B is a knave then they are of the same kind

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),  # A is a Knight or a Knave
    Or(BKnight, BKnave),  # B is a Knight or a Knave
    Or(CKnight, CKnave),  # C is a Knight or a Knave

    Implication(AKnight, Or(AKnight, AKnave)),  # if A is a knight then he can be either a knight or a knave
    Implication(AKnave, Not(Or(AKnight, AKnave))),  # if A is a knave then he can't be a knight or a knave
    Implication(BKnight, And(AKnave, CKnave)),  # if B is a knight then A and C are knaves
    Implication(BKnave, Not(And(AKnave, CKnave))),  # if B is a knave then A and C aren't knaves
    Implication(CKnight, AKnight),  # if C is a knight then A is a knight
    Implication(CKnave, Not(AKnight))  # if C is a knave then A is not a knight

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
