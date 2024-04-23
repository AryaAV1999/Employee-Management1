from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from Job_Holder.models import UserProfile,JobDescription,Comments
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=[
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2"
        ]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())


class UserProfileForm(ModelForm):
    class Meta:
        model=UserProfile
        exclude=("user",)
        # widget={
        #     "date_of_birth":forms.DateInput(attrs={"class":"form-control","type":"date"})
        # }



class PasswordRestForm(forms.Form):
    old_password=forms.CharField(widget=forms.PasswordInput)
    new_password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField()




class JobForm(ModelForm):
    class Meta:
        model=JobDescription
        fields=["Name",
                "description",
                "Created_Date",
                "Updated_Date",
                "Unique_id"]
        widgets={
            "Name":forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control"}),
            "Created_Date":forms.DateInput(attrs={"class":"form-control"}),
            "Updated_Date": forms.DateInput(attrs={"class": "form-control"}),
            "Unique_id": forms.TextInput(attrs={"class": "form-control"}),

        }


class CommentForm(ModelForm):
    class Meta:
        model=Comments
        fields=["comment"]

class ProfilePicUpdateForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=[
            "profile_pic"
        ]
        widgets={
            "profile_pic":forms.FileInput(attrs={'class':'form-control'})
        }

