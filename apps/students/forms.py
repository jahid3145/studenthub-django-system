from django import forms
from django.contrib.auth import get_user_model
from .models import StudentProfile
from apps.academics.models import Department, Course

User = get_user_model()


class StudentCreateForm(forms.ModelForm):
    # User account fields
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. rahul.sharma'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'student@example.com'})
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Set Temporary Password'})
    )

    class Meta:
        model = StudentProfile
        fields = [
            'department', 'course', 'current_semester', 'gender',
            'phone', 'address', 'guardian_name', 'guardian_phone', 'status'
        ]
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'current_semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 8}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 9876543210'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full residential address'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent/Guardian Full Name'}),
            'guardian_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 9876543210'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        return email

    def save(self, commit=True):
        # First create the User
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            password=self.cleaned_data['password'],
            role=User.Role.STUDENT,
            phone=self.cleaned_data.get('phone')
        )

        # Create the StudentProfile
        student_profile = super().save(commit=False)
        student_profile.user = user
        if commit:
            student_profile.save()
        return student_profile


class StudentEditForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = StudentProfile
        fields = [
            'department', 'course', 'current_semester', 'gender',
            'phone', 'address', 'guardian_name', 'guardian_phone', 'status'
        ]
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'current_semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 8}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        student_profile = super().save(commit=False)
        user = student_profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data.get('phone')
        if commit:
            user.save()
            student_profile.save()
        return student_profile
