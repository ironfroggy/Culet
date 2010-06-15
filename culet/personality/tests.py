import unittest
import mock

from django.contrib.auth.models import User

from culet.personality.models import Personality
from culet.personality.views import _viewier_dec, viewier, become, SuspicionError, SuspicionError_Permission, SuspicionError_Invalid


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
            return {
                'ctx':{
                    'x': 123,
                    }
                }
            

        @apply
        @mock.patch("culet.personality.views.render_to_response")
        def _(render_to_response):
            decorated = _viewier_dec(view, "the_template.html")
            result = decorated(request)

            assert render_to_response.called_with("the_template.html")
            assert render_to_response.call_args[0][1]['x'] == 123


class MockSession(mock.Mock):
    def __contains__(self, key):
        return hasattr(self, key)
    def __getitem__(self, key):
        return getattr(self, key)
    def __setitem__(self, key, value):
        return setattr(self, key, value)

class BecomeTest(unittest.TestCase):

    def test_refuseNonexistantUser(self):
        request = mock.Mock()
        def raise_user_doesnotexist(*args, **kwargs):
            assert kwargs['username'] == 'alt1'
            raise User.DoesNotExist()

        request.session = MockSession()
        request.session.SESSION_KEY = 'THE_KEY'
        request.user = mock.Mock(spec=['personalities'])
        request.user.is_anonymous = mock.Mock(return_value=False)

        personality_get = request.user.personalities.get
        personality_get.side_effect = raise_user_doesnotexist
        self.assertRaises(SuspicionError_Invalid, become.wrapped, request, "alt1")

    def test_refuseUnpermittedUser(self):
        request = mock.Mock()
        def raise_user_doesnotexist(*args, **kwargs):
            assert kwargs['username'] == 'alt1'
            raise User.DoesNotExist()
        
        request.session = MockSession()
        request.session.SESSION_KEY = 'THE_KEY'
        request.user = mock.Mock(spec=['personalities'])
        request.user.is_anonymous = mock.Mock(return_value=False)

        personality_get = request.user.personalities.get
        personality_get.side_effect = raise_user_doesnotexist
        @apply
        @mock.patch("django.contrib.auth.models.User.objects.get")
        @mock.patch("django.contrib.auth.models.User.objects.filter")
        def _(user_filter, user_get):
            user_filter.return_value = mock.Mock()
            user_filter.return_value.count = mock.Mock(return_value=1)

            self.assertRaises(SuspicionError_Permission, become.wrapped, request, "alt1")

    def test_refuseUnpermittedUser(self):
        request = mock.Mock()
        def raise_user_doesnotexist(*args, **kwargs):
            assert kwargs['username'] == 'alt1'
            raise User.DoesNotExist()
        
        request.session = MockSession()
        request.session.SESSION_KEY = 'THE_KEY'
        request.user = mock.Mock(spec=['personalities'])
        request.user.is_anonymous = mock.Mock(return_value=True)

        personality_get = request.user.personalities.get
        personality_get.side_effect = raise_user_doesnotexist
        @apply
        @mock.patch("django.contrib.auth.models.User.objects.get")
        @mock.patch("django.contrib.auth.models.User.objects.filter")
        def _(user_filter, user_get):
            user_filter.return_value = mock.Mock()
            user_filter.return_value.count = mock.Mock(return_value=1)

            self.assertRaises(SuspicionError_Permission, become.wrapped, request, "alt1")

    def test_acceptOwned(self):
        request = mock.Mock()
        alt_user = mock.Mock()
        
        request.session = MockSession()
        request.session.SESSION_key = 'THE_KEY'
        request.user = mock.Mock(spec=['personalities'])
        request.user.is_anonymous = mock.Mock(return_value=False)
        original_user = request.user

        personality_get = request.user.personalities.get
        personality_get.return_value = alt_user

        self._accept_test(request, original_user, original_user, alt_user, personality_get)

    def test_acceptSibling(self):
        request = mock.Mock()
        alt_user = mock.Mock()
        
        request.session = MockSession()
        request.session.SESSION_key = 'THE_KEY'
        request.user = mock.Mock(spec=['personalities'])
        request.user.is_anonymous = mock.Mock(return_value=False)
        original_user = request.user
        original_user.master_user = mock.Mock()
        master_user = original_user.master_user

        personality_get = master_user.personalities.get
        personality_get.return_value = alt_user

        self._accept_test(request, original_user, master_user, alt_user, personality_get)

    def _accept_test(self, request, original_user, master_user, alt_user, personality_get):
        @apply
        @mock.patch("culet.personality.views.login")
        def _(login):
            return_value = become.wrapped(request, "alt1")
            R_previous_user = return_value['ctx']['previous_user']
            R_became = return_value['ctx']['became']
            R_master_user = return_value['ctx']['master_user']
            del return_value

            assert R_previous_user is original_user, locals()
            assert R_became is alt_user, locals()
            assert R_master_user is master_user, locals()
            assert login.call_args[0][0] is request
            assert login.call_args[0][1] is alt_user

          
