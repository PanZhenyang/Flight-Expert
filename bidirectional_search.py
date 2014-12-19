import time
start_time = time.clock()
#a max value for the price
Max_val = 1000000

#read data into a dic
def read():
    names = ["from","to","departuredate","departuretime","arrivaldate","arrivaltime","price","class","code","airline","departurehash","arrivalhash"]
    data = {}
    for n in names:
        f = open(n+".txt")
        array = []
        flag = "hash" in n or "price" in n
        for ele in f:
            if flag:
                array.append(int(ele.strip()))
            else:
                array.append(ele.strip())
        f.close()
        data[n] = array
    return data
    #print data["from"]

def hash_time(day, hour, minute):
    return (day*24+hour)*60+minute

#arrive to the destination no later than 12 hours
def is_goal(current, goal):
    return current[0]==goal[0] and abs(current[1]-goal[1])<=hash_time(2,0,0)

#judge if they are the same states: st2 > st1
def is_same_state(st1, st2):
    return st1[0]==st2[0] and st2[1]-st1[1]<=hash_time(2,0,0)

#return the price for a flight with id_
def cost(id_, data):
    return data["price"][id_]

#get the successors of the current state
#state airport, time, flight_cost, flight_id 
def get_successors(current, data):
    index = 0
    result = []
    for airport in data["from"]:
        #same airport
        if airport == current[0]:
            #flight could be connected from 30 mins to 2 days
            if data["departurehash"][index]-current[1]>hash_time(0,0,10) and data["departurehash"][index]-current[1]<hash_time(2,0,0):
                #print "add"
                result.append((data["to"][index],data["arrivalhash"][index],data["price"][index]+current[2],index))
        index += 1
    return result


#get the predecessors of the current state
#state airport, time, flight_cost, flight_id 
def get_predecessors(current, data):
    index = 0
    result = []
    for airport in data["to"]:
        #same airport
        if airport == current[0]:
            #print airport, current[0]
            #flight could be connected from 30 mins to 2 days
            if abs(current[1]-data["arrivalhash"][index])>hash_time(0,0,10) and current[1]-data["arrivalhash"][index]<hash_time(2,0,0):
                result.append((data["from"][index],data["departurehash"][index],data["price"][index]+current[2],index))
        index += 1
    return result

data = read()

start = ("PEK",hash_time(20,12,0),0,-1)
goal = ("SIN",hash_time(21,24,0),0,-1)


depth = 3
#keep track of the paths
parent_front = {}
parent_back = {}
#keep track of visited airport
visited = set()

re_front = start
re_back = goal

import heapq
front = []
back = []

#the combined result
re = []

visited.add(start[0])
visited.add(goal[0])

heapq.heappush(front,(start[2],start))
heapq.heappush(back,(goal[2],goal))

while len(front)!=0 and len(back)!=0:
    #flag
    found = False
    #from the front direction
    f = heapq.heappop(front)[1]
    if is_same_state(f, goal):
        re_front = f
        found = True
    if found:
        break
    
    for ele in back:
        if is_same_state(f, ele):
            re_front = f
            found = True
    if found:
        break

    for ele in get_successors(f, data):
        if ele not in visited:
            parent_front[ele] = f
            heapq.heappush(front,(ele[2],ele))
            visited.add(ele[0])

    #from the back direction
    b = heapq.heappop(back)[1]
    if is_same_state(start, b):
        re_back = b
        found = True
    if found:
        break
    
    for ele in front:
        if is_same_state(ele, b):
            re_back = b
            found = True
    if found:
        break

    for ele in get_predecessors(b, data):
        if ele not in visited:
            parent_back[ele] = f
            heapq.heappush(back,(ele[2],ele))
            visited.add(ele[0])

#backtrack      
while parent_back.has_key(re_back):
    re.insert(0,re_back)
    re_back = parent_back[re_back]  

     
while parent_front.has_key(re_front):
    re.append(re_front)
    re_front = parent_front[re_front]       


elapsed = time.clock() - start_time
print "Time elapsed:", elapsed


i = 1
print "              Flight Expert"
if len(re)==0:
    print "Not Found"
else:
    start = re[-1]
    total = int(re[0][2])
    flights = [int(x[3]) for x in re[::-1]]
    print "======================================"
    for f_id in flights:
        print "**********************************"
        print "Flight Infomation: ", str(i)
        print "From: ", str(data["from"][f_id])
        print "To: ", str(data["to"][f_id])
        print "Departure Date: ", str(data["departuredate"][f_id])
        print "Departure Time: ", str(data["departuretime"][f_id])
        print "Arrival Date: ", str(data["arrivaldate"][f_id])
        print "Arrival Time: ", str(data["arrivaltime"][f_id])
        print "Price: ", str(data["price"][f_id])
        print "Class: ", str(data["class"][f_id])
        print "Code: ", str(data["code"][f_id])
        print "Airline: ", str(data["airline"][f_id])
        print "**********************************"
        i += 1
    print "Total Cost: ", str(total)





