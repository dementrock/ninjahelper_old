from django.forms import ModelForm
from community.models import ShortLink

class ShortLinkForm(ModelForm):
    class Meta:
        model = ShortLink
        exclude = ('user_profile', )
