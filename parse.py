data = open("flight.inst")
out = [[] for i in range(13)]

i = 1
for ele in data:
    array = ele.split(")(")
    j = 0
    l = len(array)
    for k in array:
        if j!=0:
            if j!= l-1:
                if "airline" not in k:
                    #print k.split(" ")[-1]
                    out[j].append(k.split(" ")[-1])
                else:
                    #print k.replace("airline ","")
                    out[j].append(k.replace("airline ",""))
            else:
                #print k.split(" ")[-1].split(")")[0]
                out[j].append(k.split(" ")[-1].split(")")[0])
            
        j += 1
        
    i+=1

i = 0
names = ["from","to","departuredate","departuretime","arrivaldate","arrivaltime","price","class","code","airline","departurehash","arrivalhash"]
for l in out:
    if i!=0:
        f = open(names[i-1]+".txt",'w')
        for k in l:
            f.write(k+"\n")
        f.close()
    i += 1
    
    
    
    
