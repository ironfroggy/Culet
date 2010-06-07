import unittest
import mock

from django.contrib.auth.models import User

from culet.personality.models import Personality
from culet.personality.views import _viewier_dec, viewier, SuspicionError


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

class ViewierTest(unittest.TestCase):

    def test_handlesSuspicion(self):
        request = mock.Mock()
        user = mock.Mock()
        def suspicious_function(request):
            raise SuspicionError("test", user)
        
        @apply
        @mock.patch("culet.personality.views.render_to_response")
        def _(render_to_response):
            decorated = _viewier_dec(suspicious_function, "nothing.html")
            result = decorated(request)

            assert render_to_response.called_with("culet/error.html")

    def test_usesTemplate(self):
        request = mock.Mock()
        user = mock.Mock()
        def view(request):
            return {'x': 123}

        @apply
        @mock.patch("culet.personality.views.render_to_response")
        def _(render_to_response):
            decorated = _viewier_dec(view, "the_template.html")
            result = decorated(request)

            assert render_to_response.called_with("the_template.html")
            assert render_to_response.call_args[0][1]['x'] == 123
