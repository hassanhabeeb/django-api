from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


"""------------------------------ EMAIL SENDING ---------------------------------------------"""

class SendEmails:
    
    def __init__(self, *args, **kwargs):
        pass
    
    
    def sendTemplateEmail(self, subject, request, context, template, email_host, user_email, pdf_attachment=None):
        sending_status = False
        try:
            context = context
            # Handle the request object being None
            if request is not None:
                image = request.build_absolute_uri("/")
                context['image'] = str(image) + ''
            else:
                context['image'] = ''  

            html_content = render_to_string(str(template), {'context': context})
            text_content = strip_tags(html_content)
            send_e = EmailMultiAlternatives(str(subject), text_content, email_host, [str(user_email)])
            send_e.attach_alternative(html_content, "text/html")

            if pdf_attachment:
                send_e.attach(f"invoice_{user_email}.pdf", pdf_attachment.getvalue(), 'application/pdf')

            send_e.send()
            sending_status = True
            print("email send succesfull",user_email)
        except Exception as es:
            print('Error in email thread:', es)
        return sending_status
        
