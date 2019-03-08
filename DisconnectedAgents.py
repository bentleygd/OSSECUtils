#!/usr/bin/python
import smtplib
from subprocess import check_output, check_call, CalledProcessError
from socket import gaierror, gethostbyname
from tempfile import TemporaryFile

DisconnectedAgents = []
DeadAgents = []
GF = TemporaryFile()
ossec_agents = check_output([
                             '/var/ossec/bin/agent_control', '-l', '-s'
                            ]).rstrip('\n')
for agent in ossec_agents.split('\n'):
    agent_props = agent.split(',')
    agent_details = {'id': agent_props[0],
                     'name': agent_props[1].rstrip('2'),
                     'address': agent_props[2],
                     'status': agent_props[3]}

    if agent_details['status'] == 'Disconnected':        
        try:
            address = gethostbyname(agent_details['name'])
            print '%s resolves to %s' % (agent_details['name'], address)
        except gaierror:
            print 'Name resolution failed for %s' % (agent_details['name'])
            address = 'NRF' 
            DeadAgents.append(agent_details['name'])

        if not address == 'NRF':
            try:
                check_call(['ping', '-c', '1', address], stderr=GF, 
                           stdout=GF)
                print '%s is up!  Rejoice!' % (agent_details['name'])
                DisconnectedAgents.append(agent_details['name'])
            except CalledProcessError:
                print 'Unable to reach %s' % (agent_details['name'])
                DeadAgents.append(agent_details['name'])
GF.close()
print 'Dead Agents are: %s' % (str(DeadAgents))
print 'Disconnected Agents are: %s' % (str(DisconnectedAgents))
