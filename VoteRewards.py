import re
import collections
import datetime

month = '09'
with open('vote.log', 'r') as File:
    votes = []
    content = File.readlines()
    for line in content:
        date = datetime.datetime.fromtimestamp(int(re.search('timeStamp:\d+', line).group(0).replace("timeStamp:", ''))
                                               ).strftime('%m')
        if date == month:
            votes.append(re.search('username:.* a', line).group(0).replace(" a", ''))
    print(collections.Counter(votes).most_common(10))