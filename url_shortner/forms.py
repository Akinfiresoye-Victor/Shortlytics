from django import forms
from django.forms import ModelForm
from .models import URLModel


class UrlForm(ModelForm):
    class Meta:
        model=URLModel
        fields=('long_link',
                'link_to',)
        labels={'long_link': '',
                'link_to': '',
                }
        widgets= {'long_link': forms.URLInput(attrs={'class':'form-conmtrol', 'placeholder': 'Input Long Link', 'size':70}),
                  'link_to': forms.TextInput(attrs= {'class': 'form-control', 'placeholder': 'Link Destination', 'size':20})
                  }

