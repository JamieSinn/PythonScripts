import re
import collections
from datetime import datetime
import calendar

__author__ = 'JamieSinn'
# Use this with a Votifier log to get the top 10 voters each month
# Replace the month with the month you want to check for

month = '04'
year = '2016'

with open('votes.log', 'r') as File:
    votes = []
    content = File.readlines()
    dateM = 0
    dateY = 0
    for line in content:
        timestamp = int(re.search('timeStamp:\d+', line).group(0).replace("timeStamp:", ''))
        try:
            dateM = datetime.fromtimestamp(timestamp).strftime('%m')
            dateY = datetime.fromtimestamp(timestamp).strftime('%Y')
        except ValueError:
            continue
        if dateM == month and dateY == year:
            votes.append(re.search('username:.* a', line).group(0).replace(" a", ''))
            # print timestamp
    with open('top10.txt', 'w') as out:
        month = calendar.month_name[int(dateM)]
        out.write(
            '[SIZE=3][FONT=Arial][COLOR=rgb(153, 255, 204)]Congratulations to all our ' + month + ' voting winners!')
        out.write('\n' + month + ' Top Prizes: 5/5/5/5/4/4/4/3/3/2 Event Tokens + Voting Medal!')
        out.write('\n[/COLOR][/FONT][/SIZE]')
        top10 = collections.Counter(votes).most_common(10)
        for voter in top10:
            stripped = str(str(voter[0]).replace('username:', ""))
            print stripped
            out.write('\n\t@' + stripped)
        out.write(
            '\n[SIZE=3][FONT=Arial][COLOR=rgb(153, 255, 204)]Thank you all for your support![/COLOR][/FONT][/SIZE]')
