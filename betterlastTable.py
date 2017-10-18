#!/usr/bin/env python
# -*- coding:utf-8 -*-


##
# Python function for reading linux utmp/wtmp file
# http://www.likexian.com/
#
# Copyright 2014, Kexian Li
# Released under the Apache License, Version 2.0
#
##
import struct

XTMP_STRUCT = 'hi32s4s32s256shhiii4i20x'
XTMP_STRUCT_SIZE = struct.calcsize(XTMP_STRUCT)


def read_xtmp(fname):
    result = []

    fp = open(fname, 'rb')
    while True:
        bytes = fp.read(XTMP_STRUCT_SIZE)
        if not bytes:
            break

        data = struct.unpack(XTMP_STRUCT, bytes)
        data = [(lambda s: str(s).split("\0", 1)[0])(i) for i in data]
        if data[0] != '0':
            result.append(data)

    fp.close()
    result.reverse()

    return result


def printtimeline():
   from datetime import datetime as dt

   info = {'1':[4,5],'2':[4,5],'5':[1,2],'6':[4,5],'7':[1,4,7],'8':[1,4,6,7]}
   name = {'1':'runlv','2':' boot','5':' init','6':'login','7':' proc','8':' term'}

   for ev in events:
     addinfo = ''
     for i in info[ev[0]]:
       addinfo+=' - '+ev[i]
     print "%s (%6s) [%s]%s" % (dt.fromtimestamp(int(ev[9])).strftime('%Y/%m/%d %H:%M:%S'),ev[10],name[ev[0]],addinfo)


import sys
wtmp = "/var/log/wtmp"
timeline = True

try:
    print '* accessing logs in: %s' % wtmp
    events = read_xtmp(wtmp)
except IOError as e:
    print "- failed: %s" % e
    sys.exit(1)

print "+ %i events found" % len(events)

runlv = {} #define RUN_LVL       1 /* Change in system run-level (see init(8)) */
boot  = {} #define BOOT_TIME     2 /* Time of system boot (in ut_tv) */
init  = {} #define INIT_PROCESS  5 /* Process spawned by init(8) */
login = {} #define LOGIN_PROCESS 6 /* Session leader process for user login */
proc  = {} #define USER_PROCESS  7 /* Normal process */
term  = {} #define DEAD_PROCESS  8 /* Terminated process */
others = 0

for event in events:
    pid = event[9]
    if event[0] == '1':
        runlv[pid] = event
        continue
    if event[0] == '2':
        boot[pid] = event
        continue
    if event[0] == '5':
        init[pid] = event
        continue
    if event[0] == '6':
        login[pid] = event
        continue
    if event[0] == '7':
        proc[pid] = event
        continue
    if event[0] == '8':
        term[pid] = event
        continue
    others += 1

tot = len(init)+len(login)+len(proc)+len(runlv)+len(boot)+len(term)
print "  init:  %4i  |  login: %4i  |  proc: %4i" % (len(init), len(login), len(proc))
print "  runlv: %4i  |  boot:  %4i  |  term: %4i" % (len(runlv), len(boot), len(term))
print "  Tot = %5i + not significant: %4i " % (tot, others)

if timeline:
   printtimeline()
