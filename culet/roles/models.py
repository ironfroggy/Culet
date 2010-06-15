from abc import ABCMeta, abstractmethod

from django.db import models
from django.contrib.contenttypes import generic


class Role(models.Model):

    name = models.CharField(max_length=100)
    role_group = models.ForeignKey('auth.Group')

    def grant(self, user):
        self.role_group.users.add(user)

    def deny(self, user):
        self.role_group.users.remove(user)

    def check(self, user, nothing, action):
        return user in self.role_group.users and action in self.actions.all()

    def add_action(self, action):
        RoleAction.objects.create(
            role=self,
            action_module=action.__module__,
            action_class=action.__name__)

    def drop_action(self, action):
        RoleAction.objects.filter(
            role=self,
            action_module=action.__module__,
            action_class=action.__name__).delete()

class RoleAction(models.Model):
    role = models.ForeignKey(Role, related_name='actions')
    action_module = models.CharField(max_length=300)
    action_class = models.CharField(max_length=100)

    def get_action(self):
        module = __import__(self.action_module, fromlist=[1])
        action_class = getattr(module, self.action_class)
        return action_class

class Action(object):
    """Subclasses of action define things roles can do."""

    def applies_to_instance(self, instance):
        """Returns true if the action can be used on the instance."""


class ModelPermission(Role):

    model = models.ForeignKey('contenttypes.ContentType')

    def check(self, user, instance_or_model):
        if isinstance(instance_or_model, models.Model):
            model = instance_or_model
        else:
            model = type(instance_or_model)

        return model is self.model.get_model()


class ItemPermission(Role):

    content_type = models.ForeignKey('contenttypes.ContentType')
    object_id = models.IntegerField()
    object = generic.GenericForeignKey()

    def check(self, user, instance):
        model = self.content_type.get_model()
        
        return isinstance(instance, model) and instance.id == self.object_id


