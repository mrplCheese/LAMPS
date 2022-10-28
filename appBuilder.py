import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from functools import partial
import random
import string

keyLetter = ["t", "f", "v"]
eqString = ['', '']
eqStringIndex = 0
propList = []
logEqQ= False
properVis = []
#prime = True

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title('Logic Table Generator')
        self.frame = tk.Frame(self)
        self.geometry('600x400+50+50')

        self.rowconfigure(0, minsize=50, weight=1)
        self.columnconfigure([0, 1, 2], minsize=50, weight=1)


        # set up variable
        self.option_var = tk.StringVar(self)

        # create widget
        self.create_wigets()
        
        self.bindings()

    def create_wigets(self):
        global propList
        self.eq_label= tk.Label(master=self, text = "")
        self.eq_label.grid(row = 0, column =2, sticky = "nsew")

        btn_or = tk.Button(master = self, text = "∨", command=partial(self.stringAdd, "∨", "or "))
        btn_or.grid(row=1, column=0, sticky="nsew")

        btn_xOr = tk.Button(master= self, text = "⊕", command=partial(self.stringAdd, "⊕", "^"))
        btn_xOr.grid(row=1, column=1, sticky="nsew")

        btn_and = tk.Button(master=self, text="∧", command=partial(self.stringAdd, "∧", "and "))
        btn_and.grid(row=1, column=2, sticky="nsew")

        btn_logEq = tk.Button(master=self, text="≡", command=partial(self.logEq, "≡", ""))
        btn_logEq.grid(row=1, column=3, sticky="nsew")

        btn_neg = tk.Button(master=self, text="~", command=partial(self.stringAdd, "~", "not "))
        btn_neg.grid(row=2, column=0, sticky="nsew")

        btn_true = tk.Button(master=self, text="t", command=partial(self.stringAdd, "t", "True "))
        btn_true.grid(row=2, column=1, sticky="nsew")

        btn_false = tk.Button(master=self, text="f", command=partial(self.stringAdd, "f", "False "))
        btn_false.grid(row=2, column=2, sticky="nsew")

        btn_lParen = tk.Button(master=self, text="(", command=partial(self.stringAdd, "(", "("))
        btn_lParen.grid(row=2, column=3, sticky="nsew")

        btn_rParen = tk.Button(master=self, text=")", command=partial(self.stringAdd, ")", ")"))
        btn_rParen.grid(row=3, column=0, sticky="nsew")
        
        btn_biConditional = tk.Button(master= self, text="↔", command=partial(self.stringAdd, "↔", "=="))
        btn_biConditional.grid(row = 3, column =1, sticky="nsew")
        
#         drop_letter = tk.OptionMenu(root, clicked, propList[0], *propList, command=partial(prop, propList, var = "A") )
#         drop_letter.grid(row=3, column=1, sticky="nsew")
        # option menu
        self.option_menu = ttk.OptionMenu(
            self,
            self.option_var,
            "Variable list",
            *propList,
            command=partial(self.prop, self, self.option_var))

        self.option_menu.grid(row=3, column = 3, sticky = "nsew")
        
        btn_new_prop = ttk.Button(master=self, text= "new prop variable", command=self.randLetter)
        btn_new_prop.grid(row=3, column = 2, sticky = "nsew")
        
        i = 0
        while(i<=4):
            self.grid_columnconfigure(i, weight=1, uniform="vars")
            i+=1;
            
    def bindings(self):
        self.bind('<Return>', lambda event: self.destroy())
        
        self.bind('&', partial(self.stringAdd, "∧", "and "))
        
        self.bind('^', partial(self.stringAdd, "∧", "and "))
        
        self.bind('|', partial(self.stringAdd, "∨", "or "))
        
        self.bind('(', partial(self.stringAdd, "(", "("))
        
        self.bind(')', partial(self.stringAdd, ")", ")"))
        
        self.bind('+', partial(self.stringAdd, "⊕", "^"))
        
        self.bind('=', partial(self.logEq, "≡", ""))
        
        self.bind('~', partial(self.stringAdd, "~", "not "))
        
        self.bind('t', partial(self.stringAdd, "t", "True "))
        
        self.bind('f', partial(self.stringAdd, "f", "False "))
        
        self.letterSwipe()
        
        self.bind("<BackSpace>", self.backSpace)
        
        
    
    def stringAdd(self, var, comp, trash = ""):
        global eqString
        global eqStringIndex
        global properVis
        eqString[eqStringIndex]+=(comp)
        #print(eqString)
        self.eq_label["text"]+=var
        properVis+=var
        
    def backSpace(self):
        print("backspace is under construction.")
        
    def logEq(self, var, comp):
#         global logEqQ
        global eqStringIndex
        logEqQ = True
        eqStringIndex = 1
        self.stringAdd(var, comp)
        
    def prop(self, var, tr = "", bard = ""):
        #print("tr: ", tr)
        #print("bard: ", bard)
        global keyLetter
        global propList
        global eqString
        global eqStringIndex
        global properVis
        if (not (var in propList) and not (var in keyLetter) and str(var)!='.'):
            propList.append(var)
            #print("added (:")
            keyLetter.append(var)
            #print(var)
        eqString[eqStringIndex]+="builder.get('"+str(bard)+ "') "
        #print(eqString)
        self.eq_label["text"]+=bard
        properVis+=bard
    #     drop_letter["menu"] = propList
        self.update_drop_letter()
        #print(eqString)

    def randLetter(self):
        global keyLetter
        x = 't'
        while(x in keyLetter):
            x = random.choice(string.ascii_lowercase)
    #     btn_letter["text"] = x #is now futile.
        self.prop(var = x, bard =x)
        return(x)
        
    #similar to the answer found on: https://stackoverflow.com/questions/28412496/updating-optionmenu-from-list
    def update_drop_letter(self):
        self.option_menu.destroy()
#         print(propList)
        self.option_menu = ttk.OptionMenu(
            self,
            self.option_var,
            "Variable list",
            *propList,
            command=partial(self.prop, self, self.option_var))
        self.option_menu.grid(row=3, column = 3, sticky = "nsew")
        
    def letterSwipe(self):
        global keyLetter
                
class table(tk.Tk):
    def __init__(self, listy, logEq):
        super().__init__()
        self.Notebook = ttk.Notebook(self)
        self.Notebook.grid()
        self.frame1 = ttk.Frame(self.Notebook, width=600, height=400)
        self.frame2 = ttk.Frame(self.Notebook, width=600, height=400)
        self.frame3 = ttk.Frame(self.Notebook, width=600, height=400)
        self.Notebook.add(self.frame1, text='Truths')
        self.Notebook.add(self.frame2, text='Info')
        self.Notebook.add(self.frame3, text='circuits')
        self.listy = listy
        self.title('Logic Table')
        self.frame = tk.Frame(self)
        self.geometry('600x400+50+50')

        self.rowconfigure(0, minsize=50, weight=1)
        self.columnconfigure([0, 1, 2], minsize=50, weight=1)

        self.makeTable(self.frame1)
        
        
    def makeTable(self, frame):
        for i in (range(len(self.listy))):
            for j in (range(len(self.listy[0]))):
                e = tk.Entry(self, width=20, fg='blue', font=('Arial', 16, 'bold'))
                #e.insert('end', self.listy[i][j])
                #e.insert( 'end', self.listy[i][j])
                ttk.Label(frame, text = self.listy[i][j]).grid(row = i, column = j)

class getInfo():
    def getPropList(self):
        return propList
    def getEqString(self):
        return eqString
    def getProperVis(self):
        return properVis

# app = App()
# app.mainloop()
# 
# bob = getInfo()
# prop = bob.getPropList()
# print(prop)