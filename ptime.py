from random import randint

def generate_ptime(last_start, p_duration, diff_arrival_time):

    #generating random start time
    delta = randint(0, diff_arrival_time)
    #adding to last process start
    pstart = last_start + delta

    return pstart, p_duration

"""
#testcase
initial_time = 0
for i in range(10):
    init, duration =  generate_ptime(initial_time, randint(2,10))
    initial_time = init
    print(init)
    print(duration)
"""
    



