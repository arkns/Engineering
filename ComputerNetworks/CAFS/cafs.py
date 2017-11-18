import threading
import random
import time
import math
import matplotlib.pyplot as plt
import numpy as np

num_routers = 250
routers = []
router_range = 20
sender_index = 0
receiver_index = 0
visited = []
done = False
receive_status = False
rho=0.1


def plot_routers():
    unvisited_routers = [i.index for i in routers if i.index not in visited]
    print(unvisited_routers)
    plt.scatter(routers[sender_index].x, routers[sender_index].y, color='blue')
    plt.scatter(routers[receiver_index].x, routers[receiver_index].y, color='red')
    x = []
    y = []
    for item in unvisited_routers:
        if item != sender_index and item != receiver_index:
            x.append(routers[item].x)
            y.append(routers[item].y)
    plt.scatter(x, y, color=['black' for i in range(len(x))])
    x = []
    y = []
    for item in visited:
        if item != sender_index and item != receiver_index:
            x.append(routers[item].x)
            y.append(routers[item].y)
    plt.scatter(x, y, color=['green' for i in range(len(x))])
    x = []
    y = []
    for item in visited:
        x.append(routers[item].x)
        y.append(routers[item].y)
    plt.plot(x, y)
    if receive_status:
        x = [routers[visited[len(visited)-1]].x, routers[receiver_index].x]
        y = [routers[visited[len(visited)-1]].y, routers[receiver_index].y]
        plt.plot(x, y, color='red')
    plt.show()


def angle(j, i):
    ang1 = np.arctan2(routers[j].y, routers[j].x)
    ang2 = np.arctan2(routers[i].y, routers[i].x)
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))


def calculate_theta(i):
    theta = np.arccos( router_range/(2*distance_btw_routers(i, receiver_index)))
    return theta


def calculate_angles(n, s):
    angles = {}
    for item in n:
        angles[item] = (angle(item, s)/calculate_theta(s))
    return angles


def distance_btw_routers(router1, router2):
    return math.sqrt((routers[router1].x - routers[router2].x)**2 + (routers[router1].y - routers[router2].y)**2)


def energy_cost(n, d):
    costs = {}
    for item in n:
        costs[item] = router_range * d[item]
    return costs


def distance_cost(s, n):
    costs = {}
    for item in n:
        costs[item] = math.sqrt((routers[s].x - routers[item].x)**2 + (routers[s].y - routers[item].y)**2)
    return costs


def p_costs(s, n):
    costs = {}
    for item in n:
        costs[item] = 1 - distance_btw_routers(item, receiver_index)/distance_btw_routers(s, receiver_index)
    return costs


def least_cost(s, n):
    global dest
    cost = {}

    xi=routers[s].x
    yi=routers[s].y

    xdest=routers[dest].x
    ydest=routers[dest].y
    did=math.sqrt((xdest-xi)**2+(ydest-yi)**2)
    theta=math.acos(router_range/(2*did))
    while 1:
        for item in n:
            xj=routers[item].x
            yj=routers[item].y

            djd=math.sqrt((xdest-xj)**2+(ydest-yj)**2)
            dij=math.sqrt((xi-xj)**2+(yi-yj)**2)
            try:
                pij=(router_range-(did-djd)/did)/(2*router_range)
            except Exception:
                print(did,dest,s)

            ax=xj-xi
            ay=yj-yi
            bx=xdest-xi
            by=ydest-yi
            ab=ax*bx+ay*by
            alphaj=math.acos(ab/(dij*did))
            Aj=alphaj/theta
            Eij=dij**2/router_range**2
            try:
                cost[item] = (Eij*Aj*routers[item].congestion)/pij
            except Exception:
                print(pij,dest,s)
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
    def __init__(self, i, x, y, rho):
        threading.Thread.__init__(self)
        self.index = i
        self.x = x
        self.y = y
        self.buffer = []
        self.Sender = 0
        self.Receiver = 0
        self.neighbours = []
        self.congestion = rho

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
            if self.index != item.index and distance_btw_routers(self.index, item.index) <= 20:
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
                global receive_status
                receive_status = True
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
                        done =True
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
        routers.append(Router(i, random.randint(1, 99), random.randint(1, 99), random.uniform(0.3,0.7)))
    global sender_index, receiver_index, source, dest
    sender_index = random.randint(0, num_routers - 1)
    source = sender_index
    while 1:
        receiver_index = random.randint(0, num_routers - 1)
        if receiver_index != sender_index:
            dest = receiver_index
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
    print(visited)
    plot_routers()
main()
