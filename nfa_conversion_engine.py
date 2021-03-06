import argparse, pathlib
from nfa_parser_engine import reading

sigma = []
delta = {}
states = {}


def dfa_conversion(sigma, delta, states):
    new_delta = {}
    new_states = {}
    start_state = None
    for state in states:
        if states[state] == "S" or states[state] == "S/F":
            start_state = state

    appearance = {}
    q_prime = []
    if start_state is not None:
        appearance[tuple([start_state])] = True
        q_prime.append([start_state])

    while len(q_prime):
        q = q_prime[0]

        for symbol in sigma:
            new_state = []
            for state in q:
                if state in delta:
                    for key in delta[state]:
                        if symbol in delta[state][key]:
                            new_state.append(key)
                    if tuple(new_state) not in appearance and len(new_state) > 0:
                        q_key = tuple(q)
                        if q_key not in new_delta:
                            new_delta[q_key] = {tuple(new_state): [symbol]}
                        else:
                            if tuple(new_state) not in new_delta[q_key]:
                                new_delta[q_key][tuple(new_state)] = [symbol]
                            else:
                                if symbol not in new_delta[q_key][tuple(new_state)]:
                                    new_delta[q_key][tuple(new_state)].append(symbol)

                        q_prime.append(new_state)
                        appearance[tuple(new_state)] = True
                    elif tuple(new_state) in appearance and len(new_state) > 0:
                        q_key = tuple(q)
                        if q_key not in new_delta:
                            new_delta[q_key] = {tuple(new_state): [symbol]}
                        else:
                            if tuple(new_state) not in new_delta[q_key]:
                                new_delta[q_key][tuple(new_state)] = [symbol]
                            else:
                                if symbol not in new_delta[q_key][tuple(new_state)]:
                                    new_delta[q_key][tuple(new_state)].append(symbol)

        q_prime = q_prime[1:len(q_prime)]

    new_states[tuple([start_state])] = states[start_state]
    final_state = False
    for iter_states in appearance:
        if iter_states not in new_states:
            for state in list(iter_states):
                if states[state] == "S/F" or states[state] == "F":
                    final_state = True
            new_states[iter_states] = "F" if final_state is True else "I"
            final_state = False

    return {"states": new_states, "delta": new_delta}


def showCompositeState(state):
    if len(state) > 1:
        string = "(" + ", ".join([i for i in state]) + ")"
    else:
        string = state[0]
    return string


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Give a specific NFA file config to convert to a DFA')
    parser.add_argument('file', type=pathlib.Path)
    args = parser.parse_args()

    try:
        reading(sigma, delta, states, args.file)
        dfa_data = dfa_conversion(sigma, delta, states)

        f = open("nfa_converted_config", "w")
        f.write("Sigma:\n")
        for i in sigma:
            f.write(f"{i}\n")
        f.write("End\n\n")
        f.write("States:\n")
        for states in dfa_data['states']:
            shown = showCompositeState(states)
            if dfa_data['states'][states] == "I":
                f.write(f"{shown}\n")
            elif dfa_data['states'][states] == "S/F":
                f.write(f"{shown}, S, F\n")
            elif dfa_data['states'][states] == "F":
                f.write(f"{shown}, F\n")
            elif dfa_data['states'][states] == "S":
                f.write(f"{shown}, S\n")
        f.write("End\n\n")
        f.write("Transitions:\n")
        for which_state in dfa_data['delta']:
            which_shown = showCompositeState(which_state)
            for to_go_state in dfa_data['delta'][which_state]:
                to_go_shown = showCompositeState(to_go_state)
                for k in dfa_data['delta'][which_state][to_go_state]:
                    f.write(f"{which_shown}, {k}, {to_go_shown}\n")
        f.write("End\n\n")
        f.close()
    except Exception as exception:
        print(exception.args)
