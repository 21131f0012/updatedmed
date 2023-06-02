from django.core.mail import EmailMessage, message
from django.conf import settings
from django.template.loader import render_to_string

def send_notification(mail_subject,mail_template,context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    if(isinstance(context['to_email'], str)):
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']
    mail = EmailMessage(mail_subject, message, from_email, to=to_email)
    # mail.content_subtype = "html"
    mail.send()