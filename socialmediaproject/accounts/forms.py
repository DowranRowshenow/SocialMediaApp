from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext as _
from accounts.models import User
import uuid


class SingUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
        	'username',
            'email',
            "password1",
            "password2",
        )

    def save(self, commit=True): 
        user = super().save(commit=False)
        user.auth_token = str(uuid.uuid4())
        user.hash = str(uuid.uuid4())
        user.is_active = False

        if commit:
            user.save()

        return user


class LogInForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        if not user.is_active:
            self.add_error("username", _("Please verify your email!"))

        return super().confirm_login_allowed(user)