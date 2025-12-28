from django import forms
from django.utils.text import slugify
from .models import Shop


class ShopCreationForm(forms.ModelForm):
    """
    Form for creating a new shop.
    Handles validation and auto-slug generation.
    """
    
    class Meta:
        model = Shop
        fields = ['name', 'description', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nom de votre boutique',
                'required': True,
                'maxlength': '255',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Décrivez votre boutique et ce que vous vendez...',
                'rows': 5,
                'maxlength': '2000',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'contact@votreboutique.com',
                'type': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+213 XXX XX XX XX',
                'type': 'tel',
            }),
        }
    
    def clean_name(self):
        """Validate shop name."""
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError('Le nom de la boutique est requis.')
        if len(name) < 3:
            raise forms.ValidationError('Le nom de la boutique doit contenir au moins 3 caractères.')
        if len(name) > 255:
            raise forms.ValidationError('Le nom de la boutique ne peut pas dépasser 255 caractères.')
        return name
    
    def clean_description(self):
        """Validate shop description."""
        description = self.cleaned_data.get('description', '').strip()
        if description and len(description) < 10:
            raise forms.ValidationError('La description doit contenir au moins 10 caractères.')
        return description
    
    def clean_email(self):
        """Validate email."""
        email = self.cleaned_data.get('email', '').strip()
        if email and '@' not in email:
            raise forms.ValidationError('Veuillez entrer une adresse e-mail valide.')
        return email


class ShopUpdateForm(forms.ModelForm):
    """
    Form for updating shop details.
    """
    
    class Meta:
        model = Shop
        fields = ['name', 'description', 'logo', 'banner', 'email', 'phone', 'address', 'city', 'country']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nom de votre boutique',
                'maxlength': '255',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Décrivez votre boutique...',
                'rows': 5,
            }),
            'logo': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*',
            }),
            'banner': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'contact@votreboutique.com',
                'type': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+213 XXX XX XX XX',
                'type': 'tel',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Adresse',
                'maxlength': '255',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ville',
                'maxlength': '100',
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Pays',
                'maxlength': '100',
            }),
        }
    
    def clean_name(self):
        """Validate shop name."""
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError('Le nom de la boutique est requis.')
        if len(name) < 3:
            raise forms.ValidationError('Le nom de la boutique doit contenir au moins 3 caractères.')
        return name
