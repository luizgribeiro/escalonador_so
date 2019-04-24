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
            if pids_list[proc] != initial_pid + proc:
                pids_list.insert(proc, (initial_pid+proc))
                return (pids_list, initial_pid+proc)
       #caso seja inserido no primeiro ou no final
        else:
            if len(pids_list) == 0:
                pids_list.append((initial_pid))
            else:
                npid = initial_pid + len(pids_list) + 1
                pids_list.append(npid)
            return (pids_list, initial_pid+pnumber)


lt = []

for i in range(14):

    lista , pnumber = gen_valid_pid(lt, 10, 20)

    if i % 3 ==0 and i != 0:
        del lista[randint(0,len(lista))]

    print(lista)
    print(pnumber)
        
    
    

    