import pandas as pd
from datetime import datetime


data = pd.read_excel(r'a_out_0714.xlsx')

time_new_list = []
empty = 0
level0to5 = 0
level5to10 = 0
level10to15 = 0
level15to20 = 0
level20to25 = 0
level25to30 = 0
levelabove30 = 0

datetimeFormat = '%Y-%m-%dT%H:%M:%S.%f+08:00'
datetimeFormat2 = '%Y-%m-%dT%H:%M:%S+08:00'

for index, row in data.iterrows():
    P3_CODE = row['P3_CODE']
    MM60311_CODE = row['MM60311_CODE']
    if (pd.isna(row['stop_time']) and (int(P3_CODE) != 99 or int(MM60311_CODE) != 99)):
        #print(P3_CODE == '99')
        print(P3_CODE, MM60311_CODE, index)
        empty = empty + 1
        time_new_list.append("")
        continue
    if (P3_CODE == '99' or pd.isna(row['start_time']) or pd.isna(row['stop_time'])):
        time_new_list.append("")
        continue
    # print(index)
    time_ori = float(row['cost_time'])
    try:
        date1 = datetime.strptime(str(row['start_time']), datetimeFormat)
    except ValueError:
        date1 = datetime.strptime(str(row['start_time']), datetimeFormat2)
    try:
        date2 = datetime.strptime(str(row['stop_time']), datetimeFormat)
    except ValueError:
        date2 = datetime.strptime(str(row['stop_time']), datetimeFormat2)
    delta = date2 - date1
    #print(delta)
    miao = delta.seconds
    fen = round(miao/60, 2)
    #if (fen != time_ori):
        #print(str(time_ori), str(fen), str(index))
    if (fen <= 5):
        level0to5 = level0to5 + 1
    elif (fen > 5 and fen <= 10):
        level5to10 = level5to10 + 1
    elif (fen > 10 and fen <= 15):
        level10to15 = level10to15 + 1
    elif (fen > 15 and fen <= 20):
        level15to20 = level15to20 + 1
    elif (fen > 20 and fen <= 25):
        level20to25 = level20to25 + 1
    elif (fen > 25 and fen <= 30):
        level25to30 = level25to30 + 1
    else:
        levelabove30 = levelabove30 + 1
    time_new_list.append(fen)

col_name = data.columns.tolist()

col_name.insert(col_name.index('cost_time')+1, 'time_new')
data = data.reindex(columns=col_name)
data['time_new'] = time_new_list

print(empty, level0to5, level5to10, level10to15, level15to20, level20to25, level25to30, levelabove30)

data.to_excel('a_out_0715.xlsx')