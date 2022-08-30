from django import forms
from .models import AuctionModelForm

class AuctionForm(forms.ModelForm):
  class Meta:
    model = AuctionModelForm
    fields = ('type','id','description','amount')