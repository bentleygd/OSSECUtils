#!/usr/bin/python
from subprocess import check_output, check_call, CalledProcessError
from socket import gaierror, gethostbyname
from tempfile import TemporaryFile
from email.mime.text import MIMEText
import argparse
import smtplib

def GetDisconnectedAgents():
    '''Gets disconnected OSSEC agents.'''
# Declaring list variables to be used later on.
    DisconnectedAgents = []

# Creating a temporary file.
    GF = TemporaryFile()

# Running an OSSEC command and parsing through the output, which will
# be passed to a socket function to perform DNS resolution.  If
# succesful, we pass the IP address to ping. Note that printing is for
# debugging purposes and should be removed prior to final publish.

    ossec_agents = check_output([
                                 '/var/ossec/bin/agent_control', '-l', '-s'
                                ]).rstrip('\n')
    for agent in ossec_agents.split('\n'):
        agent_props = agent.split(',')
        agent_status = agent_props[3]
        agent_name = agent_props[1].rstrip('2')

        if agent_status == 'Disconnected':        
            try:
                address = gethostbyname(agent_name)
            except gaierror:
                address = 'NRF' 

            if not address == 'NRF':
                try:
                    check_call(['ping', '-c', '1', address], stderr=GF, 
                               stdout=GF)
                    DisconnectedAgents.append(agent_name)
                except CalledProcessError:
                    pass
    GF.close()
    return DisconnectedAgents

def GetDeadAgents():
    '''Gets dead OSSEC agents.'''
# Declaring list variables to be used later on.
    DeadAgents = []

# Creating a temporary file.
    GF = TemporaryFile()

# Running an OSSEC command and parsing through the output, which will
# be passed to a socket function to perform DNS resolution.  If
# succesful, we pass the IP address to ping.

    ossec_agents = check_output([
                                 '/var/ossec/bin/agent_control', '-l', '-s'
                                ]).rstrip('\n')
    for agent in ossec_agents.split('\n'):
        agent_props = agent.split(',')
        agent_status = agent_props[3]
        agent_name = agent_props[1].rstrip('2')

        if agent_status == 'Disconnected':
            try:
                address = gethostbyname(agent_name)
            except gaierror:
                address = 'NRF'
                DeadAgents.append(agent_name)

            if not address == 'NRF':
                try:
                    check_call(['ping', '-c', '1', address], stderr=GF, 
                               stdout=GF)
                except CalledProcessError:
                    DeadAgents.append(agent_name)
    GF.close()
    return DeadAgents

def EmailAgentStatus(StatusCheck, AgentList):
    '''Emails list of agents that require attention.'''
    sender = 'sender@example.com'
    recipients = 'recipient@example.com'
    mail_body = ('Below is the list of %s agents:\n\n\n\n') % (StatusCheck)
    mail_body = mail_body + str(AgentList).strip('[]')
    msg = MIMEText(mail_body)
    msg['Subject'] = '%s OSSEC Agents' % (StatusCheck.capitalize())
    msg['From'] = sender
    msg['To'] = recipients
    s = smtplib.SMTP(gethostbyname('smtpserver.example.com'), '25')
    s.sendmail(sender, recipients, msg.as_string())
    s.quit

# Setting up an argument parser.
a_parser = argparse.ArgumentParser()
a_parser.add_argument('status', help='The agent status to check for. e.g.,\
                      disconnected or dead.')
args = a_parser.parse_args()

# Getting disconnected or dead agents and emailing them.
if args.status == 'disconnected':
    AgentList = GetDisconnectedAgents()
    EmailAgentStatus(args.status, AgentList)
elif args.status == 'dead':
    AgentList = GetDeadAgents()
    EmailAgentStatus(args.status, AgentList)
else:
    print 'Invalid agent status.  The status must be dead or disconnected.'
    exit(1)
