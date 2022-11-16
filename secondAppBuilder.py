import tkinter as tk
from tkinter import ttk
#from tkinter import Canvas
from functools import partial
import random
import string
import AppHelper

keyLetter = ["t", "f", "v"]
eqString = ['', '']
eqStringIndex = 0
propList = []
logEqQ= False
properVis = []
helper = AppHelper.liveCatch()
#One thing to do: Index of button insertion/using keys/buttons on the same entry. 
class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title('Logic Table Generator')
        self.frame = tk.Frame(self)
        self.geometry('600x400+50+50')
        
        self.proceed = False
        self.rowconfigure(0, minsize=50, weight=1)
        self.columnconfigure([0, 1, 2], minsize=50, weight=1)
        self.entryGuy = tk.Entry(self);

        # set up variable
        self.option_var = tk.StringVar(self)

        # create widget
        self.create_wigets()
        
        self.bindings()

    def create_wigets(self):
        self.entryGuy = tk.Entry(master = self);
        self.entryGuy.grid(row = 0, column =2, sticky = "nsew")
        #There's probably a much more efficient way to write this portion. Will investigate
        #if I have a little more time. 
        btn_or = tk.Button(master = self, text = "∨", command= partial(self.stringAdd,"∨ "))
        btn_or.grid(row=1, column=0, sticky="nsew")

        btn_xOr = tk.Button(master= self, text = "⊕", command=partial(self.stringAdd,"⊕ "))
        btn_xOr.grid(row=1, column=1, sticky="nsew")

        btn_and = tk.Button(master=self, text="∧", command=partial(self.stringAdd,"∧ "))
        btn_and.grid(row=1, column=2, sticky="nsew")

        btn_logEq = tk.Button(master=self, text="≡", command=partial(self.logEq, "≡", ""))
        btn_logEq.grid(row=1, column=3, sticky="nsew")

        btn_neg = tk.Button(master=self, text="~", command=partial(self.stringAdd,"~"))
        btn_neg.grid(row=2, column=0, sticky="nsew")

        btn_true = tk.Button(master=self, text="t", command=partial(self.stringAdd,"T"))
        btn_true.grid(row=2, column=1, sticky="nsew")

        btn_false = tk.Button(master=self, text="f", command=partial(self.stringAdd,"F"))
        btn_false.grid(row=2, column=2, sticky="nsew")

        btn_lParen = tk.Button(master=self, text="(", command=partial(self.stringAdd, "( "))
        btn_lParen.grid(row=2, column=3, sticky="nsew")

        btn_rParen = tk.Button(master=self, text=")", command=partial(self.stringAdd,") "))
        btn_rParen.grid(row=3, column=0, sticky="nsew")
        
        btn_biConditional = tk.Button(master= self, text="↔", command=partial(self.stringAdd,"=="))
        btn_biConditional.grid(row = 3, column =1, sticky="nsew")
        
        self.imp = tk.Label(self)
        self.imp.grid(row = 0, column = 1, sticky = "nsew")
        
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
        self.bind('<Return>', lambda event: self.check())
        #<Control-Key-Return> if you want to be bougie.
        #For a more refined, user-based syntax catcher, replace <space> with <Return>
        #self.bind('<space>', lambda event: self.syntax())
        self.bind(')', lambda event: self.stringAdd(" "))
        self.bind('(', lambda event: self.stringAdd(" "))
    def syntax(self):
        global propList
        
        word = f" {self.entryGuy.get()}"
        #print("feeding: ", word)
        helper.setRInput(word)
        aa = helper.packager()
        if (aa != "" and helper.getContQ):
            print(aa, " at secondAppBuilder")
            if (iter(aa)):
                if (not str(aa)):
                    aa = ' '.join(aa)
                else:
                    aa = ''.join(aa)
            self.imp.config(text = aa)
        self.proceed = helper.getContQ()
        propList = helper.getVars()
        
    def check(self):
        global propList
        global properVis
        #global eqString
        self.syntax()
        eqString[eqStringIndex] = ''.join(helper.getPLock())
        #print("This is eqString: ", eqString)
        propList = helper.getVars()
        #print("this is propList: ", propList)
        properVis = helper.getProperVisual()
        if (self.proceed):
            self.destroy()
    
    def stringAdd(self, var=""):
        global properVis
        #global eqString
        #print(var)
        x = self.entryGuy.get()
        self.entryGuy.insert(len(x), var)
        properVis+=var
        eqString[eqStringIndex]+=var
        
    def logEq(self, var, comp):
        global eqStringIndex
        global logEqQ
        logEqQ = True
        eqStringIndex = 1
        #Will need to do some testing with how eqStringIndex influences the processes of AppHelper. 
        self.stringAdd(var, comp)
        
    def prop(self, var, bard = ""):#tr = ""
        global properVis
        global eqString
        if (not (var in propList) and not (var in keyLetter) and str(var)!='.'):
            propList.append(var)
            keyLetter.append(var)
        eqString[eqStringIndex]+=f"builder.get('{str(bard)}') "
        properVis+=bard
        self.entryGuy.insert(len(properVis), bard)
        self.update_drop_letter()

    def randLetter(self):
        #global keyLetter
        x = 't'
        while(x in keyLetter):
            x = random.choice(string.ascii_lowercase)
        self.prop(var = x, bard =x)
        return(x)
        
    #similar to the answer found on: https://stackoverflow.com/questions/28412496/updating-optionmenu-from-list
    def update_drop_letter(self):
        self.option_menu.destroy()
        self.option_menu = ttk.OptionMenu(
            self,
            self.option_var,
            "Variable list",
            *propList,
            command=partial(self.prop, self, self.option_var))
        self.option_menu.grid(row=3, column = 3, sticky = "nsew")



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
                #e = tk.Entry(self, width=20, fg='blue', font=('Arial', 16, 'bold'))
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
# bob = getInfo()
# prop = bob.getPropList()
# print(prop)