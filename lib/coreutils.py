from email.mime.text import MIMEText
from socket import gethostbyname
from re import search
from smtplib import SMTP


class GetConfig:
    """A configuration class"""
    def __init__(self, file_location):
        self.fn = file_location

    def MonitoredGroups(self):
        """Get the groups to monitor"""
        config = open(self.fn, 'r+b')
        for line in config:
            m_groups = search(r'(^Monitored_Groups: )(.+)', line)
            if m_groups:
                return m_groups.group(2)
        config.close()

    def GetDBAGroup(self):
        """Gets the DBA group"""
        config = open(self.fn, 'r+b')
        for line in config:
            dba = search(r'(^DBA_Group: )(.+)', line)
            if dba:
                return dba.group(2)
        config.close()

    def GetSAGroup(self):
        """Gets the SA group"""
        config = open(self.fn, 'r+b')
        for line in config:
            SA_Group = search(r'SA_Group: )(.+)', line)
            if SA_Group:
                return SA_Group.group(2)
        config.close()

    def GetSecGroup(self):
        """Gets the SecAdmin group"""
        config = open(self.fn, 'r+b')
        for line in config:
            sec_group = search(r'(^SecAdm_Group: )(.+)', line)
            if sec_group:
                return sec_group.group(2)
        config.close()

    def GetDBA(self):
        """Gets the members of the DBA group"""
        config = open(self.fn, 'r+b')
        for line in config:
            dba_group = search(r'(^DBAs: )(.+)', line)
            if dba_group:
                return dba_group.group(2)
        config.close()

    def GetSA(self):
        """Get the members of the sys admin group"""
        config = open(self.fn, 'r+b')
        for line in config:
            sa_group = search(r'SAs: )(.+)', line)
            if sa_group:
                return sa_group.group(2)
        config.close()

    def GetSecAdmin(self):
        """Get the members fo the security admin group"""
        config = open(self.fn, 'r+b')
        for line in config:
            sec_admins = search(r'SecAdmin: )(.+)', line)
            if sec_admins:
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


def MailSend(mail_sender, mail_recipients, subject, mail_server, mail_body):
    """Simple function to send mail."""
    # Defining mail properties.
    msg = MIMEText(mail_body)
    msg['Subject'] = subject 
    msg['From'] = mail_sender
    msg['To'] = mail_recipients
    # Obtaining IP address of SMTP server host name.  If using an IP
    # address, omit the gethostbyname function.
    s = SMTP(gethostbyname(mail_server), '25')
    # Sending the mail.
    s.sendmail(mail_sender, mail_recipients, msg.as_string())
