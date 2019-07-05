import random        

#checking if requested page is loaded in main memory
def check_loaded(proc, acc_page):

    if acc_page in proc.loaded_pages:
        return True

    return False

#managing memory when page fault occours
def manage_memory(process, new_page, mem_info, process_queue, all_processes):

    events = []
    print(mem_info)

    #swap out de processos que devem ser executados
    if process.pid in mem_info['swap_area'].keys():
        events.extend(swap_out(process, mem_info, all_processes))
        #check if all pages for this process are occupied
        if pages_full(process, mem_info):
            events.append(change_pages(process, new_page))
        #add page to the process
        else:
            include_page(process, new_page)
            mem_info['loaded_pages'] += 1

        return events
        
    #processes that are with pages loaded in memory
    mem_procs = []
    
    for proc in all_processes:
        if len(proc.loaded_pages) > 0 and proc.pid != process.pid:
            mem_procs.append(proc.pid)


    #swap in de um processo para abrir especo para o que ocorreu page fault
    if mem_info['loaded_pages'] == mem_info['max_pages'] and mem_procs :
        #obtendo processo randomicamente para ser swappado
        swapped = random.choice(mem_procs)
        n_paginas = swap_in(swapped, all_processes, mem_info['swap_area'])

        mem_info['loaded_pages'] -= n_paginas

        events.append(f"SWAP in do processo {swapped}. Liberadas {n_paginas} paginas")

    else:
        #check if all pages for this process are occupied
        if pages_full(process, mem_info):
            events.append(change_pages(process, new_page))
        #add page to the process
        else:
            include_page(process, new_page)
            mem_info['loaded_pages'] += 1

    return events

    
#checking if a process ocupies all the available pages for it
def pages_full(process, mem_info):

    if len(process.loaded_pages) == mem_info['max_loaded']:
        return True
    else:
        return False

#change pages of a given process
def change_pages(process, new_page): 

    #deleting page by LRU POLICE
    deleted = process.loaded_pages[0]
    del process.loaded_pages[0]

    #inserting new_page using LRU policy
    process.loaded_pages.append(new_page)

    #returning log info
    return f'Processo {process.pid} trocou página {deleted} por {new_page}'

#include a page in the process context
def include_page(process, new_page):

    process.loaded_pages.append(new_page)


def LRU_update(process, page):

    #getting index of current used page
    index = process.loaded_pages.index(page)
    #deleting current page 
    del process.loaded_pages[index]
    #appending page (last used)
    process.loaded_pages.append(page)


def swap_in(process, all_processes, swap_area):

    target_proc = get_pcb(process, all_processes)

    swap_area[target_proc.pid] = target_proc.loaded_pages

    target_proc.loaded_pages = []

    return len(swap_area[target_proc.pid])

def swap_out(proc, mem_info,all_process):

    events = []

    available = mem_info['max_pages'] - mem_info['loaded_pages']

    wanted = len(mem_info['swap_area'][proc.pid])

    if wanted <= available:
        proc.loaded_pages = mem_info['swap_area'][proc.pid]
        del mem_info['swap_area'][proc.pid]
        mem_info['loaded_pages'] += wanted
        events.append(f"Processo {proc.pid} retornou da swap com {wanted} paginas")
    else:
        #swappa o numero de processos necessários até liberar memória suficiente
        free = 0
        for process in all_process:
            if process.loaded_pages:
                free += swap_in(process.pid, all_process, mem_info['swap_area'])
                if free >= wanted:
                    break
        #restaurando processo na memória e atualizando campos
        proc.loaded_pages = mem_info['swap_area'][proc.pid]
        del mem_info['swap_area'][proc.pid]
        mem_info['loaded_pages'] += wanted - free
        events.append(f"Processo {proc.pid} retornou da swap com {wanted} paginas substituindo outros processos")

    return events






#getting current process to do memory managent
def get_pcb(target_pid, all_process):

    for proc in all_process:
        if proc.pid == target_pid:
            return proc


    
