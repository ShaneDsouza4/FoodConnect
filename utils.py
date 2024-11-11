import time
from django.conf import settings
from django.core.mail import send_mail, EmailMessage

def send_email_to_us(subject, message, recipient_list):
	mail = EmailMessage(
		subject=subject,
		body=message,
		from_email=settings.EMAIL_HOST_USER,
		to=['sdsouzasc1996@gmail.com'], #Our company email to handle contatu queries
		reply_to=recipient_list
	)
	mail.send()