from django import template

register = template.Library()

@register.inclusion_tag('tags/profile_image.html', takes_context=True)
def profile_image(context, user, size='square'):
    """
    Returns img tag with users profile image.
    
    Takes ``User`` object and optional size.
    Sizes include "square" (50x50), "small" (50 pixels wide, variable height), 
    "normal" (100 pixels wide, variable height) and "large" (200 pixels wide, variable height).
    """
    
    return {
        'profile_image_url': user.profile_image_url(size, context['request'])
    }