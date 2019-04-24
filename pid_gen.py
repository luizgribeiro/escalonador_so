from random import randint 

def gen_valid_pid(pids_list, initial_pid, max_proc):
    #TODO especificar o que fazer nesse caso
    if len(pids_list) >= max_proc:
        print("IMPOSSIVEL CRIAR")
    else:
        pnumber = 0
        for proc in range(len(pids_list)):
            pnumber = proc
            #pegando primeiro pid nao utilizado na lista
            print(f"comparando   proc {(initial_pid+proc)} e  list {pids_list[proc]}")
            if pids_list[proc] != initial_pid + proc:
                pids_list.insert(proc, (initial_pid+proc))
                return (pids_list, initial_pid+proc)
       #caso seja inserido no primeiro ou no final
        else:
            pids_list.append((initial_pid+pnumber))
            return (pids_list, initial_pid+pnumber)


lt = []

for i in range(14):

    lista , pnumber = gen_valid_pid(lt, 10, 20)

    print(lista)
    print(pnumber)
        
    
    

    