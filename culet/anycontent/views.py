from django.template import RequestContext
from django.shortcuts import render_to_response

from culet.anycontent.models import Header
from culet.anycontent.forms import AnyContentForm

def list(request):

    all = Header.objects.all()

    return render_to_response(
        "anycontent/list.html",
        RequestContext(request, {"posts": all}))

def post(request, content_type):

    forms = AnyContentForm(request, content_type) 

    return render_to_response(
        "anycontent/form.html",
        RequestContext(request, {"forms": forms}))
