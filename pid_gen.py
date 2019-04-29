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
                npid = initial_pid + len(pids_list)
                pids_list.append((initial_pid))
                pnumber = npid
            else:
                npid = initial_pid + len(pids_list)
                pids_list.append(npid)
                pnumber = npid
            return (pids_list, pnumber)


"""
#testcase
lt = []

#generating 14 pids
for i in range(14):

    #generating pid and updating pids_list
    lt , pnumber = gen_valid_pid(lt, 10, 20)
    #when more than 7 process exist 
    if i > 7:
        #coin tossing to delete process or not
        value = randint(0,1)
        if value == 1:
            #selecting element to be deleted
            index = randint(0, len(lt) - 1)
            del lt[index]

    print(lt)
    print(pnumber)
"""
