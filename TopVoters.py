import re
import collections
import datetime

__author__ = 'JamieSinn'
# Use this with a Votifier log to get the top 10 voters each month
# Replace the month with the month you want to check for

month = '08'


def email():
    import smtplib
    from email.mime.text import MIMEText
    import time
    __author__ = 'Jamie'
    USERNAME = "no-reply@sinndevelopment.com"
    PASSWORD = ""
    f = open('top10.txt', 'rb')
    msg = MIMEText(re.sub("(\('username:|'|\))", '', f.read().replace(', (', '\n(')))
    f.close()
    msg['Subject'] = 'Monthly Voters for %s' % time.strftime("%m/%Y")
    msg['From'] = 'no-reply@sinndevelopment.com'
    msg['To'] = ''
    conn = smtplib.SMTP_SSL('p3plcpnl002.prod.phx3.secureserver.net', 465)
    conn.set_debuglevel(False)
    conn.ehlo()
    conn.login(USERNAME, PASSWORD)
    conn.sendmail('no-reply@sinndevelopment.com', '', msg.as_string())
    conn.quit()


with open('votes.log', 'r') as File:
    votes = []
    content = File.readlines()
    for line in content:
        date = datetime.datetime.fromtimestamp(int(re.search('timeStamp:\d+', line).group(0).replace("timeStamp:", ''))
                                               ).strftime('%m')
        if date == month:
            votes.append(re.search('username:.* a', line).group(0).replace(" a", ''))
    with open('top10.txt', 'w') as out:
        out.write(', '.join(str(x) for x in collections.Counter(votes).most_common(10)))
    email()
