import sys
import os
import string


class Node(object):
    def __init__(self, state_num, is_accept):
        self.state_num = state_num
        self.is_accept = is_accept  
        # self.outgoing = []
        # self.incoming = []

class Edge(object):
    def __init__(self, origin, destin, phrase):
        self.orig = origin
        self.dest = destin
        self.phrase = phrase

def create_dfa_from_regex(regex):

    states = []
    transitions = []
    
    pren_state_stack = []

    inital_state = Node(0, True)
    states.append(inital_state)


    if regex == "": # returns a single accepting node in case the regex is the empty string
        single_edge = Edge(0, 0, "")
        transitions.append(single_edge)
        return (states, transitions)

    else:
        states[0].is_accept = False

        for i in range(0, len(regex)):
            curr_state = states[len(states)-1] # keeps us at the current state to append transitions to
            curr_char = regex[i]
            if curr_char.isAlpha():
                #makes a new node and then a transition from the previous node to this node,
                #  with the current character as the transiton element
                new_state = Node(curr_state.state_num+1, True)
                new_transition = Edge(curr_state.state_num,new_state.state_num,curr_char)
                states.append(new_state)
                transitions.append(new_transition)
            elif curr_char == "*":
                # makes a transition from the current node to itself
                new_transition = Edge(curr_state.state_num,curr_state.state_num,regex[i-1])
                transitions.append(new_transition)
            elif curr_char == "|":
                asdf=0
                #TODO: Complete this
                # add a second edge from the current node to the destination node
            elif curr_char == "(":
                asdf=0
                #TODO: Complete this
                # Put the current state on a stack. 
                # Make a new dfa out of the elements after the pushed state,
                #  and then concat this sub-dfa to the larger one once the second 
                #  ending paren is noticed. 
                pren_state_stack.append(curr_state)
            elif curr_char == ")":
                asdf=0
                # TODO: Complete this, see previous elif case

            else:
                print("Unrecognized character entered. Valid characters are the following:\n \
                    \"|\" , \"*\", \"(\", \")\", and all letters [a-z] in lowercase.")
                return None 


def run_string_through_nfa(string, nfa):
    asdfasdf=0
    # dfa will be a tuple of ([states], [transitions])
    for letter in string:
        asdfasdf=0
        # step through the nfa with the word.
        # if there is a nondeterministic split, 
        #  run both paths and if one accepts, then return true, else false


'''
def create_state_table(expr):

    global state_table

    state_id = 0
    state_table[state_id] = (state_id, "start")

    for char in expr:
        state_id += 1
        # if char is "*":

        state_table[state_id] = (state_id, char)
    state_table[state_id] = ((state_id, "accept"))
    print(state_table)

'''