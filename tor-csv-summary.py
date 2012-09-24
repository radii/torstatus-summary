#!/usr/bin/env python

import csv, os

class router(object):
    '''The router object holds statistics about a Tor router.
    Example:

    import csv
    rl = [router(i) for i in csv.reader(open('Tor_query_EXPORT.csv'))][1:]
    '''

    def __init__(self, fieldlist):
        def to_int(s):
            '''Convert s to an int, mapping the string "N/A" to 0.'''
            if s == "N/A": return 0
            return int(s)
        (nick, cc, bw, uptime, ip, hostname, orport, dirport, auth, exit, fast,
         guard, named, stable, running, valid, v2dir, platform, hibernating,
         badexit) = fieldlist
        if orport == 'None': orport = -1
        if dirport == 'None': dirport = -1
        (self.nick, self.cc, self.ip, self.hostname, self.platform) = (
            nick, cc, ip, hostname, platform)
        if len(hostname) < 4:
            self.hostname = ip
            self.domain = '.'.join(ip.split('.')[:2])
        else:
            self.domain = '.'.join(hostname.split('.')[-2:])
        (self.bw, self.uptime, self.orport, self.dirport, self.auth, self.exit,
         self.fast, self.guard, self.named, self.stable, self.running,
         self.valid, self.v2dir, self.hibernating, self.badexit) = map(to_int,
            [bw, uptime, orport, dirport, auth, exit, fast, guard, named,
             stable, running, valid, v2dir, hibernating, badexit])
    def __repr__(self):
        return '%-6d %20s %2s %4s %s' % (self.bw, self.nick, self.cc,
                                         ['','exit'][self.exit], self.hostname)

if 0:
    f = open('Tor_query_EXPORT.csv')
else:
    f = os.popen('curl -s http://torstatus.blutmagie.de/query_export.php/Tor_query_EXPORT.csv')

L = map(router, list(csv.reader(f))[1:])

domains = sorted(set([i.domain for i in L]))

bw = {}
ebw = {}

for d in domains:
    bw[d] = sum([i.bw for i in L if i.domain == d])
    ebw[d] = sum([i.bw for i in L if i.domain == d and i.exit])

totbw = sum(bw[d] for d in bw)
totebw = sum(ebw[d] for d in ebw)

print "Total BW: %d MB/s Exit BW: %d MB/s Total Relays: %d Exits: %d" % \
      (totbw / 1024, totebw / 1024, len(L), len([i for i in L if i.exit]))

for (e,d) in sorted([(ebw[i], i) for i in domains], reverse=True):
    relays = sorted([(r.bw, r) for r in L if r.domain == d], reverse=True)
    for (b, r) in relays:
        print '   %s' % r
    if e > 0: print '%d\n' % e
