#-*-coding:utf-8-*-
from recordtype import recordtype
#from collections import namedtuple
import argparse
from random import seed 
from process_gen import gen_process_event
from pid_gen import gen_valid_pid
from ptime import generate_ptime

def gera_chegada(all_processes_list, tempo):

    arrival_list = []
    for proc in all_processes_list:
        if proc.start_time == tempo:
            arrival_list.append(proc.pid)
            print(f"Gerei chegada de {proc.pid}")

    return arrival_list

def set_running(pid, all_processes_list):

    for proc in all_processes_list:
        if proc.pid == pid:
            proc.status = 'running'

def set_active(pid, all_processes_list):

    for proc in all_processes_list:
        if proc.pid == pid:
            proc.status = 'active'

def dec_proc_time(pid, all_processes_list):

    for proc in all_processes_list:
        if proc.pid == pid:
            proc.count_duration -= 1

def switch_context(queue, all_processes_list):

    running_pid = queue[0]

    set_active(running_pid, all_processes_list)
    del queue[0]
    queue.append(running_pid)


def print_processes(all_processes):

    for proc in all_processes:
        print(proc)


if __name__ == '__main__':

    #setando semente inicial => para mesmos parametros resultados iguais
    seed(0)

    parser = argparse.ArgumentParser(description='Simulador de escalonador de processos')
    #numero de processos
    parser.add_argument('--pmax', required=False, type=int, default=5,
                        dest='max_process',
                        help='Número máximo de processos permitidos')
    #fatia de tempo (quantum)
    parser.add_argument('-t', required=False, type=int, default=5,
                        dest='quantum',
                        help='fatia de tempo máxima dedicada a cada processo')
    #tempo de io gasto com fita
    parser.add_argument('--ttape', required=False, type=int, default=8,
                        dest='tape_time',
                        help='tempo de IO gasto com leitura de fita default(8)')
    #tempo de io gasto com disco
    parser.add_argument('--tdisc', required=False, type=int, default=4,
                        dest='disc_time',
                        help='tempo de IO gasto com disco default(4)')
    #tempo de io gasto com impressão
    parser.add_argument('--tprint', required=False, type=int, default=6,
                        dest='printer_time',
                        help='tempo de IO gasto com impressão default(6)')


    args = parser.parse_args()

    #initial scheduler setup
    time = 0
    quantum = args.quantum
    all_processes = []
    active_pids = []
    high_priority_queue = []
    low_priority_queue = []
    io_queue = []
    priority_dict = {0: "HIGH", 1: "LOW"} 
    init = 1
    initial_pid = 100
    diff_arrival = 5
    

    #tuplas STRUCTS
    process = recordtype("Process", "pid, start_time, p_time, count_duration, event_info, ppid, prioridade, status")

    #seeting up initial process time 0
    active_pids, pid = gen_valid_pid(active_pids, initial_pid , args.max_process)
    p_time, p_events = gen_process_event(10, 3)
    start_time = 0
    count_duration = p_time
    proc_created = process(pid, start_time, p_time, count_duration, p_events, init, 0, 'active')

    all_processes.append(proc_created)

    #generate processes
    for i in range(args.max_process - 1):
        #updating actives pid list and obtaining a valid pid
        active_pids, pid = gen_valid_pid(active_pids, initial_pid , args.max_process)
        #generating process duration and events
        p_time, p_events = gen_process_event(10, 3)
        #generating arrival time and adding a counter to check duration
        start_time, count_duration = generate_ptime(all_processes[-1].start_time, p_time, diff_arrival)


        #creating process with all the information
        proc_created = process(pid, start_time, p_time, count_duration, p_events, init, 0, 'active')

        #updating process list
        all_processes.append(proc_created)


    for i in all_processes:
        print(i)

    print("##################PROCESSOS CRIADOS!###########################")

    while True:

        #generating process arrival
        high_priority_queue.extend(gera_chegada(all_processes, time))
        #print(high_priority_queue)

        #getting current running process =======> TODO: low priority queue
        current_proc = high_priority_queue[0]
        set_running(current_proc, all_processes)
        dec_proc_time(current_proc, all_processes)
        print(f"--------------{quantum}")
        print_processes(all_processes)
        quantum -= 1


        time += 1

        if quantum == 0:
            quantum = args.quantum
            switch_context(high_priority_queue, all_processes)

        if time > 20:
            break