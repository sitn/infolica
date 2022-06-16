
import smtplib
from email.message import EmailMessage
from email.utils import formatdate

def send_mail(request, mail_list, text, subject, html=None, signature='Infolica'):
    """
    mail_list: list of mail adresses (send to)
    text: Mail text. Note that mail footer is set to "Ce courrier a été généré automatiquement. Merci de ne pas y répondre."
    subject: mail subject
    """
    text += "\n\nMeilleures salutations,\nInfolica\n\nCe courrier a été généré automatiquement. Merci de ne pas y répondre."
    msg = EmailMessage()
    msg['From'] = request.registry.settings["infolica_mail"]
    msg['To'] = ', '.join(mail_list)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.set_content(text)
    if html:
        msg.add_alternative("""
            <html>
                <head></head>
                <body>{}<br><br>Meilleures salutations,<br>{}<br><br><em style="font-size: 14px;">Ce courrier a été généré automatiquement. Merci de ne pas y répondre.</em></body>
            </html>
        """.format(html, signature), subtype="html")
    s = smtplib.SMTP(request.registry.settings["infolica_smtp"])
    s.send_message(msg)
    s.quit()