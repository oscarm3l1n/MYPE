import pandas as pd

dummy_data_path = "../data/dummy.xlsx"
real_data_path = "../data/games.xlsx"

def get_sequences(n_events=4, path_to_file="../data/Linhac_df_keyed_20_games.xltx"):
    df = pd.read_excel(path_to_file)

    shot_sequences = []
    
    for i in range(df.shape[0]):
        row = df.iloc[i]
        if row["manpowersituation"] != "evenStrength":
            continue
        if row["eventname"] == "shot":
            shot_sequences.append([])
            for j in range(n_events):
                try:
                    tmp_row = df.iloc[j + i - n_events]
                    shot_sequences[len(shot_sequences) - 1].append(tmp_row)
                except:
                    pass
    print(f"Found {len(shot_sequences)} sequences with n_events={n_events}",end="\n\n")
    return shot_sequences

if __name__ == "__main__":
    sequences = get_sequences(n_events=4, path_to_file=real_data_path)

    my_dict = {}

    patterns = []
    for row in sequences:
        tmp_pat = ""
        for col in row:
            current_event = col["eventname"]
            tmp_pat += current_event + ";"

            try:
                my_dict[current_event] += 1
            except:
                my_dict[current_event] = 1
        # tmp_pat += "->shot"
        patterns.append(tmp_pat)
    
    # for k, v in my_dict.items():
    #     print(f"{k}: {v}")
    count_dict = {}
    for i in patterns:
        try:
            count_dict[i] += 1
        except:
            count_dict[i] = 1
    
    # for k, v in count_dict.items():
    #     print(f"{k}: {v}")
    tmp = dict(sorted(count_dict.items(), key=lambda item: item[1]))
    for k, v in tmp.items():
        print(f"{k}: {v}")
"""
gameid
opposingteamgoalieoniceid
opposingteamid
playerid
teamgoalieoniceid
opposingteamid
playerid
teamgoalieoniceid
teamid
teaminpossession
currentpossession
xg
compiledgametime
eventname
ishomegame
manpowersituation
opposingteamskateronicecount
outcome
period
playerprimaryposition
scoredifferential
teamskatersonicecount
type
xadjcoord
yadjcoord
"""