from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=settings.EMAIL_HOST_USER,
            to=[data['to_email']]
        )
        email.send()

    @staticmethod
    def send_mail_after_registration(email, auth_token, fname):
        subject = 'Your accounts need to be verified'
        link = f'https://311alert.info/verify/{auth_token}'

        context = {
            "link": link,
            "fname": fname,
        }

        from_email = settings.EMAIL_HOST_USER

        templ = get_template('templetext.txt')
        messageing = templ.render(context)
        emailnew = EmailMultiAlternatives(
            subject, messageing, "Verify Email", [from_email, email],)

        emailnew.content_subtype = 'html'
        emailnew.send()
