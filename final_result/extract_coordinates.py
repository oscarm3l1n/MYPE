game_id = 0
player_id = 3
team_id = 5
compiled_game_time = 9
event_name = 10  # type of event
man_power_situation = 12  # evenStrength
outcome = 14  # success/fail
type = 19  # description
x_coord = 20
y_coord = 21


def get_events(n_events=4, event="controlledexit", path_to_file=""):
    if path_to_file == "":
        print("Please input filename")
        return

    file = open(path_to_file)
    data = []
    for line in file.readlines():
        data.append(line)
    print(f"Data contains {len(data)} rows")

    exit_successful_before = []
    exit_fail_before = []

    for i in range(1, len(data), 1):
        row = data[i].split(";")
        if row[man_power_situation] != "evenStrength":
            continue
        if row[event_name] == event and row[outcome] == "successful":
            before_events = []
            for j in range(n_events):
                try:
                    row_before = data[i - j].split(";")
                    if row_before[event_name] == "pass":
                        before_events.append(row_before)
                        before_events.insert(0, data[i + 1].split(";"))
                        break
                    else:
                        before_events.append(row_before)
                except:
                    pass
            exit_successful_before.append(before_events[::-1])

        elif row[event_name] == event and row[outcome] == "failed":
            before_events = []
            should_add = True
            for j in range(n_events):
                try:
                    row_before = data[i - j].split(";")
                    if row_before[event_name] == "pass":
                        before_events.append(row_before)
                        before_events.insert(0, data[i + 1].split(";"))
                        break
                    elif (row_before[event_name] == event\
                            or row_before[event_name] == "dumpout")\
                            and j != 0:
                        should_add = False
                        break
                    else:
                        before_events.append(row_before)
                except:
                    pass
            if should_add:
                exit_fail_before.append(before_events[::-1])

    return exit_successful_before, exit_fail_before
"""
pass -> any event -> controlled exit
pass -> controlled exit -> any event
use "any event" as direction for the pass.
"""
def filter(data, success):
    sequences = []
    if success:
        # Pass is always seq[0]
        for sequence in data:  # a sequence contains rows
            if (
                sequence[1][event_name] == "reception"
                and sequence[2][event_name] == "controlledexit"
            ):
                sequences.append( [sequence[0]] + [sequence[1]] + [sequence[2]] )
            elif (
                sequence[1][event_name] == "controlledexit"
                and sequence[2][event_name] == "reception"
            ):
                sequences.append( [sequence[0]] + [sequence[2]] + [sequence[1]] )
    else:
        for sequence in data:  # a sequence contains rows
            if sequence[2][event_name] == "controlledexit":
                sequences.append( [sequence[0]] + [sequence[1]] + [sequence[2]] )
            elif sequence[1][event_name] == "controlledexit":
                sequences.append( [sequence[0]] + [sequence[2]] + [sequence[1]] )
    return sequences

"""
0: x for pass
1: y for pass
2: x for reception
3: y for reception
4: label 1 or 0 for success in controlled exit
sequence[0] is pass
seq[1] is reception/any event in the case of fail
seq[2] is controlled exit
"""
def create_data_row(data):
    data_rows = []
    for sequence in data: # each sequence contains 3 elements
        _pass = sequence[0]
        _reception = sequence[1]
        _ctrl_exit = sequence[2]

        x_pass = _pass[x_coord]
        y_pass = _pass[y_coord].strip()
        x_recep = _reception[x_coord]
        y_recep = _reception[y_coord].strip()
        label = "1" if _ctrl_exit[outcome] == "successful" else "0"
        data_rows.append(x_pass+";"+y_pass+";"+x_recep+";"+y_recep+";"+label+";")
    return data_rows

if __name__ == "__main__":
    success, fail = get_events(n_events=10,
                                path_to_file="../data/games.csv",
                                event="controlledexit")


    filtered_success = filter(data=success, success=True)
    filtered_fail = filter(data=fail, success=False)
    for sequence in filtered_fail:
        res =""
        for row in sequence:
            res += row[event_name]+";"
        print(res)

    row = create_data_row(filtered_success)
    result = ""
    for i in row:
        result += i + "\n"
    f = open("succesful_control_exit.csv", "w")
    f.write(result)
    f.close()

    row = create_data_row(filtered_fail)
    result = ""
    for i in row:
        result += i + "\n"
    f = open("fail_control_exit.csv", "w")
    f.write(result)
    f.close()

    row = create_data_row(filtered_fail)
    result = ""
    for i in row:
        result += i + "\n"
    row = create_data_row(filtered_success)
    for i in row:
        result += i + "\n"
    f = open("data.csv", "w")
    f.write(result)
    f.close()