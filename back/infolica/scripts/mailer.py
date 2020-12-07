
import smtplib
from email.message import EmailMessage
from email.utils import formatdate

def send_mail(request, mail_list, text, subject):
    """
    mail_list: list of mail adresses (send to)
    text: Mail text. Note that mail footer is set to "Ce mail est généré automatiquement. Ne pas répondre à cette adresse e-mail."
    subject: mail subject
    """
    text += "\n\nCe mail est généré automatiquement.\nNe pas répondre à cette adresse e-mail."
    msg = EmailMessage()
    msg['From'] = request.registry.settings["infolica_mail"]
    msg['To'] = ', '.join(mail_list)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.set_content(text)
    s = smtplib.SMTP(request.registry.settings["infolica_smtp"])
    s.send_message(msg)
    s.quit()