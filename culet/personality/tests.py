import unittest

from django.contrib.auth.models import User

from culet.personality.models import Personality


class PersonalityTest(unittest.TestCase):

    setupalready = False
    def setUp(self):
        if not self.setupalready:
            PersonalityTest.setupalready = True
            self.oneTimeSetUp()

        self.one = User.objects.get(username='one')
        self.two = User.objects.get(username='two')

    def oneTimeSetUp(self):
        user = User.objects.create(username="one")
        Personality.objects.create_for(user, "one-A")
        Personality.objects.create_for(user, "one-B")

        user = User.objects.create(username="two")
        Personality.objects.create_for(user, "two-A")
        Personality.objects.create_for(user, "two-B")

    def test_getPersonalitiesOfUser(self):
        self.assertEqual(2, self.one.personalities.count())
        alts = set(alt.username for alt in self.one.personalities.all())

        self.assertEqual(alts, set(('one-A', 'one-B')))

    def test_getAlternates(self):
        A = self.one.personalities.get(username='one-A') 
        alts = Personality.objects.alternates_of(A)
        self.assertEqual(1, alts.count())
        self.assertEqual("one-B", alts[0].username)

