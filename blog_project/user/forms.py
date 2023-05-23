from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile

class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email'] 
        
class UpdateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['photo','about_me','date_of_birth' ]