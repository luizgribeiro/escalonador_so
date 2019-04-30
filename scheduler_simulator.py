#-*-coding:utf-8-*-
from collections import namedtuple
import argparse
from random import seed 
from process_gen import gen_process_event
from pid_gen import gen_valid_pid
from ptime import generate_ptime

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
    process = namedtuple("Process", "pid, start_time, p_time, count_duration, event_info, ppid, prioridade, status")

    #seeting up initial process time 0
    active_pids, pid = gen_valid_pid(active_pids, initial_pid , args.max_process)
    p_time, p_events = gen_process_event(10, 3)
    start_time = 0
    count_duration = p_time
    proc_created = process(pid, start_time, p_time, count_duration, p_events, init, 0, 'active')

    high_priority_queue.append(proc_created)
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
        high_priority_queue.append(proc_created)
        all_processes.append(proc_created)


    for i in all_processes:
        print(i)

