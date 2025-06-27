from django.shortcuts import render
from django.contrib import messages
# Create your views here.
# worker/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from user.models import Complaint
from .models import Worker

@login_required
def worker_dashboard(request):
    try:
        worker = Worker.objects.get(user=request.user)
    except Worker.DoesNotExist:
        return redirect('login')

    complaints = Complaint.objects.filter(assigned_to=worker)

    query = request.GET.get('q')
    status_filter = request.GET.get('status', 'All')

    if query:
        complaints = complaints.filter(name__icontains=query)

    if status_filter != 'All':
        complaints = complaints.filter(status=status_filter)

    return render(request, 'worker/dashboard.html', {
        'complaints': complaints,
        'query': query,
        'status_filter': status_filter
    })


@login_required
def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id, assigned_to__user=request.user)

    if request.method == 'POST':
        complaint.status = 'Completed'
        complaint.save()
        messages.success(request, "✅ Complaint marked as completed.")
        return redirect('worker_dashboard')

    return render(request, 'worker/complaint_detail.html', {'complaint': complaint})
