#!/usr/bin/python
import os
import re
import pprint
from subprocess import Popen, PIPE, call

point = os.environ['HOST']
model = os.environ['API_NAME']
log_file = os.environ['LOG_FILE']
report_file = os.environ['REPORT_FILE']


def system(command):
    "run system command. return [code, STDOUT, STDERR ]"
    proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    ls = proc.communicate()
    rc = proc.wait()
    OUT_BUF=ls[0]
    ERR_BUF=ls[1]
    return [rc, OUT_BUF, ERR_BUF]


if __name__ == '__main__':
     
    with open('%s' % model, 'r') as fin:
	st = fin.readlines()

    lapi = []
    for r in st:
	s = r.strip()
	if s:
	    s = re.split(',| ', s)   # s.split(',')
	    if s[0][0] != '#':
 		lapi.append(s)

    pprint.pprint(lapi)
    print '---------------'
    p = re.compile('{[A-Za-z0-9_]*}')

    lapi2 = []   
    for r in lapi:
	try:
	    s = r.pop()
	    s1 = p.sub('.*', s)
	    lapi2.append([r[0], s1])
	except IndexError as e:
	    print '==============> ERROR: %s =========== %s' % (e,s) 
	    
    # pprint.pprint(lapi2)

    rr = []
    used = 0 	
    for r in lapi2:
        parm1 = "'%s %s'" % (r[0], point) 
	cmd = 'grep %s %s | grep %s | wc -l' % (parm1, log_file, r[1])
        print cmd
	res = system(cmd)
        cnt = int(res[1].strip())
	if cnt > 0:
	    used += 1
	sres = '%s \t %s' % (res[1].strip(), cmd)
	rr.append(sres)
	
    # print 'cmd:%s res:%s' % (cmd, res[1])

    with open('%s' % report_file, 'w') as fout:
	total_api = len(rr)
	for r in rr:
	    fout.write('%s\n' % r)
	fout.write('\n\n ---------------------------\n')
	fout.write('used: %s\n' % used)
	fout.write('API total: %s\n' % total_api)
        prc = float(used)*100/float(total_api)
	fout.write('Coverage: %.2f%%\n' % prc)
	print 'Repport file: [%s] was succesfully created.' % report_file

