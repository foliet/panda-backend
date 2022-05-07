from django.contrib.auth.backends import ModelBackend

from authentication.models import User


class EmailModelBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get(User.EMAIL_FIELD)
        if email is None or password is None:
            return
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
