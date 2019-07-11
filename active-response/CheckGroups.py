#!/usr/bin/python
from re import search
from smtplib import SMTP
from socket import gethostbyname
from email.mime.text import MIMEText
from ldap import initialize, SCOPE_SUBTREE

class LDAPConfig:
    """Config class for LDAP stuff"""
    def __init__(self, file_name):
        self.fl = file_name

    def LDAP_URL(self):
        """Get the URL of the LDAP server"""
        config = open(self.fl, 'r+b')
        for line in config:
            lurl = search(r'(^LDAP_URL: )(\S+)', line)
            if lurl:
                return lurl.group(2)
        config.close()

    def LDAP_Pass(self):
        """Password for the user connecting to the LDAP server."""
        config = open(self.fl, 'r+b')
        for line in config:
            ldap_secret = search(r'(^PASS: )(\S+)', line)
            if ldap_secret:
                return ldap_secret.group(2)
        config.close()

    def LDAP_BDN(self):
        """Get the LDAP Bind DN."""
        config = open(self.fl, 'r+b')
        for line in config:
            ldapbdn = search(r'(^BIND_DN: )(.+)', line)
            if ldapbdn:
                return ldapbdn.group(2)
        config.close()

class GetGroupConfig:
"""Config class for main script"""
    def __init__(self, filename)
    self.fn = filename

    def MonitoredGroups(self):
    """Get the groups to monitor"""
    config = open(self.fn, 'r+b')
    for line in config:
        m_groups = search(r'(^Monitored_Groups: )(.+)', line)
        if mgroups:
            return m_groups.group(2)
    config.close()

    def GetDBAGroup(self):
    """Get the DBA group"""
    config = open(self.fn, 'r+b')
    for line in config:
        dba_group = search(r'(^DBAs: )(.+)', line)
        if dba_group:
            return dba_group.group(2)
    config.close()

    def GetSAGroup(self):
    """Get the sys admins"""
    config = open(self.fn, 'r+b')
    for line in config:
        sa_group = search(r'SAs: )(.+)', line)
            if sa_group:
                return sa_group.group(2)
    config.close()

    def GetSecAdmins(self):
    """Get the security admins"""
    config = open(self.fn, 'r+b')
    for line in config:
        sec_admins = search(r'SecAdmin: )(.+)', line)
            if sec_admin:
                return sec_admins.group(2)
    config.close()

    def GetMailSender(self):
    """Gets mail sender"""
    config = open(self.fn, 'r+b')
    for line in config:
        sender = search(r'MailSender: )(.+)', line)
            if sender:
                return sender.group(2)
    config.close()

    def GetReportRcpts(self):
    """Gets report recipients"""
    config = open(self.fn, 'r+b')
    for line in config:
        rcpts = search(r'Recipients: )(.+)', line)
        if rcpts:
            return rcpts.group(2)
    config.close()

    def GetSMTPServer(self):
    """Get a SMTP server name from config"""
    config = open(self.fn, 'r+b')
    for line in config:
        smtpserver = search(r'SMTP: )(.+)', line)
        if smtpserver:
            return smtpserver.group(2)
    config.close()

def MailSend(sender, recipients, mailbody):
    """Simple function to send mail."""
    mail_sender = sender
    mail_recipients = recipients
    msg = MIMEText(mail_body)
    msg['Subject'] = 'Unauthorized Admin Added to Admin Group'
    msg['From'] = sender
    msg['To'] = recipients
    s = SMTP(gethostbyname('some.servername.com'), '25')
    s.sendmail(sender, recipients, msg.as_string())
    s.quit
