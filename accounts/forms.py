"""
AEGISAI – accounts/forms.py
Forms aligned with the new schema models.
"""

import re
import os

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth.models import User

from .models import (
    PoliceRegister,
    CyberCrimeReport, FileData, Feedback,
)


# ─────────────────────────────────────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────────────────────────────────────

def _validate_password(password):
    """Shared password rules."""
    if len(password) < 6:
        raise forms.ValidationError('Password must be at least 6 characters.')
    if not re.search(r'[a-zA-Z]', password):
        raise forms.ValidationError('Password must contain at least one letter.')
    if not re.search(r'[0-9]', password):
        raise forms.ValidationError('Password must contain at least one number.')
    return password


# ─────────────────────────────────────────────────────────────────────────────
# USER REGISTRATION
# ─────────────────────────────────────────────────────────────────────────────

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'First Name',
        'class': 'form-control',
    }))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Last Name',
        'class': 'form-control',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address',
        'class': 'form-control',
    }))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
    }))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        # For default User model, username is required. We use email as username.
        user.username = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


# ─────────────────────────────────────────────────────────────────────────────
# POLICE REGISTRATION
# ─────────────────────────────────────────────────────────────────────────────

class PoliceRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'First Name',
        'class': 'form-control',
    }))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Last Name',
        'class': 'form-control',
    }))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Phone Number',
        'class': 'form-control',
    }))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
    }))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control',
    }))

    class Meta:
        model = PoliceRegister
        fields = ['email', 'badge_number']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address',
                'class': 'form-control',
            }),
            'badge_number': forms.TextInput(attrs={
                'placeholder': 'Badge Number',
                'class': 'form-control',
            }),
        }

    def clean_password1(self):
        return _validate_password(self.cleaned_data.get('password1'))

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get('password1')
        pw2 = cleaned_data.get('password2')
        if pw1 and pw2 and pw1 != pw2:
            self.add_error('password2', 'Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        officer = super().save(commit=False)
        officer.firstname = self.cleaned_data.get('first_name')
        officer.lastname = self.cleaned_data.get('last_name')
        # phone_number is not in model, so we skip saving it unless I modify the model (which the user restricted)
        officer.password = make_password(self.cleaned_data['password1'])
        if commit:
            officer.save()
        return officer


# ─────────────────────────────────────────────────────────────────────────────
# USER LOGIN FORM
# ─────────────────────────────────────────────────────────────────────────────

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address',
        'class': 'form-control',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
    }))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            from django.contrib.auth import authenticate
            # Find user by email first, as username might not be exactly equal to email in all cases
            # though UserRegisterForm sets them same.
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
            
            if user is None:
                raise forms.ValidationError('Invalid email or password.')
            cleaned_data['user_obj'] = user
        return cleaned_data


# ─────────────────────────────────────────────────────────────────────────────
# POLICE LOGIN FORM
# ─────────────────────────────────────────────────────────────────────────────

class PoliceLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address',
        'class': 'form-control',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
    }))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            try:
                officer = PoliceRegister.objects.get(email=email)
            except PoliceRegister.DoesNotExist:
                raise forms.ValidationError('Invalid email or password.')
            if not check_password(password, officer.password):
                raise forms.ValidationError('Invalid email or password.')
            cleaned_data['user_obj'] = officer
        return cleaned_data


# ─────────────────────────────────────────────────────────────────────────────
# ADMIN LOGIN FORM  (validates against Django CustomUser / superuser)
# ─────────────────────────────────────────────────────────────────────────────

class AdminLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address',
        'class': 'form-control',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
    }))

    def clean(self):
        from django.contrib.auth import authenticate
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            try:
                admin_user = User.objects.get(email=email)
                user = authenticate(username=admin_user.username, password=password)
            except User.DoesNotExist:
                user = None

            if user is None or not user.is_superuser:
                raise forms.ValidationError('Invalid admin credentials.')
            cleaned_data['user_obj'] = user
        return cleaned_data


# ─────────────────────────────────────────────────────────────────────────────
# UPDATE PROFILE (USER)
# ─────────────────────────────────────────────────────────────────────────────

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'First Name',
        'class': 'form-control',
    }))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Last Name',
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address',
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Model mapping not needed if using standard User model.

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


# ─────────────────────────────────────────────────────────────────────────────
# CHANGE PASSWORD
# ─────────────────────────────────────────────────────────────────────────────

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Current Password',
        'class': 'form-control',
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'New Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm New Password',
        'class': 'form-control',
    }))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current = self.cleaned_data.get('current_password')
        if not check_password(current, self.user.password):
            raise forms.ValidationError('Current password is incorrect.')
        return current

    def clean_new_password(self):
        return _validate_password(self.cleaned_data.get('new_password'))

    def clean(self):
        cleaned_data = super().clean()
        new_pw = cleaned_data.get('new_password')
        confirm = cleaned_data.get('confirm_password')
        if new_pw and confirm and new_pw != confirm:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data

    def save(self):
        self.user.password = make_password(self.cleaned_data['new_password'])
        self.user.save()
        return self.user


# ─────────────────────────────────────────────────────────────────────────────
# FEEDBACK FORM  (maps to FEEDBACK table)
# ─────────────────────────────────────────────────────────────────────────────

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'experience', 'rating', 'comments']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Name',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your Email',
                'class': 'form-control',
            }),
            'experience': forms.Textarea(attrs={
                'placeholder': 'Describe your experience…',
                'class': 'form-control',
                'rows': 4,
            }),
            'rating': forms.Select(attrs={
                'class': 'form-control',
            }),
            'comments': forms.Textarea(attrs={
                'placeholder': 'Additional comments (optional)…',
                'class': 'form-control',
                'rows': 3,
            }),
        }


# ─────────────────────────────────────────────────────────────────────────────
# CYBER CRIME REPORT FORM  (maps to CYBER_CRIME_REPORT table)
# ─────────────────────────────────────────────────────────────────────────────

class CyberCrimeReportForm(forms.ModelForm):
    class Meta:
        model = CyberCrimeReport
        fields = ['title', 'crime_type', 'description', 'evidence_details']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Report Title',
                'class': 'form-control',
            }),
            'crime_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe the incident in detail…',
                'class': 'form-control',
                'rows': 5,
            }),
            'evidence_details': forms.Textarea(attrs={
                'placeholder': 'Provide links or additional information…',
                'class': 'form-control',
                'rows': 3,
            }),
        }


# ─────────────────────────────────────────────────────────────────────────────
# FILE SHARE FORM  (maps to FILEDATA table)
# ─────────────────────────────────────────────────────────────────────────────

ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.pdf', '.txt']
BLOCKED_EXTENSIONS = ['.exe', '.bat', '.js']


class FileShareForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(
        queryset=User.objects.none(),
        empty_label='-- Select a user --',
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Send To',
    )

    class Meta:
        model = FileData
        fields = ['receiver', 'file', 'message']
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.png,.jpg,.jpeg,.pdf,.txt',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Optional message to the recipient…',
                'class': 'form-control',
                'rows': 3,
            }),
        }

    def __init__(self, *args, current_user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if current_user is not None:
            self.fields['receiver'].queryset = User.objects.filter(
                is_superuser=False, is_staff=False
            ).exclude(pk=current_user.pk).order_by('first_name', 'last_name')

    def clean_file(self):
        uploaded = self.cleaned_data.get('file')
        if not uploaded:
            raise forms.ValidationError('Please select a file to share.')
        ext = os.path.splitext(uploaded.name)[1].lower()
        if ext in BLOCKED_EXTENSIONS:
            raise forms.ValidationError(
                f'File type "{ext}" is blocked. Executable and script files are not permitted.'
            )
        if ext not in ALLOWED_EXTENSIONS:
            raise forms.ValidationError(
                f'File type "{ext}" is not allowed. Accepted types: {", ".join(ALLOWED_EXTENSIONS)}'
            )
        if uploaded.size > 10 * 1024 * 1024:
            raise forms.ValidationError('File size cannot exceed 10 MB.')
        return uploaded


# ─────────────────────────────────────────────────────────────────────────────
# LEGACY alias — keeps any template/view that still imports LoginForm working
# ─────────────────────────────────────────────────────────────────────────────
# Re-import for other forms that still need them
from .models import (
    PoliceRegister,
    CyberCrimeReport, FileData, Feedback,
)

LoginForm = UserLoginForm
