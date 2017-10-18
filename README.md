# Stable: lastTable
linux cli table rapresentation of the last logins (last command)

- chmod 764 setup.sh
- ./setup.sh

**Parental Advisory: Explicit Tuples**
this code has been quickly pached toghether to just w0rk, 
any attempt to make sense of obscure nested structures is 
discouraged unless in the presence of an adult. 
A polished version is been developed by the minute by our team 
of trained pizzaboys 

basic idea is basic: 
--------------------
get output from *last* command --> ```$ last | python lastToLog.py``` 
- from raw entries..
```
reboot   system boot  4.10.0-35-generi Wed Oct  4 05:24 - 13:36  (08:12)
oshur    tty7         :0               Tue Oct  3 17:58 - 05:24  (11:25)
```
- ..extract time intervals and save them to logfile.
(*original idea is to collect them at system startup.
building a log of time spent on the host*) as:
```
Wed Oct 4 05:24 -> 13:36 (08:12)
Tue Oct 3 17:58 -> 05:24 (11:25)

```
Build a horrifying data structure to represent the calendar
in the form of:
```
cal = [ day1, day2 .. dayn ]
where: day = ( daynumber, [ hour1, hour2 .. hour24 ] ]
  and: hour = [ 1half, 2half ]
```
fill the 1half. 2half chars accoding to intervals read from log
tadaaa

# InDev: betterlastTable
