import sys
import csv
import math

reader = csv.reader(file(sys.argv[1],'rU'))  
classIndex = int(sys.argv[2])
table = list(reader)
a = list()


if 'ReviewCount' in table[0]:
    t = table[0].index('ReviewCount')
    temp = list([row[t] for row in table[1:]])
    temp = map(int, temp)
    temp.sort()
    upper = temp[len(temp)/4]
    lower = temp[int(len(temp)*.75)]
    for row in table[1:]:
        row[t] = int(row[t])
        if row[t] <= upper:
            row[t] = 'low'
        elif row[t] >= lower:
            row[t] = 'high'
        else:
            row[t] = 'med'
            
if 'Longitude' in table[0]:
    t = table[0].index('Longitude')
    temp = list([row[t] for row in table[1:]])
    temp = map(float, temp)
    temp.sort()
    upper = temp[len(temp)/4]
    lower = temp[len(temp)*3/4]
    for row in table[1:]:
        row[t] = float(row[t])
        if row[t] <= upper:
            row[t] = 'low'
        elif row[t] >= lower:
            row[t] = 'high'
        else:
            row[t] = 'med'

if 'Latitude' in table[0]:
    t = table[0].index('Latitude')
    temp = list([row[t] for row in table[1:]])
    temp = map(float, temp)
    temp.sort()
    upper = temp[len(temp)/4]
    lower = temp[len(temp)*3/4]
    for row in table[1:]:
        row[t] = float(row[t])
        if row[t] <= upper:
            row[t] = 'low'
        elif row[t] >= lower:
            row[t] = 'high'
        else:
            row[t] = 'med'

 

max_att = ''
max_fea = ''
max_score = 0

class_label = list(set([row[classIndex] for row in table[1:]]))

if str(sys.argv[3]) == 'C':
    x = 0
    a = list()
    dictionary = {}
    for i in class_label:
        dictionary[i] = list()

    for row in table[1:]:
        dictionary[row[classIndex]].append(list(row))

    while x < len(table[0]):
        if x == classIndex:
            x += 1
            continue
        temp = set([row[x] for row in table[1:]])
        for i in temp:
            f0 = list()
            f1 = list()
            expect0 = list()
            expect1 = list()
            for j in dictionary:
                k = [row[x] for row in dictionary[j]]
                f0.append(len(k) - k.count(i))
                f1.append(k.count(i))
            j = 0
            t1 = sum(f0)
            t2 = sum(f1)
            s = t1 + t2
            while j < len(f0):
                expect0.append(float(t1*(f0[j]+f1[j]))/s)
                expect1.append(float(t2*(f0[j]+f1[j]))/s)
                j +=1
             #compute chi-square from two lists...
            j = 0
            chi = 0
            while j < len(f0):
                chi += float((f0[j] - expect0[j])*(f0[j] - expect0[j]))/expect0[j]
                chi += float((f1[j] - expect1[j])*(f1[j] - expect1[j]))/expect1[j]
                j+=1
            if chi > max_score:
                max_att = table[0][x]
                max_fea = i
                max_score = chi
            tu = (chi,table[0][x], i)
            a.append(tu)
        x += 1

    print "Chi-Square, max feature=<"+max_att+','+max_fea+'>, max_score='+"%.2f" %max_score
elif str(sys.argv[3]) == 'I':
    class_list = list(set([row[classIndex] for row in table[1:]]))
    EntropyS = 0
    for i in class_list:
        temp = float([row[classIndex] for row in table[1:]].count(i))/len([row[classIndex] for row in table[1:]])
        EntropyS += temp*math.log(temp,2)
    EntropyS = EntropyS*-1
    x = 0
    while x < len(table[0]):
        if x == classIndex:
            x += 1
            continue
        temp = list(set([row[x] for row in table[1:]]))
        for i in temp:
            dictionary = {}
            dictionary[0] = list()
            dictionary[1] = list()
            for row in table:
                if row[x] == i:
                    dictionary[1].append(row)
                else:
                    dictionary[0].append(row)
            class_label = list(set([row[classIndex] for row in table[1:]]))
            e0 = 0
            e1 = 0
            t = [row[classIndex] for row in dictionary[1]]
            for j in class_label:
                temp = float(t.count(j))/len(t)
                if temp != 0:
                    e1 += temp*math.log(temp,2)
            e1 *= -1
            t = [row[classIndex] for row in dictionary[0]]
            for j in class_label:
                temp = float(t.count(j))/len(t)
                if temp != 0:
                    e0 += temp*math.log(temp,2)
            e0 *= -1
            t = [row[classIndex] for row in table[1:]]
            Gain = EntropyS - float(len(dictionary[0]))/len(table)*e0 - float(len(dictionary[1]))/len(table)*e1
            if Gain > max_score:
                max_score = Gain
                max_att = table[0][x]
                max_fea = i
            tu = (Gain, table[0][x], i)
            a.append(tu)
        x += 1
    print "Information-Gain, max feature=<"+max_att+','+max_fea+'>, max_score='+"%.2f" %max_score
                
#print table[0][int(sys.argv[2])]
#x = 0
#a.sort()
#while x < 10:
#    print a[len(a)-1-x]
#    x+=1










