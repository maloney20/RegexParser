import sys
statenum = 0
def isAlpha(s):
	for ch in s:
		if ord(ch) not in range(65, 90) and ord(ch) not in range(97, 122):
			return False
	return True

def isOperator(s):
	return s == "*" or s == "|"

class State:
		def __init__(self, num, accept):
			global statenum
			statenum += 1
			self.num = num
			self.accept = accept
			self.out = []

class Fragment:
	def __init__(self, start, end):
		self.start = start
		self.end = end
		self.connectors = []

	def getAcceptStates(self):
		return self.findAccept(self.start, [], [])

	#return all accept states into 'accepts' list
	def findAccept(self, state, accepts, visited):
		visited.append(state)
		if state.accept and state not in accepts:
			accepts.append(state)
		if len(state.out) > 0:
			for o in state.out:
				if not o[1] in visited:
					accepts = accepts + self.findAccept(o[1], accepts, visited)
		return accepts


class Expression:
	def __init__(self, exp):
		self.exp = exp
		self.accept = False
		self.buildNFA()
		#self.showNfa(self.start, [])
		

	def showNfa(self, state, shownStates):
		
		print(state.num)
		for t in state.out:
			print("\'"+t[0]+"\'", t[1].num, "accept" if t[1].accept else "")
		print()
		shownStates.append(state.num)
		for t in state.out:
			if t[1].num not in shownStates:
				self.showNfa(t[1], shownStates)
		
	#debug function to print state nums in list
	def printStateList(self, states):
		print(list(map(lambda x: x.num, states)))

	def stateListEquals(self, l1, l2):
		if len(l1) != len(l2):
			return False
		else:
			for i in range(len(l1)):
				if l1[i].num != l2[i].num:
					return False
		return True

	def print(self):
		print("NFA")
		print("---------------")
		self.showNfa(self.start, [])
		print("---------------")

	def buildNFA(self):
		fragments = []
		i=0
		while i < len(self.exp):
			ch = self.exp[i]
			if isAlpha(ch):
				s = State(statenum, False)
				e = State(statenum, True)
				s.out.append((ch, e))
				frag = Fragment(s, [e])
				frag.connectors.append(e)

				fragments.append(frag)
			elif ch == "*":
				f = fragments.pop()
				s = State(statenum, True)
				frag = Fragment(s, [s])
				s.out.append(("", f.start))
				frag.connectors.append(s)
				for end in f.end:
					end.accept = False
					end.out.append(("", s))

				fragments.append(frag)
			elif ch == "|":
				f = fragments.pop()
				s = State(statenum, False)
				s.out.append(("", f.start))
				for end in f.end:
					end.accept = True
					for out in end.out:
						out.out = []
				frag = Fragment(s, f.end)
				frag.connectors.append(s)
				fragments.append(frag)
			elif ch == "(":
				pstack = ["("]
				closeIndex = i
				for j in range(i+1, len(self.exp)):
					if self.exp[j] == "(":
						pstack.append("(")
					elif self.exp[j] == ")":
						pstack.pop()
					elif len(pstack)==0:
						closeIndex = j
						break
				parenExp = Expression(self.exp[i+1:closeIndex-1]).buildNFA()
				fragments.append(parenExp)
				i = closeIndex-1
			i+=1


		#put all fragments together
		for i in range(len(fragments)):
			if i == len(fragments)-1:
				break
			frag = fragments[i]
			for con in frag.connectors:
				con.accept=False
				con.out.append(("", fragments[i+1].start))

		self.start = fragments[0].start
		endStates = fragments[0].getAcceptStates()
		endStates = list(dict.fromkeys(endStates))
		rtn = Fragment(fragments[0].start, endStates)
		rtn.connectors = endStates
		return rtn

	def getEpsilonReachable(self, states):
		if len(states) == 0:
			return []
		reachable = []
		for state in states:
			for out in state.out:
				if out[0] == "":
					reachable.append(out[1])
		return reachable + self.getEpsilonReachable(reachable)

	#simulate s on the nfa
	def match(self, s):
		
		possibleStates = [self.start]
		
		for ch in s:
			newPossible = []
			epsilonReachable = self.getEpsilonReachable(possibleStates.copy())
			possibleStates += epsilonReachable
			for state in possibleStates:
				for out in state.out:
					if out[0] == ch:
						newPossible.append(out[1])
			possibleStates = newPossible
		possibleStates = possibleStates + self.getEpsilonReachable(possibleStates.copy())
		for state in possibleStates:
			if state.accept:
				return "Accepted!"
		return "Rejcted."


def main():
	print("Enter regular expression:", end=" ")
	exp = Expression(input())
	
	exp.print()
	print("Now enter some strings (or \'quit\' to quit)")
	inp = ""
	while True:
		print(">", end=" ")
		inp = input()
		if inp == "quit":
			break
		print(str(exp.match(inp)))


main()








