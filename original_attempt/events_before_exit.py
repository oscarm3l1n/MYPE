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

def get_events(n_events=4, event="controlledexit",path_to_file=""):
    if path_to_file == "":
        print("Please input filename")
        return
    
    file = open(path_to_file)
    data = []
    for line in file.readlines():
        data.append(line)
    print(f"Data contains {len(data)} rows")

    exit_successful_before = []
    exit_successful_after = []
    exit_fail_before = []
    exit_fail_after = []

    for i in range(1, len(data), 1):
        row = data[i].split(';')
        if row[man_power_situation] != "evenStrength":
            continue
        if row[event_name] == event and row[outcome] == "successful":
            before_events = []
            after_events = []
            for j in range(n_events):
                try:
                    before_events.append(data[i+j-n_events].split(';'))
                    after_events.append(data[i+j+1].split(';'))
                except:
                    pass
            exit_successful_before.append(before_events)
            exit_successful_after.append(after_events)

        elif row[event_name] == event and row[outcome] == "failed":
            before_events = []
            after_events = []
            for j in range(n_events):
                try:
                    before_events.append(data[i+j-n_events].split(';'))
                    after_events.append(data[i+j+1].split(';'))
                except:
                    pass
            exit_fail_before.append(before_events)
            exit_fail_after.append(after_events)
        
    return  exit_successful_before,\
            exit_successful_after,\
            exit_fail_before,\
            exit_fail_after
            
"""
Returns a row that you can index
with the predefined indexes starting
at line 1
"""
def custom_iterator(data):
    for seq in data:
        for row in seq:
            yield row

def iterate_events(data):
    for seq in data:
        string = ""
        for row in seq:
            string += row[event_name] + f"[{'F' if row[outcome] == 'failed' else 'S'}]" + ";"
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


def marker(text):
    print(f"**********************************\n*\t{text}\t\t*\n**********************************")

if __name__ == "__main__":
    n_events = 10

    ce_s_before,\
    ce_s_after,\
    ce_f_before,\
    ce_f_after = get_events(n_events=n_events, 
                            event="controlledexit",
                            path_to_file="../data/games.csv")

    d_s_before,\
    d_s_after,\
    d_f_before,\
    d_f_after = get_events(n_events=n_events, 
                           event="dumpout", 
                           path_to_file="../data/games.csv")
    
    marker("CONTROLLED EXIT")
    print(f"\nControlled exit that succeeded, {n_events} events before")
    my_count(ce_s_before)
    print(f"\nControlled exit that succeeded, {n_events} events after")
    my_count(ce_s_after)
    print(f"\nControlled exit that failed, {n_events} events before")
    my_count(ce_f_before)
    print(f"\nControlled exit that failed, {n_events} events after")
    my_count(ce_f_after)
    print()

    marker("DUMPOUT")
    print(f"\n Dumpout that succeeded, {n_events} events before")
    my_count(d_s_before)
    print(f"\n Dumpout that succeeded, {n_events} events after")
    my_count(d_s_after)
    print(f"\n Dumpout that failed, {n_events} events before")
    my_count(d_f_before)
    print(f"\n Dumpout that failed, {n_events} events after")
    my_count(d_f_after)

    print("=============== Errors ===============")
    print("Rows containing unevenStrength for control. exit (S) before", count_errors(ce_s_before))
    print("Rows containing unevenStrength for control. exit (S) after ", count_errors(ce_s_after))
    print("Rows containing unevenStrength for control. exit (F) before", count_errors(ce_f_before))
    print("Rows containing unevenStrength for control. exit (F) after", count_errors(ce_f_after))
    print()
    print("Rows containing unevenStrength for dumpout (S) before", count_errors(d_s_before))
    print("Rows containing unevenStrength for dumpout (S) after ", count_errors(d_s_after))
    print("Rows containing unevenStrength for dumpout (F) before", count_errors(d_f_before))
    print("Rows containing unevenStrength for dumpout (F) after", count_errors(d_f_after))
    
"""
(0, '\ufeffgameid')
(1, 'opposingteamgoalieoniceid')
(2, 'opposingteamid')
(3, 'playerid')
(4, 'teamgoalieoniceid')
(5, 'teamid')
(6, 'teaminpossession')
(7, 'currentpossession')
(8, 'xg')
(9, 'compiledgametime')
(10, 'eventname')
(11, 'ishomegame')
(12, 'manpowersituation')
(13, 'opposingteamskatersonicecount')
(14, 'outcome')
(15, 'period')
(16, 'playerprimaryposition')
(17, 'scoredifferential')
(18, 'teamskatersonicecount')
(19, 'type')
(20, 'xadjcoord')
(21, 'yadjcoord\n')
"""