#!/usr/bin/python
from subprocess import Popen, PIPE
from re import search
from sys import path, argv
path.insert(0, '../lib')
import coreutils


def GetGroups(host, monitored_groups):
    """SSH to a host and get the members of monitored groups."""
    m_groups = []
    # SSH to the host and obtain the contents of /etc/group.  This
    # takes the host name provided as input, and will produce a list
    # of all groups and their members.
    groups = str(Popen(['/usr/bin/ssh', host, 'cat', '/etc/group'],
                 stdout=PIPE).stdout.read()).strip('\n').split('\n')
    # Parsses through the groups and returns the groups and members of
    # the monitored groups.
    for group in groups:
        for m_group in monitored_groups:
            if search(r'^' + m_group, group):
                m_groups.append(group)
    return m_groups


# Obtaining configuration.
conf = coreutils.GetConfig(r'../etc/CheckGroups.cnf')
# Obtaining the list of monitored groups.
monitored_groups = conf.MonitoredGroups().split(',')
# Obtaing the DBA group name.
DBA_Group = conf.GetDBAGroup()
# Obtaining the system admin group name.
SA_Group = conf.GetSecGroup()
# Obtaining the security admin group name.
Sec_Group = conf.GetSAGroup()
# Obtaining the list of authorized DBAs.
DBA_Mbrs = conf.GetDBA()
# Obtaining the list of authorized system administrators.
SA_Mbrs = conf.GetSA()
# Obtaining the list of authorized security administrators.
Sec_Mmbrs = conf.GetSecAdmin()
# Calling the GetGroup function, using sys.argv[1] as a host name and
# the monitored groups (as defined above).  The output will be a list
# of the monitored groups (including group members).
groups = GetGroups(argv[1], monitored_groups)
