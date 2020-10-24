from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse, urlparse
import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden
from authapp.models import ShopUserProfile, ShopUser
from django.core.files.base import ContentFile



def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_200', 'domain')),
                                                access_token=response['access_token'],
                                                v='5.92')), None))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data['sex']:
        user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

    if data['about']:
        user.shopuserprofile.aboutMe = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    if data['domain']:
        user.shopuserprofile.vk_link = f"https://vk.com/{data['domain']}"

    if data['photo_200']:
        img_url = data['photo_200']
        name = urlparse(img_url).path.split('/')[-1]

        response = requests.get(img_url)
        if response.status_code == 200:
            user.avatar.save(name, ContentFile(response.content), save=True)

        print(requests.get(data['photo_200']))
        print(data['photo_200'])

    user.save()
