from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import UserProfile
from .profile_forms import UserProfileForm, ProfilePictureForm, CustomPasswordChangeForm
from payment.models import Order
import os
from django.conf import settings


@login_required
def profile_view(request):
    """Display user profile page"""
    user = request.user
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Get user's recent orders
    recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Get user statistics
    total_orders = Order.objects.filter(user=user).count()
    
    context = {
        'user': user,
        'profile': profile,
        'recent_orders': recent_orders,
        'total_orders': total_orders,
    }
    
    return render(request, 'store/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile information"""
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        
        if form.is_valid():
            form.save()
            
            # Update profile fields if they exist in POST data
            if 'phone' in request.POST:
                profile.phone = request.POST.get('phone')
            if 'address' in request.POST:
                profile.address = request.POST.get('address')
            if 'city' in request.POST:
                profile.city = request.POST.get('city')
            if 'postal_code' in request.POST:
                profile.postal_code = request.POST.get('postal_code')
            if 'birth_date' in request.POST and request.POST.get('birth_date'):
                profile.birth_date = request.POST.get('birth_date')
            
            profile.save()
            
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=user)
    
    context = {
        'form': form,
        'profile': profile,
    }
    
    return render(request, 'store/edit_profile.html', context)


@login_required
@require_http_methods(["POST"])
def upload_profile_picture(request):
    """Handle profile picture upload via AJAX"""
    form = ProfilePictureForm(request.POST, request.FILES)
    
    if form.is_valid():
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # Delete old profile picture if it exists
        if profile.profile_picture:
            old_path = profile.profile_picture.path
            if os.path.exists(old_path):
                os.remove(old_path)
        
        # Save new profile picture
        profile.profile_picture = form.cleaned_data['profile_picture']
        profile.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Profile picture updated successfully!',
            'image_url': profile.get_profile_picture_url()
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Error uploading image. Please try again.',
            'errors': form.errors
        })


@login_required
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'store/change_password.html', context)


@login_required
@require_http_methods(["POST"])
def delete_profile_picture(request):
    """Delete user's profile picture"""
    try:
        profile = UserProfile.objects.get(user=request.user)
        
        if profile.profile_picture:
            # Delete file from storage
            old_path = profile.profile_picture.path
            if os.path.exists(old_path):
                os.remove(old_path)
            
            # Clear the field
            profile.profile_picture = None
            profile.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Profile picture deleted successfully!',
                'image_url': profile.get_profile_picture_url()
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'No profile picture to delete.'
            })
    
    except UserProfile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Profile not found.'
        })
