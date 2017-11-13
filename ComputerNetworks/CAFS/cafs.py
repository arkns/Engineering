import threading
import random
import time
import math

num_routers = 50
routers = []
router_range = 35
sender_index = 0
receiver_index = 0
visited = []
done = False


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
    while 1:
        final_costs = {}
        distance = distance_cost(s, n)
        energy = energy_cost(n, distance)
        p_cost = p_costs(s, n)
        for item in n:
            final_costs[item] = energy[item]/p_cost[item]
        if final_costs == {}:
            return -1
        ind = min(final_costs, key=final_costs.get)
        print(ind)
        print(visited)
        print(n)
        if ind in visited:
            del n[n.index(ind)]
            #del distance[ind]
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
        routers.append(Router(i, random.randint(1, 99), random.randint(1, 99)))
    global sender_index, receiver_index
    sender_index = random.randint(0, num_routers-1)
    while 1:
        receiver_index = random.randint(0, num_routers-1)
        if receiver_index != sender_index:
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
