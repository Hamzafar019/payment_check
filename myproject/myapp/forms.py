from django import forms
from .models import Student, Organization, Subscription, OrganizationSubscription
from django.contrib.auth.models import User

class OrganizationSubscriptionForm(forms.ModelForm):
    class Meta:
        model = OrganizationSubscription
        fields = ['subscription', 'date_of_subscription']
        widgets = {
            'date_of_subscription': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subscription'].queryset = Subscription.objects.all()
        

class OrganizationSignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    name = forms.CharField(label='Organization Name', max_length=255)
    address = forms.CharField(label='Address', widget=forms.Textarea)
    contact_email = forms.EmailField(label='Contact Email')  





class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'description', 'price']

class StudentCreationForm(forms.ModelForm):
    # Additional fields for user registration
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    organization = forms.ModelChoiceField(queryset=Organization.objects.all(), required=False, disabled=True)
    enrollment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Student
        fields = ['name', 'email', 'password', 'organization', 'enrollment_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs:
            initial = kwargs['initial']
            if 'organization' in initial:
                organization_name = initial['organization']
                organization_instance = Organization.objects.filter(name=organization_name).first()
                if organization_instance:
                    self.fields['organization'].initial = organization_instance
