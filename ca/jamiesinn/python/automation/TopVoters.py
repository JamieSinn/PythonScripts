import re
import collections
import time
import sys

__author__ = 'JamieSinn'
# Use this with a Votifier log to get the top 10 voters each month
# Replace the month with the month you want to check for

month = '10'
year = '2015'


def email():
    import smtplib
    from email.mime.text import MIMEText
    import time
    username = "no-reply@sinndevelopment.com"
    password = ""
    f = open('top10.txt', 'rb')
    msg = MIMEText(re.sub("(\('username:|'|\))", '', f.read().replace(', (', '\n(')))
    f.close()
    if sys.argv[1] == "test":
        msg['Subject'] = 'TESTING MONTHLY VOTERS - NOT ACTUAL VOTES.'
    else:
        msg['Subject'] = 'Monthly Voters for %s' % time.strftime(int("%m")-1)
    msg['From'] = 'no-reply@sinndevelopment.com'
    msg['To'] = ''
    conn = smtplib.SMTP_SSL('p3plcpnl002.prod.phx3.secureserver.net', 465)
    conn.set_debuglevel(False)
    conn.ehlo()
    conn.login(username, password)
    conn.sendmail('no-reply@sinndevelopment.com', '', msg.as_string())
    conn.quit()


with open('votes.log', 'r') as File:
    votes = []
    content = File.readlines()
    for line in content:
        dateM = time.gmtime(
            int(re.search('timeStamp:\d+', line).group(0).replace("timeStamp:", ''))/1000).strftime('%m')
        dateY = time.gmtime(
            int(re.search('timeStamp:\d+', line).group(0).replace("timeStamp:", ''))/1000).strftime('%Y')
        if dateM == month and dateY == year:
            votes.append(re.search('username:.* a', line).group(0).replace(" a", ''))
    with open('top10.txt', 'w') as out:
        out.write(', '.join(str(x) for x in collections.Counter(votes).most_common(10)))
    email()
