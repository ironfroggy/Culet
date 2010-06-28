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

def read(request, slug):
    header = Header.objects.get(slug=slug)
    content = header.content

    return render_to_response(
        "anycontent/read.html",
        RequestContext(request, {
            "header": header,
            "content": content,
        })
    )

def post(request, content_type_name=None):

    if content_type_name is None:
        forms = []
    else:
        forms = AnyContentForm(request, content_type_name)

    posttypes = [
        {
            'name': t['name'],
            'content_type_id': ContentType.objects.get_for_model(t['model']).id,
            'content_type_name': t['name'],
        }
        for t in _types.values()
    ]

    return render_to_response(
        "anycontent/form.html",
        RequestContext(request, {"forms": forms, "posttypes": posttypes}))
