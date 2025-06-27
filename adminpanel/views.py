from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from user.models import Complaint
from .forms import AssignWorkerForm
from .forms import WorkerAddForm
from .forms import WorkerForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from adminpanel import views
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from worker.models import Worker


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard') 
            elif hasattr(user, 'worker'):
                return redirect('worker_dashboard') 
            else:
                return render(request, 'adminpanel/login.html', {'error': 'Unauthorized role'})
        else:
            return render(request, 'adminpanel/login.html', {'error': 'Invalid credentials'})

    return render(request, 'adminpanel/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def admin_dashboard(request):
    query = request.GET.get("q", "")
    status_filter = request.GET.get("status", "All")

    complaints = Complaint.objects.all()

    if query:
        complaints = complaints.filter(
            Q(name__icontains=query) |
            Q(status__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )

    if status_filter != "All":
        complaints = complaints.filter(status=status_filter)

    paginator = Paginator(complaints, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'complaints': complaints,
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
        'total': complaints.count(),
        'pending': complaints.filter(status="Pending").count(),
        'inprogress': complaints.filter(status="In Progress").count(),
        'completed': complaints.filter(status="Completed").count(),
    }
    return render(request, 'adminpanel/dashboard.html', context)

@login_required
def assign_worker(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == 'POST':
        form = AssignWorkerForm(request.POST)
        if form.is_valid():
            worker = form.cleaned_data['worker']
            complaint.assigned_to = worker
            complaint.status = "In Progress"  # Automatically update status
            complaint.save()
            messages.success(request, "✅ Worker assigned successfully.")
            return redirect('admin_dashboard')
    else:
        form = AssignWorkerForm()

    return render(request, 'adminpanel/assign_worker.html', {'form': form})

@login_required
def add_worker(request):
    if request.method == 'POST':
        form = WorkerAddForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            Worker.objects.create(user=user)
            messages.success(request, "Worker added successfully.")
            return redirect('add_worker')  
        else:
            messages.error(request, "Invalid data. Try again.")
    else:
        form = WorkerAddForm()

    return render(request, 'adminpanel/add_worker.html', {'form': form})