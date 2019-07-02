#-*-coding:utf-8-*-
from recordtype import recordtype
from colorama import Fore, Style
from memory_manager import check_loaded
import csv
from time import sleep
import argparse
from random import seed 
from process_gen import gen_process_event, gen_page_access, gen_page_num
from pid_gen import gen_valid_pid   

from ptime import generate_ptime

def gera_chegada(all_processes_list, tempo):

    arrival_list = []
    for proc in all_processes_list:
        if proc.start_time == tempo:
            arrival_list.append(proc.pid)

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

def switch_context(queue, all_processes_list, low_priority_queue):

    if queue:
        running_pid = queue[0]

        set_active(running_pid, all_processes_list)
        del queue[0]
        change_priority(running_pid, all_processes_list, 1)
        low_priority_queue.append(running_pid)
        
def change_priority(pid, all_processes_list, new_priority):

    for proc in all_processes_list:
        if proc.pid == pid:
            proc.priority = new_priority

def check_halt(pid, all_processes_list):

    for proc in all_processes_list:
        if proc.pid == pid and proc.count_duration == 0:
            proc.status = 'halt'
            return True
    
    return False

#getting current process to do memory managent
def get_pcb(target_pid, all_process):

    for proc in all_process:
        if proc.pid == target_pid:
            return proc



def dispatch_process(process_queue, all_process, io_queue, io_times, n_mem_frames):

    events = []

    #getting current process
    current_proc = process_queue[0]
    #setting current proc status to runnig
    set_running(current_proc, all_processes)
    #getting current process
    proc = get_pcb(current_proc, all_process)
    #generate access page
    acc_page = gen_page_access(proc.npages)


    #checking if page is loaded in memory
    if check_loaded(proc, acc_page):
        pass
    else:
        #TODO: Add manage memory function
        #manage_memory()
        print("Não ta carregada --- page fault")

    # if needed sends current process to io
    if not check_io(current_proc, all_processes, io_queue, io_times, process_queue):
        dec_proc_time(current_proc, all_processes)
    else:
        events.append(f'processo {current_proc} foi para I/O')

    if check_halt(current_proc, all_processes):
        events.append(f'processo {current_proc} finalizado com sucesso')
        del process_queue[0]

    return events

def check_io(pid, all_processes_list, io_queue, io_times, running_queue):

    #getting running process
    for proc in all_processes_list:
        if proc.pid == pid:
            #getting elapsed time 
            elapsed_time = proc.p_time - proc.count_duration
            #searching in process io events to find its times
            for io_event in proc.event_info:
                if elapsed_time == io_event[0]:
                    #adding pid, event type and io time io queue
                    io_queue.append([pid, io_event[1], io_times[io_event[1]]])
                    #updating IO events to be done
                    proc.status = f'blocked {io_event[1]}'
                    running_queue.remove(pid)
                    proc.event_info.remove(io_event)

                    return True

    else:
        return False

def set_proc_status(pid, all_processes_list, status):

    for proc in all_processes_list:
        if proc.pid == pid:
            proc.status = status
        

def io_queue_manager(io_queue, high_priority_queue, low_priority_queue, all_processes_list):

    events = []
    for io_proc in io_queue:
        #dec io time
        io_proc[2] -= 1
        if io_proc[2] == 0:
            set_proc_status(io_proc[0], all_processes_list, 'active')
            events.append(f'processo {io_proc[0]} finalizou I/O')
            #if comming from disc, go to low priority queue
            if io_proc[1] == 'disc':
                low_priority_queue.append(io_proc[0])
                change_priority(io_proc[0], all_processes_list, 1)
            else:
                high_priority_queue.append(io_proc[0])
            io_queue.remove(io_proc)
    return events


def simulation_end(all_processes_list):

    end_count = 0
    for proc in all_processes_list:
        if proc.status == 'halt':
            end_count += 1

    if end_count == len(all_processes_list):
        return True
    else:
        return False
        
def print_processes(all_processes):

    for proc in all_processes:
        print(Fore.RED + proc)

def print_process_list(pid, all_processes_list):

    for proc in all_processes_list:
        for number in pid:
            if proc.pid == number:
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
    parser.add_argument('-t', required=False, type=int, default=10,
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
    #tempo máximo de cada processo
    parser.add_argument('--tproc', required=False, type=int, default=50,
                        dest='max_proc_time',
                        help='tempo máximo de um processo default(10)')
    #numero maximo de operacoes de io
    parser.add_argument('--nio', required=False, type=int, default=8,
                        dest='max_n_io',
                        help='tempo máximo de um processo default(3)')
    #numero de frames que a memória comporta 
    parser.add_argument('--nframes', required=False, type=int, default=64,
                        dest='num_frames',
                        help='Número de frames na memória default(64)')
    #numero maximo de operacoes de io
    parser.add_argument('--max_pages', required=False, type=int, default=64,
                        dest='max_pages',
                        help='Número máximo de páginas de um processo default(64)')
    
    args = parser.parse_args()

    #initial scheduler setup
    time = 0
    io_times = {'disc': args.disc_time, 'tape': args.tape_time,'printer': args.printer_time}
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

    csv_file = open('escalonador.csv', 'w', newline='')
    time_logger = csv.writer(csv_file)
    time_logger.writerow(['Tempo', 'Processo'])


    #tuplas STRUCTS
    process = recordtype("Process", """pid, start_time, p_time, count_duration,
                          event_info, ppid, priority, status, npages, loaded_pages""")

    #seeting up initial process time 0
    active_pids, pid = gen_valid_pid(active_pids, initial_pid , args.max_process)
    p_time, p_events = gen_process_event(args.max_proc_time, args.max_n_io)
    start_time = 0
    count_duration = p_time
    n_pages = gen_page_num(args.max_pages)
    proc_created = process(pid, start_time, p_time, count_duration, p_events, init, 0, 'active', n_pages, [])

    all_processes.append(proc_created)

    #generate processes
    for i in range(args.max_process - 1):
        #updating actives pid list and obtaining a valid pid
        active_pids, pid = gen_valid_pid(active_pids, initial_pid , args.max_process)
        #generating process duration and events
        p_time, p_events = gen_process_event(10, 3)
        #generating arrival time and adding a counter to check duration
        _, count_duration = generate_ptime(all_processes[-1].start_time, p_time, diff_arrival)
        #generating initial time for new processes every 3 seconds (new specification -- )
        start_time += 3
        #generating number of pages
        n_pages = gen_page_num(args.max_pages)


        #creating process with all the information
        proc_created = process(pid, start_time, p_time, count_duration, p_events, init, 0, 'active', n_pages, [])

        #updating process list
        all_processes.append(proc_created)

    events = []
    print(Fore.MAGENTA + "##################PROCESSOS CRIADOS!###########################")
    print(Style.RESET_ALL)
    while True:
        
        _ = input()

        if high_priority_queue:
            qtdd_proc_io = len(io_queue)
            current_proc = high_priority_queue[0]
            events = dispatch_process(high_priority_queue, all_processes, io_queue, io_times, args.num_frames)
            quantum -= 1 
            print(Fore.GREEN + f"============delta-quantum: {quantum}, tempo decorrido: {time}============")
            #if process went to io, restart quantum
            if qtdd_proc_io < len(io_queue):
                quantum = args.quantum

            print(Fore.RED + '------------high priority queue------------')
            print_process_list(high_priority_queue, all_processes)
            print(Style.RESET_ALL)
            print(Fore.BLUE + "------------low priority queue------------")
            print_process_list(low_priority_queue, all_processes)
            print(Style.RESET_ALL)


            time_logger.writerow([time, current_proc])

        elif low_priority_queue:

            current_proc = low_priority_queue[0]
            change_priority(current_proc, all_processes, 0)
            low_priority_queue.remove(current_proc)
            high_priority_queue.append(current_proc)
            qtdd_proc_io = len(io_queue)
            events = dispatch_process(high_priority_queue, all_processes, io_queue, io_times, args.num_frames)
            events.append(f'processo {current_proc} movido para fila de alta prioridade')
            if qtdd_proc_io < len(io_queue):
                quantum = args.quantum

            print(Fore.RED + '------------high priority queue------------')
            print_process_list(high_priority_queue, all_processes)
            print(Style.RESET_ALL)
            print(Fore.BLUE + "------------low priority queue------------")
            print_process_list(low_priority_queue, all_processes)
            print(Style.RESET_ALL)

            time_logger.writerow([time, current_proc])
            quantum -= 1 
        else:
            
            time_logger.writerow([time, -1])
        
        #decrement io time from every process in io queue
        events.extend(io_queue_manager(io_queue, high_priority_queue, low_priority_queue, all_processes))
        print(Fore.CYAN + f'------------io_queue:\n {io_queue}\n------------')
        print(Style.RESET_ALL)

        #generating process arrival
        arrival_list = gera_chegada(all_processes, time)
        for proc in arrival_list:
            high_priority_queue.append(proc)
            events.append(f'Gerada chegada do processo {proc}')

        for e in events:
            print(e)

        #cleaning up events buffer
        events = []

        print(Fore.GREEN + '====================================\n')
        print(Style.RESET_ALL)

        time += 1

        if quantum == 0:
            quantum = args.quantum
            switch_context(high_priority_queue, all_processes, low_priority_queue)

        if simulation_end(all_processes):
            break

