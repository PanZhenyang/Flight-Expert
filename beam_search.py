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
    #print current[0]==goal[0] and abs(current[1]-goal[1])<hash_time(0,12,0)
    #print "a", abs(current[1]-goal[1]), hash_time(0,12,0), current[0], goal[0]
    return current[0]==goal[0] and abs(current[1]-goal[1])<=hash_time(2,0,0)

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
                result.append((data["to"][index],data["arrivalhash"][index],data["price"][index]+current[2],index))
        index += 1
    return result

data = read()

#initial state: ("PEK",hash_time(20,12,0))
start = ("PEK",hash_time(20,12,0),0,-1)
goal = ("SIN",hash_time(21,24,0),0,-1)

#IDA* depth
depth = 3
#keep track of the paths
parent = {}
re = []


#print len(succ)

#get the successors of the initial state
succ = get_successors(start, data)
#randomly select the 10 successors
import random
size_ = 10

init_state = []
size_ = min(size_, len(succ))
for i in xrange(size_):
    try:
        rd_index =  random.randint(i, len(succ))
        succ[i], succ[rd_index] = succ[rd_index], succ[i]
        init_state.append(succ[i])
    except:
        continue


#beam search
next_state = [x for x in init_state]

#to avoid the duplicate visit of the airport
explored = set()
#to record the flight path
parent = {}

explored.add(start[0])

for ele in next_state:
    parent[ele] = start
    explored.add(ele[0])

max_hop = 3
last = start
hop = 0
while True:
    temp = []
    for x in next_state:
        for y in get_successors(x, data):
            if y[0] not in explored:
                parent[y] = x
                temp.append(y)


    temp = sorted(temp,key=lambda x: x[2])
    next_state = temp[:size_]

    f = True
    for ele in next_state:
        if is_goal(ele,goal):
            last = ele
            f = False
            break
        explored.add(ele[0])
    hop += 1

    if not f:
        break

    if hop>=max_hop:
        break

while parent.has_key(last):
    re.append(last)
    last = parent[last]

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





