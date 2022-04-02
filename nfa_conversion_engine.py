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




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Give a specific NFA file config to convert to a DFA')
    parser.add_argument('file', type=pathlib.Path)
    args = parser.parse_args()

    try:
        reading(sigma, delta, states, args.file)
        print(f"SIGMA: {sigma}")
        dfa_data = dfa_conversion(sigma, delta, states)
        print(f"STATES: {dfa_data['states']}")
        print(f"DELTA: {dfa_data['delta']}")
        print("State which is noted with S or S/F means that is the start state, states noted with I are intermediate and states noted with F or S/F are final.")
    except Exception as exception:
        print(exception.args)
