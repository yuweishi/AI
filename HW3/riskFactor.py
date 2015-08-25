import sys

""" DEF AFUNCTION TO REFORMAT INPUT DATA"""
def trans(spl1,j,object):
    if j==0 or j=='income':
        if int(object)>75000:
            spl1[j] = 3
        else:
            spl1[j] =int((int(object)-1)/25000)
    if object=='yes':
        spl1[j] = 1
    elif object=='no':
        spl1[j] = 0
    elif object=='underweight':
        spl1[j] = 0
    elif object=='normal':
        spl1[j] = 1
    elif object=='overweight':
        spl1[j] = 2
    elif object=='obese':
        spl1[j] = 3

""" READ THE INPUT QUERY"""
inputFile = open(sys.argv[2])
i = 0
query = []
for line in inputFile:
    i = i+1
    spl = line.strip().split('\n')
    if i==1:
        n = int(spl[0])
    else:
        spl = eval(spl[0])
        for item in spl:
            for (key,value) in item.items():
                trans(item,key,value)
        query.append(spl)
        if i==(n+1):
            break
inputFile.close()

""" READ THE INPUT DATA"""
inputFile = open(sys.argv[4])
i = 0
data = []
for line in inputFile:
    i = i+1
    spl = line.strip().split('\n')
    if i>1:
        spl1 = spl[0].split()
        for j,object in enumerate(spl1):
            trans(spl1,j,object)
        data.append(spl1)
        if i==(10001):
            break
inputFile.close()

""" DEF A FUNCTION TO CALCULATE PROBABILITY USING COUNT DATA"""
def pro(num):
    if isinstance(num[0],list):
        for i in range(len(num)):
            pro(num[i])
    else:
        sum = 0
        for item in num:
            sum = sum+item
        for i in range(len(num)):
            num[i] = float(num[i])/sum
    return num

""" CREATE THE CPT TABLE"""
cpt = {}
income = [0,0,0,0]
exe = [['income'],[[0,0] for i in range(4)]]
smoke = [['income'],[[0,0] for i in range(4)]]
bmi = [['income','exercise'],[[[0,0,0,0] for i in range(2)] for j in range(4)]]
bp = [['income','exercise','smoke'],[[[[0,0],[0,0]] for i in range(2)] for j in range(4)]]
cho = [['income','exercise','smoke'],[[[[0,0],[0,0]] for i in range(2)] for j in range(4)]]
dia = [['bmi'],[[0,0] for i in range(4)]]
angina = [['bmi','bp','cholesterol'],[[[[0,0],[0,0]] for i in range(2)] for j in range(4)]]
attack = [['bmi','bp','cholesterol'],[[[[0,0],[0,0]] for i in range(2)] for j in range(4)]]
stroke = [['bmi','bp','cholesterol'],[[[[0,0],[0,0]] for i in range(2)] for j in range(4)]]
for i in data:
    income[i[0]] += 1
    exe[1][i[0]][i[1]] += 1
    smoke[1][i[0]][i[2]] += 1
    bmi[1][i[0]][i[1]][i[3]] +=1
    bp[1][i[0]][i[1]][i[2]][i[4]] +=1
    cho[1][i[0]][i[1]][i[2]][i[5]] +=1
    dia[1][i[3]][i[9]] += 1
    angina[1][i[3]][i[4]][i[5]][i[6]] +=1
    attack[1][i[3]][i[4]][i[5]][i[7]] +=1
    stroke[1][i[3]][i[4]][i[5]][i[8]] +=1
cpt['income'] = [pro(income)]
cpt['exercise'] = [exe[0],pro(exe[1])]
cpt['smoke'] = [smoke[0],pro(smoke[1])]
cpt['bmi'] = [bmi[0],pro(bmi[1])]
cpt['bp'] = [bp[0],pro(bp[1])]
cpt['cholesterol'] = [cho[0],pro(cho[1])]
cpt['diabetes'] = [dia[0],pro(dia[1])]
cpt['angina'] = [angina[0],pro(angina[1])]
cpt['attack'] = [attack[0],pro(attack[1])]
cpt['stroke'] = [stroke[0],pro(stroke[1])]

""" DEF A FUNCTION TO CALCULATE THE PROBABILITY OF A SINGLE BRANCH"""
def cal(d):
    product = 1
    for (key,value) in d.items():
        if key=='income':
            pcond = cpt[key][0][value]
        else:
            p = cpt[key][0]
            pcond = cpt[key][1]
            for item in p:
                i = d[item]
                pcond = pcond[i]
            pcond = pcond[value]            
        product = product*pcond
    return product

"""DEF A FUNCTION TO IMPLEMENT ENUMERATE ALL ALGORITHM"""
def enum(v, dictionary):
    if len(dictionary)==0:
        return 1
    elif len(v)==0:
        return cal(dictionary)
    else:
        vnew = v[:]
        Y = vnew.pop(0)
        if Y in dictionary:
            return enum(vnew,dictionary)
        else:
            summary = 0
            if Y=='income' or Y=='bmi':
                for i in range(4):
                    dictnew = dictionary.copy()
                    dictnew[Y] = i
                    summary += enum(vnew,dictnew)
                    
            else:
                for i in range(2):
                    dictnew = dictionary.copy()
                    dictnew[Y] = i
                    summary += enum(vnew,dictnew)                    
            return summary

""" DEF A FUNCTION TO OBTAIN THE VARS"""
def var(dictionary):
    v = []
    for (key,value) in dictionary.items():
        v.append(key)
    i = 0
    while i<len(v):
        if v[i]!='income':
            new = cpt[v[i]][0]
            for item in new:
                if item not in v:
                    v.append(item)
        i +=1
    return v

""" USE CPT TO SOLVE THE QUERY"""
solution = []
for object in query:
    dict1 = dict(object[0].items()+object[1].items())
    dict2 = object[1]
    vars1 = var(dict1)
    vars2 = var(dict2)
    ans = enum(vars1,dict1)/enum(vars2,dict2)
    solution.append(("%.4f" % ans))

""" WRITE TO THE OUTPUT FILE """
output = open("riskFactor.txt",'w')
for i,object in enumerate(solution):
    output.write((str(object))+"\n")
output.close()
