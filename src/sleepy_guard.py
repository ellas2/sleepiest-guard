import operator
import re
import sys

def parse_input(file_path):
    guard_sleep_times = {}
    with open(file_path, 'r') as file:
        #need to go over the input in chronological order
        for line in sorted(file):
            if "Guard" in line:
                guard = re.search(r"""^.+ #(\d+) .+$""", line)
                guard_id = int(guard.group(1))  #returns guard id
            elif "falls" in line:
                falls = re.search(r"""^\[.+:(\d\d)] .+$""", line)
                sleep_start = int(falls.group(1)) #returns start sleep time id
            else:
                wakes = re.search(r"""^\[.+:(\d\d)] .+$""", line)
                wakes_up = int(wakes.group(1))
                curr_sleep_lst = list(range(sleep_start, wakes_up))
                if guard_id in guard_sleep_times:
                    #merge lists
                    new_sleep_lst = curr_sleep_lst + guard_sleep_times[guard_id]
                    guard_sleep_times.update({guard_id : new_sleep_lst})
                else:
                    guard_sleep_times[guard_id] = curr_sleep_lst
    return guard_sleep_times

def sleepiest_guard(file_path):
    guard_sleep_times = parse_input(file_path)
    sleepiest_id = max(guard_sleep_times.items(), key = lambda x : len(x[1]))[0]
    sleep_mins = {} #dictionairy that will store sleepMin : Count
    for minute in guard_sleep_times[sleepiest_id]:
        if minute in sleep_mins:
            sleep_mins[minute] += 1
        else:
            sleep_mins[minute] = 1
    max_sleep_time = max(sleep_mins.items(), key=operator.itemgetter(1))[0]
    print("Guard #" + str(sleepiest_id) + " is most likely to be asleep in 00:" + str(max_sleep_time))
    return sleepiest_id, max_sleep_time

def compare_guard_tuple(tup, val1, val2, input_kind):
    if tup[0] != val1:
        print("Incorrect guard id with " + input_kind + " input")
        return False
    elif tup[1] != val2:
        print("Incorrect max sleep minute with " + input_kind +" input")
        return False
    return True

def test_sleepiest():
    tup = sleepiest_guard('src\input\sample_input.txt')
    res = compare_guard_tuple(tup, 10, 24, "sample")
    if res is False:
        return False
    tup = sleepiest_guard('src\input\different_input.txt')
    res = compare_guard_tuple(tup, 3491, 42, "long and unordered")
    if res is False:
        print("There is a bug in your code :(")
    else:
        print("With the tested inputs your program works fine! Horray!")

def main(argv):
    sleepiest_guard(argv)
    #test_sleepiest()

if __name__ == '__main__':
    main(sys.argv[1])