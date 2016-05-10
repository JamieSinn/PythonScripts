import re
import collections
from datetime import datetime

__author__ = 'JamieSinn'
# Use this with a Votifier log to get the top 10 voters each month
# Replace the month with the month you want to check for

month = '04'
year = '2016'

with open('votes.log', 'r') as File:
    votes = []
    content = File.readlines()
    for line in content:
        timestamp = int(re.search('timeStamp:\d+', line).group(0).replace("timeStamp:", ''))
        try:
            dateM = datetime.fromtimestamp(timestamp).strftime('%m')
            dateY = datetime.fromtimestamp(timestamp).strftime('%Y')
        except ValueError:
            continue
        if dateM == month and dateY == year:
            votes.append(re.search('username:.* a', line).group(0).replace(" a", ''))
            print timestamp
    with open('top10.txt', 'w') as out:
        out.write(', '.join(str(x) for x in collections.Counter(votes).most_common(10)))
