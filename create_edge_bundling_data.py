#    GoogleFormVis Creates a Visualisation with D3js of results of Google Form Surveys
#    Copyright (C) 2018  Edoardo Pasca
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import csv
import json

## unique elements in list
## https://www.peterbe.com/plog/uniqifiers-benchmark
def f4(seq): 
   # order preserving
   noDupes = []
   [noDupes.append(i) for i in seq if not noDupes.count(i)]
   return noDupes

head =  []
with open('SIRFUserPlatform.csv', 'r') as csvfile:
    read = csv.reader(csvfile)
    i = 0
    for row in read:
        head.append(row)
        
questions = [1,3,4,5,6,7,8]
all_result = {}
for question in questions:
    distribution = []
    with open('SIRFUserPlatform.csv', 'r') as csvfile:
        read = csv.reader(csvfile)
        for row in read:
            distribution.append(row[question].split(';'))
    
    # find the set of all answers and give a hash code
    answers = {}
    j = 1
    for i in range(1, len(distribution)):
        for ans in distribution[i]:
            if not ans in answers:
                answers[ans]= pow(len(distribution)-1,j)+1
                j+=1
                
           
    # one selection
    conn = []
    count = []
    for i in range(1, len(distribution)):
        if len(distribution[i]) == 1:
            #ans = distribution[i][0]
            #conn.append({'name' : ans, 'imports': [ans], 'id': answers[ans]})
            #count.append([answers[ans], ans, [ans] ])
            pass
        else:
            val = 0
            for l in range(len(distribution[i])):
                a = distribution[i].copy()
                b = a.pop(l)
                a.sort()
                for ans in a:
                    val += answers[ans]
                count.append([val, b, a])
                c = {'name' : b, 'imports':a, 'id':val}
                conn.append(c)   
                
    
    trans = list(map(list, zip(*count)))
    
    # count the number of repetitions
    sizes = {}
    a = list(set(trans[0]))
    for i in range(len(a)):
        sizes[a[i]] = trans[0].count(a[i])
        
    for i in range(len(conn)):
        conn[i]['size'] = sizes[conn[i]['id']]
    
    
    filename = "{}.json".format(head[0][question].replace(" ","_").strip("?"))
    # remove duplicates from the connlist and save to file
    json.dump(f4(conn), open(filename ,"w") )
    