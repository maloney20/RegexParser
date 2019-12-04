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

	def findAccept(self, state, accepts, visited):
		visited.append(state)
		#print("l")
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
		

	def printStateList(self, states):
		print(list(map(lambda x: x.num, states)))

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
				#e.out.append(("", "next"))
				frag = Fragment(s, [e])
				frag.connectors.append(e)

				fragments.append(frag)
			elif ch == "*":
				print("applying star")
				f = fragments.pop()
				s = State(statenum, True)
				frag = Fragment(s, [s])
				s.out.append(("", f.start))
				#s.out.append(("", "next"))
				frag.connectors.append(s)
				print("end states for star")
				self.printStateList(f.end)
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
				self.printStateList(parenExp.end)
				fragments.append(parenExp)
				i = closeIndex-1
			i+=1
			# for i in range(len(fragments)):
			# 	print("fragments[", i, "]:")
				
			# 	print("conn", list(map(lambda x: x.num, fragments[i].connectors)))


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
		#self.showNfa(rtn.start, [])
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
			#print("at", ch)
			epsilonReachable = self.getEpsilonReachable(possibleStates.copy())
			#print("reachable", list(map(lambda x: x.num, epsilonReachable)))
			possibleStates = possibleStates+epsilonReachable
			#print("possible", list(map(lambda x: x.num, possibleStates)))
			for state in possibleStates:
				for out in state.out:
					#print("checking", out)
					if out[0] == ch:
						#print("adding", out[1].num, "to possible")
						newPossible.append(out[1])
						#print(list(map(lambda x: x.num, newPossible)))
			possibleStates = newPossible
			#print("after", ch, list(map(lambda x: x.num, possibleStates)))
		#print("string consumed. Possible:", list(map(lambda x: x.num, possibleStates)))
		possibleStates = possibleStates + self.getEpsilonReachable(possibleStates.copy())
		for state in possibleStates:
			if state.accept:
				return "Accepted!"
		return "Rejcted."


def main():
	# exp = Expression("(ab)*")
	# print("-------------------------------------")
	# print(str(exp.match("ab")))
	# print(str(exp.match("abab")))
	# print(str(exp.match("")))
	# print(str(exp.match("aba")))
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








