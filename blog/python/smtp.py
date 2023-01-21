import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string


def send_mail():
    port = 465
    smtp_server = 'smtp.gmail.com'
    smtp_email = 'jnunes.developer@gmail.com'

    sender_mail = f'Marcio Jiodan <{smtp_email}>'
    receiver_email = 'jarnunesc@gmail.com'
    subject = 'Subject'

    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = sender_mail
    message['To'] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = render_to_string('emails/template.html', context={'name': 'Jardel Nunes'})

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(smtp_email, 'grscpekqbjxmwbxg')
        server.sendmail(sender_mail, receiver_email, message.as_string())

    print('HEY MAIL HAS BEEN SENT')

#
# def main():
#     send_mail()
#
#
# if __name__ == '__main__':
#     main()
