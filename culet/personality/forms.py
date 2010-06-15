from django import forms
from django.contrib.auth.models import User

from culet.personality.models import Personality

class PersonalityForm(forms.Form):

    personality_name = forms.CharField()

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(PersonalityForm, self).__init__(*args, **kwargs)

    def save(self):
        master_user = self.request.user.master_user

        self.instance = Personality.objects.create(
            username=self.cleaned_data['personality_name'],
            master_user=master_user
        )
        return True

    def clean_personality_name(self):
        name = self.cleaned_data['personality_name']
        if User.objects.filter(username=name).count():
            raise forms.ValidationError("Username is already taken. Please choose another.")
        return name
