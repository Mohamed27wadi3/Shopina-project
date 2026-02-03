"""
HTML views for user profile and settings.
These views use Django session authentication instead of JWT tokens.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from .services.user_service import UserService

User = get_user_model()


class ProfileHTMLView(LoginRequiredMixin, View):
    """HTML page for viewing and updating user profile."""
    template_name = "users/profile.html"
    login_url = '/accounts/login/'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
    
    def get(self, request):
        """Display profile page."""
        context = {
            'user': request.user,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        """Update profile."""
        user = request.user
        
        # Get data from form
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        country = request.POST.get('country', '').strip()
        bio = request.POST.get('bio', '').strip()
        shop_name = request.POST.get('shop_name', '').strip()
        
        # Handle avatar upload
        avatar = request.FILES.get('avatar')
        
        try:
            # Update user profile
            update_data = {}
            if first_name:
                update_data['first_name'] = first_name
            if last_name:
                update_data['last_name'] = last_name
            if phone_number:
                update_data['phone_number'] = phone_number
            if address:
                update_data['address'] = address
            if city:
                update_data['city'] = city
            if country:
                update_data['country'] = country
            if bio:
                update_data['bio'] = bio
            if shop_name:
                update_data['shop_name'] = shop_name
            if avatar:
                update_data['avatar'] = avatar
            
            # Use service to update
            self.user_service.update_profile(user, **update_data)
            
            messages.success(request, '✅ Profil mis à jour avec succès!')
            return redirect('users:profile_html')
            
        except Exception as e:
            messages.error(request, f'❌ Erreur: {str(e)}')
            return redirect('users:profile_html')


class ChangePasswordHTMLView(LoginRequiredMixin, View):
    """HTML page for changing password."""
    template_name = "users/change_password.html"
    login_url = '/accounts/login/'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
    
    def get(self, request):
        """Display change password page."""
        return render(request, self.template_name)
    
    def post(self, request):
        """Change password."""
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        # Validation
        if not old_password or not new_password or not confirm_password:
            messages.error(request, '❌ Tous les champs sont requis.')
            return redirect('users:change_password_html')
        
        if new_password != confirm_password:
            messages.error(request, '❌ Les mots de passe ne correspondent pas.')
            return redirect('users:change_password_html')
        
        if len(new_password) < 8:
            messages.error(request, '❌ Le mot de passe doit contenir au moins 8 caractères.')
            return redirect('users:change_password_html')
        
        # Check old password
        if not request.user.check_password(old_password):
            messages.error(request, '❌ L\'ancien mot de passe est incorrect.')
            return redirect('users:change_password_html')
        
        try:
            # Change password
            request.user.set_password(new_password)
            request.user.save()
            
            messages.success(request, '✅ Mot de passe modifié avec succès! Veuillez vous reconnecter.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'❌ Erreur: {str(e)}')
            return redirect('users:change_password_html')
