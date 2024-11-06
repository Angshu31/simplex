def fmt(n):
    if int(n) == n: return str(int(n))
    return str(round(n, 3))

def leftPad(s, l):
    while len(s) < l:
        s = " " + s
    return s

def printTableu(tableu, colTitles, basicVariables, rowOps):
    showable = [["bv"]+colTitles]
    if rowOps: showable[0].append("")
    colWidths = [len(x) for x in showable[0]]
    colWidths[0]=2
    for i in range(len(tableu)):
        row = tableu[i]
        showRow = []
        showRow.append(basicVariables[i])
        if len(basicVariables[i]) > colWidths[i]:
            colWidths[i] = len(basicVariables[i])
        for j in range(len(row)):
            s = fmt(row[j])
            showRow.append(s)
            if len(s) > colWidths[j+1]: colWidths[j+1] = len(s)
        if rowOps: showRow.append(rowOps[i])
        showable.append(showRow)


    for row in showable:
        s = " "
        for j in range(len(row)):
            entry = leftPad(row[j], colWidths[j])
            s += entry
            if j != len(row)-1:
                s += " | "
        print(s)


def iterate(tableu, colTitles, basicVariables):
    # Copy tableu first
    newBasicVariables = [x for x in basicVariables]
    newtableu = []
    for row in tableu:
        newrow = []
        for k in row: newrow.append(k)
        newtableu.append(newrow)

    # Find most negative entry in objective row
    objRow = newtableu[len(newtableu)-1]
    pivotCol = -1
    mostNegNum = 0
    for i in range(len(objRow)):
        k = objRow[i]
        if k > mostNegNum: continue
        mostNegNum = k
        pivotCol = i
    if mostNegNum == 0: return (None, None, None, None)

    # Find theta values
    leastPosTheta = float("inf")
    pivotRowIdx = -1
    for i in range(len(newtableu)-1):
        row = tableu[i]
        if row[pivotCol] == 0: continue
        theta = row[len(row)-1] / row[pivotCol]
        if theta < 0: continue
        if theta < leastPosTheta:
            pivotRowIdx = i
            leastPosTheta = theta

    pivotRow = newtableu[pivotRowIdx]
    pivotVal = pivotRow[pivotCol]
    for i in range(len(pivotRow)):
        pivotRow[i] /= pivotVal
    newBasicVariables[pivotRowIdx] = colTitles[pivotCol]
        
    rowOps = ["" for x in tableu]
    rowOps[pivotRowIdx] = "R"+str(pivotRowIdx+1) + "/" + fmt(pivotVal)

    for i in range(len(newtableu)):
        if i == pivotRowIdx: continue
        row = newtableu[i]
        k = -row[pivotCol]
        if k == 0:
            rowOps[i] = "R"+str(i+1)
            continue
        for j in range(len(row)):
            row[j] = row[j] + k*pivotRow[j]
        rowOps[i] = "R"+str(i+1) + ("+" if k > 0 else "") + fmt(k) + "R" + str(pivotRowIdx+1)

    return (newtableu, colTitles, newBasicVariables, rowOps)
    
alphabets = ["A", "B", "C", "D", "E", "F", "G", "H"]
def take(arr, a, b):
    res = []
    for i in range(a, b):
        res.append(arr[i])
    return res

def expr(coeffs, variables, WS=False):
    s = ""

    for i in range(0, len(coeffs)):
        if isinstance(coeffs[i], str):
            s += ("" if s == "" else " + ") + coeffs[i] + variables[i]
            continue
        if coeffs[i] == 0:
            if WS: s += "    " + (" " * len(variables[i]))
        elif coeffs[i] < 0:
            s += ("-" if s == "" else " - ") + ("" if coeffs[i] == -1 else str(-coeffs[i])) + variables[i]
        else:
            s += ("" if s == "" else " + ") + ("" if coeffs[i] == 1 else str(coeffs[i])) + variables[i]
    return s

# Get initial tableu
print("Normal Simplex Algorithm")
varCount = int(input("Number of main variables: "))
mainVars = []
if varCount == 0:
    print("Error")
    exit()
    
if varCount <= 3:
    if varCount == 1: mainVars = ["x"]
    elif varCount == 2: mainVars = ["x", "y"]
    else: mainVars = ["x", "y", "z"]

else:
    for i in range(1, varCount+1):
        mainVars.append("x"+str(i))

placeholders = take(alphabets, 0, varCount)

numberOfConstraints = int(input("Number of constraints (exclude non-neg.): "))
constraints = []

placeholderEq = expr(placeholders, mainVars)

objectiveCoeffs = []
print("max P = "+ placeholderEq)
for i in range(varCount):
    objectiveCoeffs.append(int(input(placeholders[i]+": ")))
print("P = " + expr(objectiveCoeffs, mainVars))
print()

placeholderEq += " <= " + alphabets[varCount]
for n in range(1, numberOfConstraints+1):
    print("Constraint "+str(n)+": "+ placeholderEq)
    row = []
    for i in range(varCount):
        row.append(int(input(placeholders[i]+": ")))
    
    row.append(int(input(alphabets[varCount]+": ")))
    constraints.append(row)
    print(expr(take(row, 0, varCount), mainVars) + " <= " + str(row[varCount]))
    print()


tableu = []
basicVariables = []
colTitles = take(mainVars, 0, varCount)
slackCount = 0

for con in constraints:
    tableu.append(take(con, 0, varCount))

objRow = []
for k in objectiveCoeffs:
    objRow.append(-k)
tableu.append(objRow)
objRow.append(0)

for i in range(len(constraints)):
    for j in range(len(tableu)):
        tableu[j].append(0)
    row = tableu[i]
    row[len(row)-1]=1
    slackCount+=1
    colTitles.append("s"+str(slackCount))

for i in range(slackCount):
    basicVariables.append("s" + str(i+1))
basicVariables.append("P")
colTitles.append("Val")

print("Equations: ")
for i in range(len(constraints)):
    row = tableu[i]
    con = constraints[i]
    print(expr([0]+row, ["P"]+colTitles) + " = " + str(con[len(con)-1]))
    row.append(con[len(con)-1])
print(expr([1] + tableu[len(tableu)-1], ["P"]+colTitles) + " = 0")
print()

print("Initial Tableu: ")
printTableu(tableu, colTitles, basicVariables, False)
print()

i = 1
while True:
    newtableu, _, bvs, rowOps = iterate(tableu, colTitles, basicVariables)
    if newtableu == None:
        opt = []
        for t in colTitles:
            if t == "Val": continue
            if t in basicVariables:
                idx = basicVariables.index(t)
                row = tableu[idx]
                opt.append(t + " = " + fmt(row[len(row)-1]))
            else:
                opt.append(t + " = 0")
                
        print("Optimal Solution: P = " + fmt(tableu[len(tableu)-1][len(tableu[0])-1]))
        print("where " + ", ".join(opt))
        break
    print("Iteration", i)
    printTableu(newtableu, colTitles, bvs, rowOps)
    print()
    
    tableu = newtableu
    basicVariables = bvs
    i += 1
