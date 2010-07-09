from sys import stderr
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify

from culet.anycontent.models import Header, content_classes

class _ccc(object):
    def __iter__(self):
        for cc in content_classes:
            ct = ContentType.objects.get_for_model(cc['model'])
            print >>stderr, "***", cc['name'], str(ct)
            yield (
                cc['name'],
                cc['name'],
            )

HF_DEBUG_FIELDS = forms.HiddenInput

class HeaderForm(forms.ModelForm):
    content_type_name = forms.ChoiceField(widget=HF_DEBUG_FIELDS, choices=_ccc())
    content_id = forms.CharField(widget=HF_DEBUG_FIELDS)
    slug = forms.CharField(widget=HF_DEBUG_FIELDS)
    class Meta:
        model = Header

def AnyContentForm(request, content_type_name):
    hf = HeaderForm(request.POST or None, prefix='header')
    content_form = content_classes[content_type_name]['form']
    cf = content_form(request.POST or None, prefix='content')

    if request.method == 'POST':
        if  cf.is_valid():
            content = cf.save()
            hf.data = dict((k, v) for (k, v) in hf.data.items())
            hf.data[hf.add_prefix('slug')] = slugify(hf.data[hf.add_prefix('title')])
            hf.data[hf.add_prefix('content')] = content.id
            hf.data[hf.add_prefix('content_type_name')] = content_classes[content_type_name]['name']
            hf.data[hf.add_prefix('content_id')] = content.id
            hf.data[hf.add_prefix('content_type')] = ContentType.objects.get_for_model(content_classes[content_type_name]['model']).id
            if hf.is_valid():
                hf.save()

    return (hf, cf)
