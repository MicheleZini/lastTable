hoursheader = "  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 " # 3*24+1 = 73
linebreaker = "\x1b[37m+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+"
indent = "       " # 7 spaces

frommonth = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
tomonth = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
# monthdays = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}


times = [] # array of (month_num,day, hour_start,min_start, hour_dur,min_dur)

# read time entries from log file
with open('./sleep.log','r') as f:
   c = f.read()

minday=99
minmonth=99

maxday=0
maxmonth=0

# parse entries
lines = c.split('\n')
for l in lines:
   if len(l)<27:
       continue
   ls = l.split(' ')
   st = ls[3].split(':')
   du = ls[6].split(':')
   time = (int(frommonth[ls[1]]),int(ls[2]),st[0],st[1],du[0][1:],du[1][:2])
   times.append(time)

   if time[0] >= maxmonth:
      maxmonth = time[0]
      if time[1] > maxday:
         maxday = time[1]
   if time[0] <= minmonth:
      minmonth = time[0]
      if time[1] < minday:
         minday = time[1]

# we now have all nice intervals in <times>
# time to initialize our "calendar"

# first we set all to '.' -> offline
cal = []
if minmonth == maxmonth:
   for daynum in range(minday,maxday+1):
       day = []
       for h in range(24):
          day.append([' ',' '])
       cal.append((daynum,day))

   import random
   # now the fun part: we need to set all intervals as '*' -> online


   for interv in times:
      color = "\x1B[%im" % random.randint(31,36)
      day = interv[1]
      hour_start= interv[2]
      if interv[3]<30:
         min_start=0
      else:
         min_start=1
      duration=0 # interval duration in minutes
      if len(interv[4].split('+'))>1:
          spl=interv[4].split('+')
          duration = int(spl[0])*24*60 + int(spl[1])*60 + int(interv[5])
      else:
          duration = int(interv[4])*60 + int(interv[5])
      duration = duration/30
      # print "day:%s at%s:%s for:%s min" % (day,hour_start,min_start,duration)
      #if (int(hour_start) + int(duration)*2) <= 24:
      if True:
          d = int(day) - int(maxday)
          h = int(hour_start)
          m = 0
          #print "%i %i %i"%(d,m,h)
          #print "%s %s %s"%(day,maxday,hour_start)
          if min_start == 0:
            cal[d][1][h][0]=color+'X'
            cal[d][1][h][1]=color+'X'
            duration-=1
          else:
            cal[d][1][h][1]=color+'X'

          for i in range(duration-1):
            cal[d][1][h][m]=color+'X'
            if m == 0:
              m=1
            else:
              h+=1
              if h >= 24:
                 h=0
                 d+=1
              m=0


print "+ %i intervals read from log" % len(times)
print "  from: %s %s" %(tomonth[minmonth],minday)
print "  to: %s %s" %(tomonth[maxmonth],maxday)
#-------------------------------------------
# !!display data!!
#-------------------------------------------

if minmonth == maxmonth:
   print indent + hoursheader
   print indent + linebreaker

   for day in cal:
      line = "%3s %2i \x1b[37m|" % (tomonth[minmonth],day[0])
      for h in day[1]:
          line+="%1s%1s\x1b[37m|" % (h[0],h[1])
      print line
      print indent + linebreaker

