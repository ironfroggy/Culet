from django.db import models
from django.contrib.contenttypes import generic


class Header(models.Model):

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    content_type_name = models.CharField(max_length=50)
    content_type = models.ForeignKey('contenttypes.ContentType')
    content_id = models.IntegerField()
    content = generic.GenericForeignKey('content_type', 'content_id')

    def render_content(self):
        from django import template
        t = template.loader.get_template(content_classes[self.content_type_name]['template'])
        return t.render(template.Context({
            'header': self,
            'content': self.content,
        }))

    def get_form(self):
        register_meta = content_classes[self.content_type_name]
        if register_meta['form'] is not None:
            form_class = register_meta['form']
        else:
            form_class = type(self).ContentMeta.form

        header = self
        class _ContentForm(form_class, ContentBaseForm):
            def save(self, *args, **kwargs):
                header.title = self.cleaned_data['title']
                header.slug = self.cleaned_data['slug']
                header.save(*args, **kwargs)
                
                nsform_class.save(*args, **kwargs)

        return _ContentForm(instance=self.content)

    class Meta:
        ordering = ['-created']

class _ContentClasses(object):
    def __init__(self):
        self._types = {}

    def register(self, name, model, template=None, form=None):
        """Register a content class and optionally bind it with a display template
        and/or form.
        """

        if template is None:
            template = model.ContentMeta.template
        if form is None:
            form = model.ContentMeta.get_form()
        self._types[name] = locals()

    def __getitem__(self, name):
        return self._types[name]
    def __iter__(self):
        return iter(self._types.values())
content_classes = _ContentClasses()

class PlainText(models.Model):

    body = models.TextField(default="")

    @property
    def tease(self):
        words = self.body.split(' ')
        if len(words) >= 500:
            words.append('...')
            return ' '.join(words)
        else:
            return self.body

    class ContentMeta:
        template = "anycontent/plain.html"    
        @classmethod
        def get_form(cls):
            from django import forms
            class TextForm(forms.ModelForm):
                class Meta:
                    model = PlainText
            return TextForm

content_classes.register("plain-text", PlainText)
content_classes.register("plain-html", PlainText, template="anycontent/plain-html.html")
