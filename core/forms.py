from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Issue, IssueType, Location, Comment, Resolution, UserProfile


class IssueForm(forms.ModelForm):
    """Form for creating a new issue report"""
    
    # Custom validators
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    # Custom fields with validators
    reporter_phone = forms.CharField(
        validators=[phone_regex], 
        max_length=17, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )
    
    # Override the default widget for incident_date to use the date input
    incident_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = Issue
        fields = [
            'issue_type', 'location', 'title', 'description', 
            'reporter_name', 'reporter_email', 'reporter_phone', 
            'incident_date', 'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the issue in detail...'}),
            'reporter_name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'reporter_email': forms.EmailInput(attrs={'placeholder': 'Your email'}),
            'title': forms.TextInput(attrs={'placeholder': 'Brief title of the issue'})
        }
    
    def clean_reporter_email(self):
        """Validate that the email contains @"""
        email = self.cleaned_data.get('reporter_email')
        if email and '@' not in email:
            raise forms.ValidationError("Please enter a valid email address with an @ symbol.")
        return email
    
    def clean_description(self):
        """Validate that the description is descriptive enough"""
        description = self.cleaned_data.get('description')
        print(f"Validating description: '{description}', word count: {len(description.split() if description else [])}")
        if description and len(description.split()) < 5:
            print("Validation failed: less than 5 words")
            raise forms.ValidationError("Please provide a more detailed description (at least 5 words).")
        return description


class IssueUpdateForm(forms.ModelForm):
    """Form for authorities to update an existing issue"""
    
    class Meta:
        model = Issue
        fields = ['status', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_status(self):
        """Validate that status transitions are logical"""
        status = self.cleaned_data.get('status')
        initial_status = self.instance.status if self.instance else None
        
        # Example validation: can't go directly from 'pending' to 'resolved' without 'in_progress'
        if initial_status == 'pending' and status == 'resolved':
            raise forms.ValidationError(
                "Issues must be marked 'in progress' before they can be resolved."
            )
            
        return status


class CommentForm(forms.ModelForm):
    """Form for adding comments to an issue"""
    
    class Meta:
        model = Comment
        fields = ['comment_text', 'author_name', 'author_email']
        widgets = {
            'comment_text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
            'author_name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'author_email': forms.EmailInput(attrs={'placeholder': 'Your email'})
        }
    
    def clean_comment_text(self):
        """Validate that the comment isn't empty or too short"""
        text = self.cleaned_data.get('comment_text')
        if text and len(text.strip()) < 10:
            raise forms.ValidationError("Please provide a more detailed comment (at least 10 characters).")
        return text


class LocationForm(forms.ModelForm):
    """Form for adding a new location"""
    
    class Meta:
        model = Location
        fields = ['name', 'address', 'latitude', 'longitude']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Location name (e.g., City Park)'}),
            'address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Full address'}),
            'latitude': forms.NumberInput(attrs={'placeholder': 'Optional: e.g., 37.7749', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'placeholder': 'Optional: e.g., -122.4194', 'step': '0.000001'})
        }
    
    def clean(self):
        """Validate that either address is provided or both lat/long"""
        cleaned_data = super().clean()
        address = cleaned_data.get('address')
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')
        
        if not address and not (latitude and longitude):
            raise forms.ValidationError(
                "Please provide either an address or both latitude and longitude."
            )
            
        return cleaned_data


class ResolutionForm(forms.ModelForm):
    """Form for marking an issue as resolved with details"""
    
    class Meta:
        model = Resolution
        fields = ['resolution_details', 'before_image', 'after_image', 'featured']
        widgets = {
            'resolution_details': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Describe how this issue was resolved...'}
            ),
        }
    
    def clean_resolution_details(self):
        """Validate that resolution details are provided"""
        details = self.cleaned_data.get('resolution_details')
        if details and len(details.strip()) < 10:
            raise forms.ValidationError("Please provide more details about the resolution (at least 10 characters).")
        return details


class IssueDeleteConfirmForm(forms.Form):
    """Form to confirm deletion of an issue"""
    
    confirm = forms.BooleanField(
        required=True,
        label="I understand this action cannot be undone",
        error_messages={'required': 'You must confirm the deletion'}
    )
    
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Why is this issue being removed?'}),
        required=True
    )
    
    def clean_reason(self):
        reason = self.cleaned_data.get('reason')
        if reason and len(reason.strip()) < 10:
            raise forms.ValidationError("Please provide a more detailed reason (at least 10 characters).")
        return reason
    


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'address')
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your address'}),
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ('username', 'email')

