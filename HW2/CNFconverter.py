import sys

""" READ THE INPUT FILE """
inputFile = open(sys.argv[2])
length = 0
i = 0
sentences = []
sentences_CNF = []
for line in inputFile:
    i = i+1
    spl = line.strip().split('\n')
    if i==1:       
        length = int(spl[0])
    else:
        sentences.append(eval(spl[0]))
        if i==(length+1):
            break
inputFile.close()

""" DEF A FUNCTION TO DEEPCOPY A LIST"""
def copylist(x):
    y = []
    if isinstance(x,list):
        for object in x:
            y.append(copylist(object))
    else:
        y = x
    return y

""" DEF A FUNCTION TO REMOVE IFF IN SENTENCES"""
def remove_iff(x):
    i = 1
    if x[0]=="iff":
        a = copylist(x[1])
        b = copylist(x[2])
        x = ["and",["implies",x[1],x[2]],["implies",b,a]]
        x = remove_iff(x)
    else:
        for object in x[1::]:
            if isinstance(object,list):
                x[i]=remove_iff(object)
            i = i+1
    return x

""" DEF A FUNCTION TO REMOVE IMPLIES IN SENTENCES"""
def remove_implies(x):
    i = 1
    if x[0]=="implies":
        x = ["or",["not",x[1]],x[2]]
        x = remove_implies(x)
    else:
        for object in x[1::]:
            if isinstance(object,list):
                x[i]=remove_implies(object)
            i = i+1
    return x

""" DEF A FUNCTION TO PUSH NEGATION DOWNWARDS/REMOVE DOUBLE NEGATION"""
def down_neg(x):
    i = 1
    if x[0]=="not" and isinstance(x[1],list):
        y = x[1]
        if y[0]=="not":
            x = y[1]
        elif y[0]=="and":
            y[0] = "or"
            for object in y[1::]:
                y[i] = ["not",object]
                i = i+1
            x = y
        elif y[0]=="or":
            y[0] = "and"
            for object in y[1::]:
                y[i] = ["not",object]
                i = i+1
            x = y 
        x = down_neg(x)
    else:
        for object in x[1::]:
            if isinstance(object,list):
                x[i] = down_neg(object)
            i = i+1 
    return x

""" DEF A FUNCTION TO PUSH DISJUNCS DOWNWARD/ELIMINATE # OF DISJUNCS"""
def down_disjun(x):
    i = 1
    if x[0]=="or":
        while i<len(x):
            object = x[i]
            if isinstance(object,list):
                if object[0]=="or":
                    x.extend(object[1::])
                    x.remove(object)
                    i = i-1
                elif object[0]=="and":
                    y=["and"]
                    x.remove(object)
                    for item in object[1::]:
                        z=["or",item,x]
                        y.append(z)
                    x=down_disjun(y)
                    break
            i = i+1
    else:
        for object in x[1::]:
            if isinstance(object,list):
                x[i] = down_disjun(object)
            i = i+1 
    return x

""" DEF A FUNCTION TO ELIMINATE CONJUNCTIONS"""
def down_conjun(x):
    i = 1
    if x[0]=="and":
        while i<len(x):
            object = x[i]
            if isinstance(object,list):
                if object[0]=="and":
                    x.extend(object[1::])
                    x.remove(object)
                    i = i-1
            i = i+1
    else:
        for object in x[1::]:
            if isinstance(object,list):
                x[i] = down_conjun(object)
            i = i+1 
    return x

""" DEF A FUNCTION TO ELIMINATE # OF SAME ELEMENTS"""
def down_same(x):
    change = 0
    change1 = 0
    if isinstance(x,list):
        i = 1
        if x[0]=="and" or x[0]=="or":
            while i<len(x):
                object = x[i]
                if x.count(object)>1:
                    x.remove(object)
                    i = i-1
                    change = 1
                i = i+1
            i = 1
            while i<len(x):
                if isinstance(x[i],list):                    
                    j = i+1
                    while j<len(x):
                        if isinstance(x[j],list):
                            match = 1
                            for object in x[i]:
                                if object not in x[j]:
                                    match = 0
                            for object in x[j]:
                                if object not in x[i]:
                                    match = 0
                            if match==1:
                                x.pop(j)
                                j = j-1
                        j = j+1
                i = i+1                    
            i = 1
            while i<len(x):
                if isinstance(x[i],list):
                    (x[i], change1) = down_same(x[i])
                    change = change or change1
                i = i+1
            if len(x)==2:
                x=x[1]
                change = 1
    return (x, change)

""" ELIMINATE THE CLAUSES WITH SAME ELEMENTS IN DIFFERENT ORDER"""
""" CONVERT SENTENCES INTO CNF"""
for object in sentences:
    object = remove_iff(object)
    object = remove_implies(object)
    object = down_neg(object)
    object = down_disjun(object)
    object = down_conjun(object)
    change = 1
    #print object
    while change ==1:
        (object, change) = down_same(object)
#        print object,change
    if isinstance(object,str):
        object = '"'+object+'"'
    sentences_CNF.append(object)

""" WRITE TO THE OUTPUT FILE """
output = open("sentences_CNF.txt",'w')
for object in sentences_CNF:
    output.write((str(object))+"\n")
output.close()
