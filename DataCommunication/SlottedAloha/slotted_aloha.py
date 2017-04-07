#defining slot as 2 seconds.
import time
import random
import _thread
n = 6
machine_active = [0 for i in range(n)]
#print(machine_active)
channel = []
def clear_channel(wait,hi):
    global channel
    if channel != [] :
        #print(channel)
        time.sleep(wait)
        channel = []
def exponential_backoff(machine_name,num_collisons):
    print(machine_name+" collided")
    delay = random.randint(0,2**num_collisons-1)
    print("Waiting {0} seconds".format(delay*2))
    time.sleep(delay*2)
def transmission(machine_name,index,start_time):
    #print(index)
    status = 0
    num_collisions = 0
    while status == 0:
        #print(channel)
        cur_time = time.time()
        if int(cur_time-start_time) % 2 == 0:
            if channel == []:
                channel.append(machine_name)
                print(channel)
                status = 1
            else:
                num_collisions += 1
                exponential_backoff(machine_name,num_collisions)
        else:
            time.sleep(1)
    machine_active[index] = 1
def main():
    _thread.start_new_thread(transmission,("Machine 1 ",0,time.time()))
    _thread.start_new_thread(transmission,("Machine 2 ",1,time.time()))
    _thread.start_new_thread(transmission,("Machine 3 ",2,time.time()))
    _thread.start_new_thread(transmission,("Machine 4 ",3,time.time()))
    _thread.start_new_thread(transmission,("Machine 5 ",4,time.time()))
    _thread.start_new_thread(transmission,("Machine 6 ",5,time.time()))
    while 1:
        _thread.start_new_thread(clear_channel,(0.05,0))
        time.sleep(0.005)
        if 0 in machine_active:
            continue
        else:
            break
    while 0 in machine_active :
        pass
s_time = time.time()
main()
e_time= time.time()
print(" Toatal time for transmission : ",end = ' ')
print(e_time-s_time)
