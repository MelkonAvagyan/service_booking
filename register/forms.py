from django import forms
f#rom django.forms import fields
#from django.contrib.auth.forms import UserCreationForm
from .models import User, Client, Specialist
from django.db import transaction
from django.contrib.auth import authenticate, login, get_user_model
#from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.safestring import mark_safe
from django.contrib import messages


User = get_user_model()
# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = '__all__'


class ClientRegisterForm(forms.ModelForm):

    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'placeholder': 'Enter First Name'}), max_length=32)
    last_name=forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name'}), max_length=32)
    email=forms.EmailField(max_length=50, widget=(forms.TextInput(attrs={'placeholder': 'Enter a valid email address','class': 'form-control'})))
    phone_number=forms.CharField(label='Phone number', widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}))
    password1=forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Set Password'}))
    password2=forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))

    class Meta:
        model = User
        #fields = '__all__'
    
    def clean_password2(self):
        
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


    @transaction.atomic

    def save(self):
        user = super().save(commit=False)
        user.is_client = True
        user.username = self.cleaned_data.get('username')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.password = self.cleaned_data.get('password1')
        user.save()
        client = Client.objects.create(user=user)
        client.phone_number=self.cleaned_data.get('phone_number')
        client.email=self.cleaned_data.get('email')
        client.save()
        return user


class SpecialistRegisterForm(forms.ModelForm): #UserCreationForm

    categories = (
	('Self&Beauty Care', 'SELF&BEAUTY CARE'),
	('Education','EDUCATION'),
	('Software Services', 'SOFTWARE SERVICES'),
	('Home Services', 'HOME SERVICES'),
	('Handmade Products', 'HANDMADE PRODUCTS'),)

	job_type = (	
	('self employed', 'Self Employed'),
	('employee', 'Employee'),
	('both', 'both'),)

	handling = (
		('delivery', 'delivery'),
		('in place', 'in place'),
		('both','both'),)

    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'placeholder': 'Enter First Name'}), max_length=32)
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name'}), max_length=32)
    email = forms.EmailField(max_length=50, widget=(forms.TextInput(attrs={'placeholder': 'Enter a valid email address','class': 'form-control'})))
    phone_number = forms.CharField(label='Phone number', widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}))
    category = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices = categories)
    job_type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices = job_type)
    company_name = forms.CharField(label='Phone number', widget=forms.TextInput(attrs={'placeholder': 'Enter company name'}))
    handling = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=handling)
    address = forms.CharField(label='Address', widget=forms.TextInput(attrs={'placeholder': 'Please mention your address'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Set Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))


    class Meta:
        model = User
        #fields = '__all__'

    def clean_password2(self):
        
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_specialist = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.password = self.cleaned_data.get('password1')
        user.save()
        specialist = Specialist.objects.create(user=user)
        specialist.phone_number = self.cleaned_data.get('phone_number')
        specialist.email = self.cleaned_data.get('email')
        specialist.category = self.cleaned_data.get('category')
        specialist.job_type = self.cleaned_data.get('job_type')
        specialist.company_name = self.cleaned_data.get('company_name')
        specialist.handling = self.cleaned_data.get('handling')
        specialist.address = self.cleaned_data.get('address')
        specialist.save()
        return user
        

class LoginForm(forms.Form):  #AuthenticationFoorm
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username  = self.cleaned_data.get("username")
        password  = self.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid credentials")
        else:
            if user.is_active:
                login(self.request, user)
                self.user = user
                return self.cleaned_data
            else:
                messages.error(self.request,"The password is valid, but the account has been disabled!")










    # def __init__(self, *args, **kwargs):
    #     super(SpecialistRegisterForm, self).__init__(*args, **kwargs)

    #     for name, field in self.fields.items():
    #         field.widget.attrs.update({'class': 'input'})
