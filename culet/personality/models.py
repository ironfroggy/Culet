from django.db import models
from django.contrib.auth.models import User

class PersonalityManager(models.Manager):

    def create_for(self, master, alt_username, alt_email=''):
        return self.create(
            master_user=master,
            username=alt_username,
            email=alt_email)

    def alternates_of(self, personality):
        return self.filter(master_user=personality.master_user).exclude(id=personality.id) 

class Personality(User):
    objects = PersonalityManager()

    master_user = models.ForeignKey(User, related_name='personalities')
