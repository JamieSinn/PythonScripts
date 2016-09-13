import urllib2
for i in range(9):
        pdf = urllib2.urlopen("https://www.student.cs.uwaterloo.ca/~cs135/assns/a0" + str(i+1) + "/a0" + str(i+1) + ".pdf")
        with open('a0'+str(i+1) + '.pdf', 'wb') as assn:
                assn.write(pdf.read())
