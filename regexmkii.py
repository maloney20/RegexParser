import sys
import os
import string

state_table = {}


class Node(object):
    def __init__(self, state_num, is_accept):
        self.state_num = state_num
        self.is_accept = is_accept  
        # self.outgoing = []
        # self.incoming = []

class Edge(object):
    def __init__(self, orig, dest, phrase):
        self.orig = orig
        self.dest = dest
        self.phrase = phrase

def create_dfa_from_regex(regex):
    states = []
    transitions = []
    
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
                #makes a transition from the current node to itself
                new_transition = Edge(curr_state.state_num,curr_state.state_num,regex[i-1])
                
            elif curr_char == "|":
                asldfkjhas = 0 # dummy code, gotta handle that stuff later
            # elif curr_char == "("

            # elif curr_char == ")" 


    


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