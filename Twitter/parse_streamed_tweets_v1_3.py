"""
this module takes a very large streaming api file and
prepares six experiment files

author: Martin McEnroe
version: 2017-05-08
MIT License
i was cutting off the last character of the user name so some of the mentions were screwed!

v1.0 good
v1.3 just to be safe after 5/2 screwup
"""

import numpy as np

df_e = []
df2 = np.array([0])
candidates = []
status_low = 0
status_high = 0

input_file = 'selected_fields.txt'

#output files
e_1f914 = '1f914.txt'
e_1f60f = '1f60f.txt'
e_1f634 = '1f634.txt'
e_1f636 = '1f636.txt'
e_1f610 = '1f610.txt'
e_1f913 = '1f913.txt'

with open('data/tweets/' + input_file ,'r') as f:
    for line in f:
        #print(line)
        try:
            #spl_ln = line.rstrip('\n').split('|')[:-1]  #split_line <- bad bad bad [:-1]
            spl_ln = line.rstrip('\n').split('|')
            df_e.append(int(spl_ln[4]))
            #used to compute quartiles exclusions
            df2 = np.vstack((df2,int(spl_ln[4])))
            if len(spl_ln[5]) == 5:
                #emoji, status.id_str, user.id_str, status_count, screen_name
                candidates.append([spl_ln[5][2],spl_ln[0],spl_ln[2],int(spl_ln[4]),spl_ln[3]])
        except:
            pass

status_low = np.percentile(df2,25)
status_high = np.percentile(df2,75)
print(status_low,status_high)

'''
#make a dictionary
'🤔':'results/1f914.txt'
'😏':'results/1f60f.txt'
'😴':'results/1f634.txt'
'😶':'results/1f636.txt'
'😐':'results/1f610.txt'
'🤓':'results/1f913.txt'
#delete all the files
'''

#this can be greatly simplified by looking something up in a dictionary
#i think opening and closing all these files takes insane time!
for candidate in candidates:
    if int(candidate[3]) > status_low and int(candidate[3]) < status_high:
        #i have to pay the piper somehow, split the list now.
        if str(candidate[0]) == '🤔':
            e_file = 'results/1f914.txt'
        elif str(candidate[0]) == '😏':
            e_file = 'results/1f60f.txt'
        elif str(candidate[0]) == '😴':
            e_file = 'results/1f634.txt'
        elif str(candidate[0]) == '😶':
            e_file = 'results/1f636.txt'
        elif str(candidate[0]) == '😐':
            e_file = 'results/1f610.txt'
        elif str(candidate[0]) == '🤓':
            e_file = 'results/1f913.txt'
        else:
            e_file = 'results/junk.txt'
        with open(e_file, 'a') as fo:
            fo.write(candidate[0] + '|' + candidate[1] + '|' + candidate[2] + '|' + str(candidate[3]) + '|' + candidate[4] + '\n')

print(len(candidates))

#not the way to define a dictionary!
trigger = {}

trigger['🤔'] = 0
trigger['😏'] = 0
trigger['😴'] = 0
trigger['😶'] = 0
trigger['😐'] = 0
trigger['🤓'] = 0

#just out of curiosity

for candidate in candidates:
    if str(candidate[0]) in trigger.keys():
        trigger[candidate[0]] += 1
print('this is the raw input prior to filtering for retweets and middle 50%')
print(dict(trigger))

trigger['🤔'] = 0
trigger['😏'] = 0
trigger['😴'] = 0
trigger['😶'] = 0
trigger['😐'] = 0
trigger['🤓'] = 0
for candidate in candidates:
    if str(candidate[0]) in trigger.keys():
        if int(candidate[3]) > status_low and int(candidate[3]) < status_high:
            trigger[candidate[0]] += 1
print('these are the sizes of the files written')
print(dict(trigger))
