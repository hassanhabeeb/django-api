from breathline.helpers.hashing import URLEncryptionDecryption
from breathline.helpers.helper import decode_email, encode_email
from breathline.helpers.mail_functions import SendEmails
from breathline import settings
import threading
import os


def subscription_mail(request, instance):
    try:
        user_email = instance.email
        subject = "Breathline Subscription Activated"
        unsubscribe_url = f"{settings.FRONTEND_WEB_URL}/unsubscribe"

        encoded_email = encode_email(instance.email)
        print("---",encoded_email)

        context = {
            'encode_email'     : encoded_email,
            'domain'           : settings.EMAIL_DOMAIN,
            'protocol'         : 'https',
            'logo_url'         : settings.API_URL + settings.LOGO_URL,
            'unsubscribe_url'  : unsubscribe_url,
        }

        send_email = SendEmails()
        email_thread = threading.Thread(
            target=send_email.sendTemplateEmail, 
            args=(subject, request, context, 'subscription.html', settings.EMAIL_HOST_USER, user_email)
        )
        email_thread.start()

    except Exception as e:
        print(f"Error while sending registration email: {str(e)}")
        pass