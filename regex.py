import sys

class Expression(object):
	def __init__(self, exp):
		self.exp = exp
		self.table = {}
		#self.subExpressions = []

	def isAlpha(c):
		return not c in ["*", "|", "(", ")"]

	def isOperator(c):
		return c in ["*", "|"]

	def getNextOperator(index):
		for i in range(index, len(self.exp)):
			if isOperator(i):
				return i

	def starify(table):
		startable = {}
		startable[(1, "")] = 0
		startable[(0, "")] = 0
		startable[(0, table.keys()[0])] = table[(1, table.keys[0])]

		return startable

	def parseSubExpressions(subexp):
		if isAlpha(subexp[0]) and isAlpha(subexp[1]):
			singletonTable = {}
			singletonTable[(1, subexp[0])] = 0
			#self.subExpressions.append(singletonTable)
			self.table = tableConcat(singletonTable, parseSubExpressions(subexp[1:]))
		elif isAlpha(subexp[0]) and subexp[1] == "*":
			singletonTable = {}
			singletonTable[(1, self.exp[0])] = 0
			operatorTable = starify(singletonTable, subexp[1])
			self.table = tableconcat(operatorTable, parseSubEcpressiont(subexp[2:]))


	def buildTable():
		parseSubExpressions(self.exp[0:])
