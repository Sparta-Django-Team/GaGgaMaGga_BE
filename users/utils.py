from rest_framework_simplejwt.tokens import RefreshToken

import urllib.request
import requests
import tempfile
from datetime import datetime

from gaggamagga.settings import get_secret
from .models import ConfirmEmail
from .tasks import send_email


class Util:

    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def profile_image_download(url):
        response = requests.get(url, stream=True)
        file_name = ''.join(url.split("/")[-2:])
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
    
    def email_authentication_send(user):
        secured_key = RefreshToken.for_user(user).access_token
        expired_at = datetime.fromtimestamp(secured_key["exp"]).strftime("%Y-%m-%dT%H:%M:%S")

        ConfirmEmail.objects.create(secured_key=secured_key, expired_at=expired_at, user=user)

        frontend_site = "www.gaggamagga.shop" 
        absurl = f"https://{frontend_site}/confirm_email.html?secured_key={str(secured_key)}"
        email_body = "안녕하세요!" + user.username +"고객님 이메일인증을 하시려면 아래 사이트를 접속해주세요 \n" + absurl
        message = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "이메일 인증",
            }
        send_email.delay(message)