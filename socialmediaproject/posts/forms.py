from django import forms
from django.db.models import Q
from django.utils.translation import gettext as _

from accounts.models import User
from .models import Post


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']