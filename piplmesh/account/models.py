import datetime, hashlib, urllib

from django.conf import settings
from django.contrib.sites import models as sites_models

import mongoengine
from mongoengine.django import auth

from piplmesh.account import utils, fields

LOWER_DATE_LIMIT = 366 * 120

POST_MESSAGE_MAX_LENGTH = 500
COMMENT_MESSAGE_MAX_LENGTH = 300

class User(auth.User):
    birthdate = fields.LimitedDateTimeField(upper_limit=datetime.datetime.today(), lower_limit=datetime.datetime.today() - datetime.timedelta(LOWER_DATE_LIMIT))
    gender = fields.GenderField()
    language = fields.LanguageField()
    
    facebook_id = mongoengine.IntField()
    facebook_token = mongoengine.StringField(max_length=150)
    
    def profile_image_url(self, size='square', request=None, is_secure=False, default_url=''):
        """
        Returns users profile image url.
        
        ``size`` can have a value of "square" (50x50), "small" (50 pixels wide, variable height), 
        "normal" (100 pixels wide, variable height) and "large" (200 pixels wide, variable height).
        
        `default_url`` must be whole url (eg. www.wlan-si.net/images/default.png) without ``http://``
        """
        
        if request:
            if sites_models.Site._meta.installed:
                domain = sites_models.Site.objects.get_current().domain
            else:
                domain = sites_models.RequestSite(request).domain
                
            is_secure = request.is_secure()
            default_url = '%s/%s/piplmesh/images/unknown.png' % (domain, settings.STATIC_URL)
        
        if self.facebook_id:
            return '%s?type=%s' % (utils.graph_api_url('%s/picture' % self), size)
        else:
            return 'http%(secure)s://secure.gravatar.com/avatar/%(email_hash)s?s=%(size)s&d=http%(secure)s%(default_url)s' % {
                'secure': 's' if is_secure else '',
                'email_hash': hashlib.md5(self.email.lower()).hexdigest(),
                'size': (50, 50, 100, 200)[('square', 'small', 'normal', 'large').index(size)],
                'default_url': urllib.quote('://' + default_url),
            }

class Comment(mongoengine.EmbeddedDocument):
    """
    This class defines document type for comments on wall posts.
    """

    created_time = mongoengine.DateTimeField(default=lambda: datetime.datetime.now())
    author = mongoengine.ReferenceField(User, required=True)
    message = mongoengine.StringField(max_length=COMMENT_MESSAGE_MAX_LENGTH)

class Post(mongoengine.Document):
    """
    This class defines document type for posts on a wall.
    """

    author = mongoengine.ReferenceField(User, required=True)
    created_time = mongoengine.DateTimeField(default=lambda: datetime.datetime.now())
    updated_time = mongoengine.DateTimeField()
    comments = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Comment))

class TextPost(Post):
    """
    This class defines document type for text posts.
    """

    message = mongoengine.StringField(max_length=POST_MESSAGE_MAX_LENGTH)

class ImagePost(Post):
    """
    This class defines document type for image posts.
    """

    image_path = mongoengine.StringField()

class LinkPost(Post):
    """
    This class defines document type for link posts.
    """

    link_url = mongoengine.URLField()  
    link_caption = mongoengine.StringField()
    link_description = mongoengine.StringField()