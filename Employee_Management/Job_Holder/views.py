from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from Job_Holder.forms import UserRegistrationForm,LoginForm,UserProfileForm,PasswordRestForm,JobForm,CommentForm,ProfilePicUpdateForm
from django.views.generic import View,CreateView,FormView,TemplateView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from Job_Holder.models import UserProfile,JobDescription,Comments
from django.contrib import messages



class SignUpView(CreateView):
    form_class = UserRegistrationForm
    template_name = "registration.html"
    model = User
    success_url = reverse_lazy("signup")





class LoginView(FormView):
    model=User
    template_name = "login.html"
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)

            if user:
                print("success")
                login(request,user)
                return redirect("home")
            else:
                return render(request,self.template_name,{"form":form})


def SignOut(request,*args,**kwargs):
    logout(request)
    return redirect("signin")



class IndexView(CreateView):
    form_class = JobForm
    model = JobDescription
    template_name = "home.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author=self.request.user
        self.object = form.save()
        messages.success(self.request,"post has been saved")
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        job=JobDescription.objects.all()
        context["jobs"]=job
        comment_form=CommentForm()
        context["comment_form"]=comment_form
        return context

    # def get_context_data(self,**kwargs):
    #     context=super().get_context_data(**kwargs)
    #     context["form"]=BlogForm()
    #     return context


class CreateUserProfileView(CreateView):
    model = UserProfile
    template_name = "addprofile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("home")

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST,files=request.FILES)
        if form.is_valid():
            form.instance.user =request.user
            form.save()
            messages.success(self.request,"profile has been created")
            return redirect("home")
        else:
            return render(request,self.template_name,{"form":form})

    # def form_valid(self, form):
    #     form.instance.user=self.request.user
    #     messages.success(self.request,"profile has been created")
    #     self.object=form.save()
    #     return super().form_valid(form)




class ViewMyProfileView(TemplateView):
    template_name = "view-profile.html"



class PasswordResetView(FormView):
    template_name="passwordreset.html"
    form_class=PasswordRestForm

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            oldpassword=form.cleaned_data.get("old_password")
            password1=form.cleaned_data.get("new_password")
            password2=form.cleaned_data.get("confirm_password")
            user=authenticate(request,username=request.user.username,password=oldpassword)

            if user:
                user.set_password(password2)
                user.save()
                messages.success(request,"password changed")
                return redirect("signin")
            else:
                messages.error(request,"invalid credentials")
                return render(request,self.template_name,{"form":form})


class ProfileUpdateView(UpdateView):
    form_class = UserProfileForm
    template_name = "profile-update.html"
    model = UserProfile
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"

    def form_valid(self, form):
        messages.success(self.request,"Your profile has been successfully updated")
        self.object=form.save()
        return super().form_valid(form)



def add_comment(request,*args,**kwargs):
    if request.method=='POST':
        blog_id=kwargs.get('post_id')
        blog=JobDescription.objects.get(id=blog_id)
        user=request.user
        comments=request.POST.get('comment')
        Comments.objects.create(blog=blog,comment=comments,user=user)
        messages.success(request,"Comment has been posted")
        return redirect('home')


class ProfilePicUpdateView(UpdateView):
    form_class = ProfilePicUpdateForm
    template_name = "profile-update.html"
    model = UserProfile
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"
    def form_valid(self, form):
        messages.success(self.request,"Profile pic has been updated")
        self.object=form.save()
        return super().form_valid(form)


def add_like(request,*args,**kwargs):
    blog_id=kwargs.get('post_id')
    blog=JobDescription.objects.get(id=blog_id)
    blog.liked_by.add(request.user)
    blog.save()
    return redirect("home")


class ProfileEditView(UpdateView):
    form_class = UserProfileForm
    template_name = "profile-edit.html"
    model = UserProfile
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"

    def form_valid(self, form):
        messages.success(self.request,"Your profile has been successfully edited")
        self.object=form.save()
        return super().form_valid(form)













