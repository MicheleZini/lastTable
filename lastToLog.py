import sys
# fetch input from <last> command
last = []
i = 0
for line in sys.stdin:
  s = line.split() # plit colums
  l = len(s)
  if l > 7 and len(s[l-7]) == 3 and s[l-1]!='in' and s[l-1]!='logout': # guess wot, it works
    date = "%s %s %s %s -> %s %s" % (s[l-7],s[l-6],s[l-5],s[l-4],s[l-2],s[l-1]) # format colums
    last.append(date)
    # print date
    i+=1

log='./sleep.log'

j = 0 # parse log entries
with open(log,'r') as f:
    c = f.read()
    sc = c.split('\n')

toadd = [] # count and select new dates to add
for date in last:
   if not (date in sc):
      j+=1
      toadd.append(date)

print "+ %i dates read from <last> command, %i new ones" % (i,j)

i = 0 # add (append) new entries
if len(toadd)>0:
    with open(log,'a') as f:
       for date in toadd:
          f.write(date)
          f.write("\n")
          i+=1

print "+ %i dates added to <sleep.log>" % i
