# adminpanel/forms.py
from django import forms
from django.contrib.auth.models import User
from worker.models import Worker

class WorkerForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Worker
        fields = ['username', 'password', 'phone', 'address']

class WorkerAddForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class AssignWorkerForm(forms.Form):
    worker = forms.ModelChoiceField(
        queryset=Worker.objects.all(),
        required=True,
        empty_label="Select a Worker",
        widget=forms.Select(attrs={"class": "form-select"})
    )
