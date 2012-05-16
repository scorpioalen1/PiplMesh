import json, urlparse, urllib

from django.conf import settings
from django.core import urlresolvers

from mongoengine.django import auth

from piplmesh.account import models

class MongoEngineBackend(auth.MongoEngineBackend):
    # TODO: Implement object permission support
    supports_object_permissions = False
    # TODO: Implement anonymous user backend
    supports_anonymous_user = False
    # TODO: Implement inactive user backend
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        user = self.user_class.objects(username__iexact=username).first()
        if user:
            if password and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return self.user_class.objects.with_id(user_id)
        except self.user_class.DoesNotExist:
            return None


    @property
    def user_class(self):
        return models.User

class FacebookBackend(MongoEngineBackend):
    def authenticate(self, token=None, request=None):
        """
        Facebook authentication.

        Retrieves an access token and Facebook data. Determine if user already has a
        profile. If not, a new profile is created using either the user's
        username or Facebook id. Finally, the user's Facebook data is saved.
        """
    
        args = {
            'client_id': settings.FACEBOOK_APP_ID,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'redirect_uri': request.build_absolute_uri(urlresolvers.reverse('facebook_callback')),
            'code': token,
        }
    
        # Retrieve access token
        url = urllib.urlopen('https://graph.facebook.com/oauth/access_token?%s' % urllib.urlencode(args)).read()
        response = urlparse.parse_qs(url)
        access_token = response['access_token'][-1]
    
        # Retrieve user's public profile information
        data = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % access_token)
        fb = json.load(data)
        
        # TODO: Check if id and other fields are returned
        # TODO: Move user retrieval/creation to User document/manager
        # TODO: get_or_create implementation has in fact a race condition, is this a problem?
        user, created = self.user_class.objects.get_or_create(
            facebook_id=fb.get('id'),
            defaults={
                'username': fb.get('username', fb.get('first_name') + fb.get('last_name')),
                'first_name': fb.get('first_name'),
                'last_name': fb.get('last_name'),
                'email': fb.get('email'),
                'gender': fb.get('gender'),
            }
        )
        user.facebook_token = access_token
        user.save()

        return user



import tweepy

class TwitterBackend(MongoEngineBackend):
    """TwitterBackend for authentication
    """
    def authenticate(self, access_token=None, request=None):
        user, created = self.user_class.objects.get_or_create(
            facebook_id = request.GET['user_id'],
            defaults = {
                'username' : request.GET['screen_name'],
            }
        )
        user.facebook_token = (access_token.key, access_token.secret)
        user.save()
        return user


