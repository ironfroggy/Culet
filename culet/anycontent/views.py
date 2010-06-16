from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType

from culet.anycontent.models import Header, _types
from culet.anycontent.forms import AnyContentForm

def list(request):

    all = Header.objects.all()

    return render_to_response(
        "anycontent/list.html",
        RequestContext(request, {"posts": all}))

def post(request, content_type=None):

    if content_type is None:
        forms = []
    else:
        forms = AnyContentForm(request, content_type) 

    posttypes = [
        {
            'name': t['name'],
            'content_type_id': ContentType.objects.get_for_model(t['model']).id,
        }
        for t in _types.values()
    ]

    return render_to_response(
        "anycontent/form.html",
        RequestContext(request, {"forms": forms, "posttypes": posttypes}))