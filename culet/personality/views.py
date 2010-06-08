from django.contrib.auth import login
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from culet.personality.models import Personality
from culet.personality.forms import PersonalityForm

class SuspicionError(Exception):
    def __init__(self, msg, user):
        self.msg = msg
        self.user = user
        self.args = (msg, user)
class SuspicionError_Permission(SuspicionError): pass
class SuspicionError_Invalid(SuspicionError): pass

def _viewier_dec(f, template, get_form=None, success_url=None):
    def _(request, *args, **kwargs):
        try:
            ctx = {}

            view_locals = f(request, *args, **kwargs) or {}
            ctx.update(view_locals.get('ctx', {}))
            def callback(name, *args, **kwargs):
                cb_function = view_locals.get(name, lambda *a, **k: a[0])
                ret = cb_function(*args, **kwargs)
                return ret

            # Creating a form
            if request.method == 'GET' and get_form is not None:
                ctx['form'] = form = get_form(request)
            # Handling a form
            elif request.method == 'POST' and get_form is not None:
                ctx['form'] = form = get_form(request, request.POST)
                if form.is_valid():
                    callback('fmrm_valid', form)
                    form.save()
                    callback('form_saved', form)
                    if success_url is not None:
                        return HttpResponseRedirect(reverse(success_url))

            # Post-view processing and result
            if view_locals.get('redirect', False):
                return HttpResponseRedirect(reverse(success_url))
            else:
                return render_to_response(
                    template,
                    RequestContext(request, ctx)
                )
        except SuspicionError:
            return render_to_response("culet/error.html", RequestContext(request, ctx))

    # TODO: Figure out what the "standard" thing is here
    _.wrapped = f
    return _
def viewier(template, **kwargs):
    return lambda func:_viewier_dec(func, template, **kwargs)

@viewier('culet/myselves.html')
def myselves(request):
    """List of current user's personalities."""

    current_user = request.user
    try:
        master_user = current_user.master_user
    except AttributeError:
        master_user = current_user

    personalities = master_user.personalities.all()

    return {'ctx': locals()}

@viewier("culet/become.html", success_url="personality-myselves")
def become(request, alternate):
    """Log a user in as one of their alternates."""

    current_user = request.user
    if current_user.is_anonymous():
        raise SuspicionError_Permission("User tried to become a personality while not logged in", user=current_user)
    try:
        master_user = current_user.master_user
    except AttributeError:
        master_user = current_user

    try:
        personality = master_user.personalities.get(username=alternate)
    except Personality.DoesNotExist:
        personality = User.objects.get(username=alternate)
        if personality.personalities.count():
            pass
        else:
            raise
    except User.DoesNotExist:
        if User.objects.filter(username=alternate).count():
            raise SuspicionError_Permission("User tried to become a personality they do not own", user=current_user)
        else:
            raise SuspicionError_Invalid("User tried to become a personality that does not exist", user=current_user)

    personality.backend = settings.AUTHENTICATION_BACKENDS[0]
    login(request, personality)

    return {'ctx':
        {
            'previous_user': current_user,
            'became': personality,
            'master_user': master_user,
        },
        'redirect': True,
    }

def delete(request, alternate, confirmation=None):
    """Delete a personality."""

@viewier('culet/create.html',
    get_form=PersonalityForm,
    success_url='personality-myselves',
    )
def create(request):
    """Create a personality."""

    pass

def update(request, alternate):
    """Update a personality."""
