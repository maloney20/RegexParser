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
			self.end = [end]


	def __init__(self, exp):
		self.exp = exp
		self.start = self.buildNFA()

	def buildNFA():
		fragments = []
		for i in range(len(self.exp)):
			ch = self.exp[i]
			if isAlpha(ch):
				s = State(False)
				e = State(True)
				s.out.append((ch, e))
				fragments.append(Fragment(s, e))
			elif ch == "*":
				f = fragments.pop()
				for end in f.end:
					for out in end.out:
						out.append(("", f.start))

		for i in range(len(fragments)):
			if i == len(fragments):
				break
			frag = fragments[i]
			for end in frag.end:
				end.out.append(("", fragments[i+1].start))

		return fragments[0].start


	def match(self, s):
		possiblestates = [self.start]
		for ch in s:
			for state in possiblestates:
				for out in state.out:
					if out[1] == ch:









