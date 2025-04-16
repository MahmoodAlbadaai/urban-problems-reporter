from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction

# Add this import
from .models import Issue, IssueType, Location, Resolution, Comment, UserProfile

from .forms import (
    UserRegistrationForm, UserProfileForm, UserUpdateForm,
    IssueForm, IssueUpdateForm, CommentForm, LocationForm, 
    ResolutionForm, IssueDeleteConfirmForm
)


# Basic page views
def index(request):
    """Home page view"""
    # Get featured resolved issues for the home page
    success_stories = Resolution.objects.filter(featured=True).order_by('-resolution_date')[:3]
    return render(request, 'core/index.html', {'success_stories': success_stories})

def report(request):
    """Report issue form page view"""
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save()
            messages.success(request, 'Your issue has been reported successfully! Thank you for helping improve your city.')
            # Redirect to a confirmation page instead of detail page
            return redirect('report_confirmation')
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = IssueForm()
    
    return render(request, 'core/report.html', {'form': form})

def map(request):
    """Map/list of reported issues view"""
    # Get filter parameters from request
    issue_type_id = request.GET.get('issue_type')
    status = request.GET.get('status')
    
    # Start with all issues
    issues = Issue.objects.all().order_by('-reported_date')
    
    # Apply filters if provided
    if issue_type_id:
        issues = issues.filter(issue_type_id=issue_type_id)
    if status:
        issues = issues.filter(status=status)
    
    # Get all issue types for the filter dropdown
    issue_types = IssueType.objects.all()
    
    # Paginate the results
    paginator = Paginator(issues, 10)  # Show 10 issues per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'issue_types': issue_types,
        'selected_type': issue_type_id,
        'selected_status': status
    }
    
    return render(request, 'core/issue_list.html', context)

def success(request):
    """Success stories page view"""
    # Get all resolutions that are featured
    resolutions = Resolution.objects.filter(featured=True).order_by('-resolution_date')
    
    return render(request, 'core/success.html', {'resolutions': resolutions})

def contact(request):
    """Contact page view"""
    return render(request, 'core/contact.html')



def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirect authorities to dashboard, regular users to homepage
            if user.is_staff or hasattr(user, 'profile') and user.profile.is_authority:
                messages.success(request, f'Welcome back, {username}!')
                return redirect('authority_dashboard')
            else:
                messages.success(request, f'Welcome back, {username}!')
                return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'core/login.html')


def register(request):
    """Register page view"""
    return render(request, 'core/register.html')

@login_required
def authority_dashboard(request):
    # Check if the user is staff or has authority permissions
    if not (request.user.is_staff or 
            (hasattr(request.user, 'profile') and request.user.profile.is_authority)):
        messages.error(request, 'You do not have permission to access the authority dashboard.')
        return redirect('index')
    
    # Get counts for the dashboard
    pending_count = Issue.objects.filter(status='pending').count()
    in_progress_count = Issue.objects.filter(status='in_progress').count()
    resolved_count = Issue.objects.filter(status='resolved').count()
    
    # Get recent issues
    recent_issues = Issue.objects.all().order_by('-reported_date')[:5]
    
    context = {
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        'recent_issues': recent_issues
    }
    
    return render(request, 'core/authority-dashboard.html', context)

# CRUD operations for Issues

def issue_detail(request, pk):
    """View a single issue with details (Read operation)"""
    issue = get_object_or_404(Issue, pk=pk)
    comments = issue.comments.all().order_by('-created_at')
    
    # Comment form
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.issue = issue
            comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect('issue_detail', pk=issue.pk)
    else:
        comment_form = CommentForm()
    
    # Check if a resolution exists
    try:
        resolution = issue.resolution
    except Resolution.DoesNotExist:
        resolution = None
    
    context = {
        'issue': issue,
        'comments': comments,
        'comment_form': comment_form,
        'resolution': resolution
    }
    
    return render(request, 'core/issue_detail.html', context)

# Ensure all issue edit/delete views have login_required
@login_required
def issue_update(request, pk):
    """Update an existing issue (Update operation)"""
    issue = get_object_or_404(Issue, pk=pk)
    
    if request.method == 'POST':
        form = IssueUpdateForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            messages.success(request, 'Issue has been updated successfully.')
            return redirect('issue_detail', pk=issue.pk)
    else:
        form = IssueUpdateForm(instance=issue)
    
    return render(request, 'core/issue_update.html', {'form': form, 'issue': issue})

@login_required
def issue_delete(request, pk):
    """Delete an existing issue (Delete operation)"""
    issue = get_object_or_404(Issue, pk=pk)
    
    if request.method == 'POST':
        form = IssueDeleteConfirmForm(request.POST)
        if form.is_valid():
            # Log the deletion reason before deleting
            deletion_reason = form.cleaned_data['reason']
            # Here you might want to log this reason to a file or another database table
            
            # Delete the issue
            issue.delete()
            messages.success(request, 'Issue has been deleted.')
            return redirect('map')
    else:
        form = IssueDeleteConfirmForm()
    
    return render(request, 'core/issue_delete.html', {'form': form, 'issue': issue})

@login_required
def add_resolution(request, pk):
    """Add a resolution to an issue"""
    issue = get_object_or_404(Issue, pk=pk)
    
    # Check if a resolution already exists
    try:
        resolution = issue.resolution
        # If it exists, redirect to update instead
        return redirect('update_resolution', pk=issue.pk)
    except Resolution.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = ResolutionForm(request.POST, request.FILES)
        if form.is_valid():
            resolution = form.save(commit=False)
            resolution.issue = issue
            resolution.resolved_by = request.user
            resolution.save()
            
            # Update the issue status to resolved
            issue.status = 'resolved'
            issue.save()
            
            messages.success(request, 'Resolution has been added successfully.')
            return redirect('issue_detail', pk=issue.pk)
    else:
        form = ResolutionForm()
    
    return render(request, 'core/add_resolution.html', {'form': form, 'issue': issue})

@login_required
def update_resolution(request, pk):
    """Update an existing resolution"""
    issue = get_object_or_404(Issue, pk=pk)
    
    try:
        resolution = issue.resolution
    except Resolution.DoesNotExist:
        # If no resolution exists, redirect to add instead
        return redirect('add_resolution', pk=issue.pk)
    
    if request.method == 'POST':
        form = ResolutionForm(request.POST, request.FILES, instance=resolution)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resolution has been updated successfully.')
            return redirect('issue_detail', pk=issue.pk)
    else:
        form = ResolutionForm(instance=resolution)
    
    return render(request, 'core/update_resolution.html', {'form': form, 'issue': issue, 'resolution': resolution})

# AJAX operations for forms

@require_POST
def ajax_add_location(request):
    """AJAX endpoint to add a new location"""
    form = LocationForm(request.POST)
    if form.is_valid():
        location = form.save()
        return JsonResponse({
            'success': True,
            'location_id': location.id,
            'location_name': location.name
        })
    else:
        # Return form errors
        return JsonResponse({
            'success': False,
            'errors': form.errors.as_json()
        }, status=400)

@require_POST
def ajax_add_comment(request, pk):
    """AJAX endpoint to add a comment to an issue"""
    issue = get_object_or_404(Issue, pk=pk)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.issue = issue
        
        # If the user is logged in, associate the comment with them
        if request.user.is_authenticated:
            comment.user = request.user
        
        comment.save()
        
        # Return comment data to update the UI
        return JsonResponse({
            'success': True,
            'comment_id': comment.id,
            'author': comment.user.username if comment.user else comment.author_name,
            'text': comment.comment_text,
            'date': comment.created_at.strftime('%B %d, %Y, %I:%M %p')
        })
    else:
        # Return form errors
        return JsonResponse({
            'success': False,
            'errors': form.errors.as_json()
        }, status=400)


# Add a new report confirmation view
def report_confirmation(request):
    """Confirmation page after successful report submission"""
    return render(request, 'core/report_confirmation.html')



def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = user_form.save()
                
                # Check if profile already exists before creating
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'phone_number': profile_form.cleaned_data.get('phone_number'),
                        'address': profile_form.cleaned_data.get('address')
                    }
                )
                
                # If profile wasn't created (already existed), update it
                if not created:
                    profile.phone_number = profile_form.cleaned_data.get('phone_number')
                    profile.address = profile_form.cleaned_data.get('address')
                    profile.save()
                
                # Log the user in
                username = user_form.cleaned_data.get('username')
                raw_password = user_form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                
                messages.success(request, f'Account created successfully. Welcome, {username}!')
                return redirect('index')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
        
    return render(request, 'core/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')

@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        try:
            profile_form = UserProfileForm(instance=request.user.profile)
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
            profile_form = UserProfileForm(instance=profile)
    
    return render(request, 'core/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



