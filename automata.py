import random


def create_automata(option: int) -> dict:
    dfa = {}
    if option == 1:
        dfa["states"] = ["q0", "q1", "q2", "q3"]
        dfa["alphabet"] = ['a', 'b']
        dfa["finals"] = [3]
        transitions = [
            [-1, 1],
            [2, -1],
            [3, -1],
            [3, -1]
        ]
        dfa["transitions"] = transitions
    elif option == 2:
        dfa["states"] = ["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8"]
        dfa["alphabet"] = ['a', 'b']
        dfa["finals"] = [4, 8]
        transitions = [
            [1, 5],
            [-1, 2],
            [-1, 3],
            [4, -1],
            [1, -1],
            [6, -1],
            [7, -1],
            [-1, 8],
            [-1, 5]
        ]
        dfa["transitions"] = transitions
    elif option == 3:
        dfa["alphabet"] = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                           "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
                           "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        dfa["states"] = ["q0", "q1", "q2"]
        dfa["finals"] = [1, 2]
        transitions = [[1 for i in range(20)] + [2 for i in range(20, len(dfa["alphabet"]))]]
        transitions.append([-1 for i in range(len(dfa["alphabet"]))])
        transitions.append([-1] + [1 for i in range(1, 11)] + [-1 for i in range(11, len(dfa["alphabet"]))])
        dfa["transitions"] = transitions
    return dfa


def generate_language(automata: dict):
    current_state = 0
    generated = []
    while True:
        if current_state in automata["finals"]:
            if all(s == -1 for s in automata["transitions"][current_state]) or random.random() < 0.5:
                break
        next_state, selected = random.choice([(s, i) for i, s in enumerate(automata["transitions"][current_state]) if s != -1])
        generated.append(automata["alphabet"][selected])
        current_state = next_state

    if len(automata["alphabet"][0]) > 1:
        return " ".join(generated)
    else:
        return "".join(generated)


def recognize_language(automata: dict, utterance: str) -> int:
    input: list
    input = list(utterance) if len(automata["alphabet"][0]) == 1 else utterance.split()

    current_state = 0
    for c in input:
        if c not in automata["alphabet"]:
            return 0
        index = automata["alphabet"].index(c)
        if automata["transitions"][current_state][index] == -1:
            return 0
        else:
            current_state = automata["transitions"][current_state][index]

    if current_state in automata["finals"]:
        return 1
    return 0