from culet.personality.models import Personality


class PersonalityMiddleware:

    def process_request(self, request):
        try:
            current_user = request.user
        except AttributeError:
            return
        else:
            
            try:
                if request.user.is_authenticated():
                    request.user = Personality.objects.get(user_ptr=request.user)
                else:
                    request.user.master_user = request.user
            except Personality.DoesNotExist:
                request.user.master_user = request.user
