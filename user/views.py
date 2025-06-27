

# Create your views here.
# user/views.py
from django.shortcuts import render, redirect
from .forms import ComplaintForm
from django.contrib import messages

def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your complaint has been submitted successfully.')
            return redirect('submit_complaint')
    else:
        form = ComplaintForm()
    return render(request, 'user/submit_complaint.html', {'form': form})
