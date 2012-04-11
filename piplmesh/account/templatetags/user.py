from django import template

from piplmesh.account.templatetags import facebook
from piplmesh.frontend.templatetags import gravatar

register = template.Library()

@register.simple_tag(takes_context=True)
def profile_image(context, user, size='square'):
    """
    Returns img tag with users avatar.
    
    Takes ``User`` object and optional size.
    Sizes include "square" (50x50), "small" (50 pixels wide, variable height), 
    "normal" (100 pixels wide, variable height) and "large" (200 pixels wide, variable height).
    """
    
    if user.facebook_id:
        return facebook.facebook_picture(user.username, size)
    else:
        return gravatar.gravatar(context, user, (50, 50, 100, 200)[('square', 'small', 'normal', 'large').index(size)])