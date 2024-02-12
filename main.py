import pandas as pd
import sys

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
global page_changes, methods
page_changes = []
methods = []


def nice_printing(data: list, el, rep):
    printer = pd.DataFrame()
    for i in range(len(data)):
        if len(data[i]) < el:
            for j in range(el - len(data[i])):
                data[i].append('')
        printer['turn ' + str(i)] = data[i]
    if not rep:
        for i in printer.columns:
            print(printer.loc[:, :i].to_string(index=False), end='')
            input()
    else:
        print(printer.to_string(index=False))


# First In First Out (FIFO):
# This is the simplest page replacement algorithm.
# In this algorithm, the operating system keeps track of all pages in the memory in a queue,
# the oldest page is in the front of the queue.
# When a page needs to be replaced page in the front of the queue is selected for removal.
def FIFO(sides, frames, sim):
    methods.append('FIFO')
    # list which is helping with report
    to_repo = []
    # now running
    what_we_have = []
    # how long is it alive
    times = []
    # just to make output nicer
    counter = 0
    for i in range(len(sides)):
        # if all frames are in usage there is need to replace one of them
        if len(what_we_have) == frames:
            # if side which should be run is one of currently running should be replaced. Else everything stays
            # as it is
            if sides[i] not in what_we_have:
                counter += 1
                my_new_index = times.index(max(times))
                what_we_have[my_new_index] = sides[i]
                times[times.index(max(times))] = 0
        # if there is some place for new sides it is enough to just add new one
        else:
            if sides[i] not in what_we_have:
                what_we_have.append(sides[i])
                times.append(0)
        to_repo.append(what_we_have.copy())
        # increasing time of running
        for time in range(len(times)):
            times[time] += 1
    nice_printing(to_repo, frames, sim)
    page_changes.append(counter)


# Least Recently Used (LRU) algorithm is a page replacement technique used for memory management. According to this
# method, the page which is least recently used is replaced. Therefore, in memory, any page that has been unused for a
# longer period of time than the others is replaced.
def LRU(sides, frames, sim):
    methods.append('LRU')
    # list which is helping with report
    to_repo = []
    # now running
    what_we_have = []
    # how long wasn't it mentioned
    times = []
    # just to make output nicer
    counter = 0
    for i in range(len(sides)):
        # if all frames are in usage there is need to replace one of them
        if len(what_we_have) == frames:
            # if side which should be run is one of currently running should be replaced. Else everything stays
            # it time should be restarted
            if sides[i] not in what_we_have:
                counter += 1
                my_new_index = times.index(max(times))
                what_we_have[my_new_index] = sides[i]
                times[my_new_index] = 0
            else:
                times[what_we_have.index(sides[i])] = 0
        # if there is some place for new sides it is enough to just add new one
        else:
            if sides[i] not in what_we_have:
                what_we_have.append(sides[i])
                times.append(0)
            else:
                times[what_we_have.index(sides[i])] = 0
        to_repo.append(what_we_have.copy())
        # increasing time of running
        for time in range(len(times)):
            times[time] += 1
    nice_printing(to_repo, frames, sim)
    page_changes.append(counter)

# The LFU page replacement algorithm stands for the Least Frequently Used.
# In the LFU page replacement algorithm, the page with the least visits in a given period of time is removed.
# It replaces the least frequently used pages. If the frequency of pages remains constant,
# the page that comes first is replaced first.
def LFU(sides_work, frames, sim):
    methods.append('LFU')
    # list which is helping with report
    to_repo = []
    sides = sides_work.copy()
    for i in range(len(sides)):
        sides[i] = int(sides[i])
    # now running
    what_we_have = []
    # how many times it was used
    used = {}
    # just to make output nicer
    counter = 0
    for i in range(len(sides)):
        # if all frames are in usage there is need to replace one of them
        if len(what_we_have) == frames:
            # if side which should be run is not one of currently running side with minimum calls should be
            # replaced. Else its call amount is increased
            if sides[i] not in what_we_have:
                counter += 1
                min_value = max(used.values())
                to_be_removed = 0
                for call in range(len(what_we_have)):
                    if used[what_we_have[call]] < min_value:
                        min_value = used[what_we_have[call]]
                        to_be_removed = call
                what_we_have[to_be_removed] = sides[i]
                if sides[i] not in used.keys():
                    used[sides[i]] = 1
                else:
                    used[sides[i]] += 1
            else:
                used[sides[i]] += 1
        # if there is some place for new sides it is enough to just add new one
        elif sides[i] not in what_we_have:
            what_we_have.append(sides[i])
            used[sides[i]] = 1
        else:
            used[sides[i]] = 1
        to_repo.append(what_we_have.copy())
    nice_printing(to_repo, frames, sim)
    page_changes.append(counter)


def counterer(arg, list):
    counter = 0
    for i in list:
        counter += 1
        if i == arg:
            break
    return counter

#  when a page needs to be swapped in,
#  the operating system swaps out the page whose next use will occur farthest in the future.
def OPT(sides_work, frames, sim):
    methods.append('OPT')
    # list which is helping with report
    to_repo = []
    # now running
    what_we_have = []
    counter = 0
    for i in range(len(sides)):
        # if all frames are in usage there is need to replace one of them
        if len(what_we_have) == frames:
            # we remove those that are the least repetitive
            if sides[i] not in what_we_have:
                counter += 1
                repetition = []
                for rep in range(frames):
                    repetition.append(counterer(what_we_have[rep], sides[i:]))
                what_we_have[repetition.index(max(repetition))] = sides[i]
        # if there is some place for new sides it is enough to just add new one
        elif sides[i] not in what_we_have:
            what_we_have.append(sides[i])
        to_repo.append(what_we_have.copy())
    nice_printing(to_repo, frames, sim)
    page_changes.append(counter)


def work_of_all(sides, frames, r):
    print('*' * 10, 'FIFO', '*' * 10)
    FIFO(sides, int(frames), r)
    print('*' * 10, 'LRU', '*' * 10)
    LRU(sides, int(frames), r)
    print('*' * 10, 'LFU', '*' * 10)
    LFU(sides, int(frames), r)
    print('*' * 10, 'OPT', '*' * 10)
    OPT(sides, int(frames), r)
    print()
    report['methods'] = ['FIFO', 'LRU', 'LFU', 'OPT']
    report['page changes'] = page_changes

file_name = input('give the data file name:')
simulation = input('do You wanna see simulation or generate raport? (S/r)')
with open(file_name, 'r') as file:
    report = pd.DataFrame()
    sides = file.readline().strip().split()
    frames = file.readline().strip()
    print(type(frames))

if simulation.upper() == 'R':
    with open('raport.txt', 'w') as file:
        # all what in console goes to the file
        sys.stdout = file
        work_of_all(frames=frames, sides=sides, r=True)
        print()
        report['methods'] = methods
        report['page changes'] = page_changes
        print(report)

else:
    print('SELECT OPTION\n1. FIFO\n2.LRU\n3.LFU\n4.OPT\n5.All')
    opinion = input('Your Choice: ')
    if '1' in opinion:
        print('*' * 10, 'FIFO', '*' * 10)
        FIFO(sides, int(frames), False)
    elif '2' in opinion:
        print('*' * 10, 'LRU', '*' * 10)
        LRU(sides, int(frames), False)
    elif '3' in opinion:
        print('*' * 10, 'LFU', '*' * 10)
        LFU(sides, int(frames), False)
    elif '4' in opinion:
        print('*' * 10, 'OPT', '*' * 10)
        OPT(sides, int(frames), False)
    elif '5' in opinion:
        work_of_all(sides, frames, False)
    print()
    report['methods'] = methods
    report['page changes'] = page_changes
    print(report)


