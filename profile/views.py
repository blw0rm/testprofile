from django.conf import settings
from models import UserProfile
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.template import RequestContext
from django.http import HttpResponse
from forms import UserProfileForm

def profile_view(request):
    result = []
    template = 'profile/profile_details.html'
    if isinstance(request.user, User):
        try:
            result = request.user.get_profile()
            return render_to_response(template,{'profile':result,}, RequestContext(request))
        except UserProfile.DoesNotExist:
            return render_to_response(template,{'profile':result,}, RequestContext(request))        
    else:
        return render_to_response(template,{'auth_form':AuthenticationForm(),}, RequestContext(request))
    
def edit_profile(request):
    try:
        profile = request.user.get_profile()
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
        profile.save()
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserProfileForm(instance=profile, initial={'first_name': request.user.first_name,
                                                      'last_name': request.user.last_name,
                                                      'contacts': request.user.email,
                                                      'birthday': profile.birthday,
                                                      'biography': profile.biography})
    print form.errors
    return render_to_response('profile/profile_edit.html', {'form': form,}, RequestContext(request))

        
