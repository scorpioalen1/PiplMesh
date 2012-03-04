from django.http import HttpResponse
from django.template import loader, RequestContext
from lazysignup.decorators import allow_lazy_user

@allow_lazy_user
def homeView(request):
    
    c = RequestContext(request,{
        'search_engine': 'Google',
        'search_engine_logo': 'google_logo.png'
    })
    
    template = 'home.html'
    t = loader.get_template(template)
    return HttpResponse(t.render(c))
