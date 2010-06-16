from django import forms
from django.contrib.contenttypes.models import ContentType

from culet.anycontent.models import Header

class HeaderForm(forms.ModelForm):
    class Meta:
        model = Header

def AnyContentForm(request, content_type):
    hf = HeaderForm(request.POST or None, prefix='header')
    content_form = ContentType.objects.get(id=content_type).model_class().ContentMeta.get_form()
    cf = content_form(request.POST or None, prefix='content')

    if request.method == 'POST':
        if  cf.is_valid():
            content = cf.save()
            hf.data = dict((k, v) for (k, v) in hf.data.items())
            hf.data[hf.add_prefix('content')] = content.id
            hf.data[hf.add_prefix('content_type_name')] = type(content).__name__
            hf.data[hf.add_prefix('content_id')] = content.id
            hf.data[hf.add_prefix('content_type')] = ContentType.objects.get_for_model(type(content)).id
            if hf.is_valid():
                hf.save()

    return (hf, cf)
