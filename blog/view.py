import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import get_access_token_model
from oauth2_provider.signals import app_authorized
from oauth2_provider.views.base import TokenView

from post.models import Profile


class TokenViewWithUserInfo(TokenView):
    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_token_response(request)
        if status == 200:
            body = json.loads(body)
            access_token = body.get("access_token")
            if access_token is not None:
                token = get_access_token_model().objects.get(
                    token=access_token)
                app_authorized.send(
                    sender=self, request=request,
                    token=token)
                try:
                    profile = Profile.objects.get(user__id=token.user.id)
                    body['id'] = str(token.user.id)
                    body['username'] = str(token.user.username)
                    body['profile_id'] = str(profile.id)
                    body = json.dumps(body)
                except Profile.DoesNotExist:
                    body['id'] = str(token.user.id)
                    body['username'] = str(token.user.username)
                    body = json.dumps(body)
        response = HttpResponse(content=body, status=status)
        for k, v in headers.items():
            response[k] = v
        return response

# This is for FB and Google OATH
# class ConvertTokenViewInfo(ConvertTokenView):
#     def post(self, request, *args, **kwargs):
#         url, headers, body, status = self.create_token_response(request)
#
#         if request.data['backend'] == 'google-oauth2':
#
#             if status == 200:
#                 body = json.loads(body)
#                 access_token = body.get("access_token")
#                 if access_token is not None:
#                     token = get_access_token_model().objects.get(
#                         token=access_token)
#                     app_authorized.send(
#                         sender=self, request=request,
#                         token=token)
#
#                     try:
#                         profile = Profile.objects.get(user__id=token.user.id)
#                         body['id'] = str(token.user.id)
#                         body['username'] = str(token.user.username)
#                         body['profile_id'] = str(profile.id)
#                     except Profile.DoesNotExist:
#                         params = {'access_token': request.data['token']}
#                         google_profile = 'https://www.googleapis.com/oauth2/v3/userinfo?'
#                         r_google = requests.get(google_profile, params=params)
#                         profile_google = r_google.json()
#                         my_user = User.objects.get(id=token.user.id)
#                         profile = Profile.objects.create(
#                             first_name=profile_google['given_name'],
#                             last_name=profile_google['family_name'],
#                             email=profile_google['email'],
#                             birth_date=date.today(),
#                             gender='Rather not to say',
#                             user=my_user
#                         )
#                         body['id'] = str(token.user.id)
#                         body['username'] = str(token.user.username)
#                         body['profile_id'] = str(profile.pk)
#                     body = json.dumps(body)
#
#         if request.data['backend'] == 'facebook':
#             if status == 200:
#                 body = json.loads(body)
#                 access_token = body.get("access_token")
#                 if access_token is not None:
#                     token = get_access_token_model().objects.get(
#                         token=access_token)
#                     app_authorized.send(
#                         sender=self, request=request,
#                         token=token)
#                     try:
#                         profile = Profile.objects.get(user__id=token.user.id)
#                         body['id'] = str(token.user.id)
#                         body['username'] = str(token.user.username)
#                         body['profile_id'] = str(profile.id)
#                     except Profile.DoesNotExist:
#                         my_user = User.objects.get(id=token.user.id)
#                         profile = Profile.objects.create(
#                             first_name=my_user.first_name,
#                             last_name=my_user.last_name,
#                             email=my_user.email,
#                             birth_date=date.today(),
#                             gender='Rather not to say',
#                             user=my_user
#                         )
#                         body['id'] = str(token.user.id)
#                         body['username'] = str(token.user.username)
#                         body['profile_id'] = str(profile.pk)
#                     body = json.dumps(body)
#
#         response = HttpResponse(content=body, status=status)
#         for k, v in headers.items():
#             response[k] = v
#         return response
