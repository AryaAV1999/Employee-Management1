from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    profile_pic=models.ImageField(upload_to="profile_pics",null=True)
    bio=models.CharField(max_length=120)
    phone=models.CharField(max_length=15)
    date_of_birth=models.DateField(null=True)
    options=(
        ("male", "male"),
        ("female", "female"),
        ("other", "other")
    )
    gender=models.CharField(max_length=12,choices=options,default="male")
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="users")

class JobDescription(models.Model):
    Name=models.CharField(max_length=120)
    description=models.CharField(max_length=230)
    Created_Date=models.DateField()
    Updated_Date=models.DateField()
    Unique_id=models.IntegerField()


def __str__(self):
    return self.title


class Comments(models.Model):
    job=models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    comment=models.CharField(max_length=160)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
