# NFA_Parsers - Lab 1 (Homework)
This is a Formal and Automata Language repository for NFA Parsers

### Requirements
---
* Python v3.10

### How to start
---
If we want to check if a config file contains a valid NFA we should look for the ```nfa_parser_engine.py```
```
python3 nfa_parser_engine.py <nfa_config_file>
```

If we want to check if a word is valid for a specific NFA we should run the following command:
```
python3 nfa_acceptance_engine.py <nfa_config_file> <word_to_be_validated>
```

If we want to convert a NFA to a DFA we would need to run the following command:
```
python3 nfa_conversion_engine.py <nfa_config_file>
```
This will generate a file named ```nfa_converted_config``` which will contains the specific DFA converted from the NFA inside the ```nfa_config_file```.

If we want to check if a word is accepted by a specific Epsilon-NFA we should run the following command:
```
python3 e_nfa_acceptance_engine.py <nfa_config_file> <word_to_be_tested>
```

