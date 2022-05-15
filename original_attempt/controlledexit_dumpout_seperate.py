def controlledexit_to_shot(list):
    gameid = 0
    templist = []
    templist2 = []
    resultList = []
    resultList2 = []
    teamid = 0
    flag = 0
    for row in list:
        s = re.split(r';', row)
        if flag == 0:
            if s[10] == 'controlledexit' and s[12] == 'evenStrength':
                flag = 1
                gameid = s[0]
                templist.append(s)
                templist2.append(row)
                teamid = s[5]
            else:
                templist.clear()
                templist2.clear()
                gameid = 0
                teamid = 0

        if flag == 1:
            if gameid == s[0]:
                if s[10] == 'shot' and s[12] == 'evenStrength':
                    templist.append(s)
                    templist2.append(row)
                    flag = 0
                    resultList.append(templist[:])
                    resultList2.append(templist2[:])

                    templist.clear()
                    templist2.clear()
                    gameid = 0
                    teamid = 0
                if s[10] == 'controlledexit' and s[12] == 'evenStrength' and s[5] == teamid:
                    templist.clear()
                    templist2.clear()
                    templist.append(s)
                    templist2.append(row)
                    flag = 1
                if s[10] == 'dumpout' and s[12] == 'evenStrength' and s[5] == teamid:
                    flag = 0
                    templist.clear()
                    templist2.clear()
                    gameid = 0
                    teamid = 0
                if s[10] not in {'shot', 'controlledexit', 'dumpout'}:
                    if s[12] == 'evenStrength':
                        templist.append(s)
                        templist2.append(row)
            else:
                templist.clear()
                templist2.clear()
                teamid = 0
                flag = 0
                gameid = 0
    out_file = open('controlledexit_to_shot.csv', 'w')
    for row in resultList2:
        for i in row:
            out_file.write(i)
        out_file.write('\n')
    out_file.close()
    return resultList


def seperate_to_controlledexit_and_dumpout_successful_failed():
    DataFile = "controlledexit_dumpout_shot.csv"
    DataCaptured = open(DataFile)
    controlledexitList_successful = []
    dumpoutList_successful = []
    controlledexitList_failed = []
    dumpoutList_failed = []
    flag = 0
    for row in DataCaptured:
        s = re.split(r';', row)
        if len(s) > 2:
            if flag == 0:
                x = s[10]
                if s[10] == 'controlledexit':
                    if s[14] == 'successful':
                        controlledexitList_successful.append(row)
                        flag = 11
                    else:
                        controlledexitList_failed.append(row)
                        flag = 12
                else:
                    if s[10] == 'dumpout':
                        if s[14] == 'successful':
                            dumpoutList_successful.append(row)
                            flag = 21
                        else:
                            dumpoutList_failed.append(row)
                            flag = 22
            else:
                if flag == 11:
                    if s[10] == 'shot':
                        controlledexitList_successful.append(row)
                        flag = 0
                    if s[10] not in {'shot', 'controlledexit','dumpout'}:
                        controlledexitList_successful.append(row)
                else:
                    if flag == 12:
                        if s[10] == 'shot':
                            controlledexitList_failed.append(row)
                            flag = 0
                        if s[10] not in {'shot', 'controlledexit', 'dumpout'}:
                            controlledexitList_failed.append(row)
                    else:
                        if flag == 21:
                            if s[10] == 'shot':
                                dumpoutList_successful.append(row)
                                flag = 0
                            else:
                                if s[10] not in {'shot', 'controlledexit', 'dumpout'}:
                                    dumpoutList_successful.append(row)
                        else:
                            if flag == 22:
                                if s[10] == 'shot':
                                    dumpoutList_failed.append(row)
                                    flag = 0
                                else:
                                    if s[10] not in {'shot', 'controlledexit', 'dumpout'}:
                                        dumpoutList_failed.append(row)


    out_file = open('dumpout_successful_to_shot.csv', 'w')
    for row in dumpoutList_successful:
        for i in row:
            out_file.write(i)
    out_file.close()

    out_file2 = open('controlledexit_successful_to_shot.csv', 'w')
    for row in controlledexitList_successful:
        for i in row:
            out_file2.write(i)
    out_file2.close()

    out_file3 = open('dumpout_failed_to_shot.csv', 'w')
    for row in dumpoutList_failed:
        for i in row:
            out_file3.write(i)
    out_file3.close()

    out_file4 = open('controlledexit_failed_to_shot.csv', 'w')
    for row in controlledexitList_failed:
        for i in row:
            out_file4.write(i)
    out_file4.close()
