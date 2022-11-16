#import secondAppBuilder
import re
"""
Is working well so far!
Major things to add:
1. logical equivelence management
2. Implies function
3. TKinter popUp for unknown symbols
4. parenthesis catcher upgrade (shows all necessary pairs at once)
5. Unknown symbol upgrade (one adaption will change every instance of it)
6. Clean up/ remove unnecessary defs (I think there are a few.): Will get around to if time remains
7. Spaces/Ease of use for user: Works!!
8. capitalization of t & f, since t and f could technically be variable names rather than True and False.
"""

from tkinter import *
"""
AppBuilder helper module:

In charge of live translations, syntax error catching, and data preperation. 

"""
"""
Logical equivelence and implications are both functions, which have their own
rules to follow.
For the tests:
    logEq can just be replaced with "==".
    a implies b can just be replaced with "False"
But for the live translation, it's a bit more complex:
    LogEq will mainly be handled by secondAppBuilder, with the indexing thing.
        But visually, it has to remain: a ≡ b
    (This will take a bit of time to figure out how that works with the new AppHelper method)
    a implies b will need to be translated to implies(Builder.get('a'),Buileder.get('b')) .
        But visually, it has to remain (a → b)

"""
class liveCatch:
#    global contQ
#    global pLock
#    global pInput
#    global rInput
    
    keyDict = {
        "and": ["and","&", "∧"],
        "or": ["or", "||", "V", "∨" ],
        "^": ["xor", "^", "⊕"],
        "==": ["iff", "==", "<->", "↔"],
        "True": ["true", "T"],
        "False": ["false", "F"],
        "implies": ["implies","->", "-->", "→"],
        "nand": ["nand", "|"],
        "nor" : ["nor", "↓"],
        "logEq" : ["logeq", "≡"],
        "not" : ["not", "¬","∼","~"],
        "(": ["("],
        ")": [")"]
        }
    
        #implies / logEq are weird. Not sure how to do them yet.
    order = ["(",")","not","and", "or", "^", "==", "True", "False", "implies", "nand", "nor", "logEq"]
    #This probably isn't the most efficient way to do this. 
    
    def __init__(self):
#         global contQ
#         global pLock
#         contQ = True
#         global pInput
#         global rInput
        self.refresh()
    
    def parenMatcher(self):
        toret = {}
        pstack = []

        for i, c in enumerate(self.rInput):
            if c == '(':
                pstack.append(i)
            elif c == ')':
                if len(pstack) == 0:
                    self.contQ = False
                    print("Missing (")
                    return ["(", ""]
                    #collection.append("(")
                toret[pstack.pop()] = i

        if len(pstack) > 0:
            self.contQ = False
            print("missing ", len(pstack), ": )")
            return ["missing ", str(len(pstack)), ": )"] # Could benefit from more versatility.
        return toret
    #ParenMatcher suggestion: Break string up into substrings of collected, proper parenthesis matches
    #Either index 1 in the array or the final index will contain too many parenthesis "(" in ind 1, ")" in final index. 
    
    def parenMatcher2(self):
        toret = {}
        pstack = []
        collection = []
        for i, c in enumerate(self.rInput):
            if c == '(':
                pstack.append(i)
            elif c == ')':
                if len(pstack) == 0:
                    self.contQ = False
                    print("Missing (")
                    collection.append("(")
                    
                toret[pstack.pop()] = i

        if len(pstack) > 0:
            self.contQ = False
            print(len(pstack))
            i = 0
            while(i<len(pstack)):
                collection.append(")")
                i-=1
            print(collection)
            return [")"]
        return toret
    #It works, but only catches the first parenthesis error, which is alright for now.
        
    def translator (self):
        #Find all indexes of spaces.
        #Translate all values to their boolean equivelence (via dict)
        #Ask if there are any odd words
        #If not, ask if there are any syntax errors.
        #If not, success (:
        #Create a sort before entering the loop?
#         inds = [i for i, letter in enumerate(self.rInput) if letter == " "]
#         inds = inds + self.spacebarManager(self.rInput)
        self.rInput = self.spacebarManager(self.rInput)
        pieces = self.rInput.split()
        #print("in: ",self.rInput)
        #print("indexes of spaces", inds) #allegedly

        #pieces = self.pieceFinder(inds)
        while("" in pieces):
            pieces.remove("")
        #print(pieces)
        pPieces = []
        oddIndex = []
        #Now we translate each piece using the dictionary
        ind = 0
        countyGuy = 0
        for piece in pieces: #Iterate through each word collection
            ind+=1
            nue = True
            while (nue):  # shortcut stops.
                countyGuy = 0
                for i in self.order: # searches through dictionary keys
                    countyGuy+=1
                    #print(self.keyDict.get(i))
                    if (self.keyDict.get(i).count(piece)>0):
                        #print("cool?")
                        # Does the list attached to a key contain the word we're looking at?
                        pPieces.append(i) #If so, we'll add the key to the "translated words"
                        self.pLock.append(i)
                        self.pLock.append(" ")
                        #self.properVisual.append(self.keyDict.get(i)[len(self.keyDict.get(i))-1]) #That's terrifying.
                        nue = False
                        break
                    else:
                        if(len(piece) == 1 and piece.isalpha() and countyGuy>8):
                            #print("WA")
                            pPieces.append("False")
                            self.vars.append(piece)
                            strGuy = f" builder.get('{piece}') "
                            self.pLock.append(strGuy)
                            self.keyDict[strGuy] = [f"{piece}"]
                            #self.properVisual.append(piece)
                            nue = False
                            break
                if (nue):
                    pPieces.append(piece)
                    self.pLock.append(piece)
                    oddIndex.append(ind)
                    nue = False #In the future, we'll have to translate logEq and implies in unique ways. 
        
        #print(pPieces)
        #print(oddIndex)
        """3 possibilities at this point: Unknown pieces, syntax error, or good to go.
        Unknown piece: Pop up asking about it, user defines it, and then it moves onto translation.
        Syntax error: The piece with the first syntax error shows up red in the TKinter applett.
        Good to go: Displays a little message saying no errors have been found on Tkinter applett
        """
        if (len(oddIndex)>0):
            self.oddWord(oddIndex, pPieces)
        return pPieces
        
    def pieceFinder(self, inds):
        piece = []
        i = 0
        while (i<len(inds)-1):
            piece.append(self.rInput[inds[i]+1:inds[i+1]])
            i+=1
        piece.append(self.rInput[inds[i]+1:len(self.rInput)])
        #print(piece)
        return piece
            
        
    def oddWord (self, oddIndex, pieces):
        #print("oddIndex: ", oddIndex)
        #print("pieces: ", pieces)
        build = infoUI("TestTest") #Only def that instaantiates an infoUI object
        keyTranslate = pieces
        replace = []
        for i in oddIndex:
            oddW = keyTranslate[i-1]
            #print("oddW: ", oddW)
            if (oddW in replace):
                #print("YEET")
                break
            #Label(wordUI, text = "WHAT?")
            #keyTranslate[i-1] = input(f"What is the meaning of this: '{oddW}' ?")
            build.setLabel(f"What is the meaning of this: '{oddW}'")
            rock = build.getValue()
            keyTranslate[i-1] = rock
            replace.append(rock)
            #self.properVisual.insert(i-1, self.keyDict.get(rock))
            #self.properVisual.insert(i-1, keyTranslate[i-1])
            counter = 0
            while (counter < len(self.pLock)):
                indy = self.pLock[counter]
                if (indy == oddW):
                    #print("'sup bby grl")
                    self.pLock[counter] = keyTranslate[i-1]
                counter+=1
                
        self.pInput = keyTranslate
        build.selfDestruct() 
    
    def syntax(self):
        pPieces = []
        for i in self.pInput:
            pPieces.append(i)
            pPieces.append(" ")
        stringCheese = ''.join(pPieces)
        #print(stringCheese)
        
        try:
            eval(stringCheese)
        except:
            self.contQ = False
            return(f"syntax error")
        else:
            print("success!", stringCheese)
        #print("huh")
    
    def visualTranslator(self):
        #Since each piece, by this point, is made up of keys, we can just convert from key to
        #last value in the associated list.
        index = 0
        part = []
        for i in self.pLock:
            if (i != " "):
                part = self.keyDict[i]
                index = len(part)-1
                self.properVisual.append(part[index])

#    def spacebarManager(self, stringy):
#         print("stringy: " + stringy)
#         indexer = []
#         counter = -1
#         for i in stringy:
#             counter+=1
#             if (i.isalpha()):
#                 indexer.append(counter-1)
#         #Give the string spaces at the indexes.
#         indexedCheese = []
#         indexedCheese[:0] = stringy
#         print("unbroken indexedCheese: ", indexedCheese)
#         #converts string to a flexible array
#         counter = len(indexer)-1
#         #Iterate through the array backwards to prevent position redundency.
#         
#         while(counter>-1):
#             indexedCheese.insert(indexer[counter], " ")
#             counter-=1
#         print("indexedCheese: ", indexedCheese)
#         return indexer
    
    def spacebarManager(self, stringy):
        res = re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", stringy)
        #print(str(res))
        return(str(res))
            
    
    def packager (self): 
        self.pInput = self.parenMatcher()
        if (not self.contQ):
            print(self.pInput, "Inside appHelper")
            return self.pInput
        self.pInput = self.translator()
        bob = self.syntax()
        if (not self.contQ):
            return bob
        self.visualTranslator()
        return ("yeye")
        
    def getPInput (self):
        return self.pInput
        
    def setRInput (self, raw):
        self.refresh()
        self.rInput = raw
    
    def getRInput(self):
        return self.rInput
    
    def getContQ (self):
        return self.contQ
    
    def getPLock(self):
        return self.pLock
    
    def getVars(self):
        #print("Here's what getVars is returning: ", self.vars)
        return self.vars
    
    def getProperVisual(self):
        return self.properVisual
        
    def refresh (self):
        self.contQ = True
        self.pInput = ""
        self.rInput = ""
        self.pLock = []
        self.vars = []
        self.properVisual = []
        
class infoUI:   
    
    def __init__(self, bobTheBuilder):
        self.window = Tk()
        self.window.geometry("250x250")
        self.clicked = StringVar()
    
        self.options =["(",")","not","and","or",
              "^", "==", "True", "False",
              "implies", "nand", "nor", "logEq"]
    
        self.imp = Label(self.window)
        self.imp.config(text = bobTheBuilder)
        self.imp.pack()
        self.dropDown = OptionMenu(self.window, self.clicked, *self.options)
        self.dropDown.pack()
        self.bindings()
        self.value = ""
    
    def setLabel(self, string):
        self.imp.config(text = string)
        self.window.mainloop()
    
    def bindings(self):
        self.window.bind('<Return>', lambda event: self.update())
        
    def update(self):
        self.value = self.clicked.get()
        self.window.quit()
        #Responsible for retrieving any changes to the dropdown.
        
    def getValue(self):
        #print("value: ", self.value)
        return self.value
    
    def selfDestruct(self):
        self.window.destroy()
        
#bob = liveCatch()
#bob.setRInput(" ha ( ( and & ^ || a & * implies -->  ) )  erye ")
#bob.setRInput(" (p andhd q) or ( not q andhd p )")
#bob.setRInput(")(")
#bob.setRInput("a and true")
#print(bob.getRInput())
#bob.packager()
#print(bob.getPLock())
#print(bob.getProperVisual())
#print(bob.packager())