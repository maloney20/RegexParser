import sys

exp = sys.argv[1]

def isAlpha(s):
	for ch in s:
		if ord(ch) not in range(65, 90) and ord(ch) not in range(97, 122):
			return False
	return True

def isOperator(s)
	return s == "*" or s == "|"

class Expression:

	class State:
		def __init__(self, accept):
			self.accept = accept
			self.out = []

	class Fragment:
		def __init__(self, start, end):
			self.start = start
			self.end = end


	def __init__(self, exp):
		self.exp = exp
		self.accept = []
		self.start = self.buildNFA()

	def buildNFA(self):
		fragments = []
		for i in range(len(self.exp)):
			ch = self.exp[i]
			if isAlpha(ch):
				s = State(False)
				e = State(True)
				s.out.append((ch, e))
				e.out.append(("", "next"))
				fragments.append(Fragment(s, [e]))
			elif ch == "*":
				f = fragments.pop()
				s = State(True)
				s.out.append(("", f.start))
				s.out.append(("", "next"))
				for end in f.end:
					end.accept = False
					for out in end.out:
						out.append(("", s))
				fragments.append(Fragment(s, [s]))
			elif ch == "|":
				f = fragments.pop()
				s = State(False)
				s.out.append("", f.start)
				s.out.append("", "next")
				for end in f.end:
					for out in end.out:
						if out[1] == "next":
							end.out.remove(out)
				fragments.append(Fragment((s, f.end)))
			elif ch == "(":
				pstack = ["("]
				closeIndex = i
				for j in range(i, len(self.exp)):
					if self.exp[j] == "(":
						pstack.append("(")
					elif self.exp[j] == ")":
						pstack.pop()
					elif pstack.isEmpty():
						closeIndex = j
						break
				parenExp = Expression(self.exp[i:closeIndex]).buildNFA()
				fragments.append(parenExp)


		#put all fragments together
		endStates = []
		for i in range(len(fragments)):
			if i == len(fragments)-1:
				endStates = fragments[i].end
				break
			frag = fragments[i]
			for end in frag.end:
				end.out.append(("", fragments[i+1].start))


		self.start = fragments[0].start
		return Fragment((fragments[0].start, endStates))


	#simulate s on the nfa
	def match(self, s):
		possiblestates = [self.start]
		for ch in s:
			for state in possiblestates:
				for out in state.out:
					if out[1] == ch:









