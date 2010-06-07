from django.contrib.auth import login
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response

from culet.personality.models import Personality

class SuspicionError(Exception):
    def __init__(self, msg, user):
        self.msg = msg
        self.user = user
        self.args = (msg, user)
class SuspicionError_Permission(SuspicionError): pass
class SuspicionError_Invalid(SuspicionError): pass

def _viewier_dec(f, template):
    def _(request, *args, **kwargs):
        try:
            data = f(request, *args, **kwargs)
            return render_to_response(
                template,
                RequestContext(request, data)
            )
        except SuspicionError:
            return render_to_response("culet/error.html", RequestContext(request, {}))
    _.wrapped = f
    return _
def viewier(template):
    return lambda func:_viewier_dec(func, template)

def myselves(request):
    """List of current user's personalities."""

@viewier("culet/become.html")
def become(request, alternate):
    """Log a user in as one of their alternates."""

    current_user = request.user
    try:
        master_user = current_user.master_user
    except AttributeError:
        master_user = current_user

    try:
        personality = master_user.personalities.get(username=alternate)
    except User.DoesNotExist:
        if User.objects.filter(username=alternate).count():
            raise SuspicionError_Permission("User tried to become a personality they do not own", user=current_user)
        else:
            raise SuspicionError_Invalid("User tried to become a personality that does not exist", user=current_user)

    else:
        login(request, personality)

        return {
            'previous_user': current_user,
            'became': personality,
            'master_user': master_user,
        }

def delete(request, alternate, confirmation=None):
    """Delete a personality."""

def create(request):
    """Create a personality."""

def update(request, alternate):
    """Update a personality."""
