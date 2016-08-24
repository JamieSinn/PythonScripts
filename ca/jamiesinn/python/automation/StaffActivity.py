import re
import os
import sys

import time
from datetime import datetime


def main():
    parseLogfile(sys.argv[2])


def parseLogfile(logfile):
    staff = parseStaffList(sys.argv[1])
    logintimes = {}
    logouttimes = {}
    if os.path.isdir(logfile):
        for _file in os.listdir(logfile):
            parseLogfile(logfile + '/' + _file)

    try:
        with open(logfile) as log:
            lines = log.readlines()
            print "Searching " + logfile
            pattern = '%Y-%m-%d %H:%M:%S'
            for staffmember in staff:
                disconnects = []
                logins = []
                for line in lines:
                    logintime = re.search(
                        '\d{4}-\d{2}-\d{2} ([01]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])? \[INFO\] %s\[' % staffmember,
                        line)
                    disconnecttime = re.search(
                        '\d{4}-\d{2}-\d{2} ([01]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])? \[INFO\] %s lost connection' %
                        staffmember,
                        line)
                    if logintime is not None:
                        login = int(time.mktime(time.strptime(re.sub(' \[INFO\].*', '', logintime.group(0)), pattern)))
                        logins.append(login)
                    if disconnecttime is not None:
                        disconnect = int(
                            time.mktime(time.strptime(re.sub(' \[INFO\].*', '', disconnecttime.group(0)), pattern)))
                        disconnects.append(disconnect)
                    logintimes[staffmember] = logins
                    logouttimes[staffmember] = disconnects
                    continue
        calcOnlineTime(logintimes, logouttimes)
    except IOError:
        print "IOError - Skipping"


def parseStaffList(_list):
    staff = []
    with open(_list) as _file:
        for line in _file.readlines():
            line = line.replace('\n', '')
            staff.append(line)
    return staff


def calcOnlineTime(logintimes, logouttimes):
    staff = parseStaffList(sys.argv[1])
    for staffmember in staff:
        login = logintimes[staffmember]
        logout = logouttimes[staffmember]
        _online = 0
        for i in range(len(logout)):
            diff = datetime.fromtimestamp(logout[i]) - datetime.fromtimestamp(login[i])
            _online += diff.seconds / 60
        print '\t' + staffmember + ': ' + str(_online)


if __name__ == '__main__':
    main()
