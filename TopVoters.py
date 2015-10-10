import re
import collections
import datetime
__author__ = 'JamieSinn'
# Use this with a Votifier log to get the top 10 voters each month
# Replace the month with the month you want to check for

month = '09'
with open('votes.log', 'r') as File:
    votes = []
    content = File.readlines()
    for line in content:
        date = datetime.datetime.fromtimestamp(int(re.search('timeStamp:\d+', line).group(0).replace("timeStamp:", ''))
                                               ).strftime('%m')
        if date == month:
            votes.append(re.search('username:.* a', line).group(0).replace(" a", ''))
    print(collections.Counter(votes).most_common(10))
