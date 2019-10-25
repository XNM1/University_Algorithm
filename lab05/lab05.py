#region `imports`
import sys
import time
from matplotlib import pyplot as plt
from matplotlib import animation
import os
import psutil
#endregion

#region `misc`
pid = os.getpid()
py = psutil.Process(pid)

def plot(info):
    title = info['title']
    frames = info['frames']
    fig = plt.figure(1, figsize=(16, 9))
    axs = fig.add_subplot(111)
    def animate(i):
        bars = []
        axs.clear()
        plt.ylim(0, max([ j['value'] for j in frames[i]['lst'] ]) + 1)
        plt.xlim(-1, len(frames[i]['lst']))
        if len(frames) - 1 == i:
            axs.set_title(title + '; Array Access: ' + str(i - 2) + '; Memory used: ' + str(frames[i]['memory']) + ' bytes; Time: ' + str(round(frames[i]['time'] * 1000, 3)) + ' ms')
        else:
            axs.set_title(title + '; Array Access: ' + str(i) + '; Memory used: ' + str(frames[i]['memory']) + ' bytes; Time: ' + str(round(frames[i]['time'] * 1000, 3)) + ' ms')
        bars += axs.bar(list(range(len(frames[i]['lst']))),
                        [ j['value'] for j in frames[i]['lst'] ],
                        0.9,
                        color=[ j['color'] for j in frames[i]['lst'] ]
                        ).get_children()
        return bars
    anim = animation.FuncAnimation(fig, animate, frames=len(frames), repeat= False)
    plt.show()
#endregion

#region `mapping function`
def three_words_count_map(string):
    return len([word for word in string.split() if len(word.rstrip('.')) == 3])

def biggest_word_map(string):
    biggest_word = ''
    for word in string.split(' '):
        if len(word.rstrip('.')) > len(biggest_word):
            biggest_word = word.rstrip('.')
    return len(biggest_word)

def and_words_count_map(string):
    return len([word for word in string.split() if word.rstrip('.') == 'and'])

def len_map(string):
    return len(string)

def a_upper_map(string):
    return string.count('A')

def words_map(string):
    return len(string.split(' '))
#endregion

#region `sort algorithms`
def counting_sort(lst, mapping_func, descending = False, stats = False):
    if stats:
        start_time = time.time()
        frames = []
        frames.append({ 'lst': [ { 'value': mapping_func(l), 'color':'green' } for l in lst], 'time': time.time() - start_time, 'memory': py.memory_info().vms})

    rng = max([mapping_func(i) for i in lst]) + 1
    counting = [ [] for i in range(rng) ]
    for i in lst:
        counting[mapping_func(i)].append(i)

        if stats:
            frames.append({ 'lst': [ { 'value': mapping_func(l), 'color':'red' if l == i else 'green' } for l in lst], 'time': time.time() - start_time, 'memory': py.memory_info().vms})

    lst.clear()
    for i in counting:
        for j in i:
            if descending:
                lst.insert(0, j)
            else:
                lst.append(j)

            if stats:
                frames.append({ 'lst': [ { 'value': mapping_func(l), 'color':'green' } for l in lst], 'time': time.time() - start_time, 'memory': py.memory_info().vms})

    if stats:
        frames.append({'lst':[ { 'value': mapping_func(l), 'color':'blue' } for l in lst], 'time': time.time() - start_time, 'memory': py.memory_info().vms})
        frames.append({'lst':[ { 'value': mapping_func(l), 'color':'green' } for l in lst], 'time': time.time() - start_time, 'memory': py.memory_info().vms})
        return { "title": 'Counting Sort', 'frames': frames}

def radix_sort_msd(lst, mapping_func, descending = False, stats = False):
    if stats:
        start_time = time.time()
        frames = []
        frames.append({ 'lst': [ { 'value': mapping_func(l), 'color':'green' } for l in lst], 'time': time.time() - start_time, 'memory': py.memory_info().vms})

    r = len(str(max([mapping_func(i) for i in lst])))
    digit = 1
    for k in range(1, r + 1):
        rng = max(int(mapping_func(i) / digit) % 10 for i in lst) + 1
        counting = [ [] for i in range(rng) ]
        for i in lst:
            counting[int(mapping_func(i) / digit) % 10].append(i)

            if stats:
                frames.append({ 'lst': [ { 'value': mapping_func(l), 'color':'red' if l == i else 'green' } for l in lst], 'time': time.time() - start_time, 'memory': py.memory_info().vms})

        lst.clear()
        for i in counting:
            for j in i:
                if descending and k == r:
                    lst.insert(0, j)
                else:
                    lst.append(j)

                if stats:
                    frames.append({ 'lst': [ { 'value': mapping_func(l), 'color':'green' } for l in lst], 'time': time.time() - start_time, 'memory': py.memory_info().vms})

        digit *= 10

    if stats:
            frames.append({'lst':[ { 'value': mapping_func(l), 'color':'blue' } for l in lst], 'time': time.time() - start_time, 'memory': py.memory_info().vms})
            frames.append({'lst':[ { 'value': mapping_func(l), 'color':'green' } for l in lst], 'time': time.time() - start_time, 'memory': py.memory_info().vms})
            return { "title": 'Radix Sort', 'frames': frames}
#endregion

#region `file`
def file_get_list(filename):
    with open(filename) as input_file:
        return list(input_file.read().splitlines())

def file_write_list(filename, lst):
    with open(filename, 'w', encoding='utf-8') as output_file:
        j = 0
        for i in lst:
            j += 1
            output_file.write(i + ('\n' if j != len(lst) else ''))
#endregion

#region `main`
def sort(in_file, out_file, algorithm, mapping_func, descending = False, stats = False):
    lst = file_get_list(in_file)
    info = algorithm(lst, mapping_func, descending, stats)
    file_write_list(out_file, lst)
    if stats:
        plot(info)

def main():
    try:
        in_file = sys.argv[1]
        out_file = sys.argv[2]

        algorithm = sys.argv[3]
        if algorithm == "counting":
            algorithm = counting_sort
        elif algorithm == "radix":
            algorithm = radix_sort_msd
        else:
            raise Exception("Incorrect algorithm")

        mapping_func = sys.argv[4]
        if mapping_func == "three":
            mapping_func = three_words_count_map
        elif mapping_func == "biggest":
            mapping_func = biggest_word_map
        elif mapping_func == "and":
            mapping_func = and_words_count_map
        elif mapping_func == "len":
            mapping_func = len_map
        elif mapping_func == "A":
            mapping_func = a_upper_map
        elif mapping_func == "words":
            mapping_func = words_map
        else:
            raise Exception("Incorrect mapping function")

        desc = sys.argv[5]
        if desc is None or desc.lower() == "f" or desc.lower() == "false":
            desc = False
        elif desc.lower() == "t" or desc.lower() == "true":
            desc = True
        else:
            raise Exception("Incorrect descending")

        stats = sys.argv[6]
        if stats is None or stats.lower() == "f" or stats.lower() == "false":
            stats = False
        elif stats.lower() == "t" or stats.lower() == "true":
            stats = True
        else:
            raise Exception("Incorrect statistics")

        sort(in_file, out_file, algorithm, mapping_func, desc, stats)
    except Exception as e:
        print(e)
#endregion

main()