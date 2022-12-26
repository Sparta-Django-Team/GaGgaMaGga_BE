from django.core.mail import EmailMessage

import urllib.request
import requests
import tempfile
import threading

from gaggamagga.settings import get_secret

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

    def profile_image_download(url):
        response = requests.get(url, stream=True)
        file_name = ''.join(url.split('/')[-2:])
        temp_image = tempfile.NamedTemporaryFile() 
        for block in response.iter_content(1024 * 8):
            if not block:
                break
            temp_image.write(block)
        return {"temp_image": temp_image, "file_name": file_name}
    
    def find_ip_country(user_ip):
        serviceKey = get_secret("WHOIS_KEY")
        url = "http://apis.data.go.kr/B551505/whois/ip_address?serviceKey=" + serviceKey + "&query=" + user_ip + "&answer=json"
        request = urllib.request.urlopen(url).read().decode("utf-8")
        return dict(eval(request))["response"]["whois"]["countryCode"]

