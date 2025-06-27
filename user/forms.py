# user/forms.py
from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['name', 'address', 'phone', 'email', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
