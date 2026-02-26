from breathline.helpers.mail_functions import SendEmails
from breathline import settings
import threading
import os


def communication_mail(request, name, email, message, phonenumber, service_category, instance ):
    try:
        admin_email  = settings.ADMIN_REPLY_MAIL if settings.ADMIN_REPLY_MAIL else "sreezodiac@gmail.com" 
        mail_subject = "Support Mail from Breathline"

        if service_category == "sleep_apnea":
            service_category = "Sleep Apnea"
        elif service_category == "adhd_treatment":
            service_category = "ADHD Treatment"
        elif service_category == "anxiety_and_depression":
            service_category = "Anxiety And Depression"
        elif service_category == "uars_treatment":
            service_category = "UARS Treatment"

        context = {
            'email'            : admin_email,
            'user_email'       : email,
            'instance'         : instance,
            'name'             : name,  
            'message'          : message,
            'phonenumber'      : phonenumber,  
            'service_category' : service_category,
            'domain'           : settings.EMAIL_DOMAIN,
            'logo_url'         : settings.API_URL + settings.LOGO_URL,
            'protocol'         : 'https',
        }

        send_email = SendEmails()
        email_thread = threading.Thread(
            target=send_email.sendTemplateEmail, 
            args=(mail_subject, request, context, 'communication.html', settings.EMAIL_HOST_USER, admin_email)
        )
        email_thread.start()

    except Exception as e:
        print(f"Error while sending registration email: {str(e)}")
        pass