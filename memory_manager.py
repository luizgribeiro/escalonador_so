        
#checking if requested page is loaded in main memory
def check_loaded(proc, acc_page):

    if acc_page in proc.loaded_pages:
        return True

    return False

#managing memory when page fault occours
def manage_memory(process, new_page, mem_info, process_queue, all_processes):

    events = []

    if mem_info['loaded_pages'] == mem_info['max_pages'] :
        #SWAP CASE
        #obtendo processo randomicamente para ser swappado
        swapped = random.choice(process_queue)
        print(swapped)
        n_paginas = swap_in(swapped, all_processes, mem_info['swap_area'])

        events.append(f"SWAP in do processo {swapped}. Liberadas {n_paginas} paginas")

        #TODO: insert pages of current proc

        #TODO: update mem_info loaded_pages

        #TODO: Implement where necessary a swap out

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


#getting current process to do memory managent
def get_pcb(target_pid, all_process):

    for proc in all_process:
        if proc.pid == target_pid:
            return proc


    
