from django.core.mail import EmailMessage

import threading

class EmailThread(threading.Thread):
    
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
        
    def run(self):
        self.email.send()

class Util:
    @staticmethod
    def send_email(message):
        email = EmailMessage(subject=message['email_subject'], body=message['email_body'], to=[message['to_email']])
        EmailThread(email).start()

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip