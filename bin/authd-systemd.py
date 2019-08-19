#!/usr/bin/python
# This is a python script that will handle starting/stopping of authd
# for systemd.
from os import remove, kill
from time import sleep
from re import search, match
from sys import argv
from subprocess import Popen, PIPE


# This function starts the ossec-authd daemon by making a system call. The
# path variables define command line arguments for the ossec authd daemon.
def AuthdStart():
    key_path = 'PATH_TO_OSSEC_SSL_KEY'
    cert_path = 'PATH_TO_OSSEC_SSL_CERT'
    authd_log = open('/tmp/authd.log', 'w+b')
    authd_start = ['/var/ossec/bin/ossec-authd', '-n', '-i', '-x', cert_path,
                   '-k', key_path]
    print('Starting ossec-authd...')
    Popen(authd_start, stdout=authd_log, stderr=authd_log)
    for proc in Popen(['/bin/ps', 'aux'], stdout=PIPE).stdout:
        if search('ossec-authd', proc):
            ossec_authd_pid = proc.split()[1]
    authd_log.write('AUTHD_PID is ' + str(ossec_authd_pid) + '\n')
    sleep(1)


# This function stops ossec by making a system call to kill the ossec-authd
# process.  Note that we are using killall, so we are killing the process
# based on name rather than process id.
def AuthdStop():
    print('Stopping ossec-authd...')
    for proc in Popen(['/bin/ps', 'aux'], stdout=PIPE).stdout:
        if search('ossec-authd', proc):
            authd_pid = proc.split()[1]
    kill(int(authd_pid), 15)
    remove('/tmp/authd.log')


# This function checks on the status of the ossec-authd daemon running as
# a service by checking to see if the authd log file exists (which is
# created when authd starts) and checks whether or not a process that
# matches ossec-authd is running.
def AuthdStatus():
    procs = []
    for process in Popen(['/bin/ps', 'aux'], stdout=PIPE).stdout:
        if search('ossec-authd', process):
            procs.append(process)
    if len(procs) > 0:
        print 'ossec-authd is running'
    else:
        print 'ossec-authd is not running'


# This is some boolean logic that takes input provided in the first argument
# and determines (based on that input) what to do to the ossec-authd daemon.
# Note that the first argument (argv[0]) is the script name.  If invalid
# input is proved to argv[1], the script prints usage.
if match('start', str(argv[1]).lower()):
    AuthdStart()
elif match('stop', str(argv[1]).lower()):
    AuthdStop()
elif match('restart', str(argv[1]).lower()):
    AuthdStop()
    sleep(3)
    AuthdStart()
elif match('status', str(argv[1]).lower()):
    AuthdStatus()
else:
    print('Usage: %s (start|stop|restart|status)' % (argv[0]))
    exit(1)
