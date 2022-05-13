from collections import Counter

game_id = 0
player_id = 3
team_id = 5
compiled_game_time = 9
event_name = 10             # type of event
man_power_situation = 12    # evenStrength
outcome = 14                # success/fail
type = 19                   # description

# controlledexit
# dumpout
def custom_iterator(data):
    for seq in data:
        for row in seq:
            yield row

def iterate_events(data):
    for seq in data:
        string = ""
        for row in seq:
            string += row[event_name]+ f"[{'F' if row[outcome] == 'failed' else 'S'}]" + ";"
        yield string

def pprint(data):
    for i in data:
        print(i)

def my_count(data, n=10):
    counter = Counter()
    for row in iterate_events(data):
        try:
            counter[row] += 1
        except:
            counter[row] = 1
    pprint(counter.most_common(20))
    sum = 0
    for i in counter.most_common(20):
        sum += i[1]
    print(sum)

def count_errors(data):
    counter = 0
    for i in custom_iterator(data):
        if i[man_power_situation] != "evenStrength":
            counter += 1
    return counter

def get_sequence(n_events=4, event="controlledexit", path_to_file=""):
    file = open(path_to_file)
    data = []
    for line in file.readlines():
        data.append(line)
    print(f"Data contains {len(data)} rows")

    exit_successful_after = []

    for i in range(1, len(data), 1):
        row = data[i].split(';')
        if row[man_power_situation] != "evenStrength":
            continue
        if row[event_name] == event and row[outcome] == "successful":
            after_events = []
            current_team = row[team_id]
            for j in range(n_events):
                try:
                    tmp_row = data[i+j].split(';')
                    if tmp_row[event_name] == 'dumpin'\
                         or tmp_row[event_name]=='controlledentry'\
                         and current_team == tmp_row[team_id]:
                        after_events.append(tmp_row)
                        break
                    after_events.append(tmp_row)
                except:
                    pass
            exit_successful_after.append(after_events)

    return exit_successful_after

def marker(text):
    print(f"**********************************\n*\t{text}\t\t*\n**********************************")

if __name__ == '__main__':
    n_events = 10
    control_exit = get_sequence(n_events=n_events, event="controlledexit", path_to_file='../data/games.csv')
    dumpout = get_sequence(n_events=n_events, event="dumpout", path_to_file='../data/games.csv')
    print(len(control_exit))
    print(len(dumpout))

    marker("CONTROLLED EXIT")
    print(f"\nControlled exit that succeeded, {n_events} events after")
    my_count(control_exit)
    print()
    marker("DUMPOUT")
    print(f"\n Dumpout that succeeded, {n_events} events after")
    my_count(dumpout)