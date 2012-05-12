from django.forms import ModelForm
from shortlink.models import ShortLink

class ShortLinkForm(ModelForm):
    class Meta:
        model = ShortLink
        exclude = ('user_profile', )
