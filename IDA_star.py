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
                result.append((data["to"][index],data["arrivalhash"][index],data["price"][index],index))
        index += 1
    return result


def get_heristic(current, goal, data):
    large = Max_val
    index = 0
    #current is the goal
    if is_goal(current,goal):
        return 0
    #print current
    for airport in data["from"]:
    #same airport
        if airport == current[0]:
            large = min(large, data["price"][index])
        index += 1

    return large



data = read()

start = ("PEK",hash_time(20,12,0),0,-1)
goal = ("SIN",hash_time(21,24,0),0,-1)

#IDA* depth
depth = 3
#keep track of the paths
parent = {}
re = []

def search(root, total_cost, goal, data, cut_off, path):
    f = total_cost + get_heristic(root,goal,data)
    if f > cut_off:
        return f

    if is_goal(root, goal):
        one = [x for x in path]
        one.append(str(total_cost))
        re.append(one)
        return 0
    min_val = Max_val

    for succ in get_successors(root, data):
        path.append(succ[0]+":"+str(succ[3]))
        t = search(succ,int(succ[2])+total_cost,goal, data, cut_off, path)
        path.pop()
        if t==0:
            return 0
        if t<min_val:
            min_val = t
    return min_val

cut_off = get_heristic(start, goal, data)
while True:
    path = [start[0]]
    k = search(start, 0, goal, data, cut_off, path)
    #found
    if k==0:
        break
    #not found
    if k>=Max_val:
        break

    #update the cut_off value
    cut_off = k

elapsed = time.clock() - start_time
print "Time elapsed:", elapsed

i = 1
print "              Flight Expert"
for ele in re:
    start = ele[0]
    total = int(ele[-1])
    flights = [int(x.split(":")[1]) for x in ele[1:-1]]
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







