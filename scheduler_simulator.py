#-*-coding:utf-8-*-
from collections import namedtuple
import argparse
from random import seed 
from process_gen import gen_process_event
from pid_gen import gen_valid_pid

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
    active_pids = []
    high_priority_queue = []
    low_priority_queue = []
    io_queue = []
    init = 1
    

    #tuplas STRUCTS
    process = namedtuple("Process", "pid, p_time, event_info")

    for i in range(args.max_process):
        active_pids, pid = gen_valid_pid(active_pids, 100, args.max_process)
        p_time, p_events = gen_process_event(10, 3)
        high_priority_queue.append(process(pid, p_time, p_events))

    print(high_priority_queue)
    print(active_pids)
