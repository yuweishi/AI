import sys

""" READ THE INPUT FILE """
inputFile = open(sys.argv[2])
n = 0
k = 0
i = 0
diseases = []
patients = []
for line in inputFile:
    i = i+1
    spl = line.strip().split('\n')
    if i==1:
        n = int((spl[0].split())[0])
        k = int((spl[0].split())[1])
    elif i<=4*n+1:
        if (i-2)%4==0:
            diseases.append([spl[0].split()])
        else:
            diseases[(i-2)/4].append(eval(spl[0]))
    else:
        if (i-2-4*n)%n==0:
            patients.append([eval(spl[0])])
        else:
            patients[(i-2-4*n)/n].append(eval(spl[0]))
        if i==(n*(4+k)+1):
            break
inputFile.close()

""" SOLVE QUESTION 1"""
def solve1(p,d):
    dpos = float(d[0][2])
    dneg = 1-float(d[0][2])
    for i,item in enumerate(p):
        if item=='T':
            dpos = dpos*d[2][i]
            dneg = dneg*d[3][i]
        elif item=='F':
            dpos = dpos*(1-d[2][i])
            dneg = dneg*(1-d[3][i])
    prob = dpos/(dpos+dneg)
    return prob

""" SOLVE QUESTION 2"""
def solve2(p,d,prob):
    dpos1 = float(prob)
    dneg1 = 1-dpos1
    dpos2 = dpos1
    dneg2 = dneg1
    for i,item in enumerate(p):
        if item=='U':
            probt = d[2][i]/(d[2][i]+d[3][i])
            probf = (1-d[2][i])/(2-d[2][i]-d[3][i])
            if probt>probf:
                dpos2 = dpos2*d[2][i]
                dneg2 = dneg2*d[3][i]
                dpos1 = dpos1*(1-d[2][i])
                dneg1 = dneg1*(1-d[3][i])
            else:
                dpos1 = dpos1*d[2][i]
                dneg1 = dneg1*d[3][i]
                dpos2 = dpos2*(1-d[2][i])
                dneg2 = dneg2*(1-d[3][i])
    prob1 = dpos1/(dpos1+dneg1)
    prob2 = dpos2/(dpos2+dneg2)
    return [("%.4f" % prob1),("%.4f" % prob2)]

""" SOLVE QUESTION 3"""
def solve3(p,d):
    fmin = 'none'
    fmax = 'none'
    vmin = 'N'
    vmax = 'N'
    pmin = 1
    pmax = 0
    for i,item in enumerate(p):
        if item=='U':
            probt = d[2][i]/(d[2][i]+d[3][i])
            probf = (1-d[2][i])/(2-d[2][i]-d[3][i])
            com = [fmin,fmax,d[1][i]]
            com.sort()
            if probt>probf:
                if probt>pmax or (probt==pmax and com.index(d[1][i])<com.index(fmax)):
                    pmax = probt
                    vmax = 'T'
                    fmax = d[1][i]
                if probf<pmin or (probf==pmin and com.index(d[1][i])<com.index(fmin)):
                    pmin = probf
                    vmin = 'F'
                    fmin = d[1][i]
            else:
                if probf>pmax or (probf==pmax and com.index(d[1][i])<com.index(fmax)):
                    pmax = probf
                    vmax = 'F'
                    fmax = d[1][i]
                if probt<pmin or (probt==pmin and com.index(d[1][i])<com.index(fmin)):
                    pmin = probt
                    vmin = 'T'
                    fmin = d[1][i]
    return [fmax,vmax,fmin,vmin]

""" SOLVE ALL PATIENTS' PROBLEMS USING ITERATION"""
ans = []
i = 0
while i<k:
    patient = patients[i]
    j = 0
    q1 = {}
    q2 = {}
    q3 = {}
    while j<n:
        disease = diseases[j]
        p = patient[j]
        name = disease[0][0]
        prob = solve1(p,disease)
        q1[name] = ("%.4f" % prob)
        q2[name] = solve2(p,disease,prob)
        q3[name] = solve3(p,disease)
        j = j+1
    ans.append([q1,q2,q3])
    i = i+1

""" WRITE TO THE OUTPUT FILE """
name = (sys.argv[2].split('.txt')[0]).split('/')[-1]
output = open(name+"_inference.txt",'w')
for i,object in enumerate(ans):
    output.write('Patient-'+str(i+1)+':\n')
    for item in object:
        output.write((str(item))+"\n")
output.close()
