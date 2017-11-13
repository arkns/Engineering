import threading
import random
import time
import math

num_routers = 50
routers = []
router_range = 20
sender_index = 0
receiver_index = 0
visited = []
done = False
rho=0.7

def least_cost(s, n):
    cost = {}

    xi=routers[s].x
    yi=routers[s].y
    global dest
    xdest=routers[dest].x
    ydest=routers[dest].y
    did=math.sqrt((xdest-xi)**2+(ydest-yi)**2)
    theta=math.acos(20/(2*did))
    while 1:
        for item in n:
            xj=routers[item].x
            yj=routers[item].y

            djd=math.sqrt((xdest-xj)**2+(ydest-yj)**2)
            dij=math.sqrt((xi-xj)**2+(yi-yj)**2)
            pij=(did-djd)/did
            ax=xi-xj
            ay=yi-yj
            bx=xdest-xi
            by=ydest-yi
            ab=ax*bx+ay*by
            alphaj=math.acos(abs(ab/(dij*did)))
            Aj=alphaj/theta
            Eij=dij**2/400
            cost[item] = (Eij*Aj*rho)/pij
        if cost == {}:
            return -1
        ind = min(cost, key=cost.get)
        print(ind)
        print(visited)
        print(n)
        if ind in visited:
            del n[n.index(ind)]
            del cost[ind]
        else:
            #visited.append(ind)
            return ind


class Router(threading.Thread):
    def __init__(self, i, x, y):
        threading.Thread.__init__(self)
        self.index = i
        self.x = x
        self.y = y
        self.buffer = []
        self.Sender = 0
        self.Receiver = 0
        self.neighbours = []

    def set_as_sender(self):
        self.Sender = 1
        self.Receiver = 0

    def set_as_receiver(self):
        self.Receiver = 1
        self.Sender = 0

    def status(self):
        if self.Sender == 1:
            return "SENDER"
        elif self.Receiver == 1:
            return "RECEIVER"
        else:
            return "ROUTER"

    def find_neighbours(self):
        for item in routers:
            if self.index != item.index and abs(self.x - item.x) <= 20 and abs(self.y - item.y) <= 20:
                self.neighbours.append(item.index)

    def print_status(self):
        print("Router : {0} . pos : ({1} , {2}) , time : {3} , Type : {4}, Neighbours : {5}"
              .format(self.index, self.x, self.y, time.time(), self.status(), self.neighbours))

    def run(self):
        if self.Sender == 1:
            visited.append(self.index)
            if receiver_index in self.neighbours:
                routers[receiver_index].start()
                routers[receiver_index].buffer.extend(self.buffer)
                global done
                done = True
                print("Data received : {0} from Router {1} to Router {2}"
                      .format(routers[receiver_index].buffer, self.index, receiver_index))
            else:
                if routers[self.index].neighbours == []:
                    print("No Connectivity.")
                    done = True
                else:
                    current_index = least_cost(self.index, routers[self.index].neighbours)
                    if current_index == -1:
                        print("No connectivity.")
                    #del routers[self.index].neighbours[routers[self.index].neighbours.index(current_index)]
                    else:
                        self.Sender = 0
                        routers[current_index].Sender = 1
                        routers[current_index].buffer = self.buffer
                        print(" Data received : {0} from Router {1} to Router {2}"
                          .format(routers[current_index].buffer, self.index, current_index))
                        routers[current_index].start()


def main():
    print("Welcome.")
    for i in range(num_routers):
        routers.append(Router(i, random.randint(1, 99), random.randint(1, 99)))
    global sender_index, receiver_index, source, dest
    sender_index = random.randint(0, num_routers-1)
    source = sender_index

    while 1:
        receiver_index = random.randint(0, num_routers-1)
        if receiver_index != sender_index:
            dest=receiver_index
            break
    routers[sender_index].set_as_sender()
    routers[receiver_index].set_as_receiver()
    for item in routers:
        item.find_neighbours()
        item.print_status()
    if routers[sender_index].neighbours == [] or routers[receiver_index].neighbours == []:
        print("No Connectivity.")
        global done
        done = True
    if not done:
        routers[sender_index].buffer.append(random.randint(0, 1000))
        routers[sender_index].start()
    while not done:
        pass
main()
