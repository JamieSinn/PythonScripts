import re
import os
import sys

import time


def main():
    parseLogfile(sys.argv[2])


def parseLogfile(logfile):
    staff = parseStaffList(sys.argv[1])
    logintimes = {}
    logouttimes = {}

    if os.path.isdir(logfile):
        for arg in logfile:
            parseLogfile(arg)

    with open(logfile) as log:
        lines = log.readlines()
        print "Searching " + logfile
        logins = []
        disconnects = []
        pattern = '%Y-%m-%d %H:%M:%S'
        for line in lines:
            for staffmember in staff:
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
    print logintimes
    print logouttimes


def parseStaffList(_list):
    staff = []
    with open(_list) as _file:
        for line in _file.readlines():
            line = line.replace('\n', '')
            staff.append(line)
    return staff


if __name__ == '__main__':
    main()
