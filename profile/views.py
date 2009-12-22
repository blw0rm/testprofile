from django.conf import settings
from models import UserProfile
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.template import RequestContext


def profile_view(request):
    result = []
    template = 'profile/profile_details.html'
    if isinstance(request.user, User):
        print request.user
        try:
            result = request.user.get_profile()
            return render_to_response(template,{'profile':result,}, RequestContext(request))
        except UserProfile.DoesNotExist:
            return render_to_response(template,{'profile':result,}, RequestContext(request))        
    else:
        print 'Anonymous user detected'
        return render_to_response(template,{'auth_form':AuthenticationForm(),}, RequestContext(request))
        
        
