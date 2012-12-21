from celery import task
import base.email_templates as emails
from django.core.mail import send_mail, mail_admins, mail_managers, BadHeaderError
from django.conf import settings

# Send an email with a specified template
@task()
def send_email(template_name, recipient, email_args):
    if template_name not in emails.email_types:
        raise LookupError('Email template type not supported')
    template = emails.email_types[template_name]['template']
    try:
        send_mail(emails.email_types[template_name]['subject'],
                       template % tuple(email_args), settings.SERVER_EMAIL, [recipient])
    except TypeError:
        raise TypeError('One or more email arguments are invalid')
    except BadHeaderError:
       raise BadHeaderError('Invalid header found.')

# Send an email to the admins, managers, or both
@task()
def backend_email(template_name, group_type, email_args):
    if template_name not in emails.email_types:
        raise LookupError('Email template type not supported')
    template = emails.email_types[template_name]['template']
    subject = emails.email_types[template_name]['subject']
    try:
        message = template % tuple(email_args)
        if 'admins' in group_type: mail_admins(subject, message)
        if 'managers' in group_type: mail_managers(subject, message)
    except TypeError:
        raise TypeError('One or more email arguments are invalid')
    except BadHeaderError:
       raise BadHeaderError('Invalid header found.')