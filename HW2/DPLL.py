import sys

""" READ THE INPUT FILE """
inputFile = open(sys.argv[2])
length = 0
i = 0
CNF_sentences = []
CNF_satisfiability = []
for line in inputFile:
    i = i+1
    spl = line.strip().split('\n')
    if i==1:       
        length = int(spl[0])
    else:
        CNF_sentences.append(eval(spl[0]))
        if i==(length+1):
            break
inputFile.close()
        
""" DEF A FUNCTION TO TRANSE CNF CLAUSES INTO PROPER FORM, IT ALSO INITIALIZE
THE LIST OF THE PROPOSITION SYMBOLS IN CLAUSES(SYMBOL REPRESENTED BY KEY: IF
IT EXIST AS POSITIVE FORM, VALUE IS 1; NEGATIVE FORM, VALUE IS 0; BOTH FORM, 2)"""
def trans_clause(clause,symbols):
    clause_new = []
    if clause[0]=="or":
        for item in clause[1::]:
            if not(symbols.has_key(item[-1])):
                symbols[item[-1]] = 2 - len(item)
            elif (symbols[item[-1]] != 2 - len(item)):
                symbols[item[-1]] = 2
            if isinstance(item,list):
                clause_new.append('-'+item[1])
            else:
                clause_new.append(item)
    else:
        if not(symbols.has_key(clause[-1])):
            symbols[clause[-1]] = 2 - len(clause)
        elif (symbols[clause[-1]] != 2 - len(clause)):
            symbols[clause[-1]] = 2
        if isinstance(clause,list)==0:
            clause_new=[clause]
        else:
            clause_new=['-'+clause[1]]
    return (clause_new,symbols)

""" DEF A FUNCTION TO IMPLYMENT PURE SYMBOL HURESTIC"""
def pure_symbol(clauses, symbols, model):
    for symbol in symbols:
        if symbols[symbol]==2:
            continue
        if symbols[symbol]==0:
            model.append(symbol+'=false')
        else:
            model.append(symbol+'=true')
        i=0
        symbol_n = '-'+symbol
        while i<len(clauses):
            if symbol in clauses[i] or symbol_n in clauses[i]:
                clauses.pop(i)
                i = i -1
            i = i+1
        del symbols[symbol]
        return True
    return False

""" DEF A FUNCTION TO IMPLYMENT UNIT CLAUSE HURESTIC"""
def unit_clause(clauses, symbols, model):
    change = False
    for clause in clauses:
        if len(clause)==1:
            symbol = clause[0]
            change = True
            break
    if change:
        if len(symbol)==2:
            model.append(symbol[-1]+'=false')
            symbol_n = symbol[-1]
        else:
            model.append(symbol[-1]+'=true')
            symbol_n = '-'+symbol
        del symbols[symbol[-1]]
        i = 0
        while i<len(clauses):
            if symbol in clauses[i]:
                clauses.pop(i)
                i = i-1
            elif symbol_n in clauses[i]:
                clauses[i].remove(symbol_n)
            i = i+1
    return change

""" DEF A FUNCTION TO IMPLEMENT SLITTING RULE"""
def splitting_rule(clauses, symbols, model, value):
    for symbol in symbols:
        symbol_n = '-'+symbol
        model.append(symbol+'='+value)
        del symbols[symbol]
        i = 0
        while i<len(clauses):
            if value=='true':
                if symbol in clauses[i]:
                    clauses.pop(i)
                    i = i-1
                elif symbol_n in clauses[i]:
                    clauses[i].remove(symbol_n)
            else:
                if symbol_n in clauses[i]:
                    clauses.pop(i)
                    i = i-1
                elif symbol in clauses[i]:
                    clauses[i].remove(symbol)
            i = i+1
        return (clauses, symbols, model)

""" DEF A FUNCTION TO IMPLEMENT DPLL ALG"""
def DPLL(clauses, symbols, model):
    if clauses==[]:
        if symbols!={}:
            for symbol in symbols:
                model.append(symbol+'=true')
            symbols.clear()
        return True
    for clause in clauses:
        if clause==[]:
            return False
    if pure_symbol(clauses, symbols, model)==True:
        return DPLL(clauses, symbols, model)
    if unit_clause(clauses, symbols, model)==True:
        return DPLL(clauses, symbols, model)
    symbols0 = symbols.copy()
    model0 = model[:]
    clauses0 = []
    for clause in clauses:
        clauses0.append(clause[:])
    splitting_rule(clauses, symbols, model, 'true')
    splitting_rule(clauses0, symbols0, model0, 'false')
    value = DPLL(clauses, symbols, model)
    if value:
        return value
    else:
        (clauses, symbols) = (clauses0, symbols0)
        del model[:]
        for object in model0:
            model.append(object)
        return DPLL(clauses, symbols, model)
            
""" DEF A FUNCTION TO CHECK WHETHER THE SENTENCE IS SATISFIABLE & RETURN MODEL"""
def DPLL_SATISFIABLE(s):
    clauses = []
    symbols = {}
    model = []
    if s[0]=="and":
        for object in s[1::]:
            (clause,symbols)=trans_clause(object,symbols)
            clauses.append(clause)
    else:
        (clause,symbols)=trans_clause(s,symbols)
        clauses = [clause]
    if DPLL(clauses, symbols, model)==1:
        model.insert(0,'true')
    else:
        model = ['false']
    return model

""" CONVERT SENTENCES INTO CNF"""
for object in CNF_sentences:
    object = DPLL_SATISFIABLE(object)
    CNF_satisfiability.append(object)

""" WRITE TO THE OUTPUT FILE """
output = open("CNF_satisfiability.txt",'w')
for object in CNF_satisfiability:
    output.write((str(object)).replace('\'','"')+"\n")
output.close()
