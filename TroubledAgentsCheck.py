#!/usr/bin/python
from subprocess import check_output, check_call, CalledProcessError
from socket import gaierror, gethostbyname
from tempfile import TemporaryFile
from email.mime.text import MIMEText
import argparse
import smtplib

def GetTroubledAgents(StatusCheck):
    '''Gets disconnected or dead OSSEC agents.'''
# Creating empty list variables to be used later on.
    DisconnectedAgents = []
    DeadAgents = []

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
                DeadAgents.append(agent_name)

            if not address == 'NRF':
                try:
                    check_call(['ping', '-c', '1', address], stderr=GF, 
                               stdout=GF)
                    DisconnectedAgents.append(agent_name)
                except CalledProcessError:
                    DeadAgents.append(agent_name)
    GF.close()
    if StatusCheck == 'disconnected':
        return DisconnectedAgents
    elif StatusCheck == 'dead':
        return DeadAgents
    else:
        print('Invalid agent status.  Valid checks are for dead or ' +
               'disconnected agents.')


def EmailAgentStatus(StatusCheck, AgentList):
    '''Emails list of agents that require attention.'''
    sender = 'OSSECAgentCheck@24hourfit.com'
    recipients = 'gbentley@24hourfit.com'
    mail_body = ('Below is the list of %s agents:\n\n\n\n') % (StatusCheck)
    for agent in AgentList:
        mail_body = mail_body + agent + '\n'
    msg = MIMEText(mail_body)
    msg['Subject'] = '%s OSSEC Agents' % (StatusCheck.capitalize())
    msg['From'] = sender
    msg['To'] = recipients
    s = smtplib.SMTP(gethostbyname('mailvip.24hourfit.com'), '25')
    s.sendmail(sender, recipients, msg.as_string())
    s.quit

# Setting up an argument parser.
a_parser = argparse.ArgumentParser()
a_parser.add_argument('status', help='The agent status to check for. e.g.,\
                      disconnected or dead.')
args = a_parser.parse_args()

# Getting disconnected or dead agents and emailing them.
AgentList = GetTroubledAgents(args.status)
EmailAgentStatus(args.status, AgentList)
