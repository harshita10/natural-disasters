# -*- coding: UTF-8 -*-
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import smtplib
from os import path


############################################################################
class Email(object):

    # ----------------------------------------------------------------------
    def __init__(self, filepath, toAddress):
        msg = MIMEMultipart('alternative')
        textMessage = """

        Please see attached Eonet Report.\n
        """
        text = MIMEText(textMessage, "plain")
        msg.attach(text)

        attachment = MIMEBase('application', "octet-stream")
        attachment.set_payload(open(filepath,"rb").read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition',
                              'attachment; filename="{}"'.format(
                                  path.basename(filepath)))
        msg.attach(attachment)


        msg['From'] = "no-reply@maplecroft.com"
        msg['To'] = toAddress
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = "Eonet Data"

        self.msg = msg

    # ----------------------------------------------------------------------
    def send(self, remoteserver="127.0.0.1"):
        try:
            smtp = smtplib.SMTP(remoteserver)
        except smtplib.socket.error as e:
            if e.errno == 111:
                print(
                    "Socket Error while attempting to send an email"
                    "- Probably unable to locate the mail server {}".format(
                        remoteserver)
                )
                raise
        try:
            smtp.sendmail(self.msg['From'],
                          self.msg['To'],
                          self.msg.as_string()
                          )
        except smtplib.SMTPRecipientsRefused as e:
            print(
                "SMTPRecipientsRefused while attempting to" +
                " send an email - Probably a blank email address {}".format(
                    self.msg['To'])
        )
            raise

        smtp.close()