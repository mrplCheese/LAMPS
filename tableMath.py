from array import *

seq = []
truth1 = []
truth1Str = []
seq2 = []
truth2 = []
truth2Str = []
#scen = []
eq = False

class tableMath:
    
    def __init__(self, eqList, propList):
        #As of now, the object must be created at the moment every value is filled in.
        #While this isn't the most flexible option, it works for our most current
        #version of the program. In the future, it may be beneficial to change this.
        global seq
        global truth1
        global truth1Str
        global seq2
        global truth2
        global truth2Str
        global eq
        #print(eqList)
        self.eqString = eqList[0]
        self.eqString2 = eqList[1]
#         print("b: ",self.eqString)
#         print("second statement: ",self.eqString2)
        #self.eqString = self.eqStringPrep()
        self.propList = propList
        self.eqLab = len(self.eqString)
        self.scLab = len(propList)
        seq = self.formatter(eqList[0])
        halBuild = self.scenarios(seq)
        truth1 = halBuild[0]
        truth1Str = halBuild[1]
        
        if(self.eqString2 != ""):
            self.eqLab2 = len(self.eqString2)
            seq2 = self.formatter(eqList[1])
            halBuild = self.scenarios(seq2)
            truth2 = halBuild[0]
            truth2Str = halBuild[1]
            eq = self.equalitys()
            #print(eq)
    
    def scenarios(self, evaluation):
        scenBuild = 2**self.scLab
        scStr = '0' +str(self.scLab)+'b'
        scOut = []
        scOutStr = []
        for val in range(scenBuild):
            scene = []
            it = str(format(val, scStr))
            #print(it)
            for e in it:
                if ("0" in e):
                    scene.append(False)
                else:
                    scene.append(True)
            halBuild = self.truth(scene, evaluation)
            scOut.append(halBuild[0])
            scOutStr.append(halBuild[1])
        unifier = [scOut, scOutStr]
        #print("sCout: ",scOut)
        return(unifier)
        
        
    def truth(self, scene, evaluation):
        x = []
        xStr = []
        builder = {}
        for state in evaluation:
            for elem in range(self.scLab):
                #initial = self.propList[elem] + ' = ' + str(scene[elem])
                builder[self.propList[elem]] = scene[elem]
            #print(builder)
            if(state != ""):
               # print("state: ",state)
                halBuild = eval(state)
                x.append(halBuild)
                if(halBuild):
                    xStr.append("T")
                else:
                    xStr.append("F")
                
            #print(str(x))
        unifier = [x, xStr]
        return(unifier)

    def formatter(self, formatted):
        info = self.find_parens(formatted)
        keys = list(info)
        stepList=[]
        for i in keys:
            strGuy = formatted[i:(info[i]+1)]
            #print(strGuy)
            stepList.append(strGuy)
        stepList.append(formatted)
        return stepList
        
    def find_parens(self, s):
        #print(s)
        toret = {}
        pstack = []

        for i, c in enumerate(s):
            if c == '(' and s[i+1] != "'":
                pstack.append(i)
            elif c == ')' and s[i-1] != "'":
                if len(pstack) == 0:
                    raise IndexError("No matching closing parens at: " + str(i))
                toret[pstack.pop()] = i

        if len(pstack) > 0:
            raise IndexError("No matching opening parens at: " + str(pstack.pop()))

        return toret
    

    def getTruths(self, index):
        if (index ==0):
            return truth1
        if(index==1):
            return truth2
        else:
            print("invalid index")
            return None
            
    def equalitys(self):
        #Should compare the last statement of every list in the list of list Truths
        ind1 = len(truth1[0])-1
        ind2 = len(truth2[0])-1
        outInd = len(truth1)-1
        if (ind1 != ind2):
            return False
        for trial in range(outInd):
            if (truth1[trial][ind1] != truth2[trial][ind1]):
                #print(truth1[trial][ind1])
                return False
        return (True)
    
class getTabInfo:
    
    def getSeq1(self):
        return seq
    
    def getSeq2(self):
        return seq2
    
    def getTruth1(self):
        return truth1
    
    def getTruth1Str(self):
        return truth1Str
    
    def getTruth2(self):
        return truth2
    
    def getTruth2Str(self):
        return truth2Str
    
    def getEquality(self):
        return eq
    
    


# equation = ["( not ( not ( builder.get('p') and builder.get('q') ) ) and ( builder.get('q') or builder.get('p') ) )", "builder.get('q') and (not builder.get('p'))"] #
# #equationy = ["builder.get('u') and builder.get('e')","builder.get('u') or builder.get('j')"]
# props = ["p", "q"]
# #propsy = ["u","e","j"]
# tab = tableMath(equation, props)
# 
# infoStealer = getTabInfo()
# 
# print(infoStealer.getSeq1())
# print(infoStealer.getSeq2())
# print(infoStealer.getTruth1())
# print(infoStealer.getTruth2())
# print(infoStealer.getEquality())