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
user     tty7         :0               Tue Oct  3 17:58 - 05:24  (11:25)
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
![demo](https://pbs.twimg.com/media/DMIY69oW0AAhbKq.jpg)

# InDev: betterlastTable

instead of this piping bash logging nonsense, can we read entries directly from source on disk?
well yes of course, last reads from `/var/log/wtmp` and we can do the same.
utmp file structure is not straightforward, values unpacking is necessary (*thx Kexian Li*)

we now have wtmp entries:
```
['6', '1740', 'tty1', 'tty1', 'LOGIN', '', '0', '0', '1740', '1506949239', '359116', '0', '0', '0', '0']
['5', '1740', 'tty1', 'tty1', '', '', '0', '0', '1740', '1506949239', '359116', '0', '0', '0', '0']
['1', '53', '~', '~~', 'runlevel', '4.10.0-35-generic', '0', '0', '0', '1506949239', '348493', '0', '0', '0', '0']
['2', '0', '~', '~~', 'reboot', '4.10.0-35-generic', '0', '0', '0', '1506949222', '76766', '0', '0', '0', '0']
```
dat we interpret as:
```
2017/10/02 13:00:39 (359116) [login] - LOGIN - 
2017/10/02 13:00:39 (359116) [ init] - 1740 - tty1
2017/10/02 13:00:39 (348493) [runlv] - runlevel - 4.10.0-35-generic
2017/10/02 13:00:22 ( 76766) [ boot] - reboot - 4.10.0-35-generic
```
Determining the data intervals:
-------------------------------
How do we correlate this data in a smart way?
