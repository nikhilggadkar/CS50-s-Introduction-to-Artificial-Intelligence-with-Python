from logic import *

# defining all symbols for Knight and Knave for A, B, and C
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
# But this is not possible. One person can't be both at the same time.

knowledge0 = And(
    # either A is knight or knave (but not both)
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # if A is a knight, then his statement must be true
    # but the statement says A is both knight and knave — which is not possible
    # so this statement is false → A can't be a knight → A must be a knave
    Implication(AKnight, And(AKnight, AKnave))
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.

knowledge1 = And(
    # basic rules: each person can be only knight or knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # if A is a knight, his statement is true
    # so both A and B are knaves — but this can't happen since A can't be both knight and knave
    Implication(AKnight, And(AKnave, BKnave)),

    # if A is a knave, then his statement is false
    # so at least one of them is not a knave
    Implication(AKnave, Not(And(AKnave, BKnave)))
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

knowledge2 = And(
    # basic rules again
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # if A is a knight, his statement is true → both are same type
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),

    # if A is a knave, then statement is false → they are different types
    Implication(AKnave, Or(And(AKnight, BKnave), And(AKnave, BKnight))),

    # if B is a knight, then his statement is true → they are different
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),

    # if B is a knave, then statement is false → they are same
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave)))
)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but we don’t know which.
# B says "A said 'I am a knave'." and also "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    Implication(BKnight, AKnave),
    Implication(AKnight, Not(AKnave)),
    Implication(BKnight, CKnave),
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight)),

    # If A is a knave and C says he is a knight, C is lying → C is a knave
    Implication(And(AKnave, CKnight), CKnave),

    # FINAL kicker: if C is NOT a knave → contradiction
    Implication(Not(CKnave), And(AKnight, Not(AKnight))),

    # ✅ This is the final step to make sure B is printed
    # If A is a knave and C is also a knave (both of B’s claims are true),
    # then B must be a knight for saying the truth
    Implication(And(AKnave, CKnave), BKnight)
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
