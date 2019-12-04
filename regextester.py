from regex import Expression

exp = "a*b"

table = Expression(exp)
table.buildTable()
print(table.table)