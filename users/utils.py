from django.core.mail import EmailMessage
from django.core.files import File

import requests
import tempfile
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

    def profile_image_download(url):
        response = requests.get(url, stream=True)
        file_name = ''.join(url.split('/')[-2:]) #파일명으로 사용
        temp_image = tempfile.NamedTemporaryFile() #임시파일 생성
        for block in response.iter_content(1024 * 8): #이미지 response를 분할로 받기 위함
            if not block:
                break
            temp_image.write(block)
        return {"temp_image": temp_image, "file_name": file_name}