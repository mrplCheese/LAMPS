#import appBuilder
import secondAppBuilder
import tableMath


#It's working!
"""
Things to add:
Appbuilder:
1. Circuits: big proj.
2. backspace: Works!
3. flexible notation: Works!
4. parenthesis suggestions: Mostly works! (Doesn't tell you how many '(', only how many ')'). But it
still works really well!
5. Syntax error catching: Works!
6. popup for undefineds: Works!

tablemath:
1. simplifer (with steps labeled): big project
2. type identification (identifier, tautology, contradiction, etc.): Smaller project
3. handle propositions: LARGE project
4. Tests validity of an argument: LARGE project
"""

"""
3 goals to complete by Monday:

1. LaTeX conversion: Should take 2 hours or so. 
2. Implies, logical equivelence: Should take 4 hours or so.
3. type identification: Should take an hour

If time remains:
1. Simplification.
2. Circuits

"""

#Architecture established
#info = appBuilder.getInfo()
info = secondAppBuilder.getInfo()
tabInfo = tableMath.getTabInfo()
#app = appBuilder.App()
app = secondAppBuilder.App()
app.mainloop()


#Getting necessary pieces back from appBuilder
finalStatement = ''.join(info.getProperVis()) #Either the two logical equivelences, or the entire first statement
# print(finalStatement)
props = info.getPropList() #A list of propositional variables as strings
while ('' in props):
    props.remove('')
#print("props: ", props)
eqs = info.getEqString() #In word form, what will be fed into the math equation
#print("eqString at unifier: ", eqs)
print("eqs ",eqs)
# if(eqs[0][0] == "(" and eqs[0][len(eqs[0])-1] == ")"):
#     eqs[0] = eqs[0][1:-1]

tabular = tableMath.tableMath(eqs, props) #This will give us all the outputs that are needed. 

eerie = tabular.formatter(finalStatement)
#print(eerie)
if(len(eqs[1])!=0):
    eerie.pop()
while ('' in eerie):
    eerie.remove('')

outputs1 = tabInfo.getTruth1Str()
#All the outputs for each step. Indexes allign (outputs1[0] is the output of steps1[0])
#print("output: ", outputs1)
outputs2 = tabInfo.getTruth2Str()
logicalEq = tabInfo.getEquality() #A boolean: True if the two equations are logically equivelent.

fullTabularHeader = props + eerie
#print(fullTabularHeader)
guy = list(dict.fromkeys(fullTabularHeader)) #A little trick to get rid of duplicates.
#print(guy)

"""
A little trick to find the indexes of the duplicates.
"""
e = guy[0]
eInd = 0
duplicatesIndex = []
i = 0
while (i < len(fullTabularHeader) and eInd<len(guy)): #I miss non-enhanced for loops
    if(e == fullTabularHeader[i]):
        eInd+=1
        if(eInd!=len(guy)):
            e = guy[eInd]
    else:
        duplicatesIndex.append(i)
    i+=1
indexControl = len(duplicatesIndex) + len(guy)
while(indexControl < len(fullTabularHeader)):
    duplicatesIndex.append(indexControl)
    indexControl+=1
duplicatesIndex.reverse() #So we don't change the index as we remove values. 
#print(duplicatesIndex)

#Set up the entire grid, and then remove entire columns.
scenBuild = 2**len(props)
scStr = '0' +str(len(props))+'b'
for val in range(scenBuild):
    scene = []
    it = str(format(val, scStr))
    for e in it:
        if ("0" in e):
            scene.append("F")
        else:
            scene.append("T")
    outputs1[val] = scene + outputs1[val]
    if(len(outputs2)!=0 ):
        outputs1[val] = outputs1[val] + outputs2[val]

outputs1.insert(0, fullTabularHeader)
#print(outputs1) #Splendid.

i = 0
j = 0
while(i<len(duplicatesIndex)):
    while (j< len(outputs1)):
        outputs1[j].pop(duplicatesIndex[i])
        j+=1
    i+=1
#print(outputs1)
#Splendid (2x)
#tableBuilder = appBuilder.table(outputs1, logicalEq)
tableBuilder = secondAppBuilder.table(outputs1, logicalEq)
tableBuilder.mainloop()