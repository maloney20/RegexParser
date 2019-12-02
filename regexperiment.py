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


class Expression:
	def __init__(self, exp):
		self.exp = exp
		self.accept = []
		self.buildNFA()
		self.showNfa(self.start, [])

	def showNfa(self, state, shownStates):
		print(state.num)
		for t in state.out:
			print(t[0], t[1].num, t[1].accept)
		print()
		shownStates.append(state.num)
		for t in state.out:
			if t[1].num not in shownStates:
				self.showNfa(t[1], shownStates)

	def buildNFA(self):
		fragments = []
		for i in range(len(self.exp)):
			ch = self.exp[i]
			if isAlpha(ch):
				s = State(statenum, False)
				e = State(statenum, False)
				s.out.append((ch, e))
				#e.out.append(("", "next"))
				frag = Fragment(s, [e])
				frag.connectors.append(e)

				fragments.append(frag)
			elif ch == "*":
				f = fragments.pop()
				s = State(statenum, False)
				frag = Fragment(s, [s])
				s.out.append(("", f.start))
				#s.out.append(("", "next"))
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

		#put all fragments together
		endStates = []
		for i in range(len(fragments)):
			if i == len(fragments)-1:
				endStates = fragments[i].end
				for end in endStates:
					#print(end.num, "accepts")
					end.accept = True
				break
			frag = fragments[i]
			for con in frag.connectors:
				con.out.append(("", fragments[i+1].start))

		self.start = fragments[0].start
		return Fragment(fragments[0].start, endStates)

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
				return True
		return False


def main():
	exp = Expression("a*b")
	print("-------------------------------------")
	print(str(exp.match("ab")))
	print(str(exp.match("aaab")))
	print(str(exp.match("b")))
	print(str(exp.match("aba")))

main()








