from random import randint 

def gen_io_type():
    # 0=>IO fita, 1=>IO disco, 2=>IO printer
    io_type = randint(0, 2)
    if io_type == 0:
        return 'tape'
    elif io_type == 1:
        return 'disc'
    else:
        return 'printer'

def gen_process_event(p_max_time, qt_max_io):

    #utilizando tempo maximo de processo para definir tempo do processo
    process_time = randint(1, p_max_time)

    #utilizando numero maximo de ios para definir quantidade de ventos
    if qt_max_io > process_time - 2:
        qtt_io = randint(0, process_time-1)
    else:
        qtt_io = randint(0, qt_max_io)

    io_list = []
    #generating IO timestamps
    if qtt_io > 0 :
        for io_num in range(0, qtt_io):
            io_time = randint(1, process_time-1)
            io_list.append(io_time)

    io_list.sort()

    #list with process_time, io_time and type of IO
    io_time_type_list = []
    for i in io_list:
        io_time_type_list.append([i, gen_io_type()])

    return process_time, io_time_type_list

def gen_page_num(max):
    return randint(1, max)

def gen_page_access(max):
    return randint(1, max)

